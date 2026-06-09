# Mechanism Atom Local Golden/Bad Evaluation

- Cases: 4
- Expectation failures: 0

| Fixture | Case | Passed | Expectation Met | Atom Primary | Findings |
|---|---|---:|---:|---:|---|
| `a2r1-claim-level-evidence-binding` | `golden` | true | true | 1.000 | None |
| `a2r1-claim-level-evidence-binding` | `global_evidence_only` | false | true | 0.000 | citation_grounding=0.000 below threshold 1.000; task_success=0.500 below threshold 0.800 |
| `a7r1-rejection-trace-completeness` | `golden` | true | true | 1.000 | None |
| `a7r1-rejection-trace-completeness` | `missing_c3_trace` | false | true | 0.000 | trace_completeness=0.000 below threshold 1.000; task_success=0.500 below threshold 0.850 |
