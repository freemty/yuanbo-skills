---
name: web-fetcher
description: >
  Use when receiving any URL to fetch content. Replaces WebFetch tool entirely.
  Triggers: any URL, fetch, read, 抓取, 读链接.
  IMPORTANT: Never use WebFetch tool directly — always use this skill for all URLs.
---

# Web Fetcher

收到 URL 时运行：

```bash
python3 ~/.claude/skills/web-fetcher/scripts/fetch.py <url>
```

保存到文件：

```bash
python3 ~/.claude/skills/web-fetcher/scripts/fetch.py <url> -o output.md
```

## 自动路由

脚本自动检测 URL 平台并选择最优工具。同平台有多个工具时按顺序 fallback：

| 平台 | 工具 (优先级) | URL 示例 |
|------|--------------|----------|
| Twitter/X | xreach (thread→tweet) → opencli twitter → Thread Reader App | `x.com/*/status/*` |
| YouTube | yt-dlp (metadata + subtitles) | `youtube.com/watch?v=*`, `youtu.be/*` |
| Bilibili | yt-dlp (metadata + subtitles) | `bilibili.com/video/*` |
| 小红书 | mcporter | `xiaohongshu.com/explore/*`, `xhs.link/*` |
| GitHub issue/PR | gh | `github.com/*/issues/*`, `github.com/*/pull/*` |
| 知乎 | opencli zhihu (question/download) | `zhihu.com/question/*`, `zhuanlan.zhihu.com/p/*` |
| Reddit | opencli reddit read | `reddit.com/r/*/comments/*` |
| arXiv | opencli arxiv paper | `arxiv.org/abs/*`, `arxiv.org/pdf/*` |
| HackerNews | Jina Reader | `news.ycombinator.com/item?id=*` |
| 微博 | opencli weibo | `weibo.com/*` |
| 其他 | Jina Reader → markdown.new → Raw HTML | 所有其他 URL |

## 重要

- **永远不要用 WebFetch tool**，所有 URL 都通过此 skill 的 fetch.py 获取
- 同平台多个工具自动按优先级 fallback（如 xreach 失败自动尝试 opencli → Thread Reader）
- 工具未安装时自动跳过，继续 fallback chain
- YouTube/Bilibili 现在会尝试获取字幕内容（中/英/日）
- 进度输出到 stderr，内容输出到 stdout
