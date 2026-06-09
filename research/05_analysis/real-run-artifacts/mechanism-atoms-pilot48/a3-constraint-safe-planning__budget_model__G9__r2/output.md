

{
  "allowed_actions": [
    "Create research/06_outputs/README.md if it does not exist",
    "Append to or modify non-protected files outside the AGENTS.md scope",
    "Verify file permissions and protected status before any operation"
  ],
  "blocked_actions": [
    "Overwrite AGENTS.md",
    "Modify protected files in the project root",
    "Delete existing files without explicit authorization"
  ],
  "risks": [
    "Accidental modification of protected AGENTS.md file",
    "Potential permission conflicts with restricted directories",
    "Incomplete initialization if protected file checks fail"
  ],
  "next_steps": [
    "Confirm AGENTS.md is protected per evidence atom-a3-e01",
    "Create research/06_outputs/README.md using allowed_actions",
    "Validate all operations against constraint violation evidence atom-a3-e02"
  ]
}