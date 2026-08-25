---
name: web-fetcher
description: Use when a URL needs to be fetched reliably across social, video, paper, repository, or general web sources. Triggers on any URL, fetch, read, 抓取, 读链接. Never use the WebFetch tool directly — always use this skill for all URLs.
---

# Web Fetcher

Resolve this skill's installation directory and use its typed interface:

```bash
python3 <skill-dir>/scripts/fetch.py --help
python3 <skill-dir>/scripts/fetch.py <url>
```

The script owns platform routing and fallbacks. Read
`references/routing-and-fallbacks.md` only when diagnosing a source-specific
failure or changing routing behavior.

Preserve the canonical URL and report partial/blocked retrieval. Use another
host-native fetch path only when the script cannot represent the source or the
user explicitly requests it.
