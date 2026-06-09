# Citation Conversion Plan

Target document: `research/06_outputs/contract-driven-harness-paper-draft.md`

Current status: internal evidence/source tags are connected and a venue-neutral BibTeX draft exists at `research/06_outputs/contract-driven-harness-references.bib`.

## Current Citation Layers

1. Paper body: internal citation tags, for example `[E:P2-E68]` and `[S:P2-EXT-DSPY]`.
2. Evidence ledger: `research/03_evidence/evidence-ledger.jsonl`.
3. Source index: `research/01_sources/source-index.md`.
4. Citation metadata: `research/01_sources/contract-driven-harness-citation-metadata.md`.
5. BibTeX draft: `research/06_outputs/contract-driven-harness-references.bib`.

## Recommended Default If No Venue Is Selected

Use arXiv-style preprint citations:

- External literature and documentation: BibTeX references from `contract-driven-harness-references.bib`.
- Local experiment artifacts: cite as a reproducibility package, with Appendix C preserving source/evidence traceability.
- Evidence IDs: keep in Appendix C, remove from body only after formal references are inserted.

## Conversion Steps

1. Choose target style: ACM numbered, IEEE numbered, APA author-year, or arXiv preprint.
2. Normalize BibTeX entries:
   - Verify final author order and spelling against the target bibliography source.
   - Add arXiv version numbers.
   - Add DOI fields where available.
   - Preserve `accessed` notes for mutable official docs.
3. Replace body-level `[S:...]` tags with target-style citations.
4. Keep body-level `[E:...]` tags only for internal drafts; for external submission, move evidence IDs into Appendix C or artifact footnotes.
5. Add a reproducibility-package section that explains local artifact paths and evaluation scripts.
6. Rerun citation audit after conversion.

## Known Open Items

| Item | Status | Reason |
|---|---|---|
| Target venue style | Pending | User has not selected conference, journal, or style. |
| Exact author lists for newer arXiv papers | Mostly complete | Placeholder author groups for OAgents, SIC, Agentproof, and LlamaFirewall have been replaced from arXiv metadata; final venue conversion should still verify author spelling/order. |
| Exact local line anchors for all method documents | Partial | Key result artifacts have line hints; whole-document method sources still need line anchors. |
| External docs version pinning | Partial | Access dates recorded; mutable docs still need version/channel notes where available. |

## Decision

Do not claim publication-ready references yet. The current state is suitable for internal review, arXiv-style preprint preparation, and venue-selection discussion.
