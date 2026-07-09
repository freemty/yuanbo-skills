#!/usr/bin/env bash
set -euo pipefail

# ybskills installer
# Creates symlinks for every SKILL.md/skill.md under skills/, plugins/, and
# bundled project skill directories.
# Defaults to Claude Code (~/.claude/skills); pass --target codex for
# OpenAI Codex CLI (~/.agents/skills) or --target antigravity for
# Google Antigravity (~/.gemini/antigravity/skills).

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET="claude"

usage() {
  cat <<'EOF'
Usage: ./install.sh [--target claude|codex|antigravity|all]

Targets:
  claude        Link skills into ~/.claude/skills (default)
  codex         Link skills into ~/.agents/skills
  antigravity   Link skills into ~/.gemini/antigravity/skills
  all           Install Claude, Codex, and Antigravity skill links
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
  local skills_dir installed skipped skill_md skill_dir skill_name seen_skill_names

  skills_dir="$(skill_target_dir "$target_name")"
  mkdir -p "$skills_dir"

  echo "Installing ybskills for $target_name from $SCRIPT_DIR"
  echo "Target: $skills_dir"
  echo ""

  installed=0
  skipped=0
  seen_skill_names=""

  while IFS= read -r -d '' skill_md; do
    skill_dir="$(dirname "$skill_md")"
    skill_name="$(basename "$skill_dir")"
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
    find "$SCRIPT_DIR/skills" "$SCRIPT_DIR/plugins" \
      -path '*/.*' -prune -o \( -name 'SKILL.md' -o -name 'skill.md' \) -print0 2>/dev/null | sort -z
    find "$SCRIPT_DIR/projects/selfos/.claude/skills" \
      \( -name 'SKILL.md' -o -name 'skill.md' \) -print0 2>/dev/null | sort -z
  )

  echo ""
  echo "Skills: $installed linked, $skipped unchanged/skipped"
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
