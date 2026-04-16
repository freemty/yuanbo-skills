#!/usr/bin/env python3
"""Unified web fetcher: platform-specific routing + generic fallback chain.

Platform routing (tried first):
  Twitter/X -> xreach (single/thread) -> opencli twitter -> Thread Reader App
  YouTube/Bilibili -> yt-dlp (metadata + subtitles)
  XiaoHongShu -> mcporter
  GitHub issue/PR -> gh
  知乎 -> opencli zhihu
  Reddit -> opencli reddit
  arXiv -> opencli arxiv
  HackerNews -> opencli hackernews
  微博 -> opencli weibo

Generic fallback chain:
  Jina Reader -> markdown.new -> OpenCLI -> Raw HTML

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


PROXY = os.environ.get("HTTP_PROXY", os.environ.get("http_proxy", "http://127.0.0.1:7890"))


def fetch_url(url: str, headers: dict | None = None, timeout: int = 30) -> str:
    h = {"User-Agent": UA}
    if headers:
        h.update(headers)
    req = urllib.request.Request(url, headers=h)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="replace")


def _format_tweet(tweet: dict) -> str:
    """Format a single tweet dict to markdown."""
    user = tweet.get("user", {})
    name = user.get("name", "Unknown")
    handle = user.get("screenName", "")
    text = tweet.get("text", "")
    created = tweet.get("createdAt", "")
    likes = tweet.get("likeCount", 0)
    retweets = tweet.get("retweetCount", 0)
    media = tweet.get("media", [])

    lines = [
        f"## {name} (@{handle})",
        f"> {created} | Likes: {likes} | Retweets: {retweets}",
        "",
        text,
    ]
    for m in media:
        media_url = m.get("url", "")
        if media_url:
            lines.append(f"\n![media]({media_url})")
    return "\n".join(lines)


def fetch_via_xreach(url: str, match: re.Match) -> str:
    """Fetch a tweet via xreach CLI → markdown. Tries thread first, falls back to single."""
    # Try thread first (gets full conversation context)
    try:
        raw = _run(["xreach", "thread", url, "--json", "--proxy", PROXY], timeout=45)
        data = json.loads(raw)
        tweets = data if isinstance(data, list) else [data]
        if len(tweets) > 1:
            parts = [f"# Thread ({len(tweets)} tweets)"]
            for t in tweets:
                parts.append(_format_tweet(t))
            return "\n\n---\n\n".join(parts)
        return f"# Tweet\n\n{_format_tweet(tweets[0])}"
    except Exception as thread_err:
        print(f"[xreach thread] Failed: {thread_err}, trying single tweet", file=sys.stderr)

    # Fallback to single tweet
    raw = _run(["xreach", "tweet", url, "--json", "--proxy", PROXY])
    data = json.loads(raw)
    tweet = data[0] if isinstance(data, list) else data
    return f"# Tweet\n\n{_format_tweet(tweet)}"


def fetch_via_ytdlp(url: str, match: re.Match) -> str:
    """Fetch video metadata + subtitles via yt-dlp → markdown."""
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

    # Try to fetch subtitles for richer content
    subtitles = data.get("subtitles", {})
    auto_captions = data.get("automatic_captions", {})
    sub_langs = subtitles or auto_captions
    if sub_langs:
        # Prefer zh/en manual subs, then auto captions
        for lang in ["zh-Hans", "zh", "zh-CN", "en", "ja"]:
            subs = subtitles.get(lang) or auto_captions.get(lang)
            if subs:
                # Find a text-based format
                sub_url = None
                for fmt in subs:
                    if fmt.get("ext") in ("srv1", "vtt", "srt", "json3"):
                        sub_url = fmt.get("url")
                        break
                if sub_url:
                    try:
                        sub_text = fetch_url(sub_url, timeout=15)
                        # Strip timing info for readability (basic cleanup)
                        clean_lines = []
                        for line in sub_text.splitlines():
                            line = line.strip()
                            if not line or re.match(r"^\d+$", line) or re.match(r"\d{2}:\d{2}", line) or line.startswith("WEBVTT"):
                                continue
                            # Remove VTT tags
                            line = re.sub(r"<[^>]+>", "", line)
                            if line and line not in clean_lines[-1:]:
                                clean_lines.append(line)
                        if clean_lines:
                            lines.append(f"\n## Subtitles ({lang})\n")
                            lines.append("\n".join(clean_lines))
                    except Exception as e:
                        print(f"[subtitles] Failed to fetch {lang}: {e}", file=sys.stderr)
                break

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


def fetch_via_opencli_twitter(url: str, match: re.Match) -> str:
    """Fetch Twitter thread via opencli twitter thread → markdown."""
    tweet_id = match.group(2)
    # Try article first (long-form Twitter articles)
    try:
        return _run(["opencli", "twitter", "article", tweet_id, "-f", "md"], timeout=45)
    except Exception:
        pass
    # Fall back to thread
    return _run(["opencli", "twitter", "thread", tweet_id, "-f", "md"], timeout=45)


def fetch_via_threadreader(url: str, match: re.Match) -> str:
    """Fetch Twitter thread via Thread Reader App (threadreaderapp.com)."""
    tweet_id = match.group(2)
    reader_url = f"https://threadreaderapp.com/thread/{tweet_id}.html"
    return fetch_url(
        f"https://r.jina.ai/{reader_url}",
        headers={"Accept": "text/markdown"},
        timeout=30,
    )


def fetch_via_opencli_zhihu(url: str, match: re.Match) -> str:
    """Fetch 知乎 content via opencli zhihu."""
    if "zhuanlan.zhihu.com/p/" in url:
        article_match = re.search(r"zhuanlan\.zhihu\.com/p/(\d+)", url)
        if article_match:
            return _run(["opencli", "zhihu", "download", url, "-f", "md"], timeout=30)
    question_match = re.search(r"zhihu\.com/question/(\d+)", url)
    if question_match:
        return _run(["opencli", "zhihu", "question", question_match.group(1), "-f", "md"], timeout=30)
    raise RuntimeError(f"unsupported zhihu URL pattern: {url}")


def fetch_via_opencli_reddit(url: str, match: re.Match) -> str:
    """Fetch Reddit post via opencli reddit read."""
    return _run(["opencli", "reddit", "read", url, "-f", "md"], timeout=30)


def fetch_via_opencli_arxiv(url: str, match: re.Match) -> str:
    """Fetch arXiv paper details via opencli arxiv paper."""
    arxiv_id = match.group(1)
    return _run(["opencli", "arxiv", "paper", arxiv_id, "-f", "md"], timeout=30)


def fetch_via_opencli_hackernews(url: str, match: re.Match) -> str:
    """Fetch HackerNews story. Uses Jina on the HN URL for full discussion."""
    return fetch_url(
        f"https://r.jina.ai/{url}",
        headers={"Accept": "text/markdown"},
        timeout=30,
    )


def fetch_via_opencli_weibo(url: str, match: re.Match) -> str:
    """Fetch Weibo post via opencli weibo comments."""
    return _run(["opencli", "weibo", "comments", url, "-f", "md"], timeout=30)


# Platform routes: (url_regex, tool_binary_name, handler_fn)
# Order matters — first match wins. Multiple entries for same platform = fallback chain.
PLATFORM_ROUTES = [
    # Twitter/X: xreach (thread+single) → opencli twitter → Thread Reader App
    (r"(twitter\.com|x\.com)/\w+/status/(\d+)", "xreach", fetch_via_xreach),
    (r"(twitter\.com|x\.com)/\w+/status/(\d+)", "opencli", fetch_via_opencli_twitter),
    (r"(twitter\.com|x\.com)/\w+/status/(\d+)", None, fetch_via_threadreader),
    # YouTube / Bilibili
    (r"(youtube\.com/watch|youtu\.be/|youtube\.com/shorts/)", "yt-dlp", fetch_via_ytdlp),
    (r"bilibili\.com/video/", "yt-dlp", fetch_via_ytdlp),
    # 小红书
    (r"(xiaohongshu\.com/(explore|discovery/item)/|xhs\.link/)", "mcporter", fetch_via_mcporter),
    # GitHub issue/PR
    (r"github\.com/[^/]+/[^/]+/(issues|pull)/\d+", "gh", fetch_via_gh),
    # 知乎
    (r"(zhihu\.com/question/\d+|zhuanlan\.zhihu\.com/p/\d+)", "opencli", fetch_via_opencli_zhihu),
    # Reddit
    (r"reddit\.com/r/\w+/comments/", "opencli", fetch_via_opencli_reddit),
    # arXiv
    (r"arxiv\.org/(?:abs|pdf)/(\d+\.\d+)", "opencli", fetch_via_opencli_arxiv),
    # HackerNews
    (r"news\.ycombinator\.com/item\?id=\d+", None, fetch_via_opencli_hackernews),
    # 微博
    (r"weibo\.com/\d+/\w+", "opencli", fetch_via_opencli_weibo),
]


def fetch_via_jina(target: str) -> str:
    return fetch_url(
        f"https://r.jina.ai/{target}",
        headers={"Accept": "text/markdown"},
    )


def fetch_via_markdown_new(target: str) -> str:
    return fetch_url(f"https://markdown.new/{target}")


def fetch_raw(target: str) -> str:
    return fetch_url(target)


GENERIC_STRATEGIES = [
    ("Jina Reader", fetch_via_jina),
    ("markdown.new", fetch_via_markdown_new),
    ("Raw HTML", fetch_raw),
]


MIN_CONTENT_LEN = 500  # skip results that are too short (likely error pages)


def fetch(target: str) -> str:
    errors = []

    # Phase 1: platform-specific handlers (with per-platform fallback chain)
    # Multiple PLATFORM_ROUTES entries for the same URL pattern are tried in order.
    for pattern, tool_bin, handler in PLATFORM_ROUTES:
        m = re.search(pattern, target)
        if not m:
            continue
        handler_name = handler.__name__.replace("fetch_via_", "")

        # Skip if tool not installed (None = no binary needed)
        if tool_bin is not None and not shutil.which(tool_bin):
            msg = f"{tool_bin} not installed, skipping {handler_name}"
            print(f"[{handler_name}] {msg}", file=sys.stderr)
            errors.append((handler_name, msg))
            continue

        try:
            print(f"[{handler_name}] Fetching...", file=sys.stderr)
            content = handler(target, m)
            if len(content) < MIN_CONTENT_LEN:
                msg = f"too short ({len(content)} chars), trying next"
                print(f"[{handler_name}] {msg}", file=sys.stderr)
                errors.append((handler_name, msg))
                continue
            print(f"[{handler_name}] Success ({len(content)} chars)", file=sys.stderr)
            return content
        except Exception as e:
            print(f"[{handler_name}] Failed: {e}", file=sys.stderr)
            errors.append((handler_name, str(e)))
            continue  # try next handler for same pattern

    # Phase 2: generic fallback chain (Jina → markdown.new → raw)
    for name, fn in GENERIC_STRATEGIES:
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
