# Benchmark Run: a7r1-rejection-trace-completeness__budget_model__G8__r1

You are completing a benchmark task. Follow the instructions for the assigned harness arm.

- Fixture: `a7r1-rejection-trace-completeness`
- Model tier: `budget_model`
- Harness arm: `G8`
- Task type: `mechanism_atom`

## Harness Arm G8

Use the harness layers provided in this packet.

## TaskSpec

```json
{
  "task_id": "stage7r1_a7r1_rejection_trace_completeness",
  "task_type": "mechanism_atom",
  "objective": "Select exactly one enumerated claim option and provide complete evidence-linked trace coverage.",
  "constraints": [
    "Return selected_option_id as one of C1, C2, C3.",
    "Use rejected_options, not a bare rejected_option_ids list.",
    "Every rejected option must include evidence_ids.",
    "decision_trace must include C2 support, C1 rejection, and C3 rejection."
  ],
  "success_conditions": [
    "selected_option_id is C2.",
    "C1 and C3 are rejected with evidence IDs.",
    "decision_trace cites atom-a7r1-e01, atom-a7r1-e02, and atom-a7r1-e03."
  ]
}
```

## EvidenceBundle

```json
{
  "bundle_id": "stage7r1_a7r1_evidence_001",
  "items": [
    {
      "evidence_id": "atom-a7r1-e01",
      "type": "EXTRACTED",
      "claim": "Weak-model G8/G9 task success improved from 0.000 to 0.667 in Stage7p v2 composition retention.",
      "source": "stage7r input"
    },
    {
      "evidence_id": "atom-a7r1-e02",
      "type": "EXTRACTED",
      "claim": "Gap compression is not universal across all tasks.",
      "source": "stage7r input"
    },
    {
      "evidence_id": "atom-a7r1-e03",
      "type": "EXTRACTED",
      "claim": "No evaluation measured prose style.",
      "source": "stage7r input"
    }
  ]
}
```

## MemorySlice

```json
{
  "slice_id": "stage7r1_a7r1_memory_001",
  "must_load": [
    "C1 is universal gap closure",
    "C2 is weak-model enablement on mechanism-bound tasks",
    "C3 is prose style improvement",
    "C3 must be rejected with atom-a7r1-e03"
  ],
  "must_not_load": [
    "unlisted contribution claims",
    "unmeasured style outcomes",
    "rejection without evidence"
  ],
  "staleness_policy": "fixed_snapshot"
}
```

## OutputContract

```json
{
  "output_contract_id": "out_stage7r1_a7r1_rejection_trace_completeness_001",
  "format": "json",
  "required_sections": [
    "selected_option_id",
    "selected_claim",
    "rejected_options",
    "decision_trace",
    "evidence_ids"
  ],
  "citation_policy": "selected_and_rejected_options",
  "style_profile": "minimal_json",
  "tool_trace_required": false,
  "schema_notes": {
    "rejected_options_item": {
      "option_id": "C1|C3",
      "reason": "string",
      "evidence_ids": [
        "evidence_id"
      ]
    },
    "decision_trace_requirement": "include evidence-linked support/rejection step for C2, C1, and C3"
  }
}
```

## Task Input

# Stage7r.1 A7R1 Input: Rejection Trace Completeness

Choose exactly one claim option for the paper contribution statement.

Options:
- `C1`: Harness universally closes the performance gap between strong and weak models.
- `C2`: Harness improves absolute contract adherence and enables weak models on mechanism-bound tasks.
- `C3`: Harness mainly improves prose style.

Evidence:
- `atom-a7r1-e01`: Weak-model G8/G9 task success improved from 0.000 to 0.667 in Stage7p v2 composition retention.
- `atom-a7r1-e02`: Gap compression was observed in some metrics but is not universal across all tasks.
- `atom-a7r1-e03`: No evaluation measured prose style.

Rules:
- Select exactly one option ID.
- Every rejected option must be represented as an object with `option_id`, `reason`, and `evidence_ids`.
- The decision trace must include at least one evidence-linked step for the selected option and one evidence-linked step for every rejected option.
- Reject universal claims unless evidence covers all tested task classes.
- Reject claims about unmeasured outcomes.

## Output Requirements

Return `json` and include these required fields/sections: `selected_option_id`, `selected_claim`, `rejected_options`, `decision_trace`, `evidence_ids`.
Citation policy: `selected_and_rejected_options`.
