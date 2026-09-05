# Story Modes

## Shared story grammar

Treat a talk as a sequence of audience-model updates, not a list of papers. Build each slide from:

| Field | Question |
| --- | --- |
| Audience question | What must the listener understand next? |
| Claim | What one sentence should they repeat? |
| Evidence | Which figure, table, formula, or example proves it? |
| Source | Where can they inspect the claim? |
| Spoken bridge | Why does the next slide now become necessary? |

Define unfamiliar objects before bottlenecks; explain the bottleneck before the technique. Open with a trade-off when it governs the rest of the talk, then recover it in the final synthesis without repeating the same slide.

## `idea` mode

Use for a concept, research proposal, mechanism, or motivation-first explanation.

Default spine:

1. Define the process or object with a direct teaching figure.
2. Show a supported bottleneck/fact, the question to explain, or an explicitly untested concern.
3. Explain the relevant limitation when known; do not invent a failed baseline.
4. State the central hypothesis or trade-off.
5. Present the proposed mechanism or method families.
6. Use papers as evidence, not as the section structure.
7. End with implications, falsifiers/evaluation, and the few takeaways the talk earns.

Do not invent results for proposals. Label observations, hypotheses, expected
outcomes and planned evidence separately. Without measurements, present the
pressure as a concern to investigate, not an observed bottleneck. A proposal's
ending states what test could reject the idea, not why it already wins.

## `paper` mode

Use for one anchor paper. Allocate pages by argumentative importance, not section count.

Empirical default spine (for theory, use the theory obligations in `paper-slide-patterns.md`):

1. Why the idea should work.
2. What prior methods fail to do.
3. Paper overview: real paper title + core method figure + one TLDR.
4. Main result: original table/plot + one headline result with conditions.
5. Ablation/application: evidence that the distinctive design matters.
6. Limitation and what the paper changes for the field.

Core papers often use 3-5 substantive slides, but duration and evidence determine
the allocation. Skip implementation detail unless it changes the contribution.
Keep an overview focused; a short talk can combine a mechanism and one interpretable result.

## `survey` mode

Use for multiple papers or a trend.

Default spine:

1. Define scope, audience question, and inclusion boundary.
2. Introduce the common pressure or trade-off.
3. Build a method-family map using one consistent comparison lens.
4. Give core works full evidence; give supporting works one method-figure + TLDR slide.
5. Compare disagreements, missing evidence, and the current frontier.
6. End with one synthesis slide, not repeated taxonomies.

Do not organize the whole talk chronologically unless chronology itself explains the field.

## `repair` mode

Use for an existing deck.

1. Inspect the source, git state, and compiled PDF before editing.
2. Map requested PDF pages to source frames.
3. Preserve the established template and unrelated user changes.
4. Patch the smallest coherent set of frames/assets.
5. Recompile and inspect changed pages plus their neighbors.
6. Run a final full-deck scan for page count, references, missing assets, and visual rhythm.
7. Keep the deliverable PDF synchronized with the verified source. A temporary QA copy is acceptable, but do not leave a tracked or user-facing PDF stale unless the user explicitly requested source-only edits.

Do not replace a user's visual system with the starter template during repair.
