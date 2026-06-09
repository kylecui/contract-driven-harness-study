# Stage 7r.1 A2R/A7R Local Prep Summary

Date: 2026-06-08

## Scope

Stage 7r.1 tightens the two low-cost-model boundary mechanisms from Stage 7r:

- A2R1: claim-level evidence binding
- A7R1: rejection trace completeness

This stage does not expand to macro-workflow composition. It targets the exact completed-run failures from Stage 7r:

- A2R low-cost G8/G9 used a global evidence list instead of claim-level evidence binding.
- A7R low-cost G8/G9 selected the right option but omitted complete evidence-linked rejection trace coverage, especially for C3.

## Adapter Logging Fix

`research/04_methods/scripts/run_openai_adapter.py` now supports an optional `--event-log` JSONL path and writes incremental per-run events:

- `run_start`
- `provider_request_start`
- `provider_response_end`
- `provider_error`
- `run_end`

It also writes partial adapter reports after each run when a report path is supplied. A dry-run with `--event-log` passed and produced the expected JSONL events.

Artifacts:

- `research/05_analysis/stage7r-logfix-adapter-dry-run.json`
- `research/05_analysis/stage7r-logfix-adapter-events.jsonl`

## Local Gates

Local validation passed:

- Fixture structure validation: 2/2 atoms passed.
- Golden/bad evaluator regression: 4 cases, 0 expectation failures.
- Stage 7r legacy local regression still passes after evaluator extension.

Artifacts:

- `research/04_methods/mechanism-atoms-stage7r1/`
- `research/05_analysis/stage7r1-a2r-a7r-local-check.md`

## Targeted Smoke Prep

Prepared a targeted low-cost-model smoke matrix:

- fixtures: A2R1, A7R1
- model tier: `budget_model`
- arms: G8, G9
- repetitions: 2
- planned runs: 8

Prompt/export/preflight status:

- Packet dry-run: 8/8 packets compiled, 0 failures.
- Real-run artifacts: 8 run directories prepared.
- Prompts and adapter requests exported.
- Preflight: PASS, 0 errors, 0 warnings.

Artifacts:

- `research/04_methods/benchmark-matrix-stage7r1-a2r-a7r-targeted.json`
- `research/05_analysis/benchmark-stage7r1-a2r-a7r-targeted-packets.md`
- `research/05_analysis/real-run-artifacts/stage7r1-a2r-a7r-targeted-manifest-with-prompts.json`
- `research/05_analysis/stage7r1-a2r-a7r-targeted-preflight.md`

## Gate Decision

Stage 7r-logfix, Stage 7r.1 fixture design, and Stage 7r.1 local prep are complete.

The next action is an explicit user-approved API run for the 8-run targeted smoke. Use the new adapter event log during execution so provider timeouts can be diagnosed from per-run events.
