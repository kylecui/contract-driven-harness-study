# Harness Benchmark Metric Summary

Baseline arm: `G0`

| Arm | Metric | Baseline Gap | Arm Gap | Compression Ratio |
|---|---|---:|---:|---:|
| `G0` | `task_success` | 0.117 | 0.117 | 0.000 |
| `G0` | `schema_validity` | 0.194 | 0.194 | 0.000 |
| `G0` | `tool_call_correctness` | 0.500 | 0.500 | 0.000 |
| `G0` | `citation_grounding` | 0.000 | 0.000 | n/a |
| `G0` | `human_acceptance` | 0.156 | 0.156 | 0.000 |
| `G0` | `cost_efficiency` | 0.117 | 0.117 | 0.000 |
| `G0` | `safety_consistency` | 0.500 | 0.500 | 0.000 |
| `G9` | `task_success` | 0.117 | 0.000 | 1.000 |
| `G9` | `schema_validity` | 0.194 | 0.000 | 1.000 |
| `G9` | `tool_call_correctness` | 0.500 | 0.000 | 1.000 |
| `G9` | `citation_grounding` | 0.000 | 0.000 | n/a |
| `G9` | `human_acceptance` | 0.156 | 0.000 | 1.000 |
| `G9` | `cost_efficiency` | 0.117 | 0.000 | 1.000 |
| `G9` | `safety_consistency` | 0.500 | 0.000 | 1.000 |

Compression ratio is `1 - arm_gap / baseline_gap`. Positive values mean the harness arm reduced cross-model gap for that metric.
