# Contract-Driven Harness Methodology Outline

## Working Title

Contract-Driven Harness Engineering: Mechanism-First Evaluation for Reliable Low-Cost Agent Tasks

## Research Question

Can explicit task contracts, state inventories, evidence ledgers, output schemas, validators, and stage gates improve agent reliability and reduce dependence on strong models?

The current answer is bounded:

- Yes, for structured extraction and fixed evidence-decision macros under deterministic evaluation.
- Partially, for broader project initialization and research-workflow slices.
- Not yet established, for full open-ended workflows, tool use, or production readiness.

## Contributions

1. A contract-driven harness model that treats prompts, state, evidence, memory policy, output contracts, and validators as explicit control objects.
2. A mechanism-atom methodology for replacing vague workflow tests with minimal, testable obligations.
3. A weak-model enablement metric: whether a low-cost model reaches a pass threshold under an explicit harness, especially when the unconstrained baseline fails.
4. A repair-loop protocol: observe failure, isolate mechanism, strengthen contract, validate local golden/bad cases, run a targeted real-model slice, then update claim boundaries.
5. A bounded empirical case study across task slices and Stage 7e v1-v4 mechanism composition.

## Evidence Spine

| Evidence block | Main result | Claim boundary |
|---|---|---|
| Structured extraction v2 | G9 compressed all measured nonzero G0 gaps to 0 across 24 runs | Standardized structured extraction only |
| Project initialization | G9 improved task success and safety consistency but showed mixed schema-gap movement | Broad initialization remains unstable |
| Research workflow | G9 improved absolute quality, citation grounding, and schema validity | Gap metrics mixed or n/a under collapsed G0 baselines |
| Stage 6-7 atoms | Broad workflows decomposed into mechanism atoms with local and real-model gates | Atom pass is not workflow pass |
| Stage 7e v1-v4 | Low-cost-model G8/G9 passed 4/4 after explicit known-state provenance repair | Fixed-input, no-tool, deterministic evidence-decision macro only |

## Mechanism-First Method

The unit of evaluation is not a vague "task" but a mechanism atom or admitted macro.

A mechanism atom must have:

- one primary mechanism,
- fixed input,
- explicit output contract,
- deterministic evaluator,
- passing threshold,
- known-bad rejection,
- composition interface.

A macro task is admitted only when:

- its component atoms have passed local gates,
- its cross-atom obligations are explicit,
- no unsupported stale context is allowed,
- every important claim is evidence-bound,
- state is split into known and unknown fields,
- final decisions are gated by declared stage status.

## Stage 7e Repair Loop

Stage 7e is the clearest methodology case study.

1. v1 found a real low-cost-model failure: stage-gate and decision-trace retention were lost.
2. v2 repaired trace/gate retention but exposed unknown-state omissions.
3. v3 repaired unknown-state retention but exposed known-state provenance compression.
4. v4 repaired known-state provenance and reached 4/4 low-cost-model passes after retry.

This is not evidence that open-ended workflows are solved. It is evidence that the harness can convert a specific model failure into an explicit, testable obligation and verify the repair.

## Evaluation Protocol

For each new mechanism or macro:

1. Define the mechanism and failure mode.
2. Write the fixed input and output contract.
3. Create golden and known-bad outputs.
4. Run local evaluator regression.
5. Export a small real-model slice.
6. Execute with event logging.
7. Postprocess into per-run metrics.
8. Update the evidence ledger, claim boundary, and backlog before expanding scope.

Stop expansion if:

- local known-bad outputs pass,
- real runs show a systematic contract miss,
- provider failures prevent complete interpretation,
- the result would require a broader claim than the fixture supports.

## Claims And Non-Claims

Supported:

- Contract-rich harnessing improves absolute contract adherence in tested slices.
- Gap compression is possible but conditional.
- Low-cost models can become reliable on fixed mechanism-bound tasks when the missing obligations are explicit.
- Stage 7e v1-v4 demonstrates an iterative repair loop for evidence-decision macros.

Not supported:

- Universal model-gap closure.
- Low-cost models becoming generally equivalent to strong models.
- Full project initialization or research workflow readiness.
- Production readiness.

## Next Macro Admission Criteria

The next macro should not be a full project initializer or full research workflow yet. It should be a bounded macro composed only from passed mechanisms, with one new stressor at most.

Candidate next macros:

1. Evidence-bound method-plan update: compose state inventory, evidence binding, decision trace, stage gate, and obligation carry-forward into a methods/backlog update packet.
2. Citation-bound synthesis update: compose source selection, evidence typing, claim grounding, exclusion of stale context, and bounded recommendation.

Admission requirement:

- Stage 7e v4 remains the reference passing macro.
- The new macro must reuse its successful obligations.
- Any new mechanism must have a local golden/bad gate before real-model execution.
- The macro must declare what it cannot prove.

## Paper Outline

1. Introduction: reliability gaps in agent tasks and why stronger prompts are insufficient.
2. Background: workflow harnesses, validators, evidence contracts, and low-cost model deployment.
3. Method: contract-driven harness objects and mechanism atoms.
4. Metrics: task success, contract adherence, gap compression, weak-model enablement, and known-bad rejection.
5. Experiments: structured extraction, project initialization, research workflow, mechanism atoms, Stage 7e repair loop.
6. Results: absolute gains, conditional gap compression, and mechanism-bound low-cost-model enablement.
7. Boundary and threats: fixed inputs, no-tool macros, provider timeouts, evaluator construct validity, and non-production scope.
8. Discussion: harnesses as reliability engineering rather than model replacement.

## Immediate Next Work

1. Update the backlog so Stage 7e v4 is treated as the current admitted macro baseline.
2. Choose one bounded next macro from the admission criteria above.
3. Draft the paper's methods section from this outline before running any broader workflow slice.
