# Stage B v4 Bounded Recomposition Smoke Plan

Planned: 2026-06-14

Status: preregistered before provider execution

## Objective

Test whether Qwen3-8B under G9 preserves B4A evidence arrays, B4B state
vocabularies, and the fixed local-first gate when those mechanisms appear in
one bounded packet.

This is the first model transfer test after the isolated atoms passed. It is
not a general robustness or production-reliability estimate.

## Baselines

Positive component baseline:

- the four isolated atom fixtures passed 8/8 Qwen3-8B + G9 smoke runs.

Negative macro baseline:

- Stage B v3 passed 18/30 runs and 6/10 cells;
- its failures included evidence-array changes and state-label substitutions.

The bounded recomposition lies between these baselines. It adds simultaneous
retention and one fixed gate without restoring the full Stage B v3 macro.

## Hypotheses

H1-canonical: the canonical recomposition fixture passes both repetitions.

H2-dual-surface: the declared `source_references` plus paraphrased
`do_not_guess_*` fixture passes both repetitions.

H3-components: every passing run has all four component metrics equal to
`1.000`.

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
- `exact_closed_vocabulary_retention`;
- `composition_gate_accuracy`;
- `composition_retention`;
- `task_success`.

A run passes only when schema, evidence, vocabulary, and gate metrics all equal
`1.000`.

## Execution Rules

- Re-run the recomposition local gate before provider execution.
- Compile all four packets and export all prompts before execution.
- Check prompt surfaces against evaluator-only alternatives.
- Run adapter dry-run and key-required provider preflight.
- Preserve incremental event logs and provider usage metadata.
- Do not retry a complete, parseable semantic failure.
- Retry only a provider failure, timeout, or truncated invalid JSON.
- Retain every original attempt.

## Decision Rule

Pass:

- four valid outputs are collected;
- both fixtures pass 2/2;
- every component metric equals `1.000` in every run.

Fail:

- either fixture passes fewer than 2/2 after valid provider recovery;
- any complete output changes an immutable array, vocabulary value, field name,
  gate field, or attestation field.

Runtime inconclusive:

- unrecovered provider or truncation failures prevent a complete four-run
  record.

## Claim Boundary

Passing would support:

> Under G9, Qwen3-8B retained the two exact-content mechanisms and fixed gate
> in two bounded recomposition variants with two repetitions each.

Passing would not establish:

- repair of the full Stage B v3 macros;
- general schema-perturbation robustness;
- stable success rates;
- workflow or production readiness.

## Validity Threats

- Two repetitions per fixture are a debugging gate, not a statistical
  reliability estimate.
- The packet remains copy-oriented, which is appropriate for retention but
  does not measure open-ended reasoning.
- The fixed gate adds limited composition pressure compared with Stage B v3.
- Temperature zero does not eliminate provider-side variability.

## Pooling Policy

These four runs must remain separate from Stage B v1, v2, v3, and the isolated
v4 atom smoke because the task and claim differ.
