# Evidence-Bound Macro Local Golden/Bad Evaluation

- Cases: 4
- Expectation failures: 0

| Fixture | Case | Passed | Expectation Met | Task | Primary | Findings |
|---|---|---:|---:|---:|---:|---|
| `stage7-next-method-plan-update` | `golden` | true | true | 1.000 | 1.000 | None |
| `stage7-next-method-plan-update` | `premature_broader_workflow_expansion` | false | true | 0.000 | 0.000 | selected_claim overclaims beyond admitted narrow macro scope; state_accuracy=0.000 below threshold 1.000; citation_grounding=0.000 below threshold 1.000; evidence_type_accuracy=0.000 below threshold 1.000; trace_completeness=0.000 below threshold 1.000; stage_completion=0.000 below threshold 1.000; context_relevance=0.000 below threshold 1.000; atom_primary_metric=0.000 below threshold 1.000; task_success=0.000 below threshold 0.850 |
| `stage7e-v4-known-state-provenance-decision` | `golden` | true | true | 1.000 | 1.000 | None |
| `stage7e-v4-known-state-provenance-decision` | `compressed_known_state_provenance` | false | true | 0.857 | 0.000 | state_accuracy=0.000 below threshold 1.000; atom_primary_metric=0.000 below threshold 1.000 |
