# Benchmark Run: a4r-strict-state-inventory__budget_model__G9__r1

You are completing a benchmark task. Follow the instructions for the assigned harness arm.

- Fixture: `a4r-strict-state-inventory`
- Model tier: `budget_model`
- Harness arm: `G9`
- Task type: `mechanism_atom`

## Harness Arm G9

Use the full harness packet. Obey the task spec, preserve evidence IDs for important claims, respect memory boundaries, and satisfy the output contract.

## TaskSpec

```json
{
  "task_id": "stage7r_a4r_strict_state_inventory",
  "task_type": "mechanism_atom",
  "objective": "Inventory known and unknown workspace state without inference.",
  "constraints": [
    "Use only the supplied fixed snapshot.",
    "Mark unstated values as unknown.",
    "Do not infer CI status, Git branch, or network approval."
  ],
  "success_conditions": [
    "Known state contains only supplied facts.",
    "Unknown state includes Git branch, CI status, and network approval.",
    "Forbidden inferences are explicit."
  ]
}
```

## EvidenceBundle

```json
{
  "bundle_id": "stage7r_a4r_evidence_001",
  "items": [
    {
      "evidence_id": "atom-a4r-e01",
      "type": "EXTRACTED",
      "claim": "AGENTS.md is present.",
      "source": "input.md"
    },
    {
      "evidence_id": "atom-a4r-e02",
      "type": "EXTRACTED",
      "claim": "Stage7p v2 is complete and Stage7r is pending.",
      "source": "input.md"
    },
    {
      "evidence_id": "atom-a4r-e03",
      "type": "EXTRACTED",
      "claim": "The Stage7p v2 evaluation file exists.",
      "source": "input.md"
    }
  ]
}
```

## MemorySlice

```json
{
  "slice_id": "stage7r_a4r_memory_001",
  "must_load": [
    "AGENTS.md is present",
    "Stage7p v2 is complete",
    "Stage7r is pending",
    "Stage7p v2 evaluation file exists"
  ],
  "must_not_load": [
    "current Git branch",
    "CI status",
    "network execution approval"
  ],
  "staleness_policy": "fixed_snapshot"
}
```

## OutputContract

```json
{
  "output_contract_id": "out_stage7r_a4r_strict_state_inventory_001",
  "format": "json",
  "required_sections": [
    "known_state",
    "unknown_state",
    "forbidden_inferences",
    "evidence_ids"
  ],
  "citation_policy": "known_state_only",
  "style_profile": "minimal_json",
  "tool_trace_required": false
}
```

## Task Input

# Stage7r A4R Input: Strict State Inventory

You are given a fixed workspace snapshot:

- `AGENTS.md` is present.
- `tasks/backlog.md` records Stage7p v2 as complete and Stage7r as pending.
- `research/05_analysis/stage7p-v2-a10-a9-a6-evaluation.md` exists.

The snapshot does not state the current Git branch, CI status, or whether the user has approved network execution.

Return only known state, unknown state, and forbidden inferences.

## Output Requirements

Return `json` and include these required fields/sections: `known_state`, `unknown_state`, `forbidden_inferences`, `evidence_ids`.
Citation policy: `known_state_only`.
