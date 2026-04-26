# Codex Support Guide

This repo supports both Claude Code and OpenAI Codex CLI from the same skill and plugin sources.

## Overview

Claude and Codex use different discovery paths:

| Agent | Skill directory | Install command |
|-------|-----------------|-----------------|
| Claude Code | `~/.claude/skills/` | `./install.sh --target claude` |
| Codex CLI | `~/.agents/skills/` | `./install.sh --target codex` |
| Both | both directories | `./install.sh --target all` |

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

## Installable Skill Keys

The installer links every public `SKILL.md` under `skills/` and `plugins/`, excluding hidden directories such as plugin-internal `.claude/` templates.

```text
analyze-experiment
beamer-style
cc-navigator
commit-changelog
flipradio-polish
flipradio-write
hook-recipes
init-project
meta-audit
monitor
new-experiment
no-more-fomo
paper-review
paper-storyteller
paper-style
read-paper
review-review
survey-literature
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

Codex plugin metadata lives beside it:

```text
plugins/labmate/.codex-plugin/plugin.json
plugins/meta-audit/.codex-plugin/plugin.json
plugins/paper-review/.codex-plugin/plugin.json
plugins/unbox-skills/.codex-plugin/plugin.json
```

The repo-local marketplace index is:

```text
.agents/plugins/marketplace.json
```

Skill symlinks are still the most portable Codex path. The `.codex-plugin` manifests and marketplace file are metadata for Codex builds that support local plugin marketplaces.

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
python3 -m json.tool plugins/unbox-skills/.codex-plugin/plugin.json >/tmp/unbox-codex-plugin.json
```

Check every public skill is visible to Codex:

```bash
for s in analyze-experiment beamer-style cc-navigator commit-changelog flipradio-polish flipradio-write hook-recipes init-project meta-audit monitor new-experiment no-more-fomo paper-review paper-storyteller paper-style read-paper review-review survey-literature todo unbox unbox-graph unbox-to-wiki update-docs update-knowhow update-project-skill visualize web-fetcher weekly-report writing-agents yuanboizer-zh; do
  test -f "$HOME/.agents/skills/$s/SKILL.md" || echo "MISSING $s"
done
```

No output means all listed skills are installed.

## Maintenance Notes

- When adding a public skill, ensure it has `SKILL.md` and rerun `./install.sh --target codex`.
- When adding a plugin, add both `.claude-plugin/plugin.json` and `.codex-plugin/plugin.json` if it should appear in both ecosystems.
- Do not install hidden template skills globally. The installer intentionally prunes paths matching `*/.*`.
- If an existing target in `~/.agents/skills/` is a real directory rather than a symlink, the installer skips it instead of overwriting user-managed content.
