# Benchmark Run: a4-state-inventory__budget_model__G8__r1

You are completing a benchmark task. Follow the instructions for the assigned harness arm.

- Fixture: `a4-state-inventory`
- Model tier: `budget_model`
- Harness arm: `G8`
- Task type: `mechanism_atom`

## Harness Arm G8

Use the harness layers provided in this packet.

## TaskSpec

```json
{
  "task_spec_version": "0.1.0",
  "task_id": "mechanism_a4_state_inventory_001",
  "task_type": "mechanism_atom",
  "intent": {
    "goal": "Inventory project state without guessing absent filesystem facts.",
    "language": "en",
    "freshness": "local_snapshot"
  },
  "constraints": [
    "Primary mechanism under test: MemorySlice.",
    "Dominant failure mode: State hallucination.",
    "Return only information supported by the fixture."
  ],
  "required_skills": [],
  "allowed_tools": [],
  "risk_profile": "medium",
  "memory_slice_id": "mem_mechanism_a4_state_inventory_001",
  "evidence_bundle_id": "ev_mechanism_a4_state_inventory_001",
  "output_contract_id": "out_mechanism_a4_state_inventory_001"
}
```

## EvidenceBundle

```json
{
  "evidence_bundle_id": "ev_mechanism_a4_state_inventory_001",
  "task_id": "mechanism_a4_state_inventory_001",
  "items": [
    {
      "source_id": "a4-fixture",
      "evidence_id": "atom-a4-e01",
      "evidence_type": "EXTRACTED",
      "claim": "Primary evidence for State Inventory.",
      "freshness": "local_snapshot",
      "authority": "fixture"
    },
    {
      "source_id": "a4-fixture",
      "evidence_id": "atom-a4-e02",
      "evidence_type": "INFERRED",
      "claim": "Supporting evidence for State hallucination.",
      "freshness": "local_snapshot",
      "authority": "fixture"
    }
  ]
}
```

## MemorySlice

```json
{
  "memory_slice_id": "mem_mechanism_a4_state_inventory_001",
  "task_id": "mechanism_a4_state_inventory_001",
  "active_topic_id": "mechanism_atom_a4",
  "mode": "task",
  "must_load": [
    "Snapshot: existing files are AGENTS.md and research/CONTEXT.md. Missing file is research/06_outputs/README.md. Protected file is AGENTS.md. Do not infer other files."
  ],
  "may_load": [
    "Composition role: Project."
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
  "output_contract_id": "out_mechanism_a4_state_inventory_001",
  "format": "json",
  "required_sections": [
    "existing_files",
    "missing_files",
    "protected_files",
    "unknown_state"
  ],
  "citation_policy": "important_claims",
  "style_profile": "minimal_json",
  "tool_trace_required": false
}
```

## Task Input

Snapshot: existing files are AGENTS.md and research/CONTEXT.md. Missing file is research/06_outputs/README.md. Protected file is AGENTS.md. Do not infer other files.

## Output Requirements

Return `json` and include these required fields/sections: `existing_files`, `missing_files`, `protected_files`, `unknown_state`.
Citation policy: `important_claims`.
