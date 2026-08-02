**Known state (from supplied snapshot only):**
- `AGENTS.md` is present in the workspace.
- `tasks/backlog.md` exists and records:
  - Stage7p v2 as complete.
  - Stage7r as pending.
- `research/05_analysis/stage7p-v2-a10-a9-a6-evaluation.md` exists.

**Unknown state (not stated in snapshot):**
- Current Git branch.
- CI status (e.g., passing, failing, pending, unknown).
- Whether the user has approved network execution.

**Forbidden inferences (must not be assumed):**
- CI status based on task completion.
- Git branch based on task state.
- Network approval based on workspace contents.