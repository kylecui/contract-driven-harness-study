# Post-Freeze Evidence Extension Plan

Prepared: 2026-06-13

Baseline: frozen v3.1.1 paper body

Purpose: address the security/systems peer review without weakening experimental discipline or silently changing the frozen paper.

## Research Questions

1. Does the low-cost model maintain contract adherence across repeated provider executions?
2. Do admitted macros survive representation-preserving perturbations?
3. What latency, token, retry, and provider-cost overhead does the harness add?
4. Does low-cost model plus G9 offer a useful cost/reliability tradeoff against a strong model with weak or full harnessing?

## Stage A: Instrumentation And Local Gates

No paid model calls.

Status: **STAGE B REPAIR ABLATION COMPLETE; STAGE C/D BLOCKED**

Required changes:

- [x] capture provider `usage` fields when available;
- [x] record prompt tokens, completion tokens, total tokens, request identifiers, and retry lineage;
- [x] preserve prompt/output bytes and elapsed time;
- [x] add a dated provider-pricing snapshot outside the run results immediately before Stage B;
- [x] define variant-aware golden and known-bad fixtures;
- [x] verify that evaluators accept permitted aliases and still reject missing evidence obligations.

Instrumentation check:

- three local response/lineage unit tests pass;
- the adapter and test module compile;
- the four-run SiliconFlow smoke manifest completes in dry-run mode;
- no provider call was made;
- see `research/07_reviews/contract-driven-harness-adapter-usage-instrumentation-check.md`.

Perturbation gate:

- 10 fixtures cover two macros and five conditions;
- 10/10 golden cases pass;
- 18/18 known-bad cases fail on their predeclared target metrics;
- 4/4 original macro regression cases preserve prior behavior;
- the 30-run Qwen3-8B + G9 queue passes preflight and adapter dry-run;
- see `research/07_reviews/contract-driven-harness-post-freeze-stage-a-summary.md`.

Gate:

- canonical golden passes;
- every perturbation golden passes;
- every perturbation known-bad fails for the intended reason;
- no secret or provider credential enters artifacts;
- dry-run manifests compile with zero errors.

## Stage B: 30-Run Perturbation Pilot

Outcome on 2026-06-13:

- 30/30 provider calls returned with no provider error;
- a post-execution construct-validity correction changed the run-pass result
  from raw 0/30 to corrected 16/30;
- 5/10 macro-condition cells reached the required 2/3 threshold;
- the pilot failed its stop rule;
- Stage C and Stage D are blocked pending a fresh Stage B v2 protocol.

See
`research/07_reviews/contract-driven-harness-stage-b-30-run-summary.md`.

### Stage B v5.2 Repair Ablation

Outcome on 2026-06-14:

- 30/30 Qwen3-8B + G9 calls completed with no provider error or retry;
- binding-separated evidence passed 15/15 exact checks;
- claim-coupled evidence passed 14/15 exact checks;
- the `0.067` risk difference missed the preregistered `0.20` engineering
  threshold, with Fisher's exact two-sided `p=1.000`;
- both profiles passed 10/15 strict aggregates;
- gate and transition accuracy passed 30/30;
- nine strict failures shared one residual forbidden-inference error;
- one claim-coupled distractor run produced a genuine evidence remapping.

Decision:

- the hypothesized large independent benefit from evidence-binding separation
  was not observed;
- no additional run is needed for that ablation question;
- Stage C and Stage D remain blocked because stable macro reliability has not
  been established;
- a future reliability experiment must restore the explicit state-removal
  operation locally and start as a new protocol with fresh runs.

See
`research/05_analysis/stage-b-v52-evidence-binding-ablation-result-summary.md`.

Model: `Qwen/Qwen3-8B`

Harness arm: G9

Inference controls: `temperature=0`, `max_tokens=2000`,
`enable_thinking=false`; do not send `reasoning_effort` or `thinking_budget`.

Macros:

- Stage 7e v4 evidence-bound decision;
- Stage 7-next method-plan update.

Conditions:

1. canonical contract;
2. evidence order shuffled;
3. declared field alias, such as `evidence_ids` to `source_references`;
4. semantically equivalent unknown-state wording;
5. irrelevant but plausible distractor evidence.

Design:

```text
2 macros x 5 conditions x 3 repetitions = 30 runs
```

Stop immediately if:

- an evaluator cannot distinguish an allowed representation from a semantic failure;
- any condition passes fewer than 2/3 runs;
- provider failure rate exceeds 20%;
- output truncation or timeout prevents a fair comparison;
- a perturbation changes the obligation rather than its representation.

## Stage C: Stability Expansion

Proceed only if Stage B passes without fixture or evaluator changes.

Current status: **BLOCKED**. Stage B did not pass and required an evaluator
construct-validity correction.

Add five repetitions to each existing cell:

```text
2 macros x 5 conditions x 5 additional repetitions = 50 additional runs
```

Combined total:

```text
2 macros x 5 conditions x 8 repetitions = 80 runs
```

Report:

- pass rate by macro and condition;
- pooled pass rate by macro;
- two-sided 95% Wilson intervals;
- provider failure/retry rate;
- latency median, P90, and range;
- prompt/completion token distributions;
- failures separated into contract, evaluator, truncation, timeout, and provider categories.

If all 40 runs for one macro pass, the descriptive 95% Wilson lower bound is approximately 0.912. This supports a bounded stability statement across the tested perturbations. It does not establish open-ended workflow reliability.

If Stage B causes any fixture, contract, or evaluator revision, Stage C must use fresh runs; the pilot cannot be pooled into the final 40-run macro estimate.

## Stage D: Overhead Matrix

Current status: **BLOCKED** until a repaired Stage B protocol passes.

Use one representative admitted macro unless Stage B shows materially different behavior between the two macros.

Primary 2x2 design:

| Model | Harness |
|---|---|
| Qwen3-8B | G0 |
| Qwen3-8B | G9 |
| DeepSeek-V3.2 | G0 |
| DeepSeek-V3.2 | G9 |

Target:

```text
4 cells x 10 repetitions = 40 runs
```

Existing compatible G9 runs may be reused only when instrumentation fields are complete and protocol-equivalent. Otherwise, run fresh cells.

Primary decision metrics:

- contract pass rate;
- provider cost per successful contract pass;
- median and P90 latency;
- prompt and completion tokens;
- timeout, truncation, and retry rate.

Do not use the current heuristic `cost_efficiency=1.000` as a billing claim.

## Statistical Boundary

- Repetition estimates run stability, not task-family generalization.
- Perturbation estimates local representation robustness, not arbitrary schema portability.
- Confidence intervals describe observed binary pass rates; they do not remove fixture dependence.
- Provider comparisons require a dated pricing snapshot and matched task/contract conditions.
- Any claim beyond the tested macros remains a non-claim.

## Execution Budget

Minimum paid extension if no reset is required:

```text
Stage B 30 + Stage C 50 + Stage D 40 = 120 calls
```

Stage B is the first paid gate. Stage C and Stage D require a separate go decision after reviewing Stage B failures, latency, and estimated cost.

## Paper Versioning

- v3.1.1 remains frozen and citable as the current bounded-evidence draft.
- Citation and layout work may continue against v3.1.1.
- Successful new evidence enters a separate v4 draft after an explicit unfreeze decision.
- Failed or mixed results must be published in the v4 evidence record rather than discarded.
