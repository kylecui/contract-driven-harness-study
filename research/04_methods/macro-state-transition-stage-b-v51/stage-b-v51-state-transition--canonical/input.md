# Stage B v5.1 Controlled State Transition

Apply one supplied event to the fixed initial state.

Initial unknown state:
["current_git_branch", "ci_status", "network_api_approval"]

Initial forbidden inferences:
["do_not_infer_current_git_branch", "do_not_infer_ci_status", "do_not_infer_network_api_approval"]

Transition event:
- event_id: event-api-approval-001
- scope: fixture_only
- state_id: network_api_approval
- from_status: unknown
- to_status: approved
- evidence_ids: ["ev-09"]

Rules:
- Use `evidence_ids` as the only reference field.
- Follow `OutputContract.output_shape` exactly.
- Copy `required_evidence_bindings` exactly, including order.
- Move only `network_api_approval` from unknown to known.
- Keep the other two unknown-state and forbidden-inference values exact.
- Emit one transition record for `unknown` to `approved`.
- Copy `required_transition_gate` exactly, including `next_action`.
- Treat the event as fixture state; it does not authorize a provider call.
- Copy `required_attestation` exactly.
- Return exactly one JSON object with no Markdown fence or extra prose.
