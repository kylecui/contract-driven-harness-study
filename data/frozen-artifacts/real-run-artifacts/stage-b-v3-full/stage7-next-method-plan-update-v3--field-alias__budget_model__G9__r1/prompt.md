# Benchmark Run: stage7-next-method-plan-update-v3--field-alias__budget_model__G9__r1

You are completing a benchmark task. Follow the instructions for the assigned harness arm.

- Fixture: `stage7-next-method-plan-update-v3--field-alias`
- Model tier: `budget_model`
- Harness arm: `G9`
- Task type: `stage7_next_evidence_bound_macro`

## Harness Arm G9

Use the full harness packet. Obey the task spec, preserve evidence IDs for important claims, respect memory boundaries, and satisfy the output contract.

## TaskSpec

```json
{
  "task_id": "stage7_next_method_plan_update",
  "task_type": "stage7_next_evidence_bound_macro",
  "objective": "Compose the passing Stage 7e v4 obligations into a bounded evidence-bound method-plan update packet.",
  "composition_chain": [
    "A4R",
    "A2R1",
    "A8R",
    "A7R1",
    "A5R",
    "trace_gate_retention_contract",
    "state_retention_contract",
    "known_state_provenance_contract",
    "method_plan_update_contract"
  ],
  "constraints": [
    "Use only supplied workspace snapshot and evidence items.",
    "Do not infer Git branch, CI status, or network/API approval.",
    "state_inventory.known_state must explicitly include stage7e_v4_macro_passed, claim_boundary_updated, methodology_outline_updated, and backlog_stage7next_open.",
    "Every known_state item must carry source_references.",
    "state_inventory.unknown_state must explicitly include current_git_branch, ci_status, and network_api_approval.",
    "state_inventory.forbidden_inferences must explicitly include do_not_infer_current_git_branch, do_not_infer_ci_status, and do_not_infer_network_api_approval.",
    "Exclude stale context from the decision.",
    "Bind every grounded claim to claim-level evidence IDs.",
    "Classify evidence into EXTRACTED, INFERRED, AMBIGUOUS, or PROPOSED.",
    "Select exactly one candidate claim.",
    "Reject overbroad or unsupported claims with evidence-linked reasons.",
    "Every decision_trace item must be an object with option_id, decision, source_references, and carried_obligations.",
    "The stage_gate must explicitly block real_model_execution, broader_workflow_expansion, and production_or_universal_claim.",
    "The stage_gate must explicitly list stage7_next_local_gate and stage7_next_targeted_smoke as missing prerequisites.",
    "The method_plan_update section must name the selected next macro, admission criteria, local gates, real-model gate, and non-claims.",
    "Carry forward negative obligations across selected_claim, rejected_options, decision_trace, stage_gate, method_plan_update, and carried_obligations."
  ],
  "success_conditions": [
    "Known-state provenance explicitly preserves the four required state IDs with source references.",
    "Unknown-state inventory explicitly preserves the three unknown state fields.",
    "Forbidden inferences explicitly block the three unknown state fields.",
    "Grounded claims have claim-level source references.",
    "Production readiness, universal gap closure, and immediate broader workflow expansion are not grounded.",
    "Evidence typing includes EXTRACTED, INFERRED, AMBIGUOUS, and PROPOSED where appropriate.",
    "Selected claim is C2.",
    "Rejected options include C1 and C3 with source references.",
    "Decision trace covers C2 support, C1 rejection, and C3 rejection as structured objects.",
    "Stage gate blocks all three blocked outputs and lists both Stage 7-next prerequisites.",
    "Method-plan update preserves macro boundaries and local-first admission criteria.",
    "Carried obligations preserve stale-context exclusion and unsupported-production-readiness exclusion."
  ],
  "perturbation_condition": "field-alias",
  "base_macro": "stage7-next-method-plan-update",
  "protocol_version": "stage_b_v3_full",
  "repair_confirmation": true,
  "fixture_id": "stage7-next-method-plan-update-v3--field-alias",
  "mechanism_atoms": [
    "hierarchical_output_shape_preservation",
    "explicit_grounded_claim_slot_preservation"
  ]
}
```

## EvidenceBundle

```json
{
  "bundle_id": "stage7_next_method_plan_update_evidence_bundle_001",
  "items": [
    {
      "evidence_id": "stage7next-e01",
      "type": "EXTRACTED",
      "claim": "Stage 7e v4 completed a targeted low-cost-model G8/G9 smoke with 4/4 completed and passed runs after retrying one provider timeout.",
      "source": "research/05_analysis/stage-reports/stage-7e-v4-known-state-provenance-summary.md"
    },
    {
      "evidence_id": "stage7next-e02",
      "type": "INFERRED",
      "claim": "Stage 7e v1-v4 supports a mechanism-first repair loop for fixed evidence-decision macros, not broad workflow readiness.",
      "source": "research/03_evidence/evidence-ledger.jsonl#P2-E69"
    },
    {
      "evidence_id": "stage7next-e03",
      "type": "AMBIGUOUS",
      "claim": "Provider execution stability remains a practical uncertainty because Stage 7e v4 required a timeout retry and one truncated retry before success.",
      "source": "research/05_analysis/stage7e-v4-known-state-provenance-decision-evaluation-final-v2.md"
    },
    {
      "evidence_id": "stage7next-e04",
      "type": "EXTRACTED",
      "claim": "The claim-boundary memo was updated to separate task-slice claims, mechanism-composition claims, and unsupported claims.",
      "source": "research/05_analysis/contract-driven-claim-boundary-memo.md"
    },
    {
      "evidence_id": "stage7next-e05",
      "type": "EXTRACTED",
      "claim": "No supplied evidence supports production readiness, universal model-gap closure, or immediate full workflow expansion.",
      "source": "research/05_analysis/contract-driven-claim-boundary-memo.md"
    },
    {
      "evidence_id": "stage7next-e06",
      "type": "PROPOSED",
      "claim": "The next bounded macro should be an evidence-bound method-plan update that reuses Stage 7e v4 obligations before any real-model execution.",
      "source": "research/05_analysis/contract-driven-methodology-outline.md"
    },
    {
      "evidence_id": "stage7next-e07",
      "type": "EXTRACTED",
      "claim": "The methodology outline defines next macro admission criteria: reuse Stage 7e v4 obligations, add at most one new stressor, run local golden/bad gates first, and declare non-claims.",
      "source": "research/05_analysis/contract-driven-methodology-outline.md"
    },
    {
      "evidence_id": "stage7next-e08",
      "type": "EXTRACTED",
      "claim": "The backlog marks Stage 7-next as open and keeps full project initialization and full research workflow blocked until the next macro passes local gates and a targeted real-model slice.",
      "source": "tasks/backlog.md"
    }
  ]
}
```

## MemorySlice

```json
{
  "slice_id": "stage7_next_method_plan_update_memory_001",
  "must_load": [
    "Stage 7e v4 low-cost-model G8/G9 passed 4/4 after retry",
    "claim-boundary memo has been updated",
    "methodology outline has been created",
    "Stage 7-next is open in the backlog",
    "full project initialization remains blocked",
    "full research workflow remains blocked",
    "current Git branch is unknown",
    "CI status is unknown",
    "network/API approval is unknown"
  ],
  "must_not_load": [
    "old universal gap-closure note",
    "old production-readiness note",
    "current Git branch value",
    "CI status value",
    "network/API approval value"
  ],
  "staleness_policy": "fixed_snapshot_with_explicit_exclusion"
}
```

## OutputContract

```json
{
  "output_contract_id": "out_stage7_next_method_plan_update_001_stage_b_v3_full",
  "format": "json",
  "retention_contract_required": true,
  "state_retention_contract_required": true,
  "known_state_retention_contract_required": true,
  "required_sections": [
    "state_inventory",
    "grounded_claims",
    "unsupported_claims",
    "typed_evidence",
    "selected_claim",
    "rejected_options",
    "decision_trace",
    "stage_gate",
    "method_plan_update",
    "carried_obligations"
  ],
  "required_nested_fields": {
    "state_inventory": [
      "known_state",
      "unknown_state",
      "forbidden_inferences"
    ],
    "grounded_claims": [
      "claim",
      "source_references"
    ],
    "unsupported_claims": [
      "claim",
      "reason"
    ],
    "selected_claim": [
      "option_id",
      "claim",
      "source_references"
    ],
    "rejected_options": [
      "option_id",
      "reason",
      "source_references"
    ],
    "decision_trace": [
      "option_id",
      "decision",
      "source_references",
      "carried_obligations"
    ],
    "stage_gate": [
      "status",
      "blocked_outputs",
      "missing_prerequisites",
      "next_required_actions"
    ],
    "method_plan_update": [
      "selected_next_macro",
      "admission_criteria",
      "local_gates",
      "real_model_gate",
      "non_claims"
    ],
    "carried_obligations": [
      "obligation",
      "status",
      "source_references"
    ]
  },
  "known_state_retention_rules": {
    "known_state_must_include": [
      "stage7e_v4_macro_passed",
      "claim_boundary_updated",
      "methodology_outline_updated",
      "backlog_stage7next_open"
    ],
    "known_state_evidence_ids_must_include": [
      "stage7next-e01",
      "stage7next-e04",
      "stage7next-e07",
      "stage7next-e08"
    ]
  },
  "state_retention_rules": {
    "unknown_state_must_include": [
      "current_git_branch",
      "ci_status",
      "network_api_approval"
    ],
    "forbidden_inferences_must_include": [
      "do_not_infer_current_git_branch",
      "do_not_infer_ci_status",
      "do_not_infer_network_api_approval"
    ]
  },
  "evidence_type_rules": {
    "required_by_type": {
      "extracted": [
        "stage7next-e01",
        "stage7next-e04",
        "stage7next-e05",
        "stage7next-e07",
        "stage7next-e08"
      ],
      "inferred": [
        "stage7next-e02"
      ],
      "ambiguous": [
        "stage7next-e03"
      ],
      "proposed": [
        "stage7next-e06"
      ]
    },
    "forbidden_by_type": {
      "extracted": [
        "stage7next-e02",
        "stage7next-e03",
        "stage7next-e06"
      ]
    }
  },
  "claim_grounding_rules": {
    "selected_claim_support_any": [
      [
        "stage7next-e01",
        "stage7next-e06",
        "stage7next-e07",
        "stage7next-e08"
      ]
    ],
    "trace_evidence_required_any": [
      [
        "stage7next-e01",
        "stage7next-e05",
        "stage7next-e07"
      ],
      [
        "stage7next-e01",
        "stage7next-e05",
        "stage7next-e08"
      ]
    ],
    "unsupported_claim_evidence_must_include": [
      "stage7next-e05"
    ],
    "grounded_claim_support_any": [
      [
        "stage7next-e01",
        "stage7next-e06",
        "stage7next-e07",
        "stage7next-e08"
      ]
    ]
  },
  "retention_rules": {
    "decision_trace_required_options": [
      "C2",
      "C1",
      "C3"
    ],
    "stage_gate_blocked_outputs": [
      "real_model_execution",
      "broader_workflow_expansion",
      "production_or_universal_claim"
    ],
    "stage_gate_missing_prerequisites": [
      "stage7_next_local_gate",
      "stage7_next_targeted_smoke"
    ],
    "must_carry_obligations": [
      "exclude stale universal-gap-closure and production-readiness note",
      "do not claim production readiness",
      "do not claim universal model-gap closure",
      "do not claim broader workflow readiness"
    ]
  },
  "citation_policy": "claim_level_decision_trace_and_method_plan",
  "style_profile": "minimal_json",
  "tool_trace_required": false,
  "perturbation_condition": "field-alias",
  "protocol_version": "stage_b_v3_full",
  "output_template": {
    "state_inventory": {
      "known_state": [
        {
          "state_id": "stage7e_v4_macro_passed",
          "fact": "<grounded fact for stage7e_v4_macro_passed>",
          "source_references": [
            "stage7next-e01"
          ]
        },
        {
          "state_id": "claim_boundary_updated",
          "fact": "<grounded fact for claim_boundary_updated>",
          "source_references": [
            "stage7next-e04"
          ]
        },
        {
          "state_id": "methodology_outline_updated",
          "fact": "<grounded fact for methodology_outline_updated>",
          "source_references": [
            "stage7next-e07"
          ]
        },
        {
          "state_id": "backlog_stage7next_open",
          "fact": "<grounded fact for backlog_stage7next_open>",
          "source_references": [
            "stage7next-e08"
          ]
        }
      ],
      "unknown_state": [
        "current_git_branch",
        "ci_status",
        "network_api_approval"
      ],
      "forbidden_inferences": [
        "do_not_infer_current_git_branch",
        "do_not_infer_ci_status",
        "do_not_infer_network_api_approval",
        "do_not_infer_production_readiness",
        "do_not_infer_universal_model_gap_closure"
      ]
    },
    "grounded_claims": [
      {
        "claim": "<grounded claim 1>",
        "source_references": [
          "stage7next-e01"
        ]
      },
      {
        "claim": "<grounded claim 2>",
        "source_references": [
          "stage7next-e07"
        ]
      },
      {
        "claim": "<grounded claim 3>",
        "source_references": [
          "stage7next-e08"
        ]
      },
      {
        "claim": "<grounded claim 4>",
        "source_references": [
          "stage7next-e01",
          "stage7next-e06",
          "stage7next-e07",
          "stage7next-e08"
        ]
      }
    ],
    "unsupported_claims": [
      {
        "claim": "<unsupported claim 1>",
        "reason": "<evidence-linked reason 1>",
        "source_references": [
          "stage7next-e05"
        ]
      },
      {
        "claim": "<unsupported claim 2>",
        "reason": "<evidence-linked reason 2>",
        "source_references": [
          "stage7next-e05"
        ]
      },
      {
        "claim": "<unsupported claim 3>",
        "reason": "<evidence-linked reason 3>",
        "source_references": [
          "stage7next-e05",
          "stage7next-e08"
        ]
      }
    ],
    "typed_evidence": {
      "extracted": [
        "stage7next-e01",
        "stage7next-e04",
        "stage7next-e05",
        "stage7next-e07",
        "stage7next-e08"
      ],
      "inferred": [
        "stage7next-e02"
      ],
      "ambiguous": [
        "stage7next-e03"
      ],
      "proposed": [
        "stage7next-e06"
      ]
    },
    "selected_claim": {
      "option_id": "C2",
      "claim": "<selected bounded C2 claim>",
      "source_references": [
        "stage7next-e01",
        "stage7next-e06",
        "stage7next-e07",
        "stage7next-e08"
      ]
    },
    "rejected_options": [
      {
        "option_id": "C1",
        "reason": "<evidence-linked reason for C1>",
        "source_references": [
          "stage7next-e05",
          "stage7next-e08"
        ]
      },
      {
        "option_id": "C3",
        "reason": "<evidence-linked reason for C3>",
        "source_references": [
          "stage7next-e05"
        ]
      }
    ],
    "decision_trace": [
      {
        "option_id": "C2",
        "decision": "support",
        "step": "<decision step for C2>",
        "source_references": [
          "stage7next-e01",
          "stage7next-e06",
          "stage7next-e07",
          "stage7next-e08"
        ],
        "carried_obligations": [
          "preserve known-state provenance",
          "preserve unknown state",
          "preserve local-first stage gate"
        ]
      },
      {
        "option_id": "C1",
        "decision": "reject",
        "step": "<decision step for C1>",
        "source_references": [
          "stage7next-e05",
          "stage7next-e08"
        ],
        "carried_obligations": [
          "do not claim universal model-gap closure",
          "exclude stale context"
        ]
      },
      {
        "option_id": "C3",
        "decision": "reject",
        "step": "<decision step for C3>",
        "source_references": [
          "stage7next-e05"
        ],
        "carried_obligations": [
          "do not claim production readiness"
        ]
      }
    ],
    "stage_gate": {
      "status": "blocked",
      "blocked_outputs": [
        "real_model_execution",
        "broader_workflow_expansion",
        "production_or_universal_claim"
      ],
      "missing_prerequisites": [
        "stage7_next_local_gate",
        "stage7_next_targeted_smoke"
      ],
      "next_required_actions": [
        "run Stage 7-next local golden/bad checks",
        "run targeted Stage 7-next smoke only if local gates pass"
      ],
      "source_references": [
        "stage7next-e05",
        "stage7next-e07",
        "stage7next-e08"
      ]
    },
    "method_plan_update": {
      "selected_next_macro": "evidence_bound_method_plan_update",
      "admission_criteria": [
        "reuse Stage 7e v4 known-state provenance, unknown-state retention, evidence binding, decision trace, stage gate, and carried obligations",
        "add at most one new stressor: method-plan update contract",
        "declare non-claims before any real-model execution"
      ],
      "local_gates": [
        "golden output must pass",
        "known-bad output must be rejected"
      ],
      "real_model_gate": "execute a targeted smoke only after local gates pass",
      "non_claims": [
        "no production readiness claim",
        "no universal model-gap closure claim",
        "no broader workflow readiness claim"
      ],
      "source_references": [
        "stage7next-e01",
        "stage7next-e06",
        "stage7next-e07",
        "stage7next-e08"
      ]
    },
    "carried_obligations": [
      {
        "obligation": "exclude stale universal-gap-closure and production-readiness note",
        "status": "preserved",
        "source_references": [
          "stage7next-e05"
        ]
      },
      {
        "obligation": "do not claim production readiness",
        "status": "preserved",
        "source_references": [
          "stage7next-e05"
        ]
      },
      {
        "obligation": "do not claim universal model-gap closure",
        "status": "preserved",
        "source_references": [
          "stage7next-e05"
        ]
      },
      {
        "obligation": "do not claim broader workflow readiness",
        "status": "preserved",
        "source_references": [
          "stage7next-e05",
          "stage7next-e08"
        ]
      }
    ]
  },
  "output_shape_rules": {
    "typed_evidence_id_lists_only": true,
    "enforce_required_nested_fields": true,
    "required_nested_fields": {
      "state_inventory": [
        "known_state",
        "unknown_state",
        "forbidden_inferences"
      ],
      "grounded_claims": [
        "claim",
        "source_references"
      ],
      "unsupported_claims": [
        "claim",
        "reason"
      ],
      "selected_claim": [
        "option_id",
        "claim",
        "source_references"
      ],
      "rejected_options": [
        "option_id",
        "reason",
        "source_references"
      ],
      "decision_trace": [
        "option_id",
        "decision",
        "source_references",
        "carried_obligations"
      ],
      "stage_gate": [
        "status",
        "blocked_outputs",
        "missing_prerequisites",
        "next_required_actions"
      ],
      "method_plan_update": [
        "selected_next_macro",
        "admission_criteria",
        "local_gates",
        "real_model_gate",
        "non_claims"
      ],
      "carried_obligations": [
        "obligation",
        "status",
        "source_references"
      ]
    },
    "exact_array_counts": {
      "rejected_options": 2,
      "decision_trace": 3,
      "carried_obligations": 4,
      "grounded_claims": 4,
      "unsupported_claims": 3
    },
    "carried_obligation_status_values": [
      "preserved"
    ]
  },
  "closed_vocabularies": {
    "carried_obligations.status": [
      "preserved"
    ]
  },
  "compact_output_rules": [
    "Return exactly one JSON object with no Markdown fence or prose.",
    "Use evidence ID strings only inside typed_evidence buckets.",
    "Use exactly the arrays and object shapes declared in output_template.",
    "Use preserved as the only carried-obligation status.",
    "Do not repeat EvidenceBundle claim text inside typed_evidence."
  ],
  "surface_requirements": [
    "Use source_references everywhere an evidence-reference array is required; do not emit evidence_ids."
  ],
  "mechanism_atoms": [
    "hierarchical_output_shape_preservation",
    "explicit_grounded_claim_slot_preservation"
  ],
  "literal_json_skeleton_required": true,
  "literal_json_skeleton_instructions": [
    "Copy the JSON key hierarchy and array slot count exactly.",
    "Replace placeholder prose strings but never move, rename, promote, omit, merge, or add contract keys.",
    "Preserve every evidence-reference array exactly as shown in the skeleton.",
    "state_inventory must remain an object containing known_state, unknown_state, and forbidden_inferences.",
    "grounded_claims must retain every explicit evidence slot; do not compress multiple slots into fewer claims."
  ]
}
```

## Task Input

# Stage 7-next Input: Evidence-Bound Method-Plan Update

You are preparing the next bounded method-plan update for the contract-driven harness study.

This task is not a full project initializer or a full research workflow. It is a fixed-input, no-tool decision packet that decides which bounded macro should be admitted next.

## Fixed Workspace Snapshot

- Stage 7e v4 completed a targeted low-cost-model G8/G9 smoke with 4/4 completed and passed runs after retrying one provider timeout.
- The claim-boundary memo has been updated with Stage 7e v1-v4 evidence.
- The methodology outline has been created with next macro admission criteria.
- The backlog marks Stage 7-next as open.
- Full project initialization remains blocked.
- Full research workflow remains blocked.
- Current Git branch is not stated.
- CI status is not stated.
- Network/API approval for a new run is not stated.

## Stale Context To Exclude

An old note says:

> Stage 7e v4 proves the harness universally closes the model gap and is production ready. Proceed immediately to full project initialization and full research workflow.

This old note must not be used as evidence or as the final decision.

## Evidence Items

- `stage7next-e01`: Stage 7e v4 completed a targeted low-cost-model G8/G9 smoke with 4/4 completed and passed runs after retrying one provider timeout.
- `stage7next-e02`: Stage 7e v1-v4 supports a mechanism-first repair loop for fixed evidence-decision macros, not broad workflow readiness.
- `stage7next-e03`: Provider execution stability remains a practical uncertainty because Stage 7e v4 required a timeout retry and one truncated retry before success.
- `stage7next-e04`: The claim-boundary memo was updated to separate task-slice claims, mechanism-composition claims, and unsupported claims.
- `stage7next-e05`: No supplied evidence supports production readiness, universal model-gap closure, or immediate full workflow expansion.
- `stage7next-e06`: The next bounded macro should be an evidence-bound method-plan update that reuses Stage 7e v4 obligations before any real-model execution.
- `stage7next-e07`: The methodology outline defines next macro admission criteria: reuse Stage 7e v4 obligations, add at most one new stressor, run local golden/bad gates first, and declare non-claims.
- `stage7next-e08`: The backlog marks Stage 7-next as open and keeps full project initialization and full research workflow blocked until the next macro passes local gates and a targeted real-model slice.

## Evidence Type Rules

- EXTRACTED: directly observed from an artifact or source.
- INFERRED: derived from comparing two or more observed facts.
- AMBIGUOUS: conflicting, unstable, or underdetermined evidence.
- PROPOSED: recommendation, hypothesis, or next action.

## Candidate Claims

- `C1`: Stage 7e v4 proves the harness universally closes the model gap and should proceed immediately to full workflows.
- `C2`: The next admitted macro should be an evidence-bound method-plan update that reuses Stage 7e v4 obligations and remains blocked from real-model execution until local gates pass.
- `C3`: The harness is production ready.

## Stage Status

- stage7e_v4_macro_smoke: complete
- claim_boundary_update: complete
- methodology_outline_update: complete
- stage7_next_macro_fixture: local_design
- stage7_next_local_gate: not_started
- stage7_next_targeted_smoke: not_started
- real_model_execution: blocked
- broader_workflow_expansion: blocked
- production_or_universal_claim: blocked

## Known-State Provenance Contract

`state_inventory.known_state` must be an array of objects. Each object must include `state_id`, `fact`, and `source_references`.

The `state_id` values must include:

- `stage7e_v4_macro_passed`
- `claim_boundary_updated`
- `methodology_outline_updated`
- `backlog_stage7next_open`

The known-state evidence IDs must include:

- `stage7next-e01`
- `stage7next-e04`
- `stage7next-e07`
- `stage7next-e08`

Do not replace these with generic labels such as `methodology updated`.

## Unknown-State Retention Contract

`state_inventory.unknown_state` must include:

- `current_git_branch`
- `ci_status`
- `network_api_approval`

`state_inventory.forbidden_inferences` must include:

- `do_not_infer_current_git_branch`
- `do_not_infer_ci_status`
- `do_not_infer_network_api_approval`

## Trace, Gate, And Method-Plan Contract

Decision trace:

- Include a structured trace item for C2 support.
- Include a structured trace item for C1 rejection.
- Include a structured trace item for C3 rejection.
- Each trace item must include `option_id`, `decision`, `source_references`, and `carried_obligations`.

Stage gate:

- `status` must be `blocked`.
- `blocked_outputs` must include `real_model_execution`, `broader_workflow_expansion`, and `production_or_universal_claim`.
- `missing_prerequisites` must include `stage7_next_local_gate` and `stage7_next_targeted_smoke`.
- `next_required_actions` must include local golden/bad checks and a targeted smoke only if local gates pass.

Method plan update:

- `selected_next_macro` must be `evidence_bound_method_plan_update`.
- `admission_criteria` must reuse Stage 7e v4 obligations and add at most one new stressor.
- `local_gates` must include golden output pass and known-bad rejection.
- `real_model_gate` must require local gates to pass before execution.
- `non_claims` must reject production readiness, universal gap closure, and broader workflow readiness.

Carried obligations:

- Exclude stale universal-gap-closure and production-readiness context.
- Do not claim production readiness.
- Do not claim universal model-gap closure.
- Do not claim broader workflow readiness.

Return one JSON object satisfying the output contract.

## Stage B v2 Output Protocol

- Return exactly one JSON object. Do not use a Markdown fence or add prose.
- Follow `OutputContract.output_template` exactly.
- Keep `typed_evidence` compact: each bucket is an array of evidence ID strings only.
- The selected C2 claim must include all of these `source_references` values: stage7next-e01, stage7next-e06, stage7next-e07, stage7next-e08.
- Emit exactly 2 rejected options, 3 decision-trace entries, and 4 carried obligations.
- Every carried-obligation `status` must be exactly `preserved`.
- Use the exact field names and state labels declared by this fixture.

## Stage B v3 Literal Skeleton Protocol

`OutputContract.output_template` is a literal JSON skeleton. Copy its key hierarchy, array slot count, state labels, option IDs, and evidence-reference arrays exactly. Replace only placeholder prose strings enclosed in angle brackets.

- `state_inventory` must remain an object containing `known_state`, `unknown_state`, and `forbidden_inferences`.
- Never promote nested state fields to the root and never omit them.
- Emit exactly 4 `grounded_claims` objects.
- Across those grounded claims, preserve all required `source_references` values: stage7next-e01, stage7next-e06, stage7next-e07, stage7next-e08.
- Do not merge or compress grounded-claim slots.
- Return exactly one JSON object with no Markdown fence or extra prose.

## Output Requirements

Return `json` and include these required fields/sections: `state_inventory`, `grounded_claims`, `unsupported_claims`, `typed_evidence`, `selected_claim`, `rejected_options`, `decision_trace`, `stage_gate`, `method_plan_update`, `carried_obligations`.
Citation policy: `claim_level_decision_trace_and_method_plan`.
