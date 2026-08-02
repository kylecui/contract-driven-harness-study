# Benchmark Run: stage-b-v51-state-transition--canonical__budget_model__G9__r2

You are completing a benchmark task. Follow the instructions for the assigned harness arm.

- Fixture: `stage-b-v51-state-transition--canonical`
- Model tier: `budget_model`
- Harness arm: `G9`
- Task type: `stage_b_v51_controlled_state_transition_macro`

## Harness Arm G9

Use the full harness packet. Obey the task spec, preserve evidence IDs for important claims, respect memory boundaries, and satisfy the output contract.

## TaskSpec

```json
{
  "task_id": "stage_b_v51_state_transition__canonical",
  "task_type": "stage_b_v51_controlled_state_transition_macro",
  "objective": "Apply one evidence-backed unknown-to-known transition while copying immutable evidence bindings and the complete gate exactly.",
  "composition_chain": [
    "B4B",
    "B4A",
    "state_transition",
    "transition_gate"
  ],
  "constraints": [
    "Use only the supplied transition event.",
    "Treat the event as fixture state, not runner authorization.",
    "Use `evidence_ids` as the only reference field.",
    "Copy every evidence-binding object exactly and in order.",
    "Move only the declared API-permission state from unknown to known.",
    "Keep branch and CI state unknown in their declared order.",
    "Remove only the matching API-permission forbidden inference.",
    "Copy the complete required transition gate exactly.",
    "Return exactly one JSON object with no extra prose."
  ],
  "success_conditions": [
    "Exact evidence-array preservation passes.",
    "Residual unknown-state vocabulary passes.",
    "The transition record and known-state item match the event.",
    "The complete gate matches the declared postcondition.",
    "The retention attestation remains complete."
  ]
}
```

## EvidenceBundle

```json
{
  "bundle_id": "stage-b-v51-state-transition--canonical_evidence_001",
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
      "claim": "Within this fixture, provider execution is explicitly approved for the state transition.",
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
    }
  ]
}
```

## MemorySlice

```json
{
  "slice_id": "stage-b-v51-state-transition--canonical_memory_001",
  "must_load": [
    "Stage B v5 smoke preserved residual state and transition semantics",
    "branch and CI state remain unknown",
    "API permission changes only through event-api-approval-001",
    "the event applies only inside this fixture"
  ],
  "must_not_load": [
    "alternative evidence fields or state vocabularies",
    "implicit branch or CI values",
    "production or full-workflow readiness claims"
  ],
  "staleness_policy": "event_driven_snapshot"
}
```

## OutputContract

```json
{
  "output_contract_id": "out_stage_b_v51_state_transition__canonical_001",
  "format": "json",
  "required_sections": [
    "state_inventory",
    "evidence_bindings",
    "transition_record",
    "transition_gate",
    "retention_attestation"
  ],
  "reference_field": "evidence_ids",
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
    "known_state_id": "network_api_approval",
    "known_state_value": "approved",
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
    "next_action": "run_targeted_state_transition_repair_smoke",
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
  "tool_trace_required": false
}
```

## Task Input

# Stage B v5.1 Controlled State Transition

Apply one supplied event to the fixed initial state.

Initial unknown state:
["current_git_branch", "ci_status", "network_api_approval"]

Initial forbidden inferences:
["do_not_infer_current_git_branch", "do_not_infer_ci_status", "do_not_infer_network_api_approval"]

Transition event:
- event_id: event-api-approval-001
- scope: fixture_only
- state_id: network_api_approval
- from_status: unknown
- to_status: approved
- evidence_ids: ["ev-09"]

Rules:
- Use `evidence_ids` as the only reference field.
- Follow `OutputContract.output_shape` exactly.
- Copy `required_evidence_bindings` exactly, including order.
- Move only `network_api_approval` from unknown to known.
- Keep the other two unknown-state and forbidden-inference values exact.
- Emit one transition record for `unknown` to `approved`.
- Copy `required_transition_gate` exactly, including `next_action`.
- Treat the event as fixture state; it does not authorize a provider call.
- Copy `required_attestation` exactly.
- Return exactly one JSON object with no Markdown fence or extra prose.

## Output Requirements

Return `json` and include these required fields/sections: `state_inventory`, `evidence_bindings`, `transition_record`, `transition_gate`, `retention_attestation`.
