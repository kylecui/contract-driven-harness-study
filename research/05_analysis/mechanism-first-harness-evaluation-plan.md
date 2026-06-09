# Mechanism-First Harness Evaluation Plan

## Purpose

The current task labels are too coarse:

- `structured-extraction` is a standard contract-following operation.
- `project-initialization` mixes planning, filesystem policy, convention selection, state inspection, and output reporting.
- `research-workflow` mixes evidence reading, inference discipline, synthesis, citation policy, and recommendation.

This makes the experiment hard to interpret. A task-class result can be positive or mixed because of task randomness rather than because a specific harness mechanism did or did not work.

The next evaluation should therefore define mechanism atoms first, test them independently, and only then compose passing atoms into one or two coarse workflow tasks.

## Revised Research Question

Primary question:

> Which contract-driven harness mechanisms make weaker models reliably complete agentic work, and under which mechanisms do cross-model gaps shrink?

Secondary fallback question:

> Even when cross-model gaps do not shrink, can harnessing make the weaker model more stable and reliable than an unconstrained stronger-model baseline on contract-critical metrics?

This fallback is important because the practical value of the harness may be weak-model enablement, not universal strong-vs-weak equivalence.

## Claim Ladder

### Claim A: Gap Compression

Strongest claim:

> Under specific task mechanisms and metrics, G9 reduces the measured gap between strong and budget models.

Current support:

- Strong on structured extraction (`P2-E27`, `P2-E28`).
- Mixed on project initialization (`P2-E29`, `P2-E30`).
- Partly interpretable on research workflow because G0 floor effects make several gaps undefined (`P2-E31`, `P2-E32`).

Failure condition:

- G9 improves both models but the budget model improves more, widening some gaps.
- G0 fails for both models, making baseline gap zero and compression ratio not meaningful.

### Claim B: Weak-Model Enablement

Fallback but still publishable claim:

> Contract-driven harnessing turns previously unreliable weak-model behavior into task-complete, schema-valid, evidence-grounded behavior on bounded agentic operations.

Current support:

- Structured extraction: budget model reaches full or near-full contract adherence under G9 (`P2-E28`).
- Project initialization: budget model improves task success from 0.778 to 1.000 and schema validity from 0.250 to 1.000 (`P2-E30`).
- Research workflow: budget model improves task success from 0.000 to 0.917 and citation grounding from 0.000 to 1.000 (`P2-E32`).

This claim does not require the strong-model gap to shrink. It only requires a clear before/after improvement for the weak model under the same provider, fixture, and evaluator.

### Claim C: Harnessed Weak Model vs Unconstrained Strong Model

Most practical claim:

> On contract-critical metrics, a harnessed weak model can be more reliable than an unconstrained strong model, even if its prose style is less fluent.

This should be tested directly as:

```text
budget_model + G9  versus  strong_model + G0
```

Candidate metrics:

- task success,
- schema validity,
- evidence/citation grounding,
- safety or no-overwrite consistency,
- evaluator warnings,
- output determinism across repetitions.

This is likely the best bridge between academic defensibility and PEtFiSh product value.

## Mechanisms To Test

Instead of adding more broad task classes, decompose G9 into mechanism modules:

| Mechanism | What it externalizes | Expected benefit | Best target operations |
|---|---|---|---|
| OutputContract | required shape, fields, sections, citation policy | schema validity, evaluator compatibility | extraction, summaries, reports |
| EvidenceBundle | allowable evidence and evidence IDs | grounding, reduced hallucinated support | research, comparison, due diligence |
| TaskSpec | objective, constraints, success criteria, forbidden actions | task success, safety consistency | initialization, tool planning, workflow runs |
| MemorySlice | active context, must-load/must-not-load scope | less context pollution, fewer irrelevant assumptions | multi-step project work |
| WorkflowGraph | ordered stages and stop conditions | fewer skipped steps, more reproducible behavior | research workflow, project initialization |
| ValidatorGate | post-output checks and repair loop | fewer invalid final artifacts | all contract-bound tasks |
| TraceLog | observable decisions, evidence use, and warnings | debuggability, regression testing | all benchmarked workflows |

## Mechanism-Based Task Atoms

The next fixtures should be small, composable operations rather than broad workflows. The detailed atom definition and acceptance rules live in `research/04_methods/mechanism-atom-definition.md`.

### Atom 1: Schema-Bound Extraction

Mechanisms:

- OutputContract,
- EvidenceBundle,
- ValidatorGate.

Question:

> Can the model extract exactly the required fields from noisy input and cite only valid evidence IDs?

This is the cleanest positive-control atom.

### Atom 2: Constraint-Safe Initialization

Mechanisms:

- TaskSpec,
- MemorySlice,
- OutputContract,
- ValidatorGate.

Question:

> Can the model plan or simulate initialization without overwriting existing project state, while reporting created/skipped/blocked actions in a fixed contract?

This is the mechanism-correct version of `project-initialization`.

### Atom 3: Evidence-to-Inference Separation

Mechanisms:

- EvidenceBundle,
- OutputContract,
- ValidatorGate.

Question:

> Can the model separate extracted evidence from inferred judgment and avoid unsupported claims?

This is the mechanism-correct version of the research workflow's core discipline.

### Atom 4: Stage-Gated Research Workflow

Mechanisms:

- TaskSpec,
- EvidenceBundle,
- WorkflowGraph,
- OutputContract,
- TraceLog.

Question:

> Can the model move through brief -> evidence -> synthesis -> recommendation without skipping required stages or mixing evidence types?

This should replace the current broad `research-workflow` fixture.

### Atom 5: Repair Under Validator Feedback

Mechanisms:

- ValidatorGate,
- OutputContract,
- TraceLog.

Question:

> When the first output violates the contract, does an explicit validator-repair loop let the weak model converge to an acceptable artifact?

This is important because real PEtFiSh skills should not rely on one-shot compliance.

## Recommended Next Experimental Matrix

Use a mechanism ladder instead of only G0 vs G9:

| Arm | Included mechanisms |
|---|---|
| G0 | raw task only |
| G2 | OutputContract |
| G3 | OutputContract + EvidenceBundle |
| G6 | TaskSpec + EvidenceBundle + OutputContract + WorkflowGraph |
| G8 | G6 + ValidatorGate |
| G9 | G8 + MemorySlice + TraceLog |

Minimum first slice:

- Models: `strong_model`, `budget_model`.
- Atoms: schema-bound extraction, constraint-safe initialization, evidence-to-inference separation.
- Repetitions: 3.
- Arms: G0, G2, G3, G8, G9.

This is 2 x 3 x 3 x 5 = 90 runs. If cost is a concern, start with:

- Models: 2.
- Atoms: 3.
- Repetitions: 2.
- Arms: G0, G2, G8, G9.

This is 48 runs and still identifies which mechanisms create most of the lift.

## Metrics

Keep the current gap-compression metric, but add two mechanism-first metrics.

### 1. Gap Compression

```text
1 - Gap_harness / Gap_baseline
```

Use only when the G0 baseline gap is nonzero.

### 2. Weak-Model Enablement Lift

```text
budget_model_Gx - budget_model_G0
```

Report per metric. This is the fallback claim's main statistic.

### 3. Harnessed Weak vs Unconstrained Strong Advantage

```text
budget_model_Gx - strong_model_G0
```

This directly tests whether a harnessed weak model can beat an unconstrained strong model on reliability metrics.

## How To Reframe Project Initialization

Current issue:

`project-initialization` is still too much like a broad skill behavior. It mixes choosing conventions, detecting existing state, respecting no-overwrite policy, planning files, and explaining risks.

Mechanism-correct redesign:

1. `StateInventory`: given a fixed project tree, identify existing files and protected paths.
2. `PolicyApplication`: apply no-overwrite and skill routing rules.
3. `PlanCompilation`: produce a deterministic create/skip/update plan.
4. `OutputContract`: report actions, blocked items, risks, and next steps.
5. `ValidatorGate`: reject plans that overwrite protected files or omit required fields.

Only after these atoms pass should they be recombined into a large `project-initializer` skill/workflow.

## How To Reframe Research Workflow

Current issue:

`research-workflow` tests the model's whole research behavior in one shot. That is useful as an end-to-end test, but weak as mechanism evidence.

Mechanism-correct redesign:

1. `BriefFraming`: convert vague research intent into research questions and boundaries.
2. `EvidenceTyping`: classify claims as extracted, inferred, ambiguous, or proposed.
3. `CitationBinding`: attach valid evidence IDs to each reportable claim.
4. `SynthesisStep`: derive findings from evidence clusters without hiding contradictions.
5. `RecommendationStep`: label recommendations as proposed, not extracted facts.
6. `QualityGate`: detect unsupported claims and evidence-type leakage.

Only after these atoms pass should they be recombined into a large research workflow.

## Decision

The next work should not be another broad task slice, and it should not immediately build large replacement workflows.

The next work should be:

1. Define the mechanism atom library and schema.
2. Build mechanism-atom fixtures for initialization and research.
3. Add evaluator support for weak-model enablement and harnessed-weak-vs-unconstrained-strong comparison.
4. Run a small mechanism ladder slice.
5. Compose only the passing atoms into one project-initialization workflow and one research-workflow.
6. Compare composed-workflow results against atom-level results before optimizing the large skills/workflows.

This directly tests the ideal picture:

> A sequence of explicit G9 mechanisms creates measurable capability lift, makes weak models complete bounded tasks, and sometimes reduces model gaps. Where gap reduction fails, the paper can still claim weak-model enablement and reliability improvement under contract.

## Non-Claims

Do not claim:

- G9 always reduces model gaps.
- Weak models become generally equivalent to strong models.
- End-to-end project initialization or research workflow is solved before mechanism atoms pass.

Do claim, if the mechanism slice supports it:

- Specific mechanisms improve specific contract-critical capabilities.
- Weak models can become reliable on bounded operations when task constraints are externalized.
- A harnessed weak model can outperform an unconstrained strong model on stability and contract adherence, even if its language quality is less elegant.
