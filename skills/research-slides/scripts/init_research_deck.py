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

    files = {"research-main.tex": "main.tex", **{
        name: name for name in ("beamer-colors.tex", "layout-metropolis.tex",
                               "layout-research.tex", "source-manifest.tsv")}}
    # Check every destination before creating even the figures directory.
    for source, name in files.items():
        target = args.target / name
        if not (assets / source).is_file():
            raise SystemExit(f"missing bundled asset: {source}")
        if target.is_symlink() or (target.exists() and not target.is_file()):
            raise SystemExit(f"refusing non-regular destination: {target}")
        if target.exists() and not args.force:
            raise SystemExit(f"refusing to overwrite {target}; pass --force")
    if args.target.is_symlink() or (args.target.exists() and not args.target.is_dir()):
        raise SystemExit(f"invalid target directory: {args.target}")
    figures = args.target / "figs"
    if figures.is_symlink() or (figures.exists() and not figures.is_dir()):
        raise SystemExit(f"invalid figures directory: {figures}")
    args.target.mkdir(parents=True, exist_ok=True)
    figures.mkdir(exist_ok=True)
    for source, name in files.items():
        copy_file(assets / source, args.target / name, args.force)

    print(args.target / "main.tex")
    print(args.target / "beamer-colors.tex")
    print(args.target / "layout-metropolis.tex")
    print(args.target / "layout-research.tex")
    print(args.target / "source-manifest.tsv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
