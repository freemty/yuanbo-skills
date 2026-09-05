#!/usr/bin/env python3
"""Validate skill frontmatter and README contracts across installable roots.

Checks per skill directory:
- SKILL.md or skill.md exists with YAML frontmatter
- frontmatter has non-empty `name` and `description`
- `name` matches the containing directory name
- a sibling README.md exists

Exits non-zero if any skill fails. Designed for CI.
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PUBLIC_ROOTS = [REPO_ROOT / "skills", REPO_ROOT / "plugins"]


from skill_inventory import discover, parse_frontmatter


def find_skill_files() -> list[Path]:
    return [item['path'] for item in discover(REPO_ROOT)]


def validate(skill_file: Path) -> list[str]:
    errors: list[str] = []
    skill_dir = skill_file.parent
    text = skill_file.read_text(encoding="utf-8")
    fm = parse_frontmatter(text)
    if fm is None:
        errors.append("missing or malformed YAML frontmatter")
        return errors

    name = fm.get("name", "")
    desc = fm.get("description", "")
    if not name:
        errors.append("frontmatter missing `name`")
    elif name != skill_dir.name:
        errors.append(f"name `{name}` != directory `{skill_dir.name}`")

    if not desc:
        errors.append("frontmatter missing `description`")

    is_top_level = skill_dir.parent in PUBLIC_ROOTS
    if is_top_level and not (skill_dir / "README.md").exists():
        errors.append("missing README.md (required for top-level skills/plugins)")

    return errors


def main() -> int:
    skill_files = find_skill_files()
    if not skill_files:
        print("no SKILL.md/skill.md files found", file=sys.stderr)
        return 1

    failed = 0
    for skill_file in skill_files:
        rel = skill_file.parent.relative_to(REPO_ROOT)
        errs = validate(skill_file)
        if errs:
            failed += 1
            print(f"FAIL {rel}")
            for e in errs:
                print(f"  - {e}")
        else:
            print(f"PASS {rel}")

    print(f"\n{len(skill_files) - failed}/{len(skill_files)} skills passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
