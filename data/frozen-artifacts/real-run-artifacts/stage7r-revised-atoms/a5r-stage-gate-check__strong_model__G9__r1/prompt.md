# Benchmark Run: a5r-stage-gate-check__strong_model__G9__r1

You are completing a benchmark task. Follow the instructions for the assigned harness arm.

- Fixture: `a5r-stage-gate-check`
- Model tier: `strong_model`
- Harness arm: `G9`
- Task type: `mechanism_atom`

## Harness Arm G9

Use the full harness packet. Obey the task spec, preserve evidence IDs for important claims, respect memory boundaries, and satisfy the output contract.

## TaskSpec

```json
{
  "task_id": "stage7r_a5r_stage_gate_check",
  "task_type": "mechanism_atom",
  "objective": "Apply stage-gate rules to decide whether synthesis and recommendation may proceed.",
  "constraints": [
    "Do not synthesize when evidence_ledger is incomplete.",
    "Do not recommend when citation_audit is not_started.",
    "Return missing prerequisites explicitly."
  ],
  "success_conditions": [
    "gate_decision blocks synthesis and recommendation.",
    "missing_prerequisites includes evidence_ledger and citation_audit.",
    "next_required_actions are limited to completing missing prerequisites."
  ]
}
```

## EvidenceBundle

```json
{
  "bundle_id": "stage7r_a5r_evidence_001",
  "items": [
    {
      "evidence_id": "atom-a5r-e01",
      "type": "EXTRACTED",
      "claim": "Evidence ledger is incomplete.",
      "source": "input.md"
    },
    {
      "evidence_id": "atom-a5r-e02",
      "type": "EXTRACTED",
      "claim": "Citation audit is not_started.",
      "source": "input.md"
    },
    {
      "evidence_id": "atom-a5r-e03",
      "type": "EXTRACTED",
      "claim": "Synthesis requires completed brief, source index, and evidence ledger.",
      "source": "input.md"
    }
  ]
}
```

## MemorySlice

```json
{
  "slice_id": "stage7r_a5r_memory_001",
  "must_load": [
    "research_brief is complete",
    "source_index is complete",
    "evidence_ledger is incomplete",
    "citation_audit is not_started"
  ],
  "must_not_load": [
    "permission to synthesize",
    "permission to issue final recommendation"
  ],
  "staleness_policy": "fixed_snapshot"
}
```

## OutputContract

```json
{
  "output_contract_id": "out_stage7r_a5r_stage_gate_check_001",
  "format": "json",
  "required_sections": [
    "stage_status",
    "gate_decision",
    "missing_prerequisites",
    "blocked_outputs",
    "next_required_actions",
    "evidence_ids"
  ],
  "citation_policy": "gate_decision_support",
  "style_profile": "minimal_json",
  "tool_trace_required": false
}
```

## Task Input

# Stage7r A5R Input: Stage Gate Check

You are preparing a research synthesis.

Stage status:
- research_brief: complete
- source_index: complete
- evidence_ledger: incomplete
- citation_audit: not_started

Policy:
- Synthesis may proceed only when `research_brief`, `source_index`, and `evidence_ledger` are complete.
- Final recommendation may proceed only after citation audit is complete.

Return a stage-gate decision.

## Output Requirements

Return `json` and include these required fields/sections: `stage_status`, `gate_decision`, `missing_prerequisites`, `blocked_outputs`, `next_required_actions`, `evidence_ids`.
Citation policy: `gate_decision_support`.
