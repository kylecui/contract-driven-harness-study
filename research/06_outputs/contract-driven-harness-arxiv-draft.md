# Contract-Driven Harness Engineering for Reliable Low-Cost Agent Tasks

arXiv-style working draft derived from the evidence-traceable full draft. External literature citations use BibTeX keys; empirical evidence traceability is preserved in Appendix C and the reproducibility package.


## Abstract

AI agent reliability is often framed as a property of the underlying language model: stronger models are expected to plan better, follow constraints more reliably, and recover from ambiguous context more effectively. This framing is incomplete for productivity tasks that can be bounded by explicit inputs, evidence, state, workflow stages, and output contracts. We study contract-driven harness engineering: a reliability layer that externalizes task obligations into task specifications, bounded memory slices, evidence bundles, output contracts, validation gates, and trace requirements.

Across structured extraction, project initialization, research workflow, mechanism-atom, and admitted-macro experiments, we find that harnessing improves absolute contract adherence and can compress model gaps when baseline gaps are nonzero and the task is highly constrained. However, gap compression is not universal. The more stable result is weak-model enablement on bounded, contract-critical operations.

In a Stage 7e repair loop, successive explicit contracts repaired low-cost-model failures in decision trace retention, stage-gate retention, unknown-state preservation, and known-state provenance, culminating in 4/4 low-cost-model passes on a fixed evidence-bound decision macro. A neighboring Stage 7-next method-plan macro reused these obligations and also passed 4/4 low-cost-model runs. These results support a mechanism-first methodology for agent harness evaluation: broad workflows should be decomposed into testable mechanisms, locally validated against golden and known-bad cases, and admitted to macro composition only when their obligations are explicit.

The current evidence does not establish production readiness or full open-ended workflow reliability. It shows that contract-driven harnesses can turn some low-cost-model failures into observable, repairable, and regression-testable engineering objects.

## 1. Introduction

AI agent systems are increasingly asked to perform productivity work: initialize projects, extract structured information, synthesize evidence, prepare plans, update documents, and coordinate multi-step workflows. In these settings, reliability is often treated as a direct consequence of model capability. If an agent fails to preserve constraints, cite evidence, follow stages, or avoid stale context, the usual explanation is that the underlying model is not strong enough.

That explanation is partly true, but incomplete. Many productivity tasks are not open-ended intelligence tests. They contain obligations that can be stated explicitly: which evidence may be used, which state is known or unknown, which actions are blocked, which fields must be present, which claims require citations, and which stage gate prevents a final recommendation. When these obligations remain implicit, the model must infer and retain them through free generation. When they are externalized into contracts, some of the burden shifts from model intelligence to system design.

This paper studies that shift. We call the approach contract-driven harness engineering: the use of explicit task specifications, bounded memory, evidence bundles, output contracts, workflow gates, validators, and trace requirements to constrain agent behavior. The central question is not whether low-cost models are generally equivalent to strong models. They are not. The question is which parts of agent reliability can be made less dependent on unconstrained model behavior by turning task obligations into inspectable and testable control objects.

The initial thesis of this project was model capability gap compression: a stable harness may reduce the performance gap between strong and low-cost models. Our results support this thesis only under specific conditions. In highly structured extraction tasks, stronger harnessing compressed measured nonzero baseline gaps. In broader project-initialization and research-workflow slices, harnessing improved absolute contract adherence but produced mixed or undefined gap movement. These broader slices revealed a methodological problem: a workflow-level task can hide many mechanisms at once, making it difficult to know whether a result reflects schema following, state retention, evidence grounding, stage discipline, trace completeness, or some interaction among them.

We therefore moved from workflow-first evaluation to mechanism-first evaluation. A mechanism atom is a fixed-input, deterministic, contract-bound operation with one primary mechanism, one dominant failure mode, a golden output, a known-bad output, and a composition interface. Mechanism atoms let us ask smaller questions: Does an explicit evidence bundle improve claim grounding? Does a memory slice prevent state hallucination? Does a stage gate prevent premature recommendation? Does a trace requirement make rejected options auditable? Passing atoms do not prove that a whole workflow is solved, but they make workflow composition interpretable.

The strongest evidence in this study comes from the repair loop created after broad workflow tests exposed unstable behavior. In Stage 7e, we composed a narrow evidence-bound decision macro from state inventory, evidence grounding, evidence typing, traceable decision, and stage-gated synthesis mechanisms. The first version showed that a low-cost model could pass under one harness arm but still lose decision-trace and stage-gate obligations under another. Rather than broadening the benchmark, we isolated the miss and revised the contract. Stage 7e v2 repaired trace and gate retention, but exposed unknown-state omissions. Stage 7e v3 repaired unknown-state retention, but exposed known-state provenance compression. Stage 7e v4 made known-state provenance explicit and reached 4/4 low-cost-model passes after retry.

We then tested whether this was merely a one-fixture patch. Stage 7-next reused the Stage 7e v4 obligations in a neighboring evidence-bound method-plan update macro, adding one new stressor: the output had to select the next admitted macro, list admission criteria, preserve local and real-model gates, and declare non-claims. The low-cost model passed 4/4 SiliconFlow runs under G8/G9, with all runs scoring 1.000 on task success and the strict primary macro metric. This does not establish open-ended workflow reliability. It does show that a repaired obligation set can transfer to a closely related bounded macro.

These findings motivate a narrower and stronger claim than the original gap-compression thesis. Contract-driven harnesses do not make weak models generally equivalent to strong models, and they do not guarantee gap compression. They can, however, raise the usable floor of low-cost models on bounded, contract-critical operations. More importantly, they turn some failures into engineering objects: a missing obligation can be named, added to the contract, captured as a known-bad case, checked locally, rerun against a model, and carried into the evidence ledger and claim boundary.

### Contributions

This paper makes five contributions:

1. We define contract-driven harness engineering as an explicit reliability layer for agent tasks.
2. We propose mechanism atoms as the unit of harness evaluation.
3. We report a multi-stage empirical evaluation across task slices, mechanism atoms, and admitted macros.
4. We introduce a repair-loop protocol for harness development.
5. We provide bounded evidence that low-cost models can become reliable on fixed, contract-critical macros.

## 2. Related Work

This work sits between agent orchestration, declarative LM programming, structured output constraints, retrieval and tool augmentation, memory systems, safety verification, and skill or capability ecosystems. The relevant prior work is not a single line of papers. It is a convergence across systems that move reliability obligations out of a model's implicit free-form generation and into explicit runtime, specification, tool, memory, validation, and evaluation layers.

### 2.1 Agent Workflows And Orchestration

Recent agent engineering guidance distinguishes between fully autonomous agents and workflows whose control paths are explicitly defined. Anthropic's discussion of effective agents is important for this distinction: workflows are appropriate when tasks can be decomposed into predictable steps, while agents are reserved for cases that require open-ended model autonomy. LangGraph, AutoGen, Semantic Kernel, and related orchestration frameworks make a similar engineering move by exposing execution state, graph structure, persistence, human-in-the-loop intervention, tool calls, and observability as system concerns rather than leaving them solely inside a prompt. \cite{P2_EXT_ANTHROPIC,P2_EXT_LANGGRAPH,P2_EXT_AUTOGEN,P2_EXT_SEMANTIC_KERNEL}

These systems solve an important class of production problems: they make execution durable, inspectable, and easier to integrate with tools and humans. However, orchestration frameworks alone do not answer the evaluation question addressed in this paper. A workflow graph can still contain under-specified obligations. It can route steps correctly while losing evidence provenance, collapsing unknown state, skipping stage gates, or producing an ungrounded final recommendation.

Contract-driven harness engineering overlaps with workflow orchestration but treats the graph as only one layer. The unit of interest is the obligation that must survive the graph: state inventory, evidence binding, evidence type separation, trace completeness, stage-gate retention, excluded-context preservation, and repairability.

### 2.2 Declarative LM Programs And Agent Specifications

Declarative LM programming systems, especially DSPy, argue that language model behavior should be represented as programs with signatures, modules, metrics, and optimizers rather than as hand-written prompts. Agent specification work such as AgentSPEX and AgentSpec pushes in a related direction for agent systems: workflows, state, steps, and interfaces should be declared in portable and inspectable forms. \cite{P2_EXT_DSPY,P2_EXT_AGENTSPEX,P2_EXT_AGENTSPEC}

This line of work is close to the method proposed here. Both assume that some reliability gains come from making task structure explicit. The difference is the evaluation target. Declarative systems often emphasize program optimization, portability, or agent specification. This paper emphasizes mechanism-first empirical repair: define one contract-critical mechanism, create golden and known-bad outputs, run deterministic local gates, execute small real-model slices, and update the claim boundary before composing broader workflows.

### 2.3 Structured Outputs, Guardrails, And Validators

Structured output systems and guardrail frameworks externalize output form. OpenAI structured output mechanisms, Outlines-style constrained generation, and Guardrails validators reduce the burden of asking a model to follow a format. They make schema adherence and selected validation checks part of the system layer. \cite{P2_EXT_OPENAI_STRUCTURED_OUTPUTS,P2_EXT_OUTLINES,P2_EXT_GUARDRAILS}

These mechanisms are necessary but insufficient for the problem studied here. Schema validity can guarantee that an output has the expected shape, but it cannot by itself guarantee that a claim is supported, that unknown state remains unknown, that excluded context is not reused, or that a recommendation is blocked when a stage gate is incomplete. The harness studied here therefore treats validators as one component in a larger contract stack. The output contract includes fields, but also semantic obligations: required evidence IDs, evidence type separation, rejected-option traces, explicit blocked outputs, and non-claims.

### 2.4 Retrieval, Tools, Memory, And Externalized Capability

RAG, ReAct, Toolformer, Gorilla, and tool/API-focused agent work show that models can become more capable when knowledge and action are externalized. Retrieval can provide updated evidence and provenance. Tool-use frameworks can turn external actions into typed calls. API benchmarks show that tool descriptions and retrieval can materially improve call generation compared with unaided model behavior. \cite{P2_EXT_RAG,P2_EXT_REACT,P2_EXT_TOOLFORMER,P2_EXT_GORILLA}

Memory-oriented systems such as MemGPT and Letta show that agents can use hierarchical, archival, or stateful memory to extend beyond a single context window. They also expose a reliability problem that is central to this paper: memory is not automatically beneficial. A system must decide what to store, when to summarize, how to retrieve, how to scope memory, and how to prevent stale or irrelevant context from contaminating a new task. \cite{P2_EXT_MEMGPT,P2_EXT_LETTA}

This paper does not primarily study live retrieval, live tool execution, or long-term memory. Most admitted mechanism atoms and macros are fixed-input, no-tool tasks. That design is deliberate. It isolates whether the model can honor explicit contracts before adding live tools, changing corpora, or runtime side effects.

### 2.5 Evaluation, Safety, Verification, And Skill Ecosystems

Agent evaluation and safety work highlights the fragility of agent claims. OAgents-style critiques emphasize protocol variance and reproducibility challenges. Semantic Integrity Constraints, Agentproof, LlamaFirewall, and related verification or guardrail systems argue that agent behavior must be constrained, audited, or checked against explicit policies and semantic rules. \cite{P2_EXT_OAGENTS,P2_EXT_SIC,P2_EXT_AGENTPROOF,P2_EXT_LLAMAFIREWALL}

Capability ecosystems such as MCP servers, agent skills, registries, pack systems, and PEtFiSh-style skill markets represent another route toward harness engineering. They externalize reusable procedures, tool access, installation state, platform routing, quality gates, and capability discovery. In PEtFiSh specifically, packs, skills, MCP servers, installers, trigger evaluators, quality gates, and context plugins make the system a useful experimental setting for studying harness design as an engineering object. Local PEtFiSh-specific evidence is preserved in Appendix C and the reproducibility package.

The gap this paper addresses is mechanism-level evaluation: which explicit obligations actually let a low-cost model complete bounded contract-critical operations, and how should a harness be repaired when those obligations fail?

## 3. Methods

### 3.1 Study Design

This study evaluates whether explicit agent harness contracts can make productivity tasks less dependent on unconstrained model behavior. We do not treat agent workflow as a primitive benchmark unit. Instead, we evaluate harness mechanisms in three levels:

1. task slices, which compare broad task classes across harness strengths;
2. mechanism atoms, which isolate a single primary harness mechanism and a dominant failure mode;
3. admitted macros, which compose only mechanisms that have passed local gates and targeted model checks.

This design is intentionally conservative. Broad workflow results can motivate failure analysis, but they do not by themselves justify claims about a general harness methodology. A workflow can enter the main claim only when its component mechanisms, local evaluators, known-bad cases, and cross-step obligations are explicit.

### 3.2 Harness Model

We define a contract-driven harness as a set of explicit control objects around a language model:

| Object | Role |
|---|---|
| `TaskSpec` | Objective, constraints, success conditions, and non-goals. |
| `MemorySlice` | Bounded context that may be used, plus excluded or unknown state. |
| `EvidenceBundle` | Admissible evidence items, evidence types, and source links. |
| `OutputContract` | Required output shape, nested fields, citation policy, and validator rules. |
| `WorkflowGraph` or stage gate | Required order of intermediate steps and blocked outputs. |
| `TraceLog` | Decision trace requirements for auditable reasoning and rejection paths. |
| `ValidatorGate` | Deterministic local checks that distinguish passing outputs from known-bad outputs. |

The key methodological assumption is that reliability should be moved from implicit model judgment into explicit, inspectable contracts whenever a task can be bounded. The harness is evaluated as a reliability-engineering layer, not as a claim that low-cost models become generally equivalent to strong models.

### 3.3 Harness Arms And Models

Experiments use harness arms to vary the strength of external control. G0 is raw or minimally constrained task input. G2/G3 represent intermediate mechanism arms when relevant. G8 is contract-rich execution with validator or evaluator obligations. G9 is the full harness packet with task spec, output contract, evidence, memory policy, workflow, trace, and regression expectations.

The real-model slices use SiliconFlow's OpenAI-compatible API. The current low-cost model tier is `Qwen/Qwen3-8B`; strong-model slices in earlier stages used `deepseek-ai/DeepSeek-V3.2`. Provider-backed runs use temperature `0`, fixed prompt artifacts exported before execution, per-run artifact directories, adapter request files, output files, validation reports, metrics files, and event logs for provider start/end, elapsed time, errors, and retry analysis. \cite{P2_EXT_SILICONFLOW_CHAT}

### 3.4 Task Slices, Mechanism Atoms, And Macros

The first empirical layer uses broad task slices to identify where harnessing helps and where broad task definitions become too noisy. Structured extraction tests a high-constraint task with deterministic output structure. Project initialization tests a multi-constraint workspace planning task. Research workflow tests evidence-backed synthesis.

A mechanism atom is the smallest testable unit of harness behavior with one primary mechanism, fixed input, explicit output contract, deterministic evaluator, known-bad rejection, pass threshold, and composition interface. Atoms are accepted only when fixture structure validates, the golden output passes, at least one known-bad output fails for the intended reason, the baseline leaves room for improvement, the low-cost model improves under the relevant harness arm, and the atom declares how it can compose with downstream mechanisms.

Macro tasks are composed only after component mechanisms pass local gates and targeted model checks. A macro must preserve cross-step obligations explicitly. The current admitted macro family is evidence-bound and fixed-input: Stage 7p v2, Stage 7e v1-v4, and Stage 7-next. Project initialization and full research workflow remain blocked because the current evidence covers bounded macros, not open-ended tool-using workflows.

### 3.5 Repair-Loop Protocol

The main methodological contribution is the repair-loop protocol:

1. observe a real model failure;
2. isolate the missing mechanism or obligation;
3. make the obligation explicit in the input and output contract;
4. add or update a known-bad fixture that captures the failure;
5. run local golden/bad regression;
6. execute a targeted real-model slice;
7. update the evidence ledger, claim boundary, and backlog before expanding scope.

Stage 7e illustrates this protocol. Stage 7e v1 found a low-cost-model G9 failure in stage-gate and decision-trace retention. Stage 7e v2 repaired trace/gate retention but exposed unknown-state omissions. Stage 7e v3 repaired unknown-state retention but exposed known-state provenance compression. Stage 7e v4 made known-state provenance explicit and reached 4/4 low-cost-model passes after retry. Stage 7-next then reused those obligations in a method-plan update macro and passed 4/4 low-cost-model runs without provider errors.

### 3.6 Metrics And Claim Rules

Each evaluated run emits metrics including `task_success`, `schema_validity`, `citation_grounding`, `state_accuracy`, `evidence_type_accuracy`, `stage_completion`, `trace_completeness`, `context_relevance`, and `atom_primary_metric`.

Gap compression is computed only where a nonzero G0 baseline gap exists. If G0 baselines collapse for both models, or if the low-cost model improves more than the strong model and reopens the absolute gap in the opposite direction, the result is reported as mixed, undefined, or negative rather than forced into a compression claim.

Weak-model enablement is reported when the low-cost model reaches a pass threshold under a harness condition after failing or underperforming under weaker conditions.

## 4. Results

### 4.1 Overview

The results support a bounded version of the original hypothesis. Contract-rich harnessing improves absolute contract adherence across several productivity-task settings, and it can compress cross-model gaps in highly constrained tasks. However, gap compression is not universal. The stronger and more stable result is weak-model enablement on bounded, contract-critical operations: when task obligations are made explicit and evaluated deterministically, the low-cost model can reach pass-level behavior on tasks where weaker harnessing or broader prompts were unstable.

### 4.2 Task Slices: Strong Absolute Lift, Conditional Gap Compression

The structured-extraction v2 slice is the clearest positive gap-compression result. Under G0, nonzero baseline gaps existed on task success, schema validity, tool-call correctness, human acceptance, cost efficiency, and safety consistency. Under G9, all measured nonzero gaps compressed to 0.000, producing compression ratios of 1.000 on those metrics. Citation grounding had a baseline gap of 0.000 and is therefore reported as n/a rather than as compression.

The project-initialization slice shows why gap compression cannot be the universal claim. G9 compressed the task-success gap from 0.111 to 0.000 and the safety-consistency gap from 0.200 to 0.000. However, schema validity moved from a baseline gap of 0.250 to an arm gap of 0.583, yielding a negative compression ratio of -1.333. Human acceptance and cost efficiency also showed negative compression ratios.

The research-workflow slice further weakens a universal gap-compression story. Several G0 baseline gaps were already 0.000, making compression undefined. G9 compressed schema-validity gap from 0.067 to 0.000, but task-success gap became 0.083 from a 0.000 baseline and human-acceptance/cost-efficiency gap movement was slightly negative.

These results are best interpreted as absolute lift with conditional gap compression, not universal gap closure.

### 4.3 Mechanism Atoms: Broad Workflows Need Smaller Units

The Stage 6 mechanism-atom pilot tested 48 real model runs and completed 48/48 after documented timeout recovery. Its strongest result was weak-model enablement. For the low-cost model relative to G0, G9 produced task_success lift of +0.576 and schema_validity and atom_primary_metric lift of +0.833.

The harnessed low-cost model also outperformed the unconstrained strong model on contract-critical metrics. Relative to strong_model + G0, low-cost model + G9 showed task_success advantage of +0.743 and schema_validity and atom_primary_metric advantages of +1.000.

Gap compression was mostly positive on general contract metrics, including G9 task_success compression of 1.000 and G9 schema_validity compression of 1.000. But atom_primary_metric remained mixed, with G9 compression of 0.000 and G2/G8 negative values. This supports the conclusion that harnesses can substantially raise low-cost-model reliability on bounded operations even when atom-specific gap compression is not uniform.

### 4.4 Composition: Atom Success Is Not Enough

Stage 7p tested whether passing atoms could compose into a narrow partial macro:

```text
A10 bounded context recall -> A9 no-overwrite action planning -> A6 validator repair
```

The execution completed cleanly with 6/6 real SiliconFlow runs. Strong_model G8 and G9 passed the full partial-composition chain. The low-cost model improved strongly under G8/G9, reaching task_success=0.800 under G8 and 0.900 under G9, with schema_validity=1.000 and safety=1.000. Yet it failed the full chain because context_relevance stayed 0.000: the composed output did not explicitly carry forward the stale-context exclusion.

Stage 7p v2 then added an explicit composition-retention contract. The same partial chain passed for both model tiers under G8/G9. This result supports a composition-layer mechanism claim: cross-step obligation retention is necessary when a macro must preserve negative context constraints across multiple atom outputs.

### 4.5 Revised Atoms And Targeted Repairs

Stage 7r redesigned six boundary-prone atoms: A2R, A3R, A4R, A5R, A7R, and A8R. Local gates passed: 6/6 fixture structures, 12/12 local golden/bad expectations, 36/36 packet compilation, and preflight with 0 errors and 0 warnings.

The real-model smoke completed 35/36 outputs. The single missing output was A8R low-cost G8, which repeatedly timed out under SiliconFlow and was treated as an execution deviation rather than a model-quality score. On completed runs, strong-model G8/G9 passed 12/12, while the low-cost model still failed strict A2R citation grounding and A7R trace completeness.

Stage 7r.1 targeted exactly those failures by tightening the contracts. A2R1 required every grounded claim to be an object with non-empty `evidence_ids`. A7R1 required rejected-option objects with evidence IDs and trace steps for C2 support, C1 rejection, and C3 rejection. The targeted 8-run low-cost-model smoke passed 8/8.

This supports the mechanism-first repair hypothesis: low-cost-model failures on claim-level evidence binding and rejection-trace completeness can be repaired by narrowing the output contract.

### 4.6 Stage 7e: Iterative Repair Of A Fixed Evidence-Decision Macro

Stage 7e composed a narrow evidence-bound decision macro from state inventory, evidence grounding, evidence-type separation, traceable decision, and stage-gated synthesis mechanisms. The first Stage 7e smoke completed 6/6 runs. Strong_model G8/G9 and low-cost-model G8 passed with task_success=1.000 and atom_primary_metric=1.000. G0 failed for both model tiers. Low-cost-model G9 partially failed with task_success=0.714 because it missed complete decision-trace and stage-gate retention.

Stage 7e v2 added explicit retention requirements for decision_trace, stage_gate, and carried_obligations. The targeted low-cost-model G8/G9 smoke completed 4/4 runs, and all 4/4 achieved trace_completeness=1.000 and stage_completion=1.000. However, only 1/4 runs fully passed because the remaining runs omitted Git branch, CI status, or network/API approval unknowns from state_inventory.

Stage 7e v3 targeted unknown-state retention. The low-cost-model smoke completed 4/4 runs. All 4/4 preserved the required Git/CI/network unknown-state fields and forbidden-inference fields. Full strict macro pass improved to 3/4. The remaining failure was narrower: one G8 run compressed known-state provenance into generic labels.

Stage 7e v4 made known-state provenance explicit. It required `state_inventory.known_state[]` entries with `state_id`, `fact`, and `evidence_ids`. After retrying one provider timeout and one truncated-output retry, the final evaluation completed 4/4 runs, and all 4/4 passed with task_success=1.000 and atom_primary_metric=1.000. State accuracy, citation grounding, evidence type accuracy, trace completeness, and stage completion all reached 1.000.

This sequence is the clearest evidence for the repair-loop protocol. The low-cost model did not become generally stronger. The harness made the missing obligations explicit, then verified that the model could satisfy them under a fixed macro contract.

### 4.7 Stage 7-next: Transfer To A Neighboring Macro

Stage 7-next tested whether the Stage 7e v4 obligation set was only a fixture-specific patch. The new macro was an evidence-bound method-plan update. It reused Stage 7e v4 obligations and added one new stressor: the output had to select the next admitted macro, specify admission criteria, preserve local and real-model gates, and declare non-claims.

The local gate passed with 2/2 expectations met: the golden output passed with task_success=1.000 and atom_primary_metric=1.000, while the known-bad premature broader-workflow expansion failed with task_success=0.000.

The real smoke used the low-cost model only:

```text
Qwen/Qwen3-8B x G8/G9 x 2 repetitions = 4 runs
```

All 4/4 runs executed without provider errors, timeout, or truncated-output retry. All 4/4 runs passed with task_success=1.000, atom_primary_metric=1.000, schema_validity=1.000, citation_grounding=1.000, state_accuracy=1.000, evidence_type_accuracy=1.000, trace_completeness=1.000, stage_completion=1.000, and context_relevance=1.000.

This supports a narrow transfer claim: the Stage 7e v4 obligations can be reused to make the low-cost model complete a closely related fixed method-plan macro with one new explicit stressor.

## 5. Discussion And Limitations

### 5.1 What The Results Mean

The main finding is not that harnesses make low-cost models equivalent to strong models. The evidence does not support that claim. The main finding is that some agent reliability requirements can be moved out of the model and into explicit contracts. When task state, admissible evidence, output shape, stage gates, trace requirements, and carried obligations are represented as inspectable objects, low-cost models can satisfy bounded tasks that were unstable under weaker or broader prompts.

This changes how we should interpret agent reliability. A model failure is often treated as a limit of model intelligence. Sometimes it is. But in our experiments, several failures were more precisely described as missing contract obligations. The low-cost model did not preserve decision-trace retention until the trace was made structurally required. It did not preserve unknown state until unknown state was enumerated. It compressed known-state provenance until provenance-bearing state objects were required. It failed partial macro composition until cross-step carried obligations were made explicit.

### 5.2 Gap Compression Is Conditional

The original research motivation was model capability gap compression. The results support that idea in structured settings but not as a universal law. Structured extraction produced the clearest compression result because the input, output, and correctness criteria are highly constrained. Project initialization and research workflow produced a more complicated pattern: harnessing improved absolute contract adherence, but gap movement was mixed, undefined, or negative depending on the metric.

This does not weaken the paper if it is framed correctly. It means gap compression is an empirical outcome of a specific task, metric, baseline gap, and harness arm. It should not be the universal thesis. The more stable claim is weak-model enablement: whether the low-cost model reaches a usable contract-adherence threshold under explicit harnessing.

### 5.3 Why Negative Results Matter

Several negative or partial results are central to the argument. Stage 7p v1 showed that passing atoms do not automatically compose. Stage 7r showed that redesigned atoms could improve low-cost-model performance without fully repairing all contract-critical behavior. Stage 7e v2 and v3 also matter because they were not fully successful. They exposed the missing obligations that made Stage 7e v4 meaningful.

In short, the negative results are not noise. They are evidence for the mechanism-first methodology.

### 5.4 Bounded Macros Are Not Full Workflows

The strongest macro results, Stage 7e v4 and Stage 7-next, are fixed-input, no-tool, deterministic tasks. They do not involve live source discovery, file mutation, external tool execution, or changing workspace state. This is a major boundary.

The result should be stated carefully:

> Low-cost models can complete bounded evidence-bound macros when reliability obligations are explicit.

It should not be stated as:

> Low-cost models can reliably run full project initialization or full research workflows.

Full workflows introduce additional problems that the current macros do not test: tool selection, permission handling, filesystem mutation, live source volatility, partial failure recovery, long-horizon memory, user clarification, and multi-step state updates. The current work provides a method for approaching those workflows, not evidence that they are already solved.

### 5.5 Deterministic Evaluation, Sample Size, And Runtime Effects

The evaluation pipeline relies on deterministic evaluators, golden outputs, and known-bad outputs. This is a strength because it makes pass/fail decisions auditable and regression-testable. It also prevents the benchmark from becoming a subjective preference test. But deterministic evaluation narrows what can be claimed. The metrics capture contract adherence, not prose quality, human usefulness, creative insight, or open-ended judgment.

Several later experiments are targeted smoke tests with small run counts. Stage 7e v4 used four low-cost-model runs after retry. Stage 7-next used four low-cost-model runs. These are acceptable for mechanism repair but not for population-level performance estimation.

Provider behavior also affected experiments. Some SiliconFlow runs timed out, and Stage 7e v4 required retrying one timed-out run and one truncated-output retry before completion. Stage 7-next did not require retry and completed 4/4 cleanly. Runtime deviations should be reported as validity threats rather than hidden.

### 5.6 PEtFiSh Specificity And Harness Cost

The fixtures and workflows are grounded in the PEtFiSh project context. This raises external-validity concerns: the exact skills, packs, evidence ledgers, and backlog structures may not generalize to all agent systems. The mitigation is to frame PEtFiSh as the implementation context, not the whole construct. The generic constructs are task specs, bounded memory, evidence bundles, output contracts, workflow gates, trace logs, validators, known-bad cases, and repair loops.

Contract-driven harnessing also adds overhead. It requires fixture design, schemas, evidence bundles, evaluators, local gates, manifests, event logs, and postprocessing. For simple tasks, this overhead may exceed the benefit. There is also a risk of over-constraint: strong models may become more stable but less flexible under strict contracts.

### 5.7 Future Work

The next empirical step is not to claim full project initialization or full research workflow readiness. It is to build the next admitted macro only after identifying the required mechanisms and cross-step obligations. Promising directions include citation-bound synthesis, state-mutating project macros, live research workflow slices, cross-provider replication, and perturbation suites.

## 6. Conclusion

Contract-driven harness engineering can make some low-cost-model failures observable, repairable, and regression-testable by externalizing reliability obligations into explicit contracts. This is not a claim that model quality no longer matters. It is a claim that for bounded productivity tasks, part of agent reliability can be engineered outside the model.

The strongest supported claim is weak-model enablement on bounded contract-critical operations. Gap compression remains important but conditional. It is strongest in structured extraction and present on some contract metrics in mechanism and partial macro tests. It is mixed or undefined in broader project-initialization and research-workflow slices.

The practical value of the method is the repair loop. A harness failure can be turned into a named obligation, a contract revision, a known-bad fixture, a local regression gate, a targeted real-model smoke test, and an updated claim boundary. That loop is the central engineering contribution of this work.

## Appendix A. Current Non-Claims

This paper should not claim:

- low-cost models are generally equivalent to strong models;
- harnessing universally compresses model gaps;
- full project initialization is solved;
- full research workflow is solved;
- the harness is production ready;
- fixed macro success implies open-ended tool-using workflow reliability.

## Appendix B. Contribution-To-Evaluation Alignment

| Contribution | Evaluation support | Boundary |
|---|---|---|
| Contract-driven harness model | Task slices and methods artifacts | Method definition, not a production-readiness claim. |
| Mechanism atoms | Atom definition, coverage framework, Stage 6-7 atom results | Atom pass does not prove workflow pass. |
| Conditional gap compression | Structured extraction, project initialization, research workflow slices | Compression only when baseline gaps are nonzero and gap movement is not reversed. |
| Repair-loop protocol | Stage 7e v1-v4 | Fixed evidence-bound decision macro. |
| Bounded weak-model enablement | Stage 7e v4 and Stage 7-next | Fixed-input, no-tool, deterministic macros. |

## Appendix C. Evidence Traceability Matrix

| Paper claim | Evidence IDs | Source IDs | Status |
|---|---|---|---|
| Contract-rich harnessing improves absolute contract adherence and can compress gaps under constrained conditions. | P2-E28, P2-E30, P2-E32, P2-E33 | P2-SILICONFLOW-V2-FULL24, P2-SILICONFLOW-PROJECT-INIT-12, P2-SILICONFLOW-RESEARCH-WORKFLOW-12, P2-CLAIM-BOUNDARY-MEMO | Supported with conditional wording. |
| Structured extraction is the clearest positive gap-compression task slice. | P2-E27, P2-E28 | P2-SILICONFLOW-V2-FULL24 | Supported for tested SiliconFlow v2 slice. |
| Project initialization and research workflow do not support universal gap compression. | P2-E30, P2-E32, P2-E33 | P2-SILICONFLOW-PROJECT-INIT-12, P2-SILICONFLOW-RESEARCH-WORKFLOW-12, P2-CLAIM-BOUNDARY-MEMO | Supported; use mixed/undefined wording. |
| Mechanism atoms make broad workflow failures interpretable. | P2-E35, P2-E36, P2-E56, P2-E60 | P2-MECHANISM-ATOM-DEFINITION, P2-MECHANISM-ATOM-COVERAGE, P2-STAGE7R-REVISED-ATOMS, P2-STAGE7R1-A2R-A7R-SMOKE | Supported as methodology and targeted empirical repair evidence. |
| Atom success does not automatically imply macro composition success. | P2-E51, P2-E52 | P2-STAGE7P-PARTIAL-COMPOSITION | Supported by Stage 7p v1 failure. |
| Explicit cross-step carried obligations can repair the Stage 7p composition failure. | P2-E53, P2-E54 | P2-STAGE7P-V2-COMPOSITION-RETENTION | Supported for A10 -> A9 -> A6 partial macro. |
| Stage 7r.1 repaired low-cost-model A2R/A7R failures through tighter output contracts. | P2-E57, P2-E58, P2-E59, P2-E60 | P2-STAGE7R1-A2R-A7R-PREP, P2-STAGE7R1-A2R-A7R-SMOKE | Supported for targeted atoms only. |
| Stage 7e v1-v4 demonstrates a repair-loop protocol for a fixed evidence-decision macro. | P2-E62, P2-E64, P2-E66, P2-E68, P2-E69, P2-E70 | P2-STAGE7E-EVIDENCE-DECISION, P2-STAGE7E-V2-RETENTION, P2-STAGE7E-V3-STATE-RETENTION, P2-STAGE7E-V4-KNOWN-STATE-PROVENANCE, P2-CLAIM-BOUNDARY-MEMO | Supported with fixed-input/no-tool boundary. |
| Stage 7-next transfers Stage 7e v4 obligations to a neighboring method-plan macro. | P2-E72, P2-E74, P2-E75 | P2-STAGE7-NEXT-METHOD-PLAN-LOCAL, P2-STAGE7-NEXT-METHOD-PLAN-SMOKE | Supported as narrow transfer evidence. |
| Full project initialization, full research workflow, production readiness, and general model equivalence remain non-claims. | P2-E33, P2-E63, P2-E69, P2-E70, P2-E75 | P2-CLAIM-BOUNDARY-MEMO, P2-STAGE7E-EVIDENCE-DECISION, P2-STAGE7E-V4-KNOWN-STATE-PROVENANCE, P2-STAGE7-NEXT-METHOD-PLAN-SMOKE | Supported as explicit boundary. |
| Related work: orchestration, declarative programs, structured outputs, retrieval/tools, memory, verification, and skill ecosystems are adjacent lines. | P2-E05, P2-E06, P2-E07, P2-E08, P2-E09, P2-E83, P2-E84, P2-E85, P2-E86, P2-E87, P2-E88, P2-E89, P2-E90, P2-E91, P2-E92, P2-E93, P2-E94, P2-E95, P2-E96, P2-E98 | External source IDs listed in `source-index.md` | Supported as background; convert to publication-style citations before submission. |

## Reproducibility Package

This draft is supported by a local reproducibility package under `research/` \cite{P2_LOCAL_ARTIFACTS}. The package includes the source index, evidence ledger, mechanism-atom definitions, macro fixtures, prompt manifests, provider event logs, model-output artifacts, deterministic evaluator outputs, metric summaries, stage reports, citation audit reports, and citation metadata.

The core traceability files are:

- `research/01_sources/source-index.md`
- `research/01_sources/contract-driven-harness-citation-metadata.md`
- `research/03_evidence/evidence-ledger.jsonl`
- `research/06_outputs/contract-driven-harness-compact-results-appendix.md`
- `research/07_reviews/contract-driven-harness-citation-audit.md`
- `research/07_reviews/contract-driven-harness-source-coverage.md`
- `research/07_reviews/contract-driven-harness-unsupported-claims.md`

External references are prepared in `research/06_outputs/contract-driven-harness-references.bib`. Local empirical claims should be checked against Appendix C and the evidence ledger rather than treated as ordinary literature citations.

## Bibliography

The BibTeX bibliography for this working draft is maintained in `research/06_outputs/contract-driven-harness-references.bib`.

For arXiv preparation, compile this manuscript with that BibTeX file and keep Appendix C as the evidence traceability layer. For ACM or IEEE submission, move most local evidence IDs to supplementary material and cite the local artifact bundle as a reproducibility package.
