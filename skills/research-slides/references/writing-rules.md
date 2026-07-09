# Writing Rules

## Titles

- Make titles specific enough to carry the claim.
- Use paper titles for paper-overview slides when recognition matters.
- Avoid short vague titles such as "Motivation" or "Overview" unless the section context is already doing the work.
- Good pattern: `Paper Title: short mechanism phrase`.

## TLDR Lines

A TLDR should answer:

1. What is the move?
2. Why does it help?
3. What does it cost or repair?

Examples:

- `TLDR for T3: tree-causal masking keeps each parallel branch conditioned on its own ancestors, so extra draft budget becomes coherent candidate paths instead of branch-agnostic guesses.`
- `Autoregressive across blocks; diffusion-style parallel denoising inside each block.`

## Bullets

- Use bullets for decisions, failure modes, or ordered contrasts.
- Keep bullets parallel in grammar.
- Avoid "this paper proposes..." unless the proposal itself is the point.
- Remove weak meta phrases: "it is worth noting", "interesting", "very important", "we can see".

## Section Flow

Recommended order for efficient language modeling talks:

1. Serving phases and bottleneck.
2. Why parallel compute is tempting.
3. Method families and what causality they remove.
4. Core papers: motivation, method, result, ablation.
5. Systems and serving policy.
6. Takeaways and references.

## Tone

Use plain, technical English. Be precise rather than dramatic. Do not over-explain for the slide; leave spoken detail to the presenter.
