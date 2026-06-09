```json
{
  "partial_composition": {
    "atoms": ["A10", "A9", "A6"],
    "A10_bounded_context_recall": {
      "must_load": ["Stage 2 is next (from current roadmap)"],
      "must_not_load": ["old plan to run another broad workflow slice"]
    },
    "A9_no_overwrite_action_plan": {
      "existing_files": ["AGENTS.md", "research/CONTEXT.md"],
      "missing_unprotected_file": "research/06_outputs/README.md",
      "protected_file": "AGENTS.md",
      "planned_action": "Create research/06_outputs/README.md"
    },
    "A6_validator_repair": {
      "original_output": {"title": "Contract-Driven Harness"},
      "validator_feedback": "add missing evidence_ids using atom-a6-e01 and keep all existing valid fields unchanged",
      "repaired_output": {
        "title": "Contract-Driven Harness",
        "evidence_ids": ["atom-a6-e01"]
      }
    }
  }
}
```