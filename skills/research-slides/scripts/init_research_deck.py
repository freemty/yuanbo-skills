#!/usr/bin/env python3
"""Create a self-contained research Beamer deck from the bundled template."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("target", type=Path)
    parser.add_argument("--force", action="store_true")
    return parser.parse_args()


def copy_file(source: Path, target: Path, force: bool) -> None:
    if target.exists() and not force:
        raise SystemExit(f"refusing to overwrite {target}; pass --force")
    shutil.copy2(source, target)


def main() -> int:
    args = parse_args()
    skill_dir = Path(__file__).resolve().parent.parent
    assets = skill_dir / "assets"

    args.target.mkdir(parents=True, exist_ok=True)
    (args.target / "figs").mkdir(exist_ok=True)
    copy_file(assets / "research-main.tex", args.target / "main.tex", args.force)
    copy_file(assets / "layout-research.tex", args.target / "layout-research.tex", args.force)
    copy_file(assets / "source-manifest.tsv", args.target / "source-manifest.tsv", args.force)

    print(args.target / "main.tex")
    print(args.target / "layout-research.tex")
    print(args.target / "source-manifest.tsv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
