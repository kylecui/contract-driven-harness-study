# Stage 7p Macro Local Golden/Bad Evaluation

- Cases: 3
- Expectation failures: 0

| Fixture | Case | Passed | Expectation Met | Task | Chain | Findings |
|---|---|---:|---:|---:|---:|---|
| `stage7p-v2-a10-a9-a6` | `golden` | true | true | 1.000 | 1.000 | None |
| `stage7p-v2-a10-a9-a6` | `claims_full_composition` | false | true | 0.917 | 0.000 | stage_completion=0.000 below threshold 1.000; atom_primary_metric=0.000 below threshold 1.000 |
| `stage7p-v2-a10-a9-a6` | `missing_obligation_retention` | false | true | 0.750 | 0.000 | schema_validity=0.833 below threshold 1.000; context_relevance=0.000 below threshold 1.000; atom_primary_metric=0.000 below threshold 1.000; task_success=0.750 below threshold 0.800; state_accuracy=0.000 below threshold 1.000 |
