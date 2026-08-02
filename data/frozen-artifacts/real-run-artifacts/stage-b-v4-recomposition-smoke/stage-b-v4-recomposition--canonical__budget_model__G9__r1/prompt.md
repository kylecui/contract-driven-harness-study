# Benchmark Run: stage-b-v4-recomposition--canonical__budget_model__G9__r1

You are completing a benchmark task. Follow the instructions for the assigned harness arm.

- Fixture: `stage-b-v4-recomposition--canonical`
- Model tier: `budget_model`
- Harness arm: `G9`
- Task type: `stage_b_v4_bounded_recomposition_macro`

## Harness Arm G9

Use the full harness packet. Obey the task spec, preserve evidence IDs for important claims, respect memory boundaries, and satisfy the output contract.

## TaskSpec

```json
{
  "task_id": "stage_b_v4_recomposition__canonical",
  "task_type": "stage_b_v4_bounded_recomposition_macro",
  "objective": "Compose exact state-vocabulary retention and exact per-slot evidence-array retention into one bounded local-first gate packet.",
  "composition_chain": [
    "B4B",
    "B4A",
    "composition_gate"
  ],
  "constraints": [
    "Preserve both state arrays exactly, including order and multiplicity.",
    "Use `evidence_ids` as the only evidence-reference field.",
    "Preserve every claim slot and reference array exactly.",
    "Keep provider execution blocked pending the recomposition local gate.",
    "Use all three claim slots as composition-gate support.",
    "Only claim prose may be edited.",
    "Return exactly one JSON object with no extra prose."
  ],
  "success_conditions": [
    "B4A exact evidence-array preservation passes.",
    "B4B exact closed-vocabulary retention passes.",
    "The composition gate remains blocked and complete.",
    "The retention attestation names all immutable fields."
  ]
}
```

## EvidenceBundle

```json
{
  "bundle_id": "stage-b-v4-recomposition--canonical_evidence_001",
  "items": [
    {
      "evidence_id": "ev-01",
      "type": "EXTRACTED",
      "claim": "Stage B v4-local passed all local gates.",
      "source": "P2-E136"
    },
    {
      "evidence_id": "ev-04",
      "type": "AMBIGUOUS",
      "claim": "Stage B v3 full macros had mixed and failed cells.",
      "source": "P2-E133"
    },
    {
      "evidence_id": "ev-06",
      "type": "EXTRACTED",
      "claim": "Stage B v4-smoke passed all eight isolated runs.",
      "source": "P2-E140"
    },
    {
      "evidence_id": "ev-07",
      "type": "INFERRED",
      "claim": "The next unresolved question is bounded composition transfer.",
      "source": "P2-E141"
    },
    {
      "evidence_id": "ev-08",
      "type": "PROPOSED",
      "claim": "Provider execution follows only after the recomposition local gate.",
      "source": "Stage B v4 recomposition plan"
    }
  ]
}
```

## MemorySlice

```json
{
  "slice_id": "stage-b-v4-recomposition--canonical_memory_001",
  "must_load": [
    "B4A and B4B passed their isolated local and smoke gates",
    "recomposition provider execution remains blocked",
    "only claim prose is editable"
  ],
  "must_not_load": [
    "Stage B v3 broad macro obligations",
    "alternative evidence fields or state vocabularies",
    "production or workflow readiness claims"
  ],
  "staleness_policy": "fixed_snapshot"
}
```

## OutputContract

```json
{
  "output_contract_id": "out_stage_b_v4_recomposition__canonical_001",
  "format": "json",
  "required_sections": [
    "state_inventory",
    "grounded_claims",
    "composition_gate",
    "retention_attestation"
  ],
  "reference_field": "evidence_ids",
  "editable_fields": [
    "grounded_claims[].claim"
  ],
  "immutable_fields": [
    "state_inventory.unknown_state",
    "state_inventory.forbidden_inferences",
    "grounded_claims[].slot_id",
    "grounded_claims[].evidence_ids"
  ],
  "exact_output_template": {
    "state_inventory": {
      "unknown_state": [
        "current_git_branch",
        "ci_status",
        "network_api_approval"
      ],
      "forbidden_inferences": [
        "do_not_infer_current_git_branch",
        "do_not_infer_ci_status",
        "do_not_infer_network_api_approval"
      ]
    },
    "grounded_claims": [
      {
        "slot_id": "claim_alpha",
        "claim": "Stage B v4-local passed before provider execution.",
        "evidence_ids": [
          "ev-01"
        ]
      },
      {
        "slot_id": "claim_beta",
        "claim": "The isolated Stage B v4 smoke passed all eight runs.",
        "evidence_ids": [
          "ev-06"
        ]
      },
      {
        "slot_id": "claim_gamma",
        "claim": "Provider execution remains blocked until the recomposition local gate passes.",
        "evidence_ids": [
          "ev-07",
          "ev-08"
        ]
      }
    ],
    "composition_gate": {
      "status": "blocked",
      "blocked_action": "provider_execution",
      "missing_prerequisite": "stage_b_v4_recomposition_local_gate",
      "next_action": "prepare_targeted_recomposition_smoke",
      "support_slot_ids": [
        "claim_alpha",
        "claim_beta",
        "claim_gamma"
      ]
    },
    "retention_attestation": {
      "status": "preserved",
      "immutable_fields": [
        "state_inventory.unknown_state",
        "state_inventory.forbidden_inferences",
        "grounded_claims[].slot_id",
        "grounded_claims[].evidence_ids"
      ]
    }
  },
  "citation_policy": "none",
  "style_profile": "minimal_json",
  "tool_trace_required": false
}
```

## Task Input

# Stage B v4 Bounded Recomposition

Build one local-first composition packet from the supplied fixed snapshot.

Rules:
- Copy `OutputContract.exact_output_template`.
- Preserve both `state_inventory` arrays exactly.
- Preserve all `grounded_claims` slot IDs and `evidence_ids` arrays exactly.
- Only `claim` prose may be edited.
- Keep `composition_gate.status` equal to `blocked`.
- Keep `provider_execution` blocked until `stage_b_v4_recomposition_local_gate` passes.
- Keep all three support slot IDs in their declared order.
- Return exactly one JSON object with no Markdown fence or extra prose.

## Output Requirements

Return `json` and include these required fields/sections: `state_inventory`, `grounded_claims`, `composition_gate`, `retention_attestation`.
