# Harness Benchmark Metric Summary

Baseline arm: `G0`

| Arm | Metric | Baseline Gap | Arm Gap | Compression Ratio |
|---|---|---:|---:|---:|
| `G0` | `task_success` | 0.320 | 0.320 | 0.000 |
| `G0` | `schema_validity` | 0.346 | 0.346 | 0.000 |
| `G0` | `tool_call_correctness` | 0.294 | 0.294 | 0.000 |
| `G0` | `citation_grounding` | 0.282 | 0.282 | 0.000 |
| `G0` | `human_acceptance` | 0.304 | 0.304 | 0.000 |
| `G0` | `cost_efficiency` | 0.230 | 0.230 | 0.000 |
| `G0` | `safety_consistency` | 0.333 | 0.333 | 0.000 |
| `G2` | `task_success` | 0.320 | 0.250 | 0.220 |
| `G2` | `schema_validity` | 0.346 | 0.270 | 0.220 |
| `G2` | `tool_call_correctness` | 0.294 | 0.229 | 0.221 |
| `G2` | `citation_grounding` | 0.282 | 0.220 | 0.220 |
| `G2` | `human_acceptance` | 0.304 | 0.237 | 0.220 |
| `G2` | `cost_efficiency` | 0.230 | 0.180 | 0.218 |
| `G2` | `safety_consistency` | 0.333 | 0.259 | 0.221 |
| `G6` | `task_success` | 0.320 | 0.167 | 0.480 |
| `G6` | `schema_validity` | 0.346 | 0.173 | 0.500 |
| `G6` | `tool_call_correctness` | 0.294 | 0.153 | 0.478 |
| `G6` | `citation_grounding` | 0.282 | 0.147 | 0.479 |
| `G6` | `human_acceptance` | 0.304 | 0.158 | 0.480 |
| `G6` | `cost_efficiency` | 0.230 | 0.120 | 0.480 |
| `G6` | `safety_consistency` | 0.333 | 0.170 | 0.488 |
| `G9` | `task_success` | 0.320 | 0.103 | 0.680 |
| `G9` | `schema_validity` | 0.346 | 0.087 | 0.748 |
| `G9` | `tool_call_correctness` | 0.294 | 0.100 | 0.660 |
| `G9` | `citation_grounding` | 0.282 | 0.096 | 0.660 |
| `G9` | `human_acceptance` | 0.304 | 0.104 | 0.660 |
| `G9` | `cost_efficiency` | 0.230 | 0.078 | 0.661 |
| `G9` | `safety_consistency` | 0.333 | 0.092 | 0.722 |

Compression ratio is `1 - arm_gap / baseline_gap`. Positive values mean the harness arm reduced cross-model gap for that metric.
