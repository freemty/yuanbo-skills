#!/usr/bin/env python3
"""Validate SKILL.md and README.md contracts across skills/ and plugins/.

Checks per skill directory:
- SKILL.md exists with YAML frontmatter
- frontmatter has non-empty `name` and `description`
- `name` matches the containing directory name
- `description` is at least MIN_DESCRIPTION_LEN characters
- a sibling README.md exists

Exits non-zero if any skill fails. Designed for CI.
"""
from __future__ import annotations

import sys
from pathlib import Path

MIN_DESCRIPTION_LEN = 20
REPO_ROOT = Path(__file__).resolve().parent.parent
ROOTS = [REPO_ROOT / "skills", REPO_ROOT / "plugins"]


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


def find_skill_dirs() -> list[Path]:
    skill_dirs: list[Path] = []
    for root in ROOTS:
        if not root.exists():
            continue
        for skill_md in root.rglob("SKILL.md"):
            if any(part.startswith(".") for part in skill_md.parts):
                continue
            skill_dirs.append(skill_md.parent)
    return sorted(set(skill_dirs))


def validate(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    skill_md = skill_dir / "SKILL.md"
    text = skill_md.read_text(encoding="utf-8")
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

    is_top_level = skill_dir.parent in ROOTS
    if is_top_level and not (skill_dir / "README.md").exists():
        errors.append("missing README.md (required for top-level skills/plugins)")

    return errors


def main() -> int:
    skill_dirs = find_skill_dirs()
    if not skill_dirs:
        print("no SKILL.md files found", file=sys.stderr)
        return 1

    failed = 0
    for d in skill_dirs:
        rel = d.relative_to(REPO_ROOT)
        errs = validate(d)
        if errs:
            failed += 1
            print(f"FAIL {rel}")
            for e in errs:
                print(f"  - {e}")
        else:
            print(f"PASS {rel}")

    print(f"\n{len(skill_dirs) - failed}/{len(skill_dirs)} skills passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
