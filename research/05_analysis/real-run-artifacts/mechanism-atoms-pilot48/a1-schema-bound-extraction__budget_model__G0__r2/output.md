

{
  "task_id": "mechanism_a1_schema_bound_extraction_001",
  "intent": {
    "goal": "Return a valid JSON object with required planning fields and supported evidence IDs.",
    "language": "en",
    "freshness": "local_snapshot"
  },
  "constraints": [
    "Primary mechanism under test: OutputContract.",
    "Dominant failure mode: Missing required structure.",
    "Return only information supported by the fixture."
  ],
  "planning": {
    "proposal": "NEXT",
    "target_venue": "ACL Findings",
    "primary_metric": "weak-model enablement lift"
  },
  "evidence_ids": ["atom-a1-e01", "atom-a1-e02"]
}