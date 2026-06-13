# Contract-Driven Harness Claim Boundary Memo

## Core Problem

The experiments look paradoxical if the only question is:

> Does the harness reduce the gap between strong and low-cost models?

That question is too narrow. The evidence now shows three separable effects:

1. Absolute contract-adherence lift: stronger contracts often raise task scores.
2. Cross-model gap movement: the measured gap may shrink, stay undefined, or widen depending on the baseline gap and which model benefits more.
3. Mechanism-bound enablement: when a specific failure mode is externalized into an explicit input, output contract, evaluator, and carry-forward obligation, a low-cost model can sometimes complete a task it previously failed.

## What The Current Evidence Supports

### Supported Task-Slice Claim

> Contract-rich harnessing improves task contract adherence across multiple task classes, and can compress cross-model gaps when the lower-scoring model gains enough to catch up on a nonzero baseline gap, but not so unevenly that the absolute gap reopens in the opposite direction.

Evidence:

- Structured extraction v2 full slice: G9 compressed all measured nonzero G0 gaps to 0 across 24 runs.
- Project initialization: G9 compressed task-success and safety-consistency gaps to 0, but widened schema-related gaps because the low-cost model benefited more.
- Research workflow: G9 strongly improved absolute performance, citation grounding, and schema validity for both models, but several gap metrics were n/a or mixed because G0 baselines were uniformly poor.

### Supported Mechanism-Composition Claim

> A contract-driven harness can repair specific low-cost-model failure modes through a mechanism-first loop: isolate the failure, make the missing obligation explicit, validate locally with golden/bad cases, then rerun only the narrowed slice.

Evidence:

- Stage 7e v1 showed that a narrow evidence-bound decision macro was feasible under G8, but low-cost-model G9 missed decision-trace and stage-gate retention.
- Stage 7e v2 made retention obligations explicit and repaired trace/gate retention in 4/4 low-cost-model runs, but exposed state-inventory omissions.
- Stage 7e v3 made unknown-state retention explicit and repaired Git/CI/network unknown-state retention in 4/4 low-cost-model runs, but exposed one known-state provenance omission.
- Stage 7e v4 made known-state provenance explicit; after retrying one provider timeout, low-cost-model G8/G9 completed 4/4 runs with task_success=1.000 and atom_primary_metric=1.000.

The Stage 7e v1-v4 sequence supports a narrower but stronger result than the earlier broad workflow slices: low-cost models can become reliable on a fixed evidence-decision macro when the harness externalizes known-state provenance, unknown-state retention, evidence binding, decision trace, stage gate, and carried obligations.

## What The Current Evidence Does Not Support

Unsupported broad claim:

> Harnesses generally make low-cost models equivalent to strong models.

Unsupported universal claim:

> Harnesses always reduce cross-model gaps.

Unsupported workflow claim:

> The current mechanism evidence validates full project initialization or full research workflow automation.

Unsupported readiness claim:

> The harness is production ready.

The project-initialization and research-workflow slices show why universal gap compression is wrong: the harness can help the low-cost model more than the strong model, which improves practical utility while widening some gap metrics. Stage 7e shows why broad workflow claims are still premature: its success is fixed-input, no-tool, deterministic, and evaluator-bound.

## Better Paper Thesis

Use this thesis:

> Contract-driven harness engineering externalizes task constraints into explicit, verifiable control objects. Across SiliconFlow task slices, this improves absolute contract adherence and sometimes compresses model gaps. More importantly, mechanism-first repair can turn specific low-cost-model failure modes into passable contract obligations. Gap compression and full-workflow generalization remain empirical outcomes, not guaranteed properties.

## Recommended Result Framing

Frame the results as four findings:

1. Contract adherence: consistently improves under stronger harnessing.
2. Gap compression: strong positive result on structured extraction; partial/mixed on project initialization and research workflow.
3. Weak-model enablement: Stage 7e v1-v4 shows a low-cost model can pass a fixed evidence-decision macro after the missing obligations are made explicit.
4. Boundary condition: the result currently covers mechanism-bound, fixed-input macros, not open-ended project initialization, tool-using research workflows, or production readiness.

## Drafting Rules

Every claim about gap compression must name:

- task class,
- model pair,
- harness arm,
- metric,
- whether the G0 baseline gap was nonzero.

Every claim about weak-model enablement must name:

- the original failure mode,
- the mechanism added to the harness,
- the local golden/bad gate,
- the real-model rerun result,
- the task boundary that prevents overgeneralization.

No sentence should say "the harness reduces model gaps" or "the harness enables weak models" without those boundaries.

## Post-Freeze Stage B v3 Boundary Update

The 2026-06-14 Stage B v3 full perturbation slice adds a negative boundary to
the mechanism-composition claim.

- The literal G9 skeleton preserved valid JSON and nested state hierarchy in
  30/30 Qwen3-8B runs.
- It passed 18/30 runs and 6/10 macro-condition cells.
- Four cells failed the preregistered 2/3 threshold.
- Failures were exact-slot misses: required evidence IDs were replaced in nine
  runs, and required paraphrased closed-vocabulary labels were rewritten in six
  runs.

The evidence therefore supports hierarchy stabilization, not general exact-slot
robustness. Stage 7e v4 remains a valid bounded repair case, but its earlier
small smoke does not establish perturbation stability. Future writing must not
describe literal skeletons as sufficient for reliable evidence-array or
closed-vocabulary preservation.
