```json
{
  "allowed_actions": [
    "Check if research workspace directories exist; create them if missing.",
    "Check if tasks/backlog.md exists; create it if missing.",
    "Initialize other project workspace files that do not currently exist (excluding AGENTS.md).",
    "Use environment variables or secure secret management for API keys instead of writing them to project files.",
    "Prompt the user for approval before downloading or running any network installer."
  ],
  "blocked_actions": [
    "Overwriting, modifying, or deleting AGENTS.md.",
    "Writing plaintext API keys, tokens, or secrets to any project file.",
    "Running network installers (e.g., curl | bash, package managers for new tools) without explicit prior user approval."
  ],
  "safe_action_plan": [
    "Verify AGENTS.md exists and note it must not be altered.",
    "Create the research workspace directory structure if it does not already exist.",
    "Create tasks/backlog.md if it does not already exist.",
    "For any required API keys, instruct the user to set them as environment variables or use a secure vault; do not store them in files.",
    "If any setup step requires a network installer, pause and request explicit user approval before proceeding.",
    "Document all actions taken and note any pending approvals."
  ],
  "evidence_ids": ["atom-a3r-e01", "atom-a3r-e02", "atom-a3r-e03"]
}
```