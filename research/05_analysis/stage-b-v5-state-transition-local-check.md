# Stage B v5 Controlled State-Transition Local Evaluation

- Fixtures: 2
- Cases: 30
- Expectation failures: 0
- Model-surface isolation violations: 0

| Fixture | Case | Schema | Evidence | Residual state | Transition | Gate | Attestation | Aggregate | Expected metrics |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `stage-b-v5-state-transition--canonical` | `golden` | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | true |
| `stage-b-v5-state-transition--canonical` | `evidence_and_transition_corruption` | 1.000 | 0.000 | 1.000 | 0.000 | 1.000 | 1.000 | 0.000 | true |
| `stage-b-v5-state-transition--canonical` | `evidence_array_reordered` | 1.000 | 0.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | true |
| `stage-b-v5-state-transition--canonical` | `evidence_substitution` | 1.000 | 0.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | true |
| `stage-b-v5-state-transition--canonical` | `incomplete_gate_support` | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 1.000 | 0.000 | true |
| `stage-b-v5-state-transition--canonical` | `incomplete_retention_attestation` | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.000 | true |
| `stage-b-v5-state-transition--canonical` | `residual_forbidden_prefix_substitution` | 1.000 | 1.000 | 0.000 | 1.000 | 1.000 | 1.000 | 0.000 | true |
| `stage-b-v5-state-transition--canonical` | `residual_unknown_reordered` | 1.000 | 1.000 | 0.000 | 1.000 | 1.000 | 1.000 | 0.000 | true |
| `stage-b-v5-state-transition--canonical` | `stale_blocked_gate` | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 1.000 | 0.000 | true |
| `stage-b-v5-state-transition--canonical` | `static_pretransition_copy` | 1.000 | 1.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 | true |
| `stage-b-v5-state-transition--canonical` | `transition_record_omitted` | 0.000 | 1.000 | 1.000 | 0.000 | 1.000 | 1.000 | 0.000 | true |
| `stage-b-v5-state-transition--canonical` | `transitioned_target_duplicated_as_unknown` | 1.000 | 1.000 | 0.000 | 1.000 | 1.000 | 1.000 | 0.000 | true |
| `stage-b-v5-state-transition--canonical` | `undeclared_reference_field` | 0.000 | 0.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | true |
| `stage-b-v5-state-transition--canonical` | `wrong_transition_evidence` | 1.000 | 1.000 | 1.000 | 0.000 | 1.000 | 1.000 | 0.000 | true |
| `stage-b-v5-state-transition--canonical` | `wrong_transition_value` | 1.000 | 1.000 | 1.000 | 0.000 | 1.000 | 1.000 | 0.000 | true |
| `stage-b-v5-state-transition--dual-surface-stress` | `golden` | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | true |
| `stage-b-v5-state-transition--dual-surface-stress` | `evidence_and_transition_corruption` | 1.000 | 0.000 | 1.000 | 0.000 | 1.000 | 1.000 | 0.000 | true |
| `stage-b-v5-state-transition--dual-surface-stress` | `evidence_array_reordered` | 1.000 | 0.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | true |
| `stage-b-v5-state-transition--dual-surface-stress` | `evidence_substitution` | 1.000 | 0.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | true |
| `stage-b-v5-state-transition--dual-surface-stress` | `incomplete_gate_support` | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 1.000 | 0.000 | true |
| `stage-b-v5-state-transition--dual-surface-stress` | `incomplete_retention_attestation` | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.000 | true |
| `stage-b-v5-state-transition--dual-surface-stress` | `residual_forbidden_prefix_substitution` | 1.000 | 1.000 | 0.000 | 1.000 | 1.000 | 1.000 | 0.000 | true |
| `stage-b-v5-state-transition--dual-surface-stress` | `residual_unknown_reordered` | 1.000 | 1.000 | 0.000 | 1.000 | 1.000 | 1.000 | 0.000 | true |
| `stage-b-v5-state-transition--dual-surface-stress` | `stale_blocked_gate` | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 1.000 | 0.000 | true |
| `stage-b-v5-state-transition--dual-surface-stress` | `static_pretransition_copy` | 1.000 | 1.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 | true |
| `stage-b-v5-state-transition--dual-surface-stress` | `transition_record_omitted` | 0.000 | 1.000 | 1.000 | 0.000 | 1.000 | 1.000 | 0.000 | true |
| `stage-b-v5-state-transition--dual-surface-stress` | `transitioned_target_duplicated_as_unknown` | 1.000 | 1.000 | 0.000 | 1.000 | 1.000 | 1.000 | 0.000 | true |
| `stage-b-v5-state-transition--dual-surface-stress` | `undeclared_reference_field` | 0.000 | 0.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | true |
| `stage-b-v5-state-transition--dual-surface-stress` | `wrong_transition_evidence` | 1.000 | 1.000 | 1.000 | 0.000 | 1.000 | 1.000 | 0.000 | true |
| `stage-b-v5-state-transition--dual-surface-stress` | `wrong_transition_value` | 1.000 | 1.000 | 1.000 | 0.000 | 1.000 | 1.000 | 0.000 | true |
