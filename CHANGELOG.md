# Changelog

All notable changes to yuanbo-skills.

## 2026-04-22

- **flipradio-write-skill**: move from `plugins/` to `skills/` (pure skill, no plugin manifest)
- **scripts/generate_readme.py**: auto-generate README skill tables from SKILLS dict, replace between `<!-- BEGIN/END SKILLS -->` markers
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
