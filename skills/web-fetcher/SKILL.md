---
name: web-fetcher
description: Use when a source needs specialized extraction, download, or saved retrieval evidence across social, video, paper and repository sites. Triggers on reliable fetch, 抓取, 提取正文, 保存链接内容.
---

# Web Fetcher

Choose the available capability that matches the requested evidence. Ordinary
text can be read directly with native search, readers or structured integrations;
visual/interactive questions need a browser or media-capable host. This skill's
CLI is an optional adapter for extraction, conversion and repeatable retrieval.

Resolve this skill's installation directory for its CLI:

```bash
python3 <skill-dir>/scripts/fetch.py --help
python3 <skill-dir>/scripts/fetch.py <url>
python3 <skill-dir>/scripts/fetch.py <url> --format json -o evidence.json
```

Read [capability selection](references/capability-selection.md) when choosing a
path, [source adapters](references/source-adapters.md) for CLI support/failures,
and [media evidence](references/media-evidence.md) for video/audio/visual claims.

Report URL, acquisition time and actual coverage. A caption supports speech,
metadata describes a source, and neither establishes observed actions. Missing
CLI tools do not prevent native reads. Reading does not authorize archival or
publishing; save only when the requested task includes it.
