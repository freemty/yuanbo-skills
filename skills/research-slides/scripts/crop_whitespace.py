#!/usr/bin/env python3
"""Crop near-white margins from a raster figure."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageChops


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path, nargs="?")
    parser.add_argument("--in-place", action="store_true")
    parser.add_argument("--threshold", type=int, default=10)
    parser.add_argument("--margin", type=int, default=24)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.in_place:
        out = args.input
    elif args.output:
        out = args.output
    else:
        raise SystemExit("provide output path or --in-place")

    image = Image.open(args.input).convert("RGB")
    bg = Image.new("RGB", image.size, (255, 255, 255))
    diff = ImageChops.difference(image, bg).convert("L")
    mask = diff.point(lambda p: 255 if p > args.threshold else 0)
    bbox = mask.getbbox()
    if bbox is None:
        image.save(out)
        print(f"no crop: {args.input} -> {out}")
        return 0

    left, top, right, bottom = bbox
    margin = max(args.margin, 0)
    left = max(0, left - margin)
    top = max(0, top - margin)
    right = min(image.width, right + margin)
    bottom = min(image.height, bottom + margin)
    cropped = image.crop((left, top, right, bottom))
    cropped.save(out)
    print(f"cropped {image.size} -> {cropped.size}: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
