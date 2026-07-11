# Figure Extraction Workflow

## Source Priority

1. arXiv source archive (`https://arxiv.org/e-print/<id>`)
2. paper PDF rendered at high DPI
3. official project page or blog image
4. manually redrawn diagram

Use the original figure unless it is unreadable or teaches the wrong level of detail. A redraw is a last resort, not a default cleanup step.

## arXiv Source

```bash
mkdir -p /tmp/paper-src
curl -L --fail https://arxiv.org/e-print/<id> -o /tmp/paper-src/source.tar
tar -xzf /tmp/paper-src/source.tar -C /tmp/paper-src
find /tmp/paper-src -maxdepth 3 -type f | sort
```

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
- For GIFs in static PDFs, use a representative still frame unless the final delivery format supports animation.
- Always cite the page or image URL below the figure.

## Quality Bar

- Text in the figure must be readable at presentation distance.
- Avoid low-resolution screenshots when source PDFs are available.
- If the original figure is visually noisy but important, crop to the relevant panel before placing it.
- Do not redraw a paper method figure unless the original is unusable.
- Do not silently remove axes, legends, conditions, or row labels needed to interpret the result.
- Verify every extracted asset exists and renders after moving the deck to a clean directory.
