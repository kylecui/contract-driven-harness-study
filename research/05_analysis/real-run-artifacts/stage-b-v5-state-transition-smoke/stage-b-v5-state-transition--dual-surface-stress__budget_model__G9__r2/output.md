{
  "state_inventory": {
    "known_state": [
      {
        "state_id": "permission_to_use_external_model_api",
        "value": "approved",
        "source_references": [
          "ev-09"
        ]
      }
    ],
    "unknown_state": [
      "branch_currently_checked_out",
      "continuous_integration_result"
    ],
    "forbidden_inferences": [
      "do_not_guess_branch_currently_checked_out",
      "do_not_guess_continuous_integration_result"
    ]
  },
  "grounded_claims": [
    {
      "slot_id": "claim_alpha",
      "claim": "Stage B v4-local passed all local gates.",
      "source_references": [
        "ev-01"
      ]
    },
    {
      "slot_id": "claim_beta",
      "claim": "A state transition should follow a clean local gate.",
      "source_references": [
        "ev-06"
      ]
    },
    {
      "slot_id": "claim_gamma",
      "claim": "Stage B v4 recomposition smoke completed four calls.",
      "source_references": [
        "ev-10"
      ]
    },
    {
      "slot_id": "claim_delta",
      "claim": "Within this fixture, provider execution is explicitly approved for the state transition.",
      "source_references": [
        "ev-09"
      ]
    }
  ],
  "transition_record": {
    "event_id": "event-api-approval-001",
    "state_id": "permission_to_use_external_model_api",
    "from_status": "unknown",
    "to_status": "approved",
    "source_references": [
      "ev-09"
    ],
    "applied": true
  },
  "transition_gate": {
    "status": "open",
    "permitted_action": "provider_execution",
    "satisfied_prerequisite": "permission_to_use_external_model_api",
    "next_action": "provider_execution",
    "support_slot_ids": [
      "claim_alpha",
      "claim_beta",
      "claim_gamma",
      "claim_delta"
    ]
  },
  "retention_attestation": {
    "status": "preserved_after_transition",
    "immutable_fields": [
      "grounded_claims[].slot_id",
      "grounded_claims[].source_references",
      "state_inventory.unknown_state",
      "state_inventory.forbidden_inferences",
      "state_inventory.known_state[].state_id",
      "state_inventory.known_state[].source_references",
      "transition_record.event_id",
      "transition_record.source_references"
    ]
  }
}