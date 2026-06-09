# Harness Benchmark Metric Summary

Baseline arm: `G0`

| Arm | Metric | Baseline Gap | Arm Gap | Compression Ratio |
|---|---|---:|---:|---:|
| `G0` | `task_success` | 0.000 | 0.000 | n/a |
| `G0` | `schema_validity` | 0.067 | 0.067 | 0.000 |
| `G0` | `tool_call_correctness` | 0.000 | 0.000 | n/a |
| `G0` | `citation_grounding` | 0.000 | 0.000 | n/a |
| `G0` | `human_acceptance` | 0.022 | 0.022 | 0.000 |
| `G0` | `cost_efficiency` | 0.033 | 0.033 | 0.000 |
| `G0` | `safety_consistency` | 0.000 | 0.000 | n/a |
| `G9` | `task_success` | 0.000 | 0.083 | n/a |
| `G9` | `schema_validity` | 0.067 | 0.000 | 1.000 |
| `G9` | `tool_call_correctness` | 0.000 | 0.000 | n/a |
| `G9` | `citation_grounding` | 0.000 | 0.000 | n/a |
| `G9` | `human_acceptance` | 0.022 | 0.028 | -0.239 |
| `G9` | `cost_efficiency` | 0.033 | 0.042 | -0.250 |
| `G9` | `safety_consistency` | 0.000 | 0.000 | n/a |

Compression ratio is `1 - arm_gap / baseline_gap`. Positive values mean the harness arm reduced cross-model gap for that metric.
