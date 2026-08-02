# Protocol: Contract-Driven Harness Benchmark

## Objective

Measure whether stronger harness layers reduce cross-model performance gaps in productivity tasks.

## Core Metric

```text
Gap_baseline = PerformanceGap(models, prompt_only)
Gap_harness = PerformanceGap(models, harness_condition)
CompressionRatio = 1 - Gap_harness / Gap_baseline
```

Report compression separately for:

- Task success.
- Schema validity.
- Tool-call correctness.
- Citation/evidence grounding.
- Human acceptance.
- Cost efficiency.
- Safety/policy consistency.

## Task Classes

| Class | Constraint Level | Example Tasks | Expected Harness Effect |
|---|---:|---|---|
| Structured extraction | High | Extract fields from fixed documents | Very strong |
| Project initialization | High | Create repo scaffold from profile | Very strong |
| Skill validation | High | Lint/check a skill package | Strong |
| Research workflow | Medium | Build brief, sources, evidence, synthesis | Medium-strong |
| Code repair | Medium | Fix test failure with tool use | Medium |
| Architecture review | Medium-low | Review design with tradeoffs | Medium-low |
| Strategic judgment | Low | Open-ended planning | Weak |

## Model Matrix

Use abstract tiers first, then bind to available providers:

- `strong_model`
- `mid_model`
- `budget_model`
- `fast_model`
- `long_context_model`

Each model must run the same task snapshots and tool mocks.

## Harness Arms

| Arm | Layers |
|---|---|
| G0 | Prompt only |
| G1 | Prompt + role + instruction |
| G2 | G1 + output schema |
| G3 | G2 + evidence bundle / RAG |
| G4 | G3 + tool contracts |
| G5 | G4 + skill procedure |
| G6 | G5 + workflow |
| G7 | G6 + memory policy |
| G8 | G7 + validator / eval |
| G9 | Full harness + trace + regression |

## Required Artifacts Per Run

Each run should emit:

- `task_spec.json`
- `memory_slice.json`
- `evidence_bundle.json`
- `output_contract.json`
- `model_output.md` or `model_output.json`
- `tool_trace.jsonl`
- `validation_report.json`
- `metrics.json`

## Evaluation Rules

- Use fixed task snapshots.
- Run at least 5 repetitions per model/arm/task.
- Keep tool outputs deterministic wherever possible.
- Store raw outputs before validation repair.
- Report confidence intervals, not only means.
- Separate invalid-format failure from wrong-answer failure.

## Minimum Viable Benchmark

Start with:

- 3 models.
- 3 task classes: high, medium, low constraint.
- 4 arms: G0, G2, G6, G9.
- 5 repetitions.

This is `3 * 3 * 4 * 5 = 180` runs, small enough to execute but enough to reveal trend direction.

## First Real Adapter Slice

Before running the full matrix, use the smaller slice defined in `model-adapter-interface.md`:

- 2 fixtures: `structured-extraction`, `project-initialization`.
- 2 model tiers: one strong model, one budget model.
- 2 harness arms: `G0`, `G9`.
- 3 repetitions.

This produces 24 real runs and is enough to test provider integration, artifact capture, validation reporting, and metric aggregation.

## Expected Findings

Hypothesis:

- High-constraint tasks should show the largest gap compression.
- Medium-constraint tasks should show partial compression.
- Low-constraint tasks should show limited compression and preserve strong-model advantage.
- Full harness may increase fixed overhead but reduce variance and review burden.

## Risk Controls

- Do not average across all task types into one grand conclusion.
- Do not call output similarity capability compression unless task success also improves or holds.
- Track cost because G9 may improve reliability while becoming too expensive for simple tasks.
- Track contract drift because stale schemas or registries can make the harness look worse than prompt-only.
