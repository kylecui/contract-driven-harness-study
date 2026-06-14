# Stage B v5 Controlled State-Transition Smoke Result

Executed: 2026-06-14

Decision: fail under the preregistered strict protocol

## Strict Result

Qwen3-8B under G9 passed 0/4 complete runs:

| Fixture | Passes | Decision |
|---|---:|---|
| Canonical state transition | 0/2 | Fail |
| Dual-surface stress | 0/2 | Fail |
| Total | 0/4 | Fail |

The preregistered rule required both fixtures to pass 2/2 and every component
metric to equal `1.000`.

## Component Result

| Metric | Passing runs |
|---|---:|
| `schema_validity` | 4/4 |
| `exact_evidence_array_preservation` | 0/4 |
| `residual_unknown_vocabulary_accuracy` | 4/4 |
| `state_transition_accuracy` | 4/4 |
| `transition_gate_accuracy` | 0/4 |
| `retention_attestation_accuracy` | 4/4 |
| `controlled_state_mutation_success` | 0/4 |

This is not a state-transition failure. The transition passed in every run,
but the complete contract did not.

## Execution Integrity

| Check | Result |
|---|---:|
| Planned calls | 4 |
| Completed calls | 4 |
| Provider errors | 0 |
| Retries | 0 |
| Invalid JSON | 0 |
| Prompt tokens | 8,320 |
| Completion tokens | 2,178 |
| Total tokens | 10,498 |
| Reasoning tokens | 0 |
| Completion-token range | 538-548 / 2,000 |
| Latency range | 21.422-26.500 seconds |
| Median latency | 21.938 seconds |

All calls used `Qwen/Qwen3-8B`, temperature zero, disabled thinking, and the
frozen G9 packets.

## Raw-Output Audit

All four raw outputs were inspected.

Every output correctly:

- moved the fixture-specific API-permission state from unknown to approved;
- preserved `ev-09` on the known-state item and transition record;
- retained branch and CI as the only unknown states;
- retained the matching two forbidden-inference labels;
- used the declared evidence field;
- emitted valid JSON with the required hierarchy;
- preserved the exact retention attestation.

Every output changed at least one grounded-claim evidence array.

Only 9/16 slot arrays were exact. `claim_gamma` omitted `ev-11` in all four
runs, and `claim_delta` retained its required `ev-09` array in only one run.

## Gate Attribution

The strict gate metric failed 0/4, but all four outputs preserved every gate
field except `next_action`.

The exact expected `next_action` was present in the evaluator but absent from
the model-visible required postconditions. This is a protocol fairness defect.
The strict score is retained, but it must not be interpreted as evidence that
the model failed to open the event-backed gate.

## Interpretation

The experiment gives a mixed but useful answer.

Positive:

> Qwen3-8B performed the controlled event-backed state transition in all four
> runs, including the paraphrased state vocabulary.

Negative:

> The model did not retain the exact grounded slot-to-evidence bindings while
> performing that transition.

Protocol issue:

> The gate evaluator required one exact field value that the visible contract
> did not fully specify.

The overall stage remains failed. Posthoc component analysis cannot replace
the preregistered aggregate decision.

## Claim Boundary

Supported:

> Under G9, Qwen3-8B applied the supplied unknown-to-approved transition in
> 4/4 runs while preserving residual unknown-state vocabulary and the
> retention attestation.

Supported:

> The combined transition-and-retention contract failed 0/4 because exact
> grounded evidence arrays were not preserved.

Not supported:

> Qwen3-8B passed the Stage B v5 state-transition macro.

Not supported:

> The strict gate failure demonstrates a model capability limit.

Not supported:

> The harness supports general state machines or workflow execution.

## Next Decision

Do not repeat the same smoke.

Proceed to Stage B v5.1-local:

1. expose the complete expected gate object;
2. remove editable claim prose from the mutation test, or separate it from the
   immutable slot-to-reference payload;
3. add gate-next-action and evidence-remapping known-bads;
4. pass local and historical regression gates;
5. seek separate approval for a repair smoke.
