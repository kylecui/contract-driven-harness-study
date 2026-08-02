# Benchmark Run: a7-traceable-decision__strong_model__G0__r1

You are completing a benchmark task. Follow the instructions for the assigned harness arm.

- Fixture: `a7-traceable-decision`
- Model tier: `strong_model`
- Harness arm: `G0`
- Task type: `mechanism_atom`

## Harness Arm G0

Use only the task input below. Do not assume extra schemas, memory, tools, or evidence beyond what is present in the task text.

## TaskSpec

```json
{
  "task_spec_version": "0.1.0",
  "task_id": "mechanism_a7_traceable_decision_001",
  "task_type": "mechanism_atom",
  "intent": {
    "goal": "Choose a claim level and provide a compact trace of the decision criteria used.",
    "language": "en",
    "freshness": "local_snapshot"
  },
  "constraints": [
    "Primary mechanism under test: TraceLog.",
    "Dominant failure mode: Non-observable reasoning.",
    "Return only information supported by the fixture."
  ],
  "required_skills": [],
  "allowed_tools": [],
  "risk_profile": "medium",
  "memory_slice_id": "mem_mechanism_a7_traceable_decision_001",
  "evidence_bundle_id": "ev_mechanism_a7_traceable_decision_001",
  "output_contract_id": "out_mechanism_a7_traceable_decision_001"
}
```

## Task Input

Options: gap compression, weak-model enablement, composition-boundary framing. Evidence says baseline gap is n/a but budget model improves strongly.

## Output Requirements

Return the best answer for the task in a concise, reviewable form.
