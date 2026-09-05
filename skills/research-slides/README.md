# research-slides

Multi-mode workflow for restrained, source-backed Beamer decks.

Use `paper`, `idea`, `survey`, or `repair` mode to create and revise talks from papers, concepts, experiments, or literature notes. New decks use the self-contained black palette and minimal Metropolis layout from the Speculative Decoding deck. The skill also bundles a legacy `layout-research` option, source manifest, figure workflow, and deterministic compile/render checks.

The default `references/speculative-decoding-reference-profile.md` also transfers the reference deck's knowledge structure: object and pressure first, source-derived trade-offs, correctness/evaluation contract, method families as answers, core-paper evidence, callbacks, and frontier synthesis. It never copies SD domain facts into unrelated topics.

The visual default remains fixed unless the user requests otherwise; story length
adapts to the audience and duration. A short talk need not include TOC, four
takeaways or a long-talk page budget. Theory needs assumptions and proof, not
invented ablations; a proposal distinguishes concerns, hypotheses and planned tests.

## Quick start

```bash
python3 scripts/init_research_deck.py /tmp/my-talk
python3 scripts/check_deck.py /tmp/my-talk/main.tex --pages 1-4
```

The initializer preflights every target before writing. `check_deck.py` supports
`--engine`, `--builder` and bounded direct-engine convergence, honors project build
configuration, and records dependency freshness. `--no-compile` does not excuse a
known stale PDF. Each `--out` render uses a unique child folder and preserves older
previews. Build checks passing leaves visual and research-evidence review pending.

Regression checks:

```bash
python3 scripts/test_template.py
python3 scripts/test_workflows.py
```

## Invoke

- Codex: `$research-slides`
- Claude Code: `/research-slides`

Provide the topic or sources; audience and duration are optional. New decks use the SD reference profile without requiring a separate `beamer-style` call.

## Install

Use the repo installer:

```bash
./install.sh --target codex
```

Manual Codex install:

```bash
ln -sf "$(pwd)" ~/.agents/skills/research-slides
```
