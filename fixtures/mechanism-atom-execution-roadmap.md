# Mechanism Atom Execution Roadmap

## Status

This roadmap is the controlling execution plan for the next phase of the contract-driven harness research.

It converts the mechanism-first direction into stage gates. Work should proceed in order unless a stage gate explicitly fails and the roadmap is revised with a recorded rationale.

## Execution Rule

Do not run additional broad workflow model slices until:

1. mechanism atoms are specified,
2. atom evaluators pass golden and known-bad checks,
3. at least one mechanism-ladder pilot has been run,
4. only passing atoms are composed into broad workflows.

This rule is meant to prevent `project_initialization` and `research_workflow` from becoming prompt-shaped, random, hard-to-interpret tasks again.

## Stage 1: Freeze The Mechanism-Atom Framework

### Objective

Make the research object stable.

### Required Inputs

- `research/04_methods/mechanism-atom-definition.md`
- `research/04_methods/mechanism-atom-coverage-framework.md`
- `research/04_methods/harness-schemas/mechanism-atom.schema.json`
- Current claim-boundary memo.

### Required Work

- Confirm the mechanism atom definition.
- Confirm the coverage rule:

```text
Harness mechanism x agent operation x failure mode
```

- Confirm the A1-A10 minimum sufficient atom library.
- Confirm the three claim levels:
  - gap compression,
  - weak-model enablement,
  - harnessed weak vs unconstrained strong advantage.

### Exit Criteria

- Framework documents exist.
- Source index and evidence ledger reference them.
- Backlog points to this roadmap.

### Current Status

Mostly complete. This roadmap makes the stage gate explicit.

## Stage 2: Specify The 10 Mechanism Atoms

### Objective

Turn A1-A10 from method concepts into fixture specifications.

### Required Work

For each atom A1-A10, create or draft:

- `mechanism_atom.json`
- `task_spec.json`
- `memory_slice.json`
- `evidence_bundle.json`
- `output_contract.json`
- `input.md`
- `golden_output.json` or `golden_output.md`
- at least one known-bad output fixture
- pass/fail criteria
- composition interface

### Exit Criteria

- Every atom has a complete spec draft.
- Each atom names one primary mechanism.
- Each atom names one dominant failure mode.
- Each atom declares what it consumes and emits.

### Constraint

No model API calls in this stage.

## Stage 3: Build First-Batch High-Value Atom Fixtures

### Objective

Implement the first empirical slice without overbuilding all 10 atoms.

### Recommended First Batch

- A1 Schema-Bound Extraction.
- A3 Constraint-Safe Planning.
- A4 State Inventory.
- A8 Evidence-Type Separation.
- A6 Validator Repair.

### Rationale

These atoms directly explain why the current broad `project_initialization` and `research_workflow` tasks are too random:

- project initialization needs state inventory, constraint planning, and no-overwrite discipline;
- research workflow needs evidence typing and claim discipline;
- both need schema and validator repair.

### Exit Criteria

- First-batch atom directories exist.
- Fixture validator recognizes atom fixtures.
- Each first-batch atom has golden and known-bad examples.

## Stage 4: Upgrade Evaluators And Metrics

### Objective

Make atom-level results interpretable.

### Required Metrics

- atom primary metric,
- task success,
- schema validity,
- citation/evidence grounding,
- constraint consistency,
- state accuracy,
- evidence-type accuracy,
- stage completion,
- repair success,
- trace completeness,
- weak-model enablement lift,
- harnessed-weak-vs-unconstrained-strong advantage,
- gap compression only when G0 baseline gap is nonzero.

### Exit Criteria

- Golden outputs pass.
- Known-bad outputs fail for the intended reason.
- Metrics identify primary mechanism lift separately from aggregate quality.
- Pending or invalid runs cannot enter final metrics.

### Constraint

No model API calls before golden/bad local checks pass.

## Stage 5: Run Local Golden And Known-Bad Validation

### Objective

Prove the benchmark can score atoms before spending provider budget.

### Required Work

- Run fixture validation.
- Run evaluator on golden outputs.
- Run evaluator on known-bad outputs.
- Confirm each bad output maps to the intended failure mode.
- Compile prompt packets and adapter requests in dry-run mode.

### Exit Criteria

- 0 structural errors.
- Golden outputs pass expected thresholds.
- Known-bad outputs fail.
- Dry-run manifests compile.

### Constraint

If a known-bad output passes, fix the evaluator or fixture before proceeding.

## Stage 6: Run First Mechanism-Atom Pilot

### Objective

Test whether mechanism arms enable the budget model and whether any model gaps shrink.

### Recommended Pilot

Cost-aware option:

```text
2 models x 3 atoms x 4 arms x 2 repetitions = 48 runs
```

Preferred option:

```text
2 models x 4 atoms x 4 arms x 2 repetitions = 64 runs
```

### Recommended Arms

- G0 raw.
- G2 OutputContract.
- G8 validator.
- G9 full.

Add G3 when the selected atoms centrally test evidence grounding.

### Exit Criteria

- All runs complete or failures are recorded.
- Metrics report weak-model enablement lift.
- Metrics report harnessed weak vs strong G0 advantage.
- Gap compression is reported only where baseline gap is nonzero.

## Stage 7: Compose Passing Atoms Into Broad Workflows

### Objective

Build coarse workflow tasks only from atoms that have passed atom-level gates.

### Project Initialization Chain

```text
State Inventory
-> Bounded Context Recall
-> Constraint-Safe Planning
-> No-Overwrite Action Plan
-> Schema Report
-> Validator Repair
-> Traceable Decision
```

### Research Workflow Chain

```text
Evidence Grounding
-> Evidence-Type Separation
-> Stage-Gated Synthesis
-> Claim Map
-> Traceable Decision
-> Validator Repair
```

### Exit Criteria

- Each composed workflow lists the atoms it uses.
- Each atom interface is wired explicitly.
- If a required atom failed Stage 6, that composed workflow is blocked or redesigned.

## Stage 8: Return To Paper Claims

### Objective

Choose the paper claim based on evidence rather than desire.

### Claim Decision Rules

Use gap compression as the main claim only if:

- relevant G0 baseline gaps are nonzero,
- G9 or target mechanism arms reduce those gaps,
- effect appears across more than one atom or workflow.

Use weak-model enablement as the main claim if:

- budget model improves meaningfully from G0 to mechanism arms,
- results are stable across repetitions,
- gap compression is mixed, undefined, or negative.

Use harnessed weak vs unconstrained strong as the product-methodology claim if:

- `budget_model + harness` beats `strong_model + G0` on contract-critical metrics.

Use composition-boundary framing if:

- atoms pass but composed workflows fail.

### Exit Criteria

- Claim-boundary memo is updated.
- Evidence ledger contains atom pilot results.
- Methodology paper outline reflects actual results.

## Strictness Policy

This roadmap is strict in ordering, not brittle in content.

Strict:

- Do not jump from current broad-task results directly to more broad-task runs.
- Do not compose workflows from atoms that have not passed.
- Do not treat atom success as end-to-end success.
- Do not claim gap compression when G0 baseline gaps are zero.

Allowed revisions:

- Replace an atom if it fails the definition gate.
- Add a perturbation if it targets a documented failure mode.
- Reduce run count for budget reasons, if the claim boundary is reduced too.
- Change model provider only after config and preflight validation.

Every revision should be recorded in the evidence ledger or an ADR-style note before it changes the experiment plan.
