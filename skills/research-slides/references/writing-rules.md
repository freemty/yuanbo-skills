# Writing Rules

## Titles

- On a paper-overview slide, use the paper's real title, optionally followed by a short mechanism subtitle.
- On later slides, use a complete natural-language claim. The audience should understand the point from the title and visual alone.
- Avoid vague labels such as `Motivation`, `Overview`, or `Method`, and internal shorthand such as `T1`, `T2 x T3`, or unexplained acronyms.
- Do not repeat the title as the first body sentence.

## TLDR Lines

A TLDR is one sentence that answers:

1. What is the move?
2. Why does it help?
3. What does it cost or repair?

Examples:

- `Tree-causal masking keeps each draft branch conditioned on its own ancestors, turning extra draft budget into coherent candidate paths.`
- `Autoregressive across blocks; diffusion-style parallel denoising inside each block.`

Do not prefix a sentence with `Point:`, `Core bet:`, or `The key insight is`. Write the claim directly.

## Bullets

- Use bullets for decisions, failure modes, or ordered contrasts.
- Keep bullets parallel in grammar.
- Prefer two or three bullets. A longer list usually needs a table, a second slide, or spoken explanation.
- Avoid "this paper proposes..." unless the proposal itself is the point.
- Remove weak meta phrases: "it is worth noting", "interesting", "very important", "we can see".

## Formulas and metrics

- Include a formula only when it explains a decision, threshold, or trade-off that the audience will use later.
- Define every symbol in nearby plain language. One interpretable equation is better than the paper's full derivation.
- Keep metrics off the overview slide. Put one headline comparison and its conditions on the result slide.
- Separate a main result from an ablation: the former establishes performance; the latter tests why the design works.

## Endings

- Prefer one takeaway slide with four declarative sentences over repeated summary tables.
- Each sentence should carry a distinct level: pressure, method choice, trade-off, and practical implication.
- Do not introduce a new taxonomy or unexplained future direction in the conclusion.

## Tone

Use plain, technical English. Be precise rather than dramatic. Avoid slogan-like symmetry, repeated three-part structures, and uniformly polished section labels that make the deck sound machine-generated. Leave connective explanation to the presenter.
