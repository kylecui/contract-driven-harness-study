# Benchmark Run: a2-evidence-grounding__budget_model__G8__r1

You are completing a benchmark task. Follow the instructions for the assigned harness arm.

- Fixture: `a2-evidence-grounding`
- Model tier: `budget_model`
- Harness arm: `G8`
- Task type: `mechanism_atom`

## Harness Arm G8

Use the harness layers provided in this packet.

## TaskSpec

```json
{
  "task_spec_version": "0.1.0",
  "task_id": "mechanism_a2_evidence_grounding_001",
  "task_type": "mechanism_atom",
  "intent": {
    "goal": "Produce an evidence-grounded claim table using only supplied evidence IDs.",
    "language": "en",
    "freshness": "local_snapshot"
  },
  "constraints": [
    "Primary mechanism under test: EvidenceBundle.",
    "Dominant failure mode: Unsupported claim.",
    "Return only information supported by the fixture."
  ],
  "required_skills": [],
  "allowed_tools": [],
  "risk_profile": "medium",
  "memory_slice_id": "mem_mechanism_a2_evidence_grounding_001",
  "evidence_bundle_id": "ev_mechanism_a2_evidence_grounding_001",
  "output_contract_id": "out_mechanism_a2_evidence_grounding_001"
}
```

## EvidenceBundle

```json
{
  "evidence_bundle_id": "ev_mechanism_a2_evidence_grounding_001",
  "task_id": "mechanism_a2_evidence_grounding_001",
  "items": [
    {
      "source_id": "a2-fixture",
      "evidence_id": "atom-a2-e01",
      "evidence_type": "EXTRACTED",
      "claim": "Primary evidence for Evidence Grounding.",
      "freshness": "local_snapshot",
      "authority": "fixture"
    },
    {
      "source_id": "a2-fixture",
      "evidence_id": "atom-a2-e02",
      "evidence_type": "INFERRED",
      "claim": "Supporting evidence for Unsupported claim.",
      "freshness": "local_snapshot",
      "authority": "fixture"
    }
  ]
}
```

## MemorySlice

```json
{
  "memory_slice_id": "mem_mechanism_a2_evidence_grounding_001",
  "task_id": "mechanism_a2_evidence_grounding_001",
  "active_topic_id": "mechanism_atom_a2",
  "mode": "task",
  "must_load": [
    "Evidence bundle contains two usable claims about G9 and one unsupported tempting claim about production readiness. Report only grounded claims."
  ],
  "may_load": [
    "Composition role: Research."
  ],
  "must_not_load": [
    "Old broad workflow plans that bypass mechanism atoms."
  ],
  "token_budget": 1200
}
```

## OutputContract

```json
{
  "output_contract_id": "out_mechanism_a2_evidence_grounding_001",
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

Evidence bundle contains two usable claims about G9 and one unsupported tempting claim about production readiness. Report only grounded claims.

## Output Requirements

Return `json` and include these required fields/sections: `grounded_claims`, `unsupported_claims`, `evidence_ids`.
Citation policy: `every_claim`.
