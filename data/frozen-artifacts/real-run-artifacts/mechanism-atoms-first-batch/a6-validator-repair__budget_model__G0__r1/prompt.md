# Benchmark Run: a6-validator-repair__budget_model__G0__r1

You are completing a benchmark task. Follow the instructions for the assigned harness arm.

- Fixture: `a6-validator-repair`
- Model tier: `budget_model`
- Harness arm: `G0`
- Task type: `mechanism_atom`

## Harness Arm G0

Use only the task input below. Do not assume extra schemas, memory, tools, or evidence beyond what is present in the task text.

## TaskSpec

```json
{
  "task_spec_version": "0.1.0",
  "task_id": "mechanism_a6_validator_repair_001",
  "task_type": "mechanism_atom",
  "intent": {
    "goal": "Return a repaired output that fixes the validator-reported missing evidence_ids field.",
    "language": "en",
    "freshness": "local_snapshot"
  },
  "constraints": [
    "Primary mechanism under test: ValidatorGate.",
    "Dominant failure mode: Repair failure.",
    "Return only information supported by the fixture."
  ],
  "required_skills": [],
  "allowed_tools": [],
  "risk_profile": "medium",
  "memory_slice_id": "mem_mechanism_a6_validator_repair_001",
  "evidence_bundle_id": "ev_mechanism_a6_validator_repair_001",
  "output_contract_id": "out_mechanism_a6_validator_repair_001"
}
```

## Task Input

Original output omitted evidence_ids. Validator feedback: add evidence_ids using atom-a6-e01 and keep all existing valid fields unchanged.

## Output Requirements

Return the best answer for the task in a concise, reviewable form.
