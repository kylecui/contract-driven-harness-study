# Model Adapter Interface

## Purpose

This document defines the replacement boundary between the current mock benchmark runner and future real model-backed runs.

The benchmark should keep these stable:

- Benchmark fixtures.
- Benchmark matrix.
- Compiled packet shape.
- Output metric schema.
- Gap-compression metric computation.

Only the runner that turns packets into model outputs should change.

## Input

Each model adapter receives one compiled packet with:

- `run_id`
- `fixture`
- `model`
- `harness_arm`
- `repetition`
- `layers`
- `task_spec`
- `input`
- optional `output_contract`
- optional `evidence_bundle`
- optional `memory_slice`
- `trace_required`
- `validator_required`

For `G0`, the adapter should only use the raw input and minimal prompt.

For `G2`, the adapter should also enforce or request the output contract.

For `G6`, the adapter should include evidence bundle, skills/workflow instructions, and trace capture.

For `G9`, the adapter should include memory policy, validation, trace, and regression checks.

## Output

Each run should emit:

```json
{
  "run_id": "fixture__model__arm__r1",
  "fixture": "structured-extraction",
  "task_class": "structured_extraction",
  "model": "strong_model",
  "harness_arm": "G9",
  "repetition": 1,
  "raw_output_path": "research/05_analysis/runs/.../output.md",
  "tool_trace_path": "research/05_analysis/runs/.../tool_trace.jsonl",
  "validation_report_path": "research/05_analysis/runs/.../validation_report.json",
  "metrics": {
    "task_success": 0.0,
    "schema_validity": 0.0,
    "tool_call_correctness": 0.0,
    "citation_grounding": 0.0,
    "human_acceptance": 0.0,
    "cost_efficiency": 0.0,
    "safety_consistency": 0.0
  },
  "mock": false
}
```

## Metric Semantics

Scores are normalized to `0.0` through `1.0`.

- `task_success`: Did the run satisfy the task goal?
- `schema_validity`: Did output match the requested structure?
- `tool_call_correctness`: Were tool calls allowed, necessary, and successful?
- `citation_grounding`: Were important claims grounded in evidence IDs?
- `human_acceptance`: Would a reviewer accept the output without major revision?
- `cost_efficiency`: Did the run achieve reasonable quality for its token/time cost?
- `safety_consistency`: Did the run consistently obey risk and policy constraints?

## Adapter Contract

Real adapters must:

- Preserve raw model output before repair.
- Preserve validation output separately.
- Never overwrite prior run artifacts.
- Record model name, provider, timestamp, temperature, and tool availability.
- Return metrics even when the run fails, with failed dimensions set to `0.0`.
- Mark output as `mock: false`.

## Recommended First Real Slice

Start with a small slice before the full 240-run matrix:

- Fixtures: `structured-extraction`, `project-initialization`
- Models: one strong model, one budget model
- Arms: `G0`, `G9`
- Repetitions: 3

This produces `2 * 2 * 2 * 3 = 24` real runs.

