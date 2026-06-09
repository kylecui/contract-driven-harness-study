# Benchmark Run: a8r-evidence-type-rules__budget_model__G0__r1

You are completing a benchmark task. Follow the instructions for the assigned harness arm.

- Fixture: `a8r-evidence-type-rules`
- Model tier: `budget_model`
- Harness arm: `G0`
- Task type: `mechanism_atom`

## Harness Arm G0

Use only the task input below. Do not assume extra schemas, memory, tools, or evidence beyond what is present in the task text.

## TaskSpec

```json
{
  "task_id": "stage7r_a8r_evidence_type_rules",
  "task_type": "mechanism_atom",
  "objective": "Classify each item into exactly one evidence type using the supplied rules.",
  "constraints": [
    "Use only EXTRACTED, INFERRED, AMBIGUOUS, PROPOSED.",
    "Classify each item exactly once.",
    "Do not resolve ambiguous items as facts."
  ],
  "success_conditions": [
    "I1 is EXTRACTED.",
    "I2 is INFERRED.",
    "I3 and I4 are PROPOSED.",
    "I5 is AMBIGUOUS."
  ]
}
```

## Task Input

# Stage7r A8R Input: Evidence Type Rules

Classify each item into exactly one evidence type.

Rules:
- `EXTRACTED`: directly observed from an artifact or source.
- `INFERRED`: derived by comparing two or more observed facts.
- `AMBIGUOUS`: conflicting or underdetermined evidence.
- `PROPOSED`: recommendation, hypothesis, or next action.

Items:
- `I1`: The Stage7p v2 adapter completed 6/6 runs with 0 warnings.
- `I2`: Because weak-model G0 failed and weak-model G8/G9 passed, explicit obligation retention likely repaired the weak model failure mode.
- `I3`: A2/A3/A5/A7 still require redesign before full Stage7.
- `I4`: We should run a Stage7r smoke after local golden/bad gates pass.
- `I5`: One note says gap compression is universal, while another note says it is conditional.

## Output Requirements

Return the best answer for the task in a concise, reviewable form.
