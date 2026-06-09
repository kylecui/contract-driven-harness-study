# Benchmark Run: research-workflow__strong_model__G0__r2

You are completing a benchmark task. Follow the instructions for the assigned harness arm.

- Fixture: `research-workflow`
- Model tier: `strong_model`
- Harness arm: `G0`
- Task type: `research_workflow`

## Harness Arm G0

Use only the task input below. Do not assume extra schemas, memory, tools, or evidence beyond what is present in the task text.

## TaskSpec

```json
{
  "task_spec_version": "0.1.0",
  "task_id": "research_workflow_001",
  "task_type": "research_workflow",
  "intent": {
    "goal": "Produce a brief, evidence-backed synthesis for a proposed systems paper.",
    "language": "en",
    "freshness": "local_snapshot"
  },
  "constraints": [
    "Separate extracted evidence from inference.",
    "Do not write final conclusions without evidence IDs.",
    "List unresolved research risks."
  ],
  "required_skills": [
    "research-router",
    "research-brief-framer",
    "research-evidence-ledger",
    "research-synthesis"
  ],
  "allowed_tools": [
    "filesystem"
  ],
  "risk_profile": "medium",
  "memory_slice_id": "mem_research_workflow_001",
  "evidence_bundle_id": "ev_research_workflow_001",
  "output_contract_id": "out_research_workflow_001"
}
```

## Task Input

# Fixture Input

Research the relationship between the two proposal tracks and decide whether they should be combined or separated.

Use the evidence bundle. Do not add outside claims.

## Output Requirements

Return the best answer for the task in a concise, reviewable form.
