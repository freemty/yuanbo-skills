---
name: research-slides
description: >
  Use when creating, editing, or QAing research presentations, Beamer decks,
  paper-reading talks, literature survey slides, or slide revisions where
  citations, paper figures/tables, restrained visual style, and rendered PDF
  verification matter.
---

# Research Slides

## Overview

Build research talks as evidence-backed arguments, not decorated summaries. Prefer a restrained Beamer surface, paper-native figures/tables, precise citations, and one clear claim per slide.

Use `beamer-style` for low-level Beamer themes and layouts. Use this skill for story structure, slide content, figure/source handling, citation discipline, and PDF QA.

## Workflow

1. Identify the talk spine before editing slides.
   - Cover: title, speaker, date only.
   - Add a table of contents after the cover for talks with multiple sections.
   - Name sections by conceptual role: motivation, method families, core papers, systems, takeaways.

2. Choose slide types by evidence need.
   - Motivation slide: one problem statement plus one simple figure or table.
   - Paper overview slide: paper title as slide title plus the paper's core figure.
   - Result slide: main table/plot plus one takeaway sentence.
   - Ablation slide: design choice plus the table/plot that proves it.
   - Backup slide: useful but nonessential details, marked optional or backup.

3. Use paper and source artifacts first.
   - For core papers, prefer figures/tables from the paper or arXiv source over redrawn diagrams.
   - For blogs or online diagrams, cite the exact source URL below the figure.
   - Redraw only when the original figure is too noisy or the talk needs a simplified conceptual contrast.

4. Keep language sparse.
   - One claim per slide.
   - Use TLDR sentences for mechanism and consequence, not method-name restatement.
   - Remove arrows, boxes, bullets, or labels that do not clarify a dependency.

5. Compile and visually verify every meaningful change.
   - Run `latexmk -xelatex -interaction=nonstopmode main.tex`.
   - Grep the log for LaTeX errors, undefined refs, and overfull boxes.
   - Render changed pages with Poppler and inspect the PNGs before reporting done.

## Reference Files

- Read `references/visual-style.md` when adjusting layout, color, density, or figure placement.
- Read `references/writing-rules.md` when rewriting slide titles, TLDRs, bullets, or section names.
- Read `references/paper-slide-patterns.md` when deciding how many slides a paper deserves.
- Read `references/citation-and-source-credit.md` when adding citations, links, or a References slide.
- Read `references/figure-extraction-workflow.md` when extracting figures/tables from PDFs, arXiv source, or blogs.

## Scripts

- `scripts/crop_whitespace.py`: crop white margins from extracted paper figures.
- `scripts/render_check_pages.py`: render selected PDF pages to PNG for visual QA.

## Defaults

- Use Beamer `layout-research` from `beamer-style` when starting a new technical research talk.
- Keep the visual surface black/gray unless a figure already carries color.
- Put source credits in semi-transparent bottom-left text.
- Put full clickable paper links in the final References slide.
