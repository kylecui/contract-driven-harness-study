# Benchmark Run: a8-evidence-type-separation__strong_model__G8__r1

You are completing a benchmark task. Follow the instructions for the assigned harness arm.

- Fixture: `a8-evidence-type-separation`
- Model tier: `strong_model`
- Harness arm: `G8`
- Task type: `mechanism_atom`

## Harness Arm G8

Use the harness layers provided in this packet.

## TaskSpec

```json
{
  "task_spec_version": "0.1.0",
  "task_id": "mechanism_a8_evidence_type_separation_001",
  "task_type": "mechanism_atom",
  "intent": {
    "goal": "Classify claims by evidence type and prevent recommendations from being presented as extracted facts.",
    "language": "en",
    "freshness": "local_snapshot"
  },
  "constraints": [
    "Primary mechanism under test: EvidenceBundle.",
    "Dominant failure mode: Type leakage.",
    "Return only information supported by the fixture."
  ],
  "required_skills": [],
  "allowed_tools": [],
  "risk_profile": "medium",
  "memory_slice_id": "mem_mechanism_a8_evidence_type_separation_001",
  "evidence_bundle_id": "ev_mechanism_a8_evidence_type_separation_001",
  "output_contract_id": "out_mechanism_a8_evidence_type_separation_001"
}
```

## EvidenceBundle

```json
{
  "evidence_bundle_id": "ev_mechanism_a8_evidence_type_separation_001",
  "task_id": "mechanism_a8_evidence_type_separation_001",
  "items": [
    {
      "source_id": "a8-fixture",
      "evidence_id": "atom-a8-e01",
      "evidence_type": "EXTRACTED",
      "claim": "Primary evidence for Evidence-Type Separation.",
      "freshness": "local_snapshot",
      "authority": "fixture"
    },
    {
      "source_id": "a8-fixture",
      "evidence_id": "atom-a8-e02",
      "evidence_type": "INFERRED",
      "claim": "Supporting evidence for Type leakage.",
      "freshness": "local_snapshot",
      "authority": "fixture"
    },
    {
      "source_id": "a8-fixture",
      "evidence_id": "atom-a8-e03",
      "evidence_type": "AMBIGUOUS",
      "claim": "Composition scalability remains unproven.",
      "freshness": "local_snapshot",
      "authority": "fixture"
    }
  ]
}
```

## MemorySlice

```json
{
  "memory_slice_id": "mem_mechanism_a8_evidence_type_separation_001",
  "task_id": "mechanism_a8_evidence_type_separation_001",
  "active_topic_id": "mechanism_atom_a8",
  "mode": "task",
  "must_load": [
    "Claims include one directly measured result, one inference from multiple slices, one unresolved risk, and one recommended next action."
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
  "output_contract_id": "out_mechanism_a8_evidence_type_separation_001",
  "format": "json",
  "required_sections": [
    "extracted",
    "inferred",
    "ambiguous",
    "proposed"
  ],
  "citation_policy": "every_claim",
  "style_profile": "minimal_json",
  "tool_trace_required": false
}
```

## Task Input

Claims include one directly measured result, one inference from multiple slices, one unresolved risk, and one recommended next action.

## Output Requirements

Return `json` and include these required fields/sections: `extracted`, `inferred`, `ambiguous`, `proposed`.
Citation policy: `every_claim`.
