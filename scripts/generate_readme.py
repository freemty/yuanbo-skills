#!/usr/bin/env python3
"""Generate README.md skill tables from skill directories.

Scans skills/, plugins/, projects/ for SKILL.md files, groups by category,
and replaces content between <!-- BEGIN SKILLS --> and <!-- END SKILLS -->
markers in README.md.

Usage:
    python3 scripts/generate_readme.py          # preview to stdout
    python3 scripts/generate_readme.py --write   # update README.md in place
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"

CATEGORIES = [
    "Writing & Style",
    "Research & Knowledge",
    "Academic Visual Identity",
    "Productivity",
]

SKILLS = {
    "yuanboizer-zh": {
        "category": "Writing & Style",
        "description": "Personal style polisher — rewrites compressed drafts to sound like Yuanbo",
    },
    "flipradio-write-skill": {
        "category": "Writing & Style",
        "description": "FlipRadio critical style: guided writing + polish (two skills in one)",
    },
    "paper-storyteller": {
        "category": "Writing & Style",
        "description": "Narrative-driven academic paper writing (Wu/Efros/Liu/Freeman/Isola style)",
    },
    "writing-agents": {
        "category": "Writing & Style",
        "description": "Guide for authoring custom coding-agent subagent markdown files",
    },
    "unbox-skills": {
        "category": "Research & Knowledge",
        "description": "Researcher deep profiling — personality, early career, mentorship lineage, direction evolution. Includes unbox, unbox-graph, unbox-to-wiki",
        "type": "plugin",
    },
    "selfos": {
        "category": "Research & Knowledge",
        "description": "Personal knowledge base — ingest, compile, query wiki, context recovery *(private)*",
        "type": "project",
    },
    "no-more-fomo": {
        "category": "Research & Knowledge",
        "description": "AI daily digest from Twitter KOLs, lab blogs, podcasts, arxiv, HackerNews",
    },
    "paper-review": {
        "category": "Research & Knowledge",
        "description": "Multi-role academic peer review — 4 expert agents cross-review, outputs venue-ready form fields. Includes review-review audit",
        "type": "plugin",
    },
    "paper-style": {
        "category": "Academic Visual Identity",
        "description": "Paper color theme system — 5 themes for figures, tables, diagrams",
    },
    "beamer-style": {
        "category": "Academic Visual Identity",
        "description": "Beamer slide theme system — shares the same 5-theme color system",
    },
    "research-slides": {
        "category": "Academic Visual Identity",
        "description": "Multi-mode research Beamer workflow — audience-first story, source-native evidence, and rendered QA",
    },
    "weekly-report": {
        "category": "Productivity",
        "description": "Weekly progress report for managers",
    },
    "web-fetcher": {
        "category": "Productivity",
        "description": "Unified URL fetcher — auto-routes Twitter/YouTube/Bilibili/小红书/GitHub etc.",
    },
    "cc-navigator": {
        "category": "Productivity",
        "description": "Agent workflow navigator — recommends the right skill, agent, tool, or workflow",
    },
    "meta-audit": {
        "category": "Productivity",
        "description": "AI automation maturity audit — L0-L5 scoring, ecosystem benchmarks, Top-3 actions",
        "type": "plugin",
    },
    "labmate": {
        "category": "Productivity",
        "description": "Research harness for AI coding agents — experiments, papers, knowhow, and project memory",
        "type": "plugin",
    },
    "papermate": {
        "category": "Research & Knowledge",
        "description": "Paper writing QA pipeline — section guard, figure QA, compile check, pre-submit challenge",
        "type": "plugin",
    },
    "swiss-knife-design": {
        "category": "Productivity",
        "description": "Personal web design system — project pages, dashboards, leaderboards, slides with consistent visual identity",
    },
    "transcribe": {
        "category": "Productivity",
        "description": "Audio transcription — speech-to-text via Whisper for meetings, voice memos, recordings",
    },
    "clone-web": {
        "category": "Productivity",
        "description": "Local webpage cloning and visual archive workflow",
    },
}

TYPE_TO_DIR = {
    "skill": "skills",
    "plugin": "plugins",
    "project": "projects",
}


def resolve_path(name: str, meta: dict) -> str:
    skill_type = meta.get("type", "skill")
    parent = TYPE_TO_DIR[skill_type]
    return f"{parent}/{name}"


def find_skill_md(name: str, meta: dict) -> Path | None:
    rel = resolve_path(name, meta)
    candidates = [
        ROOT / rel / "SKILL.md",
        ROOT / rel / "skill.md",
        *(ROOT / rel).glob("*/SKILL.md"),
        *(ROOT / rel).glob("*/skill.md"),
        *(ROOT / rel).glob("**/SKILL.md"),
        *(ROOT / rel).glob("**/skill.md"),
    ]
    return next((c for c in candidates if c.exists()), None)


def validate() -> list[str]:
    warnings = []

    for name, meta in SKILLS.items():
        skill_md = find_skill_md(name, meta)
        if skill_md is None:
            warnings.append(f"MISSING: {name} — no SKILL.md found at {resolve_path(name, meta)}/")

    for search_dir in ["skills", "plugins"]:
        base = ROOT / search_dir
        if not base.is_dir():
            continue
        for d in sorted(base.iterdir()):
            if not d.is_dir() or d.is_symlink():
                continue
            has_skill = (
                (d / "SKILL.md").exists()
                or (d / "skill.md").exists()
                or any(d.glob("*/SKILL.md"))
                or any(d.glob("*/skill.md"))
            )
            if has_skill and d.name not in SKILLS:
                warnings.append(f"UNLISTED: {d.name} has a skill file but is not in SKILLS dict")

    for cat in {m["category"] for m in SKILLS.values()}:
        if cat not in CATEGORIES:
            warnings.append(f"UNKNOWN CATEGORY: '{cat}' not in CATEGORIES list")

    return warnings


def generate_tables() -> str:
    lines: list[str] = []

    for cat in CATEGORIES:
        entries = [
            (name, meta)
            for name, meta in SKILLS.items()
            if meta["category"] == cat
        ]
        if not entries:
            continue

        lines.append(f"### {cat}")
        lines.append("")
        lines.append("| Skill | Description |")
        lines.append("|-------|-------------|")

        for name, meta in entries:
            rel = resolve_path(name, meta)
            lines.append(f"| [{name}]({rel}/) | {meta['description']} |")

        lines.append("")

    return "\n".join(lines)


def update_readme(content: str) -> str:
    tables = generate_tables()
    marker_re = re.compile(
        r"(<!-- BEGIN SKILLS -->\n).*?(<!-- END SKILLS -->)",
        re.DOTALL,
    )
    if not marker_re.search(content):
        print("ERROR: README.md missing <!-- BEGIN SKILLS --> / <!-- END SKILLS --> markers", file=sys.stderr)
        sys.exit(1)
    return marker_re.sub(rf"\1\n{tables}\2", content)


def main():
    warnings = validate()
    for w in warnings:
        print(f"  WARN: {w}", file=sys.stderr)

    if "--write" in sys.argv:
        original = README.read_text()
        updated = update_readme(original)
        if original == updated:
            print("README.md is already up to date.")
        else:
            README.write_text(updated)
            print(f"README.md updated. ({len(SKILLS)} skills across {len(CATEGORIES)} categories)")
    else:
        print(generate_tables())
        if warnings:
            print(f"\n({len(warnings)} warnings — see stderr)", file=sys.stderr)


if __name__ == "__main__":
    main()
