# Stage B v4 Targeted Smoke Plan

Planned: 2026-06-14

Status: preregistered before provider execution

## Objective

Test whether the low-cost model can satisfy the two exact-retention mechanisms
that Stage B v3 failed after those mechanisms were isolated in Stage B
v4-local.

This is a mechanism debugging smoke, not a robustness estimate.

## Hypotheses

H1-B4A: Qwen3-8B under G9 preserves every declared evidence-reference array
exactly in both the canonical-field and declared-field-alias fixtures.

H2-B4B: Qwen3-8B under G9 preserves every declared closed-vocabulary array
exactly in both the canonical and paraphrased fixtures.

The smoke passes only if every fixture passes both repetitions.

## Run Matrix

| Variable | Frozen value |
|---|---|
| Model | `Qwen/Qwen3-8B` |
| Model tier | `budget_model` |
| Harness | G9 |
| Temperature | 0 |
| Thinking | disabled |
| Maximum output tokens | 2000 |
| Fixtures | four Stage B v4 atoms |
| Repetitions | two per fixture |
| Planned calls | eight |

The four fixtures are:

- `b4a-evidence-array-immutability--canonical`;
- `b4a-evidence-array-immutability--declared-field-alias`;
- `b4b-closed-vocabulary-retention--canonical`;
- `b4b-closed-vocabulary-retention--paraphrased`.

## Metrics

For B4A:

- `schema_validity`;
- `exact_evidence_array_preservation`;
- `atom_primary_metric`;
- `task_success`.

For B4B:

- `schema_validity`;
- `exact_closed_vocabulary_retention`;
- `atom_primary_metric`;
- `task_success`.

Exact equality includes value, order, and multiplicity. Prose quality is not
scored.

## Execution Rules

- Compile all eight prompts before execution.
- Run the v4-local gate again before provider execution.
- Run adapter dry-run and key-required preflight.
- Preserve incremental adapter events and provider usage metadata.
- Do not retry a complete, parseable semantic failure.
- Retry only a provider failure, timeout, or truncated invalid JSON.
- Retain every original attempt.
- Stop before macro recomposition if any fixture fails either repetition.

## Decision Rule

Pass:

- 8/8 provider calls complete or are validly recovered under the retry rule;
- 8/8 outputs parse;
- every run has `schema_validity=1.000`;
- every run has `atom_primary_metric=1.000`;
- every fixture passes 2/2 repetitions.

Fail:

- any fixture passes fewer than 2/2 repetitions after valid provider recovery;
- any complete output changes an immutable evidence array or closed-vocabulary
  value.

Runtime inconclusive:

- unrecovered provider or truncation failures prevent a complete 8-run record.

## Claim Boundary

Passing would support:

> Under G9, Qwen3-8B completed the four isolated exact-retention fixtures in
> two repetitions each.

Passing would not establish macro transfer, general perturbation robustness,
workflow readiness, or production reliability. The next required test would
be a bounded recomposition experiment.

## Validity Threats

- Two repetitions per fixture are sufficient for debugging but not a stable
  success-rate estimate.
- The output templates make copying possible. That is appropriate for the
  preservation mechanism but does not test open-ended reasoning.
- Provider behavior may vary despite temperature zero.
- Passing isolated atoms may not transfer to the attention load of the larger
  Stage B macros.

## Pooling Policy

These runs must not be pooled with Stage B v1, v2, or v3. They use different
tasks and answer a narrower mechanism question.
