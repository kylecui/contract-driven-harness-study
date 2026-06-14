# Stage B v5.2 Evidence-Binding Ablation Analysis

- Runs: 30
- Decision: `no_engineering_scale_representation_effect_observed`
- Evidence risk difference: 0.067
- Fisher exact two-sided p: 1.00000000

## Arm Results

| Arm | Strict pass | Evidence pass | Gate pass | Transition pass |
|---|---:|---:|---:|---:|
| `binding_separated` | 10/15 | 15/15 | 15/15 | 15/15 |
| `claim_coupled` | 10/15 | 14/15 | 15/15 | 15/15 |

## Cell Results

| Arm | Condition | Strict pass | Evidence pass | Cell decision |
|---|---|---:|---:|---|
| `binding_separated` | `canonical` | 2/3 | 3/3 | pass |
| `binding_separated` | `distractor_evidence` | 3/3 | 3/3 | pass |
| `binding_separated` | `evidence_order_shuffled` | 2/3 | 3/3 | pass |
| `binding_separated` | `field_alias` | 1/3 | 3/3 | fail |
| `binding_separated` | `unknown_state_paraphrase` | 2/3 | 3/3 | pass |
| `claim_coupled` | `canonical` | 3/3 | 3/3 | pass |
| `claim_coupled` | `distractor_evidence` | 2/3 | 2/3 | pass |
| `claim_coupled` | `evidence_order_shuffled` | 3/3 | 3/3 | pass |
| `claim_coupled` | `field_alias` | 2/3 | 3/3 | pass |
| `claim_coupled` | `unknown_state_paraphrase` | 0/3 | 3/3 | fail |

## Hypotheses

- `H1_separated_robustness`: false
- `H2_representation_effect`: false
- `H3_gate_control`: true
- `H4_transition_control`: true
- `H5_surface_transfer`: false
