# Stage B v4 Bounded Recomposition Local Result

Completed: 2026-06-14

Decision: local gate passed; targeted recomposition smoke is admissible

Provider calls: 0

## Result

B4A and B4B were composed into one bounded macro with a fixed local-first
`composition_gate`.

Two representation variants were tested:

| Fixture | Evidence field | State vocabulary | Golden |
|---|---|---|---:|
| Canonical | `evidence_ids` | canonical | Pass |
| Dual-surface stress | `source_references` | paraphrased `do_not_guess_*` | Pass |

The complete local record:

| Check | Result |
|---|---:|
| Recomposition fixtures | 2 |
| Golden outputs | 2/2 passed |
| Known-bad outputs | 20/20 rejected |
| Total expectations | 22/22 met |
| Evaluator unit tests | 5/5 passed |
| Model-surface isolation violations | 0 |
| Stage B v4 atom regression | 32/32 met |
| Stage B v3 macro regression | 110/110 met |
| Future smoke packets compiled | 4/4 |

## Composition Boundary

The macro contains only:

1. exact `state_inventory` vocabulary retention;
2. exact `grounded_claims` slot and evidence-array retention;
3. a fixed gate that blocks `provider_execution` until the local gate passes;
4. an attestation listing the immutable fields.

It does not restore evidence classification, unsupported-claim analysis, long
decision traces, method-plan generation, broad synthesis, or tool use.

This is intentional. The experiment adds one composition pressure while
keeping failure attribution possible.

## Diagnostic Evaluator

Every known-bad has a preregistered component-metric vector.

Examples:

| Failure | Schema | Evidence | Vocabulary | Gate | Composition |
|---|---:|---:|---:|---:|---:|
| Evidence substitution | 1 | 0 | 1 | 1 | 0 |
| Forbidden-prefix substitution | 1 | 1 | 0 | 1 | 0 |
| Premature gate opening | 1 | 1 | 1 | 0 | 0 |
| Dual-component corruption | 1 | 0 | 0 | 1 | 0 |
| Undeclared reference field | 0 | 0 | 1 | 1 | 0 |

All 20 known-bads produced their expected vectors. This matters because a
single aggregate failure score would not show whether the evaluator can
separate component failures after composition.

## Surface Isolation

The canonical fixture exposes neither `source_references` nor the paraphrased
state labels. The dual-stress fixture exposes neither `evidence_ids` nor the
canonical state labels.

The automated scan checked `input.md`, `task_spec.json`,
`memory_slice.json`, `evidence_bundle.json`, and `output_contract.json`.
It found zero forbidden-value leaks.

## Regression

The new scripts do not modify the historical evaluators.

- Stage B v4 isolated atoms still pass 32/32 local expectations.
- Stage B v3 macros still pass 110/110 local golden/known-bad expectations.

The four-run future smoke matrix also compiles into complete G9 packets:

- two fixtures;
- `budget_model`;
- two repetitions;
- four planned calls.

No provider execution occurred in this stage.

## Interpretation

The local infrastructure can now distinguish three questions:

1. Were the evidence arrays preserved?
2. Was the state vocabulary preserved?
3. Did the local-first gate remain correct?

That is sufficient to move from isolated atom testing to a bounded model
recomposition smoke without returning to the large Stage B v3 macro.

The local result does not show that Qwen3-8B passes the recomposed task.

## Claim Boundary

Supported:

> B4A and B4B have been composed into a bounded, deterministic macro with
> component-level failure attribution.

Not supported:

> Qwen3-8B retains both mechanisms under composition.

Not supported:

> The Stage B v3 macros are repaired or generally robust.

## Next Gate

Stage B v4-recomposition-smoke is admissible:

- model: `Qwen/Qwen3-8B`;
- harness: G9;
- fixtures: canonical and dual-surface stress;
- repetitions: two;
- planned calls: four.

Both fixtures must pass 2/2. A complete semantic failure is not retryable.
Provider errors or truncated invalid JSON may be recovered only under the
existing retry rule.
