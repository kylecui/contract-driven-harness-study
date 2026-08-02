# Benchmark Run: a3-constraint-safe-planning__strong_model__G9__r1

You are completing a benchmark task. Follow the instructions for the assigned harness arm.

- Fixture: `a3-constraint-safe-planning`
- Model tier: `strong_model`
- Harness arm: `G9`
- Task type: `mechanism_atom`

## Harness Arm G9

Use the full harness packet. Obey the task spec, preserve evidence IDs for important claims, respect memory boundaries, and satisfy the output contract.

## TaskSpec

```json
{
  "task_spec_version": "0.1.0",
  "task_id": "mechanism_a3_constraint_safe_planning_001",
  "task_type": "mechanism_atom",
  "intent": {
    "goal": "Plan project initialization without violating protected-file constraints.",
    "language": "en",
    "freshness": "local_snapshot"
  },
  "constraints": [
    "Primary mechanism under test: TaskSpec.",
    "Dominant failure mode: Constraint violation.",
    "Return only information supported by the fixture."
  ],
  "required_skills": [],
  "allowed_tools": [],
  "risk_profile": "medium",
  "memory_slice_id": "mem_mechanism_a3_constraint_safe_planning_001",
  "evidence_bundle_id": "ev_mechanism_a3_constraint_safe_planning_001",
  "output_contract_id": "out_mechanism_a3_constraint_safe_planning_001"
}
```

## EvidenceBundle

```json
{
  "evidence_bundle_id": "ev_mechanism_a3_constraint_safe_planning_001",
  "task_id": "mechanism_a3_constraint_safe_planning_001",
  "items": [
    {
      "source_id": "a3-fixture",
      "evidence_id": "atom-a3-e01",
      "evidence_type": "EXTRACTED",
      "claim": "Primary evidence for Constraint-Safe Planning.",
      "freshness": "local_snapshot",
      "authority": "fixture"
    },
    {
      "source_id": "a3-fixture",
      "evidence_id": "atom-a3-e02",
      "evidence_type": "INFERRED",
      "claim": "Supporting evidence for Constraint violation.",
      "freshness": "local_snapshot",
      "authority": "fixture"
    }
  ]
}
```

## MemorySlice

```json
{
  "memory_slice_id": "mem_mechanism_a3_constraint_safe_planning_001",
  "task_id": "mechanism_a3_constraint_safe_planning_001",
  "active_topic_id": "mechanism_atom_a3",
  "mode": "task",
  "must_load": [
    "Project snapshot has existing AGENTS.md and missing research/06_outputs/README.md. Plan actions without overwriting protected files."
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
  "output_contract_id": "out_mechanism_a3_constraint_safe_planning_001",
  "format": "json",
  "required_sections": [
    "allowed_actions",
    "blocked_actions",
    "risks",
    "next_steps"
  ],
  "citation_policy": "important_claims",
  "style_profile": "minimal_json",
  "tool_trace_required": false
}
```

## Task Input

Project snapshot has existing AGENTS.md and missing research/06_outputs/README.md. Plan actions without overwriting protected files.

## Output Requirements

Return `json` and include these required fields/sections: `allowed_actions`, `blocked_actions`, `risks`, `next_steps`.
Citation policy: `important_claims`.
