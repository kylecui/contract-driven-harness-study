# Benchmark Run: stage7e-evidence-bound-decision__strong_model__G8__r1

You are completing a benchmark task. Follow the instructions for the assigned harness arm.

- Fixture: `stage7e-evidence-bound-decision`
- Model tier: `strong_model`
- Harness arm: `G8`
- Task type: `stage7e_evidence_bound_macro`

## Harness Arm G8

Use the harness layers provided in this packet.

## TaskSpec

```json
{
  "task_id": "stage7e_evidence_bound_decision",
  "task_type": "stage7e_evidence_bound_macro",
  "objective": "Compose admitted mechanisms into one bounded evidence decision packet without using stale context or overclaiming.",
  "composition_chain": [
    "A4R",
    "A2R1",
    "A8R",
    "A7R1",
    "A5R"
  ],
  "constraints": [
    "Use only supplied workspace snapshot and evidence items.",
    "Do not infer Git branch, CI status, or network/API approval.",
    "Exclude the stale context from the decision.",
    "Bind every grounded claim to claim-level evidence IDs.",
    "Classify evidence into EXTRACTED, INFERRED, AMBIGUOUS, or PROPOSED.",
    "Select exactly one candidate claim.",
    "Reject overbroad or unsupported claims with evidence-linked reasons.",
    "Block final recommendation until Stage 7e local gate and smoke are complete.",
    "Carry forward negative obligations."
  ],
  "success_conditions": [
    "State inventory separates known and unknown state.",
    "Grounded claims have claim-level evidence IDs.",
    "Production readiness and universal gap closure are not grounded.",
    "Evidence typing includes EXTRACTED, INFERRED, AMBIGUOUS, and PROPOSED where appropriate.",
    "Selected claim is C2.",
    "Rejected options include C1 and C3 with evidence IDs.",
    "Stage gate blocks final recommendation.",
    "Carried obligations preserve stale-context exclusion and unsupported-production-readiness exclusion."
  ]
}
```

## EvidenceBundle

```json
{
  "bundle_id": "stage7e_evidence_bundle_001",
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
      "claim": "Run Stage 7e local golden/bad checks before any Stage 7e SiliconFlow smoke.",
      "source": "research/05_analysis/stage-reports/stage-7r2-composition-readiness-gate.md"
    }
  ]
}
```

## MemorySlice

```json
{
  "slice_id": "stage7e_memory_001",
  "must_load": [
    "Stage 7r.1 targeted smoke completed 8/8 and passed 8/8",
    "Stage 7r.2 admits only a narrow evidence-bound decision macro",
    "full project initialization remains blocked",
    "full research workflow remains blocked"
  ],
  "must_not_load": [
    "old universal gap-closure note",
    "old production-readiness note",
    "current Git branch",
    "CI status",
    "network/API approval"
  ],
  "staleness_policy": "fixed_snapshot_with_explicit_exclusion"
}
```

## OutputContract

```json
{
  "output_contract_id": "out_stage7e_evidence_bound_decision_001",
  "format": "json",
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
    "stage_gate": [
      "status",
      "blocked_outputs",
      "next_required_actions"
    ],
    "carried_obligations": [
      "obligation",
      "status"
    ]
  },
  "citation_policy": "claim_level_and_decision_trace",
  "style_profile": "minimal_json",
  "tool_trace_required": false
}
```

## Task Input

# Stage 7e Input: Evidence-Bound Decision Packet

You are preparing a bounded research decision packet for the contract-driven harness study.

## Fixed Workspace Snapshot

- `AGENTS.md` is present.
- Stage 7r.1 A2R1/A7R1 targeted smoke is complete.
- Stage 7r.2 composition gate admits only a narrow evidence-bound decision macro.
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

## Evidence Type Rules

- EXTRACTED: directly observed from an artifact or source.
- INFERRED: derived from comparing two or more observed facts.
- AMBIGUOUS: conflicting or underdetermined evidence.
- PROPOSED: recommendation, hypothesis, or next action.

## Candidate Claims

- `C1`: The harness universally closes the performance gap between strong and low-cost models.
- `C2`: Mechanism-bound evidence decision workflows are ready for a narrow composed macro smoke under the harness.
- `C3`: The harness is production ready.

## Stage Status

- mechanism_atom_evidence: complete
- stage7e_macro_fixture: local_design
- stage7e_local_gate: not_started
- stage7e_smoke: not_started
- final_recommendation: blocked

Return one JSON object satisfying the output contract.

## Output Requirements

Return `json` and include these required fields/sections: `state_inventory`, `grounded_claims`, `unsupported_claims`, `typed_evidence`, `selected_claim`, `rejected_options`, `decision_trace`, `stage_gate`, `carried_obligations`.
Citation policy: `claim_level_and_decision_trace`.
