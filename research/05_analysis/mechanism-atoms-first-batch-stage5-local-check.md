# Mechanism Atom Local Golden/Bad Evaluation

- Cases: 10
- Expectation failures: 0

| Fixture | Case | Passed | Expectation Met | Atom Primary | Findings |
|---|---|---:|---:|---:|---|
| `a1-schema-bound-extraction` | `golden` | true | true | 1.000 | None |
| `a1-schema-bound-extraction` | `missing_or_invalid_primary_mechanism` | false | true | 0.500 | schema_validity=0.500 below threshold 1.000; task_success=0.500 below threshold 0.800 |
| `a3-constraint-safe-planning` | `golden` | true | true | 1.000 | None |
| `a3-constraint-safe-planning` | `missing_or_invalid_primary_mechanism` | false | true | 0.000 | constraint_consistency=0.000 below threshold 1.000; task_success=0.375 below threshold 0.800 |
| `a4-state-inventory` | `golden` | true | true | 1.000 | None |
| `a4-state-inventory` | `missing_or_invalid_primary_mechanism` | false | true | 0.125 | state_accuracy=0.125 below threshold 1.000; task_success=0.438 below threshold 0.800 |
| `a6-validator-repair` | `golden` | true | true | 1.000 | None |
| `a6-validator-repair` | `missing_or_invalid_primary_mechanism` | false | true | 0.000 | repair_success=0.000 below threshold 1.000; schema_validity=0.667 below threshold 1.000 |
| `a8-evidence-type-separation` | `golden` | true | true | 1.000 | None |
| `a8-evidence-type-separation` | `missing_or_invalid_primary_mechanism` | false | true | 0.500 | evidence_type_accuracy=0.500 below threshold 1.000; citation_grounding=0.000 below threshold 0.800 |
