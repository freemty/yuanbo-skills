# Multi-Platform Support Guide

This repo supports Claude Code, OpenAI Codex CLI, and Google Antigravity from the same skill and plugin sources. All three platforms use the Agent Skills open standard (agentskills.io) — the same `SKILL.md` files work everywhere without modification.

## Overview

Each platform discovers skills from a different directory:

| Agent | Skill directory | Install command |
|-------|-----------------|-----------------|
| Claude Code | `~/.claude/skills/` | `./install.sh --target claude` |
| Codex CLI | `~/.agents/skills/` | `./install.sh --target codex` |
| Google Antigravity | `~/.gemini/antigravity/skills/` | `./install.sh --target antigravity` |
| All three | all directories | `./install.sh --target all` |

The default remains Claude-compatible:

```bash
./install.sh
```

## Codex Installation

For a fresh Codex install:

```bash
git clone --recurse-submodules https://github.com/freemty/yuanbo-skills.git ~/.codex/yuanbo-skills
cd ~/.codex/yuanbo-skills
./install.sh --target codex
```

Restart Codex after installation so it reloads `~/.agents/skills/`.

## Antigravity Installation

For a fresh Google Antigravity install:

```bash
git clone --recurse-submodules https://github.com/freemty/yuanbo-skills.git ~/.antigravity/yuanbo-skills
cd ~/.antigravity/yuanbo-skills
./install.sh --target antigravity
```

Restart Antigravity (or `agy` CLI) after installation so it reloads `~/.gemini/antigravity/skills/`.

Antigravity also supports workspace-level skills at `.agents/skills/` inside your project root — the same path Codex uses.

## Installable Skill Keys

The installer links every public `SKILL.md` under `skills/`, `plugins/`, and bundled project skill directories, excluding hidden directories such as plugin-internal `.claude/` templates.

```text
analyze-experiment
beamer-style
cc-navigator
commit-changelog
compile-check
defuddle
digest
figure-qa
flipradio-polish
flipradio-write
hook-recipes
init-project
json-canvas
meta-audit
monitor
new-experiment
no-more-fomo
obsidian-bases
obsidian-cli
obsidian-markdown
paper-review
paper-storyteller
paper-style
paper-writing-qa
pre-submit-challenge
project-skill
read-paper
review-review
section-guard
selfos
selfos-completion
survey-literature
swiss-knife-design
sync-paper
thought
todo
unbox
unbox-graph
unbox-to-wiki
update-docs
update-knowhow
update-project-skill
visualize
web-fetcher
weekly-report
writing-agents
yuanboizer-zh
```

## Plugin Metadata

Claude plugin metadata stays in each plugin's `.claude-plugin/plugin.json`.

Codex and Antigravity plugin metadata lives beside it:

```text
plugins/labmate/.codex-plugin/plugin.json
plugins/meta-audit/.codex-plugin/plugin.json
plugins/paper-review/.codex-plugin/plugin.json
plugins/papermate/.codex-plugin/plugin.json
plugins/unbox-skills/.codex-plugin/plugin.json
```

Antigravity uses the same `plugin.json` format as Codex, so the `.codex-plugin/` manifests are directly compatible with both platforms.

The repo-local marketplace index is:

```text
.agents/plugins/marketplace.json
```

Skill symlinks are still the most portable cross-platform path. The `.codex-plugin` manifests and marketplace file are metadata for builds that support local plugin marketplaces.

## Verification

Check shell syntax:

```bash
bash -n install.sh
```

Check Codex manifest JSON:

```bash
python3 -m json.tool .agents/plugins/marketplace.json >/tmp/yuanbo-marketplace.json
python3 -m json.tool plugins/labmate/.codex-plugin/plugin.json >/tmp/labmate-codex-plugin.json
python3 -m json.tool plugins/meta-audit/.codex-plugin/plugin.json >/tmp/meta-audit-codex-plugin.json
python3 -m json.tool plugins/paper-review/.codex-plugin/plugin.json >/tmp/paper-review-codex-plugin.json
python3 -m json.tool plugins/papermate/.codex-plugin/plugin.json >/tmp/papermate-codex-plugin.json
python3 -m json.tool plugins/unbox-skills/.codex-plugin/plugin.json >/tmp/unbox-codex-plugin.json
```

Check every public skill is visible to Codex:

```bash
for s in analyze-experiment beamer-style cc-navigator commit-changelog compile-check defuddle digest figure-qa flipradio-polish flipradio-write hook-recipes init-project json-canvas meta-audit monitor new-experiment no-more-fomo obsidian-bases obsidian-cli obsidian-markdown paper-review paper-storyteller paper-style paper-writing-qa pre-submit-challenge project-skill read-paper review-review section-guard selfos selfos-completion survey-literature swiss-knife-design sync-paper thought todo unbox unbox-graph unbox-to-wiki update-docs update-knowhow update-project-skill visualize web-fetcher weekly-report writing-agents yuanboizer-zh; do
  test -f "$HOME/.agents/skills/$s/SKILL.md" || echo "MISSING $s"
done
```

No output means all listed skills are installed.

## Maintenance Notes

- When adding a public skill, ensure it has `SKILL.md` and rerun `./install.sh --target all`.
- When adding a plugin, add both `.claude-plugin/plugin.json` and `.codex-plugin/plugin.json` if it should appear in all ecosystems. The `.codex-plugin/` manifest is shared by Codex and Antigravity.
- Do not install hidden template skills globally. The installer intentionally prunes paths matching `*/.*`.
- If an existing target directory is a real directory rather than a symlink, the installer skips it instead of overwriting user-managed content.
- Keep Claude, Codex, and Antigravity install docs in sync when changing install behavior.
