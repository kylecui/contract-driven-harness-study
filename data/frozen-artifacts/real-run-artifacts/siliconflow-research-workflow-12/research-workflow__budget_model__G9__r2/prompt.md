# Benchmark Run: research-workflow__budget_model__G9__r2

You are completing a benchmark task. Follow the instructions for the assigned harness arm.

- Fixture: `research-workflow`
- Model tier: `budget_model`
- Harness arm: `G9`
- Task type: `research_workflow`

## Harness Arm G9

Use the full harness packet. Obey the task spec, preserve evidence IDs for important claims, respect memory boundaries, and satisfy the output contract.

## TaskSpec

```json
{
  "task_spec_version": "0.1.0",
  "task_id": "research_workflow_001",
  "task_type": "research_workflow",
  "intent": {
    "goal": "Produce a brief, evidence-backed synthesis for a proposed systems paper.",
    "language": "en",
    "freshness": "local_snapshot"
  },
  "constraints": [
    "Separate extracted evidence from inference.",
    "Do not write final conclusions without evidence IDs.",
    "List unresolved research risks."
  ],
  "required_skills": [
    "research-router",
    "research-brief-framer",
    "research-evidence-ledger",
    "research-synthesis"
  ],
  "allowed_tools": [
    "filesystem"
  ],
  "risk_profile": "medium",
  "memory_slice_id": "mem_research_workflow_001",
  "evidence_bundle_id": "ev_research_workflow_001",
  "output_contract_id": "out_research_workflow_001"
}
```

## EvidenceBundle

```json
{
  "evidence_bundle_id": "ev_research_workflow_001",
  "task_id": "research_workflow_001",
  "items": [
    {
      "source_id": "fixture-research-notes",
      "evidence_id": "fixture-rw-e01",
      "evidence_type": "EXTRACTED",
      "claim": "The proposed topic-aware compaction paper currently has a single-model A/B result.",
      "freshness": "snapshot",
      "authority": "local_fixture"
    },
    {
      "source_id": "fixture-research-notes",
      "evidence_id": "fixture-rw-e02",
      "evidence_type": "EXTRACTED",
      "claim": "The proposed harness engineering paper requires cross-model benchmark evidence.",
      "freshness": "snapshot",
      "authority": "local_fixture"
    },
    {
      "source_id": "fixture-research-notes",
      "evidence_id": "fixture-rw-e03",
      "evidence_type": "INFERRED",
      "claim": "The two papers should remain separate until the compaction work has stronger ablation evidence.",
      "freshness": "snapshot",
      "authority": "local_fixture"
    }
  ]
}
```

## MemorySlice

```json
{
  "memory_slice_id": "mem_research_workflow_001",
  "task_id": "research_workflow_001",
  "active_topic_id": "topic_research_workflow",
  "mode": "topic_and_task",
  "must_load": [
    "research_question",
    "evidence_bundle",
    "source_index"
  ],
  "may_load": [
    "prior_synthesis_notes"
  ],
  "must_not_load": [
    "unverified_external_claims"
  ],
  "token_budget": 8000
}
```

## OutputContract

```json
{
  "output_contract_id": "out_research_workflow_001",
  "format": "markdown_report",
  "required_sections": [
    "brief",
    "evidence_summary",
    "synthesis",
    "risks",
    "next_steps"
  ],
  "citation_policy": "important_claims",
  "style_profile": "rigorous_research",
  "tool_trace_required": true
}
```

## Task Input

# Fixture Input

Research the relationship between the two proposal tracks and decide whether they should be combined or separated.

Use the evidence bundle. Do not add outside claims.

## Output Requirements

Return `markdown_report` and include these required fields/sections: `brief`, `evidence_summary`, `synthesis`, `risks`, `next_steps`.
Citation policy: `important_claims`.
If tools are used, preserve a trace of what was used and why.
