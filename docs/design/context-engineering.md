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

LabMate keeps three lifecycle hooks:

- Session start: inject the current stage, experiment, and project-skill path.
- Pre-compact: provide one archival reminder.
- Pre-tool-use: guard destructive git/worktree operations.

Project initialization, experiment scaffolding, TODO mutation, and project
snapshots use deterministic scripts. The removed reminder and cross-sell hooks
must not be recreated unless a measured failure demonstrates their value.

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

The current public surface is expected to report `50/50 skills passed` and
`50 skills; 0 flagged`.

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

- `plugins/labmate/docs/papers/context-engineering-claude5-trq212.md` — primary
  source summary and LabMate implications.
- `docs/guides/skill-validation.md` — validator behavior and new-skill
  checklist.
- `docs/guides/codex-support.md` — platform installation and invocation
  boundaries.
