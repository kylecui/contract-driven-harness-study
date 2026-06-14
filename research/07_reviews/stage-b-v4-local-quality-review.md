# Stage B v4 Local Quality Review

Reviewed: 2026-06-14

Scope:

- `research/05_analysis/stage-b-v4-local-experiment-plan.md`
- `research/05_analysis/stage-b-v4-local-result-summary.md`
- `research/05_analysis/stage-b-v4-local-check.json`
- `research/04_methods/mechanism-atoms-stage-b-v4/`
- `research/04_methods/scripts/evaluate_stage_b_v4_atoms.py`

Overall rating: A for a local mechanism-definition gate

Blocking issues: none

## Nine-Dimension Review

| Dimension | Rating | Review |
|---|---|---|
| Question alignment | Pass | Both preregistered local RQs are answered directly. |
| Evidence completeness | Pass | Counts are traceable to the retained JSON report and generated fixtures. |
| Citation coverage | Pass | Internal claims are linked through P2-E136 to P2-E138; no external factual claim is introduced. |
| Logic chain | Pass | v3 failure audit leads to two atoms, local gate, then a bounded smoke admission decision. |
| Counter-evidence | Pass | The summary states that local success is not model evidence and records schema-valid known-bad cases. |
| Method fit | Pass | Exact equality is appropriate because the tested obligation is immutability, not semantic equivalence. |
| Actionability | Pass | The next gate specifies model, harness, fixtures, repetitions, call count, pass rule, and retry boundary. |
| Expression quality | Pass | Claims are concrete and avoid unsupported robustness or readiness language. |
| Risk disclosure | Pass | Synthetic-task, copying, evaluator-completeness, and transfer limitations are recorded. |

## Independent Checks

- Recounted four golden and 28 known-bad cases from the retained result.
- Confirmed 24 known-bads are schema-valid but fail the primary metric.
- Confirmed four schema-changing known-bads fail both metrics.
- Confirmed the model-surface scan reports zero violations.
- Confirmed the historical v3 regression reports 110 cases and zero failures.
- Confirmed no provider execution artifact was created for this stage.

## Residual Risks

The atoms are synthetic and intentionally small. A model can pass by exact
copying, which is acceptable for an immutability mechanism but does not test
reasoning. The later smoke must therefore be treated as a preservation test,
and later macro recomposition is still required to test transfer under
attention pressure.

Known-bad coverage is finite. The current gate supports detection of the
declared failure classes, not proof that every malformed output will be
rejected.

## Decision

Approve Stage B v4-local as complete. Approve preparation of the eight-run
Stage B v4-smoke. Do not update the frozen paper or claim model robustness from
this local result.
