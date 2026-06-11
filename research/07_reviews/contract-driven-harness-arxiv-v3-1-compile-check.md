# arXiv v3.1 Compile Check

Target package: `research/06_outputs/arxiv-source/`

Main source: `research/06_outputs/arxiv-source/contract-driven-harness-arxiv.tex`

Reader PDF: `research/06_outputs/contract-driven-harness-paper-v3.1.pdf`

Check date: 2026-06-11

## Result

**PASS for v3.1 LaTeX + BibTeX compilation after the human-style pass.**

The v3.1 package compiles to a 19-page PDF using MiKTeX 25.12 with the standard sequence:

1. `pdflatex -interaction=nonstopmode -halt-on-error contract-driven-harness-arxiv.tex`
2. `bibtex contract-driven-harness-arxiv`
3. `pdflatex -interaction=nonstopmode -halt-on-error contract-driven-harness-arxiv.tex`
4. `pdflatex -interaction=nonstopmode -halt-on-error contract-driven-harness-arxiv.tex`

## V3.1 Content Covered

- Applied a strict human-style pass to reduce generic AI-like paper voice while preserving the empirical claim boundary.
- Compressed the main empirical findings table from seven columns to six.
- Applied fixed-width ragged-right table columns for the main findings table and metric guide table.
- Added a metric reading-guide table in Methods.
- Added an explicit note that metrics evaluate contract adherence rather than open-ended quality or human preference.
- Added a closest-prior-work paragraph to Related Work.
- Reduced repetitive `targeted smoke runs` wording in the Stage 7e/Stage 7-next results.
- Added reviewer-facing reproducibility wording that stage reports include exact rerun commands or script paths when available.
- Added a visible deferred-work register for citation normalization, formal figure conversion, Appendix C placement, and future experiment expansion.

## Compile Checks

| Check | Result |
|---|---|
| PDF generated | PASS |
| PDF size | 267637 bytes |
| PDF page count | 19 |
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
| Overfull hbox | 9 | Remaining long metric names, result strings, paths, and bibliography path references exceed line width. Table 4 now has only one minor 0.8pt overfull warning. |
| Underfull hbox | 5 | Remaining loose line breaks are limited after fixed-width ragged-right table columns. |
| Infinite glue shrinkage ignored | 4 | Longtable page splitting remains stressed by dense tables. |

These warnings are not compile blockers. They are tracked by the deferred Appendix C/table-layout work item and should be reviewed before declaring a release-ready arXiv or venue package.
