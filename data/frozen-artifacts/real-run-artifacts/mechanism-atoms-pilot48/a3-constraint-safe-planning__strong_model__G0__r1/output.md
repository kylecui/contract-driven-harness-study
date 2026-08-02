**Plan for Project Initialization (Without Overwriting Protected Files)**

**Protected File Status (from snapshot):**
- `AGENTS.md` → exists (protected, must not be overwritten)
- `research/06_outputs/README.md` → missing (can be created)

**Actions to Perform:**
1. **Check existence** of `AGENTS.md` before any write operation.
2. **Skip writing** `AGENTS.md` entirely (since it already exists and is protected).
3. **Create** `research/06_outputs/README.md` (since it is missing and safe to create).
4. **Verify** no other protected files in the snapshot would be overwritten by the plan.

**Result:**  
Only `research/06_outputs/README.md` will be created; `AGENTS.md` remains untouched.