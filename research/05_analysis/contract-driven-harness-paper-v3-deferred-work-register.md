# Contract-Driven Harness Paper v3 Deferred Work Register

Prepared: 2026-06-10

Purpose: preserve important v3 review recommendations that are not part of the v3.1 minimum revision, with explicit triggers so they remain visible and actionable.

## Deferred But Not Dropped

| Item | Why deferred | Trigger to resume | Expected output |
|---|---|---|---|
| Full citation-format standardization | This is a focused publication-preparation pass and should not be mixed into the v3.1 structure/layout revision. | Resume before any arXiv/venue submission package is declared release-ready, or immediately after v3.1 PDF passes compile/layout checks. | Normalized `.bib`, updated local artifact citation title, consistent organization/title/URL/accessed-date formatting for web docs, and citation audit update. |
| Convert ASCII experiment map to a formal figure | The current Markdown-to-LaTeX converter does not support authored figures cleanly; forcing it now would add tooling risk. | Resume when selecting a venue template, adding figure support to the converter, or preparing camera-ready/public arXiv layout. | Figure 1 source artifact plus PDF rendering check; ASCII map either removed or retained only as source comment. |
| Appendix C placement and table redesign | Appendix C remains useful for traceability but stresses page layout and longtable splitting. | Resume during human PDF layout review or if compile warnings/table readability remain unacceptable after v3.1. | Decision memo: keep Appendix C in main PDF, compress it, or move it to supplementary material. |
| Cross-provider, perturbation, stability, and overhead experiments | The v3.1.1 body is frozen; new evidence belongs in a separate v4 track. Small ad hoc runs would not materially change the claim. | The security/systems peer review activated a written staged plan. Execute Stage A locally, then request a go decision before the 30-run paid Stage B gate. | See `research/05_analysis/contract-driven-harness-post-freeze-evidence-extension-plan.md`; outputs include instrumentation, perturbation fixtures, manifests, run reports, intervals, overhead matrix, evidence entries, and a v4 claim decision. |

## V3.1 Minimum Revision Scope

The v3.1 revision may proceed without the deferred items only if it completes:

1. compressed Table 3;
2. metric explanation table;
3. closest-prior-work paragraph;
4. reduced repetition of `targeted smoke runs`;
5. regenerated PDF and compile check.

## Readability Rule

Any future paper revision plan must check this register before declaring the paper release-ready. Deferred work can be closed only by either completing the expected output or writing an explicit decision note explaining why it is no longer needed.

The citation-format work has a concrete execution plan in `research/05_analysis/contract-driven-harness-citation-pass-plan.md`.
