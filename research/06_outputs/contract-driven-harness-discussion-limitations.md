# Discussion And Limitations

## 1. What The Results Mean

The main finding is not that harnesses make low-cost models equivalent to strong models. The evidence does not support that claim. The main finding is that some agent reliability requirements can be moved out of the model and into explicit contracts. When task state, admissible evidence, output shape, stage gates, trace requirements, and carried obligations are represented as inspectable objects, low-cost models can satisfy bounded tasks that were unstable under weaker or broader prompts.

This changes how we should interpret agent reliability. A model failure is often treated as a limit of model intelligence. Sometimes it is. But in our experiments, several failures were more precisely described as missing contract obligations. The low-cost model did not preserve decision-trace retention until the trace was made structurally required. It did not preserve unknown state until unknown state was enumerated. It compressed known-state provenance until provenance-bearing state objects were required. It failed partial macro composition until cross-step carried obligations were made explicit. These are not examples of the model suddenly becoming generally smarter. They are examples of reliability being externalized.

The strongest methodological contribution is therefore the repair loop. Instead of responding to a failure by writing a larger prompt or switching immediately to a stronger model, the repair loop asks what obligation was missing, how it can be represented, how a known-bad case can capture the failure, and whether a targeted real-model run verifies the repair. This makes harness engineering more like regression-driven systems work than prompt iteration.

## 2. Gap Compression Is Conditional

The original research motivation was model capability gap compression. The results support that idea in structured settings but not as a universal law.

Structured extraction produced the clearest compression result: all measured nonzero G0 gaps compressed to zero under G9. This is the task class where the harness has the most leverage because the input, output, and correctness criteria are highly constrained.

Project initialization and research workflow produced a more complicated pattern. Harnessing improved absolute contract adherence, but gap movement was mixed, undefined, or negative depending on the metric. In project initialization, task success and safety consistency compressed, while schema validity and human-acceptance-related metrics moved negatively. In research workflow, some baseline gaps were zero, making compression undefined, while schema validity improved.

This does not weaken the paper if it is framed correctly. It means gap compression is an empirical outcome of a specific task, metric, baseline gap, and harness arm. It should not be the universal thesis. The more stable claim is weak-model enablement: whether the low-cost model reaches a usable contract-adherence threshold under explicit harnessing.

## 3. Why Negative Results Matter

Several negative or partial results are central to the argument.

Stage 7p v1 showed that passing atoms do not automatically compose. The low-cost model had access to the stale-context exclusion, but did not carry it into the composed output. This failure identified cross-step obligation retention as a separate composition-layer mechanism. Without that failure, we might have incorrectly claimed that atom success was enough for macro reliability.

Stage 7r showed that redesigned atoms could improve low-cost-model performance without fully repairing all contract-critical behavior. A2R and A7R still failed for claim-level evidence binding and rejection-trace completeness. Stage 7r.1 then repaired those exact failures through tighter contracts. This sequence matters because it demonstrates that the method can identify and target specific weak-model failure modes.

Stage 7e v2 and v3 also matter because they were not fully successful. v2 repaired trace and stage-gate retention but exposed state-inventory omissions. v3 repaired unknown-state retention but exposed known-state provenance compression. These failures made the final v4 result more meaningful: the v4 success was not a one-step success story but the result of progressively making hidden obligations explicit.

In short, the negative results are not noise. They are evidence for the mechanism-first methodology.

## 4. Bounded Macros Are Not Full Workflows

The strongest macro results, Stage 7e v4 and Stage 7-next, are fixed-input, no-tool, deterministic tasks. They do not involve live source discovery, file mutation, external tool execution, or changing workspace state. This is a major boundary.

The result should therefore be stated carefully:

> Low-cost models can complete bounded evidence-bound macros when reliability obligations are explicit.

It should not be stated as:

> Low-cost models can reliably run full project initialization or full research workflows.

Full workflows introduce additional problems that the current macros do not test: tool selection, permission handling, filesystem mutation, live source volatility, partial failure recovery, long-horizon memory, user clarification, and multi-step state updates. The current work provides a method for approaching those workflows, not evidence that they are already solved.

## 5. Deterministic Evaluation Is A Strength And A Limitation

The evaluation pipeline relies on deterministic evaluators, golden outputs, and known-bad outputs. This is a strength because it makes pass/fail decisions auditable and regression-testable. It also prevents the benchmark from becoming a subjective preference test.

But deterministic evaluation narrows what can be claimed. The metrics capture contract adherence: schema validity, evidence grounding, state accuracy, evidence typing, trace completeness, stage completion, context relevance, and strict primary pass. They do not fully capture prose quality, human usefulness, creative insight, or open-ended judgment. A model can pass a contract-bound macro while still being less capable in a broader sense.

This is why the paper should not claim general intelligence parity. It should claim contract-critical reliability under defined evaluators.

## 6. Small Samples And Smoke Tests

Several later experiments are targeted smoke tests with small run counts. Stage 7e v4 used four low-cost-model runs after retry. Stage 7-next used four low-cost-model runs. These are not large-scale statistical benchmarks.

The small samples are acceptable for the current claim because the purpose is mechanism repair, not population-level performance estimation. Each smoke test asks whether a specific contract repair works under a fixed input and deterministic evaluator. However, larger studies are needed before claiming stability across task distributions, providers, model families, prompt perturbations, or real workflows.

Future work should add:

- more repetitions,
- more low-cost model families,
- noisy and adversarial variants,
- live-tool workflow tests,
- confidence intervals or effect-size reporting,
- cross-provider replication.

## 7. Provider And Runtime Effects

Provider behavior affected several experiments. Some SiliconFlow runs timed out, and Stage 7e v4 required retrying one timed-out run and one truncated-output retry before completion. Stage 7-next did not require retry and completed 4/4 cleanly.

The study records provider event logs so runtime deviations can be separated from model-quality failures. This distinction is important. A read timeout is not the same as a contract failure. At the same time, provider stability is part of real harness operation. A production harness would need retry policies, output truncation detection, cost controls, and provider fallback strategies.

Thus provider instability is both an experimental nuisance and a real operational concern. It should be reported as a validity threat rather than hidden.

## 8. PEtFiSh Specificity

The fixtures and workflows are grounded in the PEtFiSh project context. This raises external-validity concerns: the exact skills, packs, evidence ledgers, and backlog structures may not generalize to all agent systems.

The mitigation is to frame PEtFiSh as the implementation context, not the whole construct. The generic constructs are task specs, bounded memory, evidence bundles, output contracts, workflow gates, trace logs, validators, known-bad cases, and repair loops. Other agent systems can implement these constructs differently.

The paper should therefore avoid saying that PEtFiSh-specific fixtures prove general agent reliability. It can say that PEtFiSh provides a concrete artifact for studying contract-driven harness mechanisms.

## 9. Harness Cost And Over-Constraint

Contract-driven harnessing adds overhead. It requires fixture design, schemas, evidence bundles, evaluators, local gates, manifests, event logs, and postprocessing. For simple tasks, this overhead may exceed the benefit.

There is also a risk of over-constraint. Strong models may become more stable but less flexible under strict contracts. Some tasks benefit from exploration, ambiguity handling, or creative synthesis. A full harness is not always the right mode.

This suggests a practical design principle:

> Harness strength should match task regulability.

Highly structured extraction can use strict contracts. Bounded evidence decisions can use deterministic gates. Open-ended research or design work may need advisory harnessing, human checkpoints, and softer evaluation rather than full deterministic closure.

## 10. Implications For Agent Engineering

The results suggest that agent reliability should be developed through mechanism coverage, not prompt accumulation. A harness should ask:

- What obligation must survive from input to output?
- What state is known, unknown, or forbidden to infer?
- Which claims require evidence?
- Which stage gates prevent premature finalization?
- Which negative obligations must be carried across steps?
- What known-bad output proves the evaluator can catch the failure?

This is a different engineering posture from writing a better instruction. It treats the model as one component inside a contract system.

## 11. Future Work

The next empirical step is not to claim full project initialization or full research workflow readiness. It is to build the next admitted macro only after identifying the required mechanisms and cross-step obligations.

Promising directions:

1. Citation-bound synthesis macro: compose evidence selection, evidence typing, claim grounding, stale-context exclusion, and bounded recommendation.
2. State-mutating project macro: add controlled filesystem/tool state changes with no-overwrite guarantees and rollback-aware reporting.
3. Live research workflow slice: separate source discovery, access audit, note capture, evidence ledger construction, synthesis, and report writing into explicit state transitions.
4. Cross-provider replication: rerun Stage 7e and Stage 7-next on another low-cost model/provider pair.
5. Perturbation suite: add noisy and adversarial variants to test whether repaired obligations survive distractors.

## 12. Final Interpretation

The paper's central claim should be modest but valuable:

> Contract-driven harness engineering can make some low-cost-model failures observable, repairable, and regression-testable by externalizing reliability obligations into explicit contracts.

This is not a claim that model quality no longer matters. It is a claim that for bounded productivity tasks, part of agent reliability can be engineered outside the model. That is enough to make the method useful, and it is also the boundary that keeps the paper scientifically honest.
