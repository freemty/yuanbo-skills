# research-slides

Multi-mode workflow for restrained, source-backed Beamer decks.

Use `paper`, `idea`, `survey`, or `repair` mode to create and revise talks from papers, concepts, experiments, or literature notes. The skill bundles a self-contained black/gray Beamer layout, source manifest, figure workflow, and deterministic compile/render checks.

## Quick start

```bash
python3 scripts/init_research_deck.py /tmp/my-talk
python3 scripts/check_deck.py /tmp/my-talk/main.tex --pages 1-4
```

## Install

Use the repo installer:

```bash
./install.sh --target codex
```

Manual Codex install:

```bash
ln -sf "$(pwd)" ~/.agents/skills/research-slides
```
