# Benchmark Run: a4-state-inventory__budget_model__G0__r1

You are completing a benchmark task. Follow the instructions for the assigned harness arm.

- Fixture: `a4-state-inventory`
- Model tier: `budget_model`
- Harness arm: `G0`
- Task type: `mechanism_atom`

## Harness Arm G0

Use only the task input below. Do not assume extra schemas, memory, tools, or evidence beyond what is present in the task text.

## TaskSpec

```json
{
  "task_spec_version": "0.1.0",
  "task_id": "mechanism_a4_state_inventory_001",
  "task_type": "mechanism_atom",
  "intent": {
    "goal": "Inventory project state without guessing absent filesystem facts.",
    "language": "en",
    "freshness": "local_snapshot"
  },
  "constraints": [
    "Primary mechanism under test: MemorySlice.",
    "Dominant failure mode: State hallucination.",
    "Return only information supported by the fixture."
  ],
  "required_skills": [],
  "allowed_tools": [],
  "risk_profile": "medium",
  "memory_slice_id": "mem_mechanism_a4_state_inventory_001",
  "evidence_bundle_id": "ev_mechanism_a4_state_inventory_001",
  "output_contract_id": "out_mechanism_a4_state_inventory_001"
}
```

## Task Input

Snapshot: existing files are AGENTS.md and research/CONTEXT.md. Missing file is research/06_outputs/README.md. Protected file is AGENTS.md. Do not infer other files.

## Output Requirements

Return the best answer for the task in a concise, reviewable form.
