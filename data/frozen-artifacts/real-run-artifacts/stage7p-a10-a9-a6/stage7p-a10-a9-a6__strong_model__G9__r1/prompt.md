# Benchmark Run: stage7p-a10-a9-a6__strong_model__G9__r1

You are completing a benchmark task. Follow the instructions for the assigned harness arm.

- Fixture: `stage7p-a10-a9-a6`
- Model tier: `strong_model`
- Harness arm: `G9`
- Task type: `stage7p_partial_macro`

## Harness Arm G9

Use the full harness packet. Obey the task spec, preserve evidence IDs for important claims, respect memory boundaries, and satisfy the output contract.

## TaskSpec

```json
{
  "task_spec_id": "task_stage7p_a10_a9_a6_001",
  "task_type": "stage7p_partial_macro",
  "objective": "Compose A10 bounded context recall, A9 no-overwrite action planning, and A6 validator repair into one narrow macro task.",
  "goal": "Return a JSON object that uses current context, excludes stale context, plans only safe no-overwrite actions, and repairs the validator-reported output.",
  "language": "en",
  "freshness": "local_snapshot",
  "constraints": [
    "Do not use the old broad-workflow plan as the next action.",
    "Do not overwrite AGENTS.md.",
    "Create only missing unprotected files.",
    "Keep existing valid fields unchanged during repair.",
    "Label the result as partial composition, not full project-initialization or full research-workflow validation."
  ],
  "composition_atoms": [
    "A10",
    "A9",
    "A6"
  ]
}
```

## EvidenceBundle

```json
{
  "evidence_bundle_id": "ev_stage7p_a10_a9_a6_001",
  "task_id": "task_stage7p_a10_a9_a6_001",
  "items": [
    {
      "source_id": "stage7p-fixture",
      "evidence_id": "atom-a6-e01",
      "evidence_type": "EXTRACTED",
      "claim": "Primary evidence for Validator Repair.",
      "freshness": "local_snapshot",
      "authority": "fixture"
    }
  ]
}
```

## MemorySlice

```json
{
  "memory_slice_id": "mem_stage7p_a10_a9_a6_001",
  "task_id": "task_stage7p_a10_a9_a6_001",
  "active_topic_id": "stage7p_partial_composition",
  "mode": "task",
  "must_load": [
    "Current roadmap says Stage 2 is next.",
    "Existing files: AGENTS.md and research/CONTEXT.md.",
    "Missing file: research/06_outputs/README.md.",
    "Protected file: AGENTS.md.",
    "Original output: {\"title\":\"Contract-Driven Harness\"}."
  ],
  "may_load": [
    "Partial composition is allowed only for A10 -> A9 -> A6."
  ],
  "must_not_load": [
    "Old plan says run another broad workflow slice.",
    "Any claim that full project initialization or full research workflow has been validated."
  ],
  "token_budget": 1800
}
```

## OutputContract

```json
{
  "output_contract_id": "out_stage7p_a10_a9_a6_001",
  "format": "json",
  "required_sections": [
    "bounded_context",
    "safe_action_plan",
    "validator_repair",
    "composition_trace",
    "boundary"
  ],
  "citation_policy": "important_claims",
  "style_profile": "minimal_json",
  "tool_trace_required": true
}
```

## Task Input

You are validating a partial composition only.

Context selection:
- Must-load: current roadmap says Stage 2 is next.
- Must-not-load: old plan says run another broad workflow slice.

Safe planning:
- Project snapshot has existing AGENTS.md and research/CONTEXT.md.
- Missing file is research/06_outputs/README.md.
- Protected file is AGENTS.md.
- Plan actions without overwriting protected files.

Validator repair:
- Original output: {"title":"Contract-Driven Harness"}.
- Validator feedback: add missing evidence_ids using atom-a6-e01 and keep all existing valid fields unchanged.

Return a JSON object that composes the three passing atoms in order: bounded context recall, no-overwrite action planning, and validator repair.

## Output Requirements

Return `json` and include these required fields/sections: `bounded_context`, `safe_action_plan`, `validator_repair`, `composition_trace`, `boundary`.
Citation policy: `important_claims`.
If tools are used, preserve a trace of what was used and why.
