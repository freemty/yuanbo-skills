#!/usr/bin/env python3
"""Outer entrypoint for the shared discovery implementation."""
import importlib.util
from pathlib import Path

_path = Path(__file__).resolve().parents[1]/'plugins/meta-audit/scripts/skill_inventory.py'
_spec = importlib.util.spec_from_file_location('_shared_skill_inventory', _path)
_module = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_module)
discover, parse_frontmatter, main = _module.discover, _module.parse_frontmatter, _module.main

if __name__ == '__main__':
    main()
