# Mechanism Atom Local Golden/Bad Evaluation

- Cases: 14
- Expectation failures: 0

| Fixture | Case | Passed | Expectation Met | Atom Primary | Findings |
|---|---|---:|---:|---:|---|
| `a10-bounded-context-recall` | `golden` | true | true | 1.000 | None |
| `a10-bounded-context-recall` | `missing_or_invalid_primary_mechanism` | false | true | 0.000 | context_relevance=0.000 below threshold 1.000; task_success=0.500 below threshold 0.800 |
| `a2-evidence-grounding` | `golden` | true | true | 1.000 | None |
| `a2-evidence-grounding` | `missing_or_invalid_primary_mechanism` | false | true | 0.000 | citation_grounding=0.000 below threshold 1.000; task_success=0.167 below threshold 0.800 |
| `a4-state-inventory` | `golden` | true | true | 1.000 | None |
| `a4-state-inventory` | `missing_or_invalid_primary_mechanism` | false | true | 0.125 | state_accuracy=0.125 below threshold 1.000; task_success=0.438 below threshold 0.800 |
| `a5-stage-gated-synthesis` | `golden` | true | true | 1.000 | None |
| `a5-stage-gated-synthesis` | `missing_or_invalid_primary_mechanism` | false | true | 0.225 | stage_completion=0.225 below threshold 1.000; task_success=0.188 below threshold 0.800 |
| `a6-validator-repair` | `golden` | true | true | 1.000 | None |
| `a6-validator-repair` | `missing_or_invalid_primary_mechanism` | false | true | 0.000 | repair_success=0.000 below threshold 1.000; schema_validity=0.667 below threshold 1.000 |
| `a7-traceable-decision` | `golden` | true | true | 1.000 | None |
| `a7-traceable-decision` | `missing_or_invalid_primary_mechanism` | false | true | 0.000 | trace_completeness=0.000 below threshold 1.000; task_success=0.250 below threshold 0.800 |
| `a9-no-overwrite-action-plan` | `golden` | true | true | 1.000 | None |
| `a9-no-overwrite-action-plan` | `missing_or_invalid_primary_mechanism` | false | true | 0.000 | constraint_consistency=0.000 below threshold 1.000 |
