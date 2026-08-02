# Mechanism Atom Definition

## Position

The benchmark should define mechanism atoms before composing large workflow tasks.

A mechanism atom is the smallest testable unit of harness behavior that can be:

1. isolated from broad task semantics,
2. evaluated with deterministic pass criteria,
3. composed with other passing atoms into a larger skill or workflow,
4. compared across harness arms and model tiers.

This means `project_initialization` and `research_workflow` should not be treated as primitive tasks. They should be treated as composed workflows built from mechanism atoms that have already passed their local tests.

## Definition

A mechanism atom is not just a small task. It is a contract-bound operation with one primary mechanism under test.

Required properties:

- One dominant mechanism under test.
- Fixed input snapshot.
- Explicit output contract.
- Deterministic evaluator.
- Clear pass and fail conditions.
- Declared composition interface.
- Declared non-goals.

If a fixture needs several unrelated judgments to pass, it is probably not an atom yet.

## Mechanism Atom Schema

Each atom fixture should include:

```text
mechanism_atom.json
task_spec.json
memory_slice.json
evidence_bundle.json
output_contract.json
input.md
golden_output.json or golden_output.md
```

`mechanism_atom.json` describes what mechanism is being tested and how it can later compose with other atoms.

## Canonical Mechanisms

| Mechanism | Primary capability | Typical failure without harness | Main metric |
|---|---|---|---|
| OutputContract | produce a valid required shape | missing fields, wrong sections, unusable output | schema_validity |
| EvidenceBundle | use only supplied evidence | unsupported claims, fake citations | citation_grounding |
| TaskSpec | obey objective and constraints | drifting goal, unsafe action, skipped requirement | task_success |
| MemorySlice | respect context boundary | stale context, irrelevant assumptions, topic leakage | context_relevance |
| WorkflowGraph | follow stage order | skipped stage, premature final answer | stage_completion |
| ValidatorGate | repair invalid output | one-shot invalid output remains invalid | repair_success |
| TraceLog | expose decision path | unverifiable behavior | trace_completeness |

## Atom Acceptance Rules

An atom is accepted into the composition library only when:

1. The fixture validates structurally.
2. The golden output scores full or expected-high metrics.
3. The evaluator distinguishes at least one known bad output from the golden output.
4. The G0 baseline leaves room for improvement on at least one target metric.
5. The G9 or relevant mechanism arm improves the target metric for `budget_model`.
6. The atom has a declared composition interface.

Rule 4 prevents ceiling-effect atoms from entering the main benchmark.
Rule 5 keeps the focus on weak-model enablement.

## Composition Rules

Passing atoms can be composed into a large workflow only if their interfaces line up:

| Interface field | Meaning |
|---|---|
| `input_contract` | What the atom requires from the previous stage |
| `output_contract` | What the atom emits for the next stage |
| `state_dependencies` | Memory or filesystem state needed |
| `evidence_dependencies` | Required evidence bundle IDs or evidence types |
| `failure_signal` | How downstream stages know this atom failed |
| `repair_policy` | Whether the atom can retry, ask for clarification, or stop |

Composition should be treated as a second-stage experiment. A composed workflow should not be tested as if it were a primitive mechanism.

## Initial Atom Library

### A1: Schema-Bound Extraction

Primary mechanism:

- OutputContract.

Supporting mechanisms:

- EvidenceBundle,
- ValidatorGate.

Pass condition:

- Required fields are present.
- Values match the golden output.
- Evidence IDs are valid and sufficient.

Composition role:

- Provides structured state for later planning or reporting.

### A2: Evidence Grounding

Primary mechanism:

- EvidenceBundle.

Supporting mechanisms:

- OutputContract.

Pass condition:

- Every reportable claim has a valid evidence ID.
- Inferred claims are labeled as inferred.
- Unsupported claims are absent or explicitly marked as unresolved.

Composition role:

- Feeds synthesis and recommendation stages.

### A3: Constraint-Safe Planning

Primary mechanism:

- TaskSpec.

Supporting mechanisms:

- MemorySlice,
- OutputContract.

Pass condition:

- Forbidden actions are not proposed.
- Required actions are included.
- Blocked actions are labeled as blocked rather than silently skipped.

Composition role:

- Produces safe project initialization or tool-use plans.

### A4: State Inventory

Primary mechanism:

- MemorySlice.

Supporting mechanisms:

- TaskSpec.

Pass condition:

- Existing state is correctly identified.
- Protected files are identified.
- Unknown state is not guessed.

Composition role:

- Feeds constraint-safe planning.

### A5: Stage-Gated Synthesis

Primary mechanism:

- WorkflowGraph.

Supporting mechanisms:

- EvidenceBundle,
- OutputContract,
- TraceLog.

Pass condition:

- Brief, evidence typing, synthesis, recommendation, and risks are all present.
- No recommendation is presented as extracted evidence.
- The output exposes stage status.

Composition role:

- Forms the backbone of research workflow.

### A6: Validator Repair

Primary mechanism:

- ValidatorGate.

Supporting mechanisms:

- OutputContract,
- TraceLog.

Pass condition:

- The model receives validator feedback and repairs the targeted violation.
- The repaired output improves without introducing a new critical violation.

Composition role:

- Can wrap any atom or composed workflow.

## Project Initialization Composition

The large `project_initialization` workflow should be composed only after these atoms pass:

1. A4 State Inventory.
2. A3 Constraint-Safe Planning.
3. A1 Schema-Bound Extraction for plan reporting.
4. A6 Validator Repair.

Expected composed output:

- created files,
- skipped files,
- protected files,
- blocked actions,
- risks,
- next steps.

## Research Workflow Composition

The large `research_workflow` should be composed only after these atoms pass:

1. A2 Evidence Grounding.
2. A5 Stage-Gated Synthesis.
3. A1 Schema-Bound Extraction for structured claim maps.
4. A6 Validator Repair.

Expected composed output:

- research brief,
- evidence table,
- extracted vs inferred claim map,
- synthesis,
- recommendation,
- unresolved risks.

## Evaluation Order

Recommended order:

1. Define and validate atom fixtures.
2. Run G0/G2/G3/G8/G9 on atoms.
3. Accept atoms into composition library only if they pass acceptance rules.
4. Compose one project-initialization workflow and one research-workflow.
5. Run composed tasks with G0/G9 and compare against atom-level results.

This order tests whether the harness is a set of working mechanisms rather than a collection of successful prompts.

The controlling stage plan for executing this work is `research/04_methods/mechanism-atom-execution-roadmap.md`.

## Coverage Framework

Atom design should follow `research/04_methods/mechanism-atom-coverage-framework.md`.

The short rule is:

```text
Harness mechanism x agent operation x failure mode
```

An atom library is not considered systematic until it explicitly covers the chosen mechanisms, operations, and dominant failure modes, then explains which combinations are intentionally out of scope.

## Claim Boundary

If atom tests pass but composed workflows fail, the paper can claim that the mechanisms work locally but composition is still an open systems problem.

If atom tests and composed workflows both pass, the paper can claim that mechanism-level harnessing scales to bounded workflow tasks.

If gap compression fails but weak-model enablement succeeds, the paper can still claim:

> Harness mechanisms make weak models usable on bounded, contract-critical operations, even when they do not erase all strong-model advantages.
