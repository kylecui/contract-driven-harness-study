```json
{
  "state_inventory": {
    "known_state": [
      {
        "state_id": "stage7r1_targeted_smoke_complete",
        "fact": "Stage 7r.1 targeted smoke completed 8/8 and passed 8/8 runs.",
        "evidence_ids": ["stage7e-e01"]
      },
      {
        "state_id": "stage7r2_narrow_macro_admitted",
        "fact": "Stage 7r.2 admits only a narrow evidence-bound decision macro.",
        "evidence_ids": ["stage7e-e04"]
      },
      {
        "state_id": "stage7e_v2_trace_gate_retention_repaired",
        "fact": "Stage 7e v2 repaired trace and stage-gate retention in 4/4 low-cost-model runs.",
        "evidence_ids": ["stage7e-e07"]
      },
      {
        "state_id": "stage7e_v3_unknown_state_retention_repaired",
        "fact": "Stage 7e v3 repaired Git/CI/network unknown-state retention in 4/4 low-cost-model runs.",
        "evidence_ids": ["stage7e-e08"]
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
      "do_not_infer_network_api_approval"
    ]
  },
  "grounded_claims": [
    {
      "claim": "Mechanism-bound evidence decision workflows are ready for a narrow known-state-provenance v4 smoke under the harness.",
      "evidence_ids": ["stage7e-e01", "stage7e-e04", "stage7e-e07", "stage7e-e08"]
    }
  ],
  "unsupported_claims": [
    {
      "claim": "The harness universally closes the performance gap between strong and low-cost models.",
      "reason": "No evidence supports universal gap closure; only evidence for narrow known-state-provenance repair is available."
    },
    {
      "claim": "The harness is production ready.",
      "reason": "No supplied evidence supports production readiness."
    }
  ],
  "typed_evidence": [
    {
      "evidence_id": "stage7e-e01",
      "type": "EXTRACTED",
      "claim": "Stage 7r.1 completed 8/8 targeted smoke runs and passed 8/8 under low-cost-model G8/G9."
    },
    {
      "evidence_id": "stage7e-e02",
      "type": "INFERRED",
      "claim": "Stage 7r.1 supports the mechanism-first repair hypothesis for A2R/A7R low-cost-model failures."
    },
    {
      "evidence_id": "stage7e-e03",
      "type": "AMBIGUOUS",
      "claim": "A8R has mixed execution evidence because low-cost G8 timed out while low-cost G9 and strong G8/G9 passed."
    },
    {
      "evidence_id": "stage7e-e04",
      "type": "EXTRACTED",
      "claim": "Stage 7r.2 admits a narrow evidence-bound decision macro and blocks full project initialization and full research workflow composition."
    },
    {
      "evidence_id": "stage7e-e05",
      "type": "EXTRACTED",
      "claim": "No supplied evidence supports production readiness or universal model-gap closure."
    },
    {
      "evidence_id": "stage7e-e06",
      "type": "PROPOSED",
      "claim": "Run Stage 7e v4 local golden/bad checks and then a targeted low-cost-model smoke before broader macro expansion."
    },
    {
      "evidence_id": "stage7e-e07",
      "type": "EXTRACTED",
      "claim": "Stage 7e v2 repaired trace and stage-gate retention in 4/4 low-cost-model runs."
    },
    {
      "evidence_id": "stage7e-e08",
      "type": "EXTRACTED",
      "claim": "Stage 7e v3 repaired Git/CI/network unknown-state retention in 4/4 low-cost-model runs and passed full strict macro evaluation in 3/4 runs."
    },
    {
      "evidence_id": "stage7e-e09",
      "type": "EXTRACTED",
      "claim": "Stage 7e v3 still had one G8 run fail because it compressed known-state provenance into generic labels rather than preserving explicit Stage 7r.1/Stage 7r.2 evidence-linked state."
    }
  ],
  "selected_claim": {
    "option_id": "C2",
    "claim": "Mechanism-bound evidence decision workflows are ready for a narrow known-state-provenance v4 smoke under the harness.",
    "evidence_ids": ["stage7e-e01", "stage7e-e04", "stage7e-e07", "stage7e-e08"]
  },
  "rejected_options": [
    {
      "option_id": "C1",
      "reason": "No evidence supports universal gap closure; only evidence for narrow known-state-provenance repair is available.",
      "evidence_ids": ["stage7e-e05"]
    },
    {
      "option_id": "C3",
      "reason": "No supplied evidence supports production readiness.",
      "evidence_ids": ["stage7e-e05"]
    }
  ],
  "decision_trace": [
    {
      "option_id": "C2",
      "decision": "Support",
      "evidence_ids": ["stage7e-e01", "stage7e-e04", "stage7e-e07", "stage7e-e08"],
      "carried_obligations": ["exclude stale universal-gap-closure and production-readiness note", "do not claim production readiness", "do not claim universal model-gap closure", "do not claim full project initialization or full research workflow readiness"]
    },
    {
      "option_id": "C1",
      "decision": "Reject",
      "evidence_ids": ["stage7e-e05"],
      "carried_obligations": ["exclude stale universal-gap-closure and production-readiness note", "do not claim production readiness", "do not claim universal model-gap closure", "do not claim full project initialization or full research workflow readiness"]
    },
    {
      "option_id": "C3",
      "decision": "Reject",
      "evidence_ids": ["stage7e-e05"],
      "carried_obligations": ["exclude stale universal-gap-closure and production-readiness note", "do not claim production readiness", "do not claim universal model-gap closure", "do not claim full project initialization or full research workflow readiness"]
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
      "Run Stage 7e v4 local golden/bad checks",
      "Run targeted low-cost-model smoke"
    ]
  },
  "carried_obligations": [
    {
      "obligation": "exclude stale universal-gap-closure and production-readiness note",
      "status": "satisfied",
      "evidence_ids": ["stage7e-e05"]
    },
    {
      "obligation": "do not claim production readiness",
      "status": "satisfied",
      "evidence_ids": ["stage7e-e05"]
    },
    {
      "obligation": "do not claim universal model-gap closure",
      "status": "satisfied",
      "evidence_ids": ["stage7e-e05"]
    },
    {
      "obligation": "do not claim full project initialization or full research workflow readiness",
      "status": "satisfied",
      "evidence_ids": ["stage7e-e04"]
    }
  ]
}
```