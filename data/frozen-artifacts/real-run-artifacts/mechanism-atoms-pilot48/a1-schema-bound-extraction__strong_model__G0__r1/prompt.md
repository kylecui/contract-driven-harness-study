# Benchmark Run: a1-schema-bound-extraction__strong_model__G0__r1

You are completing a benchmark task. Follow the instructions for the assigned harness arm.

- Fixture: `a1-schema-bound-extraction`
- Model tier: `strong_model`
- Harness arm: `G0`
- Task type: `mechanism_atom`

## Harness Arm G0

Use only the task input below. Do not assume extra schemas, memory, tools, or evidence beyond what is present in the task text.

## TaskSpec

```json
{
  "task_spec_version": "0.1.0",
  "task_id": "mechanism_a1_schema_bound_extraction_001",
  "task_type": "mechanism_atom",
  "intent": {
    "goal": "Return a valid JSON object with required planning fields and supported evidence IDs.",
    "language": "en",
    "freshness": "local_snapshot"
  },
  "constraints": [
    "Primary mechanism under test: OutputContract.",
    "Dominant failure mode: Missing required structure.",
    "Return only information supported by the fixture."
  ],
  "required_skills": [],
  "allowed_tools": [],
  "risk_profile": "medium",
  "memory_slice_id": "mem_mechanism_a1_schema_bound_extraction_001",
  "evidence_bundle_id": "ev_mechanism_a1_schema_bound_extraction_001",
  "output_contract_id": "out_mechanism_a1_schema_bound_extraction_001"
}
```

## Task Input

Planning note: Proposal NEXT is Contract-Driven Harness. Target venue ACL Findings. Primary metric weak-model enablement lift. Evidence IDs: atom-a1-e01, atom-a1-e02. Ignore HOLD proposal Topic-Aware Compaction.

## Output Requirements

Return the best answer for the task in a concise, reviewable form.
