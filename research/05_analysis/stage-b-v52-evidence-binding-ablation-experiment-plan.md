# Stage B v5.2 Evidence-Binding Ablation Plan

Planned: 2026-06-14

Status: preregistered before fixture generation and provider execution

Execution authorization: user approved the 30-run experiment on 2026-06-14

## Research Question

Does separating immutable slot-to-reference bindings from editable claim prose
improve Qwen3-8B contract adherence when the complete transition gate is
equally visible in both arms?

The experiment also tests whether the repaired representation transfers across
five bounded prompt-surface perturbations.

## Baselines

Negative baseline:

- Stage B v5 used claim-coupled evidence arrays and an incomplete visible gate;
- its strict smoke passed 0/4 on evidence retention and 0/4 on gate accuracy.

Positive repaired baseline:

- Stage B v5.1 separated evidence bindings and exposed the complete gate;
- its targeted smoke passed 4/4 with every component at `1.000`.

Because v5 changed two factors together, neither result identifies the
independent contribution of evidence-binding separation. v5.2 holds the gate
constant and varies only the evidence representation.

## Factorial Design

Primary factor:

| Arm | Output evidence representation |
|---|---|
| `claim_coupled` | `grounded_claims[]` contains editable claim prose plus immutable slot ID and reference array |
| `binding_separated` | `evidence_bindings[]` contains only immutable slot ID and reference array |

Both arms receive:

- the same task objective and evidence;
- the same transition event;
- the same complete exact `transition_gate`;
- the same residual state obligations;
- the same reference arrays;
- the same G9 harness and provider settings.

Perturbation factor:

1. `canonical`;
2. `field-alias`;
3. `evidence-order-shuffled`;
4. `distractor-evidence`;
5. `unknown-state-paraphrase`.

Each arm-condition cell has three repetitions:

```text
2 representations x 5 perturbations x 3 repetitions = 30 runs
```

## Frozen Provider Settings

| Variable | Value |
|---|---|
| Model | `Qwen/Qwen3-8B` |
| Model tier | `budget_model` |
| Harness | G9 |
| Temperature | 0 |
| Thinking | disabled |
| Maximum output tokens | 2,000 |
| Planned calls | 30 |

## Hypotheses

H1-separated-robustness:

- `binding_separated` passes at least 13/15 runs; and
- every perturbation cell passes at least 2/3 repetitions.

H2-representation-effect:

- the exact-evidence-retention risk difference,
  `binding_separated - claim_coupled`, is at least `0.20`.

H3-gate-control:

- each arm passes complete-gate accuracy in at least 14/15 runs.

H4-transition-control:

- each arm passes state-transition accuracy in at least 14/15 runs.

H5-surface-transfer:

- field alias, shuffled evidence, distractors, and paraphrased state do not
  reduce the separated arm below the 2/3 cell threshold.

## Metrics

Per run:

- `schema_validity`;
- `exact_evidence_array_preservation`;
- `residual_unknown_vocabulary_accuracy`;
- `state_transition_accuracy`;
- `transition_gate_accuracy`;
- `retention_attestation_accuracy`;
- `controlled_state_mutation_success`;
- `task_success`.

Primary comparison:

- exact-evidence-retention pass rate by representation arm;
- risk difference with Wilson intervals for each arm;
- two-sided Fisher exact test.

Secondary comparisons:

- strict aggregate pass rate by arm;
- component pass rates by arm and perturbation cell;
- cell decisions using the preregistered 2/3 threshold.

The risk-difference threshold is the engineering-effect gate. Fisher's exact
test is reported as supporting evidence, not as the sole decision rule.

## Decision Rules

Evidence separation has a supported directional contribution if:

- H1 passes; and
- H2 passes.

Evidence separation has strong statistical support in this slice if the above
conditions pass and Fisher's exact `p < 0.05`.

No observed representation effect if:

- both arms differ by less than `0.20` on exact evidence retention.

Mixed result if:

- the separated arm is robust but H2 fails; or
- H2 passes while one separated perturbation cell fails.

Protocol failure if:

- local golden/known-bad discrimination fails;
- a model-surface isolation check fails;
- the complete gate is not equally visible in both arms;
- unrecovered runtime failures prevent the 30-run matrix from completing.

## Local Gates

Before provider execution:

- every golden output must pass;
- every known-bad output must fail the strict aggregate;
- known-bad component vectors must match their declarations;
- both arms must reject evidence omission, evidence remapping, wrong
  `next_action`, residual-state corruption, and static copying;
- alternative fields and state vocabularies must not leak across fixtures;
- all evaluator unit tests must pass;
- the complete gate objects must be identical across paired arm-condition
  fixtures except for fixture-specific state vocabulary.

## Retry Rule

- Do not retry a complete, parseable semantic failure.
- Retry only provider errors, timeouts, or truncated invalid JSON.
- Retain every attempt and retry lineage.

## Validity Threats

Internal validity:

- the claim-coupled arm has a larger output payload because it includes prose;
  that extra coupling burden is part of the tested mechanism, but token length
  may mediate the effect.

Construct validity:

- exact array retention measures adherence to a declared mapping, not whether
  alternative evidence choices are semantically defensible.

Conclusion validity:

- 15 runs per arm provide limited power. A large effect can be detected, but a
  null or small difference will remain uncertain.

External validity:

- one transition macro, one model, and five bounded perturbations do not cover
  arbitrary workflows, tools, or state machines.

## Claim Boundary

Passing H1 supports robustness of the separated representation in this
bounded perturbation suite.

Passing H1 and H2 supports a directional contribution from evidence-binding
separation under a complete visible gate.

Neither result establishes universal weak-model reliability, strong-model
equivalence, or production readiness.

## Stop Rule

Stop before provider execution on any local-gate failure.

After provider execution, stop and audit before interpretation if:

- any provider attempt is incomplete;
- any output is truncated;
- any evaluator result conflicts with raw-output inspection;
- any major deviation from the frozen matrix occurs.
