#!/usr/bin/env bash
set -euo pipefail

# ybskills installer
# Creates symlinks for SKILL.md/skill.md directories under skills/, plugins/,
# and bundled project skill directories. Codex skips plugin-owned skills by
# default so an installed plugin is not registered a second time.
# Defaults to Claude Code (~/.claude/skills); pass --target codex for
# OpenAI Codex CLI (~/.agents/skills) or --target antigravity for
# Google Antigravity (~/.gemini/antigravity/skills).

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET="claude"
INCLUDE_PLUGIN_SKILLS=0
PRUNE_PLUGIN_SKILL_LINKS=0

usage() {
  cat <<'EOF'
Usage: ./install.sh [--target claude|codex|antigravity|all] [options]

Targets:
  claude        Link skills into ~/.claude/skills (default)
  codex         Link standalone skills into ~/.agents/skills
  antigravity   Link skills into ~/.gemini/antigravity/skills
  all           Install Claude, Codex, and Antigravity skill links

Codex options:
  --include-plugin-skills       Also link skills owned by Codex plugins.
                                Use only as a legacy fallback without plugins.
  --prune-plugin-skill-links    Remove symlinks into this repository's plugin
                                skills before installing. Real directories and
                                standalone skill links are never removed.
EOF
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --target)
      TARGET="${2:-}"
      shift 2
      ;;
    --target=*)
      TARGET="${1#*=}"
      shift
      ;;
    --include-plugin-skills)
      INCLUDE_PLUGIN_SKILLS=1
      shift
      ;;
    --prune-plugin-skill-links)
      PRUNE_PLUGIN_SKILL_LINKS=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
done

case "$TARGET" in
  claude|codex|antigravity|all) ;;
  *)
    echo "Invalid target: $TARGET" >&2
    usage >&2
    exit 1
    ;;
esac

skill_target_dir() {
  case "$1" in
    claude) printf '%s\n' "$HOME/.claude/skills" ;;
    codex) printf '%s\n' "$HOME/.agents/skills" ;;
    antigravity) printf '%s\n' "$HOME/.gemini/antigravity/skills" ;;
  esac
}

plugin_root_for_skill() {
  local skill_dir="$1"
  local relative plugin_name plugin_root

  case "$skill_dir" in
    "$SCRIPT_DIR"/plugins/*)
      relative="${skill_dir#"$SCRIPT_DIR/plugins/"}"
      plugin_name="${relative%%/*}"
      plugin_root="$SCRIPT_DIR/plugins/$plugin_name"
      if [ -f "$plugin_root/.codex-plugin/plugin.json" ] &&\
         { [ -f "$skill_dir/SKILL.md" ] || [ -f "$skill_dir/skill.md" ]; }; then
        printf '%s\n' "$plugin_root"
        return 0
      fi
      ;;
  esac
  return 1
}

prune_codex_plugin_skill_links() {
  local target_root="$1"
  local link current link_dir resolved_parent plugin_root removed

  removed=0
  for link in "$target_root"/*; do
    [ -L "$link" ] || continue
    current="$(readlink "$link")"
    case "$current" in
      /*) ;;
      *)
        link_dir="$(dirname "$link")"
        resolved_parent="$(
          cd "$link_dir/$(dirname "$current")" 2>/dev/null && pwd -P
        )" || resolved_parent=""
        if [ -n "$resolved_parent" ]; then
          current="$resolved_parent/$(basename "$current")"
        fi
        ;;
    esac
    if plugin_root="$(plugin_root_for_skill "$current")"; then
      rm -- "$link"
      echo "  Pruned plugin skill link: $(basename "$link") (from $plugin_root)"
      removed=$((removed + 1))
    fi
  done
  echo "Plugin skill links: $removed pruned"
  echo ""
}

link_skill_dir() {
  local skill_dir="$1"
  local target_root="$2"
  local skill_name target current

  skill_name="$(basename "$skill_dir")"
  target="$target_root/$skill_name"

  if [ -L "$target" ]; then
    current="$(readlink "$target")"
    if [ "$current" = "$skill_dir" ] || [ "$current" = "${skill_dir%/}" ]; then
      return 1
    fi
    echo "  Updating symlink: $skill_name (was -> $current)"
    rm "$target"
  elif [ -e "$target" ]; then
    echo "  WARNING: $target exists and is not a symlink, skipping"
    return 1
  fi

  ln -s "${skill_dir%/}" "$target"
  echo "  Linked: $skill_name"
  return 0
}

install_target() {
  local target_name="$1"
  local skills_dir installed skipped plugin_skipped skill_md skill_dir skill_name seen_skill_names

  skills_dir="$(skill_target_dir "$target_name")"
  mkdir -p "$skills_dir"

  echo "Installing ybskills for $target_name from $SCRIPT_DIR"
  echo "Target: $skills_dir"
  echo ""

  if [ "$target_name" = "codex" ] && [ "$PRUNE_PLUGIN_SKILL_LINKS" -eq 1 ]; then
    prune_codex_plugin_skill_links "$skills_dir"
  fi

  installed=0
  skipped=0
  plugin_skipped=0
  seen_skill_names=""

  while IFS= read -r -d '' skill_md; do
    skill_dir="$(dirname "$skill_md")"
    skill_name="$(basename "$skill_dir")"

    if [ "$target_name" = "codex" ] &&
       [ "$INCLUDE_PLUGIN_SKILLS" -eq 0 ] &&
       plugin_root_for_skill "$skill_dir" >/dev/null; then
      plugin_skipped=$((plugin_skipped + 1))
      continue
    fi

    case " $seen_skill_names " in
      *" $skill_name "*)
        echo "  WARNING: duplicate skill name '$skill_name' at $skill_dir, skipping"
        skipped=$((skipped + 1))
        continue
        ;;
    esac
    seen_skill_names="$seen_skill_names $skill_name"
    if link_skill_dir "$skill_dir" "$skills_dir"; then
      installed=$((installed + 1))
    else
      skipped=$((skipped + 1))
    fi
  done < <(
    python3 "$SCRIPT_DIR/scripts/skill_inventory.py" "$SCRIPT_DIR" --null
  )

  echo ""
  echo "Skills: $installed linked, $skipped unchanged/skipped"
  if [ "$target_name" = "codex" ]; then
    if [ "$INCLUDE_PLUGIN_SKILLS" -eq 1 ]; then
      echo "Codex plugin skills: included in legacy symlink mode"
    else
      echo "Codex plugin skills: $plugin_skipped skipped (install plugins instead)"
    fi
  fi
  echo ""

  install_third_party "$skills_dir"

  case "$target_name" in
    claude) echo "Done. Run 'claude' to use your skills." ;;
    codex) echo "Done. Restart Codex to discover your skills." ;;
    antigravity) echo "Done. Restart Antigravity or agy CLI to discover your skills." ;;
  esac
  echo ""
}

install_third_party() {
  local skills_dir="$1"
  local tp_installed=0
  local tp_skipped=0

  clone_dep() {
    local name="$1" url="$2"
    local target="$skills_dir/$name"
    if [ -e "$target" ]; then
      tp_skipped=$((tp_skipped + 1))
      return
    fi
    echo "  Cloning: $name"
    if git clone --depth 1 "$url" "$target"; then
      tp_installed=$((tp_installed + 1))
    else
      echo "  WARNING: failed to clone $name from $url; continuing"
      tp_skipped=$((tp_skipped + 1))
    fi
  }

  clone_dep "proactive-agent" "https://github.com/halthelobster/proactive-agent.git"
  clone_dep "notion-lifeos" "https://github.com/jiahao-shao1/openclaw-skill-notion-lifeos.git"

  echo "Third-party skills: $tp_installed cloned, $tp_skipped already present"
  echo ""
}

python3 "$SCRIPT_DIR/scripts/skill_inventory.py" "$SCRIPT_DIR" --null >/dev/null

case "$TARGET" in
  claude|codex|antigravity)
    install_target "$TARGET"
    ;;
  all)
    install_target claude
    install_target codex
    install_target antigravity
    ;;
esac
