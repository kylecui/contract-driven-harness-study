# Benchmark Run: stage7e-v3-state-retention-decision__budget_model__G9__r1

You are completing a benchmark task. Follow the instructions for the assigned harness arm.

- Fixture: `stage7e-v3-state-retention-decision`
- Model tier: `budget_model`
- Harness arm: `G9`
- Task type: `stage7e_evidence_bound_macro`

## Harness Arm G9

Use the full harness packet. Obey the task spec, preserve evidence IDs for important claims, respect memory boundaries, and satisfy the output contract.

## TaskSpec

```json
{
  "task_id": "stage7e_v3_state_retention_decision",
  "task_type": "stage7e_evidence_bound_macro",
  "objective": "Repeat the evidence-bound decision packet with explicit unknown-state retention plus the Stage 7e v2 trace and gate retention contract.",
  "composition_chain": [
    "A4R",
    "A2R1",
    "A8R",
    "A7R1",
    "A5R",
    "trace_gate_retention_contract",
    "state_retention_contract"
  ],
  "constraints": [
    "Use only supplied workspace snapshot and evidence items.",
    "Do not infer Git branch, CI status, or network/API approval.",
    "state_inventory.unknown_state must explicitly include current_git_branch, ci_status, and network_api_approval.",
    "state_inventory.forbidden_inferences must explicitly include do_not_infer_current_git_branch, do_not_infer_ci_status, and do_not_infer_network_api_approval.",
    "Exclude stale context from the decision.",
    "Bind every grounded claim to claim-level evidence IDs.",
    "Classify evidence into EXTRACTED, INFERRED, AMBIGUOUS, or PROPOSED.",
    "Select exactly one candidate claim.",
    "Reject overbroad or unsupported claims with evidence-linked reasons.",
    "Every decision_trace item must be an object with option_id, decision, evidence_ids, and carried_obligations.",
    "The stage_gate must explicitly block final_recommendation, full_project_initialization, and full_research_workflow.",
    "The stage_gate must explicitly list stage7e_v3_local_gate and stage7e_v3_smoke as missing prerequisites.",
    "Carry forward negative obligations across selected_claim, rejected_options, decision_trace, stage_gate, and carried_obligations."
  ],
  "success_conditions": [
    "State inventory explicitly preserves the three unknown state fields.",
    "Forbidden inferences explicitly block the three unknown state fields.",
    "Grounded claims have claim-level evidence IDs.",
    "Production readiness and universal gap closure are not grounded.",
    "Evidence typing includes EXTRACTED, INFERRED, AMBIGUOUS, and PROPOSED where appropriate.",
    "Selected claim is C2.",
    "Rejected options include C1 and C3 with evidence IDs.",
    "Decision trace covers C2 support, C1 rejection, and C3 rejection as structured objects.",
    "Stage gate blocks all three blocked outputs and lists both v3 prerequisites.",
    "Carried obligations preserve stale-context exclusion and unsupported-production-readiness exclusion."
  ]
}
```

## EvidenceBundle

```json
{
  "bundle_id": "stage7e_v3_state_retention_evidence_bundle_001",
  "items": [
    {
      "evidence_id": "stage7e-e01",
      "type": "EXTRACTED",
      "claim": "Stage 7r.1 completed 8/8 targeted smoke runs and passed 8/8 under low-cost-model G8/G9.",
      "source": "research/05_analysis/stage-reports/stage-7r1-a2r-a7r-targeted-smoke-summary.md"
    },
    {
      "evidence_id": "stage7e-e02",
      "type": "INFERRED",
      "claim": "Stage 7r.1 supports the mechanism-first repair hypothesis for A2R/A7R low-cost-model failures.",
      "source": "research/03_evidence/evidence-ledger.jsonl#P2-E60"
    },
    {
      "evidence_id": "stage7e-e03",
      "type": "AMBIGUOUS",
      "claim": "A8R has mixed execution evidence because low-cost G8 timed out while low-cost G9 and strong G8/G9 passed.",
      "source": "research/05_analysis/stage-reports/stage-7r-revised-atoms-summary.md"
    },
    {
      "evidence_id": "stage7e-e04",
      "type": "EXTRACTED",
      "claim": "Stage 7r.2 admits a narrow evidence-bound decision macro and blocks full project initialization and full research workflow composition.",
      "source": "research/05_analysis/stage-reports/stage-7r2-composition-readiness-gate.md"
    },
    {
      "evidence_id": "stage7e-e05",
      "type": "EXTRACTED",
      "claim": "No supplied evidence supports production readiness or universal model-gap closure.",
      "source": "input.md"
    },
    {
      "evidence_id": "stage7e-e06",
      "type": "PROPOSED",
      "claim": "Run Stage 7e v3 local golden/bad checks and then a targeted low-cost-model smoke before broader macro expansion.",
      "source": "research/05_analysis/stage-reports/stage-7e-v2-retention-decision-summary.md"
    },
    {
      "evidence_id": "stage7e-e07",
      "type": "EXTRACTED",
      "claim": "Stage 7e v2 repaired trace and stage-gate retention in 4/4 low-cost-model runs.",
      "source": "research/05_analysis/stage-reports/stage-7e-v2-retention-decision-summary.md"
    },
    {
      "evidence_id": "stage7e-e08",
      "type": "EXTRACTED",
      "claim": "Stage 7e v2 did not establish full macro stability because 3/4 runs missed explicit unknown-state inventory for Git branch, CI status, and network/API approval.",
      "source": "research/05_analysis/stage-reports/stage-7e-v2-retention-decision-summary.md"
    }
  ]
}
```

## MemorySlice

```json
{
  "slice_id": "stage7e_v3_state_retention_memory_001",
  "must_load": [
    "Stage 7r.1 targeted smoke completed 8/8 and passed 8/8",
    "Stage 7r.2 admits only a narrow evidence-bound decision macro",
    "Stage 7e v2 repaired trace and stage-gate retention",
    "Stage 7e v2 still missed unknown-state inventory in 3/4 runs",
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
  "output_contract_id": "out_stage7e_v3_state_retention_decision_001",
  "format": "json",
  "retention_contract_required": true,
  "state_retention_contract_required": true,
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
      "stage7e_v3_local_gate",
      "stage7e_v3_smoke"
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
  "tool_trace_required": false
}
```

## Task Input

# Stage 7e v3 Input: State-Retention Evidence Decision Packet

You are preparing a bounded research decision packet for the contract-driven harness study.

This v3 task targets the remaining Stage 7e v2 failure: trace and stage-gate retention were repaired, but 3/4 low-cost-model runs missed explicit unknown-state inventory for current Git branch, CI status, and network/API approval.

## Fixed Workspace Snapshot

- `AGENTS.md` is present.
- Stage 7r.1 A2R1/A7R1 targeted smoke is complete.
- Stage 7r.2 composition gate admits only a narrow evidence-bound decision macro.
- Stage 7e v2 repaired trace and stage-gate retention in 4/4 low-cost-model runs.
- Stage 7e v2 did not fully pass because 3/4 runs missed explicit unknown-state inventory.
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
- `stage7e-e06`: The proposed next step is Stage 7e v3 local golden/bad checks followed by a targeted low-cost-model smoke.
- `stage7e-e07`: Stage 7e v2 repaired trace and stage-gate retention in 4/4 low-cost-model runs.
- `stage7e-e08`: Stage 7e v2 did not establish full macro stability because 3/4 runs missed explicit unknown-state inventory for Git branch, CI status, and network/API approval.

## Evidence Type Rules

- EXTRACTED: directly observed from an artifact or source.
- INFERRED: derived from comparing two or more observed facts.
- AMBIGUOUS: conflicting or underdetermined evidence.
- PROPOSED: recommendation, hypothesis, or next action.

## Candidate Claims

- `C1`: The harness universally closes the performance gap between strong and low-cost models.
- `C2`: Mechanism-bound evidence decision workflows are ready for a narrow state-retention v3 smoke under the harness.
- `C3`: The harness is production ready.

## Stage Status

- mechanism_atom_evidence: complete
- stage7e_v2_retention_smoke: complete
- stage7e_v3_macro_fixture: local_design
- stage7e_v3_local_gate: not_started
- stage7e_v3_smoke: not_started
- final_recommendation: blocked
- full_project_initialization: blocked
- full_research_workflow: blocked

## State Retention Contract

The output must preserve unknown-state obligations explicitly.

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
- `missing_prerequisites` must include `stage7e_v3_local_gate` and `stage7e_v3_smoke`.
- `next_required_actions` must include local golden/bad checks and the targeted low-cost-model smoke.

Carried obligations:

- Exclude stale universal-gap-closure and production-readiness context.
- Do not claim production readiness.
- Do not claim universal model-gap closure.
- Do not claim full project initialization or full research workflow readiness.

Return one JSON object satisfying the output contract.

## Output Requirements

Return `json` and include these required fields/sections: `state_inventory`, `grounded_claims`, `unsupported_claims`, `typed_evidence`, `selected_claim`, `rejected_options`, `decision_trace`, `stage_gate`, `carried_obligations`.
Citation policy: `claim_level_and_decision_trace`.
