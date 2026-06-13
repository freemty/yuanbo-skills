---
name: clone-web
description: "Use when replicating a webpage as a local HTML/CSS clone, reusing a previously cloned site's design, or archiving a page's visual appearance. Triggers: /clone-web <url>, /clone-web use <name>, /clone-web list"
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - AskUserQuestion
  - Agent
---

# Clone Web — Pixel-Perfect Website Cloning

Clone a webpage into a self-contained, reusable design unit. Each clone lives in `clones/<slug>/` with manifest, design tokens, and preview.

## Commands

| Command | Action |
|---------|--------|
| `/clone-web <url>` | Clone a new webpage (full pipeline below) |
| `/clone-web use <name>` | Copy a saved clone into the current project |
| `/clone-web use <name> --tokens` | Output only the design tokens for reference |
| `/clone-web list` | List all saved clones from the registry |

## Registry

Clones are stored in `clones/` with a `registry.json` index:

```
clones/
├── registry.json          # global index
└── <slug>/
    ├── manifest.json      # metadata: source URL, date, accuracy, stack, tags
    ├── tokens.json        # extracted design tokens: colors, fonts, spacing
    ├── index.html         # the clone
    ├── style*.css         # stylesheets
    ├── preview.png        # viewport screenshot of the clone
    └── *.png/woff2        # local assets referenced by HTML
```

### `use` command

Read `clones/registry.json` → find matching slug → copy the clone directory into the current project (or a user-specified path). With `--tokens`, just read and output `tokens.json`.

### `list` command

Read `clones/registry.json` → display a table: name, display_name, color_scheme, stack, accuracy, tags.

## Prerequisites

Playwright MCP must be connected.

## Clone Pipeline

### Step 0: Input

Parse the URL from args. Derive slug from domain (e.g., `generalistai.com` → `generalist`). Create output directory: `clones/<slug>/`

### Step 1: Reconnaissance

Navigate via Playwright and capture baseline:

```javascript
async (page) => {
  await page.emulateMedia({ colorScheme: 'dark' }); // or 'light' — match original
  await page.goto(URL, { waitUntil: 'domcontentloaded' });
  await page.setViewportSize({ width: 1280, height: 720 });
  await page.waitForLoadState('networkidle');
  await page.screenshot({ path: 'original-viewport.png', scale: 'css', type: 'png' });
}
```

Detect tech stack — run `page.evaluate()`:
- `document.querySelectorAll('link[rel="stylesheet"]')` → CSS bundle URLs
- `document.body.className` → Tailwind utility classes?
- `getComputedStyle(document.documentElement)` → CSS custom properties
- `document.fonts` → loaded font families + sources

### Step 2: Extraction

**CSS** — two strategies:

| Stack | Strategy |
|-------|----------|
| Custom CSS | `document.styleSheets → cssRules → cssText` → single file |
| Tailwind/Next.js | `curl` the CSS bundle files from `<link>` URLs, then purge unused selectors |

**HTML** — extract via `page.evaluate()`:
```javascript
const el = document.querySelector('main')
  || document.querySelector('article')
  || document.querySelector('[role="main"]')
  || document.querySelector('#app')
  || document.querySelector('#root')
  || document.querySelector('#__next')
  || document.querySelector('body > div');
const clone = el.cloneNode(true);
clone.querySelectorAll('script').forEach(s => s.remove());
clone.querySelectorAll('*').forEach(el => {
  Array.from(el.attributes).forEach(attr => {
    if (attr.name.startsWith('data-')) el.removeAttribute(attr.name);
  });
});
return clone.outerHTML;
```

For pages >100KB: extract header, prose sections, footer separately. Replace interactive elements (canvas, SVG charts >5KB, complex demos) with type markers.

**Fonts** — prefer original CDN when accessible:
```
@font-face { font-family: 'X'; src: url('https://original-site.com/path/font.woff2') format('woff2'); }
```

Fallback mapping for inaccessible fonts:

| Original | Free Alternative |
|---|---|
| FK Grotesk Neue | Outfit |
| Söhne | Inter |
| GT America | DM Sans |
| Neue Montreal | Space Grotesk |
| Graphik | Plus Jakarta Sans |
| signifier | Playfair Display (closest serif) |

### Step 3: Assembly

1. **CSS files** — fix relative URLs to absolute:
   ```bash
   sed -i '' 's|url(/_next/|url(https://site.com/_next/|g' style.css
   ```
   For Tailwind bundles: grep used classes from the HTML, strip unused selectors to reduce file size.

2. **Color scheme forcing** — THE #1 source of visual mismatch:
   - Edit `:root` defaults in CSS to match target mode (don't rely on `color-scheme` property)
   - Remove `@media (prefers-color-scheme: dark/light)` wrappers, keep their contents
   - CSS `color-scheme` property does NOT change `@media (prefers-color-scheme)` results

3. **Interactive element replacement:**
   - Canvas/WebGL animations → screenshot of element via Playwright, use as `<img>`
   - Video players → `<video autoplay muted loop>` with original CDN `src`
   - Complex SVG/interactive demos → placeholder or screenshot

4. **Serve locally:**
   ```bash
   python3 -m http.server 8799
   ```

### Step 4: Pixel Comparison

Take screenshots of both original and clone at identical viewport + color scheme:

```python
from PIL import Image
import numpy as np

orig = np.array(Image.open('original.png')).astype(float)
clone = np.array(Image.open('clone.png')).astype(float)
diff = np.abs(orig - clone)
pixel_avg = diff.mean(axis=2)

accuracy = (1 - diff.mean() / 255) * 100
within_5 = (pixel_avg < 5).mean() * 100

h, w = pixel_avg.shape
for i in range(3):
    for j in range(3):
        r = pixel_avg[i*h//3:(i+1)*h//3, j*w//3:(j+1)*w//3]
        print(f"  [{i},{j}]: {r.mean():.1f}")
```

**Targets:** 96%+ excellent, 94%+ good, regional diff >50 = investigate.

**CRITICAL**: Both screenshots MUST use same viewport, color scheme, and wait time.

### Step 5: Iteration

Fix in priority order: color scheme → background → grid/layout → fonts → interactive elements → spacing. Repeat Step 4→5 until target reached (max 5 rounds).

### Step 6: Package

After pixel accuracy target is met, generate the distributable unit:

1. **preview.png** — save the final clone viewport screenshot
2. **manifest.json** — write metadata:
   ```json
   {
     "name": "<slug>",
     "display_name": "<Site Name — Page Title>",
     "source_url": "<original URL>",
     "cloned_at": "<YYYY-MM-DD>",
     "accuracy": <number>,
     "color_scheme": "dark|light",
     "stack": "<Custom CSS|Tailwind + Next.js|...>",
     "tags": ["<descriptive tags>"],
     "files": ["index.html", "style.css", ...],
     "notes": "<known gaps or replacements>"
   }
   ```
3. **tokens.json** — extract design tokens from the CSS `:root` block:
   ```json
   {
     "color_scheme": "dark|light",
     "colors": { "background": "...", "foreground": "...", ... },
     "typography": { "font_primary": "...", "size_base": "...", ... },
     "layout": { "max_width": "...", "border_radius": "...", ... }
   }
   ```
4. **registry.json** — append entry to `clones/registry.json`
5. **Cleanup** — delete intermediate screenshots (diff heatmaps, iteration PNGs)

### Step 7: Deliver

Report to user:
- Pixel accuracy percentage
- Side-by-side screenshots (original vs clone)
- Clone path and available commands (`/clone-web use <slug>`)
- Known gaps

## Key Insights

- SVG `className` is `SVGAnimatedString` — use `el.getAttribute('class')` not `el.className.split()`
- YouTube iframes cause screenshot timeouts — remove before screenshotting
- Playwright defaults to `prefers-color-scheme: light` — always set explicitly
- Video `currentTime` must be set for frame to appear in screenshot
