# Benchmark Run: a5-stage-gated-synthesis__strong_model__G8__r1

You are completing a benchmark task. Follow the instructions for the assigned harness arm.

- Fixture: `a5-stage-gated-synthesis`
- Model tier: `strong_model`
- Harness arm: `G8`
- Task type: `mechanism_atom`

## Harness Arm G8

Use the harness layers provided in this packet.

## TaskSpec

```json
{
  "task_spec_version": "0.1.0",
  "task_id": "mechanism_a5_stage_gated_synthesis_001",
  "task_type": "mechanism_atom",
  "intent": {
    "goal": "Produce staged research synthesis without skipping intermediate evidence work.",
    "language": "en",
    "freshness": "local_snapshot"
  },
  "constraints": [
    "Primary mechanism under test: WorkflowGraph.",
    "Dominant failure mode: Stage skipping.",
    "Return only information supported by the fixture."
  ],
  "required_skills": [],
  "allowed_tools": [],
  "risk_profile": "medium",
  "memory_slice_id": "mem_mechanism_a5_stage_gated_synthesis_001",
  "evidence_bundle_id": "ev_mechanism_a5_stage_gated_synthesis_001",
  "output_contract_id": "out_mechanism_a5_stage_gated_synthesis_001"
}
```

## EvidenceBundle

```json
{
  "evidence_bundle_id": "ev_mechanism_a5_stage_gated_synthesis_001",
  "task_id": "mechanism_a5_stage_gated_synthesis_001",
  "items": [
    {
      "source_id": "a5-fixture",
      "evidence_id": "atom-a5-e01",
      "evidence_type": "EXTRACTED",
      "claim": "Primary evidence for Stage-Gated Synthesis.",
      "freshness": "local_snapshot",
      "authority": "fixture"
    },
    {
      "source_id": "a5-fixture",
      "evidence_id": "atom-a5-e02",
      "evidence_type": "INFERRED",
      "claim": "Supporting evidence for Stage skipping.",
      "freshness": "local_snapshot",
      "authority": "fixture"
    }
  ]
}
```

## MemorySlice

```json
{
  "memory_slice_id": "mem_mechanism_a5_stage_gated_synthesis_001",
  "task_id": "mechanism_a5_stage_gated_synthesis_001",
  "active_topic_id": "mechanism_atom_a5",
  "mode": "task",
  "must_load": [
    "Use the supplied evidence to decide whether two proposal tracks should remain separate. Output stage status for brief, evidence, synthesis, recommendation, and risks."
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
  "output_contract_id": "out_mechanism_a5_stage_gated_synthesis_001",
  "format": "json",
  "required_sections": [
    "brief",
    "evidence_summary",
    "synthesis",
    "recommendation",
    "risks",
    "stage_status"
  ],
  "citation_policy": "every_claim",
  "style_profile": "minimal_json",
  "tool_trace_required": true
}
```

## Task Input

Use the supplied evidence to decide whether two proposal tracks should remain separate. Output stage status for brief, evidence, synthesis, recommendation, and risks.

## Output Requirements

Return `json` and include these required fields/sections: `brief`, `evidence_summary`, `synthesis`, `recommendation`, `risks`, `stage_status`.
Citation policy: `every_claim`.
If tools are used, preserve a trace of what was used and why.
