# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

A monorepo of personal Claude Code skills, plugins, and projects. Organized into three top-level directories by type.

## Repo Layout

```
skills/          Single-skill directories (each has SKILL.md)
plugins/         Multi-skill plugins (may have .claude-plugin/, nested skills)
projects/        Standalone projects (selfos)
docs/            Plugin notes, knowhow, conventions
scripts/         Build & validation scripts
```

Skills are installed by `install.sh`, which symlinks every directory containing a `SKILL.md` (in `skills/` and `plugins/`, including nested) into `~/.claude/skills/`.

**Submodules** (have their own GitHub repo under `freemty/`):
- skills: beamer-style, no-more-fomo, paper-review, paper-storyteller, paper-style
- plugins: flipradio-write-skill, labmate, meta-audit, unbox-skills
- projects: selfos

**Inline directories** (tracked directly in this repo):
- skills: cc-navigator, web-fetcher, weekly-report, writing-agents, yuanboizer-zh

## Common Operations

```bash
# Clone with all submodules
git clone --recurse-submodules git@github.com:freemty/yuanbo-skills.git

# Install skills (symlink to ~/.claude/skills/)
./install.sh

# Update all submodules to latest
git submodule update --remote --merge

# Add a new skill as submodule
git submodule add git@github.com:freemty/<name>.git skills/<name>

# Add a new plugin as submodule
git submodule add git@github.com:freemty/<name>.git plugins/<name>
```

## Skill Anatomy

Each skill directory must contain:
- `SKILL.md` — frontmatter (`name`, `description`) + full skill instructions. The `description` field is what triggers Claude Code to invoke the skill.
- `README.md` — human-facing docs for the GitHub repo page.
- `references/` (optional) — supporting data files the skill reads at runtime.

## Docs

- `docs/plugins/landscape.md` — 插件总览索引（类似 labmate 的 papers/landscape.md）
- `docs/plugins/{name}.md` — 每个插件/skill/MCP server 的独立笔记
- `docs/outputs-convention.md` — Skill 产出物目录约定（`~/outputs/` 结构 + symlink 兼容）

## Knowhow

- `docs/knowhow/infrastructure/` — Servers, networking, disk, GPU issues
- `docs/knowhow/toolchain/` — CLI tools, docker, conda/pip, framework tips
- `docs/knowhow/debug-solutions/` — Error investigation paths and fixes
- `docs/knowhow/runbooks/` — Step-by-step operational procedures

## Conventions

- Skill descriptions use the CSO (Context-Situation-Outcome) format for triggering: describe *when* to use the skill, not *what* it does.
- README.md follows a consistent structure: title, one-liner, When to Use, Usage, Install (via `npx skills add` and manual), License.
- Submodule commits in this repo track pinned versions. Run `git submodule update --remote` to advance, then commit the pointer.
- After renaming/moving a directory, check for broken symlinks: `find ~/.claude/skills -maxdepth 1 -type l ! -exec test -e {} \; -print`
