

{
  "allowed_actions": [
    "Create research/06_outputs/README.md if it does not exist",
    "Generate new files in non-protected directories",
    "Initialize project structure without modifying AGENTS.md"
  ],
  "blocked_actions": [
    "Overwrite AGENTS.md",
    "Modify existing protected files",
    "Delete or alter files in restricted paths"
  ],
  "risks": [
    "Risk of accidental overwrites if file paths are misconfigured",
    "Potential for incomplete initialization if directory permissions are restricted",
    "Constraint violation risks during file creation if safeguards are bypassed"
  ],
  "next_steps": [
    "Verify AGENTS.md is not a protected file before any operations",
    "Create research/06_outputs/README.md in the specified location",
    "Validate file creation permissions for the target directory",
    "Document all actions taken in the output contract"
  ]
}