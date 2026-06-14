# Stage B v4 Smoke Result Quality Review

Reviewed: 2026-06-14

Overall rating: A for a targeted mechanism smoke

Blocking issues: none

## Reviewed Artifacts

- `research/05_analysis/stage-b-v4-smoke-experiment-plan.md`
- `research/05_analysis/stage-b-v4-smoke-execution.json`
- `research/05_analysis/stage-b-v4-smoke-adapter-events.jsonl`
- `research/05_analysis/stage-b-v4-smoke-evaluated-runs.json`
- `research/05_analysis/stage-b-v4-smoke-evaluation.md`
- eight raw output and trace artifacts
- `research/05_analysis/stage-b-v4-smoke-result-summary.md`

## Nine-Dimension Review

| Dimension | Rating | Review |
|---|---|---|
| Question alignment | Pass | The result directly answers whether each isolated mechanism passes twice. |
| Evidence completeness | Pass | Run, token, latency, retry, and metric claims are retained in machine-readable artifacts. |
| Citation coverage | Pass | Empirical claims map to P2-E139 and P2-E140; interpretation maps to P2-E141. |
| Logic chain | Pass | v3 failure leads to atom isolation, local gate, smoke, then bounded recomposition. |
| Counter-evidence | Pass | The summary preserves the negative v3 macro result and does not treat the smoke as macro repair. |
| Method fit | Pass | Exact equality matches the tested immutability obligation. |
| Actionability | Pass | The next experiment and its local gates are specified. |
| Expression quality | Pass | No unsupported robustness, production, or universal capability language appears. |
| Risk disclosure | Pass | Small sample, copying, provider variance, and transfer limits are explicit. |

## Independent Numerical Checks

- Execution records contain 8 results and all have status `executed`.
- Evaluated records contain 8 results and all have `passed=true`.
- Each fixture contributes exactly two runs.
- Prompt tokens sum to 8,348.
- Completion tokens sum to 1,110.
- Total tokens sum to 9,458.
- Reasoning tokens sum to zero.
- No completion exceeds 191 tokens against a 2,000-token limit.
- Latency ranges from 3.407 to 8.454 seconds; median is 5.765 seconds.
- No retry lineage has attempt greater than one.

## Residual Risks

Both repetitions within each fixture produced the same output, which is
consistent with temperature zero but does not establish stability under
provider or prompt variation.

The tasks are deliberately copy-oriented. This is construct-valid for exact
retention, but it means the result should not be generalized to reasoning,
selection, or synthesis quality.

The central unresolved risk is composition transfer. Stage B v3 failed under a
larger obligation set, so the next test must increase composition pressure
without returning immediately to the entire original macro.

## Decision

Approve Stage B v4-smoke as passed. Approve Stage B v4-recomposition-local.
Keep any new 30-run confirmation blocked until bounded recomposition passes
both local and targeted real-model gates.
