# Stage B v4 B4A Input: Exact Evidence-Array Immutability

Copy the three slots from `OutputContract.exact_output_template`.

Rules:
- Only `claim` prose is editable.
- `slot_id` and `evidence_ids` are immutable.
- Array order and multiplicity are part of the contract.
- Do not merge slots, add support, remove support, or rename fields.
- Return exactly one JSON object.
