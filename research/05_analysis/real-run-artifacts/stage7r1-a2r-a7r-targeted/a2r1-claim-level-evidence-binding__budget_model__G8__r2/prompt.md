# Benchmark Run: a2r1-claim-level-evidence-binding__budget_model__G8__r2

You are completing a benchmark task. Follow the instructions for the assigned harness arm.

- Fixture: `a2r1-claim-level-evidence-binding`
- Model tier: `budget_model`
- Harness arm: `G8`
- Task type: `mechanism_atom`

## Harness Arm G8

Use the harness layers provided in this packet.

## TaskSpec

```json
{
  "task_id": "stage7r1_a2r1_claim_level_evidence_binding",
  "task_type": "mechanism_atom",
  "objective": "Classify candidate claims and bind every grounded claim to its own evidence IDs.",
  "constraints": [
    "Every grounded_claims item must be an object, not a string.",
    "Every grounded_claims item must contain non-empty evidence_ids.",
    "Unsupported production readiness must not appear in grounded_claims.",
    "A global evidence_ids field may be present but cannot replace claim-level evidence binding."
  ],
  "success_conditions": [
    "Two supported claims are grounded with claim-level evidence IDs.",
    "Production readiness is listed as unsupported.",
    "No bare strings appear in grounded_claims."
  ]
}
```

## EvidenceBundle

```json
{
  "bundle_id": "stage7r1_a2r1_evidence_001",
  "items": [
    {
      "evidence_id": "atom-a2r1-e01",
      "type": "EXTRACTED",
      "claim": "G9 improved structured extraction contract adherence.",
      "source": "stage7r input"
    },
    {
      "evidence_id": "atom-a2r1-e02",
      "type": "EXTRACTED",
      "claim": "Research workflow G0 had citation grounding failures.",
      "source": "stage7r input"
    }
  ]
}
```

## MemorySlice

```json
{
  "slice_id": "stage7r1_a2r1_memory_001",
  "must_load": [
    "claim-level evidence binding is required",
    "global evidence list is insufficient",
    "production readiness has no supporting evidence"
  ],
  "must_not_load": [
    "production readiness evidence",
    "global-only citation policy"
  ],
  "staleness_policy": "fixed_snapshot"
}
```

## OutputContract

```json
{
  "output_contract_id": "out_stage7r1_a2r1_claim_level_evidence_binding_001",
  "format": "json",
  "required_sections": [
    "grounded_claims",
    "unsupported_claims",
    "evidence_ids"
  ],
  "citation_policy": "claim_level_required",
  "style_profile": "minimal_json",
  "tool_trace_required": false,
  "schema_notes": {
    "grounded_claims_item": {
      "claim": "string",
      "evidence_ids": [
        "evidence_id"
      ]
    },
    "unsupported_claims_item": {
      "claim": "string",
      "reason": "string"
    },
    "bare_strings_allowed_in_grounded_claims": false
  }
}
```

## Task Input

# Stage7r.1 A2R1 Input: Claim-Level Evidence Binding

The model must classify claims using only the evidence bundle.

Candidate claims:
- G9 improved structured extraction contract adherence.
- Research workflow G0 had citation grounding failures.
- The harness is production ready.

Rules:
- Every grounded claim must be an object with a `claim` string and an `evidence_ids` array.
- A global evidence list is not enough.
- Unsupported claims must be placed in `unsupported_claims` with a reason.
- Do not infer production readiness without an evidence ID.

## Output Requirements

Return `json` and include these required fields/sections: `grounded_claims`, `unsupported_claims`, `evidence_ids`.
Citation policy: `claim_level_required`.
