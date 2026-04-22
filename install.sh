#!/usr/bin/env bash
set -euo pipefail

# ybskills installer
# Creates symlinks in ~/.claude/skills/ for all skills and plugins
# and clones third-party skills from their repos

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_DIR="$HOME/.claude/skills"

mkdir -p "$SKILLS_DIR"

echo "Installing ybskills from $SCRIPT_DIR"
echo ""

# --- Skills and plugins: symlink each directory with a SKILL.md ---
installed=0
skipped=0

for search_dir in "$SCRIPT_DIR/skills" "$SCRIPT_DIR/plugins"; do
  [ ! -d "$search_dir" ] && continue
  for skill_dir in "$search_dir"/*/; do
    skill_name="$(basename "$skill_dir")"

    # Skip non-skill directories
    [ ! -f "$skill_dir/SKILL.md" ] && continue

    target="$SKILLS_DIR/$skill_name"

    if [ -L "$target" ]; then
      current=$(readlink "$target")
      if [ "$current" = "$skill_dir" ] || [ "$current" = "${skill_dir%/}" ]; then
        skipped=$((skipped + 1))
        continue
      fi
      echo "  Updating symlink: $skill_name (was -> $current)"
      rm "$target"
    elif [ -e "$target" ]; then
      echo "  WARNING: $target exists and is not a symlink, skipping"
      skipped=$((skipped + 1))
      continue
    fi

    ln -s "${skill_dir%/}" "$target"
    echo "  Linked: $skill_name"
    installed=$((installed + 1))
  done
done

# Also check for nested skills inside plugins (e.g. plugins/unbox-skills/unbox/)
for plugin_dir in "$SCRIPT_DIR/plugins"/*/; do
  [ ! -d "$plugin_dir" ] && continue
  for nested_skill in "$plugin_dir"/*/; do
    [ ! -f "$nested_skill/SKILL.md" ] && continue
    skill_name="$(basename "$nested_skill")"
    target="$SKILLS_DIR/$skill_name"

    if [ -L "$target" ]; then
      current=$(readlink "$target")
      if [ "$current" = "$nested_skill" ] || [ "$current" = "${nested_skill%/}" ]; then
        skipped=$((skipped + 1))
        continue
      fi
      echo "  Updating symlink: $skill_name (was -> $current)"
      rm "$target"
    elif [ -e "$target" ]; then
      skipped=$((skipped + 1))
      continue
    fi

    ln -s "${nested_skill%/}" "$target"
    echo "  Linked: $skill_name (nested)"
    installed=$((installed + 1))
  done
done

echo ""
echo "Skills: $installed linked, $skipped unchanged"
echo ""

# --- Third-party skills: clone if not present ---
tp_installed=0
tp_skipped=0

clone_dep() {
  local name="$1" url="$2"
  local target="$SKILLS_DIR/$name"
  if [ -e "$target" ]; then
    tp_skipped=$((tp_skipped + 1))
    return
  fi
  echo "  Cloning: $name"
  git clone --depth 1 "$url" "$target" 2>/dev/null
  tp_installed=$((tp_installed + 1))
}

clone_dep "proactive-agent" "https://github.com/halthelobster/proactive-agent.git"
clone_dep "notion-lifeos" "https://github.com/jiahao-shao1/openclaw-skill-notion-lifeos.git"

echo ""
echo "Third-party skills: $tp_installed cloned, $tp_skipped already present"
echo ""
echo "Done. Run 'claude' to use your skills."
