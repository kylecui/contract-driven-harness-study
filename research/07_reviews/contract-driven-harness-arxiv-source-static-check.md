# arXiv Source Package Static Check

Target package: `research/06_outputs/arxiv-source/`

Generated from: `research/06_outputs/contract-driven-harness-arxiv-draft.md`

Conversion script: `research/04_methods/scripts/convert_markdown_to_arxiv_tex.py`

Check date: 2026-06-09

## Result

**PASS for static arXiv source-package preparation.**

This report covers static source checks only. A later compile check was completed in `research/07_reviews/contract-driven-harness-arxiv-compile-check.md`.

## Package Files

| File | Status |
|---|---|
| `contract-driven-harness-arxiv.tex` | Present |
| `contract-driven-harness-references.bib` | Present |
| `README.md` | Present |

## Static Checks

| Check | Result |
|---|---|
| LaTeX document class present | PASS |
| `\begin{document}` and `\end{document}` present | PASS |
| Abstract represented as `abstract` environment | PASS |
| No `\section{Abstract}` heading | PASS |
| Markdown heading numbers stripped from sections/subsections | PASS |
| Body-level `[E:...]` tags absent | PASS |
| Body-level `[S:...]` tags absent | PASS |
| Markdown pipe-table rows absent | PASS |
| Distinct citation keys resolve to BibTeX entries | PASS |
| BibTeX entries are all used by the draft | PASS |

## Counts

- Distinct citation keys in LaTeX source: 22
- BibTeX entries: 22
- Missing BibTeX keys: 0
- Unused BibTeX keys: 0
- Inline `[E:...]` tags: 0
- Inline `[S:...]` tags: 0

## Known Limitations

1. Wide appendix longtables still need layout review after the successful LaTeX compile.
2. Final external release still needs author order, affiliation, acknowledgments, ethics/artifact statements, and artifact availability wording.

## Next Gate

Review the generated PDF for table overflow, bibliography rendering, appendix placement, and arXiv upload constraints.
