# Paper Slide Patterns

## Core Paper

For an empirical anchor paper, 3-5 substantive slides are a useful starting point,
not a minimum. Allocate by duration and argumentative importance:

1. Motivation or prior failure, only when it is non-obvious.
2. Paper overview: exact title, source-native method figure, one TLDR.
3. Main result: original table or plot, one headline comparison with conditions.
4. Ablation or application: evidence that the distinctive design matters in practice.
5. Limitation or system consequence, only when it changes the audience's conclusion.

Main result and ablation answer different questions. They can share a short-talk
page if both remain legible and correctly interpreted; otherwise split them.
Crop evidence to the discussed comparison and keep full tables in backup.

## Secondary Paper

Use one slide:

- exact paper title;
- one source-native method figure or result;
- one TLDR sentence stating the optimization and consequence;
- one clickable citation line.

If an empirical claim lacks its supporting test, narrow or label that claim.
Theoretical validation instead uses assumptions and proof; proposal status stays explicit.

## Literature Cluster

Use a taxonomy table:

| family | parallel move | causality returns via |
| --- | --- | --- |
| MTP | future heads in one pass | training or verification |
| diffusion LM | denoise many positions | refinement or block order |
| speculative decoding | draft many, verify once | target-side rejection sampling |

Keep this as a map, not a full explanation.

## Method Work

Empirical argument obligations (not one required page per item):

- Problem: what current method cannot do.
- Method: paper figure or compact mechanism.
- Evidence: result table/plot.
- Causal analysis: test the distinctive choice when claiming it causes the gain.

For experimental systems work, include application/deployment evidence when it
is part of the contribution. In a short talk, remove peripheral claims and
implementation detail before weakening evidence for the claims retained.

## Theory or Concept Work

Theory argument obligations (combine or split to match the audience):

- Objects and assumptions.
- Precise theorem or bounded claim.
- Proof or labeled proof sketch, plus a simple example when useful.
- Scope, counterexample or implication.

No experimental ablation or paper figure is required. A displayed identity may
be the dominant visual. An example illustrates a theorem; it does not prove it.

Use formulas selectively. A formula belongs on the slide only if it clarifies the mechanism or the condition under which the claim holds.

## Backup

Move slides to backup when:

- the slide explains an implementation detail not needed for the main argument
- the figure is a useful reminder but does not change the audience's model
- the slide exists only to answer a likely question
