# Benchmark Run: project-initialization__strong_model__G9__r1

You are completing a benchmark task. Follow the instructions for the assigned harness arm.

- Fixture: `project-initialization`
- Model tier: `strong_model`
- Harness arm: `G9`
- Task type: `project_initialization`

## Harness Arm G9

Use the full harness packet. Obey the task spec, preserve evidence IDs for important claims, respect memory boundaries, and satisfy the output contract.

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

## EvidenceBundle

```json
{
  "evidence_bundle_id": "ev_project_initialization_001",
  "task_id": "project_initialization_001",
  "items": [
    {
      "source_id": "fixture-file-inventory",
      "evidence_id": "fixture-pi-e01",
      "evidence_type": "EXTRACTED",
      "claim": "Existing files include AGENTS.md.",
      "freshness": "snapshot",
      "authority": "local_fixture"
    },
    {
      "source_id": "fixture-file-inventory",
      "evidence_id": "fixture-pi-e02",
      "evidence_type": "EXTRACTED",
      "claim": "The project profile is academic research.",
      "freshness": "snapshot",
      "authority": "local_fixture"
    }
  ]
}
```

## MemorySlice

```json
{
  "memory_slice_id": "mem_project_initialization_001",
  "task_id": "project_initialization_001",
  "active_topic_id": "topic_project_initialization",
  "mode": "task",
  "must_load": [
    "existing_file_inventory",
    "no_overwrite_policy"
  ],
  "may_load": [
    "installed_pack_registry"
  ],
  "must_not_load": [
    "unrelated_git_history"
  ],
  "token_budget": 6000
}
```

## OutputContract

```json
{
  "output_contract_id": "out_project_initialization_001",
  "format": "checklist",
  "required_sections": [
    "created_files",
    "skipped_files",
    "risks",
    "next_steps"
  ],
  "citation_policy": "important_claims",
  "style_profile": "concise_engineering",
  "tool_trace_required": true
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

Return `checklist` and include these required fields/sections: `created_files`, `skipped_files`, `risks`, `next_steps`.
Citation policy: `important_claims`.
If tools are used, preserve a trace of what was used and why.
