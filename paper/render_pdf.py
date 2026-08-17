#!/usr/bin/env python3
"""Render the paper markdown draft to PDF.

Usage (from repository root, requires pandoc + xelatex, e.g. MiKTeX):

    python paper/render_pdf.py [draft-stem]

Renders ``paper/contract-driven-harness-arxiv-<stem>-draft.md`` to a same-name
PDF next to the markdown source. ``\\cite{...}`` keys are stripped before
rendering because the drafts carry author-year prose references inline; the
BibTeX keys exist for a future LaTeX build. CJK glyphs (the quoted Kimi
README excerpt in §4.9) fall back to SimSun / Noto Sans CJK.
"""

from __future__ import annotations

import re
import subprocess
import sys
import tempfile
from pathlib import Path

PAPER_DIR = Path(__file__).resolve().parent
DEFAULT_STEM = "v5.1"

CITE_PATTERN = re.compile(r"\\cite\{[^}]*\}")


def build(stem: str) -> Path:
    source = PAPER_DIR / f"contract-driven-harness-arxiv-{stem}-draft.md"
    target = PAPER_DIR / f"contract-driven-harness-arxiv-{stem}-draft.pdf"
    if not source.is_file():
        raise SystemExit(f"missing draft: {source}")

    text = CITE_PATTERN.sub("", source.read_text(encoding="utf-8"))
    leftover = re.findall(r"\\[a-zA-Z]+", text)
    if leftover:
        raise SystemExit(f"unhandled LaTeX commands remain: {sorted(set(leftover))[:5]}")

    with tempfile.NamedTemporaryFile(
        "w", suffix=".md", encoding="utf-8", newline="\n", delete=False
    ) as handle:
        handle.write(text)
        temp_path = Path(handle.name)

    command = [
        "pandoc",
        str(temp_path),
        "-o",
        str(target),
        "--pdf-engine=xelatex",
        "-V",
        "geometry:margin=1in",
        "-V",
        "fontsize=11pt",
        "-V",
        "mainfont=Times New Roman",
        "-V",
        "monofont=Consolas",
        "-V",
        "CJKmainfont=SimSun",
        "-V",
        "colorlinks=true",
    ]
    try:
        subprocess.run(command, check=True)
    finally:
        temp_path.unlink(missing_ok=True)
    return target


def main() -> int:
    stem = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_STEM
    target = build(stem)
    print(f"wrote {target} ({target.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
