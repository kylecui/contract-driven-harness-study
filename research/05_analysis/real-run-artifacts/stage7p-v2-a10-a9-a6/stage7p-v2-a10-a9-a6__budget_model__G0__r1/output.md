

{
  "composition_type": "partial_composition",
  "bounded_context": {
    "included_context": {
      "current_roadmap": "Stage 2 is next"
    },
    "excluded_context": {
      "old_broad_workflow_plan": "broad-workflow plan"
    }
  },
  "action_plan": {
    "planned_actions": [
      {
        "file": "research/06_outputs/README.md",
        "action": "create",
        "reason": "Missing file identified in project snapshot"
      }
    ],
    "protected_files": [
      "AGENTS.md",
      "research/CONTEXT.md"
    ]
  },
  "validator_repair": {
    "original_output": {
      "title": "Contract-Driven Harness"
    },
    "repaired_output": {
      "title": "Contract-Driven Harness",
      "evidence_ids": ["atom-a6-e01"]
    }
  },
  "carried_obligations": [
    {
      "obligation": "exclude old broad workflow plan",
      "status": "preserved",
      "reason": "A10 obligation requires exclusion of stale context"
    }
  ],
  "new_mechanism": "cross_step_obligation_retention",
  "label": "partial_composition"
}