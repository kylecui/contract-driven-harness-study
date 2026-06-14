# Stage B v4 Bounded Recomposition Local Plan

Planned: 2026-06-14

Status: preregistered before local execution

Provider calls: 0

## Research Question

Can the two Stage B v4 mechanisms retain their exact contracts when composed
into one bounded packet with a minimal local-first gate?

This stage tests fixture and evaluator readiness. It does not test a model.

## Baselines

Component baseline:

- B4A and B4B passed 32/32 local golden/known-bad expectations;
- Qwen3-8B + G9 passed 8/8 isolated atom smoke runs.

Negative macro baseline:

- Stage B v3 passed 18/30 runs and 6/10 cells;
- its exact-content failures included evidence-array changes and
  closed-vocabulary substitutions.

The recomposition gate sits between those baselines. It adds one composition
step without restoring the full Stage B v3 obligation set.

## Composition

The bounded macro contains:

1. B4B exact state-vocabulary retention;
2. B4A exact claim-slot and evidence-array retention;
3. one fixed `composition_gate` that keeps provider execution blocked until
   the local gate passes.

It does not add evidence typing, unsupported-claim analysis, long decision
traces, method-plan generation, broad synthesis, or tool use.

## Variants

| Fixture | Evidence field | State vocabulary |
|---|---|---|
| Canonical | `evidence_ids` | canonical |
| Dual-surface stress | `source_references` | paraphrased `do_not_guess_*` |

The dual-stress fixture changes both representation surfaces at once because
both component variants already passed independently.

## Hypotheses

H1-local: both golden outputs pass schema, B4A, B4B, gate, and composition
metrics at `1.000`.

H2-local: every known-bad output fails `composition_retention`.

H3-diagnostic: single-component known-bads fail only their intended component
metric while unrelated component metrics remain `1.000`.

H4-isolation: evaluator-only alternative field names and vocabularies do not
appear in model-visible files.

H5-regression: the unchanged Stage B v3 local suite remains at 110/110
expectations.

## Metrics

- `schema_validity`;
- `exact_evidence_array_preservation`;
- `exact_closed_vocabulary_retention`;
- `composition_gate_accuracy`;
- `composition_retention`;
- `task_success`.

`composition_retention=1.000` only when every component metric and schema
validity equal `1.000`.

## Known-Bad Coverage

Each fixture includes:

- evidence ID substitution;
- evidence-array reordering;
- undeclared reference-field fallback;
- forbidden-prefix substitution;
- alternate vocabulary fallback;
- state-array reordering;
- premature gate opening;
- incomplete gate support;
- dual-component corruption;
- flattened state inventory.

The evaluator stores expected per-component metric vectors for every known-bad
case.

## Stop Rule

Stop and repair locally if:

- any golden output fails;
- any known-bad passes composition;
- any known-bad produces an unexpected component-metric vector;
- any forbidden evaluator-only value leaks into a model-visible file;
- the Stage B v3 regression changes.

Only a clean local record admits Stage B v4-recomposition-smoke.

## Validity Threats

Internal validity:

- A broad known-bad could accidentally damage multiple components. Expected
  metric vectors make that visible.

Construct validity:

- The macro remains copy-oriented. This is appropriate for retention but does
  not measure open-ended reasoning.

External validity:

- Two small variants do not represent arbitrary schema perturbations.

Conclusion validity:

- Local fixtures show evaluator discrimination, not model success or transfer.

## Claim Boundary

Passing supports only:

> B4A and B4B have been composed into a bounded, deterministic local macro with
> diagnostic component metrics and known-bad coverage.

It does not establish that Qwen3-8B passes the recomposed task.
