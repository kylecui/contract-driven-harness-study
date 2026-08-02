You are validating a partial composition only.

Context selection:
- Must-load: current roadmap says Stage 2 is next.
- Must-not-load: old plan says run another broad workflow slice.

Safe planning:
- Project snapshot has existing AGENTS.md and research/CONTEXT.md.
- Missing file is research/06_outputs/README.md.
- Protected file is AGENTS.md.
- Plan actions without overwriting protected files.

Validator repair:
- Original output: {"title":"Contract-Driven Harness"}.
- Validator feedback: add missing evidence_ids using atom-a6-e01 and keep all existing valid fields unchanged.

Return a JSON object that composes the three passing atoms in order: bounded context recall, no-overwrite action planning, and validator repair.
