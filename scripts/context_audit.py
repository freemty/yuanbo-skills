#!/usr/bin/env python3
"""Stable outer-repository entrypoint for meta-audit's context checker."""

from __future__ import annotations

import runpy
from pathlib import Path


SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "plugins"
    / "meta-audit"
    / "scripts"
    / "context_audit.py"
)

if not SCRIPT.is_file():
    raise SystemExit(
        "meta-audit context checker is unavailable; initialize the meta-audit submodule"
    )

runpy.run_path(str(SCRIPT), run_name="__main__")
