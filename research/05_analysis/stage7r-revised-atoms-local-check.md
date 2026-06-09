# Mechanism Atom Local Golden/Bad Evaluation

- Cases: 12
- Expectation failures: 0

| Fixture | Case | Passed | Expectation Met | Atom Primary | Findings |
|---|---|---:|---:|---:|---|
| `a2r-unsupported-claim-detection` | `golden` | true | true | 1.000 | None |
| `a2r-unsupported-claim-detection` | `accepts_unsupported_claim` | false | true | 0.000 | citation_grounding=0.000 below threshold 1.000; task_success=0.500 below threshold 0.800 |
| `a3r-constraint-safe-plan` | `golden` | true | true | 1.000 | None |
| `a3r-constraint-safe-plan` | `allows_overwrite_and_secret` | false | true | 0.000 | constraint_consistency=0.000 below threshold 1.000; task_success=0.500 below threshold 0.800 |
| `a4r-strict-state-inventory` | `golden` | true | true | 1.000 | None |
| `a4r-strict-state-inventory` | `invents_ci_and_branch` | false | true | 0.000 | state_accuracy=0.000 below threshold 0.850; task_success=0.500 below threshold 0.800 |
| `a5r-stage-gate-check` | `golden` | true | true | 1.000 | None |
| `a5r-stage-gate-check` | `premature_synthesis` | false | true | 0.000 | stage_completion=0.000 below threshold 1.000; task_success=0.500 below threshold 0.800 |
| `a7r-enumerated-claim-decision` | `golden` | true | true | 1.000 | None |
| `a7r-enumerated-claim-decision` | `selects_universal_claim` | false | true | 0.000 | trace_completeness=0.000 below threshold 1.000; task_success=0.500 below threshold 0.850 |
| `a8r-evidence-type-rules` | `golden` | true | true | 1.000 | None |
| `a8r-evidence-type-rules` | `flattens_all_to_extracted` | false | true | 0.000 | evidence_type_accuracy=0.000 below threshold 1.000; task_success=0.500 below threshold 0.800 |
