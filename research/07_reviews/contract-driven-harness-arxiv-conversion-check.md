# arXiv-Style Draft Conversion Check

Target draft: `research/06_outputs/contract-driven-harness-arxiv-draft.md`

BibTeX file: `research/06_outputs/contract-driven-harness-references.bib`

Check date: 2026-06-09

## Result

**PASS for arXiv-style working draft preparation.**

## Checks

| Check | Result |
|---|---|
| Body-level `[E:...]` tags removed | PASS |
| Body-level `[S:...]` tags removed | PASS |
| Evidence traceability preserved in Appendix C | PASS |
| Reproducibility package section added | PASS |
| Bibliography points to BibTeX file | PASS |
| `\cite{...}` keys resolve to BibTeX entries | PASS |
| BibTeX entries are all used by the draft | PASS |
| Placeholder author groups in BibTeX | PASS; none found |

## Counts

- Distinct citation keys in arXiv draft: 22
- BibTeX entries: 22
- Missing BibTeX keys: 0
- Unused BibTeX keys: 0
- Inline `[E:...]` tags: 0
- Inline `[S:...]` tags: 0

## Remaining Work

The current file is an arXiv-style Markdown working draft. A LaTeX source package has since been generated, checked statically, and compiled successfully. See `research/07_reviews/contract-driven-harness-arxiv-source-static-check.md` and `research/07_reviews/contract-driven-harness-arxiv-compile-check.md`. Remaining work before public posting:

1. Decide whether Appendix C remains in the main PDF or moves to supplementary material.
2. Verify final author order and spelling in the BibTeX file.
3. Add any required acknowledgments, ethics statement, and artifact availability statement.
4. Run a human PDF layout review, focusing on longtable overflow and dense appendix tables.
