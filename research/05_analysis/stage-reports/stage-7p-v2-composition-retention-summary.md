# Stage 7p v2 Summary: Composition-Retention Ablation

## Stage Objective

Test whether the Stage 7p v1 weak-model composition failure was caused by missing cross-step obligation retention.

Stage 7p v2 keeps the same partial macro chain:

```text
A10 bounded context recall -> A9 no-overwrite action planning -> A6 validator repair
```

The only intended mechanism change is adding an explicit composition-retention contract:

- `bounded_context.excluded_context` must explicitly preserve the old-plan exclusion.
- `carried_obligations` must include the A10 obligation to exclude the old broad-workflow plan and mark it preserved.

## Result

Stage 7p v2 execution completed and passed the intended ablation.

Operational result:

- Local golden/bad macro evaluator check: PASS.
- Planned real runs: 6.
- Completed real SiliconFlow runs: 6/6.
- Collection warnings: 0.
- Metrics computed: yes.

Empirical result:

- Strong model passes the full v2 partial-composition chain under G8 and G9.
- Weak/low-cost model passes the full v2 partial-composition chain under G8 and G9.
- G0 fails for both model tiers.

## Evaluation Summary

| Model tier | Arm | Task | Schema | Context | Safety | Repair | Chain | Passed |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| strong_model | G0 | 0.167 | 0.333 | 0.000 | 0.000 | 0.000 | 0.000 | false |
| strong_model | G8 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | true |
| strong_model | G9 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | true |
| weak/low-cost model | G0 | 0.333 | 0.500 | 0.000 | 0.000 | 0.000 | 0.000 | false |
| weak/low-cost model | G8 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | true |
| weak/low-cost model | G9 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | true |

## Key Metrics

For the weak/low-cost model:

- G8 task_success lift: +0.667.
- G9 task_success lift: +0.667.
- G8/G9 schema_validity lift: +0.500.
- G8/G9 context_relevance lift: +1.000.
- G8/G9 safety and constraint lift: +1.000.
- G8/G9 repair_success lift: +1.000.
- G8/G9 atom_primary_metric lift: +1.000.

Gap compression on metrics with nonzero G0 baseline gaps:

- G8 task_success compression: 1.000.
- G9 task_success compression: 1.000.
- G8 schema_validity compression: 1.000.
- G9 schema_validity compression: 1.000.

## Interpretation

Stage 7p v1 showed that isolated atom success did not automatically compose for the weak/low-cost model. The missing piece was not that the input context lacked the A10 exclusion. The v1 prompt did include it. The failure was that the exclusion obligation was not explicitly retained across the composed output.

Stage 7p v2 shows that when the macro contract adds explicit carried obligations, the weak/low-cost model preserves the A10 exclusion and passes the full A10 -> A9 -> A6 partial macro chain.

This supports a new mechanism-level claim:

> Cross-step obligation retention is a necessary composition-layer harness mechanism for preserving negative context constraints across multi-atom workflows.

## Claim Boundary

Can claim:

- Composition-retention scaffolding repaired the weak/low-cost model's Stage 7p v1 composition failure on this narrow macro task.
- Passing atoms can compose for both model tiers under G8/G9 when the macro contract includes explicit carried obligations.
- The failure mode in v1 was not missing input context, but missing enforced preservation of a negative obligation across steps.

Cannot claim:

- Full project initialization is validated.
- Full research workflow is validated.
- Composition-retention alone solves A2/A3/A5/A7.
- The effect is statistically stable beyond this one-repetition ablation.

## Methodological Consequence

Future atom and macro contracts should distinguish:

- local atom output,
- obligations exported by the atom,
- obligations that must be carried into later steps,
- final output fields proving preservation.

This should inform Stage 7r redesign:

- A2/A3/A5/A7 redesign should include exported obligations where applicable.
- A4/A8 strengthening should define which memory/evidence obligations must persist in downstream composition.

## Artifacts

- V2 macro fixture: `research/04_methods/macro-tasks/stage7p-v2-a10-a9-a6/`
- Macro evaluator: `research/04_methods/scripts/evaluate_stage7p_macro_artifacts.py`
- Local regression: `research/05_analysis/stage7p-v2-macro-local-check.md`
- Run manifest: `research/05_analysis/real-run-artifacts/stage7p-v2-a10-a9-a6-manifest-with-prompts.json`
- Adapter report: `research/05_analysis/stage7p-v2-a10-a9-a6-adapter.json`
- Evaluation: `research/05_analysis/stage7p-v2-a10-a9-a6-evaluation.md`
- Metrics: `research/05_analysis/stage7p-v2-a10-a9-a6-metrics.md`
