# Stage 7r.1 A2R/A7R Targeted Smoke Summary

Date: 2026-06-08

## Scope

Stage 7r.1 targeted the two completed-run low-cost-model failures from Stage 7r:

- A2R: low-cost G8/G9 used a global evidence list but did not bind evidence at claim level.
- A7R: low-cost G8/G9 selected the right option but omitted complete evidence-linked rejection trace coverage.

The repair was mechanism-level contract tightening, not a macro-workflow change:

- A2R1 requires every `grounded_claims` item to be an object with non-empty `evidence_ids`.
- A7R1 requires `rejected_options[]` objects with evidence IDs and a decision trace step for C2 support, C1 rejection, and C3 rejection.

## Local Gates

Local prep passed before API execution:

- Structure validation: 2/2 atoms passed.
- Golden/bad regression: 4/4 expectations met.
- Packet dry-run: 8/8 packets compiled.
- Preflight: PASS, 0 errors, 0 warnings.

## Adapter Logging

The OpenAI-compatible adapter now supports `--event-log` and writes incremental per-run events. This was used during Stage 7r.1 smoke.

The first 8-run execution completed 7/8 runs and left `a7r1-rejection-trace-completeness__budget_model__G9__r2` pending after `provider_request_start`. The single-run retry used the longer-timeout, lower-output-limit config and completed successfully:

- Retry config: `timeout_seconds=900`, `max_output_tokens=600`
- Retry elapsed time: 103015 ms
- Retry status: executed

Artifacts:

- `research/05_analysis/stage7r1-a2r-a7r-targeted-adapter-events.jsonl`
- `research/05_analysis/stage7r1-a2r-a7r-targeted-pending-a7r1-g9-r2-events.jsonl`
- `research/05_analysis/stage7r1-a2r-a7r-targeted-adapter.json`
- `research/05_analysis/stage7r1-a2r-a7r-targeted-pending-a7r1-g9-r2-adapter.json`

## Real Smoke Results

Matrix:

- model tier: `budget_model`
- provider/model: SiliconFlow `Qwen/Qwen3-8B`
- fixtures: A2R1, A7R1
- arms: G8, G9
- repetitions: 2
- planned runs: 8

Final evaluation:

| Fixture | Arm | Repetitions | Completed | Passed | Avg task success | Avg atom primary |
|---|---|---:|---:|---:|---:|---:|
| A2R1 claim-level evidence binding | G8 | 2 | 2 | 2 | 1.000 | 1.000 |
| A2R1 claim-level evidence binding | G9 | 2 | 2 | 2 | 1.000 | 1.000 |
| A7R1 rejection trace completeness | G8 | 2 | 2 | 2 | 1.000 | 1.000 |
| A7R1 rejection trace completeness | G9 | 2 | 2 | 2 | 1.000 | 1.000 |

Overall:

- Completed: 8/8
- Passed: 8/8
- Avg task success: 1.000
- Avg atom primary metric: 1.000

## Interpretation

Stage 7r.1 strongly supports the mechanism-first repair hypothesis for these two atoms.

The low-cost model did not need a larger open-ended workflow prompt. It needed a narrower and more explicit output contract:

- A2R1 converted "include evidence" into "bind each grounded claim to evidence IDs."
- A7R1 converted "explain decision" into "cover every selected/rejected option with evidence-linked trace steps."

This repairs the Stage 7r low-cost-model failures for A2R/A7R under targeted mechanism tests.

## Boundary

This is still not evidence that broad project initialization or research workflow macro tasks will pass. It is evidence that two previously blocking mechanism atoms can be repaired through contract tightening and pass under low-cost-model G8/G9.

Next gate:

- Update the Stage 7 composition-readiness view using A2R1 and A7R1.
- Decide whether A4/A8 need additional repetitions or whether existing Stage 7r/7r.1 evidence is sufficient for a narrow composed macro.
- Avoid full open-ended macro composition until the candidate macro is explicitly built from passing mechanisms and preserves cross-step obligations.
