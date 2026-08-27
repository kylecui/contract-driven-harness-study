# arXiv Submission Package

Built from the v5.1 working draft by `build_arxiv.py` (run from repo root:
`python paper/arxiv/build_arxiv.py`). Do not edit the generated files;
edit the draft and rebuild.

## Files

| File | Role |
|---|---|
| `contract-driven-harness-arxiv-v5.1.md` | Generated arXiv manuscript (no cite markers, real References section) |
| `contract-driven-harness-arxiv-v5.1.pdf` | Rendered PDF (37 pp) — the submission file |

## Submission metadata (copy into arXiv form)

- **Title**: Contracts as Task Skeleton: Externalizing Implicit Obligations for Bounded LLM-Agent Determinism
- **Authors**: [AUTHOR NAME + ORCID + AFFILIATION — fill before submitting]
- **Abstract**: use the manuscript Abstract verbatim (single paragraph, starts "Contract-driven harnesses make low-cost language-model agents inspectable...").
- **Primary category**: `cs.SE`
- **Cross-lists**: `cs.AI`, `cs.CR` (oracle-coupling audit as evaluator-trust topic)
- **Comments field** (suggested): `Working paper, 37 pages; reproducibility package with frozen SHA-256 artifacts maintained separately`
- **License**: arXiv non-exclusive license (default). Do NOT pick CC-BY unless you plan to reuse the text elsewhere under it.
- **DOI**: arXiv will assign one; record it back in this repo (README + submission plan) after posting.
- **Versioning policy**: post v1 now; on acceptance, upload the camera-ready as v2 with a "accepted at [venue]" comment. arXiv versions are immutable once announced — proofread the PDF one final time before submit.

## Pre-submission checklist

- [ ] Fill author name, ORCID, affiliation in the arXiv form (NOT in the PDF if anonymity matters later — note: arXiv posting breaks blind review; ISSTA/ASE/FSE/ICSE use non-blind or allow arXiv, USENIX Security allows arXiv; S&P has restrictions — verify current CFP policy per venue before posting if double-blind venues are on the strategy list)
- [ ] Proofread generated PDF (spot-check tables, Figure 5 caption, References)
- [ ] Decide whether to also upload the LaTeX source (optional; markdown-derived PDF alone is accepted)
- [ ] After posting: record arXiv ID/DOI in `README.md` and `paper/SUBMISSION-PLAN.md`
