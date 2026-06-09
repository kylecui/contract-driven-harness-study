# Venue And Citation Style Decision Brief

Target document: `research/06_outputs/contract-driven-harness-paper-draft.md`

Prepared on: 2026-06-09

## Decision Needed

Choose the next citation and submission style for the contract-driven harness paper.

This decision affects:

- citation syntax in the paper body;
- reference formatting;
- whether local artifacts are cited as a reproducibility package, appendix, or supplementary material;
- how much the paper must be compressed;
- whether the current evidence is framed as an arXiv methodology preprint or as a conference-style empirical paper.

## Current Draft State

The paper currently has:

- working full draft;
- internal `[E:...]` evidence citations;
- internal `[S:...]` source citations;
- Appendix C evidence traceability matrix;
- venue-neutral citation metadata;
- venue-neutral BibTeX draft;
- citation audit with conditional pass for internal research use.

The paper does not yet have:

- target venue formatting;
- formal inline citation syntax;
- venue-specific bibliography style;
- final source locators for every local method document;
- publication-ready related-work author metadata for every citation style.

## Options

| Option | Fit | Pros | Costs/Risks |
|---|---|---|---|
| arXiv-style working paper | Best immediate fit | Preserves long methodology, negative results, artifact trail, and internal evidence appendix. Fastest path to a coherent public preprint. | Less selective validation; still needs careful bibliography cleanup before public release. |
| ACM conference style | Good if targeting HCI/software engineering/AI systems venues | Natural fit for methodology, artifacts, and reproducibility framing. | Requires compression, strict reference style, possibly anonymization and artifact appendix discipline. |
| IEEE conference style | Good if targeting systems/engineering venues | Clear numbered citations and compact methods/results structure. | Can make qualitative claim-boundary discussion feel cramped; will need significant formatting work. |
| APA/author-year style | Good for a research report or thesis-style manuscript | Easier for narrative literature review and methodology discussion. | Less natural for CS conference submission; citation clutter may be high. |

## Recommendation

Default next step: **prepare an arXiv-style working paper version first**, while preserving a path to ACM or IEEE later.

Reason:

1. The current evidence is strongest as a methodology and bounded empirical case study.
2. The paper needs to preserve negative results and claim boundaries; arXiv-style preprint space is more forgiving.
3. The evidence ledger and local artifacts are unusual for a standard short conference paper but valuable for a working paper.
4. Once the arXiv-style version is clean, compression into ACM/IEEE is easier than trying to compress too early.

## Proposed Citation Handling By Option

### arXiv-style working paper

- Replace body `[S:...]` tags with BibTeX citations.
- Move body `[E:...]` tags mostly into Appendix C and artifact notes.
- Keep Appendix C as evidence traceability.
- Add a reproducibility package section.

### ACM or IEEE

- Convert all external citations to numbered references.
- Collapse internal evidence IDs into appendix or supplementary material.
- Replace long Stage-by-Stage prose with compact tables.
- Shorten Related Work.
- Move detailed claim-boundary discussion into appendix if page-limited.

### APA/report style

- Use author-year citations for external literature.
- Keep evidence IDs in footnotes or appendix.
- Preserve narrative discussion and limitations.

## Recommended Immediate Work Before User Chooses

The following work is useful regardless of target style:

1. Create a compact Results Tables appendix.
2. Create a reproducibility package inventory.
3. Add exact line anchors for method-definition documents.
4. Create a clean arXiv-style citation replacement map from `[S:...]` to BibTeX keys.

## Decision Prompt

Pick one:

- `arXiv working paper`
- `ACM-style conference`
- `IEEE-style conference`
- `APA/report`
- `undecided; continue venue-neutral cleanup`

If undecided, continue venue-neutral cleanup and prepare the compact results tables next.
