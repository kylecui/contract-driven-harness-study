# Stage B v5.1 Controlled State-Transition Local Plan

Planned: 2026-06-14

Status: preregistered before fixture generation and local execution

Provider calls: 0

## Research Question

Can the Stage B v5 controlled-transition contract be repaired without weakening
its semantic obligations by:

1. exposing the complete expected transition gate to the model; and
2. separating immutable slot-to-reference bindings from editable claim prose?

This stage validates the repaired fixture, evaluator, and failure attribution
locally. It does not test a model.

## Prior Result and Repair Scope

Stage B v5 smoke failed 0/4 on the aggregate metric.

- Schema, residual state, transition, and attestation passed 4/4.
- Exact grounded evidence arrays passed 0/4.
- Strict gate accuracy passed 0/4.
- All gate mismatches were confined to `next_action`, whose exact expected
  value was absent from the model-visible postconditions.
- The model also remapped old evidence arrays while rewriting claim prose.

The v5 result remains a failed strict record. v5.1 is a new protocol and will
not replace or rescore it.

## Contract Repair

The repaired output contains an `evidence_bindings` section with exact,
immutable objects:

```text
{slot_id, <declared reference field>}
```

Claim prose remains available in the evidence bundle as context, but it is not
an editable output field. The repair therefore preserves the evidence-binding
obligation without asking the model to rewrite the text to which the arrays
were previously attached.

The model-visible `OutputContract` also contains the complete expected
`transition_gate`, including:

- `status`;
- `permitted_action`;
- `satisfied_prerequisite`;
- `next_action`;
- `support_slot_ids`.

No evaluator-only gate value may remain.

## Variants

| Fixture | Reference field | State vocabulary |
|---|---|---|
| Canonical | `evidence_ids` | canonical |
| Dual-surface stress | `source_references` | paraphrased `do_not_guess_*` |

Both variants apply the same event and require the same four bindings in the
same order.

## Hypotheses

H1-golden: both golden outputs pass every component metric at `1.000`.

H2-known-bad: every known-bad output fails
`controlled_state_mutation_success`.

H3-diagnostic: evidence-binding, residual-state, transition, gate, and
attestation corruptions produce their preregistered component vectors.

H4-remapping: the evidence-remapping pattern observed in v5 smoke fails the
evidence-binding component while leaving unrelated semantic components
unchanged.

H5-next-action: a wrong `next_action` remains schema-valid but fails strict
gate accuracy.

H6-static-ablation: a valid pre-transition copy fails the mutation components.

H7-isolation: the alternative evidence field and state vocabulary do not leak
into either model-visible fixture.

H8-regression: the unchanged v5, v4 atom, v4 recomposition, and v3 local
records remain unchanged.

## Variables

Independent variable:

- repaired representation of the same v5 obligations.

Dependent metrics:

- `schema_validity`;
- `exact_evidence_array_preservation`;
- `residual_unknown_vocabulary_accuracy`;
- `state_transition_accuracy`;
- `transition_gate_accuracy`;
- `retention_attestation_accuracy`;
- `controlled_state_mutation_success`.

Controlled variables:

- evidence slot IDs, arrays, and ordering;
- branch and CI unknown-state obligations;
- transition event, target, value, and support;
- gate action and support slots;
- representation variants;
- absence of tools and provider calls.

## Known-Bad Coverage

Each fixture must include:

- evidence substitution;
- evidence-array reordering;
- evidence-slot reordering;
- evidence-slot renaming;
- undeclared reference-field fallback;
- the v5-observed semantic evidence remapping;
- residual unknown-state reordering;
- residual forbidden-prefix substitution;
- transitioned target duplicated as unknown;
- wrong transition value;
- wrong transition evidence;
- omitted transition record;
- wrong gate `next_action`;
- stale blocked gate;
- incomplete gate support;
- static pre-transition copy;
- combined evidence and transition corruption;
- incomplete retention attestation.

Every known-bad must have an exact expected component-metric vector.

## Stop Rule

Stop and repair locally if:

- any golden output fails;
- any known-bad passes the aggregate metric;
- any known-bad produces an unexpected component vector;
- the complete expected gate is absent from a model-visible contract;
- editable claim prose remains in the output contract;
- any evaluator-only alternative leaks into a model-visible file;
- any historical local regression changes.

No provider smoke is admissible until all local gates pass.

## Validity Threats

Internal validity:

- v5.1 changes two contract defects together. Targeted known-bads isolate the
  repaired evidence and gate components, but a later model smoke cannot
  estimate their separate causal effects without an ablation.

Construct validity:

- exact bindings measure contract retention, not whether alternative evidence
  choices might also be semantically defensible.

External validity:

- one event, four bindings, and two representation variants do not represent
  arbitrary state machines or evidence graphs.

Conclusion validity:

- local success establishes fixture discrimination and contract fairness, not
  model capability.

## Claim Boundary

Passing supports only:

> The v5 evidence and gate obligations can be expressed as a fully
> model-visible, deterministic contract with local failure attribution.

It does not show that Qwen3-8B can satisfy the repaired contract. A separate
provider smoke would require explicit approval.
