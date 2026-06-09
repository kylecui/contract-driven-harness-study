# Stage 6d Summary: Remaining Blockers and Partial Composition Gate

## Stage Objective

Resolve remaining Stage 6c composition blockers where they were still evaluator/contract artifacts, and decide whether to proceed to full Stage 7 or define a partial-composition gate.

## Result

Stage 6d completed.

Full Stage 7 macro-workflow composition is still not allowed.

A partial Stage 7 composition is allowed if it is explicitly limited to passing atoms:

- A6 Validator Repair.
- A9 No-Overwrite Action Plan.
- A10 Bounded Context Recall.

This partial composition can validate a narrow workflow pattern:

> bounded context selection -> no-overwrite safety planning -> validator repair.

It must not be described as full project-initialization or full research-workflow validation.

## Corrections Made

### A10 Bounded Context Recall

Stage 6c still mis-scored A10 because the evaluator searched the whole output for stale-context text. Correct outputs placed the stale broad-workflow plan in `excluded_context`, but the evaluator counted the phrase as if it had been used.

Correction:

- A10 now evaluates fields separately:
  - `answer` must select Stage 2.
  - `used_context` must point to current roadmap context.
  - `excluded_context` must contain the stale broad-workflow plan.
  - stale broad-workflow text in `excluded_context` is no longer treated as used context.

Result:

- A10 passes under G8/G9 for both model tiers.

### A7 Traceable Decision

Stage 6d accepts object-shaped traces when they contain steps or reasoning content. This fixes trace-format ambiguity.

Correction:

- `trace` can be a list, text string, or object with `steps` / reasoning fields.

Result:

- Trace completeness is no longer the blocker.
- Budget model still fails because it selects `budget_model` or a budget-model choice rather than the bounded option `weak-model enablement`.
- This remains a semantic decision failure.

### A5 Stage-Gated Synthesis

Stage 6d replaced overly literal golden-output matching with semantic task scoring:

- required stages complete,
- recommendation keeps tracks separate,
- evidence summary cites both supplied evidence IDs,
- risks are present.

Result:

- A5 improves, but remains mixed:
  - strong_model G9 passes,
  - budget_model G8 passes,
  - strong_model G8 and budget_model G9 remain below full pass criteria.

## Final Stage 6d Aggregate Results

Final 42-run view:

- Stage 6b outputs recomputed under Stage 6d evaluator corrections.
- A6 uses the revised-fixture rerun output from Stage 6c/6d.

Key metrics:

- G8 task_success weak lift: +0.702.
- G9 task_success weak lift: +0.661.
- G8 schema_validity weak lift: +0.833.
- G9 schema_validity weak lift: +0.833.
- G8 atom_primary_metric weak lift: +0.714.
- G9 atom_primary_metric weak lift: +0.714.
- G8 task_success compression: 0.619.
- G9 task_success compression: 0.191.
- G8 atom_primary_metric compression: 0.688.
- G9 atom_primary_metric compression: 0.875.

Harnessed weak vs unconstrained strong G0:

- G8 task_success: +0.827.
- G9 task_success: +0.786.
- G8 atom_primary_metric: +1.000.
- G9 atom_primary_metric: +1.000.

## Atom Gate Status

### Full-Pass Atoms

These pass for both model tiers under both G8 and G9:

- A6 Validator Repair.
- A9 No-Overwrite Action Plan.
- A10 Bounded Context Recall.

These atoms are eligible for partial composition.

### Boundary / Not-Yet-Passing Atoms

A2 Evidence Grounding:

- `citation_grounding=1.0`, but task_success remains below threshold.
- The model often cites supplied evidence but fails to explicitly mark `production readiness` as unsupported.
- Treat as a true evidence-discrimination boundary, not a pure evaluator issue.

A4 State Inventory:

- Budget model passes under G8/G9.
- Strong model reaches task_success 0.875 but atom_primary_metric 0.750, below the strict state inventory gate.
- Treat as useful evidence but not stable enough for all-model composition.

A5 Stage-Gated Synthesis:

- Mixed pass status after semantic scoring.
- Shows mechanism benefit, but not stable enough for full composition.

A7 Traceable Decision:

- Trace format is now handled.
- Budget model still chooses the wrong decision.
- Treat as a true semantic decision boundary.

## Gate Decision

Full Stage 7 composition: BLOCKED.

Partial Stage 7 composition: ALLOWED under a strict label:

> Stage 7p: partial composition of passing atoms A10 -> A9 -> A6.

This partial composition may support claims about:

- bounded context use,
- safe no-overwrite planning,
- validator-guided repair,
- weak-model enablement under contract-rich harnessing.

It may not support claims about:

- full project initialization,
- full evidence-backed research workflow,
- general traceable decision quality,
- general evidence-discrimination reliability.

## Next Step

Proceed to Stage 7p, not full Stage 7:

1. Compose A10, A9, and A6 into one small macro task.
2. Run local packet/evaluator gates first.
3. Run a small SiliconFlow slice only if the local macro task is deterministic and has a clear evaluator.
4. Keep A2/A4/A5/A7 as boundary cases for the paper's limitations and future work.

## Artifacts

- Local regression: `research/05_analysis/mechanism-atoms-stage6d-local-check.md`
- Final evaluated runs: `research/05_analysis/mechanism-atoms-stage6d-final-evaluated-runs.json`
- Final metrics: `research/05_analysis/mechanism-atoms-stage6d-final-metrics.md`
