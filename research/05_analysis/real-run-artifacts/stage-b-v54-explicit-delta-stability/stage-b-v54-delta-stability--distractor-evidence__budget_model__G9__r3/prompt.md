# Benchmark Run: stage-b-v54-delta-stability--distractor-evidence__budget_model__G9__r3

You are completing a benchmark task. Follow the instructions for the assigned harness arm.

- Fixture: `stage-b-v53-p2--distractor-evidence`
- Model tier: `budget_model`
- Harness arm: `G9`
- Task type: `stage_b_v53_explicit_transition_delta_ablation`

## Harness Arm G9

Use the full harness packet. Obey the task spec, preserve evidence IDs for important claims, respect memory boundaries, and satisfy the output contract.

## TaskSpec

```json
{
  "task_id": "stage_b_v53_p2__distractor_evidence",
  "task_type": "stage_b_v53_explicit_transition_delta_ablation",
  "objective": "Apply one supplied state transition while preserving exact evidence bindings, residual state, the complete gate, and the retention attestation.",
  "protocol_profile": "P2",
  "perturbation_condition": "distractor_evidence",
  "constraints": [
    "Use only the supplied fixture event.",
    "Use `evidence_ids` as the only reference field.",
    "Copy every `evidence_bindings` slot and array exactly.",
    "Execute every operation in `required_transition_delta` exactly.",
    "Copy the complete required transition gate exactly.",
    "Return exactly one JSON object with no extra prose."
  ],
  "success_conditions": [
    "Schema validity passes.",
    "Residual state exactly matches the declared result.",
    "All four evidence arrays remain exact.",
    "The transition, complete gate, and attestation remain exact."
  ]
}
```

## EvidenceBundle

```json
{
  "bundle_id": "stage-b-v53-p2--distractor-evidence_evidence_001",
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
      "claim": "Stage B v3 macros retained mixed failed cells.",
      "source": "P2-E133"
    },
    {
      "evidence_id": "ev-06",
      "type": "EXTRACTED",
      "claim": "Stage B v4 isolated smoke passed all eight runs.",
      "source": "P2-E140"
    },
    {
      "evidence_id": "ev-08",
      "type": "PROPOSED",
      "claim": "A state transition should follow a clean local gate.",
      "source": "Stage B v5 plan"
    },
    {
      "evidence_id": "ev-09",
      "type": "EXTRACTED",
      "claim": "The fixture event approves provider execution.",
      "source": "event-api-approval-001"
    },
    {
      "evidence_id": "ev-10",
      "type": "EXTRACTED",
      "claim": "Stage B v4 recomposition smoke completed four calls.",
      "source": "P2-E145"
    },
    {
      "evidence_id": "ev-11",
      "type": "EXTRACTED",
      "claim": "All four bounded recomposition outputs passed.",
      "source": "P2-E146"
    },
    {
      "evidence_id": "ev-90",
      "type": "EXTRACTED",
      "claim": "A documentation draft mentions a future dashboard.",
      "source": "unrelated-note-90"
    },
    {
      "evidence_id": "ev-91",
      "type": "AMBIGUOUS",
      "claim": "An unrelated branch may contain formatting work.",
      "source": "unrelated-note-91"
    }
  ]
}
```

## MemorySlice

```json
{
  "slice_id": "stage-b-v53-p2--distractor-evidence_memory_001",
  "must_load": [
    "branch and CI state remain unknown",
    "API permission changes only through event-api-approval-001",
    "the event applies only inside this fixture"
  ],
  "must_not_load": [
    "alternative evidence fields or state vocabularies",
    "implicit branch or CI values",
    "production readiness claims"
  ],
  "staleness_policy": "event_driven_snapshot"
}
```

## OutputContract

```json
{
  "output_contract_id": "out_stage_b_v53_p2__distractor_evidence_001",
  "format": "json",
  "required_sections": [
    "state_inventory",
    "evidence_bindings",
    "transition_record",
    "transition_gate",
    "retention_attestation"
  ],
  "reference_field": "evidence_ids",
  "protocol_profile": "P2",
  "output_shape": {
    "state_inventory": {
      "known_state": "array of {state_id, value, evidence_ids}",
      "unknown_state": "array of exact declared labels",
      "forbidden_inferences": "array of exact declared labels"
    },
    "evidence_bindings": "array of {slot_id, evidence_ids}",
    "transition_record": "{event_id, state_id, from_status, to_status, evidence_ids, applied}",
    "transition_gate": "{status, permitted_action, satisfied_prerequisite, next_action, support_slot_ids}",
    "retention_attestation": "{status, immutable_fields}"
  },
  "required_evidence_bindings": [
    {
      "slot_id": "claim_alpha",
      "evidence_ids": [
        "ev-01"
      ]
    },
    {
      "slot_id": "claim_beta",
      "evidence_ids": [
        "ev-06"
      ]
    },
    {
      "slot_id": "claim_gamma",
      "evidence_ids": [
        "ev-10",
        "ev-11"
      ]
    },
    {
      "slot_id": "claim_delta",
      "evidence_ids": [
        "ev-09"
      ]
    }
  ],
  "initial_state": {
    "known_state": [],
    "unknown_state": [
      "current_git_branch",
      "ci_status",
      "network_api_approval"
    ],
    "forbidden_inferences": [
      "do_not_infer_current_git_branch",
      "do_not_infer_ci_status",
      "do_not_infer_network_api_approval"
    ],
    "gate_status": "blocked"
  },
  "transition_event": {
    "event_id": "event-api-approval-001",
    "scope": "fixture_only",
    "state_id": "network_api_approval",
    "from_status": "unknown",
    "to_status": "approved",
    "evidence_ids": [
      "ev-09"
    ]
  },
  "required_postconditions": {
    "known_state": [
      {
        "state_id": "network_api_approval",
        "value": "approved",
        "evidence_ids": [
          "ev-09"
        ]
      }
    ],
    "residual_unknown_state": [
      "current_git_branch",
      "ci_status"
    ],
    "residual_forbidden_inferences": [
      "do_not_infer_current_git_branch",
      "do_not_infer_ci_status"
    ]
  },
  "required_transition_gate": {
    "status": "open",
    "permitted_action": "provider_execution",
    "satisfied_prerequisite": "network_api_approval",
    "next_action": "complete_stage_b_v53_explicit_transition_delta",
    "support_slot_ids": [
      "claim_alpha",
      "claim_beta",
      "claim_gamma",
      "claim_delta"
    ]
  },
  "required_attestation": {
    "status": "preserved_after_transition",
    "immutable_fields": [
      "evidence_bindings[].slot_id",
      "evidence_bindings[].evidence_ids",
      "state_inventory.unknown_state",
      "state_inventory.forbidden_inferences",
      "state_inventory.known_state[].state_id",
      "state_inventory.known_state[].evidence_ids",
      "transition_record.event_id",
      "transition_record.evidence_ids"
    ]
  },
  "editable_fields": [],
  "citation_policy": "none",
  "style_profile": "minimal_json",
  "tool_trace_required": false,
  "required_transition_delta": {
    "remove_from_unknown_state": [
      "network_api_approval"
    ],
    "remove_from_forbidden_inferences": [
      "do_not_infer_network_api_approval"
    ],
    "add_to_known_state": [
      {
        "state_id": "network_api_approval",
        "value": "approved",
        "evidence_ids": [
          "ev-09"
        ]
      }
    ],
    "preserve_unknown_state": [
      "current_git_branch",
      "ci_status"
    ],
    "preserve_forbidden_inferences": [
      "do_not_infer_current_git_branch",
      "do_not_infer_ci_status"
    ]
  }
}
```

## Task Input

# Stage B v5.3 Controlled State Transition

Protocol profile: P2
Perturbation condition: distractor-evidence

Apply the supplied fixture event to the declared initial state.

Rules:
- Use `evidence_ids` as the only reference field.
- Copy every `required_evidence_bindings` object exactly and in order.
- Execute every operation in `required_transition_delta` exactly.
- Copy `required_transition_gate` exactly, including `next_action`.
- Copy `required_attestation` exactly.
- The event has fixture-only scope and does not authorize a real tool call.
- Return exactly one JSON object with no Markdown fence or extra prose.

## Output Requirements

Return `json` and include these required fields/sections: `state_inventory`, `evidence_bindings`, `transition_record`, `transition_gate`, `retention_attestation`.
