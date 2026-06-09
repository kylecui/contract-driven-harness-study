# Stage 7e v3 State-Retention Decision Smoke Summary

Date: 2026-06-09

## Purpose

Stage 7e v3 targeted the remaining Stage 7e v2 failure: trace and stage-gate retention were repaired, but 3/4 low-cost-model runs missed explicit unknown-state inventory for current Git branch, CI status, and network/API approval.

This was a targeted state-retention ablation, not a broad workflow expansion.

## Experimental Design

Hypothesis:

- An explicit state-retention contract will repair the low-cost model's omission of unknown-state fields while preserving the Stage 7e v2 trace/gate repairs.

Independent variable:

- Explicit state-retention contract for `state_inventory.unknown_state` and `state_inventory.forbidden_inferences`.

Dependent variables:

- `state_accuracy`
- `trace_completeness`
- `stage_completion`
- full macro `atom_primary_metric`

Baseline:

- Stage 7e v2: 3/4 runs failed full macro scoring because `state_accuracy=0.000`.

Targeted smoke:

- model: `budget_model`
- provider/model: SiliconFlow `Qwen/Qwen3-8B`
- arms: G8, G9
- repetitions: 2
- planned runs: 4

## Local Gates

Local gates passed before API execution:

- v1/v2/v3 local golden/bad regression: 6/6 expectations met.
- v3 known-bad `missing_unknown_state_inventory` failed as expected with `state_accuracy=0.000`.
- Packet dry-run compiled 4/4 packets.
- Preflight passed with 0 errors and 0 warnings.

During evaluation, the v3 output contract was updated to declare acceptable C2 support-evidence combinations for the v3 candidate claim. The evaluator was then changed to read those combinations from the contract instead of using the Stage 7e v1 fixed `e01/e04` evidence rule. Local golden/bad regression still passed after this correction.

Artifacts:

- `research/04_methods/macro-tasks/stage7e-v3-state-retention-decision/`
- `research/05_analysis/stage7e-v3-state-retention-local-check-v2.md`
- `research/05_analysis/stage7e-v3-state-retention-decision-preflight.md`

## Execution

Execution completed 4/4 runs. No provider timeout or adapter error occurred.

Adapter artifacts:

- `research/05_analysis/stage7e-v3-state-retention-decision-adapter.json`
- `research/05_analysis/stage7e-v3-state-retention-decision-adapter-events.jsonl`

Final evaluation:

- `research/05_analysis/stage7e-v3-state-retention-decision-evaluation-v2.md`
- `research/05_analysis/stage7e-v3-state-retention-decision-evaluation-runs-v2.json`

## Results

| Run | Arm | Completed | Full pass | Task success | State | Trace | Gate | Primary |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| `budget_model__G8__r1` | G8 | 1 | 0 | 0.857 | 0.000 | 1.000 | 1.000 | 0.000 |
| `budget_model__G8__r2` | G8 | 1 | 1 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| `budget_model__G9__r1` | G9 | 1 | 1 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| `budget_model__G9__r2` | G9 | 1 | 1 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |

Aggregate:

- Unknown-state retention target: 4/4 runs preserved `current_git_branch`, `ci_status`, and `network_api_approval` in `unknown_state` and preserved matching forbidden-inference entries.
- Trace/gate retention: 4/4 runs passed `trace_completeness=1.000` and `stage_completion=1.000`.
- Full macro pass: 3/4 runs passed all strict metrics.
- The only non-passing run, G8 r1, failed broader `state_accuracy` because it used generic known-state labels and did not preserve the expected Stage 7r.1/Stage 7r.2 known-state provenance.

## Interpretation

Stage 7e v3 repairs the targeted unknown-state retention failure.

Compared with Stage 7e v2, the explicit state-retention contract repaired the exact failed dimension:

- required unknown state fields: absent/unstable in v2 -> present in 4/4 v3 runs
- required forbidden inference fields: absent/unstable in v2 -> present in 4/4 v3 runs

However, Stage 7e v3 still does not justify broader macro expansion. The remaining G8 r1 failure shows that even when unknown-state fields are retained, the model can compress known-state provenance into generic labels such as `mechanism_atom_evidence: complete`, which loses the explicit Stage 7r.1/Stage 7r.2 chain.

## Claim Boundary

Supported claim:

- Explicit state-retention contracts can repair the low-cost model's omission of Git/CI/network unknown-state obligations in the Stage 7e evidence-decision macro.
- Low-cost-model G9 passed the full v3 macro in 2/2 repetitions.

Not supported:

- Full Stage 7e macro stability across G8/G9 repetitions.
- Full research workflow or project initialization readiness.
- Universal model-gap closure.

## Next Gate

Before broader macro expansion, add a Stage 7e v4 known-state provenance patch:

1. Require `state_inventory.known_state` to enumerate `stage7r1_targeted_smoke_complete`, `stage7r2_narrow_macro_admitted`, `stage7e_v2_trace_gate_retention_repaired`, and `stage7e_v2_state_inventory_gap_observed`.
2. Require each known-state item to carry evidence IDs.
3. Preserve v2/v3 trace, gate, unknown-state, and forbidden-inference retention requirements.
4. Run a targeted low-cost-model G8/G9 smoke with two repetitions.

Full project initialization and full research workflow remain blocked.
