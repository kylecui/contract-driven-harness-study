# Stage B v5.3 Paired-Analysis Correction

Corrected: 2026-06-15

## Reason

The v5.3 plan preregistered a two-sided Fisher exact test. That test treats the
two arms as independent samples. The executed design instead forms 15 matched
pairs:

```text
5 perturbation conditions x 3 repetitions
```

Within each pair, the baseline and treatment use the same condition,
repetition index, initial state, required postcondition, evidence bindings,
event, gate, output contract, and evaluator. The treatment adds only the
structured transition delta.

## Corrected Analysis

The primary residual-state outcomes are:

| Treatment | Control | Pairs |
|---|---|---:|
| pass | pass | 13 |
| pass | fail | 2 |
| fail | pass | 0 |
| fail | fail | 0 |

The two discordant pairs are:

- `evidence_order_shuffled`, repetition 3;
- `field_alias`, repetition 3.

The exact two-sided McNemar test, equivalently an exact two-sided binomial test
on the discordant pairs, gives:

```text
p = 0.500
```

The absolute risk difference remains `0.133333`, below the preregistered
engineering threshold of `0.20`.

The v5.3 experiment plan fixed that threshold before execution. With 15 runs
per arm, `0.20` corresponds to at least three additional passes. It is a
coarse engineering decision gate, not a significance threshold, equivalence
margin, or power-derived minimum detectable effect. The preregistration did
not include a separate utility analysis for the cutoff.

## Effect On The Decision

The correction does not change the v5.3 decision:

- treatment adherence remains 15/15;
- control adherence remains 13/15;
- the engineering-effect threshold still does not pass;
- the exact paired test is not statistically significant;
- the result remains mixed.

With only two discordant pairs, the comparison has little power for small
effects. It establishes neither equivalence nor the absence of a modest
benefit.

The original Fisher value, `p=0.48275862`, is retained only as a legacy
independent-groups sensitivity calculation in the machine-readable analysis.
No prompt, fixture, output, evaluator score, threshold, provider record, or
retry decision changed.
