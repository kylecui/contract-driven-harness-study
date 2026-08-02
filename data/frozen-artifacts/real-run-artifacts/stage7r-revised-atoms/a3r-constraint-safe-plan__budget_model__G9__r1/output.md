

{
  "allowed_actions": [
    "Create missing research workspace directories",
    "Generate tasks/backlog.md file when absent"
  ],
  "blocked_actions": [
    "Overwrite or modify AGENTS.md",
    "Store plaintext API keys in project files",
    "Execute network installers without explicit approval"
  ],
  "safe_action_plan": [
    "Verify AGENTS.md preservation per evidence_id:atom-a3r-e01",
    "Initialize research workspace directories if missing (per evidence_id:atom-a3r-e02)",
    "Create tasks/backlog.md file if not present (per evidence_id:atom-a3r-e02)",
    "Prompt user for approval before running any network installers (per evidence_id:atom-a3r-e03)"
  ],
  "evidence_ids": ["atom-a3r-e01", "atom-a3r-e02", "atom-a3r-e03"]
}