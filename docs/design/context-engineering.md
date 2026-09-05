# Context Engineering Architecture

## Overview

This repository shares one Agent Skills source across Claude Code, Codex, and
Antigravity. The design goal is behavioral parity without forcing every host,
workflow, and reference into the model's always-loaded context.

The governing rule is: put each concern in the narrowest layer that can express
and verify it.

## Layer ownership

| Layer | Owns | Must not own |
| --- | --- | --- |
| Skill description | Invocation triggers and user intent | Workflow summaries or implementation steps |
| `SKILL.md` body | Judgment, routing, safety boundaries, output contract | Long tutorials, host-specific tool names, mechanical CRUD |
| `references/` | Domain knowledge, style guides, rubrics, detailed fallbacks | Discovery metadata or duplicated skill frontmatter |
| `scripts/` and tools | Deterministic file/state mutations | Open-ended research judgment |
| Tests and rubrics | Observable acceptance boundaries | Hidden implementation preferences |
| Host metadata | Invocation syntax, named agents, explicit-invocation policy | Portable workflow logic |
| Project memory/docs | Durable project facts, findings, and pitfalls | Skill catalogs repeated in every session |

References are loaded only after the entrypoint has identified the relevant
mode. Scripts expose plan/apply/check or narrow CRUD interfaces where preview,
idempotency, and conflict detection matter.

## LabMate contract

LabMate contains 12 portable skills. Claude Code additionally distributes five
named agents; Codex and other hosts do not need generated agent definitions.
Agent-dependent workflows use the following fallback:

1. Use the matching named agent when the host provides it.
2. Otherwise use an ordinary isolated subagent with the same role body.
3. If subagents are unavailable, apply the same role contract in the main
   thread.

`read-paper` may delegate analysis, but the main thread retains user follow-up,
saving, and archival. Slide generation is a separate explicit action and routes
research talks through `research-slides`.

The September baseline has 13 handlers across five lifecycle events (the August
revision restored them). The second-round target is four active handlers:
project state at session start, silent post-commit maintenance recording, one
pending-maintenance summary before compaction, and a Git-operation advisory.
The advisory is not a permission interceptor. Routine reads, new files and
ordinary directories must not generate initialization or cross-skill reminders.
Project initialization, experiment scaffolding, TODO mutation, and snapshots
remain deterministic script operations.

## Monitoring and scheduling

`monitor` is one invocation producing one current-state snapshot. Recurrence is
owned by the host:

- Codex App: create a Scheduled Task when persistent monitoring is wanted.
- Other hosts: repeat manually or use a documented native scheduler.
- Use a loop command only when that host explicitly provides one.

The skill must not claim that a background monitor exists when only a one-shot
check ran.

## Installation and cache boundaries

Compatibility must be checked at four independent layers:

1. Source files in this repository.
2. Plugin and marketplace metadata.
3. Installed plugin cache and enabled state.
4. Global or workspace skill symlinks.

Codex should install plugin-owned skills through the marketplace. Legacy global
symlinks are an explicit fallback and must not coexist with the same plugin
skills. LabMate uses `package.json.version` as the canonical version; release
checks keep both plugin manifests and README badges synchronized.

Source correctness does not prove installed correctness. A smoke test must use a
temporary Codex home and verify that each plugin skill appears exactly once.

## Research-slide default

`research-slides` uses the Speculative Decoding reference profile by default:
the restrained black Metropolis visual system, its causal act map, governing
dials, evidence cadence, and cross-topic slot mapping. The reference is a
structural and visual contract, not permission to copy topic-specific claims or
content.

## Verification

Run from the outer repository:

```bash
python3 scripts/validate_skills.py
bash tests/test-context-audit.sh
bash tests/test-install.sh
python3 skills/research-slides/scripts/test_template.py
```

The September baseline has 51 public entries plus a workspace-only `caveman`.
Discover counts from the shared inventory; do not hardcode them in tests.
Context review warnings locate debt; invalid references, policies and required
dependencies are errors. Static checks do not establish model behavior.

For LabMate:

```bash
bash plugins/labmate/tests/test-hooks.sh
bash plugins/labmate/tests/test-platform-compat.sh
bash plugins/labmate/tests/test-context-contract.sh
bash plugins/labmate/tests/test-scripts.sh
bash plugins/labmate/tests/test-codex-plugin-smoke.sh
python3 plugins/labmate/scripts/sync-version.py --check
```

Any future simplification must preserve representative behavior through these
tests. Passing static checks alone is not evidence that an installed cache or
native host payload is correct.

## Sources

### September 2026 capability review

- **Author experience, 2026-09-04:** [Victor Nunez's post](https://x.com/victornunez/status/2095895077381972247)
  recommends reviewing instruction files and reasoning effort during the Astra
  rollout. His favorable experience with Light is an observation, not a universal
  quality guarantee. Replies by other accounts are not the author's thread.
- **Official guidance, retrieved 2026-09-05:** [GPT-6 prompting guidance](https://developers.openai.com/api/docs/guides/latest-model#prompting-best-practices)
  describes stronger sensitivity to skills, excess clarification and testing,
  and task-dependent delegation. It recommends auditing accessible instructions,
  honoring user intent and calibrating verification to the change.
- **Repository decisions:** choose text/structured, visual/browser, or scripted
  execution from the task and available capabilities. Keep provenance, identity,
  output schemas and authorization boundaries. Audit called references alongside
  entrypoints. Retain existing effective reasoning settings; compare supported
  Light/Medium configurations before recommending changes. CUA availability does
  not prove that video frames, audio or continuous actions were observed.

Implementation scope, hook migration, evidence contracts, acceptance scenarios,
and isolated-install delivery are tracked in
[`2026-09-05-skill-capability-refactor.md`](../specs/2026-09-05-skill-capability-refactor.md).

- `plugins/labmate/docs/papers/context-engineering-claude5-trq212.md` — primary
  source summary and LabMate implications.
- `docs/guides/skill-validation.md` — validator behavior and new-skill
  checklist.
- `docs/guides/codex-support.md` — platform installation and invocation
  boundaries.
