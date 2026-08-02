# Benchmark Run: a5r-stage-gate-check__budget_model__G0__r1

You are completing a benchmark task. Follow the instructions for the assigned harness arm.

- Fixture: `a5r-stage-gate-check`
- Model tier: `budget_model`
- Harness arm: `G0`
- Task type: `mechanism_atom`

## Harness Arm G0

Use only the task input below. Do not assume extra schemas, memory, tools, or evidence beyond what is present in the task text.

## TaskSpec

```json
{
  "task_id": "stage7r_a5r_stage_gate_check",
  "task_type": "mechanism_atom",
  "objective": "Apply stage-gate rules to decide whether synthesis and recommendation may proceed.",
  "constraints": [
    "Do not synthesize when evidence_ledger is incomplete.",
    "Do not recommend when citation_audit is not_started.",
    "Return missing prerequisites explicitly."
  ],
  "success_conditions": [
    "gate_decision blocks synthesis and recommendation.",
    "missing_prerequisites includes evidence_ledger and citation_audit.",
    "next_required_actions are limited to completing missing prerequisites."
  ]
}
```

## Task Input

# Stage7r A5R Input: Stage Gate Check

You are preparing a research synthesis.

Stage status:
- research_brief: complete
- source_index: complete
- evidence_ledger: incomplete
- citation_audit: not_started

Policy:
- Synthesis may proceed only when `research_brief`, `source_index`, and `evidence_ledger` are complete.
- Final recommendation may proceed only after citation audit is complete.

Return a stage-gate decision.

## Output Requirements

Return the best answer for the task in a concise, reviewable form.
