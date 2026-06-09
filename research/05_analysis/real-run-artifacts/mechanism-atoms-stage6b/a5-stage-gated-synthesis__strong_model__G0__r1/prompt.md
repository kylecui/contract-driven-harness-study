# Benchmark Run: a5-stage-gated-synthesis__strong_model__G0__r1

You are completing a benchmark task. Follow the instructions for the assigned harness arm.

- Fixture: `a5-stage-gated-synthesis`
- Model tier: `strong_model`
- Harness arm: `G0`
- Task type: `mechanism_atom`

## Harness Arm G0

Use only the task input below. Do not assume extra schemas, memory, tools, or evidence beyond what is present in the task text.

## TaskSpec

```json
{
  "task_spec_version": "0.1.0",
  "task_id": "mechanism_a5_stage_gated_synthesis_001",
  "task_type": "mechanism_atom",
  "intent": {
    "goal": "Produce staged research synthesis without skipping intermediate evidence work.",
    "language": "en",
    "freshness": "local_snapshot"
  },
  "constraints": [
    "Primary mechanism under test: WorkflowGraph.",
    "Dominant failure mode: Stage skipping.",
    "Return only information supported by the fixture."
  ],
  "required_skills": [],
  "allowed_tools": [],
  "risk_profile": "medium",
  "memory_slice_id": "mem_mechanism_a5_stage_gated_synthesis_001",
  "evidence_bundle_id": "ev_mechanism_a5_stage_gated_synthesis_001",
  "output_contract_id": "out_mechanism_a5_stage_gated_synthesis_001"
}
```

## Task Input

Use the supplied evidence to decide whether two proposal tracks should remain separate. Output stage status for brief, evidence, synthesis, recommendation, and risks.

## Output Requirements

Return the best answer for the task in a concise, reviewable form.
