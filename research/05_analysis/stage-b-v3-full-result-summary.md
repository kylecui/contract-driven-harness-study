# Stage B v3 Full-Slice Result Summary

Executed: 2026-06-14

Protocol: `stage_b_v3_full_literal_skeleton_perturbation_slice`

Model: `Qwen/Qwen3-8B`

Harness: G9

Decision: preregistered H1 failed

## Result

Stage B v3 completed all 30 planned SiliconFlow calls. All outputs were valid
JSON, no provider call failed, no completion reached the 3000-token limit, and
no retry was used.

The semantic result did not meet the preregistered gate:

- 18/30 runs passed the full deterministic contract;
- 6/10 macro-condition cells passed the required 2/3 threshold;
- 4/10 cells failed;
- overall run pass rate: 0.600, 95% Wilson CI [0.423, 0.754].

The aggregate rate is descriptive. The preregistered decision is cell-based,
so one failed cell is enough to falsify H1.

## Cell Results

| Macro | Condition | Pass | Rate | 95% Wilson CI | Cell decision |
|---|---|---:|---:|---|---|
| Stage 7-next | canonical | 0/3 | 0.000 | [0.000, 0.562] | Fail |
| Stage 7-next | distractor evidence | 3/3 | 1.000 | [0.439, 1.000] | Pass |
| Stage 7-next | evidence order shuffled | 3/3 | 1.000 | [0.439, 1.000] | Pass |
| Stage 7-next | field alias | 2/3 | 0.667 | [0.208, 0.939] | Pass |
| Stage 7-next | unknown-state paraphrase | 0/3 | 0.000 | [0.000, 0.562] | Fail |
| Stage 7e v4 | canonical | 1/3 | 0.333 | [0.061, 0.792] | Fail |
| Stage 7e v4 | distractor evidence | 3/3 | 1.000 | [0.439, 1.000] | Pass |
| Stage 7e v4 | evidence order shuffled | 3/3 | 1.000 | [0.439, 1.000] | Pass |
| Stage 7e v4 | field alias | 3/3 | 1.000 | [0.439, 1.000] | Pass |
| Stage 7e v4 | unknown-state paraphrase | 0/3 | 0.000 | [0.000, 0.562] | Fail |

## Execution Integrity

| Check | Result |
|---|---|
| Planned calls | 30 |
| Completed calls | 30 |
| Provider errors | 0 |
| JSON parse failures | 0 |
| Retries | 0 |
| Prompt tokens | 207,078 |
| Completion tokens | 54,865 |
| Total tokens | 261,943 |
| Reasoning tokens | 0 |
| Completion-token maximum | 2,013 / 3,000 |
| Latency | 14.937-33.704 seconds |
| Median latency | 19.906 seconds |
| P90 latency | 25.638 seconds |

The dated SiliconFlow list-price snapshot records `Qwen/Qwen3-8B` input and
output prices as CNY 0 per million tokens on 2026-06-13. This does not imply
zero engineering or runtime cost.

## What Worked

The v3 hierarchy repair was effective at the structural level:

- all 30 outputs were valid JSON;
- all 30 kept `state_inventory` as a nested object;
- distractor-evidence and evidence-order-shuffled cells passed 12/12;
- field aliases passed 5/6;
- trace, gate, evidence typing, context relevance, and safety obligations
  remained intact across the slice.

This supports a narrow claim: literal skeletons can stabilize broad JSON shape
and many cross-section obligations for this low-cost model.

## What Failed

The literal skeleton did not make exact content slots immutable:

- 9 runs failed citation grounding;
- 7 omitted required support `stage7next-e06`;
- 2 omitted required support `stage7e-e08`;
- 6 paraphrase runs replaced required `do_not_guess_*` labels with undeclared
  `do_not_infer_*` labels;
- 3 Stage 7-next paraphrase runs contained both failure types.

All 12 failed outputs were complete and parseable. These are semantic contract
failures, not provider failures or truncations, so the retry rule does not
apply.

## Interpretation

Stage B v3 resolves the earlier hierarchy-collapse failure but does not provide
robust exact-slot preservation. The low-cost model often preserves the shape
while rewriting fixed evidence arrays or closed-vocabulary labels toward
semantically familiar alternatives.

The surprising contrast between failed canonical cells and passing shuffled or
distractor cells also shows that representation changes are not monotonically
harder. Small prompt-surface changes can alter which exact obligations receive
attention, even with temperature 0.

## Claim Boundary

Supported:

> Under a literal G9 JSON skeleton, Qwen3-8B reliably preserved the overall
> hierarchy and passed six of ten tested macro-condition cells.

Not supported:

> A literal skeleton is sufficient to guarantee exact evidence-slot and
> closed-vocabulary value preservation across these macro perturbations.

Not supported:

> Stage B v3 establishes general perturbation robustness or workflow
> readiness.

## Decision

Stage B v3 is closed as a failed full-slice protocol. Its 30 runs remain a
standalone negative-result dataset and must not be pooled with Stage B v1, v2,
the v3 smoke, or a future repair protocol.

Stage C and Stage D remain blocked. The next experiment should isolate two
mechanisms before another full slice:

1. exact evidence-array immutability;
2. exact closed-vocabulary value retention under declared paraphrase.

Each mechanism needs its own local golden/known-bad gate and a small targeted
real-model smoke before a new 30-run confirmation.
