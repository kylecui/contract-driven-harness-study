# Mechanism Atom Local Golden/Bad Evaluation

- Cases: 6
- Expectation failures: 0

| Fixture | Case | Passed | Expectation Met | Atom Primary | Findings |
|---|---|---:|---:|---:|---|
| `a10-bounded-context-recall` | `golden` | true | true | 1.000 | None |
| `a10-bounded-context-recall` | `missing_or_invalid_primary_mechanism` | false | true | 0.000 | context_relevance=0.000 below threshold 1.000; task_success=0.500 below threshold 0.800 |
| `a5-stage-gated-synthesis` | `golden` | true | true | 1.000 | None |
| `a5-stage-gated-synthesis` | `missing_or_invalid_primary_mechanism` | false | true | 0.225 | stage_completion=0.225 below threshold 1.000; task_success=0.000 below threshold 0.800 |
| `a7-traceable-decision` | `golden` | true | true | 1.000 | None |
| `a7-traceable-decision` | `missing_or_invalid_primary_mechanism` | false | true | 0.000 | trace_completeness=0.000 below threshold 1.000; task_success=0.000 below threshold 0.800 |
