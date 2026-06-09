# Harness Benchmark Metric Summary

Baseline arm: `G0`
Strong model: `strong_model`
Weak model: `budget_model`

| Arm | Metric | Baseline Gap | Arm Gap | Compression Ratio | Weak Lift | Weak vs Strong G0 |
|---|---|---:|---:|---:|---:|---:|
| `G0` | `task_success` | 0.000 | 0.000 | n/a | 0.000 | 0.000 |
| `G0` | `schema_validity` | 0.000 | 0.000 | n/a | 0.000 | 0.000 |
| `G0` | `tool_call_correctness` | 0.000 | 0.000 | n/a | 0.000 | 0.000 |
| `G0` | `citation_grounding` | 0.000 | 0.000 | n/a | 0.000 | 0.000 |
| `G0` | `human_acceptance` | 0.000 | 0.000 | n/a | 0.000 | 0.000 |
| `G0` | `cost_efficiency` | 0.000 | 0.000 | n/a | 0.000 | 0.000 |
| `G0` | `safety_consistency` | 0.000 | 0.000 | n/a | 0.000 | 0.000 |
| `G0` | `constraint_consistency` | 0.000 | 0.000 | n/a | 0.000 | 0.000 |
| `G0` | `state_accuracy` | 0.000 | 0.000 | n/a | 0.000 | 0.000 |
| `G0` | `evidence_type_accuracy` | 0.000 | 0.000 | n/a | 0.000 | 0.000 |
| `G0` | `stage_completion` | 0.000 | 0.000 | n/a | 0.000 | 0.000 |
| `G0` | `repair_success` | 0.000 | 0.000 | n/a | 0.000 | 0.000 |
| `G0` | `trace_completeness` | 0.000 | 0.000 | n/a | 0.000 | 0.000 |
| `G0` | `context_relevance` | 0.000 | 0.000 | n/a | 0.000 | 0.000 |
| `G0` | `atom_primary_metric` | 0.000 | 0.000 | n/a | 0.000 | 0.000 |
| `G8` | `task_success` | 0.000 | 0.200 | n/a | 0.800 | 0.800 |
| `G8` | `schema_validity` | 0.000 | 0.000 | n/a | 1.000 | 1.000 |
| `G8` | `tool_call_correctness` | 0.000 | 0.000 | n/a | 0.000 | 0.000 |
| `G8` | `citation_grounding` | 0.000 | 0.000 | n/a | 0.000 | 0.000 |
| `G8` | `human_acceptance` | 0.000 | 0.100 | n/a | 0.900 | 0.900 |
| `G8` | `cost_efficiency` | 0.000 | 0.200 | n/a | 0.800 | 0.800 |
| `G8` | `safety_consistency` | 0.000 | 0.000 | n/a | 1.000 | 1.000 |
| `G8` | `constraint_consistency` | 0.000 | 0.000 | n/a | 1.000 | 1.000 |
| `G8` | `state_accuracy` | 0.000 | 0.000 | n/a | 0.000 | 0.000 |
| `G8` | `evidence_type_accuracy` | 0.000 | 0.000 | n/a | 0.000 | 0.000 |
| `G8` | `stage_completion` | 0.000 | 0.000 | n/a | 1.000 | 1.000 |
| `G8` | `repair_success` | 0.000 | 1.000 | n/a | 0.000 | 0.000 |
| `G8` | `trace_completeness` | 0.000 | 0.000 | n/a | 1.000 | 1.000 |
| `G8` | `context_relevance` | 0.000 | 1.000 | n/a | 0.000 | 0.000 |
| `G8` | `atom_primary_metric` | 0.000 | 1.000 | n/a | 0.000 | 0.000 |
| `G9` | `task_success` | 0.000 | 0.100 | n/a | 0.900 | 0.900 |
| `G9` | `schema_validity` | 0.000 | 0.000 | n/a | 1.000 | 1.000 |
| `G9` | `tool_call_correctness` | 0.000 | 0.000 | n/a | 0.000 | 0.000 |
| `G9` | `citation_grounding` | 0.000 | 0.000 | n/a | 0.000 | 0.000 |
| `G9` | `human_acceptance` | 0.000 | 0.050 | n/a | 0.950 | 0.950 |
| `G9` | `cost_efficiency` | 0.000 | 0.100 | n/a | 0.900 | 0.900 |
| `G9` | `safety_consistency` | 0.000 | 0.000 | n/a | 1.000 | 1.000 |
| `G9` | `constraint_consistency` | 0.000 | 0.000 | n/a | 1.000 | 1.000 |
| `G9` | `state_accuracy` | 0.000 | 0.000 | n/a | 0.000 | 0.000 |
| `G9` | `evidence_type_accuracy` | 0.000 | 0.000 | n/a | 0.000 | 0.000 |
| `G9` | `stage_completion` | 0.000 | 0.000 | n/a | 1.000 | 1.000 |
| `G9` | `repair_success` | 0.000 | 0.000 | n/a | 1.000 | 1.000 |
| `G9` | `trace_completeness` | 0.000 | 0.000 | n/a | 1.000 | 1.000 |
| `G9` | `context_relevance` | 0.000 | 1.000 | n/a | 0.000 | 0.000 |
| `G9` | `atom_primary_metric` | 0.000 | 1.000 | n/a | 0.000 | 0.000 |

Compression ratio is `1 - arm_gap / baseline_gap`. Positive values mean the harness arm reduced cross-model gap for that metric.
Weak lift is `weak_model_arm - weak_model_G0`.
Weak vs Strong G0 is `weak_model_arm - strong_model_G0`.
