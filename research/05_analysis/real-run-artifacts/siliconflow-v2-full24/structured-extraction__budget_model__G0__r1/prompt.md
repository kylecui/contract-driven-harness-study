# Benchmark Run: structured-extraction__budget_model__G0__r1

You are completing a benchmark task. Follow the instructions for the assigned harness arm.

- Fixture: `structured-extraction`
- Model tier: `budget_model`
- Harness arm: `G0`
- Task type: `structured_extraction`

## Harness Arm G0

Use only the task input below. Do not assume extra schemas, memory, tools, or evidence beyond what is present in the task text.

## TaskSpec

```json
{
  "task_spec_version": "0.1.0",
  "task_id": "structured_extraction_001",
  "task_type": "structured_extraction",
  "intent": {
    "goal": "Extract project metadata from a fixed proposal excerpt.",
    "language": "en",
    "freshness": "local_snapshot"
  },
  "constraints": [
    "Do not infer missing fields.",
    "Return only fields supported by the evidence bundle.",
    "Mark absent fields as null."
  ],
  "required_skills": [],
  "allowed_tools": [],
  "risk_profile": "low",
  "memory_slice_id": "mem_structured_extraction_001",
  "evidence_bundle_id": "ev_structured_extraction_001",
  "output_contract_id": "out_structured_extraction_001"
}
```

## Task Input

# Fixture Input

Project title: Topic-Aware Compaction.

Target venue: COLM 2026.

Primary metric: token savings.

No backup venue is specified in this fixture.

## Output Requirements

Return the best answer for the task in a concise, reviewable form.
