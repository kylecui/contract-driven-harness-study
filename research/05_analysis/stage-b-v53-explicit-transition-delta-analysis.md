# Stage B v5.3 Explicit Transition-Delta Analysis

- Runs: 30
- Decision: `mixed_result`
- Residual-state risk difference: 0.133
- Fisher exact two-sided p: 0.48275862

## Arm Results

| Arm | Strict pass | State pass | Evidence pass | Gate pass |
|---|---:|---:|---:|---:|
| `explicit_delta` | 15/15 | 15/15 | 15/15 | 15/15 |
| `postcondition_only` | 13/15 | 13/15 | 15/15 | 15/15 |

## Cell Results

| Arm | Condition | Strict pass | State pass | Cell decision |
|---|---|---:|---:|---|
| `explicit_delta` | `canonical` | 3/3 | 3/3 | pass |
| `explicit_delta` | `distractor_evidence` | 3/3 | 3/3 | pass |
| `explicit_delta` | `evidence_order_shuffled` | 3/3 | 3/3 | pass |
| `explicit_delta` | `field_alias` | 3/3 | 3/3 | pass |
| `explicit_delta` | `unknown_state_paraphrase` | 3/3 | 3/3 | pass |
| `postcondition_only` | `canonical` | 3/3 | 3/3 | pass |
| `postcondition_only` | `distractor_evidence` | 3/3 | 3/3 | pass |
| `postcondition_only` | `evidence_order_shuffled` | 2/3 | 2/3 | pass |
| `postcondition_only` | `field_alias` | 2/3 | 2/3 | pass |
| `postcondition_only` | `unknown_state_paraphrase` | 3/3 | 3/3 | pass |

## Hypotheses

- `H1_delta_robustness`: true
- `H2_delta_effect`: false
- `H3_obligation_preservation`: true
- `H4_no_regression`: true
