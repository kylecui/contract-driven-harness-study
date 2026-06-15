# Contract-Driven Harness v4 Body Freeze

Freeze date: 2026-06-15

Frozen source:
`research/06_outputs/contract-driven-harness-arxiv-v4-frozen.md`

Frozen PDF:
`research/06_outputs/contract-driven-harness-paper-v4-frozen.pdf`

Pre-freeze commit:
`f1b0a3bdadaf86034805db7861a20bd76310c845`

## Decision

The v4 body and empirical narrative are frozen.

The frozen artifacts preserve the reviewed account of:

- the mechanism-first method and repair-loop protocol;
- the Stage B v5.2 bounded null result;
- the Stage B v5.3 mixed paired-ablation result;
- the Stage B v5.4 bounded 40/40 stability confirmation;
- the exact McNemar correction and its limited-power interpretation;
- the `0.20` absolute risk-difference engineering gate;
- pooled and per-condition Wilson intervals;
- the paper's contribution boundaries, limitations, and non-claims.

No further provider run is required to support this v4 narrative.

## Frozen Artifact Hashes

| Artifact | SHA-256 |
| --- | --- |
| Frozen Markdown | `2a0d79c39f7ec8a6d7d89f425796cc7841a4f9c18e7eea2142bee4ac86fb2e33` |
| Frozen PDF | `0c3e26b4ccd9662e757c280c1078cdfae03592278b20d69f1c6062b0b4d52118` |

The frozen Markdown is byte-identical to the reviewed
`contract-driven-harness-arxiv-v4-draft.md`. The frozen PDF is
byte-identical to the reviewed
`contract-driven-harness-paper-v4-draft.pdf`.
The repository marks the frozen Markdown as `-text` so Git does not normalize
its historical mixed line endings; the staged repository object therefore
matches the recorded SHA-256.

## Freeze Verification

- 52 method-script unit tests passed.
- All 60 paper evidence references resolve in the evidence ledger.
- All 25 project source references resolve in the source index.
- All 22 external citation keys resolve in the v4 bibliography.
- The evidence ledger contains 187 valid JSONL records with no duplicate
  evidence IDs; the freeze record is `P2-E177`.
- The tracked public tree contains no detected credential or machine-private
  path.
- The earlier v3.1.1 Markdown and frozen-PDF hashes remain unchanged.

The frozen PDF inherits the pre-freeze compile and layout result: 23 pages,
281534 bytes, zero LaTeX errors, zero unresolved citations or references,
zero BibTeX warnings, and no sampled-page overlap or clipping.

## Still Open

The following publication-preparation work remains open:

- bibliography and citation normalization;
- venue-template adaptation and page-limit compression;
- moving detailed audit material, artifact IDs, or Appendix C content to a
  supplement;
- formalizing Figure 1;
- mechanical typesetting, accessibility, and metadata work;
- repository normalization that does not change the paper's claims.

These activities must produce derivative artifacts. They must not overwrite
the frozen Markdown or PDF.

## Change Control

- Typographical, citation, layout, and venue changes may be made only in a
  derivative submission source.
- A change to a quantitative result, empirical interpretation, contribution,
  limitation, or non-claim requires an explicit unfreeze decision or a new
  paper version.
- New provider runs, overhead comparisons, cross-provider evidence, or
  expanded task families belong to a post-freeze evidence track and, if
  integrated into the paper, to v5 or later.
- The frozen hashes above are the reference check for future release and
  submission work.
