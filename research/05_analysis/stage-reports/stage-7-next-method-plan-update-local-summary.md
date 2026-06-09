# Stage 7-next Method-Plan Update Local Summary

## Scope

Stage 7-next introduces a bounded evidence-bound method-plan update macro.

This is not a full project initialization task and not a full research workflow. It is a fixed-input, no-tool, deterministic JSON macro that decides the next admitted macro while preserving Stage 7e v4 obligations.

## Fixture

- Fixture directory: `research/04_methods/macro-tasks/stage7-next-method-plan-update/`
- Evaluator: `research/04_methods/scripts/evaluate_stage7e_macro_artifacts.py`
- Local report: `research/05_analysis/stage7-next-method-plan-update-local-check.md`
- Local JSON: `research/05_analysis/stage7-next-method-plan-update-local-check.json`

## Contract Additions

The new macro reuses Stage 7e v4 obligations:

- known-state provenance,
- unknown-state retention,
- forbidden inference retention,
- evidence typing,
- claim-level grounding,
- structured decision trace,
- stage gate,
- carried negative obligations.

It adds one new stressor:

- `method_plan_update`, requiring the selected next macro, admission criteria, local gates, real-model gate, and non-claims.

## Evaluator Generalization

The Stage 7e macro evaluator was generalized so fixture-specific evidence IDs are declared in `output_contract.json` instead of being hard-coded.

Generalized rules now cover:

- evidence type requirements,
- unsupported-claim evidence requirements,
- stage-gate blocked outputs,
- macro ID reporting.

Stage 7e v4 regression still passed after evaluator generalization.

## Local Result

| Case | Expected | Actual | Result |
|---|---:|---:|---|
| `golden` | pass | pass | met |
| `premature_broader_workflow_expansion` | fail | fail | met |

Summary:

- Cases: 2
- Expectation failures: 0
- Golden task_success: 1.000
- Golden atom_primary_metric: 1.000
- Known-bad task_success: 0.000
- Known-bad atom_primary_metric: 0.000

## Interpretation

Stage 7-next local gates pass for the bounded method-plan update macro.

This supports only the local fixture/evaluator readiness claim. It does not yet provide real-model evidence that low-cost models can complete the new macro.

## Decision

Proceeding to a targeted real-model smoke is admissible if API execution is approved.

Recommended smoke:

- low-cost model only,
- G8 and G9,
- two repetitions each,
- event logging enabled,
- stop and review on any systematic contract miss or repeated provider timeout.

Full project initialization and full research workflow remain blocked.
