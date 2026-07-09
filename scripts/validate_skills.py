#!/usr/bin/env python3
"""Validate skill frontmatter and README contracts across installable roots.

Checks per skill directory:
- SKILL.md or skill.md exists with YAML frontmatter
- frontmatter has non-empty `name` and `description`
- `name` matches the containing directory name
- `description` is at least MIN_DESCRIPTION_LEN characters
- a sibling README.md exists

Exits non-zero if any skill fails. Designed for CI.
"""
from __future__ import annotations

import sys
import os
from pathlib import Path

MIN_DESCRIPTION_LEN = 20
REPO_ROOT = Path(__file__).resolve().parent.parent
PUBLIC_ROOTS = [REPO_ROOT / "skills", REPO_ROOT / "plugins"]
BUNDLED_ROOTS = [REPO_ROOT / "projects" / "selfos" / ".claude" / "skills"]
ROOTS = PUBLIC_ROOTS + BUNDLED_ROOTS


def parse_frontmatter(text: str) -> dict[str, str] | None:
    """Minimal YAML frontmatter parser.

    Supports scalar `key: value` and folded/literal block scalars
    (`key: >`, `key: |`, plus `-`/`+` chomping indicators) where the
    continuation lines are indented more than the key.
    """
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    out: dict[str, str] = {}
    i = 1
    while i < len(lines):
        line = lines[i]
        if line.strip() == "---":
            return out
        stripped = line.lstrip()
        indent = len(line) - len(stripped)
        if ":" in stripped and indent == 0:
            key, _, value = stripped.partition(":")
            key = key.strip()
            value = value.strip()
            if value in (">", "|", ">-", "|-", ">+", "|+"):
                parts: list[str] = []
                j = i + 1
                while j < len(lines):
                    nxt = lines[j]
                    if nxt.strip() == "---":
                        break
                    nxt_indent = len(nxt) - len(nxt.lstrip())
                    if nxt.strip() and nxt_indent <= indent:
                        break
                    parts.append(nxt.strip())
                    j += 1
                out[key] = " ".join(p for p in parts if p)
                i = j
                continue
            out[key] = value.strip('"').strip("'")
        i += 1
    return None


def find_skill_files() -> list[Path]:
    skill_files: list[Path] = []
    for root in ROOTS:
        if not root.exists():
            continue
        for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
            dirnames[:] = [
                d for d in dirnames
                if not d.startswith(".") and not (Path(dirpath) / d).is_symlink()
            ]
            current = Path(dirpath)
            if any(part.startswith(".") for part in current.relative_to(root).parts):
                continue
            for name in ("SKILL.md", "skill.md"):
                if name in filenames:
                    skill_files.append(current / name)
                    break
    return sorted(skill_files)


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
    elif len(desc) < MIN_DESCRIPTION_LEN:
        errors.append(
            f"description too short ({len(desc)} < {MIN_DESCRIPTION_LEN} chars)"
        )

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
