# Benchmark Run: a7r-enumerated-claim-decision__strong_model__G0__r1

You are completing a benchmark task. Follow the instructions for the assigned harness arm.

- Fixture: `a7r-enumerated-claim-decision`
- Model tier: `strong_model`
- Harness arm: `G0`
- Task type: `mechanism_atom`

## Harness Arm G0

Use only the task input below. Do not assume extra schemas, memory, tools, or evidence beyond what is present in the task text.

## TaskSpec

```json
{
  "task_id": "stage7r_a7r_enumerated_claim_decision",
  "task_type": "mechanism_atom",
  "objective": "Select exactly one enumerated claim option using explicit evidence and rules.",
  "constraints": [
    "Return selected_option_id as one of C1, C2, C3.",
    "Reject unsupported or overbroad options.",
    "Include a decision_trace with at least two evidence-linked steps."
  ],
  "success_conditions": [
    "selected_option_id is C2.",
    "C1 and C3 are rejected with reasons.",
    "Decision trace cites supplied evidence IDs."
  ]
}
```

## Task Input

# Stage7r A7R Input: Enumerated Claim Decision

Choose exactly one claim option for the paper contribution statement.

Options:
- `C1`: Harness universally closes the performance gap between strong and weak models.
- `C2`: Harness improves absolute contract adherence and enables weak models on mechanism-bound tasks.
- `C3`: Harness mainly improves prose style.

Evidence:
- `atom-a7r-e01`: Weak-model G8/G9 task success improved from 0.000 to 0.667 in Stage7p v2 composition retention.
- `atom-a7r-e02`: Gap compression was observed in some metrics but is not universal across all tasks.
- `atom-a7r-e03`: No evaluation measured prose style.

Decision rule:
- Reject universal claims unless evidence covers all tested task classes.
- Reject claims about unmeasured outcomes.
- Prefer the most specific claim supported by the supplied evidence.

## Output Requirements

Return the best answer for the task in a concise, reviewable form.
