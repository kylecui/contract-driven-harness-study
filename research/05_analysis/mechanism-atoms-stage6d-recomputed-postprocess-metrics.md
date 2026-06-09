# Harness Benchmark Metric Summary

Baseline arm: `G0`
Strong model: `strong_model`
Weak model: `budget_model`

| Arm | Metric | Baseline Gap | Arm Gap | Compression Ratio | Weak Lift | Weak vs Strong G0 |
|---|---|---:|---:|---:|---:|---:|
| `G0` | `task_success` | 0.125 | 0.125 | 0.000 | 0.000 | 0.125 |
| `G0` | `schema_validity` | 0.167 | 0.167 | 0.000 | 0.000 | 0.167 |
| `G0` | `tool_call_correctness` | 0.429 | 0.429 | 0.000 | 0.000 | 0.429 |
| `G0` | `citation_grounding` | 0.000 | 0.000 | n/a | 0.000 | 0.000 |
| `G0` | `human_acceptance` | 0.146 | 0.146 | 0.000 | 0.000 | 0.146 |
| `G0` | `cost_efficiency` | 0.125 | 0.125 | 0.000 | 0.000 | 0.125 |
| `G0` | `safety_consistency` | 0.429 | 0.429 | 0.000 | 0.000 | 0.429 |
| `G0` | `constraint_consistency` | 0.143 | 0.143 | 0.000 | 0.000 | 0.143 |
| `G0` | `state_accuracy` | 0.000 | 0.000 | n/a | 0.000 | 0.000 |
| `G0` | `evidence_type_accuracy` | 0.000 | 0.000 | n/a | 0.000 | 0.000 |
| `G0` | `stage_completion` | 0.000 | 0.000 | n/a | 0.000 | 0.000 |
| `G0` | `repair_success` | 0.000 | 0.000 | n/a | 0.000 | 0.000 |
| `G0` | `trace_completeness` | 0.143 | 0.143 | 0.000 | 0.000 | 0.143 |
| `G0` | `context_relevance` | 0.000 | 0.000 | n/a | 0.000 | 0.000 |
| `G0` | `atom_primary_metric` | 0.286 | 0.286 | 0.000 | 0.000 | 0.286 |
| `G8` | `task_success` | 0.125 | 0.048 | 0.619 | 0.690 | 0.815 |
| `G8` | `schema_validity` | 0.167 | 0.000 | 1.000 | 0.833 | 1.000 |
| `G8` | `tool_call_correctness` | 0.429 | 0.000 | 1.000 | 0.429 | 0.857 |
| `G8` | `citation_grounding` | 0.000 | 0.286 | n/a | 0.714 | 0.714 |
| `G8` | `human_acceptance` | 0.146 | 0.024 | 0.838 | 0.762 | 0.908 |
| `G8` | `cost_efficiency` | 0.125 | 0.048 | 0.619 | 0.690 | 0.815 |
| `G8` | `safety_consistency` | 0.429 | 0.000 | 1.000 | 0.429 | 0.857 |
| `G8` | `constraint_consistency` | 0.143 | 0.000 | 1.000 | 0.000 | 0.143 |
| `G8` | `state_accuracy` | 0.000 | 0.036 | n/a | 0.143 | 0.143 |
| `G8` | `evidence_type_accuracy` | 0.000 | 0.000 | n/a | 0.000 | 0.000 |
| `G8` | `stage_completion` | 0.000 | 0.054 | n/a | 0.143 | 0.143 |
| `G8` | `repair_success` | 0.000 | 0.000 | n/a | 0.000 | 0.000 |
| `G8` | `trace_completeness` | 0.143 | 0.000 | 1.000 | 0.000 | 0.143 |
| `G8` | `context_relevance` | 0.000 | 0.036 | n/a | 0.286 | 0.286 |
| `G8` | `atom_primary_metric` | 0.286 | 0.089 | 0.688 | 0.571 | 0.857 |
| `G9` | `task_success` | 0.125 | 0.101 | 0.191 | 0.649 | 0.774 |
| `G9` | `schema_validity` | 0.167 | 0.000 | 1.000 | 0.833 | 1.000 |
| `G9` | `tool_call_correctness` | 0.429 | 0.000 | 1.000 | 0.429 | 0.857 |
| `G9` | `citation_grounding` | 0.000 | 0.286 | n/a | 0.357 | 0.357 |
| `G9` | `human_acceptance` | 0.146 | 0.051 | 0.654 | 0.741 | 0.887 |
| `G9` | `cost_efficiency` | 0.125 | 0.101 | 0.191 | 0.649 | 0.774 |
| `G9` | `safety_consistency` | 0.429 | 0.000 | 1.000 | 0.429 | 0.857 |
| `G9` | `constraint_consistency` | 0.143 | 0.000 | 1.000 | 0.000 | 0.143 |
| `G9` | `state_accuracy` | 0.000 | 0.036 | n/a | 0.143 | 0.143 |
| `G9` | `evidence_type_accuracy` | 0.000 | 0.000 | n/a | 0.000 | 0.000 |
| `G9` | `stage_completion` | 0.000 | 0.000 | n/a | 0.143 | 0.143 |
| `G9` | `repair_success` | 0.000 | 0.000 | n/a | 0.000 | 0.000 |
| `G9` | `trace_completeness` | 0.143 | 0.000 | 1.000 | 0.000 | 0.143 |
| `G9` | `context_relevance` | 0.000 | 0.036 | n/a | 0.286 | 0.286 |
| `G9` | `atom_primary_metric` | 0.286 | 0.036 | 0.875 | 0.571 | 0.857 |

Compression ratio is `1 - arm_gap / baseline_gap`. Positive values mean the harness arm reduced cross-model gap for that metric.
Weak lift is `weak_model_arm - weak_model_G0`.
Weak vs Strong G0 is `weak_model_arm - strong_model_G0`.
