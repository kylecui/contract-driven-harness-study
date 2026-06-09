"""Convert the contract-driven harness Markdown draft to a simple arXiv LaTeX source.

This is a narrow converter for the paper draft in this repository. It handles the
Markdown constructs used in the draft: headings, paragraphs, bullets, blockquotes,
fenced code, and pipe tables.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


SPECIALS = {
    "&": r"\&",
    "%": r"\%",
    "$": r"\$",
    "#": r"\#",
    "_": r"\_",
    "{": r"\{",
    "}": r"\}",
    "~": r"\textasciitilde{}",
    "^": r"\textasciicircum{}",
}


def escape_latex(text: str) -> str:
    placeholders: list[str] = []

    def protect(pattern: str, value: str) -> str:
        token = f"@@PROTECTED{len(placeholders)}@@"
        placeholders.append(value)
        return token

    text = re.sub(r"\\cite\{[^}]+\}", lambda m: protect("", m.group(0)), text)
    text = re.sub(
        r"`([^`]+)`",
        lambda m: protect("", r"\path|" + m.group(1).replace("|", "/") + "|"),
        text,
    )
    text = re.sub(
        r"https?://[^\s)]+",
        lambda m: protect("", r"\url{" + m.group(0) + "}"),
        text,
    )

    text = "".join(SPECIALS.get(ch, ch) for ch in text)
    for idx, value in enumerate(placeholders):
        text = text.replace(f"@@PROTECTED{idx}@@", value)
    return text


def split_table_row(line: str) -> list[str]:
    stripped = line.strip().strip("|")
    return [cell.strip() for cell in stripped.split("|")]


def is_table_separator(line: str) -> bool:
    cells = split_table_row(line)
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell.strip()) for cell in cells)


def convert_table(lines: list[str]) -> str:
    header = split_table_row(lines[0])
    rows = [split_table_row(line) for line in lines[2:]]
    col_count = len(header)
    spec = "p{0.22\\linewidth}" + "p{0.22\\linewidth}" * max(0, col_count - 1)
    out = [r"\begin{longtable}{" + spec + "}", r"\toprule"]
    out.append(" & ".join(escape_latex(c) for c in header) + r" \\")
    out.extend([r"\midrule", r"\endfirsthead", r"\toprule"])
    out.append(" & ".join(escape_latex(c) for c in header) + r" \\")
    out.extend([r"\midrule", r"\endhead"])
    for row in rows:
        padded = row + [""] * (col_count - len(row))
        out.append(" & ".join(escape_latex(c) for c in padded[:col_count]) + r" \\")
    out.extend([r"\bottomrule", r"\end{longtable}"])
    return "\n".join(out)


def strip_heading_number(text: str) -> str:
    return re.sub(r"^\d+(?:\.\d+)*\.?\s+", "", text.strip())


def convert_markdown(markdown: str) -> tuple[str, str]:
    lines = markdown.splitlines()
    title = "Contract-Driven Harness Engineering for Reliable Low-Cost Agent Tasks"
    body: list[str] = []
    i = 0
    in_code = False
    in_itemize = False
    in_enumerate = False
    in_quote = False
    in_abstract = False
    para: list[str] = []

    def flush_para() -> None:
        nonlocal para
        if para:
            body.append(escape_latex(" ".join(p.strip() for p in para)))
            body.append("")
            para = []

    def close_itemize() -> None:
        nonlocal in_itemize
        if in_itemize:
            body.append(r"\end{itemize}")
            body.append("")
            in_itemize = False

    def close_enumerate() -> None:
        nonlocal in_enumerate
        if in_enumerate:
            body.append(r"\end{enumerate}")
            body.append("")
            in_enumerate = False

    def close_abstract() -> None:
        nonlocal in_abstract
        if in_abstract:
            body.append(r"\end{abstract}")
            body.append("")
            in_abstract = False

    def close_quote() -> None:
        nonlocal in_quote
        if in_quote:
            body.append(r"\end{quote}")
            body.append("")
            in_quote = False

    while i < len(lines):
        line = lines[i]

        if line.strip().startswith("```"):
            flush_para()
            close_itemize()
            close_enumerate()
            close_quote()
            if not in_code:
                body.append(r"\begin{verbatim}")
                in_code = True
            else:
                body.append(r"\end{verbatim}")
                body.append("")
                in_code = False
            i += 1
            continue

        if in_code:
            body.append(line)
            i += 1
            continue

        if line.strip().startswith("arXiv-style working draft derived"):
            i += 1
            continue

        if line.startswith("# "):
            title = line[2:].strip()
            i += 1
            continue

        if re.match(r"^\|.*\|$", line) and i + 1 < len(lines) and is_table_separator(lines[i + 1]):
            flush_para()
            close_itemize()
            close_enumerate()
            close_quote()
            table_lines = [line, lines[i + 1]]
            i += 2
            while i < len(lines) and re.match(r"^\|.*\|$", lines[i]):
                table_lines.append(lines[i])
                i += 1
            body.append(convert_table(table_lines))
            body.append("")
            continue

        if line.startswith("## "):
            flush_para()
            close_itemize()
            close_enumerate()
            close_quote()
            close_abstract()
            heading = strip_heading_number(line[3:])
            if heading.lower() == "abstract":
                body.append(r"\begin{abstract}")
                in_abstract = True
            else:
                body.append(r"\section{" + escape_latex(heading) + "}")
            body.append("")
            i += 1
            continue

        if line.startswith("### "):
            flush_para()
            close_itemize()
            close_enumerate()
            close_quote()
            heading = strip_heading_number(line[4:])
            body.append(r"\subsection{" + escape_latex(heading) + "}")
            body.append("")
            i += 1
            continue

        if line.startswith("> "):
            flush_para()
            close_itemize()
            close_enumerate()
            if not in_quote:
                body.append(r"\begin{quote}")
                in_quote = True
            body.append(escape_latex(line[2:].strip()))
            i += 1
            continue

        if re.match(r"^\s*-\s+", line):
            flush_para()
            close_enumerate()
            close_quote()
            if not in_itemize:
                body.append(r"\begin{itemize}")
                in_itemize = True
            item = re.sub(r"^\s*-\s+", "", line).strip()
            body.append(r"\item " + escape_latex(item))
            i += 1
            continue

        if re.match(r"^\s*\d+\.\s+", line):
            flush_para()
            close_itemize()
            close_quote()
            if not in_enumerate:
                body.append(r"\begin{enumerate}")
                in_enumerate = True
            item = re.sub(r"^\s*\d+\.\s+", "", line).strip()
            body.append(r"\item " + escape_latex(item))
            i += 1
            continue

        if not line.strip():
            flush_para()
            close_itemize()
            close_enumerate()
            close_quote()
            i += 1
            continue

        para.append(line)
        i += 1

    flush_para()
    close_itemize()
    close_enumerate()
    close_quote()
    close_abstract()
    return title, "\n".join(body)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--bib", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    source = Path(args.input)
    bib = Path(args.bib)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    title, body = convert_markdown(source.read_text(encoding="utf-8"))
    body = body.replace(
        "arXiv-style working draft derived from the evidence-traceable full draft. External literature citations use BibTeX keys; empirical evidence traceability is preserved in Appendix C and the reproducibility package.\n\n",
        "",
    )

    tex = rf"""\documentclass[11pt]{{article}}
\usepackage[margin=1in]{{geometry}}
\usepackage[T1]{{fontenc}}
\usepackage[utf8]{{inputenc}}
\usepackage{{booktabs}}
\usepackage{{longtable}}
\usepackage{{array}}
\usepackage{{url}}
\usepackage{{hyperref}}
\usepackage{{enumitem}}
\usepackage{{verbatim}}

\title{{{escape_latex(title)}}}
\author{{Contract-Driven Harness Study}}
\date{{June 9, 2026}}

\begin{{document}}
\maketitle

{body}

\bibliographystyle{{plain}}
\bibliography{{contract-driven-harness-references}}

\end{{document}}
"""
    (output_dir / "contract-driven-harness-arxiv.tex").write_text(tex, encoding="utf-8")
    (output_dir / "contract-driven-harness-references.bib").write_text(
        bib.read_text(encoding="utf-8"), encoding="utf-8"
    )
    (output_dir / "README.md").write_text(
        "# arXiv Source Package\n\n"
        "Generated from `research/06_outputs/contract-driven-harness-arxiv-draft.md`.\n\n"
        "Files:\n\n"
        "- `contract-driven-harness-arxiv.tex`\n"
        "- `contract-driven-harness-references.bib`\n\n"
        "Compile with a standard LaTeX + BibTeX workflow, for example `pdflatex`, "
        "`bibtex`, `pdflatex`, `pdflatex`. Local compilation was not performed if "
        "a LaTeX engine is unavailable in the workspace.\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
