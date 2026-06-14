# Stage B v5 State-Transition Smoke Failure Audit

Audited: 2026-06-14

Strict protocol decision: fail

## Component Result

| Component | Passing runs |
|---|---:|
| Schema | 4/4 |
| Exact grounded evidence arrays | 0/4 |
| Residual unknown-state vocabulary | 4/4 |
| State transition | 4/4 |
| Strict transition gate | 0/4 |
| Retention attestation | 4/4 |
| Aggregate | 0/4 |

All four outputs were complete parseable semantic attempts. No retry was
permitted or performed.

## Evidence Binding Failure

The model-visible `grounded_claim_contract` declared the required slot IDs and
reference arrays. Even so, every run changed at least one array.

Across 16 slot instances:

- 9 arrays were exact;
- 7 arrays were not exact;
- exact slot-array retention was 56.25%.

The pattern was systematic:

- `claim_alpha` passed 4/4;
- `claim_beta` passed 4/4;
- `claim_gamma` passed 0/4 because every output omitted `ev-11`;
- `claim_delta` passed 1/4.

The model often rewrote editable claim prose and then selected evidence that
appeared semantically related to the rewritten sentence. This does not excuse
the failure: the slot-to-array mapping was explicitly declared as fixed.

It does reveal a design confound. The target mechanism was state mutation, but
editable prose introduced an unnecessary opportunity to re-ground claims.

## Gate Fairness Audit

Every run produced the correct:

- `status=open`;
- `permitted_action=provider_execution`;
- fixture-specific `satisfied_prerequisite`;
- four ordered support slot IDs.

All four strict gate failures came from `next_action`.

The evaluator expected:

```text
run_targeted_state_transition_smoke
```

The outputs used `provider_execution` or `none`.

This strict mismatch cannot be attributed fairly to the model because the
model-visible `required_postconditions` declared the gate status and permitted
action but did not declare the exact `next_action` value. The input also
described opening provider execution, making `provider_execution` a plausible
completion.

The preregistered strict metric remains unchanged, so the stage still fails.
The fairness audit only limits attribution: gate failure is a protocol defect,
not evidence of model inability.

## State-Mutation Finding

The target transition itself passed 4/4:

- API permission moved from unknown to approved;
- event ID and evidence remained exact;
- branch and CI remained unknown;
- the corresponding API forbidden-inference label was removed;
- the retention attestation remained exact.

The correct conclusion is therefore:

> Qwen3-8B completed the controlled state transition in all four runs, but the
> combined contract failed because exact grounded evidence bindings were not
> retained. The strict gate score was additionally affected by an
> evaluator-to-contract mismatch.

## Repair Decision

Do not rerun the current protocol.

Prepare Stage B v5.1-local:

1. expose the complete exact `transition_gate`, including `next_action`;
2. freeze grounded claim objects, or separate immutable slot-to-reference
   bindings from editable prose;
3. add a `wrong_next_action` known-bad;
4. add known-bads that remap evidence based on rewritten claim prose;
5. rerun local, isolation, and historical regression gates;
6. request separate approval before any v5.1 provider smoke.
