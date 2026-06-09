# Benchmark Run: project-initialization__budget_model__G0__r1

You are completing a benchmark task. Follow the instructions for the assigned harness arm.

- Fixture: `project-initialization`
- Model tier: `budget_model`
- Harness arm: `G0`
- Task type: `project_initialization`

## Harness Arm G0

Use only the task input below. Do not assume extra schemas, memory, tools, or evidence beyond what is present in the task text.

## TaskSpec

```json
{
  "task_spec_version": "0.1.0",
  "task_id": "project_initialization_001",
  "task_type": "project_initialization",
  "intent": {
    "goal": "Create a no-overwrite academic research project scaffold.",
    "language": "en",
    "freshness": "local_snapshot"
  },
  "constraints": [
    "Do not overwrite existing AGENTS.md.",
    "Create missing files only.",
    "Use research workflow directories."
  ],
  "required_skills": [
    "project-initializer",
    "research-router"
  ],
  "allowed_tools": [
    "filesystem"
  ],
  "risk_profile": "medium",
  "memory_slice_id": "mem_project_initialization_001",
  "evidence_bundle_id": "ev_project_initialization_001",
  "output_contract_id": "out_project_initialization_001"
}
```

## Task Input

# Fixture Input

Initialize this existing workspace as an academic research project.

Existing important files:

- AGENTS.md
- .agents/installed-packs.json
- .git/

Use no-overwrite behavior.

## Output Requirements

Return the best answer for the task in a concise, reviewable form.
