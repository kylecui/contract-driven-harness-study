# Stage B v5.4 Explicit-Delta Stability Confirmation Plan

Prepared: 2026-06-14

Status: preregistered before v5.4 provider execution

## Rationale

Stage B v5.3 produced a mixed causal result but a clean absolute pilot:
explicit delta passed 15/15 complete runs across five perturbations.

This experiment asks a different question from v5.3:

> Does the frozen explicit-delta protocol maintain high absolute contract
> adherence over 40 fresh executions?

It does not test or claim a `0.20` causal advantage over postcondition-only.

## Frozen Protocol

Reuse the exact model-facing P2 fixtures frozen for Stage B v5.3:

- same task spec;
- same evidence bundles;
- same memory slices;
- same output contracts;
- same structured transition delta;
- same evaluator;
- same provider settings.

No fixture or evaluator change is permitted.

## Matrix

```text
5 perturbation conditions x 8 fresh repetitions = 40 calls
```

Conditions:

1. canonical;
2. field alias;
3. evidence order shuffled;
4. distractor evidence;
5. unknown-state paraphrase.

Model: `Qwen/Qwen3-8B`

Harness: G9

Temperature: 0

Thinking: disabled

Maximum output tokens: 2,000

## Primary Hypothesis

H1-absolute-stability passes if:

- strict aggregate success is at least 38/40;
- every condition passes at least 7/8 repetitions.

## Component Guardrails

H2-critical-components passes if each of the following reaches at least 39/40:

- exact evidence-array preservation;
- residual-state accuracy;
- state-transition accuracy;
- complete-gate accuracy.

H3-execution-integrity passes if:

- all 40 calls produce complete evaluable outputs;
- provider error rate does not exceed 10%;
- no semantic failure is retried.

## Decision

Confirmed bounded stability:

- H1, H2, and H3 all pass.

Mixed stability:

- H1 passes but a component guardrail fails;
- or pooled success passes while one condition is below 7/8.

Stability not confirmed:

- strict aggregate is below 38/40.

Protocol failure:

- fixtures, prompts, evaluator, or thresholds change after freeze;
- unrecovered runtime failures prevent a fair 40-run result.

## Statistics

Report:

- strict and component success counts;
- pooled and per-condition rates;
- two-sided 95% Wilson intervals;
- latency range, median, and P90;
- prompt, completion, and total tokens;
- provider errors and retries.

No hypothesis test against v5.3 or P1 is planned. The 40 v5.4 runs are the
confirmatory dataset and are not pooled with the 15 v5.3 pilot runs for the
primary stability rate.

## Retry Rule

- Do not retry complete semantic failures.
- Retry only provider errors, timeouts, or truncated invalid JSON.
- Preserve all attempts and retry lineage.

## Claim Boundary

If confirmed, the experiment supports:

> Under the frozen explicit-delta G9 protocol, Qwen3-8B maintained high exact
> contract adherence across 40 fresh runs and five bounded perturbations.

It does not establish:

- causal superiority over postcondition-only;
- arbitrary state-machine reliability;
- autonomous tool execution;
- rollback or concurrent transition correctness;
- workflow or production readiness.

