# Stage B v5.3 Pre-Execution Audit

Date: 2026-06-14

## Protocol

- P1: exact initial state and exact required postconditions.
- P2: the same contract plus `required_transition_delta`.
- Five perturbation conditions.
- Three repetitions per profile-condition cell.
- 30 planned Qwen/Qwen3-8B + G9 calls.
- Temperature 0, thinking disabled, 2,000-token output limit.

## Fairness Audit

For each paired condition, P1 and P2 have identical:

- golden output;
- evidence bindings;
- initial state;
- transition event;
- required postconditions;
- transition gate;
- retention attestation;
- output schema;
- evaluator;
- perturbation.

P2 adds only the structured transition-delta control and the instruction to
execute that control. Model-visible profiles are neutral P1 and P2. Internal
arm labels do not appear in prompts.

## Local Gates

- Fixtures: 10
- Golden outputs passed: 10/10
- Known-bad outputs rejected: 100/100
- Local component expectations: 110/110
- Evaluator unit tests: 6/6
- Model-surface violations: 0
- Paired-protocol violations: 0
- Stage B v5.2 regression cases: 100/100
- Stage B v5.1 regression cases: 38/38

The local suite rejects the observed v5.2 failure in which the transitioned
state remains in `forbidden_inferences`.

## Prompt Audit

- Exported prompts: 30
- P1 prompts containing exact postconditions: 15/15
- P1 prompts containing transition delta: 0/15
- P2 prompts containing exact postconditions: 15/15
- P2 prompts containing transition delta: 15/15
- Prompts containing complete transition gate: 30/30
- Prompts exposing golden output: 0/30
- Prompts exposing evaluation spec: 0/30
- Prompts exposing internal arm labels: 0/30
- Prompt length range: 7,444 to 8,531 characters

## Execution Readiness

- Packet compilation: 30/30
- Adapter dry-run: 30/30
- Key-required preflight: PASS
- Preflight errors: 0
- Preflight warnings: 0
- Provider calls made during preparation: 0

Provider execution may proceed under the frozen retry rule. Complete semantic
failures are not eligible for retry.
