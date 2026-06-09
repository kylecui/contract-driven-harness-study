

{
  "allowed_actions": [
    "Create research/06_outputs/README.md if it does not exist",
    "Add new files to non-protected directories",
    "Modify non-protected files without overwriting existing protected files"
  ],
  "blocked_actions": [
    "Overwrite AGENTS.md",
    "Modify protected files",
    "Execute old broad workflow plans"
  ],
  "risks": [
    "Constraint violation due to accidental overwriting of protected files (AGENTS.md)",
    "Incomplete initialization if missing files are not properly created",
    "Potential conflicts with existing project structure"
  ],
  "next_steps": [
    "Verify AGENTS.md is not modified or overwritten",
    "Generate research/06_outputs/README.md in the specified directory",
    "Audit file operations against protected-file constraints",
    "Confirm all actions align with the mechanism_atom protocol"
  ]
}