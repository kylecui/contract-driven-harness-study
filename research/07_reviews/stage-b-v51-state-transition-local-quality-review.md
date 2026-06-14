# Stage B v5.1 State-Transition Local Quality Review

Reviewed: 2026-06-14

Overall rating: A for a local contract-repair gate

Blocking issues: none

## Reviewed Artifacts

- `research/05_analysis/stage-b-v51-state-transition-local-experiment-plan.md`
- `research/05_analysis/stage-b-v51-state-transition-local-check.json`
- `research/05_analysis/stage-b-v51-state-transition-regression-check.json`
- `research/05_analysis/stage-b-v51-state-transition-local-result-summary.md`
- `research/04_methods/macro-state-transition-stage-b-v51/`
- Stage B v5.1 builder, evaluator, and unit tests
- Evidence records `P2-E154` through `P2-E156`

## Nine-Dimension Review

| Dimension | Rating | Review |
|---|---|---|
| Question alignment | Pass | The stage tests whether the two diagnosed v5 contract defects can be repaired without weakening exact evidence or state-transition obligations. |
| Evidence completeness | Pass | Golden, known-bad, repair-contract, isolation, unit-test, regression, and deviation records are retained. |
| Citation coverage | Pass | Local facts map to P2-E154, regressions to P2-E155, and the next-gate inference to P2-E156. |
| Logic chain | Pass | The v5 failure audit identifies two defects; v5.1 changes only those surfaces and tests both with targeted known-bads. |
| Counter-evidence | Pass | The original 0/4 v5 result remains explicit and is neither replaced nor rescored. |
| Method fit | Pass | Exact equality is appropriate for immutable bindings, closed state vocabulary, and a fully declared deterministic gate. |
| Actionability | Pass | The next model, harness, fixtures, repetitions, retry boundary, and approval requirement are explicit. |
| Expression quality | Pass | Counts and claim boundaries replace broad reliability or workflow claims. |
| Risk disclosure | Pass | The report states the bundled repair, single-event scope, two variants, and absence of model evidence. |

## Independent Checks

- Recounted two golden and 36 known-bad cases.
- Confirmed all 38 expectations and component vectors pass.
- Confirmed 36/36 known-bads fail the aggregate metric.
- Confirmed 32/36 known-bads remain schema-valid.
- Confirmed the v5 semantic-remap pattern fails only evidence retention.
- Confirmed wrong `next_action` fails only strict gate accuracy.
- Confirmed the static-copy ablation fails residual state, transition, and gate.
- Confirmed zero model-surface and zero repair-contract violations.
- Confirmed nine v5.1 evaluator tests pass.
- Confirmed regressions remain 30/30, 32/32, 22/22, and 110/110.
- Confirmed evidence-ledger JSON is valid and IDs are unique.
- Confirmed no provider call occurred.

## Residual Risks

The repair changes evidence representation and gate disclosure together. A
future model smoke can test the repaired protocol but cannot estimate the
separate causal effect of each change without an ablation.

Exact evidence retention measures compliance with a declared mapping. It does
not establish that the mapping is the only semantically defensible one.

The experiment covers one supplied approval event and two representation
variants. It does not test event selection, conflicting events, rollback,
concurrency, or tool enforcement.

## Decision

Approve Stage B v5.1-local as complete. Approve preparation of a four-run
Qwen3-8B + G9 repair smoke after separate user authorization. Keep the failed
v5 record unchanged and prohibit cross-protocol pooling.
