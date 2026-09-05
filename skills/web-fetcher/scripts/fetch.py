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
import html
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from datetime import datetime, timezone
from urllib.parse import urlparse


@dataclass
class Extraction:
    content: str
    content_kind: str = "text"
    status: str = "ok"
    limitations: list[str] = field(default_factory=list)


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


PROXY = os.environ.get("HTTPS_PROXY") or os.environ.get("HTTP_PROXY") or os.environ.get("http_proxy")


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
    tweet_id = tweet.get("id") or tweet.get("id_str")
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
    if tweet_id and handle:
        lines.append(f"\nSource: https://x.com/{handle}/status/{tweet_id}")
    for m in media:
        media_url = m.get("url", "")
        if media_url:
            lines.append(f"\nAttached media (not inspected): [{m.get('type', 'media')}]({media_url})")
    return "\n".join(lines)


def fetch_via_xreach(url: str, match: re.Match) -> Extraction:
    """Fetch a tweet via xreach CLI → markdown. Tries thread first, falls back to single."""
    # Try thread first (gets full conversation context)
    try:
        raw = _run(["xreach", "thread", url, "--json"] + (["--proxy", PROXY] if PROXY else []), timeout=45)
        data = json.loads(raw)
        tweets = data if isinstance(data, list) else [data]
        return format_conversation(tweets, url)
    except Exception as thread_err:
        print(f"[xreach thread] Failed: {thread_err}, trying single tweet", file=sys.stderr)

    # Fallback to single tweet
    raw = _run(["xreach", "tweet", url, "--json"] + (["--proxy", PROXY] if PROXY else []))
    data = json.loads(raw)
    tweet = data[0] if isinstance(data, list) else data
    return format_conversation([tweet], url)


def format_conversation(tweets: list[dict], url: str) -> Extraction:
    wanted = urlparse(url).path.rstrip('/').split('/')[-1]
    root = next((t for t in tweets if str(t.get('id') or t.get('id_str')) == wanted), None)
    if root is None or not (root.get('text') or root.get('media')):
        raise ValueError('requested root tweet missing; conversation is not source evidence')
    author = root.get('user', {}).get('screenName', '').lower()
    replies = [t for t in tweets if t is not root and t.get('user', {}).get('screenName', '').lower() == author]
    others = [t for t in tweets if t is not root and t not in replies]
    parts = ['# Root post', _format_tweet(root)]
    for heading, items in [('Author replies', replies), ('Other accounts / conversation context', others)]:
        if items:
            parts += [f'# {heading}'] + [_format_tweet(t) for t in items]
    limits = ['Conversation retrieval may be incomplete; other accounts are not author claims.']
    if any(t.get('media') for t in tweets):
        limits.append('Attached media links were retrieved, not visually or aurally inspected.')
    return Extraction('\n\n---\n\n'.join(parts), 'social_post', limitations=limits)


def timestamp(seconds: float) -> str:
    millis = round(float(seconds) * 1000)
    hours, rest = divmod(millis, 3600000)
    minutes, rest = divmod(rest, 60000)
    secs, ms = divmod(rest, 1000)
    return f'{hours:02}:{minutes:02}:{secs:02}.{ms:03}'


def parse_captions(raw: str, ext: str) -> list[str]:
    """Normalize supported caption formats to timestamped cues, never a flat transcript."""
    cues = []
    if ext == 'json3':
        for event in json.loads(raw).get('events', []):
            text = ''.join(s.get('utf8', '') for s in event.get('segs', []))
            if text.strip():
                start = event.get('tStartMs', 0) / 1000
                end = start + event.get('dDurationMs', 0) / 1000
                cues.append(f'[{timestamp(start)} --> {timestamp(end)}] {text.strip()}')
    elif ext == 'srv1':
        for node in ET.fromstring(raw).iter('text'):
            start = float(node.get('start', 0))
            end = start + float(node.get('dur', 0))
            text = html.unescape(''.join(node.itertext())).strip()
            if text:
                cues.append(f'[{timestamp(start)} --> {timestamp(end)}] {text}')
    elif ext in {'vtt', 'srt'}:
        timing = None
        parts = []
        def flush():
            if timing and parts:
                cues.append(f'[{timing}] ' + ' '.join(parts))
        for line in raw.replace('\r', '').split('\n') + ['']:
            if '-->' in line:
                flush()
                timing = ' '.join(line.strip().replace(',', '.').split()[:3])
                parts = []
            elif not line.strip():
                flush()
                timing, parts = None, []
            elif timing:
                text = html.unescape(re.sub(r'<[^>]+>', '', line)).strip()
                if text:
                    parts.append(text)
    else:
        raise ValueError(f'unsupported caption format: {ext}')
    return cues


def fetch_via_ytdlp(url: str, match: re.Match) -> Extraction:
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

    # Captions support speech claims only; no frames or audio are inspected here.
    subtitles = data.get("subtitles", {})
    auto_captions = data.get("automatic_captions", {})
    sub_langs = subtitles or auto_captions
    if sub_langs:
        # Prefer zh/en manual subs, then auto captions
        for lang in dict.fromkeys(["zh-Hans", "zh", "zh-CN", "en", "ja", *sub_langs]):
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
                        clean_lines = parse_captions(sub_text, fmt['ext'])
                        if clean_lines:
                            lines.append(f"\n## Subtitles ({lang})\n")
                            lines.append("\n".join(clean_lines))
                            return Extraction('\n'.join(lines), 'video_captions', 'partial',
                                [f"{'Manual' if lang in subtitles else 'Automatic'} captions ({lang}); timestamps retained.",
                                 'No frames or audio inspected; caption coverage may omit silence, actions or uncaptioned speech.'])
                    except Exception as e:
                        print(f"[subtitles] Failed to fetch {lang}: {e}", file=sys.stderr)

    return Extraction('\n'.join(lines), 'video_metadata', 'partial',
                      ['No usable captions retrieved.', 'No frames or audio inspected. Description is uploader metadata, not observed video.'])


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


def fetch_via_baike_mobile(url: str, match: re.Match) -> str:
    """Fetch Baidu Baike via mobile version (wapbaike) which has simpler HTML.

    Desktop baike.baidu.com is JS-rendered and Jina Reader only gets the navbar.
    Mobile wapbaike.baidu.com serves actual content in lighter HTML that Jina can parse.
    """
    mobile_url = url.replace("baike.baidu.com", "wapbaike.baidu.com", 1)
    return fetch_url(
        f"https://r.jina.ai/{mobile_url}",
        headers={"Accept": "text/markdown"},
        timeout=30,
    )


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
    # 百度百科 (desktop → rewrite to mobile for better content extraction)
    (r"baike\.baidu\.com/(item|view)/", None, fetch_via_baike_mobile),
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


def assess(content: str | Extraction, target: str, backend: str) -> Extraction:
    if isinstance(content, Extraction):
        return content
    text = content.strip()
    if not text or text.startswith('%PDF'):
        raise ValueError('empty or binary content; use a native document reader')
    # Look for a gate in the title/leading content, not a mention inside an article.
    lead = re.sub(r'<[^>]+>', ' ', text[:1200]).strip()
    if re.search(r'(?im)^(?:title:\s*|#*\s*)?(?:403\b|404\b|access denied\b|sign in to (?:continue|x)|log in to continue|just a moment|verify (?:you are|that you)|captcha\b|page not found|this page requires javascript)', lead):
        raise ValueError('login, challenge or error page')
    if re.search(r'<(?:html|!doctype)\b', text, re.I):
        body = re.sub(r'<(?:script|style|nav|header|footer)\b[^>]*>.*?</(?:script|style|nav|header|footer)>', '', text, flags=re.S|re.I)
        paragraphs = re.findall(r'<(?:p|article)\b[^>]*>(.*?)</(?:p|article)>', body, re.S|re.I)
        extracted = '\n\n'.join(html.unescape(re.sub(r'<[^>]+>', '', p)).strip() for p in paragraphs).strip()
        if not extracted:
            raise ValueError('HTML shell has no extractable article/paragraph evidence')
        result = assess(extracted, target, backend)
        result.status = 'partial'
        result.limitations.append('Basic HTML extraction; layout and completeness unverified.')
        return result
    prose = re.sub(r'!?\[[^\]]*\]\([^)]*\)', '', text)
    prose = re.sub(r'(?im)^(?:title:|url source:|markdown content:).*$', '', prose).strip(' #*\n-')
    if not prose:
        raise ValueError('navigation-only result')
    if re.search(r'(youtube\.com|youtu\.be|bilibili\.com)', urlparse(target).netloc):
        return Extraction(text, 'video_metadata', 'partial', ['Text page only; no verified captions, frames or audio.'])
    if urlparse(target).netloc == 'arxiv.org':
        return Extraction(text, 'paper_page', 'partial', ['Paper landing/extracted page; full-text coverage and requested anchors not validated.'])
    if re.search(r'(?:twitter|x)\.com$', urlparse(target).netloc):
        return Extraction(text, 'social_page', 'partial', ['Unstructured social extraction; root/reply attribution and media not validated.'])
    return Extraction(text)


def fetch_result(target: str) -> dict:
    retrieved = datetime.now(timezone.utc).isoformat()
    def packet(extraction: Extraction, backend: str) -> dict:
        return dict(source_url=target, retrieved_at=retrieved, backend=backend,
                    status=extraction.status, content_kind=extraction.content_kind,
                    content=extraction.content, limitations=extraction.limitations)
    if urlparse(target).scheme not in {'http', 'https'} or not urlparse(target).netloc:
        return packet(Extraction('', 'none', 'unsupported', ['Only absolute HTTP(S) URLs are supported.']), 'none')
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
            result = assess(handler(target, m), target, handler_name)
            return packet(result, handler_name)
        except Exception as e:
            print(f"[{handler_name}] Failed: {e}", file=sys.stderr)
            errors.append((handler_name, str(e)))
            continue  # try next handler for same pattern

    # Phase 2: generic fallback chain (Jina → markdown.new → raw)
    for name, fn in GENERIC_STRATEGIES:
        try:
            print(f"[{name}] Fetching...", file=sys.stderr)
            return packet(assess(fn(target), target, name), name)
        except Exception as e:
            print(f"[{name}] Failed: {e}", file=sys.stderr)
            errors.append((name, str(e)))

    return packet(Extraction('', 'none', 'blocked', [f'{name}: {err}' for name, err in errors]), 'none')


def markdown(result: dict) -> str:
    note = f"Source: {result['source_url']}\nRetrieved: {result['retrieved_at']}\nBackend: {result['backend']}\nCoverage: {result['status']} / {result['content_kind']}"
    if result['limitations']:
        note += '\n' + '\n'.join('- ' + item for item in result['limitations'])
    return result['content'] + '\n\n---\n' + note + '\n'


def fetch(target: str) -> str:
    result = fetch_result(target)
    if result['status'] in {'blocked', 'unsupported'}:
        raise RuntimeError('; '.join(result['limitations']))
    return markdown(result)


def main():
    parser = argparse.ArgumentParser(description="Fetch web page content as text")
    parser.add_argument("url", help="Target URL to fetch")
    parser.add_argument("-o", "--output", help="Output file (default: stdout)")
    parser.add_argument('--format', choices=['markdown', 'json'], default='markdown')
    args = parser.parse_args()

    result = fetch_result(args.url)
    content = json.dumps(result, ensure_ascii=False, indent=2) if args.format == 'json' else markdown(result)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Saved to {args.output}", file=sys.stderr)
    else:
        print(content)
    return 1 if result['status'] in {'blocked', 'unsupported'} else 0


if __name__ == "__main__":
    sys.exit(main())
