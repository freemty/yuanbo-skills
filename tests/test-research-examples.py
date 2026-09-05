#!/usr/bin/env python3
"""Rebuild retained independent consumer-test artifacts; visual QA is separate."""
import argparse
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True, help="new output directory")
    args = parser.parse_args()
    output = args.out.resolve()
    output.mkdir(parents=True, exist_ok=False)
    fixtures = ROOT / "tests/fixtures/research-artifacts"
    scripts = ROOT / "skills/research-slides/scripts"
    shutil.copy2(fixtures / "fixtures.md", output / "fixtures.md")
    for name, pages in (("queue", 5), ("midpoint", 8), ("adaptive", 7)):
        target = output / name
        subprocess.run([sys.executable, str(scripts / "init_research_deck.py"), str(target)], check=True, capture_output=True)
        for source in (fixtures / name).iterdir():
            shutil.copy2(source, target / source.name)
        result = subprocess.run([sys.executable, str(scripts / "check_deck.py"), str(target / "main.tex"), "--out", str(target / "previews")], text=True, capture_output=True)
        (target / "check.txt").write_text(result.stdout + result.stderr)
        if result.returncode:
            raise SystemExit(result.stdout + result.stderr)
        info = subprocess.run(["pdfinfo", str(target / "main.pdf")], text=True, capture_output=True, check=True).stdout
        actual = next(int(line.split()[1]) for line in info.splitlines() if line.startswith("Pages:"))
        assert actual == pages, f"unexpected page drift in fixed fixture {name}: {actual}"
        print(f"{name}: {actual} pages built; inspect previews before visual approval")
    print(output)


if __name__ == "__main__":
    main()
