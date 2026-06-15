# V4 Statistical And Presentation Review Response

Reviewed: 2026-06-15

## 1. Paired Analysis

Classification: **valid criticism, major technical correction**

The reviewer is correct. Stage B v5.3 forms 15 matched pairs by perturbation
condition and repetition. The preregistered Fisher exact test treated the arms
as independent and did not match the executed design.

Revision:

- added explicit pair construction and validation to the analysis script;
- reported 13 pass/pass, 2 treatment-pass/control-fail, 0 reverse, and
  0 fail/fail pairs;
- replaced Fisher as the primary result with exact McNemar
  (`p=0.500`);
- retained the old Fisher value only as a legacy sensitivity calculation;
- added tests for pair completeness and the exact McNemar calculation.

The mixed decision does not change because the `0.133` risk difference remains
below the preregistered `0.20` engineering threshold.

## 2. Abstract Density

Classification: **valid presentation criticism**

Revision: removed `15/15 versus 13/15` and `0.133 versus 0.20` from the
Abstract. The Abstract now reports the 40/40 stability result, its pooled
Wilson interval, and a short statement that the paired ablation did not meet
the preregistered engineering threshold.

## 3. Stage B Positioning

Classification: **valid contribution-framing concern**

Revision: Section 4.8 now states that Stage B is not a new general
state-transition method. It is presented as a stricter validation case for
the repair loop: bundled repair, component effect, and frozen-protocol
stability.

## 4. Per-Condition Uncertainty

Classification: **valid evaluation criticism**

Revision: added a condition table reporting five `8/8` results with Wilson
intervals `[0.676, 1.000]`, beside the pooled `40/40` interval
`[0.912, 1.000]`. The limitations section now states that each condition has
only eight runs.

## 5. Contribution 5

Classification: **valid precision edit**

Revision: Contribution 5 now names Qwen3-8B, one frozen protocol, 40 fresh
runs, and five designed perturbation conditions.

## 6. Table 4

Classification: **valid presentation criticism**

Revision: split the former Stage B row into:

- an ablation row for v5.2-v5.3 (`30 + 30`);
- a stability row for v5.4 (`40`).

This keeps component-effect evidence separate from frozen-protocol stability.

## Freeze-Proofreading Follow-Up

The final proofreading pass made four additional presentation and
interpretation corrections:

- rounded the reported McNemar result to `p=0.500`;
- removed the repeated `v5.4` label from the Table 4 Runs column;
- defined the preregistered `0.20` threshold as an absolute risk-difference
  engineering gate, equivalent to at least three additional passes in a
  15-run arm, and identified the Stage B v5.3 experiment plan as its source;
- stated that the two-discordant-pair comparison establishes neither
  equivalence nor the absence of a modest benefit.

Venue-specific compression remains separate from the evidence freeze. The
traceability matrix, detailed Stage B audit trail, and most artifact-level
material are candidates for supplementary placement once a target venue is
selected.
