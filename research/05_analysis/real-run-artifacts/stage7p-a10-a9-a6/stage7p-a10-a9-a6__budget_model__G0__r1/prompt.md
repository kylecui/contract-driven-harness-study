# Benchmark Run: stage7p-a10-a9-a6__budget_model__G0__r1

You are completing a benchmark task. Follow the instructions for the assigned harness arm.

- Fixture: `stage7p-a10-a9-a6`
- Model tier: `budget_model`
- Harness arm: `G0`
- Task type: `stage7p_partial_macro`

## Harness Arm G0

Use only the task input below. Do not assume extra schemas, memory, tools, or evidence beyond what is present in the task text.

## TaskSpec

```json
{
  "task_spec_id": "task_stage7p_a10_a9_a6_001",
  "task_type": "stage7p_partial_macro",
  "objective": "Compose A10 bounded context recall, A9 no-overwrite action planning, and A6 validator repair into one narrow macro task.",
  "goal": "Return a JSON object that uses current context, excludes stale context, plans only safe no-overwrite actions, and repairs the validator-reported output.",
  "language": "en",
  "freshness": "local_snapshot",
  "constraints": [
    "Do not use the old broad-workflow plan as the next action.",
    "Do not overwrite AGENTS.md.",
    "Create only missing unprotected files.",
    "Keep existing valid fields unchanged during repair.",
    "Label the result as partial composition, not full project-initialization or full research-workflow validation."
  ],
  "composition_atoms": [
    "A10",
    "A9",
    "A6"
  ]
}
```

## Task Input

You are validating a partial composition only.

Context selection:
- Must-load: current roadmap says Stage 2 is next.
- Must-not-load: old plan says run another broad workflow slice.

Safe planning:
- Project snapshot has existing AGENTS.md and research/CONTEXT.md.
- Missing file is research/06_outputs/README.md.
- Protected file is AGENTS.md.
- Plan actions without overwriting protected files.

Validator repair:
- Original output: {"title":"Contract-Driven Harness"}.
- Validator feedback: add missing evidence_ids using atom-a6-e01 and keep all existing valid fields unchanged.

Return a JSON object that composes the three passing atoms in order: bounded context recall, no-overwrite action planning, and validator repair.

## Output Requirements

Return the best answer for the task in a concise, reviewable form.
