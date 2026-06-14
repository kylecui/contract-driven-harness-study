# Stage B v5.4 Pre-Execution Audit

Prepared: 2026-06-14

Decision: PASS

## Research Boundary

- v5.4 tests absolute stability of the frozen explicit-delta protocol.
- It does not retest the v5.3 causal effect threshold.
- The 40 fresh runs will not be pooled with the 15-run v5.3 pilot for the
  primary stability rate.
- Passing v5.4 cannot erase the mixed v5.3 comparison.

## Matrix

- Planned calls: 40
- Model: `Qwen/Qwen3-8B`
- Harness: G9
- Conditions: 5
- Fresh repetitions per condition: 8
- Referenced fixtures: only the five frozen v5.3 P2 fixtures
- P1 fixtures referenced: 0

The generated packet audit found:

- 40/40 packets contain `required_transition_delta`;
- 8 packets in each declared perturbation condition;
- 40/40 packets use `budget_model` and G9;
- 0 golden-output, known-bad, or evaluation-spec leaks.

## Prompt Equivalence

Each v5.4 prompt body was compared with the corresponding frozen v5.3 P2
prompt body after removing only the first benchmark-run heading.

- Equivalent prompt bodies: 40/40
- Mismatches: 0
- Prompt character range: 7,820 to 8,248

The first heading differs only because v5.4 uses fresh run identifiers.

## Local Verification

- Python compilation: PASS
- New v5.4 analysis tests: 5/5
- Full method-script unit suite: 50/50
- Provider config validation with required key: PASS
- Adapter dry run: 40/40
- Preflight: PASS, 0 errors, 0 warnings

## Frozen Thresholds

- strict aggregate: at least 38/40;
- strict success in every condition: at least 7/8;
- evidence, residual state, transition, and gate: each at least 39/40;
- all 40 calls evaluable;
- provider error rate no greater than 10%;
- no semantic retries.

## Retry Policy

Complete parseable semantic failures will not be retried. Retries are allowed
only for provider errors, timeouts, or truncated invalid JSON, with attempt
lineage preserved.

## v5.3 Analysis Correction

The v5.3 decision-branch correction is recorded separately. It changed the
machine label to match the preregistered written rule (`mixed_result`) and did
not change prompts, fixtures, evaluator behavior, metrics, thresholds, or
outputs. v5.4 freezes the corrected analysis state before any v5.4 call.

## Execution Gate

The protocol is ready to freeze. Real provider execution may begin only after
the freeze manifest is written.
