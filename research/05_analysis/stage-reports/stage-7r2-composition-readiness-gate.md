# Stage 7r.2 Composition Readiness Gate

Date: 2026-06-08

## Purpose

Stage 7r.2 decides whether the mechanism-atom evidence is strong enough to restart composition, and if so, what kind of macro task is allowed.

This is a gate decision, not a new model run.

## Evidence Inputs

Primary inputs:

- Stage 7p v2: A10 -> A9 -> A6 composition-retention macro passed under G8/G9 for both model tiers.
- Stage 7r: revised A2/A3/A4/A5/A7/A8 real smoke, 35/36 completed, one A8R low-cost G8 provider timeout.
- Stage 7r.1: tightened A2R1/A7R1 targeted low-cost-model smoke, 8/8 completed and 8/8 passed.

Key reports:

- `research/05_analysis/stage-reports/stage-7p-v2-composition-retention-summary.md`
- `research/05_analysis/stage-reports/stage-7r-revised-atoms-summary.md`
- `research/05_analysis/stage-reports/stage-7r1-a2r-a7r-targeted-smoke-summary.md`

## Composition Admission Table

| Mechanism | Admitted version | Evidence status | Gate decision | Notes |
|---|---|---|---|---|
| Bounded context recall | A10 from Stage 6d/7p v2 | Passed in partial macro v2 under G8/G9 | Admit | Use only with explicit `carried_obligations` and `excluded_context`. |
| No-overwrite action planning | A9 from Stage 6d/7p v2 | Passed in partial macro v2 under G8/G9 | Admit | Safe action boundaries are composition-safe when protected files are explicit. |
| Validator repair | A6 from Stage 6c/7p v2 | Passed in partial macro v2 under G8/G9 | Admit | Use when downstream output can be validator-checked. |
| Constraint-safe plan | A3R | Stage 7r G8/G9 passed for both model tiers | Admit | Good candidate for project-init-like macro steps. |
| Strict state inventory | A4R | Stage 7r G8/G9 passed for both model tiers | Admit | Requires fixed snapshot and unknown-state contract. |
| Stage-gate check | A5R | Stage 7r G8/G9 passed for both model tiers | Admit | Good candidate for research workflow gating. |
| Claim-level evidence binding | A2R1 | Stage 7r.1 low-cost G8/G9 passed 4/4 | Admit | Replaces A2R for composition. A2R original remains not admitted for low-cost composition. |
| Rejection trace completeness | A7R1 | Stage 7r.1 low-cost G8/G9 passed 4/4 | Admit | Replaces A7R for composition. A7R original remains not admitted for low-cost composition. |
| Evidence-type rules | A8R | Stage 7r strong G8/G9 passed; low-cost G9 passed; low-cost G8 pending due provider timeout | Conditional admit | Allowed in a narrow macro if not used as the sole decisive mechanism, and if the macro evaluator distinguishes model failure from provider timeout. |

## What Remains Blocked

Full open-ended project initialization remains blocked.

Reason:

- Project initialization would require A3R/A4R/A9/A10 plus filesystem-side action execution and cross-step state mutation. We have atom and one partial macro evidence, but not enough evidence that a broad project-init workflow remains stable across multiple mutable steps.

Full open-ended research workflow remains blocked.

Reason:

- Research workflow would require source discovery, evidence extraction, evidence typing, claim grounding, synthesis, decision trace, and stage gating. We now have stronger atom evidence for several mechanisms, but not yet a composed evidence-bound research macro.

The next macro must therefore be narrow, fixed-input, no-tool-execution, and evaluator-deterministic.

## Next Allowed Macro

Recommended next macro: **Stage 7e evidence-bound decision packet**.

Composition chain:

1. A4R strict state inventory
2. A2R1 claim-level evidence binding
3. A8R evidence-type rules
4. A7R1 rejection trace completeness
5. A5R stage-gate check

Purpose:

Test whether individually passing evidence/state/decision/gate mechanisms compose into one coherent research-decision packet.

Why this macro:

- It directly targets the research-workflow failure class without opening the full research workflow.
- It uses the newly repaired A2R1/A7R1 mechanisms.
- It avoids filesystem mutation and external tool execution.
- It produces a deterministic JSON artifact that can be evaluated with explicit contract checks.

## Proposed Macro Contract

Input:

- fixed workspace snapshot,
- fixed evidence bundle,
- candidate contribution claims,
- evidence type rules,
- stage status,
- stale context to exclude.

Required output sections:

- `state_inventory`
- `grounded_claims`
- `unsupported_claims`
- `typed_evidence`
- `selected_claim`
- `rejected_options`
- `decision_trace`
- `stage_gate`
- `carried_obligations`

Critical obligations:

- Preserve unknown state instead of inferring it.
- Bind every grounded claim to claim-level evidence IDs.
- Classify evidence into EXTRACTED / INFERRED / AMBIGUOUS / PROPOSED.
- Select only the supported contribution claim.
- Reject overbroad or unmeasured claims with evidence-linked trace.
- Block final recommendation if stage gate prerequisites are incomplete.
- Carry forward negative obligations, including stale context exclusion and no unsupported production-readiness claim.

Recommended model slice:

- models: `strong_model`, `budget_model`
- arms: G0, G8, G9
- repetitions: 1 first smoke
- total: 6 runs

Escalation rule:

- If the low-cost model passes G8/G9 and G0 fails, expand to 12 runs with repetition=2.
- If G8/G9 fail because of missing carried obligations, add a composition-retention field before rerunning.
- If provider timeout occurs, use event logs and single-run retry before interpreting model quality.

## Gate Decision

Stage 7r.2 allows a **narrow evidence-bound decision macro**.

It does not allow full project initialization or full research workflow composition yet.

Accepted next step:

- Build Stage 7e macro fixture and local evaluator.
- Run local golden/bad checks.
- Only after local gates pass, run a 6-run SiliconFlow smoke.

Claim boundary:

- If Stage 7e passes, we may claim that mechanism-bound evidence decision workflows can be composed under the harness.
- We still may not claim that arbitrary research workflows or project initialization workflows are solved.
