# Methods: Contract-Driven Harness Evaluation

## 1. Study Design

This study evaluates whether explicit agent harness contracts can make productivity tasks less dependent on unconstrained model behavior. We do not treat "agent workflow" as a primitive benchmark unit. Instead, we evaluate harness mechanisms in three levels:

1. task slices, which compare broad task classes across harness strengths;
2. mechanism atoms, which isolate a single primary harness mechanism and a dominant failure mode;
3. admitted macros, which compose only mechanisms that have passed local gates and targeted model checks.

This design is intentionally conservative. Broad workflow results can motivate failure analysis, but they do not by themselves justify claims about a general harness methodology. A workflow can enter the main claim only when its component mechanisms, local evaluators, known-bad cases, and cross-step obligations are explicit.

## 2. Harness Model

We define a contract-driven harness as a set of explicit control objects around a language model:

- `TaskSpec`: the objective, constraints, success conditions, and non-goals.
- `MemorySlice`: the bounded context that may be used, plus excluded or unknown state.
- `EvidenceBundle`: admissible evidence items, evidence types, and source links.
- `OutputContract`: required output shape, nested fields, citation policy, and validator rules.
- `WorkflowGraph` or stage gate: required order of intermediate steps and blocked outputs.
- `TraceLog`: decision trace requirements for auditable reasoning and rejection paths.
- `ValidatorGate`: deterministic local checks that distinguish passing outputs from known-bad outputs.

The key methodological assumption is that reliability should be moved from implicit model judgment into explicit, inspectable contracts whenever a task can be bounded. The harness is therefore evaluated as a reliability-engineering layer, not as a claim that low-cost models become generally equivalent to strong models.

## 3. Harness Arms

Experiments use harness arms to vary the strength of external control. Earlier broad slices used a ladder from raw prompting to full harnessing. The later mechanism and macro stages focus on selected arms:

| Arm | Meaning in this study |
|---|---|
| G0 | Raw or minimally constrained task input. |
| G2/G3 | Intermediate mechanism arms, such as schema or evidence support, when relevant to the atom. |
| G8 | Contract-rich execution with validator/evaluator obligations. |
| G9 | Full harness packet with task spec, output contract, evidence, memory policy, workflow, trace, and regression expectations. |

For the Stage 7e and Stage 7-next macro tests, we use G8 and G9 for the low-cost model because the research question at that point is no longer whether G0 fails. It is whether explicit obligations can make the low-cost model pass a bounded composed macro.

## 4. Model And Provider Setup

The real-model slices use SiliconFlow's OpenAI-compatible API. The current low-cost model tier is `Qwen/Qwen3-8B`; strong-model slices in earlier stages used `deepseek-ai/DeepSeek-V3.2`. Provider-backed runs use:

- temperature `0`,
- fixed prompt artifacts exported before execution,
- per-run artifact directories,
- adapter request files,
- output files,
- validation reports,
- metrics files,
- event logs for provider start/end, elapsed time, errors, and retry analysis.

The Stage 7-next smoke used only the low-cost model under G8 and G9 with two repetitions each. This was a targeted transfer test, not a full model-comparison slice.

## 5. Task Slices

The first empirical layer uses broad task slices to identify where harnessing helps and where broad task definitions become too noisy.

| Slice | Purpose | Main methodological role |
|---|---|---|
| Structured extraction | High-constraint task with deterministic output structure | Tests whether strong contracts can compress nonzero baseline gaps. |
| Project initialization | Multi-constraint workspace planning task | Exposes mixed effects and broad-workflow instability. |
| Research workflow | Evidence-backed synthesis task | Exposes grounding, schema, and stage-order failures under open synthesis. |

These slices are useful for discovering failure modes, but the later stages treat broad workflows as composed systems rather than primitives.

## 6. Mechanism Atoms

A mechanism atom is the smallest testable unit of harness behavior with one primary mechanism, fixed input, explicit output contract, deterministic evaluator, known-bad rejection, pass threshold, and composition interface.

The atom coverage framework uses:

```text
Harness mechanism x agent operation x failure mode
```

The initial atom library covers output contracts, evidence bundles, task specs, memory slices, workflow graphs, validator gates, and trace logs. It also covers operations such as extraction, classification, planning, synthesis, decision, repair, and reporting.

Atoms are accepted only when:

1. fixture structure validates;
2. the golden output passes;
3. at least one known-bad output fails for the intended reason;
4. the baseline leaves room for improvement;
5. the low-cost model improves under the relevant harness arm;
6. the atom declares how it can compose with downstream mechanisms.

This prevents the study from treating successful prompts as reusable mechanisms.

## 7. Admitted Macro Composition

Macro tasks are composed only after component mechanisms pass local gates and targeted model checks. A macro must preserve cross-step obligations explicitly. The current admitted macro family is evidence-bound and fixed-input:

| Macro | Composition focus | Result boundary |
|---|---|---|
| Stage 7p v2 | Bounded context and no-overwrite obligation retention | Shows explicit carried obligations can repair a low-cost composition failure in a partial macro. |
| Stage 7e v1-v4 | Evidence-bound decision with state, trace, gate, and provenance retention | Shows an iterative repair loop for a fixed decision macro. |
| Stage 7-next | Evidence-bound method-plan update with one new method-plan stressor | Shows transfer of Stage 7e v4 obligations to a neighboring fixed macro. |

Project initialization and full research workflow remain blocked because the current evidence covers bounded macros, not open-ended tool-using workflows.

## 8. Repair-Loop Protocol

The main methodological contribution is the repair-loop protocol:

1. observe a real model failure;
2. isolate the missing mechanism or obligation;
3. make the obligation explicit in the input and output contract;
4. add or update a known-bad fixture that captures the failure;
5. run local golden/bad regression;
6. execute a targeted real-model slice;
7. update the evidence ledger, claim boundary, and backlog before expanding scope.

Stage 7e illustrates this protocol. Stage 7e v1 found a low-cost-model G9 failure in stage-gate and decision-trace retention. Stage 7e v2 repaired trace/gate retention but exposed unknown-state omissions. Stage 7e v3 repaired unknown-state retention but exposed known-state provenance compression. Stage 7e v4 made known-state provenance explicit and reached 4/4 low-cost-model passes after retry. Stage 7-next then reused those obligations in a method-plan update macro and passed 4/4 low-cost-model runs without provider errors.

## 9. Metrics

Each evaluated run emits a metric vector. The core metrics are:

| Metric | Meaning |
|---|---|
| `task_success` | Aggregate contract completion score. |
| `schema_validity` | Required sections and fields are present. |
| `citation_grounding` | Important claims are bound to valid evidence IDs. |
| `state_accuracy` | Known state, unknown state, and forbidden inferences are preserved without hallucination. |
| `evidence_type_accuracy` | Evidence is correctly classified as extracted, inferred, ambiguous, or proposed. |
| `stage_completion` | Stage gates and blocked outputs are preserved. |
| `trace_completeness` | Decision paths include supported and rejected options with evidence. |
| `context_relevance` | Stale or excluded context is not used for the selected claim. |
| `atom_primary_metric` | Strict pass indicator for the mechanism or macro chain. |

Gap compression is computed only where a nonzero G0 baseline gap exists. If G0 baselines collapse for both models, or if the lower-cost model improves more than the strong model and reopens the absolute gap in the opposite direction, the result is reported as mixed, undefined, or negative rather than forced into a compression claim.

Weak-model enablement is reported when the low-cost model reaches a pass threshold under a harness condition after failing or underperforming under weaker conditions.

## 10. Evaluation Pipeline

Every mechanism or macro follows the same pipeline:

1. create fixture files (`task_spec`, `memory_slice`, `evidence_bundle`, `output_contract`, input, golden output, known-bad outputs);
2. run local fixture and evaluator checks;
3. compile packets into a JSONL benchmark queue;
4. prepare per-run artifact directories;
5. export prompts and adapter requests;
6. run preflight checks against manifests, config, prompt paths, and required API keys;
7. execute provider-backed runs with event logging;
8. evaluate outputs with deterministic scripts;
9. write stage summaries and evidence-ledger entries;
10. update the backlog and claim-boundary memo before further expansion.

If a known-bad output passes, no provider run is allowed. If provider execution fails, the event log is used to distinguish model-quality evidence from provider/runtime deviations. If a real-model run shows a systematic contract miss, the next stage targets that miss rather than expanding the macro.

## 11. Claim Decision Rules

The paper's claims are selected from evidence, not from the original thesis.

Use gap compression as a main claim only when:

- the G0 baseline gap is nonzero;
- the harness arm reduces that gap;
- the effect appears across more than one task, atom, or admitted macro.

Use weak-model enablement as a main claim when:

- the low-cost model improves meaningfully from G0 or weaker harness arms;
- contract-critical metrics reach the pass threshold;
- results are stable across repetitions;
- gap compression is mixed, undefined, or not the right construct.

Use composition-boundary framing when:

- atoms pass but broad workflows fail;
- bounded macros pass but open-ended workflows remain untested;
- the result is valid only under fixed-input, no-tool, deterministic evaluation.

## 12. Validity Threats

Construct validity: deterministic contract metrics may oversimplify human judgments of workflow success. We mitigate this by separating atom-level, macro-level, and broad-workflow claims.

Internal validity: supporting mechanisms may contribute to observed lift. We mitigate this by naming primary mechanisms, supporting mechanisms, and the specific failure mode each repair targets.

External validity: the fixtures are derived from PEtFiSh-style workflows. We mitigate this by defining mechanisms generically and by reporting PEtFiSh as the implementation context, not the whole construct.

Conclusion validity: several targeted runs have small sample sizes. We therefore report them as smoke or targeted repair evidence, not final production benchmarks.

Ecological validity: Stage 7e and Stage 7-next are fixed-input, no-tool macros. They do not represent live research or project initialization with changing filesystem, web, or tool state.

## 13. Reproducibility Artifacts

The study records:

- source index entries,
- evidence-ledger entries,
- fixture directories,
- local golden/bad reports,
- packet JSONL files,
- manifests with prompts,
- provider adapter reports,
- provider event logs,
- evaluation JSON and Markdown summaries,
- stage reports,
- backlog decisions.

This artifact trail is part of the method. Claims are allowed only when they can be traced from paper text to evidence IDs, source IDs, and evaluated run artifacts.
