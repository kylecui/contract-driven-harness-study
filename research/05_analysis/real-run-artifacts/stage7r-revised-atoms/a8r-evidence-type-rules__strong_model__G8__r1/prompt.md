# Benchmark Run: a8r-evidence-type-rules__strong_model__G8__r1

You are completing a benchmark task. Follow the instructions for the assigned harness arm.

- Fixture: `a8r-evidence-type-rules`
- Model tier: `strong_model`
- Harness arm: `G8`
- Task type: `mechanism_atom`

## Harness Arm G8

Use the harness layers provided in this packet.

## TaskSpec

```json
{
  "task_id": "stage7r_a8r_evidence_type_rules",
  "task_type": "mechanism_atom",
  "objective": "Classify each item into exactly one evidence type using the supplied rules.",
  "constraints": [
    "Use only EXTRACTED, INFERRED, AMBIGUOUS, PROPOSED.",
    "Classify each item exactly once.",
    "Do not resolve ambiguous items as facts."
  ],
  "success_conditions": [
    "I1 is EXTRACTED.",
    "I2 is INFERRED.",
    "I3 and I4 are PROPOSED.",
    "I5 is AMBIGUOUS."
  ]
}
```

## EvidenceBundle

```json
{
  "bundle_id": "stage7r_a8r_evidence_001",
  "items": [
    {
      "evidence_id": "atom-a8r-e01",
      "type": "EXTRACTED",
      "claim": "I1 is a directly observed adapter completion result.",
      "source": "input.md"
    },
    {
      "evidence_id": "atom-a8r-e02",
      "type": "EXTRACTED",
      "claim": "I2 is derived from comparing G0 and G8/G9 outcomes.",
      "source": "input.md"
    },
    {
      "evidence_id": "atom-a8r-e03",
      "type": "EXTRACTED",
      "claim": "I5 contains conflicting notes about gap compression.",
      "source": "input.md"
    }
  ]
}
```

## MemorySlice

```json
{
  "slice_id": "stage7r_a8r_memory_001",
  "must_load": [
    "evidence type rules",
    "items I1 through I5"
  ],
  "must_not_load": [
    "unstated evidence resolving I5"
  ],
  "staleness_policy": "fixed_snapshot"
}
```

## OutputContract

```json
{
  "output_contract_id": "out_stage7r_a8r_evidence_type_rules_001",
  "format": "json",
  "required_sections": [
    "extracted",
    "inferred",
    "ambiguous",
    "proposed",
    "evidence_ids"
  ],
  "citation_policy": "classification_support",
  "style_profile": "minimal_json",
  "tool_trace_required": false
}
```

## Task Input

# Stage7r A8R Input: Evidence Type Rules

Classify each item into exactly one evidence type.

Rules:
- `EXTRACTED`: directly observed from an artifact or source.
- `INFERRED`: derived by comparing two or more observed facts.
- `AMBIGUOUS`: conflicting or underdetermined evidence.
- `PROPOSED`: recommendation, hypothesis, or next action.

Items:
- `I1`: The Stage7p v2 adapter completed 6/6 runs with 0 warnings.
- `I2`: Because weak-model G0 failed and weak-model G8/G9 passed, explicit obligation retention likely repaired the weak model failure mode.
- `I3`: A2/A3/A5/A7 still require redesign before full Stage7.
- `I4`: We should run a Stage7r smoke after local golden/bad gates pass.
- `I5`: One note says gap compression is universal, while another note says it is conditional.

## Output Requirements

Return `json` and include these required fields/sections: `extracted`, `inferred`, `ambiguous`, `proposed`, `evidence_ids`.
Citation policy: `classification_support`.
