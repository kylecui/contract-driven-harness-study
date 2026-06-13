# Stage B v2 Experiment Plan

Prepared: 2026-06-13

## 1. Hypothesis

- H1: every macro-condition cell passes at least 2/3 Qwen3-8B G9 runs.
- Falsifiability condition: one or more cells pass fewer than 2/3 runs.
- Success threshold: 10/10 cells meet the threshold without post-execution
  evaluator or fixture changes.

## 2. Variables

| Variable | Type | Values | Rationale |
|---|---|---|---|
| Macro | Independent | Stage 7e v4; Stage 7-next | Tests both admitted compositions |
| Representation condition | Independent | Canonical; shuffled; field alias; state paraphrase; distractor | Tests declared representation robustness |
| Contract pass | Dependent | 0 or 1 | Primary admission outcome |
| Failed metric | Dependent | Evaluator metric name | Locates the violated mechanism |
| Runtime and tokens | Dependent | Milliseconds and provider counts | Separates contract and runtime failures |

## 3. Controls

| Control factor | Fixed setting | Why it matters |
|---|---|---|
| Provider/model | SiliconFlow `Qwen/Qwen3-8B` | Avoids mixing model and perturbation effects |
| Harness | G9 v2 | Tests one repaired package |
| Temperature | 0 | Reduces configured sampling variation |
| Thinking | Disabled | Avoids hidden reasoning-budget variation |
| Output budget | 3000 tokens | Reduces v1 truncation risk uniformly |
| Repetitions | 3 per cell | Preserves the preregistered screening design |
| Evaluator | Frozen before execution | Prevents outcome-driven scoring changes |
| Contract visibility | Surface-only model contract; canonical evaluator contract | Prevents evaluator internals from contaminating alias prompts |

## 4. Baselines

| Baseline | Category | Use | Fairness boundary |
|---|---|---|---|
| v2 canonical cell | Within-protocol | Reference for each macro | Same model, budget, prompt contract, and evaluator |
| Stage B v1 | Historical diagnostic | Shows failure that motivated repair | Not pooled because contract and output budget changed |
| Golden/known-bad local gate | Deterministic control | Validates evaluator construct behavior | Not a model-performance baseline |

## 5. Metrics

| Claim | Metric | Computation | Reporting |
|---|---|---|---|
| Cell stability | Cell pass proportion | Passed runs / 3 | Count, proportion, Wilson interval |
| Contract adherence | Binary pass | All required metrics meet thresholds | Every run listed |
| Failure localization | Failed metric | Metrics below threshold | Category and artifact links |
| Runtime integrity | Provider/timeout/truncation status | Event-log classification | Counts and lineage |
| Cost observation | Token use | Provider usage metadata | Descriptive only |

These metrics evaluate contract adherence rather than open-ended output quality
or human preference.

## 6. Workload

The workload contains ten cells: two admitted macros crossed with five
representation conditions. Each cell has three sequential provider runs, for 30
runs total.

The fixtures cover one canonical case, two surface-variation cases, one order
variation, and one irrelevant-evidence stressor. They do not represent arbitrary
real-world workflow variation.

## 7. Execution Order

1. Freeze code, fixtures, prompts, provider config, and checksums.
2. Confirm local golden/known-bad and v1 regression gates.
3. Run structural preflight with key presence required.
4. Run adapter dry-run and inspect all 30 mappings.
5. Obtain explicit approval for paid execution.
6. Execute all 30 calls while writing incremental events.
7. Evaluate without modifying the frozen evaluator.
8. Review every failed, truncated, timed-out, or retried run.
9. Apply the preregistered cell stop rule.
10. Publish raw and corrected interpretations only if a new construct defect is
    found; do not pool across scoring versions.

## 8. Statistical Handling

The primary decision is threshold-based rather than a null-hypothesis test.
Three observations per cell are too small for a precise stability estimate.
Wilson intervals will show this uncertainty; aggregate proportions will not be
treated as 30 independent samples for broad inference.

## 9. Reproducibility Requirements

- record Git commit and file checksums;
- preserve exact prompts, adapter requests, outputs, traces, and event logs;
- record model ID, temperature, output budget, and thinking setting;
- preserve retry lineage and original failures;
- keep Stage B v1 and v2 artifacts in separate directories;
- run repository safety scans before publication.
