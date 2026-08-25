---
name: research-slides
description: Use when creating or revising Beamer research talks, single-paper presentations, idea or motivation decks, literature surveys, experiment updates, existing-slide repairs, or decks requested in the Speculative Decoding/SD slides reference style.
---

# Research Slides

Build an evidence-backed argument in which each slide changes one audience belief. New decks use the bundled SD story and visual profile.

## Default reference profile

For every new deck, first read `references/speculative-decoding-reference-profile.md`, then the mode references below. Transfer its structure, not its domain facts. For `repair`, preserve the existing deck unless the user requests the SD reference.

## Route the task

| Signal | Mode | Required reference |
| --- | --- | --- |
| One anchor paper | `paper` | `references/story-modes.md`, `references/paper-slide-patterns.md` |
| Concept, hypothesis, proposal, or motivation | `idea` | `references/story-modes.md` |
| Multiple papers or a field trend | `survey` | `references/story-modes.md`, `references/paper-slide-patterns.md` |
| Existing `.tex`/PDF/screenshots and requested fixes | `repair` | `references/story-modes.md`, `references/qa-workflow.md` |

Infer the mode when clear. Ask only when missing context would materially change the deck.

## Shared workflow

1. Record audience, duration, objective, core sources, and delivery format.
2. Write a storyboard before LaTeX: `audience question -> slide claim -> governing tension -> evidence -> source -> spoken bridge/callback`.
3. For substantial decks, follow `references/multi-agent-workflow.md`; keep one `.tex` writer.
4. Select one dominant source-backed visual per slide. Follow `references/visual-style.md`, `references/writing-rules.md`, `references/figure-extraction-workflow.md`, and `references/citation-and-source-credit.md`; record assets in `source-manifest.tsv`.
5. For new decks, run `scripts/init_research_deck.py <target>`. For existing decks, preserve their template and render a baseline before editing.
6. Compile twice, scan the log and assets, render changed plus adjacent pages, then inspect the PNGs. Use `references/qa-workflow.md`.

## Hard gates

- Keep the cover to talk title, presenter, and date. Add a table of contents after it for a multi-section talk.
- Explain the object and failure before naming the solution.
- Give core papers method, main-result, and ablation/application evidence; compress secondary papers to one sourced slide.
- Prefer the paper's figure/table, then an authoritative teaching figure, then a minimal redraw.
- For new decks, keep the bundled black `beamer-colors.tex` plus `layout-metropolis.tex` default.
- Do not fill whitespace with cards, colors, arrows, or prose.
- Put each source on its own clickable citation line and finish with a dense reference list.
- Never report completion from a successful compile alone; inspect rendered pages for overlap, blur, clipping, and citation collisions.

## Utilities

- `scripts/crop_whitespace.py`: crop raster figures while preserving transparency.
- `scripts/render_check_pages.py`: render a clean page range to PNG.
- `scripts/check_deck.py`: compile, scan logs/assets, and render selected pages.
- `references/speculative-decoding-reference-profile.md`: default story architecture, evidence cadence, and cross-topic mapping.

Use `beamer-style` only when the user requests another theme or layout. Do not silently substitute `layout-research` for the default. This skill's bundled starter is self-contained.
