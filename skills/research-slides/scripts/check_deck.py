#!/usr/bin/env python3
"""Compile, lint, and render a Beamer deck for visual QA."""

from __future__ import annotations

import argparse
import hashlib
import os
import re
import shutil
import signal
import subprocess
import sys
import tempfile
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
    parser.add_argument("--engine", choices=("auto", "xelatex", "lualatex", "pdflatex"), default="auto")
    parser.add_argument("--builder", choices=("auto", "latexmk", "engine"), default="auto")
    parser.add_argument("--max-passes", type=int, default=5, help="direct-engine convergence bound (minimum 2)")
    parser.add_argument("--timeout", type=float, default=180, help="seconds per build/render command")
    return parser.parse_args()


def require_command(name: str) -> str:
    path = shutil.which(name)
    if not path:
        raise SystemExit(f"missing required command: {name}")
    return path


def run_checked(cmd: list[str], cwd: Path, timeout: float = 180) -> None:
    if timeout <= 0:
        raise SystemExit("command timeout must be positive")
    process = subprocess.Popen(
        cmd,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        start_new_session=True,
    )
    try:
        output, _ = process.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        if os.name == "posix":
            os.killpg(process.pid, signal.SIGTERM)
        else:
            process.terminate()
        try:
            output, _ = process.communicate(timeout=5)
        except subprocess.TimeoutExpired:
            if os.name == "posix":
                os.killpg(process.pid, signal.SIGKILL)
            else:
                process.kill()
            output, _ = process.communicate()
        print("\n".join(output.splitlines()[-20:]), file=sys.stderr)
        raise SystemExit(f"command timed out after {timeout}s: {' '.join(cmd)}; inspect toolchain or raise --timeout")
    if process.returncode:
        tail = "\n".join(output.splitlines()[-40:])
        print(tail, file=sys.stderr)
        raise SystemExit(f"command failed ({process.returncode}): {' '.join(cmd)}")


def compile_deck(tex: Path, engine: str = "auto", builder: str = "auto", max_passes: int = 5, timeout: float = 180) -> None:
    if max_passes < 2:
        raise SystemExit("--max-passes must be at least 2")
    use_latexmk = builder == "latexmk" or (builder == "auto" and shutil.which("latexmk"))
    if engine == "auto":
        magic = re.search(r"^%\s*!TeX\s+program\s*=\s*(xelatex|lualatex|pdflatex)\s*$",
                          tex.read_text(), re.I | re.M)
        project_config = any((tex.parent / name).is_file() for name in ("latexmkrc", ".latexmkrc"))
        if magic:
            engine = magic.group(1).lower()
        elif use_latexmk and project_config:
            engine = "project"
        else:
            engine = next((name for name in ("xelatex", "lualatex", "pdflatex") if shutil.which(name)), "xelatex")
    if use_latexmk:
        flags = {"xelatex": "-xelatex", "lualatex": "-lualatex", "pdflatex": "-pdf"}
        cmd = [require_command("latexmk")]
        if engine != "project":
            require_command(engine)
            cmd.append(flags[engine])
        # Revisit conditional inputs that did not exist in the previous build.
        cmd += ["-g", "-interaction=nonstopmode", "-halt-on-error", "-recorder", tex.name]
        run_checked(cmd, tex.parent, timeout)
        return
    cmd = [require_command(engine), "-interaction=nonstopmode", "-halt-on-error", "-recorder", tex.name]
    previous = None
    for _ in range(max_passes):
        run_checked(cmd, tex.parent, timeout)
        state = tuple((suffix, hashlib.sha256(tex.with_suffix(suffix).read_bytes()).hexdigest())
                      for suffix in (".aux", ".toc", ".nav", ".snm", ".out") if tex.with_suffix(suffix).exists())
        log = tex.with_suffix(".log").read_text(errors="replace")
        rerun = re.search(r"Rerun to get|Label\(s\) may have changed|Please \(re\)run", log, re.I)
        if previous == state and not rerun:
            return
        previous = state
    raise SystemExit(f"references did not converge in {max_passes} passes; inspect the log or use latexmk")


def source_freshness(tex: Path, pdf: Path) -> tuple[list[str], list[str]]:
    inputs = {tex}
    recorder = tex.with_suffix(".fls")
    warnings = []
    if recorder.exists():
        generated = {".aux", ".toc", ".nav", ".snm", ".out", ".log", ".vrb"}
        for line in recorder.read_text(errors="replace").splitlines():
            if line.startswith("INPUT "):
                raw = line[6:]
                # XeTeX records this version probe as an INPUT, not a filename.
                if raw == "extractbb --version" or raw.startswith("|"):
                    warnings.append(f"recorded process input has no file freshness check: {raw}")
                    continue
                path = (tex.parent / raw).resolve()
                if path.suffix not in generated:
                    inputs.add(path)
    else:
        warnings.append("no recorder (.fls): dependency freshness is incomplete; rerun without --no-compile")
    failures = []
    for path in sorted(inputs):
        if not path.exists():
            failures.append(f"recorded input missing: {path}")
        elif path.stat().st_mtime > pdf.stat().st_mtime:
            failures.append(f"PDF is older than input: {path}; rebuild before delivery")
    return failures, warnings


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
        if not re.fullmatch(r"\d+(?:-\d+)?", part):
            raise SystemExit(f"invalid page selection: {part}; use pages or ranges such as 2,7-9")
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
    if not pages:
        raise SystemExit("page selection is empty")
    return sorted(pages)


def render_pages(pdf: Path, pages: list[int], out: Path, dpi: int, timeout: float = 180) -> list[Path]:
    pdftoppm = require_command("pdftoppm")
    out.mkdir(parents=True, exist_ok=True)
    out = Path(tempfile.mkdtemp(prefix="render-", dir=out))
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
            timeout,
        )
        rendered.append(prefix.with_suffix(".png"))
    return rendered


def main() -> int:
    args = parse_args()
    tex = args.tex.resolve()
    if not tex.exists():
        raise SystemExit(f"missing TeX source: {tex}")
    if not args.no_compile:
        compile_deck(tex, args.engine, args.builder, args.max_passes, args.timeout)

    pdf = tex.with_suffix(".pdf")
    log = tex.with_suffix(".log")
    failures, warnings = scan_log(log)
    warnings.extend(source_warnings(tex))
    if args.no_compile:
        warnings.append("no rebuild: recorder checks known inputs only; new conditional inputs and external preprocessing/bibliography dependencies may be unobserved")
    if pdf.exists():
        stale, coverage = source_freshness(tex, pdf)
        failures.extend(stale)
        warnings.extend(coverage)

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
    out = (args.out or Path(tempfile.gettempdir()) / "research-slide-check").resolve()
    rendered = render_pages(pdf, pages, out, args.dpi, args.timeout)

    print(f"BUILD CHECKS PASSED: {pdf} ({total} pages)")
    print(f"static assets: {len(assets)}")
    for path in rendered:
        print(path)
    print("VISUAL REVIEW PENDING: inspect PNGs for overlap, blur, clipping, density, and citation collisions. This is not evidence/story approval.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
