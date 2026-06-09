# Benchmark Run: a10-bounded-context-recall__strong_model__G0__r1

You are completing a benchmark task. Follow the instructions for the assigned harness arm.

- Fixture: `a10-bounded-context-recall`
- Model tier: `strong_model`
- Harness arm: `G0`
- Task type: `mechanism_atom`

## Harness Arm G0

Use only the task input below. Do not assume extra schemas, memory, tools, or evidence beyond what is present in the task text.

## TaskSpec

```json
{
  "task_spec_version": "0.1.0",
  "task_id": "mechanism_a10_bounded_context_recall_001",
  "task_type": "mechanism_atom",
  "intent": {
    "goal": "Answer from the active memory slice without importing stale or forbidden context.",
    "language": "en",
    "freshness": "local_snapshot"
  },
  "constraints": [
    "Primary mechanism under test: MemorySlice.",
    "Dominant failure mode: Irrelevant or stale context use.",
    "Return only information supported by the fixture."
  ],
  "required_skills": [],
  "allowed_tools": [],
  "risk_profile": "medium",
  "memory_slice_id": "mem_mechanism_a10_bounded_context_recall_001",
  "evidence_bundle_id": "ev_mechanism_a10_bounded_context_recall_001",
  "output_contract_id": "out_mechanism_a10_bounded_context_recall_001"
}
```

## Task Input

Must-load: current roadmap says Stage 2 is next. Must-not-load: old plan says run another broad workflow slice. Answer what work comes next.

## Output Requirements

Return the best answer for the task in a concise, reviewable form.
