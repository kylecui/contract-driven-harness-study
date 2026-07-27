# Essence Reframe + Scope-Limit Paragraphs

**Purpose**: Ready-to-insert prose for the v5 paper draft. Implements plan v2.1 WP1 subtask 1 + P1 patch (scope-limit).
**Status**: DRAFT — author reviews before insertion into `contract-driven-harness-arxiv-v5-draft.md`.

---

## Refined main thesis (Essence reframe)

The contract-driven-harness approach rests on a single empirical observation: the binding constraint on bounded LLM-agent determinism is the completeness of an explicit contract, not the intelligence of the model. Across the studied task family, every instance of "model failure" we isolated was, on inspection, a missing obligation whose absence the model could not infer from implicit convention. Once those obligations were externalized into the contract stack and captured as known-bad fixtures, the same model — without retraining, prompt-tuning, or parameter adjustment — produced strict-conforming output on every fresh run.

This reframes the reliability question. The 0/40 → 40/40 trajectory observed during repair-loop iterations is not a story about a model being "fixed"; the model did not change. It is a story about how much implicit obligation was hiding in unwritten conventions, and how that obligation can be surfaced, named, and captured as a regression-testable asset. The contract stack, not the model, is the load-bearing structure.

## P1 patch — mandatory scope-limit (must appear in abstract and §1)

**Abstract (second sentence, immediately after the binding-constraint claim)**:

> This claim is grounded in a single task family — controlled state mutation under a frozen G9 protocol — and five model configurations. We do not claim that completeness is universally the binding constraint across all agentic tasks, nor that the contract stack alone explains variance in settings involving tool use, open-ended planning, or live retrieval. The contribution is the methodology (contract stack + repair-loop + known-bad regression) and the empirical demonstration within the studied scope; generalization beyond this scope is left to future work.

**§1 Introduction (scope-limit paragraph, after the contributions list)**:

> The contributions of this paper are scoped. Empirically, all results come from one task family (controlled state mutation), one provider (SiliconFlow), and a small set of model configurations (Qwen3-8B as the primary low-cost model, with auxiliary confirmation on GLM-4-9B, Qwen3-14B, DeepSeek-V3.2, and Qwen2.5-7B). Methodologically, the contract stack and repair-loop are presented as a methodology for bounded contract-critical operations; we explicitly do not claim that completeness is the binding constraint in unbounded settings, nor that the contract stack alone explains determinism in tasks involving tool use, open-ended planning, or live retrieval. Whenever the phrase "binding constraint" appears in subsequent chapters, it should be read as scoped to the studied task family.

## Why the scope-limit is mandatory (not optional)

The reframe upgrades the rhetorical claim from "repair-loop improves contract quality" (v1's framing) to "completeness is the binding constraint on bounded LLM-agent determinism" (v2's framing). The upgrade is supported by the data only within the studied task family. The data do not isolate completeness from co-varying factors (prompt engineering, evaluator strictness, known-bad set evolution, task-family specifics). Without explicit scope-limiting in the abstract and §1:

- Reviewers will read "binding constraint" as a universal claim and demand evidence from other task families.
- The reframe becomes an attack surface rather than a contribution.
- The paper trades v1's empirical over-claim for a new reframe-level over-claim.

With scope-limiting, "binding constraint" is honest: it is the binding constraint *in the studied scope*, and the methodology (not the universal claim) is the contribution.

## Suggested Abstract (rewrite integrating reframe + scope-limit)

> Contract-driven harnesses make low-cost language-model agents inspectable on bounded tasks by externalizing obligations into an explicit contract stack: task specifications, bounded memory, evidence bundles, output contracts, stage gates, execution traces, and deterministic validators. We show that in the studied task family — controlled state mutation under a frozen protocol — the binding constraint on agent determinism is the completeness of this contract, not the intelligence of the model: across five model configurations, a frozen contract produced 40/40 strict-conforming runs on above-floor models and 0/40 on a below-floor model, with the same model moving from 0/40 to 40/40 over four repair-loop iterations without retraining or prompt-tuning. This claim is grounded in a single task family and five model configurations; we do not claim universality. The contributions are the methodology (contract stack, repair-loop protocol, fixture-driven admission, model-admission probes) and an empirical demonstration that reliability can be accumulated as a regression-testable asset rather than re-derived per prompt. We release the framework-agnostic reference core (320 lines), ContractBench-v1 (task family and evaluator release), and the contract evolution ledger as reproducibility artifacts.

## Suggested Title (per Essence + P2 patch)

**Current V4 title**: `Contract-Driven Harness Engineering for Reliable Low-Cost Agent Tasks`

**v5 candidate A** (Essence-aligned, mentions the reframe):
> `Contracts as Task Skeleton: Externalizing Implicit Obligations for Bounded LLM-Agent Determinism`

**v5 candidate B** (more conservative, keeps the harness framing):
> `Contract-Driven Harness Engineering: A Mechanism-First Case Study on Bounded LLM-Agent Determinism`

**Recommendation**: Candidate A if the venue tolerates conceptual titles; Candidate B for SE venues expecting methodological framing. Author decides after D4 (venue) is locked.

## What changes in the body

The reframe affects how the *same evidence* is presented, not the evidence itself:

| V4 framing | V5 reframing |
|---|---|
| "Weak-model enablement" as headline | "Contract completeness as binding constraint" as headline; weak-model enablement as corollary |
| Repair-loop as engineering protocol | Repair-loop as a process for externalizing implicit obligation |
| 40/40 as the result | 0/40 → 40/40 as the result (the trajectory is the contribution, not the endpoint) |
| "Maintained strict contract adherence" | "Repair-loop iterations externalize obligation; the repaired contract enables strict adherence" |
| Interchangeability as one section (§4.11) | Interchangeability as the natural corollary of "contract captures task structure" |

The data is identical; the narrative emphasis shifts to make the most defensible and publishable claim visible.
