# Stage7r.1 A2R1 Input: Claim-Level Evidence Binding

The model must classify claims using only the evidence bundle.

Candidate claims:
- G9 improved structured extraction contract adherence.
- Research workflow G0 had citation grounding failures.
- The harness is production ready.

Rules:
- Every grounded claim must be an object with a `claim` string and an `evidence_ids` array.
- A global evidence list is not enough.
- Unsupported claims must be placed in `unsupported_claims` with a reason.
- Do not infer production readiness without an evidence ID.
