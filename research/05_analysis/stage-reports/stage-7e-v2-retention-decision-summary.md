# Stage 7e v2 Retention Decision Smoke Summary

Date: 2026-06-09

## Purpose

Stage 7e v2 targeted one specific Stage 7e v1 failure: the low-cost-model G9 run preserved schema, grounding, evidence typing, and state inventory, but missed complete stage-gate and decision-trace retention.

This was a targeted retention ablation, not a broad workflow expansion.

## Experimental Design

Hypothesis:

- An explicit retention contract will repair the low-cost model's Stage 7e v1 stage-gate and decision-trace omissions.

Independent variable:

- Explicit retention contract for `decision_trace`, `stage_gate`, and `carried_obligations`.

Dependent variables:

- `trace_completeness`
- `stage_completion`
- full macro `atom_primary_metric`

Baseline:

- Stage 7e v1 low-cost-model G9: `task_success=0.714`, `trace_completeness=0.000`, `stage_completion=0.000`.

Targeted smoke:

- model: `budget_model`
- provider/model: SiliconFlow `Qwen/Qwen3-8B`
- arms: G8, G9
- repetitions: 2
- planned runs: 4

## Local Gates

Local gates passed before API execution:

- v1/v2 local golden/bad regression: 4/4 expectations met.
- v2 known-bad `missing_retention_gate_and_trace` failed as expected with `task_success=0.714`, `trace_completeness=0.000`, and `stage_completion=0.000`.
- Packet dry-run compiled 4/4 packets.
- Preflight passed with 0 errors and 0 warnings.

Artifacts:

- `research/04_methods/macro-tasks/stage7e-v2-retention-decision/`
- `research/05_analysis/stage7e-v2-retention-local-check.md`
- `research/05_analysis/stage7e-v2-retention-decision-preflight.md`

## Execution

Execution completed 4/4 runs. No provider timeout or adapter error occurred.

Adapter artifacts:

- `research/05_analysis/stage7e-v2-retention-decision-adapter.json`
- `research/05_analysis/stage7e-v2-retention-decision-adapter-events.jsonl`

Final evaluation:

- `research/05_analysis/stage7e-v2-retention-decision-evaluation.md`
- `research/05_analysis/stage7e-v2-retention-decision-evaluation-runs.json`

## Results

| Run | Arm | Completed | Full pass | Task success | State | Trace | Gate | Primary |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| `budget_model__G8__r1` | G8 | 1 | 0 | 0.857 | 0.000 | 1.000 | 1.000 | 0.000 |
| `budget_model__G8__r2` | G8 | 1 | 0 | 0.857 | 0.000 | 1.000 | 1.000 | 0.000 |
| `budget_model__G9__r1` | G9 | 1 | 1 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| `budget_model__G9__r2` | G9 | 1 | 0 | 0.857 | 0.000 | 1.000 | 1.000 | 0.000 |

Aggregate:

- Retention repair metrics: 4/4 runs passed `trace_completeness=1.000` and `stage_completion=1.000`.
- Full macro pass: 1/4 runs passed all strict metrics.
- All non-passing runs failed only `state_accuracy`; schema, grounding, evidence typing, trace, gate, and carried obligations were all correct.

## Interpretation

Stage 7e v2 repairs the targeted retention failure.

Compared with Stage 7e v1 low-cost-model G9, the explicit retention contract repaired the exact failed dimensions:

- `trace_completeness`: 0.000 -> 1.000 in 2/2 G9 v2 runs
- `stage_completion`: 0.000 -> 1.000 in 2/2 G9 v2 runs

However, Stage 7e v2 does not fully close the macro task. Three runs omitted the required unknown-state inventory for current Git branch, CI status, and network/API approval. This is an A4R-style state inventory retention issue, not the original A5/A7 retention miss.

## Claim Boundary

Supported claim:

- Explicit retention contracts can repair the low-cost model's stage-gate and decision-trace omissions in the Stage 7e evidence-decision macro.

Not supported:

- Full Stage 7e v2 macro is stable across repetitions.
- G8/G9 universally solve the composed evidence-decision macro.
- Full research workflow or project initialization is ready.
- The harness universally closes strong-vs-low-cost model gaps.

## Next Gate

Before broader macro expansion, add a Stage 7e v3 state-retention patch:

1. Require `state_inventory.unknown_state` to enumerate `current_git_branch`, `ci_status`, and `network_api_approval`.
2. Require those same unknowns to appear in `forbidden_inferences`.
3. Preserve the v2 retention requirements for trace and stage gate.
4. Run a targeted low-cost-model G8/G9 smoke with two repetitions.

Full project initialization and full research workflow remain blocked.
