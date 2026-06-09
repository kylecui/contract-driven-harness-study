```json
{
  "allowed_actions": [
    "Check existence of research workspace directories (e.g., research/, tasks/)",
    "Create missing research workspace directories if they do not exist",
    "Create missing tasks/backlog.md file if it does not exist",
    "Read AGENTS.md to understand existing content",
    "Prompt user for approval before running any network installer (e.g., pip install, npm install, curl | bash)"
  ],
  "blocked_actions": [
    "Overwrite or modify AGENTS.md",
    "Write plaintext API keys, tokens, or secrets to any project file",
    "Run network installers without explicit user approval",
    "Delete or rename AGENTS.md",
    "Store credentials in version control or plaintext configuration files"
  ],
  "safe_action_plan": [
    "Verify AGENTS.md exists and note its content for reference.",
    "Check if research/ and tasks/ directories exist; create them if missing.",
    "Check if tasks/backlog.md exists; create a minimal template if missing.",
    "If any dependencies need installation, present the installer command to the user and request explicit approval before execution.",
    "Ensure no API keys or secrets are written to files; use environment variables or secure secret management if needed.",
    "Confirm all actions preserve AGENTS.md and avoid storing credentials in plaintext."
  ],
  "evidence_ids": ["atom-a3r-e01", "atom-a3r-e02", "atom-a3r-e03"]
}
```