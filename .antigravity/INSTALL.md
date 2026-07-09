# Installing yuanbo-skills for Google Antigravity

Enable `yuanbo-skills` in Google Antigravity via native skill discovery.

## Prerequisites

- Git
- Google Antigravity 2.0

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

| Scope | Path |
|-------|------|
| Global | `~/.gemini/antigravity/skills/<skill-name>/` |
| Workspace | `<workspace-root>/.agents/skills/<skill-name>/` |

The installer targets the global path. For workspace-level installation, symlink individual skills into `.agents/skills/` in the workspace root.

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

## Plugin Metadata

Antigravity can use the same local plugin metadata as Codex:

- `plugins/labmate/.codex-plugin/plugin.json`
- `plugins/meta-audit/.codex-plugin/plugin.json`
- `plugins/paper-review/.codex-plugin/plugin.json`
- `plugins/papermate/.codex-plugin/plugin.json`
- `plugins/unbox-skills/.codex-plugin/plugin.json`

The local marketplace index is `.agents/plugins/marketplace.json`.

## Hooks Compatibility

Labmate and papermate ship standalone `hooks/hooks.json` files. Hook scripts are best-effort: they run when the host supports local plugin hooks and degrade silently when optional shell dependencies such as `jq`, `gh`, or project files are unavailable.

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

All skills use the Agent Skills open standard. The same `SKILL.md`/`skill.md` files work across Claude Code, OpenAI Codex, and Google Antigravity without modification.
