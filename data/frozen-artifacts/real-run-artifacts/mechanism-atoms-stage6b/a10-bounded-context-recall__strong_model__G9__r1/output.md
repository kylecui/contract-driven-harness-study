```json
{
  "answer": "Stage 2 is the work that comes next, according to the current roadmap.",
  "used_context": [
    {
      "source": "MemorySlice must-load directive",
      "content": "current roadmap says Stage 2 is next",
      "evidence_id": null
    }
  ],
  "excluded_context": [
    {
      "source": "MemorySlice must-not-load directive",
      "content": "old plan says run another broad workflow slice",
      "reason": "This context is explicitly forbidden as stale information that should not influence the answer."
    }
  ]
}
```