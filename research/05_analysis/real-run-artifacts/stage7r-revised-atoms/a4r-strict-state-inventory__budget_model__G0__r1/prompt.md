# Benchmark Run: a4r-strict-state-inventory__budget_model__G0__r1

You are completing a benchmark task. Follow the instructions for the assigned harness arm.

- Fixture: `a4r-strict-state-inventory`
- Model tier: `budget_model`
- Harness arm: `G0`
- Task type: `mechanism_atom`

## Harness Arm G0

Use only the task input below. Do not assume extra schemas, memory, tools, or evidence beyond what is present in the task text.

## TaskSpec

```json
{
  "task_id": "stage7r_a4r_strict_state_inventory",
  "task_type": "mechanism_atom",
  "objective": "Inventory known and unknown workspace state without inference.",
  "constraints": [
    "Use only the supplied fixed snapshot.",
    "Mark unstated values as unknown.",
    "Do not infer CI status, Git branch, or network approval."
  ],
  "success_conditions": [
    "Known state contains only supplied facts.",
    "Unknown state includes Git branch, CI status, and network approval.",
    "Forbidden inferences are explicit."
  ]
}
```

## Task Input

# Stage7r A4R Input: Strict State Inventory

You are given a fixed workspace snapshot:

- `AGENTS.md` is present.
- `tasks/backlog.md` records Stage7p v2 as complete and Stage7r as pending.
- `research/05_analysis/stage7p-v2-a10-a9-a6-evaluation.md` exists.

The snapshot does not state the current Git branch, CI status, or whether the user has approved network execution.

Return only known state, unknown state, and forbidden inferences.

## Output Requirements

Return the best answer for the task in a concise, reviewable form.
