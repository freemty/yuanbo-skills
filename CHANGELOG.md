# Changelog

All notable changes to yuanbo-skills.

## 2026-07-09

### 新增
- **research-slides**: add a restrained research Beamer workflow with paper-native figures/tables, citation rules, source credits, and rendered PDF QA scripts.
- **docs/guides/research-slides.md**: document the workflow, Beamer/style boundary, file map, and verification loop.

### 变更
- **beamer-style**: add a `research` layout for black/gray paper talks, reading groups, and research surveys.

## 2026-05-25

### 新增
- **antigravity**: add Google Antigravity as third install target (`./install.sh --target antigravity`)
- **docs/install-antigravity.md**: full install guide for Antigravity (manual, single-skill, hooks, verify)

### 变更
- **README**: update intro to reflect three-platform support (Claude Code / Codex / Antigravity)
- **CLAUDE.md**: add antigravity target path, index new docs
- **AGENTS.md**: update for three-platform scope
- **docs/guides/codex-support.md**: expand to cover all three platforms

## 2026-05-24

### 变更
- **README**: add papermate, swiss-knife-design, transcribe to skill tables; update Codex skill keys (add papermate sub-skills); update repo structure counts
- **CLAUDE.md**: add swiss-knife-design, transcribe to inline directories list
- **.codex/INSTALL.md**: sync skill keys + add papermate to plugin manifest list
- **scripts/generate_readme.py**: add papermate, swiss-knife-design, transcribe to SKILLS dict

### 其他
- **submodules**: bump unbox-skills (entity subagent prompt), no-more-fomo (process/sources), papermate (.codex-plugin), selfos (5/08-5/24 batch)

## 2026-05-19

### 新增
- **transcribe**: add audio transcription skill (speech-to-text via Whisper)
- **papermate**: add as submodule (`freemty/papermate`) — paper writing QA pipeline with 6 sub-skills (compile-check, figure-qa, paper-writing-qa, pre-submit-challenge, section-guard, sync-paper)
- **.agents/plugins/marketplace.json**: Codex local plugin marketplace index

### 变更
- **install.sh**: expand skill discovery to selfos project skills + Codex marketplace metadata

## 2026-05-11

- **CLAUDE.md**: add papermate to submodules list
- **labmate**: bump pointer — CLAUDE.md sync

## 2026-05-09

- **labmate**: bump pointer — unified update-docs + knowledge maintenance hooks

## 2026-04-30

### 新增
- **swiss-knife-design**: add personal web design system skill (project pages, dashboards, leaderboards, slides with consistent visual identity)

## 2026-04-26

### 新增
- **caveman**: add ultra-compressed communication mode skill (lite/full/ultra + wenyan variants)
- **ci**: add SKILL.md contract validation workflow (`validate_skills.py` + GitHub Actions)
- **docs/install-codex.md**: Codex CLI install guide, skill keys, manual install/uninstall

### 变更
- **AGENTS.md**: new file — Codex-specific project guidance
- Codex support across all plugins: `.codex-plugin/plugin.json` manifests for labmate, meta-audit, paper-review, unbox-skills
- **docs**: add Related repos section (ai-dotfiles, cc-switch)

### 其他
- Archive sjh-skills and evolve_bench design philosophies in `docs/plugins/`
- **unbox**: bump pointer — output to `~/outputs/unbox/` per convention

## 2026-04-25

- **docs**: archive sjh-skills and evolve_bench philosophies

## 2026-04-23

- **meta-audit/hook-recipes**: add sub-skill with 10 curated hook templates (PostToolUse type-check/lint/format, PreToolUse guards, project-level templates) — closes the "audit finds gap → now what?" loop
- **meta-audit**: update plugin.json to register hook-recipes, update SKILL.md action template to reference `/hook-recipes`, update README with recipes table

## 2026-04-22

### skills.sh Publishing (Batch 1)

Standardized 6 skills for skills.sh and pushed to independent GitHub repos:

- **paper-storyteller**: README rewrite (skills.sh template), LICENSE added → `freemty/paper-storyteller`
- **paper-style**: install header unified to "Via skills.sh", LICENSE added → `freemty/paper-style`
- **beamer-style**: README rewrite, soften paper-style sister-skill ref, LICENSE added → `freemty/beamer-style`
- **writing-agents**: new independent repo created from inline directory → `freemty/writing-agents`
- **cc-navigator**: repo flattened (SKILL.md to root), README rewrite, Chinese availability tags → English → `freemty/cc-navigator`
- **meta-audit**: full English translation (SKILL.md + README + sources.md), repo flattened, personal paths removed from collect.sh → `freemty/meta-audit`
- **docs/guides/skills-sh-publishing.md**: publishing standard — repo structure, SKILL.md/README templates, standardization checklist
- cc-navigator and writing-agents converted from inline directories to submodules

### Other

- **paper-review**: move from `skills/` to `plugins/` (has two skills: paper-review + review-review = upstream/downstream plugin)
- **review-review**: recover from `freemty/paper-review-plugin`, add as nested skill in paper-review
- **install.sh**: extend nested skill discovery to `skills/` (was plugins-only)
- **flipradio-write-skill**: move from `plugins/` to `skills/` (pure skill, no plugin manifest)
- **scripts/generate_readme.py**: auto-generate README skill tables from SKILLS dict, replace between `<!-- BEGIN/END SKILLS -->` markers
- **convention**: skill vs plugin 分类原则 — 同功能多入口=skill，流程上下游独立协作=plugin
- **paper-review**: convert from inline directory to submodule (`freemty/paper-review`)
- **CLAUDE.md**: create project-level guidance for future Claude Code sessions
- Clean up stale root files (`TODO.md`, `weekly-report-2026-03-26.md`)
- **docs/plugins**: expand huggingface-skills notes (11 skills 清单 + 工程实践借鉴 + gstack 条目)
- **docs/outputs-convention**: establish `~/outputs/` convention for skill output directories + symlink compatibility
- **housekeeping**: remove 8 scattered submodule copies from `~/code/projects/` (now only in yuanbo-skills submodules)
- **housekeeping**: consolidate 6 output directories into `~/outputs/` (no-more-fomo, unbox, weekly-report, zhihu-articles, gemini-exporter, maqianzu-wiki)
- **selfos**: merge public template + private worktree into single `~/selfOS/` repo, update README clone path
- **selfos**: ⚠️ `worktree remove --force` 导致 gitignored 源数据丢失（notion/claude/gemini exports），需重新导出
- **docs/knowhow**: add 3 runbooks (worktree-to-standalone, consolidate-output-dirs, cleanup-scattered-submodules)

## 2026-04-21

- **paper-review**: add multi-role academic peer review skill (4 expert agents, venue-formatted output)
- **cc-navigator**: move from meta-audit plugin to this repo as inline skill
- Migrate 8 skills to independent submodules: flipradio-write-skill, paper-storyteller, selfos, meta-audit, no-more-fomo, paper-style, beamer-style, labmate, unbox-skills
- Add plugin manifests to meta-audit and unbox-skills
- Unify all skill descriptions to CSO-compliant format
- Overhaul README with categorized skill table
- Remove non-skill directories (diagrams, docs, zhihu-articles, notebooklm, frontend-slides)

## 2026-04-20

- **meta-audit**: add AI automation maturity audit skill (L0-L5 scoring)

## 2026-04-17

- **unbox-skills**: add unbox-backfill and unbox-to-wiki skills
- **unbox**: systematic coverage improvement for Chinese biographical info

## 2026-04-16

- **web-fetcher**: improve fetch.py robustness and SKILL routing

## 2026-04-07

- **yuanboizer-zh**: add personal style polisher skill (6 style dimensions + scoring + example pairs)

## 2026-03-29

- **flipradio-write / flipradio-polish**: add guided writing + article polishing skills
- Remove outdated third-party skills (keep only personal skills)
- Remove slides-dispatch, commit-changelog, clash-split-routing

## 2026-03-27

- **paper-storyteller**: add narrative-driven academic paper writing skill

## 2026-03-25

- **no-more-fomo**: deep layer pipeline, HTML template, bilingual output
- **cc-navigator**: replace old claude-code-best-practices entry

## 2026-03-24

- Initial monorepo with 17 original skills and install.sh
