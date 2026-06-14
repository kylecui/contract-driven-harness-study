# Stage B v5.2 Evidence-Binding Ablation

Representation profile: R1
Perturbation condition: distractor-evidence

Apply the supplied fixture event to the declared initial state.

Rules:
- Use `evidence_ids` as the only reference field.
- Write non-empty claim prose in each grounded claim, but copy every slot ID and reference array exactly.
- Move only `network_api_approval` from unknown to approved.
- Preserve the other unknown-state and forbidden-inference values exactly.
- Copy `required_transition_gate` exactly, including `next_action`.
- Copy `required_attestation` exactly.
- The event has fixture-only scope and does not authorize a real tool call.
- Return exactly one JSON object with no Markdown fence or extra prose.
