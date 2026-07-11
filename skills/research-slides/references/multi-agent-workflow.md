# Multi-Agent Workflow

Use parallel agents when a deck covers several papers, needs historical style recovery, or requires figure/result extraction from many sources. Keep a small repair local.

## Read-only audit split

Run independent agents for:

- **Story:** test the causal spine against the target audience.
- **Evidence:** extract the method figure, main result, ablation, and exact claim from each core paper.
- **Style:** separate narrative conventions from visual conventions. Use historical corpora to recover story habits; use only the newest explicit preference or named reference deck to infer the current visual system.
- **QA:** inspect rendered pages for overlap, clipping, blur, density, and citation collisions.

Ask each evidence agent to return: `claim, source URL, figure/table number, page, crop recommendation, caveat`.

## Write ownership

- Keep one coordinator as the only writer of `main.tex` and shared layout files.
- Agents may create disjoint source notes or figure crops only when their file ownership is explicit.
- Never let multiple agents reorder the same deck concurrently.
- Continue local work while agents run; wait only when their result blocks the next decision.

## Merge gate

Before editing, reconcile agent outputs into one storyboard. Reject a suggestion that lacks a source, does not change the audience's model, or duplicates another slide. Never choose a palette or cover treatment merely because it appears frequently in older decks.
