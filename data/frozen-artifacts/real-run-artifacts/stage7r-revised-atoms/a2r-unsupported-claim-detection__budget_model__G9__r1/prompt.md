# Benchmark Run: a2r-unsupported-claim-detection__budget_model__G9__r1

You are completing a benchmark task. Follow the instructions for the assigned harness arm.

- Fixture: `a2r-unsupported-claim-detection`
- Model tier: `budget_model`
- Harness arm: `G9`
- Task type: `mechanism_atom`

## Harness Arm G9

Use the full harness packet. Obey the task spec, preserve evidence IDs for important claims, respect memory boundaries, and satisfy the output contract.

## TaskSpec

```json
{
  "task_spec_version": "0.2.0-stage7r",
  "task_id": "stage7r_a2r_unsupported_claim_detection_001",
  "task_type": "mechanism_atom",
  "intent": {
    "goal": "Return supported claims with evidence IDs and reject unsupported production-readiness claims.",
    "language": "en",
    "freshness": "local_snapshot"
  },
  "constraints": [
    "Every grounded claim must cite at least one supplied evidence_id.",
    "The phrase production readiness must appear only in unsupported_claims.",
    "Do not create evidence IDs."
  ],
  "required_skills": [],
  "allowed_tools": [],
  "risk_profile": "medium",
  "memory_slice_id": "mem_stage7r_a2r_unsupported_claim_detection_001",
  "evidence_bundle_id": "ev_stage7r_a2r_unsupported_claim_detection_001",
  "output_contract_id": "out_stage7r_a2r_unsupported_claim_detection_001"
}
```

## EvidenceBundle

```json
{
  "evidence_bundle_id": "ev_stage7r_a2r_unsupported_claim_detection_001",
  "task_id": "stage7r_a2r_unsupported_claim_detection_001",
  "items": [
    {
      "source_id": "stage7r-a2r-fixture",
      "evidence_id": "atom-a2r-e01",
      "evidence_type": "EXTRACTED",
      "claim": "G9 improved structured extraction contract adherence.",
      "freshness": "local_snapshot",
      "authority": "fixture"
    },
    {
      "source_id": "stage7r-a2r-fixture",
      "evidence_id": "atom-a2r-e02",
      "evidence_type": "INFERRED",
      "claim": "Research workflow G0 had citation grounding failures.",
      "freshness": "local_snapshot",
      "authority": "fixture"
    }
  ]
}
```

## MemorySlice

```json
{
  "memory_slice_id": "mem_stage7r_a2r_unsupported_claim_detection_001",
  "task_id": "stage7r_a2r_unsupported_claim_detection_001",
  "active_topic_id": "stage7r_a2r",
  "mode": "task",
  "must_load": [
    "Two claims are supported by evidence IDs.",
    "Production readiness is a tempting unsupported claim and must be rejected."
  ],
  "may_load": [
    "Composition role: research evidence ledger."
  ],
  "must_not_load": [
    "Any external evidence about production readiness."
  ],
  "token_budget": 1200
}
```

## OutputContract

```json
{
  "output_contract_id": "out_stage7r_a2r_unsupported_claim_detection_001",
  "format": "json",
  "required_sections": [
    "grounded_claims",
    "unsupported_claims",
    "evidence_ids"
  ],
  "citation_policy": "every_claim",
  "style_profile": "minimal_json",
  "tool_trace_required": false
}
```

## Task Input

Evidence bundle contains two supported claims and one tempting unsupported claim: production readiness. Return grounded claims with evidence IDs and explicitly list unsupported claims.

## Output Requirements

Return `json` and include these required fields/sections: `grounded_claims`, `unsupported_claims`, `evidence_ids`.
Citation policy: `every_claim`.
