# Installing yuanbo-skills for Google Antigravity

Enable `yuanbo-skills` in Google Antigravity 2.0 via native skill discovery.

## Prerequisites

- Git
- Google Antigravity 2.0 (desktop app or `agy` CLI)

## Installation

1. Clone the repository:

   ```bash
   git clone --recurse-submodules https://github.com/freemty/yuanbo-skills.git ~/.antigravity/yuanbo-skills
   ```

2. Create Antigravity skill symlinks:

   ```bash
   cd ~/.antigravity/yuanbo-skills
   ./install.sh --target antigravity
   ```

   This links every `SKILL.md`/`skill.md` found under `skills/`, `plugins/`, and bundled project skill directories into `~/.gemini/antigravity/skills/`.

3. Restart Antigravity or `agy` to discover the skills.

## Skill Discovery Paths

Antigravity discovers skills from two locations:

| Scope | Path |
|-------|------|
| Global (all workspaces) | `~/.gemini/antigravity/skills/<skill-name>/` |
| Workspace (per-project) | `<workspace-root>/.agents/skills/<skill-name>/` |

The installer targets the global path. For per-project installation, symlink individual skills into `.agents/skills/` at your workspace root.

## Installable Skill Keys

The installer links every public `SKILL.md`/`skill.md` under `skills/`, `plugins/`, and bundled project skill directories, excluding hidden directories such as plugin-internal `.claude/` templates. Public `skills/` and `plugins/` entries take precedence over bundled project skills when names collide.

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
git clone --recurse-submodules https://github.com/freemty/yuanbo-skills.git ~/.antigravity/yuanbo-skills
mkdir -p ~/.gemini/antigravity/skills
seen_skill_names=""
{
  find ~/.antigravity/yuanbo-skills/skills ~/.antigravity/yuanbo-skills/plugins \
    -path '*/.*' -prune -o \( -name SKILL.md -o -name skill.md \) -print0
  find ~/.antigravity/yuanbo-skills/projects/selfos/.claude/skills \
    \( -name SKILL.md -o -name skill.md \) -print0
} |
while IFS= read -r -d '' skill_md; do
  skill_dir="$(dirname "$skill_md")"
  skill_name="$(basename "$skill_dir")"
  case " ${seen_skill_names:-} " in *" $skill_name "*) continue ;; esac
  seen_skill_names="${seen_skill_names:-} $skill_name"
  ln -sf "$skill_dir" ~/.gemini/antigravity/skills/"$(basename "$skill_dir")"
done
```

## Install a Single Skill

```bash
git clone --recurse-submodules https://github.com/freemty/yuanbo-skills.git ~/.antigravity/yuanbo-skills
mkdir -p ~/.gemini/antigravity/skills
ln -sf ~/.antigravity/yuanbo-skills/skills/web-fetcher ~/.gemini/antigravity/skills/web-fetcher
ln -sf ~/.antigravity/yuanbo-skills/skills/paper-style ~/.gemini/antigravity/skills/paper-style
```

For nested plugin skills:

```bash
ln -sf ~/.antigravity/yuanbo-skills/plugins/unbox-skills/unbox ~/.gemini/antigravity/skills/unbox
ln -sf ~/.antigravity/yuanbo-skills/plugins/labmate/skills/read-paper ~/.gemini/antigravity/skills/read-paper
```

## Plugin Metadata

Antigravity uses `plugin.json` for plugin manifests (same format as Codex). Existing `.codex-plugin/plugin.json` files are compatible:

- `plugins/labmate/.codex-plugin/plugin.json`
- `plugins/meta-audit/.codex-plugin/plugin.json`
- `plugins/paper-review/.codex-plugin/plugin.json`
- `plugins/papermate/.codex-plugin/plugin.json`
- `plugins/unbox-skills/.codex-plugin/plugin.json`

The local marketplace index is `.agents/plugins/marketplace.json`.

## Hooks Compatibility

Antigravity supports hooks via standalone `hooks.json` files (not `settings.json`). The labmate and papermate plugins ship `hooks.json` files that run when the host supports local plugin hooks and degrade silently when optional shell dependencies such as `jq`, `gh`, or project files are unavailable.

Supported hook events: `PreToolUse`, `PostToolUse`, `PreInvocation`, `PostInvocation`, `Stop`.

## Verify

```bash
ls -la ~/.gemini/antigravity/skills/
```

You should see symlinks pointing to skill directories under `~/.antigravity/yuanbo-skills/`.

## Updating

```bash
cd ~/.antigravity/yuanbo-skills
git pull --recurse-submodules
```

Skills update instantly through the symlinks.

## Uninstalling

Remove symlinks:

```bash
for skill in ~/.gemini/antigravity/skills/*; do
  case "$(readlink "$skill")" in *yuanbo-skills*) rm "$skill" ;; esac
done
```

Optionally delete the clone:

```bash
rm -rf ~/.antigravity/yuanbo-skills
```

## Compatibility Note

All skills use the Agent Skills open standard (agentskills.io). The same `SKILL.md`/`skill.md` files work across Claude Code, OpenAI Codex, and Google Antigravity without modification. The format requires `name` and `description` in YAML frontmatter — both fields are present in every skill in this repo.
