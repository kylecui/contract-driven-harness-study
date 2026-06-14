# Stage B v5.1 Controlled State Transition

Apply one supplied event to the fixed initial state.

Initial unknown state:
["branch_currently_checked_out", "continuous_integration_result", "permission_to_use_external_model_api"]

Initial forbidden inferences:
["do_not_guess_branch_currently_checked_out", "do_not_guess_continuous_integration_result", "do_not_guess_permission_to_use_external_model_api"]

Transition event:
- event_id: event-api-approval-001
- scope: fixture_only
- state_id: permission_to_use_external_model_api
- from_status: unknown
- to_status: approved
- source_references: ["ev-09"]

Rules:
- Use `source_references` as the only reference field.
- Follow `OutputContract.output_shape` exactly.
- Copy `required_evidence_bindings` exactly, including order.
- Move only `permission_to_use_external_model_api` from unknown to known.
- Keep the other two unknown-state and forbidden-inference values exact.
- Emit one transition record for `unknown` to `approved`.
- Copy `required_transition_gate` exactly, including `next_action`.
- Treat the event as fixture state; it does not authorize a provider call.
- Copy `required_attestation` exactly.
- Return exactly one JSON object with no Markdown fence or extra prose.
