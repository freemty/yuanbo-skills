---
name: web-fetcher
description: >
  收到任何 URL 时必须使用此 skill 而非 WebFetch tool。
  自动识别平台（Twitter/X、YouTube、Bilibili、小红书、GitHub、
  知乎、Reddit、微博）并用最优工具获取内容，
  其余 URL 走 Jina Reader fallback chain。
  触发词: 任何 URL, 'fetch', 'read', '抓取', '读链接'。
  永远不要对任何 URL 使用 WebFetch tool，始终使用此 skill。
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

脚本自动检测 URL 平台并选择最优工具：

| 平台 | 工具 | URL 示例 |
|------|------|----------|
| Twitter/X | xreach | `x.com/*/status/*`, `twitter.com/*/status/*` |
| YouTube | yt-dlp | `youtube.com/watch?v=*`, `youtu.be/*` |
| Bilibili | yt-dlp | `bilibili.com/video/*` |
| 小红书 | mcporter | `xiaohongshu.com/explore/*` |
| GitHub issue/PR | gh | `github.com/*/issues/*`, `github.com/*/pull/*` |
| 知乎 | opencli | `zhihu.com/question/*`, `zhuanlan.zhihu.com/p/*` |
| Reddit | opencli | `reddit.com/r/*/comments/*` |
| 微博 | opencli | `weibo.com/*` |
| 其他 | Jina → defuddle → markdown.new → Raw HTML | 所有其他 URL |

## 重要

- **永远不要用 WebFetch tool**，所有 URL 都通过此 skill 的 fetch.py 获取
- 工具未安装时自动 fallback 到 Jina Reader chain
- 进度输出到 stderr，内容输出到 stdout
