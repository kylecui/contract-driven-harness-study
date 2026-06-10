# arXiv v2 Source Package Compile and Public Scan

Target package: `research/06_outputs/arxiv-source/`

Main source: `research/06_outputs/arxiv-source/contract-driven-harness-arxiv.tex`

Generated from: `research/06_outputs/contract-driven-harness-arxiv-draft.md`

Generated PDF: `research/06_outputs/arxiv-source/contract-driven-harness-arxiv.pdf`

Check date: 2026-06-10

## Result

**PASS for v2 LaTeX + BibTeX compilation.**

The v2 package compiles to a 19-page PDF using MiKTeX 25.12 with the standard sequence:

1. `pdflatex -interaction=nonstopmode -halt-on-error contract-driven-harness-arxiv.tex`
2. `bibtex contract-driven-harness-arxiv`
3. `pdflatex -interaction=nonstopmode -halt-on-error contract-driven-harness-arxiv.tex`
4. `pdflatex -interaction=nonstopmode -halt-on-error contract-driven-harness-arxiv.tex`

The first sandboxed compile attempt failed because MiKTeX needed to create or update user-level configuration under `AppData/Roaming/MiKTeX`. The same compile sequence succeeded when run with user-level filesystem access.

## v2 Content Delta Covered

The regenerated package includes the first v2 paper revision pass after the 2026-06-10 external review:

- Sharpened abstract and introduction around bounded low-cost-model enablement rather than general model equivalence.
- Explicit distinction among model capability, harness specification, and workflow composition.
- Related-work comparison table.
- Formal mechanism-atom admission criteria.
- Result-boundary table separating supported claims from non-claims.
- Clearer wording that PEtFiSh is the implementation context, not the transferable claim itself.
- Public repository locator: `https://github.com/kylecui/contract-driven-harness-study`.

## Compile Checks

| Check | Result |
|---|---|
| PDF generated | PASS |
| PDF size | 206304 bytes |
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
| Overfull hbox | 8 | Long inline paths, metric names, source IDs, and dense result strings exceed line width in a few paragraphs. |
| Underfull hbox | 161 | Narrow table columns and dense appendix tables create loose line breaks. |
| Infinite glue shrinkage ignored | 5 | Longtable page splitting is stressed by dense tables, but compilation continues and produces output. |

These warnings are not source-package failures. They remain a publication-preparation issue. Before public arXiv posting, the likely fix is to move the densest evidence trace table to supplementary material or redesign appendix tables with smaller type, wider layout, or a more compact trace format.

## Public Artifact Safety Scan

The repository is public, so the v2 pass included a local public-artifact scan.

| Check | Result |
|---|---|
| Files larger than 50MB | 0 |
| `SILICONFLOW_API_KEY` literal | 0 matches |
| `OPENAI_API_KEY` literal | 0 matches |
| `sk-...` secret-like token pattern | 0 matches |
| `Bearer ...` token-like pattern | 0 matches |
| `api_key` / `apikey` / `password` patterns | 0 matches after excluding known prompt and benchmark artifacts |

The scan does not prove the repository is free of all sensitive data, but it found no obvious large artifact or secret-pattern blocker for keeping the repository public.

## Remaining Gate

Run a human PDF layout review and decide whether Appendix C and dense evidence trace tables should remain in the main PDF or move to supplementary material.
