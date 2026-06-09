# Token Trajectory Label Report

## Method Note

This report uses token-only heuristics because the current result JSON does not include full message or tool-call text. Treat labels as screening signals for later manual session inspection.

## Variant Summary

| Variant | API calls | Compactions | Wall time (s) | Peak context | Avg effective ctx |
|---|---:|---:|---:|---:|---:|
| baseline | 140 | 2 | 2938.2 | 151285 | 81127.24 |
| plugin | 89 | 2 | 1780.9 | 148017 | 66366.03 |

## Label Counts

| Label | Baseline | Plugin | Delta |
|---|---:|---:|---:|
| `compaction_or_context_reset` | 3 | 2 | -1 |
| `large_generation` | 9 | 10 | +1 |
| `large_tool_or_state_rebuild` | 17 | 11 | -6 |
| `normal_progress` | 107 | 66 | -41 |
| `short_control_step` | 4 | 0 | -4 |

## Interpretation

- `large_tool_or_state_rebuild` and `context_jump` are candidate signals for state rebuilding or large tool-result ingestion.
- `compaction_or_context_reset` marks cache-read-zero calls after the first call; these should align with compaction/reset points.
- A real behavioral-change claim still requires message/tool text labels such as `state_rebuild`, `useful_progress`, and `verification`.

## Next Step

Preserve full session messages in future harness runs and join this token report with human or scripted tool-call labels.
