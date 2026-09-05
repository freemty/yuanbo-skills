#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
python3 scripts/validate_skills.py
python3 scripts/check_release.py
bash tests/test-context-audit.sh
python3 skills/web-fetcher/scripts/test_fetch.py
python3 plugins/unbox-skills/tests/test_graph_sync.py
python3 plugins/papermate/tests/test_compile_feedback.py
python3 plugins/meta-audit/tests/test_collect.py
(cd projects/selfos && python3 -B -m unittest tests.test_selfos_skill_contracts tests.test_validate_wiki_evidence tests.test_note_mode tests.test_wiki_search)
bash plugins/labmate/tests/test-hooks.sh
bash plugins/labmate/tests/test-platform-compat.sh
bash plugins/labmate/tests/test-context-contract.sh
bash plugins/labmate/tests/test-scripts.sh
python3 plugins/labmate/scripts/sync-version.py --check
bash tests/test-install.sh
git diff --check
echo "Offline capability refactor regression passed. Native/model/media checks are separate."
