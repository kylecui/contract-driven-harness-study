# Harness Benchmark Metric Summary

Baseline arm: `G0`

| Arm | Metric | Baseline Gap | Arm Gap | Compression Ratio |
|---|---|---:|---:|---:|
| `G0` | `task_success` | 0.400 | 0.400 | 0.000 |
| `G0` | `schema_validity` | 0.400 | 0.400 | 0.000 |
| `G0` | `tool_call_correctness` | 0.300 | 0.300 | 0.000 |
| `G0` | `citation_grounding` | 0.300 | 0.300 | 0.000 |
| `G0` | `human_acceptance` | 0.400 | 0.400 | 0.000 |
| `G0` | `cost_efficiency` | 0.300 | 0.300 | 0.000 |
| `G0` | `safety_consistency` | 0.200 | 0.200 | 0.000 |
| `G9` | `task_success` | 0.400 | 0.100 | 0.750 |
| `G9` | `schema_validity` | 0.400 | 0.050 | 0.875 |
| `G9` | `tool_call_correctness` | 0.300 | 0.050 | 0.833 |
| `G9` | `citation_grounding` | 0.300 | 0.050 | 0.833 |
| `G9` | `human_acceptance` | 0.400 | 0.100 | 0.750 |
| `G9` | `cost_efficiency` | 0.300 | 0.150 | 0.500 |
| `G9` | `safety_consistency` | 0.200 | 0.050 | 0.750 |

Compression ratio is `1 - arm_gap / baseline_gap`. Positive values mean the harness arm reduced cross-model gap for that metric.
