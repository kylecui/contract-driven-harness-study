{
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
      "claim": "Stage B v4-local passed all local gates.",
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
      "claim": "Provider execution follows only after the recomposition local gate.",
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
}