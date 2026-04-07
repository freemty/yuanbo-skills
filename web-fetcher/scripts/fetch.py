#!/usr/bin/env python3
"""Unified web fetcher: platform-specific routing + generic fallback chain.

Platform routing (tried first):
  Twitter/X -> xreach, YouTube/Bilibili -> yt-dlp,
  XiaoHongShu -> mcporter, GitHub issue/PR -> gh

Generic fallback chain:
  Jina Reader -> defuddle.md -> markdown.new -> OpenCLI -> Raw HTML

Usage:
    python3 fetch.py <url> [--output <file>]
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.request


UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"


def _run(cmd: list[str], timeout: int = 30) -> str:
    """Run a subprocess and return stdout. Raises on failure."""
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or f"exit code {result.returncode}")
    out = result.stdout.strip()
    if not out:
        raise RuntimeError("empty output")
    return out

# URL pattern → (opencli command, args extractor)
# Each entry: (regex, opencli_subcommand_list_fn)
OPENCLI_ROUTES = [
    # zhihu question: zhihu.com/question/12345
    (r"zhihu\.com/question/(\d+)", lambda m: ["zhihu", "question", m.group(1)]),
    # zhihu article: zhuanlan.zhihu.com/p/12345
    (r"zhuanlan\.zhihu\.com/p/(\d+)", lambda m: ["zhihu", "download", f"https://zhuanlan.zhihu.com/p/{m.group(1)}"]),
    # reddit post: reddit.com/r/xxx/comments/xxx
    (r"reddit\.com/r/\w+/comments/", lambda m: ["reddit", "read", m.string]),
    # twitter/x thread (fallback when xreach unavailable — Phase 1 tries xreach first)
    (r"(twitter\.com|x\.com)/\w+/status/(\d+)", lambda m: ["twitter", "thread", m.group(2)]),
    # weibo
    (r"weibo\.com/\d+/(\w+)", lambda m: ["weibo", "search", m.group(0)]),
]


PROXY = os.environ.get("HTTP_PROXY", os.environ.get("http_proxy", "http://127.0.0.1:7890"))


def fetch_via_xreach(url: str, match: re.Match) -> str:
    """Fetch a tweet via xreach CLI → markdown."""
    raw = _run(["xreach", "tweet", url, "--json", "--proxy", PROXY])
    data = json.loads(raw)
    tweet = data[0] if isinstance(data, list) else data
    user = tweet.get("user", {})
    name = user.get("name", "Unknown")
    handle = user.get("screenName", "")
    text = tweet.get("text", "")
    created = tweet.get("createdAt", "")
    likes = tweet.get("likeCount", 0)
    retweets = tweet.get("retweetCount", 0)
    media = tweet.get("media", [])

    lines = [
        f"# Tweet by {name} (@{handle})",
        f"> {created} | Likes: {likes} | Retweets: {retweets}",
        "",
        text,
    ]
    for m in media:
        media_url = m.get("url", "")
        if media_url:
            lines.append(f"\n![media]({media_url})")
    return "\n".join(lines)


def fetch_via_ytdlp(url: str, match: re.Match) -> str:
    """Fetch video metadata via yt-dlp → markdown."""
    raw = _run(["yt-dlp", "--dump-json", "--no-warnings", url], timeout=60)
    data = json.loads(raw)
    title = data.get("title", "Untitled")
    uploader = data.get("uploader", "Unknown")
    upload_date = data.get("upload_date", "")
    if upload_date and len(upload_date) == 8:
        upload_date = f"{upload_date[:4]}-{upload_date[4:6]}-{upload_date[6:]}"
    duration = data.get("duration") or 0
    view_count = data.get("view_count") or 0
    description = data.get("description", "")
    webpage_url = data.get("webpage_url", url)

    mins, secs = divmod(int(duration), 60)
    hours, mins = divmod(mins, 60)
    dur_str = f"{hours}:{mins:02d}:{secs:02d}" if hours else f"{mins}:{secs:02d}"

    lines = [
        f"# {title}",
        f"> {uploader} | {upload_date} | {dur_str} | Views: {view_count:,}",
        f"> URL: {webpage_url}",
        "",
    ]
    if description:
        lines.append(description)
    return "\n".join(lines)


def fetch_via_mcporter(url: str, match: re.Match) -> str:
    """Fetch XiaoHongShu note via mcporter → markdown."""
    # Resolve xhs.link short URLs to full xiaohongshu.com URLs
    if "xhs.link" in url:
        req = urllib.request.Request(url, headers={"User-Agent": UA}, method="HEAD")
        with urllib.request.urlopen(req, timeout=10) as resp:
            url = resp.url
    feed_match = re.search(r"xiaohongshu\.com/(?:explore|discovery/item)/([a-f0-9]+)", url)
    if not feed_match:
        raise RuntimeError(f"cannot extract feed_id from {url}")
    feed_id = feed_match.group(1)
    return _run(["mcporter", "call", f'xiaohongshu.get_feed_detail(feed_id: "{feed_id}")'])


def fetch_via_gh(url: str, match: re.Match) -> str:
    """Fetch GitHub issue/PR via gh CLI → markdown."""
    gh_match = re.search(r"github\.com/([^/]+/[^/]+)/(issues|pull)/(\d+)", url)
    if not gh_match:
        raise RuntimeError(f"cannot parse GitHub URL: {url}")
    repo = gh_match.group(1)
    kind = gh_match.group(2)
    number = gh_match.group(3)
    cmd_type = "issue" if kind == "issues" else "pr"
    return _run(["gh", cmd_type, "view", number, "-R", repo])


# (url_regex, tool_binary_name, handler_fn)
PLATFORM_ROUTES = [
    (r"(twitter\.com|x\.com)/\w+/status/\d+", "xreach", fetch_via_xreach),
    (r"(youtube\.com/watch|youtu\.be/|youtube\.com/shorts/)", "yt-dlp", fetch_via_ytdlp),
    (r"bilibili\.com/video/", "yt-dlp", fetch_via_ytdlp),
    (r"(xiaohongshu\.com/(explore|discovery/item)/|xhs\.link/)", "mcporter", fetch_via_mcporter),
    (r"github\.com/[^/]+/[^/]+/(issues|pull)/\d+", "gh", fetch_via_gh),
]


def fetch_url(url: str, headers: dict | None = None, timeout: int = 30) -> str:
    h = {"User-Agent": UA}
    if headers:
        h.update(headers)
    req = urllib.request.Request(url, headers=h)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="replace")


def fetch_via_jina(target: str) -> str:
    return fetch_url(
        f"https://r.jina.ai/{target}",
        headers={"Accept": "text/markdown"},
    )


def fetch_via_defuddle(target: str) -> str:
    return fetch_url(f"https://defuddle.md/{target}")


def fetch_via_markdown_new(target: str) -> str:
    return fetch_url(f"https://markdown.new/{target}")


def fetch_via_opencli(target: str) -> str:
    if not shutil.which("opencli"):
        raise RuntimeError("opencli not installed")
    for pattern, args_fn in OPENCLI_ROUTES:
        m = re.search(pattern, target)
        if m:
            cmd = ["opencli"] + args_fn(m)
            print(f"  → {' '.join(cmd)}", file=sys.stderr)
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout
            raise RuntimeError(result.stderr.strip() or f"exit code {result.returncode}")
    raise RuntimeError(f"no opencli route for {target}")


def fetch_raw(target: str) -> str:
    return fetch_url(target)


STRATEGIES = [
    ("Jina Reader", fetch_via_jina),
    ("defuddle.md", fetch_via_defuddle),
    ("markdown.new", fetch_via_markdown_new),
    ("OpenCLI", fetch_via_opencli),
    ("Raw HTML", fetch_raw),
]


MIN_CONTENT_LEN = 500  # skip results that are too short (likely error pages)


def fetch(target: str) -> str:
    errors = []

    # Phase 1: platform-specific handlers
    for pattern, tool_bin, handler in PLATFORM_ROUTES:
        m = re.search(pattern, target)
        if m:
            if not shutil.which(tool_bin):
                msg = f"{tool_bin} not installed, skipping"
                print(f"[{tool_bin}] {msg}", file=sys.stderr)
                errors.append((tool_bin, msg))
                break  # fall through to generic chain
            try:
                name = handler.__name__.replace("fetch_via_", "")
                print(f"[{name}] Fetching...", file=sys.stderr)
                content = handler(target, m)
                print(f"[{name}] Success ({len(content)} chars)", file=sys.stderr)
                return content
            except Exception as e:
                print(f"[{handler.__name__}] Failed: {e}", file=sys.stderr)
                errors.append((handler.__name__, str(e)))
                break  # fall through to generic chain

    # Phase 2: generic fallback chain (Jina, defuddle, markdown.new, OpenCLI, raw)
    for name, fn in STRATEGIES:
        try:
            print(f"[{name}] Fetching...", file=sys.stderr)
            content = fn(target)
            if len(content) < MIN_CONTENT_LEN:
                msg = f"too short ({len(content)} chars), likely error page"
                print(f"[{name}] Skipped: {msg}", file=sys.stderr)
                errors.append((name, msg))
                continue
            print(f"[{name}] Success ({len(content)} chars)", file=sys.stderr)
            return content
        except Exception as e:
            print(f"[{name}] Failed: {e}", file=sys.stderr)
            errors.append((name, str(e)))

    raise RuntimeError(
        "All strategies failed:\n"
        + "\n".join(f"  - {name}: {err}" for name, err in errors)
    )


def main():
    parser = argparse.ArgumentParser(description="Fetch web page content as text")
    parser.add_argument("url", help="Target URL to fetch")
    parser.add_argument("-o", "--output", help="Output file (default: stdout)")
    args = parser.parse_args()

    try:
        content = fetch(args.url)
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Saved to {args.output}", file=sys.stderr)
    else:
        print(content)


if __name__ == "__main__":
    main()
