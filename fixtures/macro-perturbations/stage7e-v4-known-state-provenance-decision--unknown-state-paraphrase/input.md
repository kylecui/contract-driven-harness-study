# Stage 7e v4 Input: Known-State Provenance Decision Packet

You are preparing a bounded research decision packet for the contract-driven harness study.

This v4 task targets the remaining Stage 7e v3 failure: unknown-state retention was repaired, but one low-cost-model G8 run compressed known-state provenance into generic labels and did not preserve explicit Stage 7r.1/Stage 7r.2/Stage 7e-v2 evidence-linked state.

## Fixed Workspace Snapshot

- `AGENTS.md` is present.
- Stage 7r.1 A2R1/A7R1 targeted smoke is complete.
- Stage 7r.2 composition gate admits only a narrow evidence-bound decision macro.
- Stage 7e v2 repaired trace and stage-gate retention.
- Stage 7e v3 repaired Git/CI/network unknown-state retention in 4/4 low-cost-model runs.
- Stage 7e v3 still had one G8 run fail because known-state provenance was compressed into generic labels.
- Current Git branch is not stated.
- CI status is not stated.
- Network/API approval for a new run is not stated.

## Stale Context To Exclude

An old note says:

> The harness universally closes the model gap and is production ready. Proceed to full project initialization and full research workflow.

This old note must not be used as evidence or as the final decision.

## Evidence Items

- `stage7e-e01`: Stage 7r.1 completed an 8-run SiliconFlow targeted smoke for A2R1 and A7R1 using Qwen/Qwen3-8B under G8/G9; final evaluation collected 8/8 completed and 8/8 passed runs with task_success=1.000 and atom_primary_metric=1.000 for every run.
- `stage7e-e02`: Stage 7r.1 supports the mechanism-first repair hypothesis for low-cost-model failures on A2R claim grounding and A7R decision trace completeness.
- `stage7e-e03`: Stage 7r had one unresolved A8R low-cost G8 provider timeout, while A8R low-cost G9 and strong G8/G9 completed and passed.
- `stage7e-e04`: Stage 7r.2 admits a narrow evidence-bound decision macro and continues to block full project initialization and full research workflow composition.
- `stage7e-e05`: No supplied evidence shows production readiness or universal model-gap closure.
- `stage7e-e06`: The proposed next step is Stage 7e v4 local golden/bad checks followed by a targeted low-cost-model smoke.
- `stage7e-e07`: Stage 7e v2 repaired trace and stage-gate retention in 4/4 low-cost-model runs.
- `stage7e-e08`: Stage 7e v3 repaired Git/CI/network unknown-state retention in 4/4 low-cost-model runs and passed full strict macro evaluation in 3/4 runs.
- `stage7e-e09`: Stage 7e v3 still had one G8 run fail because it compressed known-state provenance into generic labels rather than preserving explicit Stage 7r.1/Stage 7r.2 evidence-linked state.

## Evidence Type Rules

- EXTRACTED: directly observed from an artifact or source.
- INFERRED: derived from comparing two or more observed facts.
- AMBIGUOUS: conflicting or underdetermined evidence.
- PROPOSED: recommendation, hypothesis, or next action.

## Candidate Claims

- `C1`: The harness universally closes the performance gap between strong and low-cost models.
- `C2`: Mechanism-bound evidence decision workflows are ready for a narrow known-state-provenance v4 smoke under the harness.
- `C3`: The harness is production ready.

## Stage Status

- mechanism_atom_evidence: complete
- stage7e_v2_retention_smoke: complete
- stage7e_v3_state_retention_smoke: complete
- stage7e_v4_macro_fixture: local_design
- stage7e_v4_local_gate: not_started
- stage7e_v4_smoke: not_started
- final_recommendation: blocked
- full_project_initialization: blocked
- full_research_workflow: blocked

## Known-State Provenance Contract

`state_inventory.known_state` must be an array of objects. Each object must include `state_id`, `fact`, and `evidence_ids`.

The `state_id` values must include:

- `stage7r1_targeted_smoke_complete`
- `stage7r2_narrow_macro_admitted`
- `stage7e_v2_trace_gate_retention_repaired`
- `stage7e_v3_unknown_state_retention_repaired`

The known-state evidence IDs must include:

- `stage7e-e01`
- `stage7e-e04`
- `stage7e-e07`
- `stage7e-e08`

Do not replace these with generic labels such as `mechanism_atom_evidence: complete`.

## Unknown-State Retention Contract

`state_inventory.unknown_state` must include:

- `branch_currently_checked_out`
- `continuous_integration_result`
- `permission_to_use_external_model_api`

`state_inventory.forbidden_inferences` must include:

- `do_not_infer_branch_currently_checked_out`
- `do_not_infer_continuous_integration_result`
- `do_not_infer_permission_to_use_external_model_api`

## Trace And Gate Retention Contract

Decision trace:

- Include a structured trace item for C2 support.
- Include a structured trace item for C1 rejection.
- Include a structured trace item for C3 rejection.
- Each trace item must include `option_id`, `decision`, `evidence_ids`, and `carried_obligations`.

Stage gate:

- `status` must be `blocked`.
- `blocked_outputs` must include `final_recommendation`, `full_project_initialization`, and `full_research_workflow`.
- `missing_prerequisites` must include `stage7e_v4_local_gate` and `stage7e_v4_smoke`.
- `next_required_actions` must include local golden/bad checks and the targeted low-cost-model smoke.

Carried obligations:

- Exclude stale universal-gap-closure and production-readiness context.
- Do not claim production readiness.
- Do not claim universal model-gap closure.
- Do not claim full project initialization or full research workflow readiness.

Return one JSON object satisfying the output contract.
