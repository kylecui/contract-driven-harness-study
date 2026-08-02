```json
{
  "create": [
    {
      "action": "create README.md",
      "reason": "File does not exist, safe to create"
    },
    {
      "action": "create research/04_methods/new.md",
      "reason": "File does not exist, safe to create"
    }
  ],
  "skip": [],
  "blocked": [
    {
      "action": "overwrite AGENTS.md",
      "reason": "File exists and is protected; overwrite would be unsafe without explicit confirmation"
    }
  ],
  "ask_first": []
}
```