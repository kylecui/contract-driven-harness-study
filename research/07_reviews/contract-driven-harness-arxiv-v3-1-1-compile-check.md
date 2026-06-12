# arXiv v3.1.1 Compile Check

Target package: `research/06_outputs/arxiv-source/`

Main source: `research/06_outputs/arxiv-source/contract-driven-harness-arxiv.tex`

Reader PDF: `research/06_outputs/contract-driven-harness-paper-v3.1.1.pdf`

Check date: 2026-06-12

## Result

**PASS for v3.1.1 LaTeX + BibTeX compilation.**

The v3.1.1 package compiles to a 20-page PDF using MiKTeX 25.12 with the standard sequence:

1. `pdflatex -interaction=nonstopmode -halt-on-error contract-driven-harness-arxiv.tex`
2. `bibtex contract-driven-harness-arxiv`
3. `pdflatex -interaction=nonstopmode -halt-on-error contract-driven-harness-arxiv.tex`
4. `pdflatex -interaction=nonstopmode -halt-on-error contract-driven-harness-arxiv.tex`

## V3.1.1 Scope

- Applied the accepted local changes from the PEtFiSh-style cross-review.
- Tied the Abstract scope to failures observed in low-cost-model runs.
- Moved Stage 7e/Stage 7-next support after the Abstract's method statement.
- Replaced residual lecture-note transitions in the Introduction, Methods, and Discussion.
- Added the nonzero-baseline condition to the Results overview gap-compression claim.
- Reframed the Related Work contribution as operationally different rather than merely narrower.
- Kept the existing Conclusion without adding another defensive non-claim sentence.

No model runs, metrics, empirical claims, or citation keys changed.

## Compile Checks

| Check | Result |
|---|---|
| PDF generated | PASS |
| PDF size | 268210 bytes |
| PDF page count | 20 |
| LaTeX fatal errors | 0 |
| LaTeX errors | 0 |
| Emergency stops | 0 |
| Undefined citations | 0 |
| Undefined references | 0 |
| BibTeX warnings | 0 |
| Rerun warnings after final pass | 0 |

## Layout Warnings

| Warning type | Count | Interpretation |
|---|---:|---|
| Overfull hbox | 9 | Long metric names, result strings, paths, and bibliography path references still exceed line width. |
| Underfull hbox | 5 | Remaining loose line breaks are concentrated in bibliography entries. |
| Infinite glue shrinkage ignored | 3 | Dense longtable page splitting remains stressed. |

These are existing layout concerns rather than blockers introduced by the v3.1.1 wording patch. Citation normalization and final venue layout remain separate tasks.
