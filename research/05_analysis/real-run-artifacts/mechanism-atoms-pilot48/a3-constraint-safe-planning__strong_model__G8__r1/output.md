```json
{
  "allowed_actions": [
    "Create research/06_outputs/README.md with appropriate content",
    "Read AGENTS.md to understand existing constraints",
    "Update other project documentation not listed as protected",
    "Create new directories and files in research/06_outputs/ (excluding protected files)",
    "Run project initialization scripts that don't modify protected files"
  ],
  "blocked_actions": [
    "Overwrite or modify AGENTS.md",
    "Delete AGENTS.md",
    "Rename AGENTS.md",
    "Create a new file with the same name as AGENTS.md in any location",
    "Any action that would alter the content, permissions, or existence of AGENTS.md"
  ],
  "risks": [
    "Accidental overwrite of AGENTS.md through automated scripts",
    "Unintended modification of AGENTS.md during bulk file operations",
    "Creating conflicting documentation that contradicts AGENTS.md constraints",
    "Missing research/06_outputs/README.md may cause incomplete project documentation"
  ],
  "next_steps": [
    "Verify AGENTS.md content to understand specific constraints before proceeding",
    "Create research/06_outputs/README.md with project-specific documentation",
    "Document the constraint protection mechanism for AGENTS.md in project notes",
    "Consider adding a backup of AGENTS.md (read-only copy) for reference",
    "Review other potentially protected files that may have similar constraints"
  ]
}
```