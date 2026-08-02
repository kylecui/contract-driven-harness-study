# Benchmark Run: a8-evidence-type-separation__budget_model__G0__r1

You are completing a benchmark task. Follow the instructions for the assigned harness arm.

- Fixture: `a8-evidence-type-separation`
- Model tier: `budget_model`
- Harness arm: `G0`
- Task type: `mechanism_atom`

## Harness Arm G0

Use only the task input below. Do not assume extra schemas, memory, tools, or evidence beyond what is present in the task text.

## TaskSpec

```json
{
  "task_spec_version": "0.1.0",
  "task_id": "mechanism_a8_evidence_type_separation_001",
  "task_type": "mechanism_atom",
  "intent": {
    "goal": "Classify claims by evidence type and prevent recommendations from being presented as extracted facts.",
    "language": "en",
    "freshness": "local_snapshot"
  },
  "constraints": [
    "Primary mechanism under test: EvidenceBundle.",
    "Dominant failure mode: Type leakage.",
    "Return only information supported by the fixture."
  ],
  "required_skills": [],
  "allowed_tools": [],
  "risk_profile": "medium",
  "memory_slice_id": "mem_mechanism_a8_evidence_type_separation_001",
  "evidence_bundle_id": "ev_mechanism_a8_evidence_type_separation_001",
  "output_contract_id": "out_mechanism_a8_evidence_type_separation_001"
}
```

## Task Input

Claims include one directly measured result, one inference from multiple slices, one unresolved risk, and one recommended next action.

## Output Requirements

Return the best answer for the task in a concise, reviewable form.
