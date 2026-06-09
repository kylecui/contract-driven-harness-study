# Benchmark Run: a6-validator-repair__strong_model__G9__r1

You are completing a benchmark task. Follow the instructions for the assigned harness arm.

- Fixture: `a6-validator-repair`
- Model tier: `strong_model`
- Harness arm: `G9`
- Task type: `mechanism_atom`

## Harness Arm G9

Use the full harness packet. Obey the task spec, preserve evidence IDs for important claims, respect memory boundaries, and satisfy the output contract.

## TaskSpec

```json
{
  "task_spec_version": "0.1.0",
  "task_id": "mechanism_a6_validator_repair_001",
  "task_type": "mechanism_atom",
  "intent": {
    "goal": "Return a repaired output that fixes the validator-reported missing evidence_ids field.",
    "language": "en",
    "freshness": "local_snapshot"
  },
  "constraints": [
    "Primary mechanism under test: ValidatorGate.",
    "Dominant failure mode: Repair failure.",
    "Return only information supported by the fixture."
  ],
  "required_skills": [],
  "allowed_tools": [],
  "risk_profile": "medium",
  "memory_slice_id": "mem_mechanism_a6_validator_repair_001",
  "evidence_bundle_id": "ev_mechanism_a6_validator_repair_001",
  "output_contract_id": "out_mechanism_a6_validator_repair_001"
}
```

## EvidenceBundle

```json
{
  "evidence_bundle_id": "ev_mechanism_a6_validator_repair_001",
  "task_id": "mechanism_a6_validator_repair_001",
  "items": [
    {
      "source_id": "a6-fixture",
      "evidence_id": "atom-a6-e01",
      "evidence_type": "EXTRACTED",
      "claim": "Primary evidence for Validator Repair.",
      "freshness": "local_snapshot",
      "authority": "fixture"
    },
    {
      "source_id": "a6-fixture",
      "evidence_id": "atom-a6-e02",
      "evidence_type": "INFERRED",
      "claim": "Supporting evidence for Repair failure.",
      "freshness": "local_snapshot",
      "authority": "fixture"
    }
  ]
}
```

## MemorySlice

```json
{
  "memory_slice_id": "mem_mechanism_a6_validator_repair_001",
  "task_id": "mechanism_a6_validator_repair_001",
  "active_topic_id": "mechanism_atom_a6",
  "mode": "task",
  "must_load": [
    "Original output: {\"title\":\"Contract-Driven Harness\"}. Validator feedback: add missing evidence_ids using atom-a6-e01 and keep all existing valid fields unchanged."
  ],
  "may_load": [
    "Composition role: Shared."
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
  "output_contract_id": "out_mechanism_a6_validator_repair_001",
  "format": "json",
  "required_sections": [
    "repaired_output",
    "repair_trace",
    "remaining_warnings"
  ],
  "citation_policy": "important_claims",
  "style_profile": "minimal_json",
  "tool_trace_required": true
}
```

## Task Input

Original output: {"title":"Contract-Driven Harness"}. Validator feedback: add missing evidence_ids using atom-a6-e01 and keep all existing valid fields unchanged.

## Output Requirements

Return `json` and include these required fields/sections: `repaired_output`, `repair_trace`, `remaining_warnings`.
Citation policy: `important_claims`.
If tools are used, preserve a trace of what was used and why.
