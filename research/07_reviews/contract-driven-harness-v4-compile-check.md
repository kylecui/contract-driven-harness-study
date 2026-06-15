# Contract-Driven Harness v4 Compile And Layout Check

Reviewed: 2026-06-15

Target package:
`research/06_outputs/arxiv-source-v4/`

Reader PDF:
`research/06_outputs/contract-driven-harness-paper-v4-draft.pdf`

Result: **PASS**

## Build

The v4 evidence-extension source compiled with MiKTeX 25.12 using:

1. `pdflatex -interaction=nonstopmode -halt-on-error`
2. `bibtex`
3. `pdflatex -interaction=nonstopmode -halt-on-error`
4. `pdflatex -interaction=nonstopmode -halt-on-error`

## Checks

| Check | Result |
|---|---:|
| PDF pages | 23 |
| PDF size | 281534 bytes |
| PDF SHA-256 | `0c3e26b4ccd9662e757c280c1078cdfae03592278b20d69f1c6062b0b4d52118` |
| LaTeX errors | 0 |
| Undefined citations | 0 |
| Undefined references | 0 |
| BibTeX warnings | 0 |
| Distinct citation keys | 22 |
| BibTeX entries | 22 |
| Missing or unused BibTeX entries | 0 |

MiKTeX reported that its package update check had not been run. This did not
affect compilation.

## Layout Review

Pages 1, 5, 10, 11, 13, 14, 15, 17, and 20 were rendered and inspected.

- The title page carries the June 15, 2026 draft date and no converter banner.
- The metric guide is readable and includes the human-preference boundary.
- Table 4 uses fixed-width columns, allows the repair description to wrap,
  keeps allowed claims short, separates ablation from stability, and continues
  cleanly from page 10 to page 11.
- The Methods threshold definition, three-decimal McNemar result, and
  limited-power statement are readable without overlap or clipping.
- The Stage B condition table reports the five per-condition Wilson intervals
  without overlap, clipping, or ambiguous pooling.
- The Stage B result section, current non-claims, contribution alignment, and
  evidence traceability appendix show no overlap or clipped content.

## Nonblocking Warnings

| Warning | Count | Assessment |
|---|---:|---|
| Overfull hbox | 12 | Long metric names, result strings, contribution-table text, and repository paths. |
| Underfull hbox | 5 | Bibliography URL wrapping. |
| Infinite glue shrinkage ignored | 5 | Longtable page splitting. |

The largest overflow is an existing long reproducibility-package path in the
bibliography section. The new Stage B paragraph produces a 4.67 pt warning,
and the contribution table produces a 35.21 pt warning. Sampled pages remain
readable. These warnings are venue-layout debt, not evidence or compile
blockers.

## Freeze Check

The v3.1.1 artifacts remain unchanged:

- Markdown SHA-256:
  `67cfa09c4e947fd06c13c0cf34c4b4dd8be2fc7aed703f8b939fbeba40b37f9f`
- Frozen PDF SHA-256:
  `eb7ad4afc9cd8086a0ab7710da2f673304775d95203d27c5ea4fa16807613bfb`
