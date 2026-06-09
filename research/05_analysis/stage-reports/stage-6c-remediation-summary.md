# Stage 6c Summary: Composition-Critical Atom Remediation

## Stage Objective

Separate evaluator/fixture construct-validity problems from actual model failures in the Stage 6b composition-critical atom pilot, then rerun only the affected model-backed atoms that required new prompts.

## Result

Stage 6c remediation completed, but Stage 7 macro-workflow composition remains blocked.

Operational result:

- Local evaluator syntax check: PASS.
- Local golden/bad regression for A5, A6, A7, A9, and A10: PASS.
- Stage 6b recomputation after evaluator fixes: 42/42 completed runs, 0 warnings.
- A6 revised-fixture rerun: 6/6 completed runs, 0 warnings.
- Final Stage 6c view: 42 runs, replacing old under-specified A6 runs with revised A6 reruns.

## Corrections Made

### A5 Stage-Gated Synthesis

Issue:

- Outputs used `completed` where the evaluator expected `complete`.

Judgment:

- Evaluator brittleness. Typo/wording normalization should not be counted as model failure unless typo correction is the task.

Correction:

- `stage_status` now accepts both `complete` and `completed`.

### A6 Validator Repair

Issue:

- The fixture asked the model to keep existing valid fields unchanged, but the input did not explicitly provide those fields.
- The evaluator also over-weighted exact `repair_trace` wording.

Judgment:

- Fixture under-specification plus overly literal repair-success scoring.

Correction:

- A6 input now provides the original output: `{"title":"Contract-Driven Harness"}`.
- A6 `repair_success` now checks semantic repair success: title preserved, `atom-a6-e01` added, repair trace explains the evidence-id addition, and warnings are clear.
- A6 was rerun under `strong_model` and `budget_model` for G0/G8/G9.

### A7 Traceable Decision

Issue:

- Strong model G9 returned a valid decision and a textual trace, while the evaluator expected a list trace.
- Budget model G9 selected `budget_model`, which is not one of the task options.

Judgment:

- Strong model trace-string failure was evaluator/contract ambiguity.
- Budget model decision failure is retained as a real semantic failure.

Correction:

- Textual traces with enough step content are accepted.
- Decision scoring now normalizes minor formatting but still requires the correct bounded decision: `weak-model enablement`.

### A9 No-Overwrite Action Plan

Issue:

- Outputs blocked `AGENTS.md`; the evaluator expected `overwrite AGENTS.md` or `protected files`.

Judgment:

- Evaluator brittleness. Blocking `AGENTS.md` is semantically correct for the no-overwrite constraint.

Correction:

- Constraint consistency accepts `AGENTS.md` as a valid blocked target.

### A10 Bounded Context Recall

Issue:

- Outputs excluded the stale broad-workflow plan with wording different from the evaluator's expected phrase.

Judgment:

- Evaluator brittleness.

Correction:

- Context relevance accepts broader stale-plan exclusion phrasings involving `old plan` and `broad workflow`.

## A6 Rerun Outcome

After fixture clarification and semantic repair-success scoring:

- G0: both models remain at `repair_success=0`.
- G8: both models reach `repair_success=1`.
- G9: both models reach `repair_success=1`.

This supports the weak-model enablement claim for the validator-repair mechanism: the budget model failed without harness structure and succeeded with G8/G9 harness structure.

## Final Stage 6c Aggregate Results

Final 42-run view:

- A2/A4/A5/A7/A9/A10: Stage 6b outputs recomputed under the corrected evaluator.
- A6: Stage 6c revised-fixture reruns.

Key aggregate metrics:

- G8 task_success weak lift: +0.524.
- G9 task_success weak lift: +0.542.
- G8 schema_validity weak lift: +0.833.
- G9 schema_validity weak lift: +0.833.
- G8 atom_primary_metric weak lift: +0.429.
- G9 atom_primary_metric weak lift: +0.571.
- G8 task_success compression: 0.890.
- G9 task_success compression: 0.435.
- G8 atom_primary_metric compression: 0.812.
- G9 atom_primary_metric compression: 0.875.

Harnessed weak vs unconstrained strong G0 remains positive:

- G8 task_success weak-vs-strong-G0: +0.661.
- G9 task_success weak-vs-strong-G0: +0.679.
- G8 atom_primary_metric weak-vs-strong-G0: +0.714.
- G9 atom_primary_metric weak-vs-strong-G0: +0.857.

## Remaining Gate Blockers

Stage 7 is still not allowed under the strict roadmap.

Reasons:

- A10 Bounded Context Recall still has `atom_primary_metric=0` across G8/G9 for both model tiers after evaluator wording remediation.
- A7 Traceable Decision still fails for `budget_model` under G8/G9 because the decision is semantically wrong or incomplete.
- A2 and A5 show improved contract structure but still do not consistently meet full pass criteria.

## Deviation Judgment

The Stage 6c result is mixed but useful.

Positive:

- The earlier A5/A6/A7/A9/A10 construct-validity problems were separated from model behavior.
- A6 now gives clean weak-model enablement evidence.
- Aggregate weak-model enablement and atom-primary compression improved after remediation.

Negative:

- The composition-critical atom set is still not fully passing.
- The remaining failures are no longer mostly typo/evaluator issues; at least A7 budget-model decision and A10 bounded-context recall appear to be real mechanism weaknesses or under-designed atom contracts.

## Decision

Stage 6c is complete as a remediation stage.

Do not proceed to full Stage 7 macro-workflow composition yet.

Recommended next step:

1. Add a Stage 6d gate focused on remaining true blockers: A7 and A10 first, then A2/A5 full-pass thresholds.
2. Decide whether to revise atom contracts or accept these atoms as non-passing boundaries.
3. Compose only passing atom subsets if we need an interim macro demonstration, but label it as partial composition rather than full project-initialization or research-workflow validation.

## Artifacts

- Local regression: `research/05_analysis/mechanism-atoms-stage6c-local-check.md`
- Stage 6b recomputation: `research/05_analysis/mechanism-atoms-stage6c-recomputed-postprocess-metrics.md`
- A6 rerun manifest: `research/05_analysis/real-run-artifacts/mechanism-atoms-stage6c-a6-rerun-manifest-with-prompts.json`
- A6 rerun metrics: `research/05_analysis/mechanism-atoms-stage6c-a6-rerun-postprocess-metrics.md`
- Final merged run view: `research/05_analysis/mechanism-atoms-stage6c-final-evaluated-runs.json`
- Final metrics: `research/05_analysis/mechanism-atoms-stage6c-final-metrics.md`
