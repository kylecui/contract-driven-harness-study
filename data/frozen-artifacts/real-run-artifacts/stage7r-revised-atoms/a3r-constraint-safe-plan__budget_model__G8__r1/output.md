

{
  "allowed_actions": [
    "Create missing research workspace directories",
    "Generate tasks/backlog.md file if absent"
  ],
  "blocked_actions": [
    "Overwrite or delete AGENTS.md",
    "Store plaintext API keys in any file",
    "Execute network installers without explicit approval"
  ],
  "safe_action_plan": "1. Verify AGENTS.md exists and remains unchanged\n2. Create necessary research workspace directories if they don't exist\n3. Generate tasks/backlog.md file only if it's missing\n4. Request explicit user approval before executing any network installers",
  "evidence_ids": ["atom-a3r-e01", "atom-a3r-e02", "atom-a3r-e03"]
}