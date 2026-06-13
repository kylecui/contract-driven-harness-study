# Evidence-Bound Macro Local Golden/Bad Evaluation

- Cases: 28
- Expectation failures: 0

| Fixture | Case | Passed | Expectation Met | Task | Primary | Findings |
|---|---|---:|---:|---:|---:|---|
| `stage7-next-method-plan-update--canonical` | `golden` | true | true | 1.000 | 1.000 | None |
| `stage7-next-method-plan-update--canonical` | `missing_required_known_state_evidence` | false | true | 0.857 | 0.000 | state_accuracy=0.000 below threshold 1.000; atom_primary_metric=0.000 below threshold 1.000 |
| `stage7-next-method-plan-update--canonical` | `undeclared_source_references` | false | true | 0.571 | 0.000 | state_accuracy=0.000 below threshold 1.000; citation_grounding=0.000 below threshold 1.000; trace_completeness=0.000 below threshold 1.000; atom_primary_metric=0.000 below threshold 1.000; task_success=0.571 below threshold 0.850 |
| `stage7-next-method-plan-update--distractor-evidence` | `golden` | true | true | 1.000 | 1.000 | None |
| `stage7-next-method-plan-update--distractor-evidence` | `distractor_mixed_with_valid_support` | false | true | 0.714 | 0.000 | citation_grounding=0.000 below threshold 1.000; trace_completeness=0.000 below threshold 1.000; atom_primary_metric=0.000 below threshold 1.000; task_success=0.714 below threshold 0.850 |
| `stage7-next-method-plan-update--distractor-evidence` | `distractor_used_as_primary_support` | false | true | 0.714 | 0.000 | citation_grounding=0.000 below threshold 1.000; trace_completeness=0.000 below threshold 1.000; atom_primary_metric=0.000 below threshold 1.000; task_success=0.714 below threshold 0.850 |
| `stage7-next-method-plan-update--evidence-order-shuffled` | `golden` | true | true | 1.000 | 1.000 | None |
| `stage7-next-method-plan-update--evidence-order-shuffled` | `missing_grounded_claim_evidence` | false | true | 0.857 | 0.000 | citation_grounding=0.000 below threshold 1.000; atom_primary_metric=0.000 below threshold 1.000 |
| `stage7-next-method-plan-update--field-alias` | `golden` | true | true | 1.000 | 1.000 | None |
| `stage7-next-method-plan-update--field-alias` | `canonical_field_fallback` | false | true | 0.857 | 0.000 | schema_validity=0.000 below threshold 1.000; atom_primary_metric=0.000 below threshold 1.000 |
| `stage7-next-method-plan-update--field-alias` | `missing_aliased_claim_evidence` | false | true | 0.857 | 0.000 | citation_grounding=0.000 below threshold 1.000; atom_primary_metric=0.000 below threshold 1.000 |
| `stage7-next-method-plan-update--unknown-state-paraphrase` | `golden` | true | true | 1.000 | 1.000 | None |
| `stage7-next-method-plan-update--unknown-state-paraphrase` | `canonical_unknown_state_fallback` | false | true | 0.857 | 0.000 | schema_validity=0.000 below threshold 1.000; atom_primary_metric=0.000 below threshold 1.000 |
| `stage7-next-method-plan-update--unknown-state-paraphrase` | `missing_paraphrased_unknown_state` | false | true | 0.714 | 0.000 | schema_validity=0.000 below threshold 1.000; state_accuracy=0.000 below threshold 1.000; atom_primary_metric=0.000 below threshold 1.000; task_success=0.714 below threshold 0.850 |
| `stage7e-v4-known-state-provenance-decision--canonical` | `golden` | true | true | 1.000 | 1.000 | None |
| `stage7e-v4-known-state-provenance-decision--canonical` | `missing_required_known_state_evidence` | false | true | 0.857 | 0.000 | state_accuracy=0.000 below threshold 1.000; atom_primary_metric=0.000 below threshold 1.000 |
| `stage7e-v4-known-state-provenance-decision--canonical` | `undeclared_source_references` | false | true | 0.571 | 0.000 | state_accuracy=0.000 below threshold 1.000; citation_grounding=0.000 below threshold 1.000; trace_completeness=0.000 below threshold 1.000; atom_primary_metric=0.000 below threshold 1.000; task_success=0.571 below threshold 0.850 |
| `stage7e-v4-known-state-provenance-decision--distractor-evidence` | `golden` | true | true | 1.000 | 1.000 | None |
| `stage7e-v4-known-state-provenance-decision--distractor-evidence` | `distractor_mixed_with_valid_support` | false | true | 0.714 | 0.000 | citation_grounding=0.000 below threshold 1.000; trace_completeness=0.000 below threshold 1.000; atom_primary_metric=0.000 below threshold 1.000; task_success=0.714 below threshold 0.850 |
| `stage7e-v4-known-state-provenance-decision--distractor-evidence` | `distractor_used_as_primary_support` | false | true | 0.714 | 0.000 | citation_grounding=0.000 below threshold 1.000; trace_completeness=0.000 below threshold 1.000; atom_primary_metric=0.000 below threshold 1.000; task_success=0.714 below threshold 0.850 |
| `stage7e-v4-known-state-provenance-decision--evidence-order-shuffled` | `golden` | true | true | 1.000 | 1.000 | None |
| `stage7e-v4-known-state-provenance-decision--evidence-order-shuffled` | `missing_grounded_claim_evidence` | false | true | 0.857 | 0.000 | citation_grounding=0.000 below threshold 1.000; atom_primary_metric=0.000 below threshold 1.000 |
| `stage7e-v4-known-state-provenance-decision--field-alias` | `golden` | true | true | 1.000 | 1.000 | None |
| `stage7e-v4-known-state-provenance-decision--field-alias` | `canonical_field_fallback` | false | true | 0.857 | 0.000 | schema_validity=0.000 below threshold 1.000; atom_primary_metric=0.000 below threshold 1.000 |
| `stage7e-v4-known-state-provenance-decision--field-alias` | `missing_aliased_claim_evidence` | false | true | 0.857 | 0.000 | citation_grounding=0.000 below threshold 1.000; atom_primary_metric=0.000 below threshold 1.000 |
| `stage7e-v4-known-state-provenance-decision--unknown-state-paraphrase` | `golden` | true | true | 1.000 | 1.000 | None |
| `stage7e-v4-known-state-provenance-decision--unknown-state-paraphrase` | `canonical_unknown_state_fallback` | false | true | 0.857 | 0.000 | schema_validity=0.000 below threshold 1.000; atom_primary_metric=0.000 below threshold 1.000 |
| `stage7e-v4-known-state-provenance-decision--unknown-state-paraphrase` | `missing_paraphrased_unknown_state` | false | true | 0.714 | 0.000 | schema_validity=0.000 below threshold 1.000; state_accuracy=0.000 below threshold 1.000; atom_primary_metric=0.000 below threshold 1.000; task_success=0.714 below threshold 0.850 |
