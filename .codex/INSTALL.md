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

   This links every `SKILL.md`/`skill.md` found under `skills/`, `plugins/`, and bundled project skill directories into `~/.agents/skills/`.

3. Restart Codex to discover the skills.

## Installable Skill Keys

The installer links these skills into `~/.agents/skills/`. Public `skills/` and `plugins/` entries take precedence over bundled project skills when names collide.

```text
academic-writing
analyze-experiment
beamer-style
cc-navigator
clone-web
commit-changelog
compile-check
de-ai
digest
figure-qa
flipradio-polish
flipradio-write
hook-recipes
init-project
interview
meta-audit
monitor
new-experiment
no-more-fomo
paper-plot
paper-review
paper-storyteller
paper-style
paper-writing-qa
pre-submit-challenge
read-paper
review-review
section-guard
survey-literature
swiss-knife-design
sync-paper
thought
todo
transcribe
unbox
unbox-graph
unbox-to-wiki
update-docs
update-knowhow
update-project-skill
visualize
web-fetcher
weekly-report
wiki
wiki-help
writing-agents
yuanboizer-zh
```

## Manual Installation

If you do not want to run the installer:

```bash
git clone --recurse-submodules https://github.com/freemty/yuanbo-skills.git ~/.codex/yuanbo-skills
mkdir -p ~/.agents/skills
seen_skill_names=""
{
  find ~/.codex/yuanbo-skills/skills ~/.codex/yuanbo-skills/plugins \
    -path '*/.*' -prune -o \( -name SKILL.md -o -name skill.md \) -print0
  find ~/.codex/yuanbo-skills/projects/selfos/.claude/skills \
    \( -name SKILL.md -o -name skill.md \) -print0
} |
while IFS= read -r -d '' skill_md; do
  skill_dir="$(dirname "$skill_md")"
  skill_name="$(basename "$skill_dir")"
  case " ${seen_skill_names:-} " in *" $skill_name "*) continue ;; esac
  seen_skill_names="${seen_skill_names:-} $skill_name"
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
- `plugins/papermate/.codex-plugin/plugin.json`
- `plugins/unbox-skills/.codex-plugin/plugin.json`

The local marketplace index is `.agents/plugins/marketplace.json`. Skill symlinks are still the most portable Codex install path; plugin manifests provide metadata for Codex builds that support local plugin marketplaces.

## Hooks Compatibility

The labmate and papermate Codex plugin manifests point to standalone `hooks/hooks.json` files. Hook scripts are best-effort: they run when the host supports local plugin hooks and degrade silently when optional shell dependencies such as `jq`, `gh`, or project files are unavailable.

## Third-Party Skills

`install.sh` also attempts to install these optional third-party skills into `~/.agents/skills/`:

- `notion-lifeos`
- `proactive-agent`

If a network clone fails, the installer reports a warning and keeps the local yuanbo skills installed.

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
