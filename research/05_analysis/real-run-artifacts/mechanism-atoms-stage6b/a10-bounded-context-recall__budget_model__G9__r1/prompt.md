# Benchmark Run: a10-bounded-context-recall__budget_model__G9__r1

You are completing a benchmark task. Follow the instructions for the assigned harness arm.

- Fixture: `a10-bounded-context-recall`
- Model tier: `budget_model`
- Harness arm: `G9`
- Task type: `mechanism_atom`

## Harness Arm G9

Use the full harness packet. Obey the task spec, preserve evidence IDs for important claims, respect memory boundaries, and satisfy the output contract.

## TaskSpec

```json
{
  "task_spec_version": "0.1.0",
  "task_id": "mechanism_a10_bounded_context_recall_001",
  "task_type": "mechanism_atom",
  "intent": {
    "goal": "Answer from the active memory slice without importing stale or forbidden context.",
    "language": "en",
    "freshness": "local_snapshot"
  },
  "constraints": [
    "Primary mechanism under test: MemorySlice.",
    "Dominant failure mode: Irrelevant or stale context use.",
    "Return only information supported by the fixture."
  ],
  "required_skills": [],
  "allowed_tools": [],
  "risk_profile": "medium",
  "memory_slice_id": "mem_mechanism_a10_bounded_context_recall_001",
  "evidence_bundle_id": "ev_mechanism_a10_bounded_context_recall_001",
  "output_contract_id": "out_mechanism_a10_bounded_context_recall_001"
}
```

## EvidenceBundle

```json
{
  "evidence_bundle_id": "ev_mechanism_a10_bounded_context_recall_001",
  "task_id": "mechanism_a10_bounded_context_recall_001",
  "items": [
    {
      "source_id": "a10-fixture",
      "evidence_id": "atom-a10-e01",
      "evidence_type": "EXTRACTED",
      "claim": "Primary evidence for Bounded Context Recall.",
      "freshness": "local_snapshot",
      "authority": "fixture"
    },
    {
      "source_id": "a10-fixture",
      "evidence_id": "atom-a10-e02",
      "evidence_type": "INFERRED",
      "claim": "Supporting evidence for Irrelevant or stale context use.",
      "freshness": "local_snapshot",
      "authority": "fixture"
    }
  ]
}
```

## MemorySlice

```json
{
  "memory_slice_id": "mem_mechanism_a10_bounded_context_recall_001",
  "task_id": "mechanism_a10_bounded_context_recall_001",
  "active_topic_id": "mechanism_atom_a10",
  "mode": "task",
  "must_load": [
    "Must-load: current roadmap says Stage 2 is next. Must-not-load: old plan says run another broad workflow slice. Answer what work comes next."
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
  "output_contract_id": "out_mechanism_a10_bounded_context_recall_001",
  "format": "json",
  "required_sections": [
    "answer",
    "used_context",
    "excluded_context"
  ],
  "citation_policy": "important_claims",
  "style_profile": "minimal_json",
  "tool_trace_required": false
}
```

## Task Input

Must-load: current roadmap says Stage 2 is next. Must-not-load: old plan says run another broad workflow slice. Answer what work comes next.

## Output Requirements

Return `json` and include these required fields/sections: `answer`, `used_context`, `excluded_context`.
Citation policy: `important_claims`.
