# Harness Benchmark Metric Summary

Baseline arm: `G0`
Strong model: `strong_model`
Weak model: `budget_model`

| Arm | Metric | Baseline Gap | Arm Gap | Compression Ratio | Weak Lift | Weak vs Strong G0 |
|---|---|---:|---:|---:|---:|---:|
| `G0` | `task_success` | 0.167 | 0.167 | 0.000 | 0.000 | 0.167 |
| `G0` | `schema_validity` | 0.167 | 0.167 | 0.000 | 0.000 | 0.167 |
| `G0` | `tool_call_correctness` | 0.500 | 0.500 | 0.000 | 0.000 | 0.500 |
| `G0` | `citation_grounding` | 0.000 | 0.000 | n/a | 0.000 | 0.000 |
| `G0` | `human_acceptance` | 0.167 | 0.167 | 0.000 | 0.000 | 0.167 |
| `G0` | `cost_efficiency` | 0.167 | 0.167 | 0.000 | 0.000 | 0.167 |
| `G0` | `safety_consistency` | 0.500 | 0.500 | 0.000 | 0.000 | 0.500 |
| `G0` | `constraint_consistency` | 0.000 | 0.000 | n/a | 0.000 | 0.000 |
| `G0` | `state_accuracy` | 0.000 | 0.000 | n/a | 0.000 | 0.000 |
| `G0` | `evidence_type_accuracy` | 0.000 | 0.000 | n/a | 0.000 | 0.000 |
| `G0` | `stage_completion` | 0.000 | 0.000 | n/a | 0.000 | 0.000 |
| `G0` | `repair_success` | 0.000 | 0.000 | n/a | 0.000 | 0.000 |
| `G0` | `trace_completeness` | 0.000 | 0.000 | n/a | 0.000 | 0.000 |
| `G0` | `context_relevance` | 0.000 | 0.000 | n/a | 0.000 | 0.000 |
| `G0` | `atom_primary_metric` | 0.167 | 0.167 | 0.000 | 0.000 | 0.167 |
| `G2` | `task_success` | 0.167 | 0.062 | 0.625 | 0.521 | 0.688 |
| `G2` | `schema_validity` | 0.167 | 0.000 | 1.000 | 0.833 | 1.000 |
| `G2` | `tool_call_correctness` | 0.500 | 0.000 | 1.000 | 0.167 | 0.667 |
| `G2` | `citation_grounding` | 0.000 | 0.000 | n/a | 0.000 | 0.000 |
| `G2` | `human_acceptance` | 0.167 | 0.031 | 0.813 | 0.677 | 0.844 |
| `G2` | `cost_efficiency` | 0.167 | 0.062 | 0.625 | 0.521 | 0.688 |
| `G2` | `safety_consistency` | 0.500 | 0.000 | 1.000 | 0.167 | 0.667 |
| `G2` | `constraint_consistency` | 0.000 | 0.333 | n/a | 0.333 | 0.333 |
| `G2` | `state_accuracy` | 0.000 | 0.000 | n/a | 0.000 | 0.000 |
| `G2` | `evidence_type_accuracy` | 0.000 | 0.000 | n/a | 0.333 | 0.333 |
| `G2` | `stage_completion` | 0.000 | 0.000 | n/a | 0.000 | 0.000 |
| `G2` | `repair_success` | 0.000 | 0.000 | n/a | 0.000 | 0.000 |
| `G2` | `trace_completeness` | 0.000 | 0.000 | n/a | 0.000 | 0.000 |
| `G2` | `context_relevance` | 0.000 | 0.000 | n/a | 0.000 | 0.000 |
| `G2` | `atom_primary_metric` | 0.167 | 0.333 | -1.000 | 0.833 | 1.000 |
| `G8` | `task_success` | 0.167 | 0.007 | 0.958 | 0.549 | 0.715 |
| `G8` | `schema_validity` | 0.167 | 0.000 | 1.000 | 0.833 | 1.000 |
| `G8` | `tool_call_correctness` | 0.500 | 0.000 | 1.000 | 0.167 | 0.667 |
| `G8` | `citation_grounding` | 0.000 | 0.167 | n/a | 0.167 | 0.167 |
| `G8` | `human_acceptance` | 0.167 | 0.004 | 0.978 | 0.691 | 0.858 |
| `G8` | `cost_efficiency` | 0.167 | 0.007 | 0.958 | 0.549 | 0.715 |
| `G8` | `safety_consistency` | 0.500 | 0.000 | 1.000 | 0.167 | 0.667 |
| `G8` | `constraint_consistency` | 0.000 | 0.333 | n/a | 0.333 | 0.333 |
| `G8` | `state_accuracy` | 0.000 | 0.000 | n/a | 0.000 | 0.000 |
| `G8` | `evidence_type_accuracy` | 0.000 | 0.000 | n/a | 0.333 | 0.333 |
| `G8` | `stage_completion` | 0.000 | 0.000 | n/a | 0.000 | 0.000 |
| `G8` | `repair_success` | 0.000 | 0.000 | n/a | 0.000 | 0.000 |
| `G8` | `trace_completeness` | 0.000 | 0.000 | n/a | 0.000 | 0.000 |
| `G8` | `context_relevance` | 0.000 | 0.000 | n/a | 0.000 | 0.000 |
| `G8` | `atom_primary_metric` | 0.167 | 0.333 | -1.000 | 0.833 | 1.000 |
| `G9` | `task_success` | 0.167 | 0.000 | 1.000 | 0.576 | 0.743 |
| `G9` | `schema_validity` | 0.167 | 0.000 | 1.000 | 0.833 | 1.000 |
| `G9` | `tool_call_correctness` | 0.500 | 0.000 | 1.000 | 0.167 | 0.667 |
| `G9` | `citation_grounding` | 0.000 | 0.167 | n/a | 0.333 | 0.333 |
| `G9` | `human_acceptance` | 0.167 | 0.000 | 1.000 | 0.705 | 0.872 |
| `G9` | `cost_efficiency` | 0.167 | 0.000 | 1.000 | 0.576 | 0.743 |
| `G9` | `safety_consistency` | 0.500 | 0.000 | 1.000 | 0.167 | 0.667 |
| `G9` | `constraint_consistency` | 0.000 | 0.167 | n/a | 0.333 | 0.333 |
| `G9` | `state_accuracy` | 0.000 | 0.000 | n/a | 0.000 | 0.000 |
| `G9` | `evidence_type_accuracy` | 0.000 | 0.000 | n/a | 0.333 | 0.333 |
| `G9` | `stage_completion` | 0.000 | 0.000 | n/a | 0.000 | 0.000 |
| `G9` | `repair_success` | 0.000 | 0.000 | n/a | 0.000 | 0.000 |
| `G9` | `trace_completeness` | 0.000 | 0.000 | n/a | 0.000 | 0.000 |
| `G9` | `context_relevance` | 0.000 | 0.000 | n/a | 0.000 | 0.000 |
| `G9` | `atom_primary_metric` | 0.167 | 0.167 | 0.000 | 0.833 | 1.000 |

Compression ratio is `1 - arm_gap / baseline_gap`. Positive values mean the harness arm reduced cross-model gap for that metric.
Weak lift is `weak_model_arm - weak_model_G0`.
Weak vs Strong G0 is `weak_model_arm - strong_model_G0`.
