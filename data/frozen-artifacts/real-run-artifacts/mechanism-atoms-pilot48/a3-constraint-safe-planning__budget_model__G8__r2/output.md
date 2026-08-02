

{
  "allowed_actions": [
    "Create research/06_outputs/README.md in the project snapshot",
    "Add new files to non-protected directories",
    "Modify non-protected files without overwriting protected ones"
  ],
  "blocked_actions": [
    "Overwrite AGENTS.md",
    "Modify protected files",
    "Use deprecated workflow plans"
  ],
  "risks": [
    "Accidental overwriting of protected files (AGENTS.md) during initialization",
    "Incomplete project setup if constraints are not strictly enforced"
  ],
  "next_steps": [
    "Generate research/06_outputs/README.md using the project snapshot",
    "Verify file permissions and protected status of all existing files",
    "Validate the plan against the constraint-safe policy before execution"
  ],
  "citation": {
    "important_claims": [
      "atom-a3-e01: Primary evidence for Constraint-Safe Planning",
      "atom-a3-e02: Supporting evidence for Constraint violation"
    ]
  }
}