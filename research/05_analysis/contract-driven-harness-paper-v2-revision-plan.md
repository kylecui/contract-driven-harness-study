# Contract-Driven Harness Paper Revision Plan v2

Prepared: 2026-06-10

Trigger: external review intake in `research/07_reviews/contract-driven-harness-external-review-intake-2026-06-10.md`.

## Revision Goal

Upgrade the paper from a first arXiv-style working draft into a sharper bounded-agent-reliability paper. The revision should make the central contribution easier to evaluate:

> Contract-driven harness engineering makes some low-cost-model failures on bounded productivity tasks observable, repairable, and regression-testable by externalizing task obligations into explicit contracts.

## Non-Negotiable Claim Boundaries

The paper must not claim:

- low-cost models are generally equivalent to strong models;
- harnessing universally closes model gaps;
- Stage 7e or Stage 7-next proves full workflow reliability;
- project initialization or full research workflow is solved;
- production readiness;
- PEtFiSh-specific results automatically generalize to all agent systems.

## Paper Revision Tasks

| Area | Required change | Status |
|---|---|---|
| Abstract | Center weak-model enablement and repair-loop protocol; demote gap compression to conditional result. | Applied in v2 draft pass |
| Introduction | Add model capability vs harness specification vs workflow composition distinction. | Applied in v2 draft pass |
| Related Work | Add comparison table for orchestration, structured outputs, guardrails, declarative LM programs, agent specs, retrieval/tools, memory, and safety verification. | Applied in v2 draft pass |
| Methods | Add formal atom-to-macro admission criteria. | Applied in v2 draft pass |
| Results | Add compact claim/evidence/boundary summary in the main Results section. | Applied in v2 draft pass |
| Discussion | State that PEtFiSh is the implementation context, not the claim. | Applied in v2 draft pass |
| Artifact package | Update reproducibility package wording for public repository availability. | Applied in v2 draft pass |
| Layout | Recompile PDF and review longtable/appendix warnings after revision. | v3 compiled; v3.1 table/layout pass pending |
| V3.1 minimum revision | Compress Table 3, add metric explanation table, add closest-prior-work paragraph, reduce repeated targeted-smoke wording, and regenerate PDF. | Completed in v3.1 |
| Deferred work register | Preserve citation-format standardization, formal figure conversion, Appendix C placement, and future experiment expansion with explicit resume triggers. | `research/05_analysis/contract-driven-harness-paper-v3-deferred-work-register.md` |

## Next Experiment Queue

Run these only after the v2 paper draft and artifact package are stable:

1. G9 object ablation suite:
   - G0 raw/minimal prompt
   - schema-only
   - evidence-only
   - trace-only
   - gate-only
   - full G9 contract
2. Stage 7e and Stage 7-next perturbation suite:
   - evidence order changes
   - irrelevant evidence injection
   - conflicting evidence insertion
   - missing unknown-state field
   - inducive stale recommendation
   - semantically equivalent field-name variants
   - extra incomplete stage gate
   - equivalent known-state phrasing variants
3. Controlled state-mutating macro:
   - mock file tree
   - restricted write simulator
   - path safety gate
   - rollback trace
   - known-bad cases for unsafe writes, skipped approval, stale context, and state hallucination
4. Cross-provider replication after ablations and perturbations are stable.

## Artifact Publication Gate

Because the repository is public, every release-oriented revision must pass:

- credential scan;
- large-file scan;
- artifact locator check;
- PDF compile check;
- source package check;
- claim-boundary check;
- public/private wording check.
