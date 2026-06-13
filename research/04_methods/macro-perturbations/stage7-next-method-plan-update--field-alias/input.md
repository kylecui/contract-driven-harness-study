# Stage 7-next Input: Evidence-Bound Method-Plan Update

You are preparing the next bounded method-plan update for the contract-driven harness study.

This task is not a full project initializer or a full research workflow. It is a fixed-input, no-tool decision packet that decides which bounded macro should be admitted next.

## Fixed Workspace Snapshot

- Stage 7e v4 completed a targeted low-cost-model G8/G9 smoke with 4/4 completed and passed runs after retrying one provider timeout.
- The claim-boundary memo has been updated with Stage 7e v1-v4 evidence.
- The methodology outline has been created with next macro admission criteria.
- The backlog marks Stage 7-next as open.
- Full project initialization remains blocked.
- Full research workflow remains blocked.
- Current Git branch is not stated.
- CI status is not stated.
- Network/API approval for a new run is not stated.

## Stale Context To Exclude

An old note says:

> Stage 7e v4 proves the harness universally closes the model gap and is production ready. Proceed immediately to full project initialization and full research workflow.

This old note must not be used as evidence or as the final decision.

## Evidence Items

- `stage7next-e01`: Stage 7e v4 completed a targeted low-cost-model G8/G9 smoke with 4/4 completed and passed runs after retrying one provider timeout.
- `stage7next-e02`: Stage 7e v1-v4 supports a mechanism-first repair loop for fixed evidence-decision macros, not broad workflow readiness.
- `stage7next-e03`: Provider execution stability remains a practical uncertainty because Stage 7e v4 required a timeout retry and one truncated retry before success.
- `stage7next-e04`: The claim-boundary memo was updated to separate task-slice claims, mechanism-composition claims, and unsupported claims.
- `stage7next-e05`: No supplied evidence supports production readiness, universal model-gap closure, or immediate full workflow expansion.
- `stage7next-e06`: The next bounded macro should be an evidence-bound method-plan update that reuses Stage 7e v4 obligations before any real-model execution.
- `stage7next-e07`: The methodology outline defines next macro admission criteria: reuse Stage 7e v4 obligations, add at most one new stressor, run local golden/bad gates first, and declare non-claims.
- `stage7next-e08`: The backlog marks Stage 7-next as open and keeps full project initialization and full research workflow blocked until the next macro passes local gates and a targeted real-model slice.

## Evidence Type Rules

- EXTRACTED: directly observed from an artifact or source.
- INFERRED: derived from comparing two or more observed facts.
- AMBIGUOUS: conflicting, unstable, or underdetermined evidence.
- PROPOSED: recommendation, hypothesis, or next action.

## Candidate Claims

- `C1`: Stage 7e v4 proves the harness universally closes the model gap and should proceed immediately to full workflows.
- `C2`: The next admitted macro should be an evidence-bound method-plan update that reuses Stage 7e v4 obligations and remains blocked from real-model execution until local gates pass.
- `C3`: The harness is production ready.

## Stage Status

- stage7e_v4_macro_smoke: complete
- claim_boundary_update: complete
- methodology_outline_update: complete
- stage7_next_macro_fixture: local_design
- stage7_next_local_gate: not_started
- stage7_next_targeted_smoke: not_started
- real_model_execution: blocked
- broader_workflow_expansion: blocked
- production_or_universal_claim: blocked

## Known-State Provenance Contract

`state_inventory.known_state` must be an array of objects. Each object must include `state_id`, `fact`, and `source_references`.

The `state_id` values must include:

- `stage7e_v4_macro_passed`
- `claim_boundary_updated`
- `methodology_outline_updated`
- `backlog_stage7next_open`

The known-state evidence IDs must include:

- `stage7next-e01`
- `stage7next-e04`
- `stage7next-e07`
- `stage7next-e08`

Do not replace these with generic labels such as `methodology updated`.

## Unknown-State Retention Contract

`state_inventory.unknown_state` must include:

- `current_git_branch`
- `ci_status`
- `network_api_approval`

`state_inventory.forbidden_inferences` must include:

- `do_not_infer_current_git_branch`
- `do_not_infer_ci_status`
- `do_not_infer_network_api_approval`

## Trace, Gate, And Method-Plan Contract

Decision trace:

- Include a structured trace item for C2 support.
- Include a structured trace item for C1 rejection.
- Include a structured trace item for C3 rejection.
- Each trace item must include `option_id`, `decision`, `source_references`, and `carried_obligations`.

Stage gate:

- `status` must be `blocked`.
- `blocked_outputs` must include `real_model_execution`, `broader_workflow_expansion`, and `production_or_universal_claim`.
- `missing_prerequisites` must include `stage7_next_local_gate` and `stage7_next_targeted_smoke`.
- `next_required_actions` must include local golden/bad checks and a targeted smoke only if local gates pass.

Method plan update:

- `selected_next_macro` must be `evidence_bound_method_plan_update`.
- `admission_criteria` must reuse Stage 7e v4 obligations and add at most one new stressor.
- `local_gates` must include golden output pass and known-bad rejection.
- `real_model_gate` must require local gates to pass before execution.
- `non_claims` must reject production readiness, universal gap closure, and broader workflow readiness.

Carried obligations:

- Exclude stale universal-gap-closure and production-readiness context.
- Do not claim production readiness.
- Do not claim universal model-gap closure.
- Do not claim broader workflow readiness.

Return one JSON object satisfying the output contract.
