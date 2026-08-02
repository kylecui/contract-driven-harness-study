# Benchmark Run: a8-evidence-type-separation__budget_model__G2__r1

You are completing a benchmark task. Follow the instructions for the assigned harness arm.

- Fixture: `a8-evidence-type-separation`
- Model tier: `budget_model`
- Harness arm: `G2`
- Task type: `mechanism_atom`

## Harness Arm G2

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
