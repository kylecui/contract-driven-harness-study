# Benchmark Run: b4b-closed-vocabulary-retention--paraphrased__budget_model__G9__r2

You are completing a benchmark task. Follow the instructions for the assigned harness arm.

- Fixture: `b4b-closed-vocabulary-retention--paraphrased`
- Model tier: `budget_model`
- Harness arm: `G9`
- Task type: `mechanism_atom`

## Harness Arm G9

Use the full harness packet. Obey the task spec, preserve evidence IDs for important claims, respect memory boundaries, and satisfy the output contract.

## TaskSpec

```json
{
  "task_id": "stage_b_v4_b4b-closed-vocabulary-retention--paraphrased",
  "task_type": "mechanism_atom",
  "objective": "Copy the two declared closed-vocabulary arrays without normalization.",
  "constraints": [
    "Use only the labels declared in the output template.",
    "Preserve value order and multiplicity.",
    "Do not replace guess with infer or infer with guess.",
    "Do not mix canonical and paraphrased labels.",
    "Return exactly one JSON object with no extra prose."
  ],
  "success_conditions": [
    "unknown_state exactly matches the declared array.",
    "forbidden_inferences exactly matches the declared array.",
    "retention_status is preserved."
  ]
}
```

## EvidenceBundle

```json
{
  "bundle_id": "stage_b_v4_b4b_paraphrased_evidence_001",
  "items": []
}
```

## MemorySlice

```json
{
  "slice_id": "stage_b_v4_b4b_paraphrased_memory_001",
  "must_load": [
    "state labels are closed-vocabulary protocol tokens",
    "semantic similarity does not authorize substitution",
    "value order and multiplicity are immutable"
  ],
  "must_not_load": [
    "alternative field names or value aliases",
    "undeclared evidence IDs or state labels"
  ],
  "staleness_policy": "fixed_snapshot"
}
```

## OutputContract

```json
{
  "output_contract_id": "out_stage_b_v4_b4b_paraphrased_001",
  "format": "json",
  "required_sections": [
    "state_inventory",
    "retention_status"
  ],
  "required_nested_fields": {
    "state_inventory": [
      "unknown_state",
      "forbidden_inferences"
    ]
  },
  "closed_vocabularies": {
    "state_inventory.unknown_state": [
      "branch_currently_checked_out",
      "continuous_integration_result",
      "permission_to_use_external_model_api"
    ],
    "state_inventory.forbidden_inferences": [
      "do_not_guess_branch_currently_checked_out",
      "do_not_guess_continuous_integration_result",
      "do_not_guess_permission_to_use_external_model_api"
    ],
    "retention_status": [
      "preserved"
    ]
  },
  "exact_output_template": {
    "state_inventory": {
      "unknown_state": [
        "branch_currently_checked_out",
        "continuous_integration_result",
        "permission_to_use_external_model_api"
      ],
      "forbidden_inferences": [
        "do_not_guess_branch_currently_checked_out",
        "do_not_guess_continuous_integration_result",
        "do_not_guess_permission_to_use_external_model_api"
      ]
    },
    "retention_status": "preserved"
  },
  "citation_policy": "none",
  "style_profile": "minimal_json",
  "tool_trace_required": false
}
```

## Task Input

# Stage B v4 B4B Input: Exact Closed-Vocabulary Retention

Copy both arrays from `OutputContract.exact_output_template`.

Rules:
- The labels are protocol tokens, not prose.
- Preserve exact spelling, order, and multiplicity.
- Do not normalize a token to a familiar synonym.
- Do not add or omit a token.
- Return exactly one JSON object.

## Output Requirements

Return `json` and include these required fields/sections: `state_inventory`, `retention_status`.
