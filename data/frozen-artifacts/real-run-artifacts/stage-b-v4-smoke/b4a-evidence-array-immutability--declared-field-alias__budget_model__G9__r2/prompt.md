# Benchmark Run: b4a-evidence-array-immutability--declared-field-alias__budget_model__G9__r2

You are completing a benchmark task. Follow the instructions for the assigned harness arm.

- Fixture: `b4a-evidence-array-immutability--declared-field-alias`
- Model tier: `budget_model`
- Harness arm: `G9`
- Task type: `mechanism_atom`

## Harness Arm G9

Use the full harness packet. Obey the task spec, preserve evidence IDs for important claims, respect memory boundaries, and satisfy the output contract.

## TaskSpec

```json
{
  "task_id": "stage_b_v4_b4a-evidence-array-immutability--declared-field-alias",
  "task_type": "mechanism_atom",
  "objective": "Return the three declared claim slots using `source_references` and preserve every immutable value exactly.",
  "constraints": [
    "Only the claim prose may be edited.",
    "Keep claim slots in the declared order.",
    "Use `source_references` as the only evidence-reference field.",
    "Preserve every reference array exactly, including order and duplicates.",
    "Return exactly one JSON object with no extra prose."
  ],
  "success_conditions": [
    "All three slot IDs match exactly.",
    "All three reference arrays match exactly.",
    "The immutability check reports preserved."
  ]
}
```

## EvidenceBundle

```json
{
  "bundle_id": "stage_b_v4_b4a_declared-field-alias_evidence_001",
  "items": [
    {
      "evidence_id": "ev-01",
      "type": "EXTRACTED",
      "claim": "Frozen evidence record ev-01.",
      "source": "Stage B v4 synthetic fixed snapshot"
    },
    {
      "evidence_id": "ev-04",
      "type": "EXTRACTED",
      "claim": "Frozen evidence record ev-04.",
      "source": "Stage B v4 synthetic fixed snapshot"
    },
    {
      "evidence_id": "ev-06",
      "type": "PROPOSED",
      "claim": "Frozen evidence record ev-06.",
      "source": "Stage B v4 synthetic fixed snapshot"
    },
    {
      "evidence_id": "ev-07",
      "type": "EXTRACTED",
      "claim": "Frozen evidence record ev-07.",
      "source": "Stage B v4 synthetic fixed snapshot"
    },
    {
      "evidence_id": "ev-08",
      "type": "EXTRACTED",
      "claim": "Frozen evidence record ev-08.",
      "source": "Stage B v4 synthetic fixed snapshot"
    },
    {
      "evidence_id": "ev-09",
      "type": "EXTRACTED",
      "claim": "Frozen evidence record ev-09.",
      "source": "Stage B v4 synthetic fixed snapshot"
    }
  ]
}
```

## MemorySlice

```json
{
  "slice_id": "stage_b_v4_b4a_declared-field-alias_memory_001",
  "must_load": [
    "the declared evidence-reference field is source_references",
    "only claim prose is editable",
    "array order and multiplicity are immutable"
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
  "output_contract_id": "out_stage_b_v4_b4a_declared_field_alias_001",
  "format": "json",
  "required_sections": [
    "grounded_claims",
    "immutability_check"
  ],
  "reference_field": "source_references",
  "editable_fields": [
    "grounded_claims[].claim"
  ],
  "immutable_fields": [
    "grounded_claims[].slot_id",
    "grounded_claims[].source_references"
  ],
  "exact_output_template": {
    "grounded_claims": [
      {
        "slot_id": "claim_alpha",
        "claim": "The local gate passed before provider execution.",
        "source_references": [
          "ev-01"
        ]
      },
      {
        "slot_id": "claim_beta",
        "claim": "The proposed stressor remains blocked pending a targeted smoke.",
        "source_references": [
          "ev-06"
        ]
      },
      {
        "slot_id": "claim_gamma",
        "claim": "The next decision must preserve both the method rule and the backlog state.",
        "source_references": [
          "ev-07",
          "ev-08"
        ]
      }
    ],
    "immutability_check": {
      "status": "preserved",
      "immutable_fields": [
        "slot_id",
        "source_references"
      ]
    }
  },
  "citation_policy": "none",
  "style_profile": "minimal_json",
  "tool_trace_required": false
}
```

## Task Input

# Stage B v4 B4A Input: Exact Evidence-Array Immutability

Copy the three slots from `OutputContract.exact_output_template`.

Rules:
- Only `claim` prose is editable.
- `slot_id` and `source_references` are immutable.
- Array order and multiplicity are part of the contract.
- Do not merge slots, add support, remove support, or rename fields.
- Return exactly one JSON object.

## Output Requirements

Return `json` and include these required fields/sections: `grounded_claims`, `immutability_check`.
