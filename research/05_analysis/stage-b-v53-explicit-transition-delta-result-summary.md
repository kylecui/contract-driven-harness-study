# Stage B v5.3 Explicit Transition-Delta Result

Executed: 2026-06-14

Decision: mixed result

## Result

| Protocol | Strict pass | Residual state | Evidence | Transition | Gate |
|---|---:|---:|---:|---:|---:|
| Explicit transition delta | 15/15 | 15/15 | 15/15 | 15/15 | 15/15 |
| Exact postcondition only | 13/15 | 13/15 | 15/15 | 15/15 | 15/15 |

The residual-state risk difference was `0.133`, below the preregistered
engineering threshold of `0.20`.

The 30 runs form 15 matched pairs by perturbation condition and repetition.
Thirteen pairs were pass/pass, two were explicit-delta pass/postcondition-only
fail, and none favored the postcondition-only arm. The exact McNemar
two-sided result was `p=0.500`.

H1 delta robustness, H3 obligation preservation, and H4 no-regression passed.
H2 delta effect did not pass.

## Failure Audit

Both failed P1 outputs:

- moved API permission out of `unknown_state`;
- added the correct known-state object;
- emitted the correct transition record;
- preserved evidence, gate, and attestation;
- retained the obsolete API-permission entry in `forbidden_inferences`.

No P2 output failed. No provider, timeout, truncation, parse, or retry issue
occurred.

## Interpretation

The experiment supports an absolute result:

> The explicit-delta protocol satisfied the complete controlled-transition
> contract in 15/15 runs across all five perturbation conditions.

It does not support the preregistered large causal-effect claim:

> Current evidence does not show that the explicit delta improves residual
> state by at least 0.20 over an exact, strongly stated postcondition.

With only two discordant pairs, the paired result has little power for small
effects. It rules out neither a modest benefit nor equivalence.

The baseline was deliberately strong. It exposed the same exact final state
and instructed the model to satisfy that object exactly. This prevents an
artificially easy comparison, but it also means the observed marginal effect
is smaller than the v5.2 failure rate suggested.

## Post-Freeze Analysis Correction

The first analysis-script ordering classified `H1=true, H2=false` as
`no_engineering_scale_delta_effect_observed`. The written preregistration
defines that combination as a mixed result.

The decision branch and its synthetic test were corrected to follow the
written rule. No prompt, fixture, evaluator, metric, threshold, output, or
provider record changed.

On 2026-06-15, a second analysis correction replaced the preregistered Fisher
exact test with an exact McNemar test because the outcomes are paired by
condition and repetition. The original independent-groups Fisher value,
`p=0.48275862`, remains in the machine-readable analysis as a legacy
sensitivity value. It is no longer the primary inferential result. The
engineering-threshold decision and the mixed result did not change.

## Next Gate

The preregistered causal-confirmation gate did not pass, so v5.4 must not be
described as causal confirmation.

The 15/15 P2 result is sufficient to motivate a separate fresh absolute
stability confirmation. That experiment must:

- use only the frozen explicit-delta protocol;
- use 40 new runs;
- preserve all five perturbation conditions;
- freeze thresholds before execution;
- make no comparative causal claim.

