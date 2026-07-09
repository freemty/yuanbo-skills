# Research Slides Skill

`research-slides` is the human-facing workflow for making restrained, source-backed research talks. It captures the style decisions from recent Beamer deck work: sparse language, paper-native figures and tables, real citations, and rendered PDF QA before reporting a slide edit as done.

## When to Use

Use `research-slides` when a task asks for:

- a paper-reading talk, literature survey, or research group presentation;
- converting paper notes into a Beamer deck;
- revising a technical deck for style, section order, citations, or figure quality;
- checking a compiled PDF for layout problems such as overlap, low-resolution figures, or footnote crowding.

Use `beamer-style` for the low-level LaTeX layout and color system. Use `research-slides` for the talk story, paper-figure workflow, source-credit rules, and visual QA loop.

## Design Contract

Research slides should read like evidence-backed arguments, not decorated summaries.

- Cover slide: title, speaker, date only.
- Table of contents: add after the cover when the talk has multiple sections.
- Sections: name the conceptual role, such as motivation, method family, core paper, systems, takeaway, or backup.
- Paper pages: put the paper title in the slide title and make the paper's own figure or table the center of the slide.
- Result pages: show the result table or plot first, then add one takeaway sentence.
- Citations: put concise slide-level citations in semi-transparent bottom-left text; put full clickable links on the final References slide.
- Online figures: credit the exact source URL below the figure, not only the blog name.
- Visual style: black/gray by default; let paper figures carry color.

## File Map

| Path | Purpose |
|------|---------|
| `skills/research-slides/SKILL.md` | Runtime workflow and routing instructions |
| `skills/research-slides/references/visual-style.md` | Visual density, color, layout, and anti-AI-slop rules |
| `skills/research-slides/references/writing-rules.md` | Title, TLDR, bullet, and section-name rules |
| `skills/research-slides/references/paper-slide-patterns.md` | How many slides each paper type deserves |
| `skills/research-slides/references/citation-and-source-credit.md` | Footnote, source-credit, and references-list format |
| `skills/research-slides/references/figure-extraction-workflow.md` | Extracting figures from PDFs, arXiv source, and blogs |
| `skills/research-slides/assets/research-main.tex` | Minimal starter Beamer deck using `layout-research` |
| `skills/beamer-style/templates/layout-research.tex` | Restrained black/gray Beamer layout |

## Standard Workflow

1. Decide the talk spine before editing individual slides.
2. For each core paper, extract the central figure or table instead of redrawing it from scratch.
3. Write one TLDR sentence that states mechanism plus consequence.
4. Add slide-level citations with author, paper title, and arXiv URL or exact source URL.
5. Compile with XeLaTeX.
6. Render changed pages to PNG and inspect them before finalizing.

```bash
latexmk -xelatex -interaction=nonstopmode main.tex
rg -n "(^!|LaTeX Error|Package .* Error|Overfull|Undefined control sequence)" main.log
skills/research-slides/scripts/render_check_pages.py main.pdf --first 1 --last 8 --out /tmp/research-slides-rendered
```

## Maintenance

When the talk style changes in a real deck, update the relevant reference file instead of expanding `SKILL.md`. Keep `SKILL.md` as the compact router; put detailed examples and house rules in `references/`.

When changing `layout-research`, compile `skills/research-slides/assets/research-main.tex` in a temporary directory and inspect the rendered pages. This catches the main failure modes: hidden color leakage from Beamer defaults, footnotes colliding with the progress bar, and dense references pages.
