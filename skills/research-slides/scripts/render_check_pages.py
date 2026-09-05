#!/usr/bin/env python3
"""Render selected PDF pages to PNG for visual slide QA."""

from __future__ import annotations

import argparse
import subprocess
import tempfile
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--first", "-f", type=int, required=True)
    parser.add_argument("--last", "-l", type=int)
    parser.add_argument("--dpi", "-r", type=int, default=180)
    parser.add_argument("--out", "-o", type=Path, default=Path("/tmp/research-slide-check"))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    last = args.last or args.first
    if args.first < 1 or last < args.first or args.dpi < 1:
        raise SystemExit("invalid page range or DPI")
    args.out.mkdir(parents=True, exist_ok=True)
    run_dir = Path(tempfile.mkdtemp(prefix="render-", dir=args.out))
    prefix = run_dir / "page"
    cmd = [
        "pdftoppm",
        "-png",
        "-r",
        str(args.dpi),
        "-f",
        str(args.first),
        "-l",
        str(last),
        str(args.pdf),
        str(prefix),
    ]
    subprocess.run(cmd, check=True)
    for path in sorted(run_dir.glob("page-*.png")):
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
