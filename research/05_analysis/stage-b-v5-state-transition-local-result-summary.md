# Stage B v5 Controlled State-Transition Local Result

Completed: 2026-06-14

Decision: local gate passed; targeted state-transition smoke preparation is
admissible

Provider calls: 0

## Result

Stage B v5 adds one deterministic mutation to the passed bounded
recomposition:

> explicit event evidence moves API permission from unknown to approved, while
> Git branch and CI status remain unknown and the gate changes from blocked to
> open.

The complete local record:

| Check | Result |
|---|---:|
| Transition fixtures | 2 |
| Golden outputs | 2/2 passed |
| Known-bad outputs | 28/28 rejected |
| Total local expectations | 30/30 met |
| Evaluator unit tests | 7/7 passed |
| Model-surface isolation violations | 0 |
| Stage B v4 atom regression | 32/32 met |
| Stage B v4 recomposition regression | 22/22 met |
| Stage B v3 macro regression | 110/110 met |

## Transition Boundary

Both fixtures begin with three unknown states:

- Git branch;
- CI status;
- permission to use the external model API.

The supplied `event-api-approval-001`, supported by `ev-09`, changes only API
permission to `approved`.

The event has `fixture_only` scope. It represents a controlled state-machine
input and does not authorize a real provider call.

The golden post-transition state:

- contains one evidence-linked known-state item for API permission;
- retains only branch and CI in `unknown_state`;
- retains only the matching branch and CI forbidden-inference labels;
- preserves all four grounded-claim slots and reference arrays;
- records `unknown -> approved`;
- opens `provider_execution`;
- attests the preserved fields.

The canonical fixture uses `evidence_ids`. The dual-surface fixture uses
`source_references` and the paraphrased `do_not_guess_*` vocabulary.

## Diagnostic Evaluator

The evaluator reports six component checks before the aggregate result:

1. schema validity;
2. exact grounded evidence arrays;
3. residual unknown-state vocabulary;
4. known-state and transition-record accuracy;
5. post-transition gate accuracy;
6. retention-attestation accuracy.

All 28 known-bads produced their preregistered component vectors.

Twenty-four known-bads remained schema-valid but failed at least one semantic
component. This separates field-shape errors from incorrect state mutation.

## Static-Copy Ablation

`static_pretransition_copy` preserves valid JSON and all grounded evidence
arrays but ignores the event.

For both fixtures it received:

- `schema_validity=1.000`;
- `exact_evidence_array_preservation=1.000`;
- `residual_unknown_vocabulary_accuracy=0.000`;
- `state_transition_accuracy=0.000`;
- `transition_gate_accuracy=0.000`;
- `controlled_state_mutation_success=0.000`.

The evaluator therefore does not reward a valid copy of the initial state.

## Model-Surface Contract

The model-visible `OutputContract` declares:

- the complete nested output shape;
- four grounded-claim slots and their exact reference arrays;
- the initial state;
- the transition event;
- required postconditions;
- gate support slots;
- the retention attestation.

It does not expose `golden_output.json`. The final object must be assembled
from the initial state and transition rule.

The isolation scan found no alternate evidence field or alternate state
vocabulary in either model-visible surface.

## Regression

The new builder and evaluator are separate from all historical evaluators.

- Stage B v4 atoms remain 32/32.
- Stage B v4 bounded recomposition remains 22/22.
- Stage B v3 macros remain 110/110.

No historical scoring behavior changed.

## Deviation Review

An initial model-surface audit found that the first generated
`OutputContract` declared top-level sections and postconditions but omitted
the full nested shape and grounded-claim slot contract.

Execution stopped before historical regression. The contract was expanded to
declare those structures without exposing the golden output, then the
fixtures, 30 local cases, and seven unit tests were rerun. The research
question, hypotheses, transition semantics, evaluator, and decision rule did
not change.

This was an implementation correction, not a post-result hypothesis change.

## Interpretation

The local infrastructure now distinguishes static retention from controlled
mutation. A candidate can preserve all old evidence arrays and still fail if
it leaves the target unknown, writes the wrong post-state, cites the wrong
event, or leaves the gate stale.

This establishes fixture and evaluator readiness only. It does not show that
Qwen3-8B can perform the transition.

## Claim Boundary

Supported:

> One deterministic unknown-to-known transition is represented by two
> model-visible contracts with component-level failure attribution and a
> static-copy ablation.

Not supported:

> Qwen3-8B performs the transition correctly.

Not supported:

> The harness supports general state machines, tool execution, rollback, or
> concurrent workflow updates.

## Next Gate

Stage B v5-state-transition-smoke may now be prepared:

- model: `Qwen/Qwen3-8B`;
- harness: G9;
- fixtures: canonical and dual-surface stress;
- repetitions: two per fixture;
- planned provider calls: four.

Both fixtures must pass 2/2. Complete semantic failures are not retryable.
Provider failures or truncated invalid JSON may be retried only under the
existing declared rule. Actual execution still requires separate user
approval; the fixture event is not execution authorization.
