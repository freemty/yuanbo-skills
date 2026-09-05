#!/usr/bin/env python3
"""Behavioral regression tests; PDF integration is exercised separately."""
import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPTS = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("deck", SCRIPTS / "check_deck.py")
deck = importlib.util.module_from_spec(spec)
spec.loader.exec_module(deck)


class WorkflowTests(unittest.TestCase):
    def test_late_conflict_leaves_target_untouched(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp)
            (target / "source-manifest.tsv").write_text("user evidence")
            result = subprocess.run([sys.executable, str(SCRIPTS / "init_research_deck.py"), temp], capture_output=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(sorted(p.name for p in target.iterdir()), ["source-manifest.tsv"])
            self.assertEqual((target / "source-manifest.tsv").read_text(), "user evidence")

    def test_render_does_not_delete_prior_previews(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp)
            sentinel = target / "page-001.png"
            sentinel.write_bytes(b"user preview")
            deck.render_pages(target / "unused.pdf", [], target, 72)
            self.assertEqual(sentinel.read_bytes(), b"user preview")

    def test_empty_page_selection_is_not_success(self):
        with self.assertRaises(SystemExit):
            deck.parse_pages(" , ", 3)

    def test_non_numeric_page_selection_has_actionable_error(self):
        with self.assertRaises(SystemExit):
            deck.parse_pages("hello", 3)

    def test_existing_valid_page_ranges(self):
        self.assertEqual(deck.parse_pages("3,1-2,2", 4), [1, 2, 3])

    def test_xetex_recorder_probe_is_not_a_missing_file(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            tex = root / "main.tex"
            tex.write_text("source")
            tex.with_suffix(".fls").write_text("INPUT main.tex\nINPUT extractbb --version\n")
            pdf = tex.with_suffix(".pdf")
            pdf.write_bytes(b"freshness fixture, not a real PDF")
            failures, warnings = deck.source_freshness(tex, pdf)
            self.assertEqual(failures, [])
            self.assertTrue(warnings)

    def test_command_timeout_reports_failure(self):
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaisesRegex(SystemExit, "timed out"):
                deck.run_checked([sys.executable, "-c", "import time; time.sleep(2)"], Path(temp), timeout=0.05)


if __name__ == "__main__":
    unittest.main()
