# clone-web

Local webpage cloning and visual archive workflow.

Use when replicating a webpage as a self-contained HTML/CSS clone, reusing a saved clone's design, or archiving a page's visual appearance.

## Install

Use the repo installer:

```bash
./install.sh --target codex
```

Manual Codex install:

```bash
ln -sf "$(pwd)" ~/.agents/skills/clone-web
```

## Notes

Requires Playwright MCP access for navigation, screenshots, and pixel comparison.
