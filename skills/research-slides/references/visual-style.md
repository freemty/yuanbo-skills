# Visual Style

## Canonical research mode

- The named visual reference is the current Speculative Decoding deck. New decks use its exact pairing: `beamer-colors.tex` with the `black` theme and `layout-metropolis.tex`.
- The resulting surface is 16:9, white canvas, black/gray type and rules, no accent color, left-aligned titles, automatic section pages, and a thin bottom progress bar.
- Historical Keynote/PPT corpora are useful for recovering story order, paper-reading habits, and progressive builds. Do not infer the current visual template from their color frequency, cover collages, logos, or decoration.
- Resolve conflicts in this order: newest explicit user preference, current named reference deck, then historical corpus. Mature preferences override earlier habits.
- Source-native paper figures may retain their colors; the surrounding slide should remain neutral.

## Visual hierarchy

- Give every slide one dominant object: a paper figure, result table, formula, or short contrast.
- Let the title make the claim and let the visual provide the evidence. Do not restate both in a paragraph.
- Keep enough white space that the evidence can be read from the back of a room and in a phone PDF preview.
- Use two columns only when the comparison itself is the point. Do not shrink two unrelated ideas merely to fill the canvas.

## Surface

- Keep the deck surface white, black, and gray.
- Avoid red accents, multicolor section coding, gradients, blobs, icon clusters, thick borders, nested cards, and filler boxes.
- Do not add prose, color, or a diagram because a slide feels empty. Empty space is acceptable when the claim is clear.
- Avoid visible containers around ordinary prose. A rule, aligned label, or whitespace usually provides enough structure.
- Do not restore red emphasis, cover collages, or organization logos unless the user explicitly asks to match an older deck.

## Layout

- Keep title, rule, body, footnote, and progress bar aligned across slides.
- Use the bundled Metropolis title page, frame-title rule, section-page behavior, and footline by default. `layout-research.tex` remains a compatibility option, not the default.
- Use wide paper figures when the figure is the point. Use two columns only when the comparison is the point.
- Use arrows only when both endpoints are named and the arrow expresses a dependency the audience must follow.
- Avoid decorative dashed paths, arbitrary flow networks, and hand-drawn replacements for usable paper figures.
- Use tables for taxonomy and mechanism contrast; use paper screenshots for evidence.
- Do not substitute an adjacent systems metric for the concept being taught. For example, define prefill and decode with a process figure before showing a serving-throughput chart.
- Put backup material after References or mark the frame `noframenumbering`.
- Do not spend a blank section-divider page on a section with only one substantive slide.
- Limit progressive builds to two or three slides and make the newly revealed step visually unambiguous. Do not create long runs of near-duplicate archival pages.

## Density

- Main slides: one sentence plus figure/table is often enough.
- A slide should usually have either bullets or a figure, not both at full density.
- If text competes with the paper figure, move the text into a one-line TLDR.
- Crop a full paper table to the rows and columns that prove the claim; keep the full table in backup.
- If labels in a rendered figure cannot be read at normal slide scale, the figure is not ready.
- References can be dense; main slides should not.

## Common Fixes

- If a figure feels blurry, extract from arXiv source or render at 250-400 dpi.
- If a paper figure has too much white margin, crop whitespace before placing it.
- If a slide has many arrows, delete any arrow whose dependency is not named in text.
- If citations collide with content, reduce content or split the slide. Do not hide the source or move it into speaker notes.
- If a full-deck screenshot looks uniformly busy, remove one object from every dense slide before changing font size.
