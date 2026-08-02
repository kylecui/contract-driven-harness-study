# Stage B v4 Bounded Recomposition

Build one local-first composition packet from the supplied fixed snapshot.

Rules:
- Copy `OutputContract.exact_output_template`.
- Preserve both `state_inventory` arrays exactly.
- Preserve all `grounded_claims` slot IDs and `evidence_ids` arrays exactly.
- Only `claim` prose may be edited.
- Keep `composition_gate.status` equal to `blocked`.
- Keep `provider_execution` blocked until `stage_b_v4_recomposition_local_gate` passes.
- Keep all three support slot IDs in their declared order.
- Return exactly one JSON object with no Markdown fence or extra prose.
