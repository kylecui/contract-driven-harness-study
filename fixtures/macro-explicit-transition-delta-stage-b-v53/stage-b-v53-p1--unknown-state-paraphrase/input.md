# Stage B v5.3 Controlled State Transition

Protocol profile: P1
Perturbation condition: unknown-state-paraphrase

Apply the supplied fixture event to the declared initial state.

Rules:
- Use `evidence_ids` as the only reference field.
- Copy every `required_evidence_bindings` object exactly and in order.
- Satisfy `required_postconditions` exactly.
- Copy `required_transition_gate` exactly, including `next_action`.
- Copy `required_attestation` exactly.
- The event has fixture-only scope and does not authorize a real tool call.
- Return exactly one JSON object with no Markdown fence or extra prose.
