# Stage B v5 Controlled State-Transition Local Plan

Planned: 2026-06-14

Status: preregistered before fixture generation and local execution

Provider calls: 0

## Research Question

Can the bounded Stage B v4 recomposition be extended with one deterministic
state transition while preserving its exact evidence and residual
unknown-state obligations?

This stage validates the fixture, evaluator, and failure attribution locally.
It does not test a model.

## Baselines

Positive static baseline:

- Stage B v4-recomposition-local passed 22/22 expectations;
- Qwen3-8B + G9 passed 4/4 bounded recomposition smoke runs.

Negative broad-macro baseline:

- Stage B v3 passed 18/30 runs and 6/10 cells;
- failures included evidence-array and state-vocabulary loss under a larger
  obligation set.

The new stage adds one state mutation to the passed static composition. It
does not restore the full Stage B v3 macro.

## Controlled Transition

Initial state:

- Git branch is unknown;
- CI status is unknown;
- permission to use the external model API is unknown;
- provider execution is blocked.

Supplied event:

- `event-api-approval-001` explicitly changes API permission from `unknown` to
  `approved`;
- the event is supported by `ev-09`.

Required post-transition state:

1. API permission appears once in `known_state` with value `approved` and
   support `ev-09`;
2. API permission is removed from `unknown_state`;
3. its matching forbidden-inference label is removed;
4. Git branch and CI status remain unknown in their declared order;
5. all grounded-claim slots and evidence arrays remain exact;
6. the transition record states `unknown -> approved`;
7. the gate changes from `blocked` to `open` and permits
   `provider_execution`.

## Variants

| Fixture | Evidence field | State vocabulary |
|---|---|---|
| Canonical | `evidence_ids` | canonical |
| Dual-surface stress | `source_references` | paraphrased `do_not_guess_*` |

Both variants apply the same semantic transition. Only the declared
representation surface changes.

## Hypotheses

H1-golden: both golden outputs pass every component metric at `1.000`.

H2-known-bad: every known-bad output fails
`controlled_state_mutation_success`.

H3-diagnostic: evidence, residual vocabulary, transition, and gate failures
are distinguishable through their preregistered component vectors.

H4-static-ablation: a valid pre-transition copy fails because it does not
apply the supplied event.

H5-isolation: evaluator-only alternative fields and vocabularies do not appear
in model-visible files.

H6-regression: the unchanged Stage B v4 atom, v4 recomposition, and Stage B v3
local records remain unchanged.

## Variables

Independent variable:

- presence of one explicit API-approval transition event.

Dependent metrics:

- `schema_validity`;
- `exact_evidence_array_preservation`;
- `residual_unknown_vocabulary_accuracy`;
- `state_transition_accuracy`;
- `transition_gate_accuracy`;
- `controlled_state_mutation_success`.

Controlled variables:

- grounded-claim slots and evidence arrays;
- branch and CI unknown-state obligations;
- output hierarchy;
- transition target and value;
- gate action;
- absence of tools and provider calls.

## Known-Bad Coverage

Each fixture includes:

- grounded evidence substitution;
- grounded evidence-array reordering;
- undeclared reference-field fallback;
- residual unknown-state reordering;
- residual forbidden-prefix substitution;
- transitioned target duplicated in unknown state;
- wrong transition value;
- wrong transition evidence;
- omitted transition record;
- stale blocked gate;
- incomplete gate support;
- static pre-transition copy;
- evidence plus transition corruption.

Every known-bad has an expected component-metric vector.

## Ablation

`static_pretransition_copy` is the explicit mutation ablation. It preserves a
valid representation of the initial state but ignores the event, retains the
API permission as unknown, and leaves the gate blocked.

Passing this known-bad would show that the evaluator measures static
reproduction rather than state mutation, so it is a blocking failure.

## Stop Rule

Stop and repair locally if:

- any golden output fails;
- any known-bad passes the aggregate metric;
- any known-bad produces an unexpected component vector;
- any evaluator-only alternative leaks into a model-visible file;
- any historical local regression changes.

No provider smoke is admissible until all local gates pass.

## Validity Threats

Internal validity:

- a known-bad can damage several components at once. Expected metric vectors
  make this visible.

Construct validity:

- this is a deterministic state update, not open-ended planning or tool use.

External validity:

- one approval transition and two representation variants do not represent
  arbitrary workflow state machines.

Conclusion validity:

- local success establishes evaluator discrimination and fixture readiness,
  not model success.

## Claim Boundary

Passing supports only:

> One deterministic unknown-to-known transition can be represented and
> evaluated locally while retaining the previously isolated evidence and
> residual unknown-state obligations.

It does not establish that Qwen3-8B performs the transition correctly.
