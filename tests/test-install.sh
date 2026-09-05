#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TEST_ROOT="$(mktemp -d "${TMPDIR:-/tmp}/yuanbo-skills-install.XXXXXX")"

cleanup() {
  case "$TEST_ROOT" in
    "${TMPDIR:-/tmp}"/yuanbo-skills-install.*) rm -rf -- "$TEST_ROOT" ;;
  esac
}
trap cleanup EXIT

TEST_HOME="$TEST_ROOT/home"
CODEX_SKILLS="$TEST_HOME/.agents/skills"
mkdir -p \
  "$CODEX_SKILLS/proactive-agent" \
  "$CODEX_SKILLS/notion-lifeos"

run_installer() {
  HOME="$TEST_HOME" bash "$REPO_ROOT/install.sh" --target codex "$@"
}

fail() {
  echo "FAIL: $*" >&2
  exit 1
}

run_installer

[ -L "$CODEX_SKILLS/web-fetcher" ] ||
  fail "Codex default did not link a standalone skill"
[ ! -e "$CODEX_SKILLS/read-paper" ] ||
  fail "Codex default linked a plugin-owned skill"

run_installer --include-plugin-skills

[ -L "$CODEX_SKILLS/read-paper" ] ||
  fail "legacy mode did not link Labmate's read-paper skill"
case "$(readlink "$CODEX_SKILLS/read-paper")" in
  "$REPO_ROOT/plugins/labmate/skills/read-paper") ;;
  *) fail "read-paper link does not point to the Labmate plugin" ;;
esac

mkdir -p "$CODEX_SKILLS/keep-real"
ln -s "$REPO_ROOT/skills/web-fetcher" "$CODEX_SKILLS/keep-standalone"
ln -s "$REPO_ROOT/plugins/labmate/docs" "$CODEX_SKILLS/keep-plugin-docs"
rm -- "$CODEX_SKILLS/read-paper"
mkdir -p "$CODEX_SKILLS/read-paper"
touch "$CODEX_SKILLS/read-paper/user-owned"

run_installer --prune-plugin-skill-links

[ ! -e "$CODEX_SKILLS/monitor" ] ||
  fail "prune did not remove the managed plugin-skill symlink"
[ -f "$CODEX_SKILLS/read-paper/user-owned" ] ||
  fail "prune removed a real directory at a plugin skill name"
[ -d "$CODEX_SKILLS/keep-real" ] ||
  fail "prune removed a real directory"
[ -L "$CODEX_SKILLS/keep-standalone" ] ||
  fail "prune removed a standalone skill symlink"
[ -L "$CODEX_SKILLS/keep-plugin-docs" ] ||
  fail "prune removed a non-skill plugin path"
[ -L "$CODEX_SKILLS/web-fetcher" ] ||
  fail "prune removed the installed standalone skill"

ALL_HOME="$TEST_ROOT/all-home"
mkdir -p \
  "$ALL_HOME/.claude/skills/proactive-agent" \
  "$ALL_HOME/.claude/skills/notion-lifeos" \
  "$ALL_HOME/.agents/skills/proactive-agent" \
  "$ALL_HOME/.agents/skills/notion-lifeos" \
  "$ALL_HOME/.gemini/antigravity/skills/proactive-agent" \
  "$ALL_HOME/.gemini/antigravity/skills/notion-lifeos"
HOME="$ALL_HOME" bash "$REPO_ROOT/install.sh" --target all >/dev/null

[ -L "$ALL_HOME/.claude/skills/read-paper" ] ||
  fail "--target all changed Claude plugin-skill behavior"
[ -L "$ALL_HOME/.gemini/antigravity/skills/read-paper" ] ||
  fail "--target all changed Antigravity plugin-skill behavior"
[ ! -e "$ALL_HOME/.agents/skills/read-paper" ] ||
  fail "--target all did not apply the Codex plugin-skill exclusion"

echo "installer compatibility tests passed"
