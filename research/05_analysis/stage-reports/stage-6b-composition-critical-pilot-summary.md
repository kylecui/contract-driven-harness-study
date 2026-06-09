# Stage 6b Summary: Composition-Critical Atom Pilot

## Stage Objective

Run a composition-critical atom pilot for atoms required by project-initialization and research-workflow composition but not covered in the first Stage 6 pilot.

## Result

Stage 6b model execution completed, but Stage 7 remains blocked.

The run succeeded operationally:

- Planned runs: 42.
- Completed runs collected: 42/42.
- Collection warnings: 0.
- Metrics computed: yes.

However, the composition gate did not pass because several composition-critical atoms either did not pass or exposed evaluator/fixture construct-validity issues.

## Pilot Matrix

```text
2 models x 7 atoms x 3 arms x 1 repetition = 42 runs
```

Models:

- `strong_model`: `deepseek-ai/DeepSeek-V3.2`
- `budget_model`: `Qwen/Qwen3-8B`

Atoms:

- A2 Evidence Grounding.
- A4 State Inventory.
- A5 Stage-Gated Synthesis.
- A6 Validator Repair.
- A7 Traceable Decision.
- A9 No-Overwrite Action Plan.
- A10 Bounded Context Recall.

Arms:

- G0
- G8
- G9

## Main Aggregate Results

Weak-model enablement remains positive:

- G8 task_success weak lift: +0.583.
- G9 task_success weak lift: +0.566.
- G8 schema_validity weak lift: +0.833.
- G9 schema_validity weak lift: +0.833.
- G8 atom_primary_metric weak lift: +0.214.
- G9 atom_primary_metric weak lift: +0.357.

Harnessed weak vs unconstrained strong remains positive on broad contract metrics:

- G8 task_success weak-vs-strong-G0: +0.702.
- G9 task_success weak-vs-strong-G0: +0.685.
- G8 schema_validity weak-vs-strong-G0: +1.000.
- G9 schema_validity weak-vs-strong-G0: +1.000.

Gap compression is positive on general metrics:

- G8 task_success compression: 0.826.
- G9 task_success compression: 0.801.
- G8 schema_validity compression: 1.000.
- G9 schema_validity compression: 1.000.
- G8 safety_consistency compression: 1.000.
- G9 safety_consistency compression: 1.000.

Atom-primary compression is weaker:

- G8 atom_primary_metric compression: 0.125.
- G9 atom_primary_metric compression: 0.750.

## Composition Gate Findings

Full composition is not yet allowed.

Reason:

- A4 passed for `budget_model` under G8/G9, but not for `strong_model`.
- A9 passed for `strong_model` under G8/G9, but not for `budget_model` under current evaluator.
- A2, A5, A6, A7, and A10 did not meet full pass criteria under all required harness/model conditions.

This means the current atom library is not yet safe to compose into full macro workflows.

## Major Deviations

### D1: A9 evaluator appears too brittle

Observed output:

```json
{
  "blocked": ["AGENTS.md"]
}
```

The evaluator expected text closer to `overwrite AGENTS.md` or `protected files`. Since blocking `AGENTS.md` in a no-overwrite task is semantically correct, this is likely an evaluator construct-validity issue.

Status:

- Reasonable deviation.
- Requires evaluator correction and local known-bad regression before rerun.

### D2: A10 evaluator appears too brittle

Observed output correctly excluded:

```json
"old plan says run another broad workflow slice"
```

The evaluator looked for a narrower phrase, `old broad workflow slice plan`, so it under-scored context relevance.

Status:

- Reasonable deviation.
- Requires evaluator correction and local known-bad regression before rerun.

### D3: A6 fixture is under-specified

A6 asks the model to preserve existing valid fields, but the fixture input does not clearly provide the original valid fields. Some outputs repaired `evidence_ids` but did not reproduce the expected `title`.

Status:

- Fixture design issue.
- Requires fixture revision before rerun.

### D4: A5/A7 may include real model or fixture difficulty

A5 stage-gated synthesis and A7 traceable decision improved under harness arms but did not consistently pass full atom criteria.

Status:

- Possibly real model weakness, possibly overly strict fixture/evaluator.
- Requires targeted output review before deciding whether to revise evaluator, fixture, or expectation.

## Deviation Judgment

This is a major deviation from the optimistic expectation that all composition-critical atoms would pass after G8/G9.

It does not invalidate the core method.

It does require changing the execution plan before Stage 7:

1. Do not compose macro workflows yet.
2. Add a remediation stage before Stage 7.
3. Separate evaluator/fixture construct issues from actual model failures.
4. Rerun only the affected atoms after local regression checks pass.

## Decision

Stop before Stage 7.

Add Stage 6c:

> Remediate composition-critical atom evaluator/fixture issues, rerun local golden/bad checks, and rerun only affected model-backed atoms before macro workflow composition.

## Stage 6c Scope

Minimum affected atoms:

- A5 Stage-Gated Synthesis.
- A6 Validator Repair.
- A7 Traceable Decision.
- A9 No-Overwrite Action Plan.
- A10 Bounded Context Recall.

A2 and A4 may be retained as partial evidence but should be included in the readiness review after Stage 6c.

## Non-Claim Boundary

Do not claim yet:

- The full mechanism atom library is composition-ready.
- Project-initialization macro workflow can be composed.
- Research-workflow macro workflow can be composed.

Can claim now:

- Stage 6b completed 42/42 real model runs with 0 collection warnings.
- Harness arms improved weak-model broad contract metrics.
- Composition readiness is blocked by atom-specific failures and construct-validity issues that require remediation.
