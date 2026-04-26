# Installing yuanbo-skills for Codex

Enable `yuanbo-skills` in Codex via native skill discovery.

## Prerequisites

- Git
- OpenAI Codex CLI

## Installation

1. Clone the repository:

   ```bash
   git clone --recurse-submodules https://github.com/freemty/yuanbo-skills.git ~/.codex/yuanbo-skills
   ```

2. Create Codex skill symlinks:

   ```bash
   cd ~/.codex/yuanbo-skills
   ./install.sh --target codex
   ```

   This links every `SKILL.md` found under `skills/` and `plugins/` into `~/.agents/skills/`.

3. Restart Codex to discover the skills.

## Installable Skill Keys

The installer links these public skills into `~/.agents/skills/`:

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

## Manual Installation

If you do not want to run the installer:

```bash
git clone --recurse-submodules https://github.com/freemty/yuanbo-skills.git ~/.codex/yuanbo-skills
mkdir -p ~/.agents/skills
find ~/.codex/yuanbo-skills/skills ~/.codex/yuanbo-skills/plugins -path '*/.*' -prune -o -name SKILL.md -print0 |
  while IFS= read -r -d '' skill_md; do
    skill_dir="$(dirname "$skill_md")"
    ln -sf "$skill_dir" ~/.agents/skills/"$(basename "$skill_dir")"
  done
```

## Install a Single Skill

```bash
git clone --recurse-submodules https://github.com/freemty/yuanbo-skills.git ~/.codex/yuanbo-skills
mkdir -p ~/.agents/skills
ln -sf ~/.codex/yuanbo-skills/skills/web-fetcher ~/.agents/skills/web-fetcher
ln -sf ~/.codex/yuanbo-skills/skills/paper-style ~/.agents/skills/paper-style
```

For nested plugin skills:

```bash
ln -sf ~/.codex/yuanbo-skills/plugins/unbox-skills/unbox ~/.agents/skills/unbox
ln -sf ~/.codex/yuanbo-skills/plugins/labmate/skills/read-paper ~/.agents/skills/read-paper
```

## Local Plugin Metadata

This repo also includes Codex plugin manifests:

- `plugins/labmate/.codex-plugin/plugin.json`
- `plugins/meta-audit/.codex-plugin/plugin.json`
- `plugins/paper-review/.codex-plugin/plugin.json`
- `plugins/unbox-skills/.codex-plugin/plugin.json`

The local marketplace index is `.agents/plugins/marketplace.json`. Skill symlinks are still the most portable Codex install path; plugin manifests provide metadata for Codex builds that support local plugin marketplaces.

## Verify

```bash
ls -la ~/.agents/skills/
```

You should see symlinks pointing to skill directories under `~/.codex/yuanbo-skills/`.

## Updating

```bash
cd ~/.codex/yuanbo-skills
git pull --recurse-submodules
```

Skills update instantly through the symlinks.

## Uninstalling

Remove symlinks:

```bash
for skill in ~/.agents/skills/*; do
  case "$(readlink "$skill")" in *yuanbo-skills*) rm "$skill" ;; esac
done
```

Optionally delete the clone:

```bash
rm -rf ~/.codex/yuanbo-skills
```
