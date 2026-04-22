# Ecosystem: Web Access & Network Tools

Tools for giving Claude Code the ability to browse, fetch, and interact with the web.

## Jina Reader

> https://r.jina.ai/

Prefix any URL with `https://r.jina.ai/` to get clean markdown. Fast, free, no auth.

```bash
# Read any webpage as markdown
curl -s "https://r.jina.ai/URL" -H "Accept: text/markdown"

# Search the web
curl -s "https://s.jina.ai/query" -H "Accept: text/markdown"
```

Limitations: may fail on JS-heavy pages, sometimes needs timeout header (`-H "X-Timeout: 30"`).

## markdown-proxy

> https://github.com/joeseesun/markdown-proxy

Fetch any URL as clean Markdown via proxy services (r.jina.ai / defuddle.md) or built-in scripts. Works with login-required pages like X/Twitter, WeChat.

Useful when Jina Reader fails or when you need authenticated page access.

## Agent-Reach

> https://github.com/Panniantong/Agent-Reach

Installer and config tool for 12+ platform access tools. After setup, call upstream tools directly.

```bash
pip install https://github.com/Panniantong/agent-reach/archive/main.zip
agent-reach install --env=auto
agent-reach doctor
```

Supported platforms:
- **Twitter/X**: xreach CLI (`xreach search`, `xreach tweet`)
- **YouTube**: yt-dlp (`--dump-json`, subtitle download)
- **Reddit**: JSON API (`curl reddit.com/r/xxx.json`)
- **GitHub**: gh CLI
- **Bilibili**: yt-dlp
- **XiaoHongShu**: mcporter + xiaohongshu-mcp
- **Douyin**: mcporter + douyin-mcp-server
- **LinkedIn**: mcporter + linkedin-scraper-mcp

## Playwright CLI

> https://github.com/microsoft/playwright-cli

CLI for common Playwright actions. Record and generate Playwright code, inspect selectors and take screenshots.

Best for: automated browser testing, recording user flows, element inspection.

## Web Access Skill (by eze_is_1)

> https://github.com/eze-is/web-access
> https://x.com/eze_is_1/status/2035907179652522324

A skill that optimizes Claude Code's web browsing strategy:
- Reduces the pattern of "only searching without browsing" or "only fetching without searching"
- Auto-summarizes site operation experience, improving speed with each execution
- Supports opening 100+ browser pages at once
- Automated social media posting
- Web app automated testing

## Decision Guide

| Need | Tool |
|------|------|
| Quick webpage read | Jina Reader |
| Login-required pages | markdown-proxy |
| Multi-platform access (Twitter, YouTube, etc.) | Agent-Reach |
| Browser automation & testing | Playwright CLI |
| Comprehensive web browsing skill | Web Access Skill |
| Headless browser QA | gstack /browse or /qa |
