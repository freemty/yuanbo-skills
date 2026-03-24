#!/usr/bin/env bash
set -euo pipefail

# ybskills installer
# Creates symlinks in ~/.claude/skills/ for all original skills
# and clones third-party skills from their repos

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_DIR="$HOME/.claude/skills"

mkdir -p "$SKILLS_DIR"

echo "Installing ybskills from $SCRIPT_DIR"
echo ""

# --- Original skills: symlink each directory with a SKILL.md ---
installed=0
skipped=0

for skill_dir in "$SCRIPT_DIR"/*/; do
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

echo ""
echo "Original skills: $installed linked, $skipped unchanged"
echo ""

# --- Third-party skills: clone if not present ---
declare -A DEPS=(
  ["proactive-agent"]="https://github.com/halthelobster/proactive-agent.git"
  ["notion-lifeos"]="https://github.com/jiahao-shao1/openclaw-skill-notion-lifeos.git"
)

tp_installed=0
tp_skipped=0

for dep_name in "${!DEPS[@]}"; do
  dep_target="$SKILLS_DIR/$dep_name"
  if [ -e "$dep_target" ]; then
    tp_skipped=$((tp_skipped + 1))
    continue
  fi
  echo "  Cloning: $dep_name"
  git clone --depth 1 "${DEPS[$dep_name]}" "$dep_target" 2>/dev/null
  tp_installed=$((tp_installed + 1))
done

echo ""
echo "Third-party skills: $tp_installed cloned, $tp_skipped already present"
echo ""
echo "Done. Run 'claude' to use your skills."
