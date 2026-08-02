# Benchmark Run: structured-extraction-hard__strong_model__G0__r3

You are completing a benchmark task. Follow the instructions for the assigned harness arm.

- Fixture: `structured-extraction-hard`
- Model tier: `strong_model`
- Harness arm: `G0`
- Task type: `structured_extraction_hard`

## Harness Arm G0

Use only the task input below. Do not assume extra schemas, memory, tools, or evidence beyond what is present in the task text.

## TaskSpec

```json
{
  "task_spec_version": "0.1.0",
  "task_id": "structured_extraction_hard_001",
  "task_type": "structured_extraction_hard",
  "intent": {
    "goal": "Extract routing metadata for the active proposal from noisy planning notes with decoys.",
    "language": "en",
    "freshness": "local_snapshot"
  },
  "constraints": [
    "Select only the proposal marked NEXT.",
    "Do not use HOLD proposals or external comparators as the active candidate.",
    "Distinguish primary venue from fallback venue.",
    "Return only fields supported by the evidence bundle.",
    "Mark absent fields as null."
  ],
  "required_skills": [],
  "allowed_tools": [],
  "risk_profile": "medium",
  "memory_slice_id": "mem_structured_extraction_hard_001",
  "evidence_bundle_id": "ev_structured_extraction_hard_001",
  "output_contract_id": "out_structured_extraction_hard_001"
}
```

## Task Input

# Fixture Input

You are preparing routing metadata from messy proposal planning notes. Extract the active proposal to move next. Ignore proposals marked HOLD and ignore comparator methods that are not proposals.

Planning notes:

- [hard-e01] Topic-Aware Compaction is a promising paper, but it is marked HOLD until semantic trajectory labels and ablations are complete. Its target venue is COLM 2026. Its primary metric is token savings.
- [hard-e02] Contract-Driven Agent Harness Engineering is marked NEXT. Its primary target venue is ACL 2026 Findings. Its primary metric is cross-model gap compression.
- [hard-e03] If the benchmark evidence remains partial, Contract-Driven Agent Harness Engineering should use COLM systems workshop as fallback venue.
- [hard-e04] The immediate blocker for Contract-Driven Agent Harness Engineering is proving a nonzero baseline model gap before running the full benchmark.
- [hard-e05] LLMLingua is a comparator family for prompt compression, not a proposal to route.

Return concise routing metadata for the active proposal.

## Output Requirements

Return the best answer for the task in a concise, reviewable form.
