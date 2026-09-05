# Figure Extraction Workflow

## Choose an available source

Use an original vector/source asset when available and faithful to the cited
figure; otherwise use a readable PDF crop or the original project-page image.
Choose based on the needed figure and current access, not a fixed download chain.
A redraw must be labeled and preserve the mechanism/data rather than inventing
details. Native PDF screenshots are valid without a separate CLI.

## arXiv Source

If using an arXiv source archive, download into a unique temporary directory.
Inspect entries before extracting; reject absolute paths, parent traversal and
links escaping that directory. Do not overwrite project files or execute source
scripts. Inspect extracted figures against the actual paper caption.

Look for `figures/`, `figure_text/`, `*.pdf`, `*.png`, `*.jpg`, and table `.tex` files. Use the paper's caption text to identify the correct figure.

Record the source while extracting:

| asset | source URL | figure/table | page | crop | claim supported |
| --- | --- | --- | --- | --- | --- |
| `figs/method.pdf` | exact URL | Fig. 2 | 4 | full | mechanism |

## Render From PDF

```bash
pdftoppm -png -r 300 -f <page> -l <page> paper.pdf /tmp/page
```

Then crop the relevant region manually or use a PDF screenshot tool if needed.

Prefer vector PDF crops when the deck toolchain supports them. For raster output, render at 250-400 dpi and inspect the labels at final slide size.

## Crop Whitespace

```bash
python3 <research-slides>/scripts/crop_whitespace.py input.png output.png --margin 28
```

Use in-place only for generated assets:

```bash
python3 <research-slides>/scripts/crop_whitespace.py figure.png --in-place
```

## Blogs and Web Images

- Prefer direct image URLs when available.
- For GIFs in static PDFs, use a timestamped representative still for appearance; a single frame does not establish the animation's temporal behavior.
- Always cite the page or image URL below the figure.

## Quality Bar

- Text in the figure must be readable at presentation distance.
- Avoid low-resolution screenshots when source PDFs are available.
- If the original figure is visually noisy but important, crop to the relevant panel before placing it.
- Do not redraw a paper method figure unless the original is unusable.
- Do not silently remove axes, legends, conditions, or row labels needed to interpret the result.
- Verify every extracted asset exists and renders after moving the deck to a clean directory.
