# Skills 第二轮改造：按宿主能力执行，以证据判断完成

Approved 2026-09-05. Implementation branch: `codex/context-engineering-20260731`.
Baseline: main `b6aee12`, 51 public skills plus workspace caveman. Sources and
their interpretation are recorded in [the design](../design/context-engineering.md).

## Scope and invariants

Fast-forward the existing isolated worktree to main before editing; use isolated
submodule checkouts on `codex/skill-capability-20260905`. Preserve the primary
checkout, global installations, historical research, wiki data and artifacts.
Audit all owned entrypoints and execution references, including callers. Record
retain/rewrite/merge/delete decisions. Third-party/system skills are inventory
subjects only; do not edit vendor files.

Choose available native search/text/structured integrations for ordinary content,
browser/CUA for visual or interactive tasks, and scripts for batching, conversion
and caching. Keep identity, provenance, citation locators, formats and external
action permissions. Remove historic tool-failure folklore, fixed search chains,
step quotas and repeated approvals. Carry forward the user's authorization; ask
only when a missing choice materially affects results or scope. Reading does not
authorize archival, commit or publication. Preserve names, Chinese triggers,
supported host metadata, allowed-tools grants and invocation policies. Verify
proportionately to actual risk.

## Delivery batches

1. Documentation baseline and resource audit inventory.
2. Retrieval: web-fetcher and all unbox research/backfill/subtask references.
3. Consumers: LabMate paper/survey, no-more-fomo, transcribe, clone-web and slides.
4. Workflows: remaining LabMate roles/skills/hooks, Papermate and reviews.
5. Domain skills: writing, styles, plotting, weekly, selfOS and navigation.
6. Regression, isolated installation, release parity and migration report.

Web-fetcher keeps `fetch.py URL [-o FILE]` Markdown output and adds `--format json`
with `source_url`, `retrieved_at`, `backend`, `status`, `content_kind`, `content`,
`limitations`. Status: `ok`, `partial`, `blocked`, `unsupported`. Accept valid
short posts; reject login/errors/navigation shells. Keep caption timestamps and
parse formats correctly. Metadata-only video is partial; scripts cannot claim
native visual observation. References cover capability choice, adapters and media
evidence. Host-native tools are selected by the host, not simulated in Python.

Unbox retains namesake isolation, identity anchors, chronology, collaborators,
historical sources, incremental saves, dates and unresolved gaps. Search around
open questions, recheck identity conflicts/time-sensitive facts. Remove forced
search chains, personal paths, fixed concurrency and stale reliability rankings.
Video evidence separates self-report, observed behavior and inference with time
intervals and actual modality coverage. Delegate independent work only when
available/appropriate; avoid concurrent shared browser state; main-thread fallback.

Consumers distinguish speech, screen content and action sequences. Record viewed
intervals, missing modalities and continuity limits. Preserve read-paper packet
schema and formula/figure/page checks; abstract is not full text. Clone-web permits
any suitable browser while retaining same-viewport and interaction comparison.
Research-slides retains SD default profile, causal knowledge structure, black
Metropolis and PDF QA. FOMO keeps RSS/API batches, deduplication and selective
deep reads. selfOS keeps user quotes, analysis and external evidence separate;
only skill/execution instructions change, not records or formats.

## Four default LabMate handlers

- SessionStart: existing state, project knowledge and maintenance only; ordinary
  uninitialized directories are quiet.
- PostToolUse: silently record concrete changelog/docs/project-skill maintenance
  after successful code commits. Ignore failed operations and irrelevant docs-only
  commits; no per-tool reminders.
- PreCompact: one pending-maintenance summary per session; do not infer resolved
  knowhow from errors, and do not depend on the old knowhow reminder counter.
- PreToolUse: Git destructive-operation advisory, not a permission gate.

Remove arXiv confirmation, new-file brainstorming, analysis/monitor/survey
cross-sell injections. Closing responsibilities belong to owning skills. Preserve
host payload/output normalization and dual project-skill paths. Dedupe by session
ID, transcript path, then date bucket. Monitor remains one check; host schedules.

## Acceptance

Share public discovery among validator, installer and context audit; count workspace
entries separately. Parse quoted/multiline YAML; allow supported host fields. Walk
references, roles and generated templates. Invalid links/policies/required local
dependencies are errors; length/tool examples/imperative density are review clues.

Offline cases: short tweet; root/author replies/others/media; metadata-only video,
captions/no captions and timestamp preservation; CLI compatibility and JSON;
native-without-CLI and no-CUA fallback contracts; namesake/conflict/resume/video
citations; abstract/full-text and requested paper anchors; normal reads/docs/status
quiet; failed commands not complete; no-subagent/Claude role fallback and templates.

Live evaluation is separate from fixtures: short tweet, video demo, namesake
researcher and paper locator, old/new instructions at supported Light/Medium.
Record quality, elapsed time, calls, capability coverage and actual model/effort.
Use higher effort only for unresolved complex cases. Do not change global defaults.
Unavailable native/Claude/model runs remain explicitly unverified, never mock passes.

## Commits and release

Commit each changed submodule before the parent pointer. LabMate version 0.11.0;
other changed plugins advance one minor and synchronize version sources. All work
stays on the reform branch: no push, PR or main merge. Test temporary HOME/Codex
installations without changing active installs. Deliver audit dispositions,
reproducible test results, outstanding live cases and a rollback-aware migration
list (including old real web-fetcher directory and duplicate global/plugin skills).
