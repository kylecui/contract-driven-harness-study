#!/usr/bin/env python3
"""Build the arXiv-ready manuscript from the v5.1 working draft.

Produces ``paper/arxiv/contract-driven-harness-arxiv-v5.1.md`` and its PDF:

- strips ``\\cite{...}`` markers (prose already carries author-year citations)
- removes working-draft genealogy from the header note
- replaces the pointer-only ``## Bibliography`` section with a real
  ``## References`` list generated from the .bib file (author-year style)
- drops the venue-conversion notes that instruct ourselves how to prepare
  for ACM/IEEE submission (they are not part of the manuscript)

Requires: pandoc + xelatex (see render_pdf.py).
"""

from __future__ import annotations

import re
import subprocess
import sys
import tempfile
from pathlib import Path

PAPER = Path(__file__).resolve().parents[1]
DRAFT = PAPER / "contract-driven-harness-arxiv-v5.1-draft.md"
BIB = PAPER / "contract-driven-harness-references.bib"
OUT_DIR = PAPER / "arxiv"
OUT_MD = OUT_DIR / "contract-driven-harness-arxiv-v5.1.md"
OUT_PDF = OUT_DIR / "contract-driven-harness-arxiv-v5.1.pdf"

CITE_RE = re.compile(r"\\cite\{[^}]*\}")


def parse_bib(path: Path) -> list[dict]:
    entries: list[dict] = []
    current: dict | None = None
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line.startswith("@"):
            if current:
                entries.append(current)
            current = {
                "type": line.split("{", 1)[0][1:].strip(),
                "key": line.split("{", 1)[1].rstrip(",").strip(),
            }
            continue
        if current is None:
            continue
        if line == "}":
            entries.append(current)
            current = None
            continue
        m = re.match(r"(\w+)\s*=\s*(.*)$", line)
        if m:
            field, value = m.group(1).lower(), m.group(2).strip().rstrip(",").strip()
            current[field] = value.strip("{} ")
    if current:
        entries.append(current)
    return entries


def fmt_authors(author: str) -> str:
    return author.replace("{", "").replace("}", "").replace("~", " ").replace("\\'e", "é")


def fmt_entry(entry: dict) -> str:
    authors = fmt_authors(entry.get("author", ""))
    year = entry.get("year", "n.d.")
    title = entry.get("title", "").replace("{", "").replace("}", "")
    pieces = []
    if entry["type"] == "article":
        venue = entry.get("journal", "")
        vol = entry.get("volume", "")
        no = entry.get("number", "")
        pages = entry.get("pages", "")
        venue_full = venue
        if vol:
            venue_full += f", {vol}"
        if no:
            venue_full += f"({no})"
        if pages:
            venue_full += f", pp. {pages.replace('--', '–')}"
        pieces = [venue_full]
    elif entry["type"] == "inproceedings":
        pieces = [entry.get("booktitle", "")]
    else:
        if "eprint" in entry:
            pieces = [f"arXiv:{entry['eprint']}"]
        elif "howpublished" in entry:
            pieces = [entry["howpublished"].replace("\\url{", "").rstrip("}")]
    doi = entry.get("doi", "")
    if doi:
        pieces.append(f"doi:{doi}")
    note = entry.get("note", "")
    tail = ". ".join(p for p in pieces if p)
    ref = f"{authors} ({year}). {title}."
    if tail:
        ref += f" {tail}."
    if note and "accessed" in note.lower():
        ref += f" [{note}]"
    return ref


def references_section() -> str:
    entries = parse_bib(BIB)
    def sort_key(e: dict) -> tuple[str, str]:
        first = fmt_authors(e.get("author", "")).split(" and ")[0].split(",")[0].strip()
        return (first.lower(), e.get("year", ""))
    lines = ["## References", ""]
    for e in sorted(entries, key=sort_key):
        lines.append(f"- {fmt_entry(e)}")
    return "\n".join(lines) + "\n"


def build_markdown() -> str:
    text = DRAFT.read_text(encoding="utf-8")
    # 1. strip \cite markers
    text = CITE_RE.sub("", text)
    # 2. clean header genealogy note
    text = text.replace(
        "Version 5.1 evidence-extension draft derived from the v5 body; adds the "
        "oracle-coupling provenance audit (§4.14, Figure 5). External literature "
        "citations use prose references; empirical evidence traceability is "
        "preserved in Appendix C and the reproducibility package.\n",
        "",
    )
    # 3. replace pointer Bibliography section (from '## Bibliography' up to next '## ') with real references
    m = re.search(r"^## Bibliography\n.*?(?=^## |\Z)", text, flags=re.S | re.M)
    if not m:
        raise SystemExit("Bibliography section not found")
    text = text[: m.start()] + references_section() + "\n" + text[m.end() :]
    # 4. drop arXiv/venue preparation meta-paragraph if it survived inside another section
    text = re.sub(
        r"For arXiv preparation, compile this manuscript.*?(?=\n[A-Z#>]|\Z)",
        "",
        text,
        flags=re.S,
    )
    text = re.sub(r"\n{4,}", "\n\n\n", text)
    return text


def render(md_text: str) -> None:
    OUT_DIR.mkdir(exist_ok=True)
    OUT_MD.write_text(md_text, encoding="utf-8", newline="\n")
    with tempfile.NamedTemporaryFile(
        "w", suffix=".md", encoding="utf-8", newline="\n", delete=False
    ) as fh:
        fh.write(md_text)
        tmp = Path(fh.name)
    try:
        subprocess.run(
            [
                "pandoc", str(tmp), "-o", str(OUT_PDF),
                "--pdf-engine=xelatex",
                "-V", "geometry:margin=1in",
                "-V", "fontsize=11pt",
                "-V", "mainfont=Times New Roman",
                "-V", "monofont=Consolas",
                "-V", "CJKmainfont=SimSun",
                "-V", "colorlinks=true",
            ],
            check=True,
        )
    finally:
        tmp.unlink(missing_ok=True)


def main() -> int:
    md = build_markdown()
    leftover = set(re.findall(r"\\[a-zA-Z]+", md))
    if leftover:
        print(f"WARN: leftover LaTeX commands: {sorted(leftover)[:5]}", file=sys.stderr)
    render(md)
    print(f"wrote {OUT_MD}")
    print(f"wrote {OUT_PDF} ({OUT_PDF.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
