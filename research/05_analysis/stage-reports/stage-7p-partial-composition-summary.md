# Stage 7p Summary: Partial Macro Composition A10 -> A9 -> A6

## Stage Objective

Test whether the passing mechanism atoms can compose into a narrow macro task:

```text
A10 bounded context recall -> A9 no-overwrite action planning -> A6 validator repair
```

This is a partial-composition test only. It is not a full project-initialization or full research-workflow validation.

## Result

Stage 7p execution completed.

Operational result:

- Local golden/bad macro evaluator check: PASS.
- Planned real runs: 6.
- Completed real SiliconFlow runs: 6/6.
- Collection warnings: 0.
- Metrics computed: yes.

Empirical result:

- Strong model passes the full partial-composition chain under G8 and G9.
- Budget model improves strongly under G8/G9 but does not pass the full chain.
- G0 fails for both model tiers.

## Matrix

```text
2 models x 1 macro task x 3 arms x 1 repetition = 6 runs
```

Models:

- `strong_model`: `deepseek-ai/DeepSeek-V3.2`
- `budget_model`: `Qwen/Qwen3-8B`

Arms:

- G0
- G8
- G9

## Evaluation Summary

| Model | Arm | Task | Schema | Context | Safety | Repair | Chain | Passed |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| strong_model | G0 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | false |
| strong_model | G8 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | true |
| strong_model | G9 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | true |
| budget_model | G0 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | false |
| budget_model | G8 | 0.800 | 1.000 | 0.000 | 1.000 | 0.000 | 0.000 | false |
| budget_model | G9 | 0.900 | 1.000 | 0.000 | 1.000 | 1.000 | 0.000 | false |

## Main Findings

### F1: Composition works for the strong model under harness arms

Both strong_model G8 and strong_model G9 complete the entire partial macro chain.

This supports a bounded composition claim:

> Passing atoms can compose into a narrow macro task under contract-rich harnessing for the strong model.

### F2: Budget model receives strong lift but does not complete the whole chain

Budget model G8/G9 reaches valid schema and strong task_success:

- G8 task_success weak lift: +0.800.
- G9 task_success weak lift: +0.900.
- G8/G9 schema_validity weak lift: +1.000.
- G8/G9 safety and constraint weak lift: +1.000.

But the chain gate remains false because the budget model fails to explicitly carry the bounded-context exclusion:

- G8 context_relevance: 0.000.
- G9 context_relevance: 0.000.

This means weak-model enablement is strong but not complete at the composed-workflow level.

### F3: Atomic success does not automatically imply weak-model composition success

A10, A9, and A6 each passed as atoms for the budget model under G8/G9, but the composed macro fails for the budget model because one atomic obligation disappears during composition: explicit stale-context exclusion.

This is an important methodological result:

> Composition introduces cross-step retention requirements that are not fully tested by isolated atoms.

## Deviation Judgment

This is not a failure of Stage 7p execution.

It is a meaningful negative/partial result:

- The partial macro task executed cleanly.
- The evaluator exposed a real composition fragility.
- The result strengthens the argument for testing atoms before broad workflows, and then testing selected atom compositions before claiming full workflow validity.

## Claim Boundary

Can claim:

- Strong model + G8/G9 can compose A10 -> A9 -> A6 successfully.
- Budget model + G8/G9 shows large absolute gains over G0 on schema, safety, repair, and task_success.
- Isolated atom success is insufficient to guarantee composed weak-model success.

Cannot claim:

- Budget model fully passes the partial macro composition.
- Full project initialization is validated.
- Full research workflow is validated.
- Passing atoms always compose without additional cross-step memory/trace constraints.

## Next Step

Do not expand to full Stage 7 yet.

Proceed to Stage 7r:

- Redesign A2, A3, A5, and A7.
- Strengthen A4 and A8.
- Add an explicit composition-retention rule learned from Stage 7p: obligations from earlier atoms, such as `excluded_context`, must be preserved into the macro output.

## Artifacts

- Macro fixture: `research/04_methods/macro-tasks/stage7p-a10-a9-a6/`
- Macro evaluator: `research/04_methods/scripts/evaluate_stage7p_macro_artifacts.py`
- Local regression: `research/05_analysis/stage7p-macro-local-check.md`
- Run manifest: `research/05_analysis/real-run-artifacts/stage7p-a10-a9-a6-manifest-with-prompts.json`
- Adapter report: `research/05_analysis/stage7p-a10-a9-a6-adapter.json`
- Evaluation: `research/05_analysis/stage7p-a10-a9-a6-evaluation.md`
- Metrics: `research/05_analysis/stage7p-a10-a9-a6-metrics.md`
