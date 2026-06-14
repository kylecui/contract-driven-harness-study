# Stage B v5.1 State-Transition Repair Smoke Plan

Planned: 2026-06-14

Status: preregistered before provider execution

Execution authorization: user explicitly approved this four-call smoke on
2026-06-14

## Objective

Test whether Qwen3-8B under G9 satisfies the repaired v5.1 contract:

- copy four immutable slot-to-reference bindings exactly;
- apply one supplied unknown-to-known API-permission transition;
- preserve residual branch and CI unknown-state duties;
- return the complete declared post-transition gate;
- preserve the retention attestation.

This is a targeted repair smoke, not a reliability estimate.

## Baselines

Negative model baseline:

- Stage B v5 smoke failed 0/4 on the strict aggregate;
- the state transition itself passed 4/4;
- exact evidence arrays and strict gate passed 0/4;
- the gate mismatch was confined to an undisclosed exact `next_action`.

Positive local baseline:

- Stage B v5.1 local passed 38/38 expectations;
- nine evaluator tests passed;
- surface and repair-contract audits found zero violations;
- historical records remained 30/30, 32/32, 22/22, and 110/110.

## Repair Under Test

The v5.1 protocol changes two model-facing surfaces:

1. immutable arrays are declared in `evidence_bindings`, separate from
   editable claim prose;
2. the complete exact `transition_gate`, including `next_action`, appears in
   the model-visible `OutputContract`.

The evidence arrays, state transition, residual state, gate, and attestation
remain exact obligations. The original v5 result will not be rescored.

## Hypotheses

H1-canonical: the canonical v5.1 fixture passes both repetitions.

H2-dual-surface: the `source_references` and paraphrased-state fixture passes
both repetitions.

H3-binding: every output preserves all four exact evidence bindings.

H4-mutation: every output moves only the API-permission state from unknown to
approved.

H5-gate: every output copies the complete declared transition gate, including
`next_action`.

The smoke passes only if both fixtures pass 2/2.

## Frozen Matrix

| Variable | Value |
|---|---|
| Model | `Qwen/Qwen3-8B` |
| Model tier | `budget_model` |
| Harness | G9 |
| Temperature | 0 |
| Thinking | disabled |
| Maximum output tokens | 2000 |
| Fixtures | canonical, dual-surface stress |
| Repetitions | two per fixture |
| Planned calls | four |

## Metrics

- `schema_validity`;
- `exact_evidence_array_preservation`;
- `residual_unknown_vocabulary_accuracy`;
- `state_transition_accuracy`;
- `transition_gate_accuracy`;
- `retention_attestation_accuracy`;
- `controlled_state_mutation_success`;
- `task_success`.

A run passes only when every component metric equals `1.000`.

## Ablation Evidence

The local suite already contains:

- `v5_observed_semantic_remap`, which fails only evidence retention;
- `wrong_gate_next_action`, which fails only strict gate accuracy;
- `static_pretransition_copy`, which fails residual state, transition, and
  gate.

This smoke does not add paid ablation arms. Its four calls test transfer of the
fully repaired contract.

## Execution Rules

- Re-run the v5.1 local gate before provider execution.
- Compile all four full G9 packets and export exact prompts.
- Verify every fixture event remains `fixture_only`.
- Check prompts for golden-output or evaluator-only leakage.
- Run adapter dry-run and key-required provider preflight.
- Preserve incremental events, raw outputs, provider usage, and retry lineage.
- Do not retry a complete, parseable semantic failure.
- Retry only a provider error, timeout, or truncated invalid JSON.
- Retain every original attempt.

## Decision Rule

Pass:

- four valid outputs are collected;
- both fixtures pass 2/2;
- every component metric equals `1.000` in every run.

Fail:

- either fixture passes fewer than 2/2 after valid provider recovery;
- any complete output changes a binding, residual state value, transition
  field, gate field, or attestation field.

Runtime inconclusive:

- unrecovered provider or truncation failures prevent a complete four-run
  record.

## Claim Boundary

Passing would support:

> Under G9, Qwen3-8B satisfied one repaired, fully model-visible controlled
> transition contract in two representation variants with two repetitions
> each.

Passing would not establish:

- a stable success rate;
- that either repair alone caused the result;
- general state-machine competence;
- autonomous tool authorization or execution;
- rollback, concurrency, conflicting-event handling, or production readiness.

## Validity Threats

Internal validity:

- both repairs are bundled, so this smoke cannot isolate their individual
  causal effects.

Construct validity:

- exact binding retention measures declared contract adherence, not whether
  alternative evidence mappings are semantically reasonable.

External validity:

- one event and two representation variants do not represent general state
  machines or workflows.

Conclusion validity:

- four runs are a debugging gate, not a statistical reliability estimate;
  temperature zero does not remove provider-side variability.

## Pooling Policy

v5.1 is a new protocol. These runs must not replace, rescore, or pool with the
failed Stage B v5 smoke or any earlier Stage B protocol.
