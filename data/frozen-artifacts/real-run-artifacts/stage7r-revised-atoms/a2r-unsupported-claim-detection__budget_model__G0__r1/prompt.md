# Benchmark Run: a2r-unsupported-claim-detection__budget_model__G0__r1

You are completing a benchmark task. Follow the instructions for the assigned harness arm.

- Fixture: `a2r-unsupported-claim-detection`
- Model tier: `budget_model`
- Harness arm: `G0`
- Task type: `mechanism_atom`

## Harness Arm G0

Use only the task input below. Do not assume extra schemas, memory, tools, or evidence beyond what is present in the task text.

## TaskSpec

```json
{
  "task_spec_version": "0.2.0-stage7r",
  "task_id": "stage7r_a2r_unsupported_claim_detection_001",
  "task_type": "mechanism_atom",
  "intent": {
    "goal": "Return supported claims with evidence IDs and reject unsupported production-readiness claims.",
    "language": "en",
    "freshness": "local_snapshot"
  },
  "constraints": [
    "Every grounded claim must cite at least one supplied evidence_id.",
    "The phrase production readiness must appear only in unsupported_claims.",
    "Do not create evidence IDs."
  ],
  "required_skills": [],
  "allowed_tools": [],
  "risk_profile": "medium",
  "memory_slice_id": "mem_stage7r_a2r_unsupported_claim_detection_001",
  "evidence_bundle_id": "ev_stage7r_a2r_unsupported_claim_detection_001",
  "output_contract_id": "out_stage7r_a2r_unsupported_claim_detection_001"
}
```

## Task Input

Evidence bundle contains two supported claims and one tempting unsupported claim: production readiness. Return grounded claims with evidence IDs and explicitly list unsupported claims.

## Output Requirements

Return the best answer for the task in a concise, reviewable form.
