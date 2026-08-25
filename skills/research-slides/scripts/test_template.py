#!/usr/bin/env python3
"""Regression test for the Research Slides profile and generated starter."""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path


def require(text: str, needle: str, source: Path) -> None:
    if needle not in text:
        raise AssertionError(f"{source} is missing {needle!r}")


def main() -> int:
    skill_dir = Path(__file__).resolve().parent.parent
    initializer = skill_dir / "scripts" / "init_research_deck.py"
    skill_md = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    profile_path = skill_dir / "references" / "speculative-decoding-reference-profile.md"
    profile = profile_path.read_text(encoding="utf-8")
    openai_yaml = (skill_dir / "agents" / "openai.yaml").read_text(encoding="utf-8")

    require(skill_md, "references/speculative-decoding-reference-profile.md", skill_dir / "SKILL.md")
    require(skill_md, "For every new deck", skill_dir / "SKILL.md")
    require(openai_yaml, "Speculative Decoding reference profile", skill_dir / "agents" / "openai.yaml")

    for invariant in (
        "Memory bandwidth versus idle compute",
        "Draft quality versus draft cost",
        "Causality versus parallelism",
        "Per-request speed versus system throughput",
        "Cross-topic slot mapping",
        "Never fabricate a symmetry",
        "SD-specific facts, labels, formulas, or paper names",
        "idea + survey",
        "4–6 to methods/evidence",
    ):
        require(profile, invariant, profile_path)

    with tempfile.TemporaryDirectory(prefix="research-slides-template-") as temp_dir:
        deck_dir = Path(temp_dir)
        subprocess.run(
            [sys.executable, str(initializer), str(deck_dir)],
            check=True,
            capture_output=True,
            text=True,
        )

        expected = {
            "main.tex",
            "beamer-colors.tex",
            "layout-metropolis.tex",
            "layout-research.tex",
            "source-manifest.tsv",
        }
        missing = sorted(name for name in expected if not (deck_dir / name).is_file())
        if missing:
            raise AssertionError(f"initializer omitted: {', '.join(missing)}")
        if not (deck_dir / "figs").is_dir():
            raise AssertionError("initializer omitted figs/")

        main_tex = (deck_dir / "main.tex").read_text(encoding="utf-8")
        require(main_tex, r"\input{beamer-colors}", deck_dir / "main.tex")
        require(main_tex, r"\input{layout-metropolis}", deck_dir / "main.tex")
        require(main_tex, r"\newcommand{\slidecite}", deck_dir / "main.tex")
        if r"\input{layout-research}" in main_tex:
            raise AssertionError("main.tex still selects the legacy layout")
        if r"\sectiondivider" in main_tex:
            raise AssertionError("main.tex duplicates automatic Metropolis section pages")

        colors_tex = (deck_dir / "beamer-colors.tex").read_text(encoding="utf-8")
        require(colors_tex, r"\providecommand{\beamerthemename}{black}", deck_dir / "beamer-colors.tex")
        for value in ("111111", "444444", "FAFAFA", "D7D7D7"):
            require(colors_tex, value, deck_dir / "beamer-colors.tex")

        layout_tex = (deck_dir / "layout-metropolis.tex").read_text(encoding="utf-8")
        require(layout_tex, r"\AtBeginSection", deck_dir / "layout-metropolis.tex")
        require(layout_tex, r"\setbeamertemplate{footline}", deck_dir / "layout-metropolis.tex")
        require(layout_tex, r"\setbeamertemplate{frametitle}", deck_dir / "layout-metropolis.tex")

    print("research-slides profile and template contract: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
