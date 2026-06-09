# Contract-Driven Harness Paper Front Matter

## Title Candidates

1. Contract-Driven Harness Engineering for Reliable Low-Cost Agent Tasks
2. From Prompting to Contracts: Mechanism-First Evaluation of Agent Harness Reliability
3. Externalizing Reliability: Contract-Driven Harnesses for Bounded Agent Workflows
4. Can Agent Harnesses Enable Low-Cost Models on Contract-Critical Tasks?

Working title:

> Contract-Driven Harness Engineering for Reliable Low-Cost Agent Tasks

## Abstract Seed

AI agent reliability is often framed as a property of the underlying language model: stronger models are expected to plan better, follow constraints more reliably, and recover from ambiguous context more effectively. This framing is incomplete for productivity tasks that can be bounded by explicit inputs, evidence, state, workflow stages, and output contracts. We study contract-driven harness engineering: a reliability layer that externalizes task obligations into task specifications, bounded memory slices, evidence bundles, output contracts, validation gates, and trace requirements. Across structured extraction, project initialization, research workflow, mechanism-atom, and admitted-macro experiments, we find that harnessing improves absolute contract adherence and can compress model gaps when baseline gaps are nonzero and the task is highly constrained. However, gap compression is not universal. The more stable result is weak-model enablement on bounded, contract-critical operations. In a Stage 7e repair loop, successive explicit contracts repaired low-cost-model failures in decision trace retention, stage-gate retention, unknown-state preservation, and known-state provenance, culminating in 4/4 low-cost-model passes on a fixed evidence-bound decision macro. A neighboring Stage 7-next method-plan macro reused these obligations and also passed 4/4 low-cost-model runs. These results support a mechanism-first methodology for agent harness evaluation: broad workflows should be decomposed into testable mechanisms, locally validated against golden and known-bad cases, and admitted to macro composition only when their obligations are explicit. The current evidence does not establish production readiness or full open-ended workflow reliability; it shows that contract-driven harnesses can turn some low-cost-model failures into observable, repairable, and regression-testable engineering objects.

## Introduction

AI agent systems are increasingly asked to perform productivity work: initialize projects, extract structured information, synthesize evidence, prepare plans, update documents, and coordinate multi-step workflows. In these settings, reliability is often treated as a direct consequence of model capability. If an agent fails to preserve constraints, cite evidence, follow stages, or avoid stale context, the usual explanation is that the underlying model is not strong enough.

That explanation is partly true, but it is incomplete. Many productivity tasks are not open-ended intelligence tests. They contain obligations that can be stated explicitly: which evidence may be used, which state is known or unknown, which actions are blocked, which fields must be present, which claims require citations, and which stage gate prevents a final recommendation. When these obligations remain implicit, the model must infer and retain them through free generation. When they are externalized into contracts, some of the burden shifts from model intelligence to system design.

This paper studies that shift. We call the approach contract-driven harness engineering: the use of explicit task specifications, bounded memory, evidence bundles, output contracts, workflow gates, validators, and trace requirements to constrain agent behavior. The central question is not whether low-cost models are generally equivalent to strong models. They are not. The question is which parts of agent reliability can be made less dependent on unconstrained model behavior by turning task obligations into inspectable and testable control objects.

The initial thesis of this project was model capability gap compression: a stable harness may reduce the performance gap between strong and low-cost models. Our results support this thesis only under specific conditions. In highly structured extraction tasks, stronger harnessing compressed measured nonzero baseline gaps. In broader project-initialization and research-workflow slices, harnessing improved absolute contract adherence but produced mixed or undefined gap movement. These broader slices revealed a methodological problem: a workflow-level task can hide many mechanisms at once, making it difficult to know whether a result reflects schema following, state retention, evidence grounding, stage discipline, trace completeness, or some interaction among them.

We therefore moved from workflow-first evaluation to mechanism-first evaluation. A mechanism atom is a fixed-input, deterministic, contract-bound operation with one primary mechanism, one dominant failure mode, a golden output, a known-bad output, and a composition interface. Mechanism atoms let us ask smaller questions: Does an explicit evidence bundle improve claim grounding? Does a memory slice prevent state hallucination? Does a stage gate prevent premature recommendation? Does a trace requirement make rejected options auditable? Passing atoms do not prove that a whole workflow is solved, but they make workflow composition interpretable.

The strongest evidence in this study comes from the repair loop created after broad workflow tests exposed unstable behavior. In Stage 7e, we composed a narrow evidence-bound decision macro from state inventory, evidence grounding, evidence typing, traceable decision, and stage-gated synthesis mechanisms. The first version showed that a low-cost model could pass under one harness arm but still lose decision-trace and stage-gate obligations under another. Rather than broadening the benchmark, we isolated the miss and revised the contract. Stage 7e v2 repaired trace and gate retention, but exposed unknown-state omissions. Stage 7e v3 repaired unknown-state retention, but exposed known-state provenance compression. Stage 7e v4 made known-state provenance explicit and reached 4/4 low-cost-model passes after retry.

We then tested whether this was merely a one-fixture patch. Stage 7-next reused the Stage 7e v4 obligations in a neighboring evidence-bound method-plan update macro, adding one new stressor: the output had to select the next admitted macro, list admission criteria, preserve local and real-model gates, and declare non-claims. The low-cost model passed 4/4 SiliconFlow runs under G8/G9, with all runs scoring 1.000 on task success and the strict primary macro metric. This does not establish open-ended workflow reliability. It does show that a repaired obligation set can transfer to a closely related bounded macro.

These findings motivate a narrower and stronger claim than the original gap-compression thesis. Contract-driven harnesses do not make weak models generally equivalent to strong models, and they do not guarantee gap compression. They can, however, raise the usable floor of low-cost models on bounded, contract-critical operations. More importantly, they turn some failures into engineering objects: a missing obligation can be named, added to the contract, captured as a known-bad case, checked locally, rerun against a model, and carried into the evidence ledger and claim boundary.

This reframes agent reliability as a systems problem. The model remains important, especially for open-ended reasoning, ambiguous goals, and exception recovery. But for task regions where inputs, evidence, state, outputs, and gates can be specified, reliability can be partially externalized. The contribution of a harness is not simply that it prompts better. It changes what has to live inside the model.

## Contributions

This paper makes five contributions.

First, we define contract-driven harness engineering as an explicit reliability layer for agent tasks. The method represents task obligations as task specifications, memory slices, evidence bundles, output contracts, workflow gates, validators, and trace requirements. This framing separates harness reliability from unconstrained model ability.

Second, we propose mechanism atoms as the unit of harness evaluation. Instead of treating project initialization or research workflow as primitive benchmarks, we decompose broad workflows into fixed-input, deterministic, contract-bound mechanisms with golden outputs, known-bad outputs, pass thresholds, and composition interfaces.

Third, we report a multi-stage empirical evaluation across task slices, mechanism atoms, and admitted macros. The results show strong gap compression in structured extraction, mixed or undefined gap movement in broader task slices, and stronger evidence for absolute contract-adherence lift and weak-model enablement.

Fourth, we introduce a repair-loop protocol for harness development. The protocol observes a model failure, isolates the missing obligation, makes it explicit in the contract, validates the fix against golden and known-bad outputs, reruns a targeted real-model slice, and updates the claim boundary before expanding scope.

Fifth, we provide bounded evidence that low-cost models can become reliable on fixed, contract-critical macros. Stage 7e v4 achieved 4/4 low-cost-model passes on an evidence-bound decision macro after explicit state, evidence, trace, gate, and provenance obligations were added. Stage 7-next transferred those obligations to a neighboring method-plan update macro and also achieved 4/4 low-cost-model passes.

## Contribution-To-Evaluation Alignment

| Contribution | Evaluation support | Boundary |
|---|---|---|
| Contract-driven harness model | Task slices and methods artifacts | Method definition, not a production-readiness claim |
| Mechanism atoms | Atom definition, coverage framework, Stage 6-7 atom results | Atom pass does not prove workflow pass |
| Conditional gap compression | Structured extraction, project initialization, research workflow slices | Compression only when baseline gaps are nonzero and gap movement is not reversed |
| Repair-loop protocol | Stage 7e v1-v4 | Fixed evidence-bound decision macro |
| Bounded weak-model enablement | Stage 7e v4 and Stage 7-next | Fixed-input, no-tool, deterministic macros |

## Current Non-Claims

This paper should not claim:

- low-cost models are generally equivalent to strong models;
- harnessing universally compresses model gaps;
- full project initialization is solved;
- full research workflow is solved;
- the harness is production ready;
- fixed macro success implies open-ended tool-using workflow reliability.

The intended claim is narrower:

> Contract-driven harness engineering can externalize specific reliability obligations and enable low-cost models on bounded, contract-critical agent tasks; gap compression is an important but conditional outcome, not the universal thesis.
