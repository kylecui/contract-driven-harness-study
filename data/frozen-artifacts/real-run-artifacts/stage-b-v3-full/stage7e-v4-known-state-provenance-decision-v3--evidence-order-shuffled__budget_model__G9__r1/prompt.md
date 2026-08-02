# Benchmark Run: stage7e-v4-known-state-provenance-decision-v3--evidence-order-shuffled__budget_model__G9__r1

You are completing a benchmark task. Follow the instructions for the assigned harness arm.

- Fixture: `stage7e-v4-known-state-provenance-decision-v3--evidence-order-shuffled`
- Model tier: `budget_model`
- Harness arm: `G9`
- Task type: `stage7e_evidence_bound_macro`

## Harness Arm G9

Use the full harness packet. Obey the task spec, preserve evidence IDs for important claims, respect memory boundaries, and satisfy the output contract.

## TaskSpec

```json
{
  "task_id": "stage7e_v4_known_state_provenance_decision",
  "task_type": "stage7e_evidence_bound_macro",
  "objective": "Repeat the evidence-bound decision packet with explicit evidence-linked known-state provenance plus the Stage 7e v2/v3 retention contracts.",
  "composition_chain": [
    "A4R",
    "A2R1",
    "A8R",
    "A7R1",
    "A5R",
    "trace_gate_retention_contract",
    "state_retention_contract",
    "known_state_provenance_contract"
  ],
  "constraints": [
    "Use only supplied workspace snapshot and evidence items.",
    "Do not infer Git branch, CI status, or network/API approval.",
    "state_inventory.known_state must explicitly include stage7r1_targeted_smoke_complete, stage7r2_narrow_macro_admitted, stage7e_v2_trace_gate_retention_repaired, and stage7e_v3_unknown_state_retention_repaired.",
    "Every known_state item must carry evidence_ids.",
    "state_inventory.unknown_state must explicitly include current_git_branch, ci_status, and network_api_approval.",
    "state_inventory.forbidden_inferences must explicitly include do_not_infer_current_git_branch, do_not_infer_ci_status, and do_not_infer_network_api_approval.",
    "Exclude stale context from the decision.",
    "Bind every grounded claim to claim-level evidence IDs.",
    "Classify evidence into EXTRACTED, INFERRED, AMBIGUOUS, or PROPOSED.",
    "Select exactly one candidate claim.",
    "Reject overbroad or unsupported claims with evidence-linked reasons.",
    "Every decision_trace item must be an object with option_id, decision, evidence_ids, and carried_obligations.",
    "The stage_gate must explicitly block final_recommendation, full_project_initialization, and full_research_workflow.",
    "The stage_gate must explicitly list stage7e_v4_local_gate and stage7e_v4_smoke as missing prerequisites.",
    "Carry forward negative obligations across selected_claim, rejected_options, decision_trace, stage_gate, and carried_obligations."
  ],
  "success_conditions": [
    "Known-state provenance explicitly preserves the four required state IDs with evidence IDs.",
    "Unknown-state inventory explicitly preserves the three unknown state fields.",
    "Forbidden inferences explicitly block the three unknown state fields.",
    "Grounded claims have claim-level evidence IDs.",
    "Production readiness and universal gap closure are not grounded.",
    "Evidence typing includes EXTRACTED, INFERRED, AMBIGUOUS, and PROPOSED where appropriate.",
    "Selected claim is C2.",
    "Rejected options include C1 and C3 with evidence IDs.",
    "Decision trace covers C2 support, C1 rejection, and C3 rejection as structured objects.",
    "Stage gate blocks all three blocked outputs and lists both v4 prerequisites.",
    "Carried obligations preserve stale-context exclusion and unsupported-production-readiness exclusion."
  ],
  "perturbation_condition": "evidence-order-shuffled",
  "base_macro": "stage7e-v4-known-state-provenance-decision",
  "protocol_version": "stage_b_v3_full",
  "repair_confirmation": true,
  "fixture_id": "stage7e-v4-known-state-provenance-decision-v3--evidence-order-shuffled",
  "mechanism_atoms": [
    "hierarchical_output_shape_preservation",
    "explicit_grounded_claim_slot_preservation"
  ]
}
```

## EvidenceBundle

```json
{
  "bundle_id": "stage7e_v4_known_state_provenance_evidence_bundle_001",
  "items": [
    {
      "evidence_id": "stage7e-e09",
      "type": "EXTRACTED",
      "claim": "Stage 7e v3 still had one G8 run fail because it compressed known-state provenance into generic labels rather than preserving explicit Stage 7r.1/Stage 7r.2 evidence-linked state.",
      "source": "research/05_analysis/stage-reports/stage-7e-v3-state-retention-decision-summary.md"
    },
    {
      "evidence_id": "stage7e-e08",
      "type": "EXTRACTED",
      "claim": "Stage 7e v3 repaired Git/CI/network unknown-state retention in 4/4 low-cost-model runs and passed full strict macro evaluation in 3/4 runs.",
      "source": "research/05_analysis/stage-reports/stage-7e-v3-state-retention-decision-summary.md"
    },
    {
      "evidence_id": "stage7e-e07",
      "type": "EXTRACTED",
      "claim": "Stage 7e v2 repaired trace and stage-gate retention in 4/4 low-cost-model runs.",
      "source": "research/05_analysis/stage-reports/stage-7e-v2-retention-decision-summary.md"
    },
    {
      "evidence_id": "stage7e-e06",
      "type": "PROPOSED",
      "claim": "Run Stage 7e v4 local golden/bad checks and then a targeted low-cost-model smoke before broader macro expansion.",
      "source": "research/05_analysis/stage-reports/stage-7e-v3-state-retention-decision-summary.md"
    },
    {
      "evidence_id": "stage7e-e05",
      "type": "EXTRACTED",
      "claim": "No supplied evidence supports production readiness or universal model-gap closure.",
      "source": "input.md"
    },
    {
      "evidence_id": "stage7e-e04",
      "type": "EXTRACTED",
      "claim": "Stage 7r.2 admits a narrow evidence-bound decision macro and blocks full project initialization and full research workflow composition.",
      "source": "research/05_analysis/stage-reports/stage-7r2-composition-readiness-gate.md"
    },
    {
      "evidence_id": "stage7e-e03",
      "type": "AMBIGUOUS",
      "claim": "A8R has mixed execution evidence because low-cost G8 timed out while low-cost G9 and strong G8/G9 passed.",
      "source": "research/05_analysis/stage-reports/stage-7r-revised-atoms-summary.md"
    },
    {
      "evidence_id": "stage7e-e02",
      "type": "INFERRED",
      "claim": "Stage 7r.1 supports the mechanism-first repair hypothesis for A2R/A7R low-cost-model failures.",
      "source": "research/03_evidence/evidence-ledger.jsonl#P2-E60"
    },
    {
      "evidence_id": "stage7e-e01",
      "type": "EXTRACTED",
      "claim": "Stage 7r.1 completed 8/8 targeted smoke runs and passed 8/8 under low-cost-model G8/G9.",
      "source": "research/05_analysis/stage-reports/stage-7r1-a2r-a7r-targeted-smoke-summary.md"
    }
  ]
}
```

## MemorySlice

```json
{
  "slice_id": "stage7e_v4_known_state_provenance_memory_001",
  "must_load": [
    "Stage 7r.1 targeted smoke completed 8/8 and passed 8/8",
    "Stage 7r.2 admits only a narrow evidence-bound decision macro",
    "Stage 7e v2 repaired trace and stage-gate retention",
    "Stage 7e v3 repaired Git/CI/network unknown-state retention",
    "Stage 7e v3 still had one known-state provenance compression failure",
    "current Git branch is unknown",
    "CI status is unknown",
    "network/API approval is unknown",
    "full project initialization remains blocked",
    "full research workflow remains blocked"
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
  "output_contract_id": "out_stage7e_v4_known_state_provenance_decision_001_stage_b_v3_full",
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
      "evidence_ids"
    ],
    "unsupported_claims": [
      "claim",
      "reason"
    ],
    "selected_claim": [
      "option_id",
      "claim",
      "evidence_ids"
    ],
    "rejected_options": [
      "option_id",
      "reason",
      "evidence_ids"
    ],
    "decision_trace": [
      "option_id",
      "decision",
      "evidence_ids",
      "carried_obligations"
    ],
    "stage_gate": [
      "status",
      "blocked_outputs",
      "missing_prerequisites",
      "next_required_actions"
    ],
    "carried_obligations": [
      "obligation",
      "status",
      "evidence_ids"
    ]
  },
  "known_state_retention_rules": {
    "known_state_must_include": [
      "stage7r1_targeted_smoke_complete",
      "stage7r2_narrow_macro_admitted",
      "stage7e_v2_trace_gate_retention_repaired",
      "stage7e_v3_unknown_state_retention_repaired"
    ],
    "known_state_evidence_ids_must_include": [
      "stage7e-e01",
      "stage7e-e04",
      "stage7e-e07",
      "stage7e-e08"
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
  "claim_grounding_rules": {
    "selected_claim_support_any": [
      [
        "stage7e-e01",
        "stage7e-e04",
        "stage7e-e07",
        "stage7e-e08",
        "stage7e-e09"
      ]
    ],
    "trace_evidence_required_any": [
      [
        "stage7e-e01",
        "stage7e-e04",
        "stage7e-e05"
      ],
      [
        "stage7e-e04",
        "stage7e-e05",
        "stage7e-e07",
        "stage7e-e08"
      ],
      [
        "stage7e-e05",
        "stage7e-e06",
        "stage7e-e08",
        "stage7e-e09"
      ]
    ],
    "grounded_claim_support_any": [
      [
        "stage7e-e01",
        "stage7e-e04",
        "stage7e-e08",
        "stage7e-e09"
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
      "final_recommendation",
      "full_project_initialization",
      "full_research_workflow"
    ],
    "stage_gate_missing_prerequisites": [
      "stage7e_v4_local_gate",
      "stage7e_v4_smoke"
    ],
    "must_carry_obligations": [
      "exclude stale universal-gap-closure and production-readiness note",
      "do not claim production readiness",
      "do not claim universal model-gap closure",
      "do not claim full project initialization or full research workflow readiness"
    ]
  },
  "citation_policy": "claim_level_and_decision_trace",
  "style_profile": "minimal_json",
  "tool_trace_required": false,
  "perturbation_condition": "evidence-order-shuffled",
  "protocol_version": "stage_b_v3_full",
  "output_template": {
    "state_inventory": {
      "known_state": [
        {
          "state_id": "stage7r1_targeted_smoke_complete",
          "fact": "<grounded fact for stage7r1_targeted_smoke_complete>",
          "evidence_ids": [
            "stage7e-e01"
          ]
        },
        {
          "state_id": "stage7r2_narrow_macro_admitted",
          "fact": "<grounded fact for stage7r2_narrow_macro_admitted>",
          "evidence_ids": [
            "stage7e-e04"
          ]
        },
        {
          "state_id": "stage7e_v2_trace_gate_retention_repaired",
          "fact": "<grounded fact for stage7e_v2_trace_gate_retention_repaired>",
          "evidence_ids": [
            "stage7e-e07"
          ]
        },
        {
          "state_id": "stage7e_v3_unknown_state_retention_repaired",
          "fact": "<grounded fact for stage7e_v3_unknown_state_retention_repaired>",
          "evidence_ids": [
            "stage7e-e08"
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
        "evidence_ids": [
          "stage7e-e01"
        ]
      },
      {
        "claim": "<grounded claim 2>",
        "evidence_ids": [
          "stage7e-e08",
          "stage7e-e09"
        ]
      },
      {
        "claim": "<grounded claim 3>",
        "evidence_ids": [
          "stage7e-e04"
        ]
      }
    ],
    "unsupported_claims": [
      {
        "claim": "<unsupported claim 1>",
        "reason": "<evidence-linked reason 1>",
        "evidence_ids": [
          "stage7e-e05"
        ]
      },
      {
        "claim": "<unsupported claim 2>",
        "reason": "<evidence-linked reason 2>",
        "evidence_ids": [
          "stage7e-e05"
        ]
      }
    ],
    "typed_evidence": {
      "extracted": [
        "stage7e-e01",
        "stage7e-e04",
        "stage7e-e05",
        "stage7e-e07",
        "stage7e-e08",
        "stage7e-e09"
      ],
      "inferred": [
        "stage7e-e02"
      ],
      "ambiguous": [
        "stage7e-e03"
      ],
      "proposed": [
        "stage7e-e06"
      ]
    },
    "selected_claim": {
      "option_id": "C2",
      "claim": "<selected bounded C2 claim>",
      "evidence_ids": [
        "stage7e-e01",
        "stage7e-e04",
        "stage7e-e07",
        "stage7e-e08",
        "stage7e-e09"
      ]
    },
    "rejected_options": [
      {
        "option_id": "C1",
        "reason": "<evidence-linked reason for C1>",
        "evidence_ids": [
          "stage7e-e05",
          "stage7e-e03"
        ]
      },
      {
        "option_id": "C3",
        "reason": "<evidence-linked reason for C3>",
        "evidence_ids": [
          "stage7e-e05",
          "stage7e-e04"
        ]
      }
    ],
    "decision_trace": [
      {
        "option_id": "C2",
        "decision": "support",
        "step": "<decision step for C2>",
        "evidence_ids": [
          "stage7e-e01",
          "stage7e-e04",
          "stage7e-e07",
          "stage7e-e08",
          "stage7e-e09"
        ],
        "carried_obligations": [
          "preserve known-state provenance",
          "preserve unknown state",
          "preserve stage gate"
        ]
      },
      {
        "option_id": "C1",
        "decision": "reject",
        "step": "<decision step for C1>",
        "evidence_ids": [
          "stage7e-e05",
          "stage7e-e03"
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
        "evidence_ids": [
          "stage7e-e05",
          "stage7e-e04"
        ],
        "carried_obligations": [
          "do not claim production readiness",
          "do not claim full workflow readiness"
        ]
      }
    ],
    "stage_gate": {
      "status": "blocked",
      "blocked_outputs": [
        "final_recommendation",
        "full_project_initialization",
        "full_research_workflow"
      ],
      "missing_prerequisites": [
        "stage7e_v4_local_gate",
        "stage7e_v4_smoke"
      ],
      "next_required_actions": [
        "run Stage 7e v4 local golden/bad checks",
        "run targeted low-cost-model Stage 7e v4 smoke only if local gates pass"
      ],
      "evidence_ids": [
        "stage7e-e04",
        "stage7e-e06",
        "stage7e-e09"
      ]
    },
    "carried_obligations": [
      {
        "obligation": "exclude stale universal-gap-closure and production-readiness note",
        "status": "preserved",
        "evidence_ids": [
          "stage7e-e05"
        ]
      },
      {
        "obligation": "do not claim production readiness",
        "status": "preserved",
        "evidence_ids": [
          "stage7e-e05"
        ]
      },
      {
        "obligation": "do not claim universal model-gap closure",
        "status": "preserved",
        "evidence_ids": [
          "stage7e-e05",
          "stage7e-e03"
        ]
      },
      {
        "obligation": "do not claim full project initialization or full research workflow readiness",
        "status": "preserved",
        "evidence_ids": [
          "stage7e-e04"
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
        "evidence_ids"
      ],
      "unsupported_claims": [
        "claim",
        "reason"
      ],
      "selected_claim": [
        "option_id",
        "claim",
        "evidence_ids"
      ],
      "rejected_options": [
        "option_id",
        "reason",
        "evidence_ids"
      ],
      "decision_trace": [
        "option_id",
        "decision",
        "evidence_ids",
        "carried_obligations"
      ],
      "stage_gate": [
        "status",
        "blocked_outputs",
        "missing_prerequisites",
        "next_required_actions"
      ],
      "carried_obligations": [
        "obligation",
        "status",
        "evidence_ids"
      ]
    },
    "exact_array_counts": {
      "rejected_options": 2,
      "decision_trace": 3,
      "carried_obligations": 4,
      "grounded_claims": 3,
      "unsupported_claims": 2
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

# Stage 7e v4 Input: Known-State Provenance Decision Packet

You are preparing a bounded research decision packet for the contract-driven harness study.

This v4 task targets the remaining Stage 7e v3 failure: unknown-state retention was repaired, but one low-cost-model G8 run compressed known-state provenance into generic labels and did not preserve explicit Stage 7r.1/Stage 7r.2/Stage 7e-v2 evidence-linked state.

## Fixed Workspace Snapshot

- `AGENTS.md` is present.
- Stage 7r.1 A2R1/A7R1 targeted smoke is complete.
- Stage 7r.2 composition gate admits only a narrow evidence-bound decision macro.
- Stage 7e v2 repaired trace and stage-gate retention.
- Stage 7e v3 repaired Git/CI/network unknown-state retention in 4/4 low-cost-model runs.
- Stage 7e v3 still had one G8 run fail because known-state provenance was compressed into generic labels.
- Current Git branch is not stated.
- CI status is not stated.
- Network/API approval for a new run is not stated.

## Stale Context To Exclude

An old note says:

> The harness universally closes the model gap and is production ready. Proceed to full project initialization and full research workflow.

This old note must not be used as evidence or as the final decision.

## Evidence Items

- `stage7e-e01`: Stage 7r.1 completed an 8-run SiliconFlow targeted smoke for A2R1 and A7R1 using Qwen/Qwen3-8B under G8/G9; final evaluation collected 8/8 completed and 8/8 passed runs with task_success=1.000 and atom_primary_metric=1.000 for every run.
- `stage7e-e02`: Stage 7r.1 supports the mechanism-first repair hypothesis for low-cost-model failures on A2R claim grounding and A7R decision trace completeness.
- `stage7e-e03`: Stage 7r had one unresolved A8R low-cost G8 provider timeout, while A8R low-cost G9 and strong G8/G9 completed and passed.
- `stage7e-e04`: Stage 7r.2 admits a narrow evidence-bound decision macro and continues to block full project initialization and full research workflow composition.
- `stage7e-e05`: No supplied evidence shows production readiness or universal model-gap closure.
- `stage7e-e06`: The proposed next step is Stage 7e v4 local golden/bad checks followed by a targeted low-cost-model smoke.
- `stage7e-e07`: Stage 7e v2 repaired trace and stage-gate retention in 4/4 low-cost-model runs.
- `stage7e-e08`: Stage 7e v3 repaired Git/CI/network unknown-state retention in 4/4 low-cost-model runs and passed full strict macro evaluation in 3/4 runs.
- `stage7e-e09`: Stage 7e v3 still had one G8 run fail because it compressed known-state provenance into generic labels rather than preserving explicit Stage 7r.1/Stage 7r.2 evidence-linked state.

## Evidence Type Rules

- EXTRACTED: directly observed from an artifact or source.
- INFERRED: derived from comparing two or more observed facts.
- AMBIGUOUS: conflicting or underdetermined evidence.
- PROPOSED: recommendation, hypothesis, or next action.

## Candidate Claims

- `C1`: The harness universally closes the performance gap between strong and low-cost models.
- `C2`: Mechanism-bound evidence decision workflows are ready for a narrow known-state-provenance v4 smoke under the harness.
- `C3`: The harness is production ready.

## Stage Status

- mechanism_atom_evidence: complete
- stage7e_v2_retention_smoke: complete
- stage7e_v3_state_retention_smoke: complete
- stage7e_v4_macro_fixture: local_design
- stage7e_v4_local_gate: not_started
- stage7e_v4_smoke: not_started
- final_recommendation: blocked
- full_project_initialization: blocked
- full_research_workflow: blocked

## Known-State Provenance Contract

`state_inventory.known_state` must be an array of objects. Each object must include `state_id`, `fact`, and `evidence_ids`.

The `state_id` values must include:

- `stage7r1_targeted_smoke_complete`
- `stage7r2_narrow_macro_admitted`
- `stage7e_v2_trace_gate_retention_repaired`
- `stage7e_v3_unknown_state_retention_repaired`

The known-state evidence IDs must include:

- `stage7e-e01`
- `stage7e-e04`
- `stage7e-e07`
- `stage7e-e08`

Do not replace these with generic labels such as `mechanism_atom_evidence: complete`.

## Unknown-State Retention Contract

`state_inventory.unknown_state` must include:

- `current_git_branch`
- `ci_status`
- `network_api_approval`

`state_inventory.forbidden_inferences` must include:

- `do_not_infer_current_git_branch`
- `do_not_infer_ci_status`
- `do_not_infer_network_api_approval`

## Trace And Gate Retention Contract

Decision trace:

- Include a structured trace item for C2 support.
- Include a structured trace item for C1 rejection.
- Include a structured trace item for C3 rejection.
- Each trace item must include `option_id`, `decision`, `evidence_ids`, and `carried_obligations`.

Stage gate:

- `status` must be `blocked`.
- `blocked_outputs` must include `final_recommendation`, `full_project_initialization`, and `full_research_workflow`.
- `missing_prerequisites` must include `stage7e_v4_local_gate` and `stage7e_v4_smoke`.
- `next_required_actions` must include local golden/bad checks and the targeted low-cost-model smoke.

Carried obligations:

- Exclude stale universal-gap-closure and production-readiness context.
- Do not claim production readiness.
- Do not claim universal model-gap closure.
- Do not claim full project initialization or full research workflow readiness.

Return one JSON object satisfying the output contract.

## Stage B v2 Output Protocol

- Return exactly one JSON object. Do not use a Markdown fence or add prose.
- Follow `OutputContract.output_template` exactly.
- Keep `typed_evidence` compact: each bucket is an array of evidence ID strings only.
- The selected C2 claim must include all of these `evidence_ids` values: stage7e-e01, stage7e-e04, stage7e-e07, stage7e-e08, stage7e-e09.
- Emit exactly 2 rejected options, 3 decision-trace entries, and 4 carried obligations.
- Every carried-obligation `status` must be exactly `preserved`.
- Use the exact field names and state labels declared by this fixture.

## Stage B v3 Literal Skeleton Protocol

`OutputContract.output_template` is a literal JSON skeleton. Copy its key hierarchy, array slot count, state labels, option IDs, and evidence-reference arrays exactly. Replace only placeholder prose strings enclosed in angle brackets.

- `state_inventory` must remain an object containing `known_state`, `unknown_state`, and `forbidden_inferences`.
- Never promote nested state fields to the root and never omit them.
- Emit exactly 3 `grounded_claims` objects.
- Across those grounded claims, preserve all required `evidence_ids` values: stage7e-e01, stage7e-e04, stage7e-e08, stage7e-e09.
- Do not merge or compress grounded-claim slots.
- Return exactly one JSON object with no Markdown fence or extra prose.

## Output Requirements

Return `json` and include these required fields/sections: `state_inventory`, `grounded_claims`, `unsupported_claims`, `typed_evidence`, `selected_claim`, `rejected_options`, `decision_trace`, `stage_gate`, `carried_obligations`.
Citation policy: `claim_level_and_decision_trace`.
