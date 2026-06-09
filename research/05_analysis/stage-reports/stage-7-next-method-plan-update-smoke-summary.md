# Stage 7-next Method-Plan Update Smoke Summary

## Scope

Stage 7-next tested the bounded evidence-bound method-plan update macro against the low-cost model only.

This smoke does not test full project initialization, full research workflow execution, tool use, or production readiness.

## Run Configuration

- Fixture: `stage7-next-method-plan-update`
- Manifest: `research/05_analysis/real-run-artifacts/stage7-next-method-plan-update-manifest-with-prompts.json`
- Provider config: `research/04_methods/provider-config.siliconflow-stage7e-v4-retry.json`
- Provider: SiliconFlow
- Model tier: `budget_model`
- Model: `Qwen/Qwen3-8B`
- Harness arms: `G8`, `G9`
- Repetitions: 2 each
- Total runs: 4
- Temperature: 0
- Max output tokens: 2000
- Timeout: 900 seconds
- Event log: `research/05_analysis/stage7-next-method-plan-update-adapter-events.jsonl`

## Execution Result

All 4 runs executed successfully.

| Arm | Repetitions | Executed | Provider errors |
|---|---:|---:|---:|
| G8 | 2 | 2 | 0 |
| G9 | 2 | 2 | 0 |

Elapsed times:

- G8 r1: 95.063 seconds
- G8 r2: 104.687 seconds
- G9 r1: 120.688 seconds
- G9 r2: 212.469 seconds

No timeout or truncated-output retry was needed.

## Evaluation Result

Evaluation artifacts:

- Markdown: `research/05_analysis/stage7-next-method-plan-update-evaluation.md`
- JSON: `research/05_analysis/stage7-next-method-plan-update-evaluation-runs.json`

| Run | Task success | Primary metric | Passed |
|---|---:|---:|---:|
| `stage7-next-method-plan-update__budget_model__G8__r1` | 1.000 | 1.000 | true |
| `stage7-next-method-plan-update__budget_model__G8__r2` | 1.000 | 1.000 | true |
| `stage7-next-method-plan-update__budget_model__G9__r1` | 1.000 | 1.000 | true |
| `stage7-next-method-plan-update__budget_model__G9__r2` | 1.000 | 1.000 | true |

All runs also scored 1.000 on:

- schema validity,
- citation grounding,
- evidence type accuracy,
- state accuracy,
- trace completeness,
- stage completion,
- context relevance.

## Interpretation

Stage 7-next supports a narrow real-model claim:

> The low-cost model can complete a fixed evidence-bound method-plan update macro under G8/G9 when Stage 7e v4 obligations are reused and the new method-plan obligation is explicit.

This strengthens the mechanism-first repair-loop story because the passing behavior transferred from a decision macro to a closely related method-plan update macro with one new stressor.

## Boundary

This result does not support:

- universal model-gap closure,
- production readiness,
- full project initialization readiness,
- full research workflow readiness,
- open-ended tool-using workflow execution.

## Decision

Stage 7-next-smoke passes.

The next recommended work is Stage 8 methods drafting:

1. Write the methods section around the mechanism-first repair loop.
2. Treat Stage 7e v1-v4 and Stage 7-next as the central bounded-composition evidence.
3. Keep broader workflow expansion blocked unless a new macro is defined with local gates and a targeted smoke.
