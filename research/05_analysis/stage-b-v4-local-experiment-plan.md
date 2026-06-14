# Stage B v4 Local Mechanism-Isolation Plan

Planned: 2026-06-14

Status: preregistered before local execution

Provider calls: 0

## Motivation

Stage B v3 preserved JSON hierarchy but failed two exact-content obligations:

1. nine runs rewrote frozen evidence-reference arrays;
2. six paraphrase runs rewrote declared `do_not_guess_*` labels as
   undeclared `do_not_infer_*` labels.

The v3 macro combined hierarchy, evidence binding, state retention, decision
trace, stage gates, and method-plan updates. Stage B v4-local removes those
other demands and tests the two failed mechanisms independently.

## Research Questions

RQ-B4A: Can exact evidence-array immutability be represented as a single
mechanism atom with a deterministic exact-equality evaluator?

RQ-B4B: Can exact closed-vocabulary retention be represented as a single
mechanism atom with a deterministic exact-equality evaluator?

This stage does not ask whether a model passes either atom. It asks whether the
fixtures and evaluators can distinguish valid preservation from the failures
observed in Stage B v3.

## Experimental Units

Four fixed fixtures are used:

| Atom | Variant | Isolated variable |
|---|---|---|
| B4A | canonical `evidence_ids` | Exact per-slot array preservation |
| B4A | declared `source_references` alias | Same mechanism under a declared field rename |
| B4B | canonical labels | Exact closed-vocabulary retention |
| B4B | paraphrased labels | Exact retention of the Stage B v3 stress vocabulary |

Each fixture has one golden output and known-bad outputs covering substitution,
reordering, omission, addition, duplication or mixed vocabularies as
applicable.

## Variables

Independent variables:

- mechanism atom: B4A or B4B;
- declared representation variant: canonical or renamed/paraphrased.

Dependent variables:

- `schema_validity`;
- `exact_evidence_array_preservation`;
- `exact_closed_vocabulary_retention`;
- `atom_primary_metric`;
- local expectation agreement.

Controlled variables:

- fixed input snapshot;
- deterministic JSON fixtures;
- no provider call;
- no sampling parameter;
- no tool execution;
- exact list equality including value, order, and multiplicity.

## Hypotheses

H1-local: every golden output receives `schema_validity=1.000` and its atom
primary metric equals `1.000`.

H2-local: every known-bad output receives atom primary metric `0.000`, including
known-bads that remain schema-valid.

H3-local: evaluator-only alternate field names and value vocabularies do not
appear in model-visible fixture files.

H4-regression: the existing Stage B v3 local perturbation gate remains
unchanged and passing after the v4 evaluator is added.

## Admission Rule

Stage B v4-smoke is admissible only if all four hypotheses pass. A failure in
any hypothesis stops the stage. The fixture or evaluator must be repaired and
the local record rerun before any model API execution.

Passing v4-local supports only this claim:

> The two Stage B v3 failure mechanisms have been isolated into deterministic,
> regression-testable atoms.

It does not support model reliability, perturbation robustness, workflow
readiness, or a paper result.

## Validity Threats

- Exact equality may overstate the operational importance of token order.
  Order is intentionally included because v4 tests immutability, not semantic
  equivalence.
- Synthetic atom inputs are smaller than the original macros. A later targeted
  smoke and recomposition test are required to evaluate transfer.
- Known-bad coverage cannot prove evaluator completeness. It can only show that
  the declared failure classes are detected.
- A model may pass by copying the template without understanding it. That is
  acceptable for this mechanism, whose contract is preservation rather than
  open-ended reasoning.

## Planned Commands

```powershell
python research/04_methods/scripts/build_stage_b_v4_local_atoms.py `
  --output-dir research/04_methods/mechanism-atoms-stage-b-v4

python research/04_methods/scripts/validate_mechanism_atoms.py `
  --atoms-dir research/04_methods/mechanism-atoms-stage-b-v4

python research/04_methods/scripts/test_evaluate_stage_b_v4_atoms.py

python research/04_methods/scripts/evaluate_stage_b_v4_atoms.py `
  --atoms-dir research/04_methods/mechanism-atoms-stage-b-v4 `
  --local-check `
  --output-runs research/05_analysis/stage-b-v4-local-check.json `
  --output-md research/05_analysis/stage-b-v4-local-check.md
```
