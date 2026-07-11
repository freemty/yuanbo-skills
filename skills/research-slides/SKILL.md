---
name: research-slides
description: Use when creating or revising Beamer research talks, single-paper presentations, idea or motivation decks, literature surveys, experiment updates, or existing-slide repairs where the audience story and source-backed evidence must remain clear.
---

# Research Slides

Build an evidence-backed argument in which each slide changes one audience belief. Use the restrained bundled Beamer layout; let source figures carry the visual detail.

## Route the task

| Signal | Mode | Required reference |
| --- | --- | --- |
| One anchor paper | `paper` | `references/story-modes.md`, `references/paper-slide-patterns.md` |
| Concept, hypothesis, proposal, or motivation | `idea` | `references/story-modes.md` |
| Multiple papers or a field trend | `survey` | `references/story-modes.md`, `references/paper-slide-patterns.md` |
| Existing `.tex`/PDF/screenshots and requested fixes | `repair` | `references/story-modes.md`, `references/qa-workflow.md` |

Infer the mode when clear and state it briefly. Ask only when audience, duration, or the core claim would materially change the deck.

## Shared workflow

1. Record audience, duration, objective, core sources, and delivery format.
2. Write a storyboard before LaTeX: `audience question -> slide claim -> evidence -> source -> spoken bridge`.
3. For substantial decks, use the read-only agent split in `references/multi-agent-workflow.md`; keep one writer for the `.tex` file.
4. Select one dominant source-backed visual per slide. Follow `references/visual-style.md`, `references/writing-rules.md`, `references/figure-extraction-workflow.md`, and `references/citation-and-source-credit.md`; record assets in `source-manifest.tsv`.
5. For new decks, run `scripts/init_research_deck.py <target>`. For existing decks, preserve their template and render a baseline before editing.
6. Compile twice, scan the log and assets, render changed plus adjacent pages, then inspect the PNGs. Use `references/qa-workflow.md`.

## Hard gates

- Keep the cover to talk title, presenter, and date. Add a table of contents after it for a multi-section talk.
- Explain the object and failure before naming the solution.
- Give core papers method, main-result, and ablation/application evidence; compress secondary papers to one sourced slide.
- Prefer the paper's figure/table, then an authoritative teaching figure, then a minimal redraw.
- Keep a white canvas with black/gray type and rules. Do not fill whitespace with cards, colors, arrows, or prose.
- Treat historical slide corpora as evidence of storytelling habits, not as palette or layout authority. The newest explicit visual preference wins.
- Put each source on its own clickable citation line and finish with a dense reference list.
- Never report completion from a successful compile alone; inspect rendered pages for overlap, blur, clipping, and citation collisions.

## Utilities

- `scripts/crop_whitespace.py`: crop raster figures while preserving transparency.
- `scripts/render_check_pages.py`: render a clean page range to PNG.
- `scripts/check_deck.py`: compile, scan logs/assets, and render selected pages.
- `references/worked-example.md`: example storyboard for an idea-to-survey talk.

Use `beamer-style` only when the user requests another theme or layout. This skill's bundled starter is self-contained.
