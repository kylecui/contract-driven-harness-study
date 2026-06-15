# Contract-Driven Harness v4 Stage-Label Presentation Pass

Reviewed: 2026-06-15

Result: **PASS**

## Review Disposition

The comment is classified as a valid presentation criticism. The internal
sequence identifiers are necessary for artifact traceability, but their
project-history origin is not self-explanatory to a first-time paper reader.

The change was adopted in a presentation-layer derivative. The frozen v4
Markdown and PDF were not modified.

## Changes Applied

1. Added a Methods mapping from internal stage IDs to paper-facing labels and
   purposes.
2. Added descriptive labels at the first Introduction occurrence of Stage 7e,
   Stage 7-next, and Stage B.
3. Renamed the Results headings and first-use sentences for:
   - Mechanism-Atom Pilot (Stage 6);
   - Partial Macro Composition (Stage 7p);
   - Atom Revision and Repair (Stage 7r / 7r.1);
   - Evidence-Decision Macro Repair (Stage 7e);
   - Neighboring Macro Transfer (Stage 7-next);
   - Controlled State-Mutation Study (Stage B).
4. Retained every internal identifier and version number used by the
   reproducibility package.
5. Added a dedicated converter column-width rule for the new three-column
   mapping table.

## Artifact Boundary

Derivative Markdown:
`research/06_outputs/contract-driven-harness-arxiv-v4-presentation-draft.md`

Derivative PDF:
`research/06_outputs/contract-driven-harness-paper-v4-presentation-draft.pdf`

Derivative source package:
`research/06_outputs/arxiv-source-v4-presentation/`

| Artifact | SHA-256 |
| --- | --- |
| Presentation Markdown (Git blob, LF) | `8df54751245315ab785d07a7ea1caadbd3310b77e7ae1761e0501bd4595a8fda` |
| Presentation Markdown (Windows working tree) | `11b41a1072781896b4397d8f2e77521dd52f578dcec5f5935ab55bb8dc3d6005` |
| Presentation PDF | `c1c815b0dd1f8a0209aefda35cbb2d70fdff2568245d27b560234b85d0d394ed` |

The two Markdown hashes differ only because the Windows checkout converts the
repository's LF line endings in the working tree. The Git-blob hash is the
portable repository reference.

The frozen v4 reference hashes remain:

- Markdown:
  `2a0d79c39f7ec8a6d7d89f425796cc7841a4f9c18e7eea2142bee4ac86fb2e33`;
- PDF:
  `0c3e26b4ccd9662e757c280c1078cdfae03592278b20d69f1c6062b0b4d52118`.

## Verification

- The line-ending-insensitive semantic diff contains only stage-label
  additions, the Methods mapping table, and corresponding heading/first-use
  wording.
- All 60 evidence references are unchanged.
- All 25 project source references are unchanged.
- All 22 external citation keys resolve.
- No quantitative result, statistical interpretation, contribution,
  limitation, non-claim, evidence ID, or source ID changed.
- The LaTeX + BibTeX build completed without undefined citations or
  references.
- The derivative PDF contains 24 pages and is 283652 bytes.
- Manual inspection of pages 6, 7, 12, 13, and 14 found no overlap, clipping,
  orphaned mapping explanation, or unreadable stage heading.

## Decision

Use the presentation derivative as the current reader-facing v4 draft. Keep
the frozen v4 artifacts as the immutable empirical reference. This pass does
not create a new empirical paper version and does not reopen the v4 evidence
narrative.
