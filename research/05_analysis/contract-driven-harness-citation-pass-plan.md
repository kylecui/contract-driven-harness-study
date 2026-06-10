# Contract-Driven Harness Citation Pass Plan

Prepared: 2026-06-10

Purpose: convert the current working-draft bibliography into a release-oriented citation package before any arXiv or venue submission is declared ready.

## Scope

This pass is intentionally separate from the v3.1 layout patch. It should update citation metadata and bibliography consistency without changing empirical claims or paper results.

## Required Changes

| Area | Required action | Output |
|---|---|---|
| Paper/preprint references | Ensure every paper entry has complete title, authors, year, arXiv ID or venue/preprint status, and stable URL or DOI when available. | Updated `research/06_outputs/contract-driven-harness-references.bib` |
| Documentation references | Normalize web documentation entries as organization, title, URL, and accessed date. | Updated `.bib` plus citation metadata notes |
| Local artifact citation | Rename the local artifact citation from an internal title such as "Local experiment artifacts" to a public "Reproducibility package" citation with the GitHub repository URL. | Updated BibTeX key/body and paper reference wording if needed |
| Version notes | Move volatile statements such as "v4 as of..." or preprint-version notes into BibTeX `note` fields. | Stable title/year fields with version details in notes |
| Key stability | Verify that all `\cite{...}` keys in the generated LaTeX resolve and that no unused or missing BibTeX entries remain. | Citation audit result |

## Acceptance Criteria

The citation pass is complete only when:

1. all BibTeX entries have a normalized author or organization field;
2. all external web documentation entries include accessed dates;
3. all paper/preprint entries include title, year, and venue/arXiv/preprint status;
4. the local artifact bundle is cited as a public reproducibility package;
5. a structural citation check reports zero missing keys and zero unused keys;
6. the paper compiles with zero undefined citations and zero BibTeX warnings.

## Trigger

Run this pass after the v3.1 layout patch and before any release-ready arXiv or venue package.
