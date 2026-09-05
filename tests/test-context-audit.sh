#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"

python3 "$ROOT/scripts/context_audit.py" --check "$ROOT"
python3 "$ROOT/tests/test_context_audit.py"

echo "context audit checks passed"
