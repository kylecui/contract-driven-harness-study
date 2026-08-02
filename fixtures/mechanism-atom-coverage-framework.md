# Mechanism Atom Coverage Framework

## Purpose

Mechanism atoms should be designed through a coverage framework, not by brainstorming examples.

The goal is not to create many small tasks. The goal is to cover the harness mechanisms that plausibly explain why weak models become more reliable under contract-driven execution.

This framework defines:

1. the coverage space,
2. selection rules for atom candidates,
3. a minimum sufficient atom library,
4. expansion rules for later studies,
5. validity threats and non-claim boundaries.

## Core Principle

Use mechanism coverage before workflow coverage.

The correct order is:

```text
mechanism taxonomy
  -> failure-mode taxonomy
  -> atom candidates
  -> deterministic evaluators
  -> accepted atom library
  -> composed project/research workflows
```

This prevents broad workflows such as `project_initialization` and `research_workflow` from hiding multiple uncontrolled mechanisms inside one fixture.

## Coverage Space

Mechanism atoms should cover a three-dimensional space:

```text
Harness mechanism x agent operation x failure mode
```

### Axis 1: Harness Mechanism

| Mechanism | Research question |
|---|---|
| OutputContract | Does an explicit output contract improve valid, usable artifacts? |
| EvidenceBundle | Does bounded evidence improve grounding and claim discipline? |
| TaskSpec | Does an explicit task contract improve constraint obedience and task completion? |
| MemorySlice | Does bounded context reduce irrelevant assumptions and stale-state errors? |
| WorkflowGraph | Does staged execution prevent skipped or premature steps? |
| ValidatorGate | Does validation feedback improve repair and final acceptance? |
| TraceLog | Does required traceability improve observability without harming task success? |

### Axis 2: Agent Operation

| Operation | Why it matters |
|---|---|
| Extract | Converts unstructured input into structured state. |
| Classify | Assigns evidence, state, or risk labels. |
| Plan | Produces safe action plans before execution. |
| Transform | Converts one artifact form into another. |
| Synthesize | Combines evidence into findings and recommendations. |
| Decide | Selects among alternatives under constraints. |
| Repair | Responds to validator feedback or detected failure. |
| Report | Produces final user-facing artifacts. |

### Axis 3: Failure Mode

| Failure mode | Typical weak-model behavior |
|---|---|
| Missing required structure | Omits fields, sections, or machine-readable shape. |
| Unsupported claim | Makes claims without valid evidence IDs. |
| Constraint violation | Proposes forbidden actions or ignores safety policy. |
| State hallucination | Assumes files, sources, or facts not in the snapshot. |
| Stage skipping | Jumps to final answer without required intermediate steps. |
| Type leakage | Presents inference as extracted evidence or recommendation as fact. |
| Repair failure | Repeats the same invalid output after feedback. |
| Non-observable reasoning | Produces outputs that cannot be audited or debugged. |

## Minimum Coverage Requirement

An initial atom library is sufficient only if it covers:

1. every canonical harness mechanism at least once as a primary mechanism,
2. extraction, planning, synthesis, and repair as agent operations,
3. structure, grounding, constraint, state, stage, type-leakage, and repair failure modes,
4. at least one atom needed by project initialization,
5. at least one atom needed by research workflow,
6. at least one shared atom used by both composed workflows.

The shared atom requirement matters because the paper should show reusable mechanisms, not one-off fixtures.

## Selection Rules

### Rule 1: One Primary Mechanism

Each atom should have one primary mechanism. Supporting mechanisms are allowed, but the evaluator must identify the metric primarily affected by the primary mechanism.

Bad atom:

> "Do an entire research workflow with citations and recommendations."

Better atoms:

> Evidence grounding, evidence-to-inference typing, stage-gated synthesis, validator repair.

### Rule 2: One Dominant Failure Mode

Each atom should be designed around one dominant known failure.

This makes negative examples possible and keeps evaluator logic interpretable.

### Rule 3: Fixed Input Snapshot

The atom must not depend on live web state, current filesystem drift, or fresh provider behavior unless that changing state is explicitly part of the atom.

### Rule 4: Deterministic Evaluator

The evaluator should produce the same score for the same output. Human acceptance can remain an aggregate metric, but the atom's pass/fail rule should not depend on subjective prose quality.

### Rule 5: Improvement Room

An atom should not enter the main model benchmark if `G0` already scores near ceiling for both models. It can remain a smoke or sanity fixture, but it cannot support lift claims.

### Rule 6: Composition Interface

Every accepted atom must declare what it consumes and what it emits. If it cannot compose, it is a unit test, not a mechanism atom for workflow construction.

## Minimum Sufficient Atom Library

The first scientifically defensible library should include 10 atoms.

| Atom ID | Atom | Primary mechanism | Operation | Dominant failure mode | Composition role |
|---|---|---|---|---|---|
| A1 | Schema-Bound Extraction | OutputContract | Extract | Missing required structure | Shared |
| A2 | Evidence Grounding | EvidenceBundle | Classify/Report | Unsupported claim | Research |
| A3 | Constraint-Safe Planning | TaskSpec | Plan | Constraint violation | Project |
| A4 | State Inventory | MemorySlice | Extract/Classify | State hallucination | Project |
| A5 | Stage-Gated Synthesis | WorkflowGraph | Synthesize | Stage skipping | Research |
| A6 | Validator Repair | ValidatorGate | Repair | Repair failure | Shared |
| A7 | Traceable Decision | TraceLog | Decide | Non-observable reasoning | Shared |
| A8 | Evidence-Type Separation | EvidenceBundle | Classify/Synthesize | Type leakage | Research |
| A9 | No-Overwrite Action Plan | TaskSpec | Plan/Report | Unsafe overwrite proposal | Project |
| A10 | Bounded Context Recall | MemorySlice | Extract/Report | Irrelevant or stale context use | Shared |

This set covers all seven canonical mechanisms, all critical operation types, and the dominant failure modes observed in the current project-initialization and research-workflow slices.

## Coverage Matrix

| Mechanism | A1 | A2 | A3 | A4 | A5 | A6 | A7 | A8 | A9 | A10 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| OutputContract | P | S | S |  | S | S |  | S | S | S |
| EvidenceBundle | S | P |  |  | S |  |  | P |  |  |
| TaskSpec |  |  | P | S |  |  | S |  | P |  |
| MemorySlice |  |  | S | P |  |  |  |  | S | P |
| WorkflowGraph |  |  |  |  | P |  | S | S |  |  |
| ValidatorGate | S |  |  |  |  | P |  |  | S |  |
| TraceLog |  |  |  |  | S | S | P |  |  |  |

Legend:

- `P`: primary mechanism.
- `S`: supporting mechanism.

## Project Initialization Atom Chain

Project initialization should be composed from:

1. A4 State Inventory.
2. A10 Bounded Context Recall.
3. A3 Constraint-Safe Planning.
4. A9 No-Overwrite Action Plan.
5. A1 Schema-Bound Extraction for final action report.
6. A6 Validator Repair.
7. A7 Traceable Decision for risk and blocker decisions.

This turns project initialization from a vague "initialize the project" prompt into a staged contract:

```text
observe state -> bound context -> plan safely -> apply no-overwrite policy -> report -> validate/repair -> trace decision
```

## Research Workflow Atom Chain

Research workflow should be composed from:

1. A2 Evidence Grounding.
2. A8 Evidence-Type Separation.
3. A5 Stage-Gated Synthesis.
4. A1 Schema-Bound Extraction for claim maps.
5. A7 Traceable Decision for recommendation logic.
6. A6 Validator Repair.

This turns research workflow from a broad synthesis task into a staged contract:

```text
ground evidence -> type claims -> synthesize by stage -> structure claim map -> trace recommendation -> validate/repair
```

## Experimental Design

### Hypotheses

H1:

> For each accepted atom, the target mechanism arm improves the budget model on the atom's primary metric relative to G0.

H2:

> For atoms with nonzero G0 cross-model gaps, stronger harness arms reduce the gap on primary metrics.

H3:

> On contract-critical metrics, `budget_model + target mechanism` can outperform `strong_model + G0`.

### Independent Variables

- Model tier: `strong_model`, `budget_model`.
- Harness arm: G0, target mechanism arm, G8, G9.
- Atom type: A1-A10.
- Perturbation level: clean, noisy, adversarial/decoy.

### Dependent Variables

- Primary atom metric.
- Task success.
- Schema validity.
- Citation/evidence grounding.
- Constraint consistency.
- Stage completion.
- Repair success.
- Trace completeness.
- Weak-model enablement lift.
- Harnessed-weak-vs-unconstrained-strong advantage.
- Gap compression where baseline gaps are nonzero.

### Controls

- Same input snapshot for all models and arms.
- Same evaluator and golden output.
- Same provider configuration.
- Same temperature and output token budget.
- Same repetitions.
- Raw outputs stored before repair.

## Perturbation Design

Each atom should eventually have three fixture levels:

| Level | Purpose | Example |
|---|---|---|
| Clean | Verify the atom can be completed under normal conditions. | Required fields are obvious. |
| Noisy | Test robustness to irrelevant but plausible distractors. | Extra proposal IDs, stale files, unused evidence. |
| Adversarial/decoy | Test whether the mechanism blocks a known failure. | Forbidden overwrite, fake evidence ID, conflicting stage instruction. |

Do not start with all levels. Start with clean and noisy for the first slice, then add adversarial/decoy once the evaluator is stable.

## Acceptance Gates

An atom moves through four gates:

### Gate 0: Specification Gate

- `mechanism_atom.json` validates against schema.
- TaskSpec, MemorySlice, EvidenceBundle, and OutputContract validate.
- Pass criteria name measurable metrics.

### Gate 1: Evaluator Gate

- Golden output passes.
- At least one intentionally bad output fails.
- Metric reasons identify the intended failure.

### Gate 2: Mechanism Gate

- Budget model improves under the target mechanism arm relative to G0.
- The improvement appears on the primary metric, not only on unrelated aggregate metrics.

### Gate 3: Composition Gate

- The atom's output can feed at least one downstream atom.
- Failure signal and repair policy are explicit.
- The atom is assigned to a composed workflow chain.

## What Counts As Comprehensive?

Comprehensive does not mean every possible task. It means coverage is explicit and auditable.

The first paper-level study is comprehensive enough if it reports:

1. mechanism coverage: all seven canonical mechanisms covered,
2. operation coverage: extract, classify, plan, synthesize, decide, repair, report covered,
3. failure coverage: all dominant failure modes covered,
4. workflow coverage: both project initialization and research workflow can be composed from accepted atoms,
5. negative coverage: at least one atom or condition where gap compression fails or becomes n/a,
6. perturbation coverage: at least clean and noisy variants for the core atoms,
7. reproducibility coverage: fixed fixtures, raw outputs, validators, metrics, and run manifests.

## Expansion Strategy

After the first atom library, expand by coverage gaps rather than by intuition:

1. Add a new atom only if it covers a currently uncovered mechanism-operation-failure combination.
2. Add a new perturbation only if it targets a known failure mode.
3. Add a new composed workflow only if its required atoms have already passed.
4. Add a new model tier only after the atom/evaluator path is stable.

This keeps the benchmark from becoming a bag of unrelated tasks.

## Validity Threats

### Construct Validity

Risk:

- Atom metrics may oversimplify real workflow success.

Mitigation:

- Report atom-level and composed-workflow results separately.
- Do not claim end-to-end reliability from atom success alone.

### Internal Validity

Risk:

- Supporting mechanisms may cause the observed lift rather than the declared primary mechanism.

Mitigation:

- Use mechanism arms and ablations.
- Keep one primary metric per atom.
- Report supporting mechanisms explicitly.

### External Validity

Risk:

- Atoms may be too PEtFiSh-specific.

Mitigation:

- Define mechanisms generically.
- Keep PEtFiSh as one implementation context.
- Include reusable operation and failure taxonomies.

### Conclusion Validity

Risk:

- Small run counts may overstate stability.

Mitigation:

- Use repetitions, confidence intervals, effect sizes, and disclose n/a gap compression cases.

### Ecological Validity

Risk:

- Fixed snapshots may not reflect live project work.

Mitigation:

- Treat atom experiments as microbenchmarks.
- Use composed workflows as macrobenchmarks after atom validation.

## Non-Claims

Do not claim:

- The atom library covers all agent work.
- Atom success proves production readiness.
- Gap compression is guaranteed.
- Weak models become generally equivalent to strong models.

Can claim, if supported:

- The atom library systematically covers the chosen harness mechanisms, operations, and failure modes.
- Specific mechanisms enable weak-model reliability on bounded contract-critical operations.
- Composed workflows inherit reliability only when their component atoms and interfaces pass.
