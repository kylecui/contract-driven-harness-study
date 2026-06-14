# Stage B v5 Controlled State-Transition Smoke Plan

Planned: 2026-06-14

Status: preregistered before provider execution

Execution authorization: user explicitly approved this four-call smoke on
2026-06-14

## Objective

Test whether Qwen3-8B under G9 applies one supplied unknown-to-known API
permission transition while preserving exact grounded evidence arrays,
residual branch and CI unknown-state duties, the post-transition gate, and the
retention attestation.

This is a targeted mechanism-composition smoke, not a reliability estimate or
general state-machine test.

## Baselines

Positive static baseline:

- Qwen3-8B + G9 passed 4/4 Stage B v4 bounded recomposition runs.

Positive local mutation baseline:

- Stage B v5 local passed 30/30 expectations;
- its static-copy ablation was correctly rejected;
- historical regressions remained 32/32, 22/22, and 110/110.

Negative broad-macro baseline:

- Stage B v3 passed 18/30 runs and 6/10 cells.

## Hypotheses

H1-canonical: the canonical state-transition fixture passes both repetitions.

H2-dual-surface: the `source_references` and paraphrased-state fixture passes
both repetitions.

H3-mutation: every passing output moves only the API-permission state from
unknown to approved.

H4-retention: every passing output preserves all grounded reference arrays and
the two residual unknown-state obligations.

H5-gate: every passing output opens the fixture gate only after recording the
event-backed transition.

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
- `residual_unknown_vocabulary_accuracy`;
- `state_transition_accuracy`;
- `transition_gate_accuracy`;
- `retention_attestation_accuracy`;
- `controlled_state_mutation_success`;
- `task_success`.

A run passes only when every component metric equals `1.000`.

## Execution Rules

- Re-run the v5 local gate before provider execution.
- Compile all four full G9 packets and export all prompts.
- Verify the fixture event remains marked `fixture_only`.
- Check prompt surfaces for golden-output or evaluator-only leakage.
- Run adapter dry-run and key-required provider preflight.
- Preserve incremental events, raw outputs, provider usage, and retry lineage.
- Do not retry a complete, parseable semantic failure.
- Retry only a provider error, timeout, or truncated invalid JSON.
- Retain every original attempt.

## Decision Rule

Pass:

- four valid outputs are collected;
- both fixtures pass 2/2;
- every component metric equals `1.000` in every run.

Fail:

- either fixture passes fewer than 2/2 after valid provider recovery;
- any complete output fails to apply the transition;
- any complete output changes a required evidence array, residual state value,
  field name, gate field, or attestation field.

Runtime inconclusive:

- unrecovered provider or truncation failures prevent a complete four-run
  record.

## Claim Boundary

Passing would support:

> Under G9, Qwen3-8B applied one supplied evidence-backed unknown-to-known
> transition in two representation variants with two repetitions each.

Passing would not establish:

- general state-machine competence;
- tool authorization or actual tool execution;
- rollback, concurrency, or conflicting-event handling;
- stable success rates;
- full workflow or production readiness.

## Validity Threats

- Two repetitions per fixture are a debugging gate, not a statistical
  reliability estimate.
- The event and postconditions are explicit, so event discovery and planning
  remain untested.
- The gate is represented in JSON and does not itself invoke a tool.
- Temperature zero does not eliminate provider-side variability.

## Pooling Policy

These runs remain separate from every prior Stage B protocol because the task
and claim differ.
