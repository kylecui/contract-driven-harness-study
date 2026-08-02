# Benchmark Run: structured-extraction__strong_model__G9__r2

You are completing a benchmark task. Follow the instructions for the assigned harness arm.

- Fixture: `structured-extraction`
- Model tier: `strong_model`
- Harness arm: `G9`
- Task type: `structured_extraction`

## Harness Arm G9

Use the full harness packet. Obey the task spec, preserve evidence IDs for important claims, respect memory boundaries, and satisfy the output contract.

## TaskSpec

```json
{
  "task_spec_version": "0.1.0",
  "task_id": "structured_extraction_001",
  "task_type": "structured_extraction",
  "intent": {
    "goal": "Extract project metadata from a fixed proposal excerpt.",
    "language": "en",
    "freshness": "local_snapshot"
  },
  "constraints": [
    "Do not infer missing fields.",
    "Return only fields supported by the evidence bundle.",
    "Mark absent fields as null."
  ],
  "required_skills": [],
  "allowed_tools": [],
  "risk_profile": "low",
  "memory_slice_id": "mem_structured_extraction_001",
  "evidence_bundle_id": "ev_structured_extraction_001",
  "output_contract_id": "out_structured_extraction_001"
}
```

## EvidenceBundle

```json
{
  "evidence_bundle_id": "ev_structured_extraction_001",
  "task_id": "structured_extraction_001",
  "items": [
    {
      "source_id": "fixture-proposal-excerpt",
      "evidence_id": "fixture-e01",
      "evidence_type": "EXTRACTED",
      "claim": "Project title: Topic-Aware Compaction.",
      "freshness": "snapshot",
      "authority": "local_fixture"
    },
    {
      "source_id": "fixture-proposal-excerpt",
      "evidence_id": "fixture-e02",
      "evidence_type": "EXTRACTED",
      "claim": "Target venue: COLM 2026.",
      "freshness": "snapshot",
      "authority": "local_fixture"
    },
    {
      "source_id": "fixture-proposal-excerpt",
      "evidence_id": "fixture-e03",
      "evidence_type": "EXTRACTED",
      "claim": "Primary metric: token savings.",
      "freshness": "snapshot",
      "authority": "local_fixture"
    }
  ]
}
```

## MemorySlice

```json
{
  "memory_slice_id": "mem_structured_extraction_001",
  "task_id": "structured_extraction_001",
  "active_topic_id": "topic_structured_extraction",
  "mode": "task",
  "must_load": [
    "task_spec",
    "evidence_bundle",
    "output_contract"
  ],
  "may_load": [],
  "must_not_load": [
    "unrelated_project_notes",
    "prior_user_preferences"
  ],
  "token_budget": 4000
}
```

## OutputContract

```json
{
  "output_contract_id": "out_structured_extraction_001",
  "format": "json",
  "required_sections": [
    "title",
    "target_venue",
    "primary_metric",
    "evidence_ids"
  ],
  "citation_policy": "every_claim",
  "style_profile": "minimal_json",
  "tool_trace_required": false
}
```

## Task Input

# Fixture Input

Project title: Topic-Aware Compaction.

Target venue: COLM 2026.

Primary metric: token savings.

No backup venue is specified in this fixture.

## Output Requirements

Return `json` and include these required fields/sections: `title`, `target_venue`, `primary_metric`, `evidence_ids`.
Citation policy: `every_claim`.
