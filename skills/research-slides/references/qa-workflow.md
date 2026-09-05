# QA Workflow

## Before editing

- Record `git status` and preserve unrelated changes.
- Compile or open the current PDF and render the target pages.
- Note the current page count, neighboring slide density, and citation baseline.

## After a coherent change set

1. Use the project build configuration (XeLaTeX/LuaLaTeX for the bundled profile); rerun as needed to resolve references, or use latexmk.
2. Scan for fatal errors, undefined references/citations, missing assets, overfull boxes, and hyperlink warnings.
3. Render every changed page and its immediate neighbors at 180 dpi or higher.
4. Inspect the PNGs, not only extracted text.

Check:

- no text, figure, citation, or progress-bar collision;
- paper figures are legible at projection distance and in a phone PDF view;
- crops retain labels, legends, and the relevant panel;
- arrows touch named start/end objects;
- titles and body density remain consistent with adjacent slides;
- every online figure has a visible clickable source;
- TOC, section order, page count, References, and backup placement remain coherent.
- the final deliverable PDF was built from the edited source and is not an older preserved artifact.
- title/author/date metadata is current, starter placeholders are gone, and no stray backup or placeholder frame remains visible after References.

Run:

```bash
python3 scripts/check_deck.py path/to/main.tex --pages 7,12-14
```

The script prepares rendered pages; the agent must still inspect them visually. A clean log is necessary, not sufficient.

## Build and review states

`check_deck.py` keeps existing options and adds `--engine auto|xelatex|lualatex|pdflatex`,
`--builder auto|latexmk|engine`, `--max-passes` and `--timeout` (180 seconds per
build/render command by default). A timed-out build is a failure, not a background
success; investigate the toolchain or explicitly raise the bound for a known slow
build. Auto prefers latexmk when available,
honors a `% !TeX program = ...` directive, then a local latexmk configuration;
otherwise it chooses an available engine (XeLaTeX first for the bundled profile).
Direct-engine mode reruns until auxiliary state converges, with a bounded pass
count. Bibliography workflows should use the project's latexmk configuration.
Nonstandard output/job names require a project build and an explicit QA source/PDF
mapping; this helper expects a same-stem PDF beside the source and fails otherwise.

`--no-compile` inspects existing outputs, rejects known stale/missing recorded
inputs, and reports incomplete dependency coverage when no `.fls` exists.
The recorder cannot discover newly appearing conditional files or every external
preprocessing/bibliography dependency without rebuilding; `--no-compile` reports
that limit even when all known inputs are fresh.
`--out` is a parent directory: every render gets a unique child directory, leaving
prior previews intact. Scripts report build checks passed and visual review pending.

Completion records distinguish: source/evidence checked; build checked; pages
actually viewed; issues fixed; remaining coverage. For a new deck inspect every
page. For repair inspect changed and neighboring pages, then review navigation
and source/PDF synchronization. Neither a clean build nor attractive layout proves
the research claim.
