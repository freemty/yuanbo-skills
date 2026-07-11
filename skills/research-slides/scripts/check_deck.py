#!/usr/bin/env python3
"""Compile, lint, and render a Beamer deck for visual QA."""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path


FATAL_PATTERNS = (
    re.compile(r"^!"),
    re.compile(r"LaTeX Error"),
    re.compile(r"Package .* Error"),
    re.compile(r"Undefined control sequence"),
    re.compile(r"Emergency stop"),
    re.compile(r"Fatal error", re.IGNORECASE),
)
UNDEFINED_PATTERNS = (
    re.compile(r"There were undefined references"),
    re.compile(r"Citation .* undefined"),
    re.compile(r"Reference .* undefined"),
)
OVERFULL_PATTERN = re.compile(r"Overfull \\[hv]box")
HYPERLINK_PATTERN = re.compile(r"(?:hyperref|pdfTeX).*Warning", re.IGNORECASE)
INCLUDEGRAPHICS_PATTERN = re.compile(
    r"\\includegraphics(?:\s*\[[^\]]*\])?\s*\{([^}]+)\}"
)
GRAPHIC_EXTENSIONS = (".pdf", ".png", ".jpg", ".jpeg", ".eps")
PLACEHOLDER_STRINGS = (
    "Talk Title",
    "Your Name",
    "Place the paper's source-native method figure here.",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("tex", type=Path)
    parser.add_argument(
        "--pages",
        help="comma-separated pages and ranges, for example 2,7-9; defaults to all",
    )
    parser.add_argument("--out", type=Path)
    parser.add_argument("--dpi", type=int, default=180)
    parser.add_argument("--no-compile", action="store_true")
    return parser.parse_args()


def require_command(name: str) -> str:
    path = shutil.which(name)
    if not path:
        raise SystemExit(f"missing required command: {name}")
    return path


def run_checked(cmd: list[str], cwd: Path) -> None:
    result = subprocess.run(
        cmd,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if result.returncode:
        tail = "\n".join(result.stdout.splitlines()[-40:])
        print(tail, file=sys.stderr)
        raise SystemExit(f"command failed ({result.returncode}): {' '.join(cmd)}")


def compile_twice(tex: Path) -> None:
    xelatex = require_command("xelatex")
    cmd = [
        xelatex,
        "-interaction=nonstopmode",
        "-halt-on-error",
        tex.name,
    ]
    run_checked(cmd, tex.parent)
    run_checked(cmd, tex.parent)


def static_assets(tex: Path) -> tuple[list[Path], list[str]]:
    text = tex.read_text(encoding="utf-8")
    optional_assets = set(re.findall(r"\\IfFileExists\{([^}]+)\}", text))
    assets: list[Path] = []
    skipped: list[str] = []
    for raw in INCLUDEGRAPHICS_PATTERN.findall(text):
        if raw in optional_assets:
            skipped.append(f"optional: {raw}")
            continue
        if "\\" in raw or "#" in raw:
            skipped.append(raw)
            continue
        candidate = tex.parent / raw
        if candidate.suffix:
            assets.append(candidate)
            continue
        existing = next(
            (candidate.with_suffix(ext) for ext in GRAPHIC_EXTENSIONS if candidate.with_suffix(ext).exists()),
            candidate,
        )
        assets.append(existing)
    return assets, skipped


def source_warnings(tex: Path) -> list[str]:
    text = tex.read_text(encoding="utf-8")
    return [f"starter placeholder remains: {item}" for item in PLACEHOLDER_STRINGS if item in text]


def scan_log(log: Path) -> tuple[list[str], list[str]]:
    if not log.exists():
        return [f"missing log: {log}"], []
    lines = log.read_text(encoding="utf-8", errors="replace").splitlines()
    failures: list[str] = []
    warnings: list[str] = []
    for line in lines:
        if any(pattern.search(line) for pattern in FATAL_PATTERNS):
            failures.append(line.strip())
        elif any(pattern.search(line) for pattern in UNDEFINED_PATTERNS):
            failures.append(line.strip())
        elif OVERFULL_PATTERN.search(line):
            failures.append(line.strip())
        elif HYPERLINK_PATTERN.search(line):
            warnings.append(line.strip())
    return sorted(set(failures)), sorted(set(warnings))


def pdf_page_count(pdf: Path) -> int:
    pdfinfo = require_command("pdfinfo")
    result = subprocess.run(
        [pdfinfo, str(pdf)],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
    )
    match = re.search(r"^Pages:\s+(\d+)$", result.stdout, re.MULTILINE)
    if not match:
        raise SystemExit(f"could not determine page count for {pdf}")
    return int(match.group(1))


def parse_pages(spec: str | None, total: int) -> list[int]:
    if not spec:
        return list(range(1, total + 1))
    pages: set[int] = set()
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            start_text, end_text = part.split("-", 1)
            start, end = int(start_text), int(end_text)
            if start > end:
                raise SystemExit(f"invalid page range: {part}")
            pages.update(range(start, end + 1))
        else:
            pages.add(int(part))
    invalid = sorted(page for page in pages if page < 1 or page > total)
    if invalid:
        raise SystemExit(f"pages outside 1-{total}: {invalid}")
    return sorted(pages)


def render_pages(pdf: Path, pages: list[int], out: Path, dpi: int) -> list[Path]:
    pdftoppm = require_command("pdftoppm")
    out.mkdir(parents=True, exist_ok=True)
    for stale in out.glob("page-*.png"):
        stale.unlink()
    rendered: list[Path] = []
    for page in pages:
        prefix = out / f"page-{page:03d}"
        run_checked(
            [
                pdftoppm,
                "-png",
                "-singlefile",
                "-r",
                str(dpi),
                "-f",
                str(page),
                "-l",
                str(page),
                str(pdf),
                str(prefix),
            ],
            pdf.parent,
        )
        rendered.append(prefix.with_suffix(".png"))
    return rendered


def main() -> int:
    args = parse_args()
    tex = args.tex.resolve()
    if not tex.exists():
        raise SystemExit(f"missing TeX source: {tex}")
    if not args.no_compile:
        compile_twice(tex)

    pdf = tex.with_suffix(".pdf")
    log = tex.with_suffix(".log")
    failures, warnings = scan_log(log)
    warnings.extend(source_warnings(tex))
    if args.no_compile and pdf.exists() and pdf.stat().st_mtime < tex.stat().st_mtime:
        warnings.append("PDF is older than the TeX source; compile before delivery")

    assets, skipped = static_assets(tex)
    missing_assets = sorted(path for path in assets if not path.exists())
    failures.extend(f"missing asset: {path}" for path in missing_assets)

    if warnings:
        print("WARNINGS")
        for warning in warnings:
            print(f"  {warning}")
    if skipped:
        print("DYNAMIC ASSETS (verify manually)")
        for item in skipped:
            print(f"  {item}")
    if failures:
        print("FAILURES", file=sys.stderr)
        for failure in failures:
            print(f"  {failure}", file=sys.stderr)
        return 1
    if not pdf.exists():
        print(f"missing PDF: {pdf}", file=sys.stderr)
        return 1

    total = pdf_page_count(pdf)
    pages = parse_pages(args.pages, total)
    out = (args.out or Path(f"/tmp/research-slide-check-{tex.stem}")).resolve()
    rendered = render_pages(pdf, pages, out, args.dpi)

    print(f"PASS: {pdf} ({total} pages)")
    print(f"static assets: {len(assets)}")
    for path in rendered:
        print(path)
    print("Inspect the rendered PNGs for overlap, blur, clipping, density, and citation collisions.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
