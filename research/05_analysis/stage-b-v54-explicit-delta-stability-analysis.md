# Stage B v5.4 Explicit-Delta Stability Analysis

- Runs: 40
- Decision: `bounded_stability_confirmed`

## Overall

| Metric | Pass | Rate | Wilson 95% |
|---|---:|---:|---|
| `controlled_state_mutation_success` | 40/40 | 1.000 | [0.912, 1.000] |
| `exact_evidence_array_preservation` | 40/40 | 1.000 | [0.912, 1.000] |
| `residual_unknown_vocabulary_accuracy` | 40/40 | 1.000 | [0.912, 1.000] |
| `state_transition_accuracy` | 40/40 | 1.000 | [0.912, 1.000] |
| `transition_gate_accuracy` | 40/40 | 1.000 | [0.912, 1.000] |
| `schema_validity` | 40/40 | 1.000 | [0.912, 1.000] |
| `retention_attestation_accuracy` | 40/40 | 1.000 | [0.912, 1.000] |

## Conditions

| Condition | Strict pass | State pass |
|---|---:|---:|
| `canonical` | 8/8 | 8/8 |
| `distractor_evidence` | 8/8 | 8/8 |
| `evidence_order_shuffled` | 8/8 | 8/8 |
| `field_alias` | 8/8 | 8/8 |
| `unknown_state_paraphrase` | 8/8 | 8/8 |

## Hypotheses

- `H1_absolute_stability`: true
- `H2_critical_components`: true
- `H3_execution_integrity`: true
