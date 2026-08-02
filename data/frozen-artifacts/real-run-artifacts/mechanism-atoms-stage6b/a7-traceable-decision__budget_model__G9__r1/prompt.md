# Benchmark Run: a7-traceable-decision__budget_model__G9__r1

You are completing a benchmark task. Follow the instructions for the assigned harness arm.

- Fixture: `a7-traceable-decision`
- Model tier: `budget_model`
- Harness arm: `G9`
- Task type: `mechanism_atom`

## Harness Arm G9

Use the full harness packet. Obey the task spec, preserve evidence IDs for important claims, respect memory boundaries, and satisfy the output contract.

## TaskSpec

```json
{
  "task_spec_version": "0.1.0",
  "task_id": "mechanism_a7_traceable_decision_001",
  "task_type": "mechanism_atom",
  "intent": {
    "goal": "Choose a claim level and provide a compact trace of the decision criteria used.",
    "language": "en",
    "freshness": "local_snapshot"
  },
  "constraints": [
    "Primary mechanism under test: TraceLog.",
    "Dominant failure mode: Non-observable reasoning.",
    "Return only information supported by the fixture."
  ],
  "required_skills": [],
  "allowed_tools": [],
  "risk_profile": "medium",
  "memory_slice_id": "mem_mechanism_a7_traceable_decision_001",
  "evidence_bundle_id": "ev_mechanism_a7_traceable_decision_001",
  "output_contract_id": "out_mechanism_a7_traceable_decision_001"
}
```

## EvidenceBundle

```json
{
  "evidence_bundle_id": "ev_mechanism_a7_traceable_decision_001",
  "task_id": "mechanism_a7_traceable_decision_001",
  "items": [
    {
      "source_id": "a7-fixture",
      "evidence_id": "atom-a7-e01",
      "evidence_type": "EXTRACTED",
      "claim": "Primary evidence for Traceable Decision.",
      "freshness": "local_snapshot",
      "authority": "fixture"
    },
    {
      "source_id": "a7-fixture",
      "evidence_id": "atom-a7-e02",
      "evidence_type": "INFERRED",
      "claim": "Supporting evidence for Non-observable reasoning.",
      "freshness": "local_snapshot",
      "authority": "fixture"
    }
  ]
}
```

## MemorySlice

```json
{
  "memory_slice_id": "mem_mechanism_a7_traceable_decision_001",
  "task_id": "mechanism_a7_traceable_decision_001",
  "active_topic_id": "mechanism_atom_a7",
  "mode": "task",
  "must_load": [
    "Options: gap compression, weak-model enablement, composition-boundary framing. Evidence says baseline gap is n/a but budget model improves strongly."
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
  "output_contract_id": "out_mechanism_a7_traceable_decision_001",
  "format": "json",
  "required_sections": [
    "decision",
    "criteria_used",
    "evidence_ids",
    "trace"
  ],
  "citation_policy": "important_claims",
  "style_profile": "minimal_json",
  "tool_trace_required": true
}
```

## Task Input

Options: gap compression, weak-model enablement, composition-boundary framing. Evidence says baseline gap is n/a but budget model improves strongly.

## Output Requirements

Return `json` and include these required fields/sections: `decision`, `criteria_used`, `evidence_ids`, `trace`.
Citation policy: `important_claims`.
If tools are used, preserve a trace of what was used and why.
