# Stage 7r Revised Mechanism Atoms Summary

Date: 2026-06-08

## Scope

Stage 7r redesigned the previously boundary-prone mechanism atoms before broader Stage 7 composition:

- A2R: unsupported claim detection
- A3R: constraint-safe plan
- A4R: strict state inventory
- A5R: deterministic stage-gate check
- A7R: enumerated claim decision
- A8R: evidence-type rules

The goal was not to prove full project initialization or research workflow composition. The goal was to test whether narrower mechanism atoms with fixed input, explicit output contracts, known-bad fixtures, and semantic evaluators are locally valid and model-testable.

## Local Gates

Local validation passed:

- Fixture structure validation: 6/6 atoms passed.
- Golden/bad evaluator regression: 12 cases, 0 expectation failures.
- Packet dry-run: 36/36 packets compiled.
- Preflight: PASS, 0 errors, 0 warnings.

Key local artifacts:

- `research/04_methods/mechanism-atoms-stage7r/`
- `research/05_analysis/stage7r-revised-atoms-local-check.md`
- `research/05_analysis/benchmark-stage7r-revised-atoms-packets.md`
- `research/05_analysis/stage7r-revised-atoms-preflight.md`

## Real Smoke Execution

Planned real-model smoke:

- 6 revised atoms
- 2 model tiers: `strong_model`, `budget_model`
- 3 arms: G0, G8, G9
- 1 repetition
- Total planned: 36 runs

Execution status:

- Completed real outputs: 35/36
- Pending: 1/36
- Pending run: `a8r-evidence-type-rules__budget_model__G8__r1`
- Pending reason: repeated SiliconFlow read timeout on `Qwen/Qwen3-8B`, including a single-run retry and a final controlled retry with `timeout_seconds=900` and `max_output_tokens=600`.

This pending run is treated as an execution deviation, not as a model-quality failure. Further retries were stopped to avoid turning provider instability into an uncontrolled experimental variable.

## Results On Completed Runs

By model and harness arm:

| Model tier | Arm | Planned | Complete | Passed | Pass rate on completed | Avg task success | Avg atom primary |
|---|---|---:|---:|---:|---:|---:|---:|
| `strong_model` | G0 | 6 | 6 | 0 | 0.000 | 0.000 | 0.000 |
| `strong_model` | G8 | 6 | 6 | 6 | 1.000 | 1.000 | 1.000 |
| `strong_model` | G9 | 6 | 6 | 6 | 1.000 | 1.000 | 1.000 |
| `budget_model` | G0 | 6 | 6 | 0 | 0.000 | 0.228 | 0.167 |
| `budget_model` | G8 | 6 | 5 | 3 | 0.600 | 0.800 | 0.600 |
| `budget_model` | G9 | 6 | 6 | 4 | 0.667 | 0.833 | 0.667 |

## Atom-Level Interpretation

Clear positive mechanisms:

- A3R constraint-safe plan: both model tiers pass under G8/G9.
- A5R stage-gate check: both model tiers pass under G8/G9.
- A8R evidence-type rules: strong model passes under G8/G9; low-cost model passes under G9, while G8 is pending from provider timeout.

Conditional or still weak mechanisms:

- A2R unsupported claim detection: strong model passes under G8/G9; low-cost model produces schema-valid output but does not bind each grounded claim to evidence IDs, so it fails strict citation grounding.
- A7R enumerated claim decision: strong model passes under G8/G9; low-cost model selects the right option but omits a complete evidence-linked rejection trace, so it fails strict trace completeness.
- A4R strict state inventory: low-cost model passes under G8/G9; strong model also passes after evaluator normalization for structured key/value output.

## Deviation Review

The only execution deviation is the pending A8R low-cost G8 run. Because:

- A8R low-cost G9 completed and passed,
- A8R strong G8/G9 completed and passed,
- all other low-cost G8 runs completed,
- the failed retries returned `The read operation timed out`,

the most reasonable interpretation is provider/model-response timeout for one request, not a fixture defect. A controlled retry with longer provider timeout and smaller `max_output_tokens` was attempted and still timed out, so Stage 7r should be reported as a 35/36 completed smoke with one formally documented execution deviation.

## Gate Decision

Stage 7r design and local validation are complete.

Stage 7r smoke is partially complete: 35/36 real outputs, with one documented provider-timeout deviation after final controlled retry.

Broader Stage 7 macro composition should not start as a full claim yet. The next valid step is to either:

1. formally accept a 35/36 partial smoke and proceed only with atoms whose G8/G9 behavior is already clean enough for composition, or
2. revisit the A8R low-cost G8 run later with a different provider/model routing path.

Under either path, A2R and A7R require additional low-cost-model optimization before they should be used in a large mixed workflow.
