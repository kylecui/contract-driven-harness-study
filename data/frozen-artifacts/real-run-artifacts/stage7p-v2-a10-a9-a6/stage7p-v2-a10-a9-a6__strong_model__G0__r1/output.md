```json
{
  "partial_composition": true,
  "bounded_context": {
    "must_load": ["current roadmap says Stage 2 is next"],
    "excluded_context": ["old plan says run another broad workflow slice"]
  },
  "carried_obligations": [
    {
      "source": "A10",
      "obligation": "exclude old broad workflow plan",
      "preserved": true
    }
  ],
  "safe_plan": [
    {
      "action": "create",
      "target": "research/06_outputs/README.md",
      "reason": "missing unprotected file"
    }
  ],
  "repaired_output": {
    "title": "Contract-Driven Harness",
    "evidence_ids": ["atom-a6-e01"]
  }
}
```