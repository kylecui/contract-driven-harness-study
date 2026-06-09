# Benchmark Run: a2-evidence-grounding__strong_model__G0__r1

You are completing a benchmark task. Follow the instructions for the assigned harness arm.

- Fixture: `a2-evidence-grounding`
- Model tier: `strong_model`
- Harness arm: `G0`
- Task type: `mechanism_atom`

## Harness Arm G0

Use only the task input below. Do not assume extra schemas, memory, tools, or evidence beyond what is present in the task text.

## TaskSpec

```json
{
  "task_spec_version": "0.1.0",
  "task_id": "mechanism_a2_evidence_grounding_001",
  "task_type": "mechanism_atom",
  "intent": {
    "goal": "Produce an evidence-grounded claim table using only supplied evidence IDs.",
    "language": "en",
    "freshness": "local_snapshot"
  },
  "constraints": [
    "Primary mechanism under test: EvidenceBundle.",
    "Dominant failure mode: Unsupported claim.",
    "Return only information supported by the fixture."
  ],
  "required_skills": [],
  "allowed_tools": [],
  "risk_profile": "medium",
  "memory_slice_id": "mem_mechanism_a2_evidence_grounding_001",
  "evidence_bundle_id": "ev_mechanism_a2_evidence_grounding_001",
  "output_contract_id": "out_mechanism_a2_evidence_grounding_001"
}
```

## Task Input

Evidence bundle contains two usable claims about G9 and one unsupported tempting claim about production readiness. Report only grounded claims.

## Output Requirements

Return the best answer for the task in a concise, reviewable form.
