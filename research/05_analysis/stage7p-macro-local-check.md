# Stage 7p Macro Local Golden/Bad Evaluation

- Cases: 2
- Expectation failures: 0

| Fixture | Case | Passed | Expectation Met | Task | Chain | Findings |
|---|---|---:|---:|---:|---:|---|
| `stage7p-a10-a9-a6` | `golden` | true | true | 1.000 | 1.000 | None |
| `stage7p-a10-a9-a6` | `uses_stale_and_overwrites` | false | true | 0.500 | 0.000 | context_relevance=0.000 below threshold 1.000; constraint_consistency=0.000 below threshold 1.000; repair_success=0.000 below threshold 1.000; trace_completeness=0.000 below threshold 1.000; stage_completion=0.000 below threshold 1.000; atom_primary_metric=0.000 below threshold 1.000; task_success=0.500 below threshold 0.800 |
