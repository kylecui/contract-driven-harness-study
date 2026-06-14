# Stage B v5 Controlled State Transition

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
- Preserve all four `grounded_claim_contract` slot IDs and reference arrays.
- Move only `permission_to_use_external_model_api` from unknown to known.
- Keep the other two unknown-state values and forbidden-inference values exact.
- Emit one transition record for `unknown` to `approved`.
- Open `provider_execution` only because this event satisfies `permission_to_use_external_model_api`.
- Treat the event as fixture state; it does not authorize a real provider call.
- Copy `required_support_slot_ids` and `required_attestation` exactly.
- Return exactly one JSON object with no Markdown fence or extra prose.
