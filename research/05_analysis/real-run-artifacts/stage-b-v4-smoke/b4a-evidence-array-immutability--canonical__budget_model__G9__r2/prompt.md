# Benchmark Run: b4a-evidence-array-immutability--canonical__budget_model__G9__r2

You are completing a benchmark task. Follow the instructions for the assigned harness arm.

- Fixture: `b4a-evidence-array-immutability--canonical`
- Model tier: `budget_model`
- Harness arm: `G9`
- Task type: `mechanism_atom`

## Harness Arm G9

Use the full harness packet. Obey the task spec, preserve evidence IDs for important claims, respect memory boundaries, and satisfy the output contract.

## TaskSpec

```json
{
  "task_id": "stage_b_v4_b4a-evidence-array-immutability--canonical",
  "task_type": "mechanism_atom",
  "objective": "Return the three declared claim slots using `evidence_ids` and preserve every immutable value exactly.",
  "constraints": [
    "Only the claim prose may be edited.",
    "Keep claim slots in the declared order.",
    "Use `evidence_ids` as the only evidence-reference field.",
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
  "bundle_id": "stage_b_v4_b4a_canonical_evidence_001",
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
  "slice_id": "stage_b_v4_b4a_canonical_memory_001",
  "must_load": [
    "the declared evidence-reference field is evidence_ids",
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
  "output_contract_id": "out_stage_b_v4_b4a_canonical_001",
  "format": "json",
  "required_sections": [
    "grounded_claims",
    "immutability_check"
  ],
  "reference_field": "evidence_ids",
  "editable_fields": [
    "grounded_claims[].claim"
  ],
  "immutable_fields": [
    "grounded_claims[].slot_id",
    "grounded_claims[].evidence_ids"
  ],
  "exact_output_template": {
    "grounded_claims": [
      {
        "slot_id": "claim_alpha",
        "claim": "The local gate passed before provider execution.",
        "evidence_ids": [
          "ev-01"
        ]
      },
      {
        "slot_id": "claim_beta",
        "claim": "The proposed stressor remains blocked pending a targeted smoke.",
        "evidence_ids": [
          "ev-06"
        ]
      },
      {
        "slot_id": "claim_gamma",
        "claim": "The next decision must preserve both the method rule and the backlog state.",
        "evidence_ids": [
          "ev-07",
          "ev-08"
        ]
      }
    ],
    "immutability_check": {
      "status": "preserved",
      "immutable_fields": [
        "slot_id",
        "evidence_ids"
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
- `slot_id` and `evidence_ids` are immutable.
- Array order and multiplicity are part of the contract.
- Do not merge slots, add support, remove support, or rename fields.
- Return exactly one JSON object.

## Output Requirements

Return `json` and include these required fields/sections: `grounded_claims`, `immutability_check`.
