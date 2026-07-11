# Paper Slide Patterns

## Core Paper

Use 3-5 substantive slides, allocated by argumentative importance rather than paper-section count:

1. Motivation or prior failure, only when it is non-obvious.
2. Paper overview: exact title, source-native method figure, one TLDR.
3. Main result: original table or plot, one headline comparison with conditions.
4. Ablation or application: evidence that the distinctive design matters in practice.
5. Limitation or system consequence, only when it changes the audience's conclusion.

Do not merge the main result and ablation merely to save a page: they answer different questions. Crop evidence to the comparison being discussed and keep full tables in backup.

## Secondary Paper

Use one slide:

- exact paper title;
- one source-native method figure or result;
- one TLDR sentence stating the optimization and consequence;
- one clickable citation line.

If the talk cannot support result or ablation evidence, label the work as a related method or outlook instead of presenting it as a validated core result.

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

For experimental systems work, add one application or deployment slide when the system behavior is part of the contribution. For a short talk, move scheduler and implementation details to backup before removing the result or ablation.

## Theory or Concept Work

Minimum slide set:

- Claim.
- Formalization or simple example.
- One figure/table from the paper.
- Limitation or implication.

Use formulas selectively. A formula belongs on the slide only if it clarifies the mechanism or the condition under which the claim holds.

## Backup

Move slides to backup when:

- the slide explains an implementation detail not needed for the main argument
- the figure is a useful reminder but does not change the audience's model
- the slide exists only to answer a likely question
