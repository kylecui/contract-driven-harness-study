# arXiv Source Package Compile Check

Target package: `research/06_outputs/arxiv-source/`

Main source: `research/06_outputs/arxiv-source/contract-driven-harness-arxiv.tex`

Generated PDF: `research/06_outputs/arxiv-source/contract-driven-harness-arxiv.pdf`

Check date: 2026-06-09

## Result

**PASS for LaTeX + BibTeX compilation.**

The package compiles to a 17-page PDF using MiKTeX 25.12 with the standard sequence:

1. `pdflatex -interaction=nonstopmode -halt-on-error contract-driven-harness-arxiv.tex`
2. `bibtex contract-driven-harness-arxiv`
3. `pdflatex -interaction=nonstopmode -halt-on-error contract-driven-harness-arxiv.tex`
4. `pdflatex -interaction=nonstopmode -halt-on-error contract-driven-harness-arxiv.tex`

## Environment

| Item | Result |
|---|---|
| LaTeX distribution | MiKTeX 25.12 |
| Install scope | User-level install |
| `pdflatex` | Available |
| `xelatex` | Available |
| `lualatex` | Available |
| `bibtex` | Available |
| User PATH updated | Yes |

MiKTeX installed several missing first-use packages during compilation, including `ltxcmds`, `infwarerr`, `hycolor`, `gettitlestring`, and `kvoptions`.

## Compile Checks

| Check | Result |
|---|---|
| PDF generated | PASS |
| PDF size | 199501 bytes |
| PDF page count | 17 |
| Page size probe | Letter, 612 x 792 pt |
| LaTeX fatal errors | 0 |
| LaTeX errors | 0 |
| Emergency stops | 0 |
| Undefined citations | 0 |
| Undefined references | 0 |
| BibTeX warnings | 0 |
| Rerun warnings after final pass | 0 |

## Layout Warnings

The compile log still contains layout warnings:

| Warning type | Count | Interpretation |
|---|---:|---|
| Overfull hbox | 8 | Long inline paths, metric names, and dense result strings exceed line width in a few paragraphs. |
| Underfull hbox | 130 | Narrow table columns in Appendix B/C create loose line breaks. |
| Infinite glue shrinkage ignored | 4 | Longtable page splitting is stressed by dense appendix tables, but compilation continues and produces output. |

These are not source/package failures, but they should be reviewed before public posting. The likely fix is to move Appendix C to supplementary material or redesign the appendix tables with smaller type, wider landscape pages, or a more compact evidence-trace format.

## Next Gate

Run a human PDF layout review and decide whether Appendix C stays in the main PDF or moves to supplementary material before arXiv posting.
