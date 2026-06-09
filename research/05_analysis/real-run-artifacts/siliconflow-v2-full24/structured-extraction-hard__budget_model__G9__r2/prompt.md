# Benchmark Run: structured-extraction-hard__budget_model__G9__r2

You are completing a benchmark task. Follow the instructions for the assigned harness arm.

- Fixture: `structured-extraction-hard`
- Model tier: `budget_model`
- Harness arm: `G9`
- Task type: `structured_extraction_hard`

## Harness Arm G9

Use the full harness packet. Obey the task spec, preserve evidence IDs for important claims, respect memory boundaries, and satisfy the output contract.

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

## EvidenceBundle

```json
{
  "evidence_bundle_id": "ev_structured_extraction_hard_001",
  "task_id": "structured_extraction_hard_001",
  "items": [
    {
      "source_id": "hard-routing-notes",
      "evidence_id": "hard-e01",
      "evidence_type": "EXTRACTED",
      "claim": "Topic-Aware Compaction is marked HOLD with target venue COLM 2026 and primary metric token savings.",
      "freshness": "snapshot",
      "authority": "local_fixture"
    },
    {
      "source_id": "hard-routing-notes",
      "evidence_id": "hard-e02",
      "evidence_type": "EXTRACTED",
      "claim": "Contract-Driven Agent Harness Engineering is marked NEXT with primary venue ACL 2026 Findings and primary metric cross-model gap compression.",
      "freshness": "snapshot",
      "authority": "local_fixture"
    },
    {
      "source_id": "hard-routing-notes",
      "evidence_id": "hard-e03",
      "evidence_type": "EXTRACTED",
      "claim": "If the benchmark evidence remains partial, Contract-Driven Agent Harness Engineering should use COLM systems workshop as fallback venue.",
      "freshness": "snapshot",
      "authority": "local_fixture"
    },
    {
      "source_id": "hard-routing-notes",
      "evidence_id": "hard-e04",
      "evidence_type": "EXTRACTED",
      "claim": "The immediate blocker for Contract-Driven Agent Harness Engineering is proving a nonzero baseline model gap before running the full benchmark.",
      "freshness": "snapshot",
      "authority": "local_fixture"
    },
    {
      "source_id": "hard-routing-notes",
      "evidence_id": "hard-e05",
      "evidence_type": "EXTRACTED",
      "claim": "LLMLingua is a comparator family, not a proposal to route.",
      "freshness": "snapshot",
      "authority": "local_fixture"
    }
  ]
}
```

## MemorySlice

```json
{
  "memory_slice_id": "mem_structured_extraction_hard_001",
  "task_id": "structured_extraction_hard_001",
  "scope": "fixture_local",
  "items": [
    {
      "memory_id": "hard-m01",
      "content": "Only the NEXT proposal is eligible for routing metadata.",
      "topic": "selection_rule"
    },
    {
      "memory_id": "hard-m02",
      "content": "A fallback venue is not the same field as the primary target venue.",
      "topic": "field_disambiguation"
    }
  ]
}
```

## OutputContract

```json
{
  "output_contract_id": "out_structured_extraction_hard_001",
  "format": "json",
  "required_sections": [
    "title",
    "target_venue",
    "fallback_venue",
    "primary_metric",
    "blocker",
    "evidence_ids"
  ],
  "citation_policy": "every_claim",
  "style_profile": "minimal_json",
  "tool_trace_required": false
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

Return `json` and include these required fields/sections: `title`, `target_venue`, `fallback_venue`, `primary_metric`, `blocker`, `evidence_ids`.
Citation policy: `every_claim`.
