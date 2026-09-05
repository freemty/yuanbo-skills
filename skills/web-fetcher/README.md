# web-fetcher

Unified URL fetcher with platform-aware routing.

Use for specialized extraction, repeatable retrieval or saved source evidence. Native readers and browser/media capabilities remain available directly. The optional CLI supports social, video, paper and repository adapters and reports actual coverage.

## Install

Use the repo installer:

```bash
./install.sh --target codex
```

Manual Codex install:

```bash
ln -sf "$(pwd)" ~/.agents/skills/web-fetcher
```

## Script

Run `scripts/fetch.py URL [-o FILE]` from the installed skill directory for Markdown.
Add `--format json` for a provenance/coverage envelope. Video metadata and captions
are partial observations, never proof that frames or audio were analyzed.
