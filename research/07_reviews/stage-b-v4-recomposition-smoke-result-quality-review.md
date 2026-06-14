# Stage B v4 Recomposition Smoke Result Quality Review

Reviewed: 2026-06-14

Overall rating: A for a targeted bounded-composition smoke

Blocking issues: none

## Reviewed Artifacts

- `research/05_analysis/stage-b-v4-recomposition-smoke-experiment-plan.md`
- `research/05_analysis/stage-b-v4-recomposition-smoke-execution.json`
- `research/05_analysis/stage-b-v4-recomposition-smoke-adapter-events.jsonl`
- `research/05_analysis/stage-b-v4-recomposition-smoke-evaluated-runs.json`
- `research/05_analysis/stage-b-v4-recomposition-smoke-evaluation.md`
- four raw output artifacts
- `research/05_analysis/stage-b-v4-recomposition-smoke-result-summary.md`

## Nine-Dimension Review

| Dimension | Rating | Review |
|---|---|---|
| Question alignment | Pass | The result answers whether both exact-retention mechanisms and the fixed gate survive bounded recomposition. |
| Evidence completeness | Pass | Execution, usage, latency, retry, raw output, and component metrics are retained. |
| Citation coverage | Pass | Execution and evaluation claims map to P2-E145 and P2-E146; interpretation maps to P2-E147. |
| Logic chain | Pass | Failed broad macro leads to isolated atoms, atom smoke, local recomposition, then model recomposition. |
| Counter-evidence | Pass | The 18/30 Stage B v3 result remains the negative baseline and limits the claim. |
| Method fit | Pass | Exact equality and component gates match the tested immutable obligations. |
| Actionability | Pass | The next local experiment and its admission gates are specified. |
| Expression quality | Pass | The summary avoids converting four passes into reliability or full-macro claims. |
| Risk disclosure | Pass | Small sample, fixed gate, copy orientation, and absent state mutation are explicit. |

## Independent Numerical Checks

- Execution records contain four results and all have status `executed`.
- Evaluated records contain four results and all have `passed=true`.
- Each fixture contributes exactly two runs.
- Prompt tokens sum to 6,110.
- Completion tokens sum to 1,479.
- Total tokens sum to 7,589.
- Reasoning tokens sum to zero.
- Completion usage ranges from 367 to 372 tokens against a 2,000-token limit.
- Latency ranges from 13.750 to 17.343 seconds; median is 15.813 seconds.
- Every retry lineage remains on attempt one.

## Raw-Output Checks

The four outputs preserve the fixture-specific evidence field, ordered evidence
arrays, state labels, forbidden-inference labels, gate values, support slots,
and immutable-field attestation.

The claim prose varies across runs, but those strings were not preregistered as
immutable. The evaluator does not hide a failure by accepting an alternative
required identifier or array.

## Residual Risks

The sample is a debugging gate, not a confidence-interval study. Passing both
fixtures twice does not estimate a stable success probability.

The composition pressure remains limited. The model copies exact payloads and
emits a fixed gate; it does not update state after an action or reconcile a
changed prerequisite.

The dual-surface fixture is useful evidence against one prior failure pattern,
but two representation variants do not establish general schema robustness.

## Decision

Approve Stage B v4-recomposition-smoke as passed. Approve design and local
validation of one controlled state-mutating macro. Keep a new 30-run provider
slice blocked until that local gate identifies the new transition failure
mode and rejects corresponding known-bads.
