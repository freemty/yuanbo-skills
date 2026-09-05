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
