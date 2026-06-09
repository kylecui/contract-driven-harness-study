# Stage 7e Evidence-Bound Decision Macro Smoke Summary

Date: 2026-06-08

## Scope

Stage 7e tested the narrow macro admitted by the Stage 7r.2 composition gate.

Composition chain:

1. A4R strict state inventory
2. A2R1 claim-level evidence binding
3. A8R evidence-type rules
4. A7R1 rejection trace completeness
5. A5R stage-gate check

This was a fixed-input, no-tool-execution, deterministic JSON macro. It does not test full project initialization, full research workflow execution, source discovery, filesystem mutation, or open-ended synthesis.

## Local Gates

Local gates passed before model execution:

- Fixture: `research/04_methods/macro-tasks/stage7e-evidence-bound-decision/`
- Evaluator: `research/04_methods/scripts/evaluate_stage7e_macro_artifacts.py`
- Golden/bad regression: 2/2 expectations met
- Bad case `uses_stale_full_claims` remained blocked after evaluator normalization
- Packet dry-run: 6/6 packets compiled
- Preflight: PASS, 0 errors, 0 warnings

After the first real-output evaluation, the evaluator was corrected for construct validity:

- Accepted `typed_evidence` as either bucketed object keys (`EXTRACTED`) or list items with `type`.
- Accepted `Stage 7e` and `stage7e` spacing variants.
- Accepted short evidence references such as `e05` in decision trace when unambiguous.
- Accepted `active` and `fulfilled` as carried-obligation preservation statuses.

The correction did not relax overclaim detection: the known-bad stale/full-claim output still failed with task_success=0.000 and atom_primary_metric=0.000.

## Real Smoke Execution

Matrix:

- models: `strong_model`, `budget_model`
- SiliconFlow models: `deepseek-ai/DeepSeek-V3.2`, `Qwen/Qwen3-8B`
- arms: G0, G8, G9
- repetitions: 1
- planned runs: 6

Execution completed 6/6 runs. No provider error or timeout occurred.

Adapter event log:

- `research/05_analysis/stage7e-evidence-bound-decision-adapter-events.jsonl`

Final evaluated artifacts:

- `research/05_analysis/stage7e-evidence-bound-decision-evaluation-v3.md`
- `research/05_analysis/stage7e-evidence-bound-decision-evaluation-runs-v3.json`

## Results

| Model tier | Arm | Completed | Passed | Task success | Primary metric | Main failure if any |
|---|---|---:|---:|---:|---:|---|
| strong_model | G0 | 1 | 0 | 0.063 | 0.000 | Unconstrained output used wrong schema and missed core contract sections. |
| strong_model | G8 | 1 | 1 | 1.000 | 1.000 | None. |
| strong_model | G9 | 1 | 1 | 1.000 | 1.000 | None. |
| budget_model | G0 | 1 | 0 | 0.016 | 0.000 | Unconstrained output did not satisfy the macro contract. |
| budget_model | G8 | 1 | 1 | 1.000 | 1.000 | None. |
| budget_model | G9 | 1 | 0 | 0.714 | 0.000 | Missed complete stage gate and decision-trace coverage. |

## Interpretation

Stage 7e supports a narrow but important composition claim:

- Under G8, both the strong model and the low-cost model completed the evidence-bound decision macro with full task_success and atom_primary_metric.
- Both G0 baselines failed, including the strong model, which shows that the macro contract mattered more than raw model strength for this fixed-input task.
- The low-cost model G9 run partially failed despite correct schema, grounding, evidence typing, and state inventory. Its remaining failure was composition-level retention: the output did not preserve enough stage-gate and trace obligations in the expected places.

This supports mechanism-bound weak-model enablement for a fixed evidence-decision packet. It does not support a claim that G9 is strictly better than G8, that the harness universally closes model gaps, or that full research/project workflows are solved.

## Deviation Review

The first evaluation under-scored semantically valid outputs because the evaluator expected overly narrow field shapes and exact tokenization. This was a construct-validity deviation, not a model-quality failure.

The correction was reasonable because:

- It accepted equivalent JSON representations already allowed by the output contract.
- It preserved the known-bad stale/full-claim rejection.
- It did not change the model outputs.
- It still left the low-cost G9 run failed for real missing obligations.

## Gate Decision

Stage 7e passes as a narrow composed macro smoke for G8 and strong-model G9.

Stage 7e does not yet justify full open-ended macro composition.

Next recommended work:

1. Add a Stage 7e v2 retention check targeting the low-cost G9 missing stage-gate and trace obligations.
2. If Stage 7e v2 passes, update the claim-boundary memo and paper outline around fixed-input evidence-decision workflows.
3. Continue blocking full project initialization and full research workflow until a separate macro is built with explicit cross-step obligation retention and deterministic evaluation.
