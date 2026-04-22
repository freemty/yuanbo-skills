# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

A monorepo of personal Claude Code skills. Each top-level directory is one skill — either a git submodule (independent repo) or an inline directory tracked directly in this repo.

## Repo Layout

Skills are installed by `install.sh`, which symlinks every directory containing a `SKILL.md` into `~/.claude/skills/`. Directories without `SKILL.md` (like `labmate`, `meta-audit`, `selfos`) are plugin/project repos included as submodules but not symlinked as skills.

**Submodules** (have their own GitHub repo under `freemty/`):
beamer-style, flipradio-write-skill, labmate, meta-audit, no-more-fomo, paper-review, paper-storyteller, paper-style, selfos, unbox-skills

**Inline directories** (tracked directly in this repo):
cc-navigator, web-fetcher, weekly-report, writing-agents, yuanboizer-zh

## Common Operations

```bash
# Clone with all submodules
git clone --recurse-submodules git@github.com:freemty/yuanbo-skills.git

# Install skills (symlink to ~/.claude/skills/)
./install.sh

# Update all submodules to latest
git submodule update --remote --merge

# Add a new skill as submodule
git submodule add git@github.com:freemty/<name>.git <name>

# Convert an inline directory to submodule:
# 1. Create repo on GitHub
# 2. cd <dir> && git init && git remote add origin ... && git add -A && git commit && git push
# 3. Back in root: git rm -rf <dir> && git submodule add <url> <dir>
# 4. Restore files: cd <dir> && git restore .
```

## Skill Anatomy

Each skill directory must contain:
- `SKILL.md` — frontmatter (`name`, `description`) + full skill instructions. The `description` field is what triggers Claude Code to invoke the skill.
- `README.md` — human-facing docs for the GitHub repo page.
- `references/` (optional) — supporting data files the skill reads at runtime.

## Conventions

- Skill descriptions use the CSO (Context-Situation-Outcome) format for triggering: describe *when* to use the skill, not *what* it does.
- README.md follows a consistent structure: title, one-liner, When to Use, Usage, Install (via `npx skills add` and manual), License.
- Submodule commits in this repo track pinned versions. Run `git submodule update --remote` to advance, then commit the pointer.
- After renaming/moving a directory, check for broken symlinks: `find ~/.claude/skills -maxdepth 1 -type l ! -exec test -e {} \; -print`
