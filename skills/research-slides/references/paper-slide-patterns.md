# Paper Slide Patterns

## Core Paper

Use at least two slides:

1. Overview or method figure.
2. Main result or ablation.

Use three slides when the paper has a non-obvious motivation:

1. Why this problem exists.
2. Method figure.
3. Result or ablation.

## Secondary Paper

Use one slide:

- title is the paper title or method family
- one figure/table if available
- one TLDR sentence
- one citation line

## Literature Cluster

Use a taxonomy table:

| family | parallel move | causality returns via |
| --- | --- | --- |
| MTP | future heads in one pass | training or verification |
| diffusion LM | denoise many positions | refinement or block order |
| speculative decoding | draft many, verify once | target-side rejection sampling |

Keep this as a map, not a full explanation.

## Method Work

Minimum slide set:

- Problem: what current method cannot do.
- Method: paper figure or compact mechanism.
- Evidence: result table/plot.
- Ablation: why the design choice matters.

## Theory or Concept Work

Minimum slide set:

- Claim.
- Formalization or simple example.
- One figure/table from the paper.
- Limitation or implication.

## Backup

Move slides to backup when:

- the slide explains an implementation detail not needed for the main argument
- the figure is a useful reminder but does not change the audience's model
- the slide exists only to answer a likely question
