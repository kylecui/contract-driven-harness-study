# Stage B v5.2 Pre-Execution Audit

Date: 2026-06-14

## Scope

This audit covers the frozen 30-run evidence-binding ablation before any
provider call:

- 2 representation profiles: R1 and R2;
- 5 perturbation conditions;
- 3 repetitions per profile-condition cell;
- Qwen/Qwen3-8B with G9 on SiliconFlow;
- temperature 0, thinking disabled, and a 2,000-token output limit.

The semantic profile names remain available to the evaluator and analysis
scripts. The model-visible packets identify them only as R1 and R2.

## Local Gates

- Generated fixtures: 10
- Generated planned runs: 30
- Evaluator unit tests: 6/6 passed
- Local golden and known-bad cases: 100
- Local expectation failures: 0
- Model-surface isolation violations: 0
- Paired-gate violations: 0
- Stage B v5.1 regression cases: 38
- Stage B v5.1 regression failures: 0

## Prompt Audit

All 30 exported prompts were inspected mechanically and representative R1/R2
prompts were inspected directly.

- R1 runs: 15
- R2 runs: 15
- Runs per condition and profile: 3
- Prompts containing the complete required transition gate: 30/30
- Prompts containing the required next action: 30/30
- Prompts exposing `golden_output`: 0/30
- Prompts exposing `evaluation_spec`: 0/30
- Prompts exposing semantic arm labels: 0/30
- Prompt length range: 7,432 to 8,241 characters

The paired profiles share the same event, initial state, residual-state
requirements, reference arrays, and transition gate. Their intended difference
is the evidence representation: R1 couples immutable evidence arrays to editable
claim prose, while R2 separates the immutable bindings.

## Execution Readiness

- Packet compilation: 30/30, with 0 failures
- Adapter dry-run: 30/30 resolved to SiliconFlow and Qwen/Qwen3-8B
- Key-required preflight: PASS
- Preflight errors: 0
- Preflight warnings: 0
- Provider calls made during preparation: 0

The execution may proceed under the preregistered retry rule: retry only
provider errors, timeouts, or truncated invalid JSON. Semantic failures are not
eligible for retry.
