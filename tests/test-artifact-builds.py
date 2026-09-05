#!/usr/bin/env python3
"""Real local TeX/PDF integration, not a mocked engine or venue certification."""
import argparse
import hashlib
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def run(*args, cwd=None, success=True):
    result = subprocess.run([str(a) for a in args], cwd=cwd, text=True, capture_output=True)
    if success and result.returncode:
        raise AssertionError(result.stdout[-4000:] + result.stderr[-4000:])
    return result


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True, help="new evidence directory")
    parser.add_argument("--tex-cache", type=Path, help="optional reusable temporary TeX cache, never the installed profile")
    parser.add_argument("--engines", nargs="+", choices=("xelatex", "lualatex", "pdflatex"), default=["xelatex", "lualatex", "pdflatex"])
    args = parser.parse_args()
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=False)
    cache = (args.tex_cache or out / "tex-cache").resolve()
    cache.mkdir(parents=True, exist_ok=True)
    os.environ["TEXMFVAR"] = str(cache)
    os.environ["TEXMFCACHE"] = str(cache)
    slides = ROOT / "skills/research-slides/scripts"
    paper = ROOT / "skills/paper-style/scripts/init_paper_style.py"
    checks = []

    # Authored stand-in for a venue template: preserves layout, anonymity,
    # existing macros and natbib/hyperref. It is not an official venue class.
    venue = out / "venue"
    venue.mkdir()
    (venue / "venue.cls").write_text(r"""\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{venue}[2026/09/05 Synthetic QA fixture]
\LoadClass[10pt,twocolumn]{article}
\RequirePackage[margin=1in]{geometry}
\RequirePackage{natbib}
\RequirePackage[hidelinks]{hyperref}
\newcommand{\thelogo}{venue-logo}
""")
    (venue / "main.tex").write_text(r"""% !TeX program = pdflatex
\documentclass{venue}
\IfFileExists{colors.tex}{\input{colors}}{}
\title{A Synthetic Venue Compatibility Check}
\author{Anonymous Authors}
\date{}
\begin{document}
\maketitle
\makeatletter
\typeout{QA-LAYOUT: \the\textwidth; \the\textheight; \f@family; \thelogo}
\makeatother
\section{A fixed manuscript}
The midpoint minimizes two equally weighted squared Euclidean distances.
This authored example is a template test, not a research result claim.
The citation remains in the venue's style: \citep{fixture}.
\begin{center}
\begin{tabular}{lr}
Point & Analytic value \\
Midpoint & \ifdefined\fst\fst{2}\else 2\fi \\
Endpoint & 4
\end{tabular}
\end{center}
\begin{thebibliography}{1}
\bibitem[Fixture(2026)]{fixture} QA Fixture. Supplied synthetic calculation. 2026.
\end{thebibliography}
\end{document}
""")
    preserved = {p: digest(p) for p in venue.iterdir() if p.is_file()}
    result = run(sys.executable, slides / "check_deck.py", venue / "main.tex", "--out", out / "previews")
    (out / "venue-baseline-check.txt").write_text(result.stdout)
    layout_before = re.findall(r"QA-LAYOUT:.*", (venue / "main.log").read_text())
    shutil.copy2(venue / "main.pdf", out / "venue-before.pdf")
    run(sys.executable, paper, venue, "--python-dir", out / "python", "--inject", "--theme", "blue")
    assert all(digest(p) == value for p, value in preserved.items()), "venue/source changed"
    result = run(sys.executable, slides / "check_deck.py", venue / "main.tex", "--out", out / "previews")
    (out / "venue-after-check.txt").write_text(result.stdout)
    assert "(./colors.tex" in (venue / "main.log").read_text(), "new palette was not included in the rebuilt PDF"
    assert re.findall(r"QA-LAYOUT:.*", (venue / "main.log").read_text()) == layout_before, "layout/font/logo changed"
    assert not (venue / "mystyle.cls").exists()
    assert not (venue / "preamble.tex").exists()
    checks.append("venue fixture: source/class hashes, geometry, font family, logo, anonymity and resolved citation preserved")

    report = out / "report"
    run(sys.executable, paper, report, "--python-dir", out / "report-python", "--theme", "red")
    (report / "main.tex").write_text(r"""% !TeX program = pdflatex
\documentclass[11pt,letterpaper]{mystyle}
\input{colors}
\input{preamble}
\title{A Personal Technical Report}
\author{Skill QA}
\date{5 September 2026}
\begin{document}
\begin{abstract}A synthetic fixture checks the original personal-report entry and its split components.\end{abstract}
\maketitle
\section{A bounded claim}
For fixed $a,b\in\mathbb{R}^d$, the midpoint minimizes their equally weighted squared Euclidean distances.
\begin{abox}This is a template regression, not an external research citation.\end{abox}
\end{document}
""")
    result = run(sys.executable, slides / "check_deck.py", report / "main.tex", "--out", out / "previews")
    (out / "report-check.txt").write_text(result.stdout)
    checks.append("personal report: original colors + preamble entry builds with mystyle")

    configured = out / "configured"
    configured.mkdir()
    (configured / ".latexmkrc").write_text("$pdf_mode = 1;\n")
    (configured / "main.tex").write_text(r"\documentclass{article}\begin{document}Project-configured build.\end{document}")
    run(sys.executable, slides / "check_deck.py", configured / "main.tex", "--out", out / "previews")
    assert "This is pdfTeX" in (configured / "main.log").read_text(), "project engine ignored"
    checks.append("local latexmk configuration selects pdfTeX instead of the default XeTeX")

    preview_parent = out / "preserved-previews"
    preview_parent.mkdir()
    sentinel = preview_parent / "page-001.png"
    sentinel.write_bytes(b"previous user preview")
    run(sys.executable, slides / "render_check_pages.py", report / "main.pdf", "--first", "1", "--out", preview_parent)
    assert sentinel.read_bytes() == b"previous user preview"
    assert len(list(preview_parent.glob("render-*/*.png"))) == 1
    checks.append("standalone render CLI preserves older previews and writes a unique run folder")

    # Each real engine must resolve references before a build pass is reported.
    for engine in args.engines:
        target = out / engine
        target.mkdir()
        (target / "body.tex").write_text(r"\section{Local evidence}\label{sec:evidence}A source-backed statement.")
        (target / "main.tex").write_text(r"\documentclass{article}\begin{document}See Section~\ref{sec:evidence}.\input{body}\end{document}")
        result = run(sys.executable, slides / "check_deck.py", target / "main.tex", "--builder", "engine", "--engine", engine, "--out", out / "previews")
        assert "VISUAL REVIEW PENDING" in result.stdout
        assert "undefined" not in (target / "main.log").read_text()
        (out / f"{engine}-check.txt").write_text(result.stdout)
        (target / "body.tex").write_text(r"\section{Changed evidence}\label{sec:evidence}Changed after PDF build.")
        stale = run(sys.executable, slides / "check_deck.py", target / "main.tex", "--no-compile", success=False)
        assert stale.returncode != 0 and "older than input" in stale.stderr, stale.stdout + stale.stderr
        # Restore source/PDF synchronization for the retained evidence artifact.
        run(sys.executable, slides / "check_deck.py", target / "main.tex", "--builder", "engine", "--engine", engine, "--out", out / "previews")
        checks.append(f"{engine}: converged real build, visual status separate, included-source staleness rejected")

    fallback = out / "fallback"
    fallback.mkdir()
    (fallback / "main.tex").write_text(r"\documentclass{article}\begin{document}Available engine fallback.\end{document}")
    binaries = out / "fallback-bin"
    binaries.mkdir()
    for command in ("pdflatex", "pdfinfo", "pdftoppm"):
        (binaries / command).symlink_to(shutil.which(command))
    old_path = os.environ["PATH"]
    try:
        os.environ["PATH"] = str(binaries)
        run(sys.executable, slides / "check_deck.py", fallback / "main.tex", "--out", out / "previews")
    finally:
        os.environ["PATH"] = old_path
    assert "This is pdfTeX" in (fallback / "main.log").read_text()
    checks.append("auto falls back to real pdfTeX when XeTeX, LuaTeX and latexmk are absent from PATH")

    (out / "checks.txt").write_text("\n".join(checks) + "\nVisual inspection remains a separate manual record.\n")
    print("\n".join(checks))
    print(out)


if __name__ == "__main__":
    main()
