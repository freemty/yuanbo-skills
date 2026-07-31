#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"

output=$(python3 "$ROOT/scripts/context_audit.py" --check "$ROOT")
printf '%s\n' "$output"
printf '%s' "$output" | grep -q '^50 skills; 0 flagged$'

echo "context audit checks passed"
