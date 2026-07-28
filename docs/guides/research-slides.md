# Research Slides Skill

`research-slides` builds research talks as audience-model updates rather than decorated paper summaries. Its default starter now matches the current Speculative Decoding deck: the bundled black palette plus minimal Metropolis layout, with sparse language, source-native evidence, standard clickable citations, and rendered PDF QA.

## Four modes

| Mode | Use it for | Default story |
| --- | --- | --- |
| `paper` | one anchor paper | why it should work -> prior failure -> method -> main result -> ablation/application |
| `idea` | a concept, hypothesis, or proposal | define object -> observed pressure -> failed obvious fix -> hypothesis -> evidence -> evaluation |
| `survey` | a field trend or paper cluster | common pressure -> comparison lens -> evidence ladders -> disagreements -> frontier |
| `repair` | an existing `.tex`/PDF deck | baseline -> page/source map -> minimal patch -> neighbor regression -> full scan |

The mode changes the story, not the visual identity. New decks use `beamer-colors.tex` with the black theme and `layout-metropolis.tex`; repairs preserve the existing deck's template.

## Design contract

- Cover: title, speaker, and date only.
- Add a table of contents after the cover for multi-section talks.
- Define an unfamiliar process before presenting its bottleneck or solution.
- Give each slide one claim and one dominant source-backed object.
- Paper overview: exact paper title, original method figure, one TLDR; no metric dump.
- Core paper: method, main result, and ablation/application are separate evidence obligations.
- Secondary paper: one source-native figure plus one TLDR and citation.
- Deck surface: white canvas with black/gray type and rules; source figures may retain their native color.
- Historical slide corpora inform storytelling and QA, not the active palette. New explicit preferences and the named current reference deck override older visual habits.
- Avoid filler prose, decorative cards, red accents, gratuitous arrows, dashed networks, and internal shorthand in titles.
- End with one four-sentence takeaway slide and one or two dense reference pages.

## Source contract

Prefer evidence in this order:

1. figure/table from arXiv source;
2. high-resolution crop from the paper PDF;
3. authoritative project page or teaching blog;
4. minimal redraw only when the original cannot teach the point.

Every external asset must appear in `source-manifest.tsv` with its exact URL, figure/table number, page, crop, and supported claim. Slide footnotes use `Author et al., Title, arXiv:id`; each source gets its own clickable line.

## Initialize a deck

```bash
python3 skills/research-slides/scripts/init_research_deck.py /tmp/my-talk
```

This creates:

- `main.tex`;
- the default `beamer-colors.tex` and `layout-metropolis.tex` pair;
- a legacy `layout-research.tex` compatibility option;
- `source-manifest.tsv`;
- `figs/`.

No separate `beamer-style` install is required. Use `beamer-style` only when changing to another theme or layout; do not replace the default pair unless requested.

## Multi-agent workflow

For a substantial talk, run read-only agents in parallel for story, evidence, style history, and rendered QA. Evidence agents return a strict record: claim, source URL, figure/table number, page, crop, and caveat. Keep one coordinator as the only writer of `main.tex`; do not let multiple agents reorder a deck concurrently.

## Deterministic QA

```bash
python3 skills/research-slides/scripts/check_deck.py path/to/main.tex --pages 7,12-14
```

The checker:

1. runs XeLaTeX twice;
2. fails on LaTeX errors, undefined references/citations, overfull boxes, and missing static assets;
3. reports hyperlink warnings and dynamic asset paths;
4. renders selected pages into a clean directory.

The final step is visual: inspect changed pages and adjacent pages for overlap, blur, clipping, unreadable paper labels, citation collisions, and broken rhythm. Compilation success alone is not completion.

## File map

| Path | Purpose |
| --- | --- |
| `skills/research-slides/SKILL.md` | compact mode router and hard gates |
| `skills/research-slides/references/story-modes.md` | paper, idea, survey, and repair story spines |
| `skills/research-slides/references/paper-slide-patterns.md` | evidence allocation for core and secondary papers |
| `skills/research-slides/references/visual-style.md` | visual hierarchy and anti-AI-slop rules |
| `skills/research-slides/references/writing-rules.md` | titles, TLDRs, formulas, metrics, and endings |
| `skills/research-slides/references/citation-and-source-credit.md` | clickable citation and source format |
| `skills/research-slides/references/figure-extraction-workflow.md` | source-native asset workflow |
| `skills/research-slides/references/multi-agent-workflow.md` | read-only agent split and merge gate |
| `skills/research-slides/references/qa-workflow.md` | baseline and rendered regression loop |
| `skills/research-slides/assets/` | self-contained starter layout, deck, and source manifest |
| `skills/research-slides/scripts/` | initialization, cropping, compilation, and rendering tools |

When the house style changes in a real deck, update the relevant reference file rather than expanding `SKILL.md`. Keep the router short and the behavioral rules testable.
