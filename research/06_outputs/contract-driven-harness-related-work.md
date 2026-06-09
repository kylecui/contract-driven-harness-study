# Related Work: Contract-Driven Harness Engineering

## 1. Scope

This related work positions contract-driven harness engineering at the intersection of agent orchestration, declarative LM programming, structured output constraints, retrieval and tool augmentation, memory systems, safety verification, and skill or capability ecosystems.

The relevant prior work is not a single line of papers. It is a convergence across systems that move reliability obligations out of a model's implicit free-form generation and into explicit runtime, specification, tool, memory, validation, and evaluation layers. This paper's claim is narrower than most general agent-reliability claims: it asks whether those externalized obligations can make low-cost models reliable on bounded, contract-critical operations.

## 2. Agent Workflows And Orchestration

Recent agent engineering guidance distinguishes between fully autonomous agents and workflows whose control paths are explicitly defined. Anthropic's discussion of effective agents is important for this distinction: workflows are appropriate when tasks can be decomposed into predictable steps, while agents are reserved for cases that require open-ended model autonomy. LangGraph, AutoGen, Semantic Kernel, and related orchestration frameworks make a similar engineering move by exposing execution state, graph structure, persistence, human-in-the-loop intervention, tool calls, and observability as system concerns rather than leaving them solely inside a prompt.

These systems solve an important class of production problems: they make execution durable, inspectable, and easier to integrate with tools and humans. However, orchestration frameworks alone do not answer the evaluation question addressed in this paper. A workflow graph can still contain under-specified obligations. It can route steps correctly while losing evidence provenance, collapsing unknown state, skipping stage gates, or producing an ungrounded final recommendation.

Contract-driven harness engineering overlaps with workflow orchestration but treats the graph as only one layer. The unit of interest is the obligation that must survive the graph: state inventory, evidence binding, evidence type separation, trace completeness, stage-gate retention, excluded-context preservation, and repairability. The Stage 7p failure is an example of this distinction. The macro chain had a reasonable structure, but the low-cost model failed to retain a stale-context exclusion until the composition contract made that obligation explicit.

## 3. Declarative LM Programs And Agent Specifications

Declarative LM programming systems, especially DSPy, argue that language model behavior should be represented as programs with signatures, modules, metrics, and optimizers rather than as hand-written prompts. Agent specification work such as AgentSPEX and AgentSpec pushes in a related direction for agent systems: workflows, state, steps, and interfaces should be declared in portable and inspectable forms.

This line of work is close to the method proposed here. Both assume that some reliability gains come from making task structure explicit. The difference is the evaluation target. Declarative systems often emphasize program optimization, portability, or agent specification. This paper emphasizes mechanism-first empirical repair: define one contract-critical mechanism, create golden and known-bad outputs, run deterministic local gates, execute small real-model slices, and update the claim boundary before composing broader workflows.

In this framing, a mechanism atom is not just a small task. It is a minimal testable unit with a primary mechanism, fixed input, output contract, deterministic evaluator, pass threshold, and composition interface. This differs from broad benchmark tasks because it makes failures interpretable. If an atom fails, the missing obligation can be named and repaired. If a macro fails, the repair process asks which atom-level obligation did not survive composition.

## 4. Structured Outputs, Guardrails, And Validators

Structured output systems and guardrail frameworks externalize output form. OpenAI structured output mechanisms, Outlines-style constrained generation, and Guardrails validators all reduce the burden of asking a model to "please follow the format." They make schema adherence and selected validation checks part of the system layer.

These mechanisms are necessary but insufficient for the problem studied here. Schema validity can guarantee that an output has the expected shape, but it cannot by itself guarantee that a claim is supported, that unknown state remains unknown, that excluded context is not reused, or that a recommendation is blocked when a stage gate is incomplete. The early structured-extraction slice in this project showed strong measured gap compression under a contract-rich harness, but the broader project-initialization and research-workflow slices showed that format control alone does not explain reliability.

The harness studied here therefore treats validators as one component in a larger contract stack. The output contract includes fields, but also semantic obligations: required evidence IDs, evidence type separation, rejected-option traces, explicit blocked outputs, and non-claims. The evaluator checks whether those obligations are present, not merely whether JSON parses.

## 5. Retrieval, Tools, And Externalized Capability

RAG, ReAct, Toolformer, Gorilla, and tool/API-focused agent work show that models can become more capable when knowledge and action are externalized. Retrieval can provide updated evidence and provenance. Tool-use frameworks can turn external actions into typed calls. API benchmarks show that tool descriptions and retrieval can materially improve call generation compared with unaided model behavior.

These works support the broader premise behind harness engineering: some weaknesses of a model can be reduced by moving facts, actions, and interfaces into external systems. However, this paper does not primarily study live retrieval or tool execution. Most admitted mechanism atoms and macros are fixed-input, no-tool tasks. That design is deliberate. It isolates whether the model can honor explicit contracts before adding live tools, changing corpora, or runtime side effects.

The implication is that tool and retrieval systems are likely future composition layers, not evidence already established by the current experiments. Full research workflow and full project initialization remain blocked because open-ended source discovery, tool choice, execution failures, and live state changes introduce mechanisms that have not yet passed the same contract-bound evaluation pipeline.

## 6. Memory And Context Governance

Memory-oriented systems such as MemGPT and Letta show that agents can use hierarchical, archival, or stateful memory to extend beyond a single context window. They also expose a reliability problem that is central to this paper: memory is not automatically beneficial. A system must decide what to store, when to summarize, how to retrieve, how to scope memory, and how to prevent stale or irrelevant context from contaminating a new task.

Contract-driven harness engineering treats memory as a governed state object rather than as background context. A bounded memory slice can specify known state, unknown state, excluded context, provenance, and forbidden inferences. Stage 7e v2 and v3 illustrate why this matters. Low-cost-model failures were not caused by absence of a broad memory system; they were caused by missing retention obligations for unknown state. Stage 7e v4 then showed that even known state needed explicit provenance requirements to prevent compression into vague labels.

This connects memory research to evaluation discipline. The question is not only whether memory expands context capacity. It is whether memory obligations can be represented, checked, and carried through a multi-step output.

## 7. Agent Evaluation, Safety, And Verification

Agent evaluation and safety work highlights the fragility of agent claims. OAgents-style critiques emphasize protocol variance and reproducibility challenges. Semantic Integrity Constraints, Agentproof, LlamaFirewall, and related verification or guardrail systems argue that agent behavior must be constrained, audited, or checked against explicit policies and semantic rules.

This paper shares that concern but applies it to a narrower empirical question: can reliability obligations be made local enough to test and repair? The evaluation design uses fixed manifests, local golden and known-bad cases, deterministic evaluators, event logs, and evidence ledger entries. Provider timeouts, truncated outputs, and missing runs are treated as execution deviations rather than silently mixed with model-quality scores.

The repair-loop protocol is also a response to evaluation fragility. Instead of treating a failed broad workflow as a vague negative result, the protocol converts a failure into a contract revision and a regression case. This does not remove all validity threats. It does make the claim boundary more explicit: a passing bounded macro does not imply production readiness, live tool reliability, or general model equivalence.

## 8. Skill And Capability Ecosystems

Capability ecosystems such as MCP servers, agent skills, registries, pack systems, and PEtFiSh-style skill markets represent another route toward harness engineering. They externalize reusable procedures, tool access, installation state, platform routing, quality gates, and capability discovery. In PEtFiSh specifically, packs, skills, MCP servers, installers, trigger evaluators, quality gates, and context plugins make the system a useful experimental setting for studying harness design as an engineering object.

The present work should not be read as a claim that PEtFiSh itself is production ready or that any skill ecosystem automatically improves model behavior. Instead, PEtFiSh provides a concrete context where harness obligations can be named and tested: routing rules, output contracts, evidence ledgers, installation status, context state, and quality gates can be represented as artifacts rather than only as conversational conventions.

The broader contribution is methodological. Skill ecosystems make capability reuse possible, but reuse becomes reliable only when each capability has an explicit contract, local checks, real-model smoke evidence, and a claim boundary that prevents a narrow pass from being generalized too far.

## 9. Synthesis

Prior work already supports the components of harness engineering: orchestration runtimes make execution explicit, declarative LM programs make pipelines inspectable, structured output systems make formats enforceable, retrieval and tools externalize knowledge and action, memory systems externalize state, and safety or verification systems externalize constraints.

What remains under-tested is the mechanism-level question studied here: which explicit obligations actually let a low-cost model complete bounded contract-critical operations, and how should a harness be repaired when those obligations fail? This paper contributes a mechanism-first evaluation and repair-loop methodology for that question.

The central boundary follows directly from the related work. Harnesses reduce some dependence on model ability when tasks are specifiable, evidence-bound, state-bound, and externally checkable. They do not eliminate model ability as a variable in open-ended planning, ambiguous semantic judgment, live tool use, adversarial contexts, or broad workflow composition.

## 10. Citation Coverage Audit

| Source ID | Covered? | Section | Notes |
|---|---:|---|---|
| P2-LOCAL-SURVEY | Yes | All | Used as the existing project survey organizing the related-work landscape. |
| P2-LOCAL-PETFISH | Yes | 8 | Used for PEtFiSh-specific positioning as an experimental harness setting. |
| P2-EXT-ANTHROPIC | Yes | 2, 5, 9 | Used for workflow vs agent and augmented LLM framing. |
| P2-EXT-LANGGRAPH | Yes | 2, 9 | Used for orchestration runtime framing. |
| P2-EXT-DSPY | Yes | 3, 9 | Used for declarative LM program framing. |
| P2-EXT-AGENTSPEX | Yes | 3, 9 | Used for explicit agent specification framing. |
| P2-EXT-AGENTSPEC | Yes | 3 | Used for portable declarative agent specification framing. |
| P2-EXT-GUARDRAILS | Yes | 4, 7, 9 | Used for validators and quality-control framing. |
| P2-EXT-OPENAI-MODELS | No | Experimental setup | Provider/model documentation belongs in methods, not related work. |
| P2-EXT-SILICONFLOW-CHAT | No | Experimental setup | Provider/model documentation belongs in methods, not related work. |
| P2-MECHANISM-ATOM-DEFINITION | Yes | 3 | Used to define mechanism atoms as testable units. |
| P2-MECHANISM-ATOM-COVERAGE | Yes | 3, 9 | Used to connect mechanism coverage to composition. |
| P2-STAGE7E-V4-KNOWN-STATE-PROVENANCE | Yes | 6, 7 | Used as the strongest repair-loop case. |
| P2-STAGE7-NEXT-METHOD-PLAN-SMOKE | Yes | 7, 9 | Used as narrow transfer evidence. |
