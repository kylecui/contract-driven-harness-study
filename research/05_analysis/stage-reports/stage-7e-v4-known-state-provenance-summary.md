# Stage 7e v4 Known-State Provenance Smoke Summary

Date: 2026-06-09

## Purpose

Stage 7e v4 targeted the remaining Stage 7e v3 failure: the low-cost model could preserve unknown-state fields, trace, and gate obligations, but one G8 run compressed known-state provenance into generic labels.

This was a targeted known-state provenance ablation, not a broad workflow expansion.

## Experimental Design

Hypothesis:

- An explicit known-state provenance contract will repair low-cost-model compression of Stage 7r.1 / Stage 7r.2 / Stage 7e-v2 / Stage 7e-v3 state into generic labels.

Independent variable:

- Explicit `state_inventory.known_state[]` contract requiring `state_id`, `fact`, and `evidence_ids`.

Dependent variables:

- `state_accuracy`
- `citation_grounding`
- `evidence_type_accuracy`
- full macro `atom_primary_metric`

Baseline:

- Stage 7e v3: 3/4 full macro pass; one G8 run failed because known-state provenance was compressed.

Targeted smoke:

- model: `budget_model`
- provider/model: SiliconFlow `Qwen/Qwen3-8B`
- arms: G8, G9
- repetitions: 2
- planned runs: 4

## Local Gates

Local gates passed before API execution:

- v1/v2/v3/v4 local golden/bad regression: 8/8 expectations met.
- v4 known-bad `compressed_known_state_provenance` failed as expected with `state_accuracy=0.000`.
- Packet dry-run compiled 4/4 packets.
- Preflight passed with 0 errors and 0 warnings.

During evaluation, the evaluator was updated to accept construct-valid output variants:

- `grounded_claims` as either a single object or a list of objects.
- `typed_evidence` as either bucketed evidence lists, list items with `type`, or an `evidence_id -> type` mapping.
- carried-obligation statuses such as `excluded` and `enforced`.

Local golden/bad regression still passed after these corrections.

## Execution

Initial execution:

- 3/4 runs executed successfully.
- `budget_model G9 r2` failed with a SiliconFlow read timeout at 420 seconds.

Retry sequence:

- Retry 1 used `timeout_seconds=900` and `max_output_tokens=600`; the provider returned, but output JSON was truncated.
- Retry 2 used `timeout_seconds=900` and `max_output_tokens=2000`; the provider returned a complete output and evaluation completed.

Execution artifacts:

- `research/05_analysis/stage7e-v4-known-state-provenance-decision-adapter.json`
- `research/05_analysis/stage7e-v4-known-state-provenance-decision-adapter-events.jsonl`
- `research/05_analysis/stage7e-v4-known-state-provenance-decision-g9-r2-retry-adapter.json`
- `research/05_analysis/stage7e-v4-known-state-provenance-decision-g9-r2-retry-events.jsonl`
- `research/05_analysis/stage7e-v4-known-state-provenance-decision-g9-r2-retry2000-adapter.json`
- `research/05_analysis/stage7e-v4-known-state-provenance-decision-g9-r2-retry2000-events.jsonl`

Final evaluation:

- `research/05_analysis/stage7e-v4-known-state-provenance-decision-evaluation-final-v2.md`
- `research/05_analysis/stage7e-v4-known-state-provenance-decision-evaluation-runs-final-v2.json`

## Results

| Run | Arm | Completed | Full pass | Task success | State | Grounding | Evidence type | Trace | Gate | Primary |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `budget_model__G8__r1` | G8 | 1 | 1 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| `budget_model__G8__r2` | G8 | 1 | 1 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| `budget_model__G9__r1` | G9 | 1 | 1 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| `budget_model__G9__r2` | G9 | 1 | 1 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |

Aggregate:

- Completed: 4/4 after retry.
- Full macro pass: 4/4.
- `task_success`: 1.000 for every run.
- `atom_primary_metric`: 1.000 for every run.

## Interpretation

Stage 7e v4 repairs the known-state provenance failure observed in Stage 7e v3.

Across Stage 7e v2-v4, the repair path is now clear:

- v2 repaired stage-gate and decision-trace retention.
- v3 repaired Git/CI/network unknown-state retention.
- v4 repaired evidence-linked known-state provenance retention.

This is strong evidence for a narrow mechanism composition claim: when state, evidence, trace, gate, and carried obligations are made explicit, the low-cost model can complete a fixed evidence-bound decision macro under G8/G9.

## Claim Boundary

Supported claim:

- Low-cost-model G8/G9 can complete the fixed Stage 7e evidence-bound decision macro when the harness makes known-state provenance, unknown-state retention, evidence binding, decision trace, and stage gate obligations explicit.

Not supported:

- Full research workflow readiness.
- Full project initialization readiness.
- Universal model-gap closure.
- Production readiness.

## Next Gate

Stage 7e v4 closes the current narrow evidence-decision macro repair loop.

Next recommended work:

1. Update the claim-boundary memo and methodology outline with Stage 7e v1-v4 evidence.
2. Define the next macro only if it can preserve the same explicit contracts.
3. Keep full project initialization and full research workflow blocked until a separate macro fixture is built with deterministic evaluation and explicit cross-step state mutation boundaries.
