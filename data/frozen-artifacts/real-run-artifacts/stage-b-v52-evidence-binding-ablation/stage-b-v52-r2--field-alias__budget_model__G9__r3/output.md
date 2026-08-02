{
  "state_inventory": {
    "known_state": [
      {
        "state_id": "network_api_approval",
        "value": "approved",
        "source_references": [
          "ev-09"
        ]
      }
    ],
    "unknown_state": [
      "current_git_branch",
      "ci_status"
    ],
    "forbidden_inferences": [
      "do_not_infer_current_git_branch",
      "do_not_infer_ci_status"
    ]
  },
  "evidence_bindings": [
    {
      "slot_id": "claim_alpha",
      "source_references": [
        "ev-01"
      ]
    },
    {
      "slot_id": "claim_beta",
      "source_references": [
        "ev-06"
      ]
    },
    {
      "slot_id": "claim_gamma",
      "source_references": [
        "ev-10",
        "ev-11"
      ]
    },
    {
      "slot_id": "claim_delta",
      "source_references": [
        "ev-09"
      ]
    }
  ],
  "transition_record": {
    "event_id": "event-api-approval-001",
    "state_id": "network_api_approval",
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
    "satisfied_prerequisite": "network_api_approval",
    "next_action": "complete_stage_b_v52_evidence_binding_ablation",
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
      "evidence_bindings[].slot_id",
      "evidence_bindings[].source_references",
      "state_inventory.unknown_state",
      "state_inventory.forbidden_inferences",
      "state_inventory.known_state[].state_id",
      "state_inventory.known_state[].source_references",
      "transition_record.event_id",
      "transition_record.source_references"
    ]
  }
}