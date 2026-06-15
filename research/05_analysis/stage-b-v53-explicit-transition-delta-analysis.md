# Stage B v5.3 Explicit Transition-Delta Analysis

- Runs: 30
- Decision: `mixed_result`
- Residual-state risk difference: 0.133
- Exact McNemar two-sided p: 0.500
- Discordant pairs (treatment pass/control fail vs treatment fail/control pass): 2 vs 0

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

## Matched-Pair Results

| Condition | Repetition | Treatment | Control | Classification |
|---|---:|---|---|---|
| `canonical` | 1 | pass | pass | `treatment_pass_control_pass` |
| `canonical` | 2 | pass | pass | `treatment_pass_control_pass` |
| `canonical` | 3 | pass | pass | `treatment_pass_control_pass` |
| `distractor_evidence` | 1 | pass | pass | `treatment_pass_control_pass` |
| `distractor_evidence` | 2 | pass | pass | `treatment_pass_control_pass` |
| `distractor_evidence` | 3 | pass | pass | `treatment_pass_control_pass` |
| `evidence_order_shuffled` | 1 | pass | pass | `treatment_pass_control_pass` |
| `evidence_order_shuffled` | 2 | pass | pass | `treatment_pass_control_pass` |
| `evidence_order_shuffled` | 3 | pass | fail | `treatment_pass_control_fail` |
| `field_alias` | 1 | pass | pass | `treatment_pass_control_pass` |
| `field_alias` | 2 | pass | pass | `treatment_pass_control_pass` |
| `field_alias` | 3 | pass | fail | `treatment_pass_control_fail` |
| `unknown_state_paraphrase` | 1 | pass | pass | `treatment_pass_control_pass` |
| `unknown_state_paraphrase` | 2 | pass | pass | `treatment_pass_control_pass` |
| `unknown_state_paraphrase` | 3 | pass | pass | `treatment_pass_control_pass` |

## Hypotheses

- `H1_delta_robustness`: true
- `H2_delta_effect`: false
- `H3_obligation_preservation`: true
- `H4_no_regression`: true
