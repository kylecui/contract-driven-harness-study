# Stage B v5.3 Explicit Transition-Delta Ablation Plan

Prepared: 2026-06-14

Status: preregistered before fixture generation and provider execution

Statistical-method correction (2026-06-15): the plan below preregistered a
two-sided Fisher exact test. The completed matrix forms 15 matched pairs by
perturbation condition and repetition, so the primary paired analysis was
corrected post-execution to an exact McNemar test. The original plan remains
visible for audit. See
`research/05_analysis/stage-b-v53-paired-analysis-correction.md`.

## Motivation

Stage B v5.2 did not observe an engineering-scale independent effect from
separating evidence bindings. Its failure audit instead found a repeated state
mutation error: the model moved API permission from unknown to known but
retained the obsolete matching `forbidden_inferences` entry in 9/30 runs.

The next question is whether an explicit state-difference control object
improves exact multi-array state mutation relative to an equally visible
declarative postcondition.

## Research Question

Does a structured `required_transition_delta` improve exact residual-state
adherence for Qwen3-8B under G9 when the event, evidence bindings, initial
state, final postconditions, gate, output schema, perturbations, and evaluator
are held constant?

## Arms

Model-visible arm labels are neutral.

| Profile | Internal arm | Additional control |
|---|---|---|
| P1 | `postcondition_only` | Exact initial state and exact required postconditions |
| P2 | `explicit_delta` | The same objects plus `required_transition_delta` |

The P2 delta declares:

- the value to remove from `unknown_state`;
- the matching value to remove from `forbidden_inferences`;
- the exact known-state object to add;
- the residual unknown and forbidden values to preserve in order.

Both profiles use separated immutable `evidence_bindings`. No claim-prose
representation factor is varied.

## Perturbation Conditions

1. canonical;
2. field alias (`evidence_ids` to `source_references`);
3. evidence-bundle order shuffled;
4. distractor evidence;
5. paraphrased state vocabulary.

## Matrix

```text
2 profiles x 5 conditions x 3 repetitions = 30 calls
```

Model: `Qwen/Qwen3-8B`

Harness: G9

Provider: SiliconFlow

Temperature: 0

Thinking: disabled

Maximum output tokens: 2,000

## Variables

Independent variable:

- presence of the structured `required_transition_delta`.

Primary dependent variable:

- `residual_unknown_vocabulary_accuracy`.

Secondary dependent variables:

- strict controlled-state-mutation success;
- schema validity;
- exact evidence-array preservation;
- state-transition accuracy;
- complete-gate accuracy;
- retention-attestation accuracy.

Controlled variables:

- model and provider settings;
- evidence bindings;
- initial state and final postconditions;
- transition event;
- expected output;
- output schema;
- gate and attestation;
- perturbation conditions;
- evaluator and retry policy.

## Hypotheses

H1-delta-robustness:

- P2 passes residual-state accuracy in at least 14/15 runs;
- P2 passes strict aggregate success in at least 13/15 runs;
- every P2 perturbation cell passes at least 2/3 strict repetitions.

H2-delta-effect:

- the residual-state risk difference,
  `explicit_delta - postcondition_only`, is at least `0.20`.

H3-obligation-preservation:

- P2 passes evidence, transition, gate, and attestation accuracy in at least
  14/15 runs for each component.

H4-no-regression:

- P1 and P2 each pass schema validity in at least 14/15 runs.

## Statistical Analysis

Primary comparison:

- residual-state pass rate by arm;
- absolute risk difference;
- two-sided Fisher exact test;
- 95% Wilson interval for each arm.

The `0.20` risk-difference threshold is the engineering-effect gate. Fisher's
exact result is supporting evidence, not the sole decision rule.

Secondary comparisons:

- strict aggregate rate by arm;
- component rates by arm and cell;
- per-cell 2/3 decisions.

## Decision Rules

Supported mechanism contribution:

- H1 and H2 pass.

Strong statistical support:

- H1 and H2 pass and Fisher's exact `p < 0.05`.

Mixed result:

- only one of H1 or H2 passes;
- or P2 passes globally but fails a perturbation cell.

No engineering-scale effect:

- the absolute primary risk difference is below `0.20`.

Protocol failure:

- the paired expected outputs differ;
- a non-delta obligation differs between paired fixtures;
- local golden/known-bad discrimination fails;
- prompts leak evaluator or golden artifacts;
- unrecovered runtime failures prevent completing the matrix.

## Reasonable Optimization Boundary

Allowed before freeze:

- make the state operation explicit and structurally inspectable;
- repeat the same obligation in a local instruction and control object;
- add deterministic known-bads for observed state errors;
- improve prompt clarity without changing expected output.

Not allowed after seeing provider results:

- relax exact matching;
- remove a failed perturbation;
- change the primary metric or threshold;
- retry complete semantic failures;
- rescore outputs under a new interpretation;
- pool v5.2 and v5.3 runs.

## Local Gates

Before provider execution:

- every golden output passes;
- every known-bad output fails the declared component vector;
- the observed obsolete-forbidden-inference pattern is rejected;
- paired expected outputs are byte-equivalent after fixture IDs are excluded;
- paired event, postcondition, evidence, gate, and attestation objects match;
- the only model-visible semantic difference is the delta control;
- all unit tests and v5.2/v5.1 regression checks pass;
- preflight reports zero errors and zero warnings.

## Retry Rule

- Do not retry complete, parseable semantic failures.
- Retry only provider errors, timeouts, or truncated invalid JSON.
- Preserve every attempt and retry lineage.

## Stage B v5.4 Gate

Proceed to a fresh 40-run P2 stability confirmation only if v5.3 supports the
mechanism contribution.

The planned v5.4 matrix is:

```text
5 perturbation conditions x 8 fresh repetitions = 40 calls
```

Provisional stability thresholds:

- strict aggregate at least 38/40;
- every condition at least 7/8;
- evidence, transition, and gate each at least 39/40;
- zero semantic retries.

These thresholds must be frozen in a separate v5.4 protocol before execution.

## Claim Boundary

If positive, v5.3 may support a bounded causal claim that explicit transition
deltas improve exact multi-array state mutation for this model, macro, and
perturbation suite.

It cannot establish arbitrary state-machine reliability, tool execution,
rollback, concurrency, workflow autonomy, or production readiness.

