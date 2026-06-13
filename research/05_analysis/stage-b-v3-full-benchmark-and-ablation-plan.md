# Stage B v3 Full Benchmark And Ablation Plan

Prepared: 2026-06-13

## Benchmark

The matrix contains two macros, five representation conditions, and three
repetitions: 30 planned Qwen3-8B G9 runs.

| Condition | Changed fixture factor |
|---|---|
| Canonical | None |
| Evidence order shuffled | EvidenceBundle order |
| Field alias | `evidence_ids` to `source_references` surface |
| Unknown-state paraphrase | Declared state-label surface |
| Distractor evidence | One irrelevant plausible evidence item |

All conditions use the same literal-skeleton mechanism and admission threshold.

## Repair Mapping

| Observed failure | v3 control |
|---|---|
| Flattened state hierarchy | Literal nested `state_inventory` object |
| Root-promoted state fields | Exact key hierarchy and known-bad |
| Omitted unknown/forbidden state | Exact nested labels and slot checks |
| Grounded evidence compression | Explicit grounded-claim slots and exact count |
| Field-alias fallback | Surface-only model contract |
| Open status vocabulary | Exact `preserved` value |

## Deferred Ablations

Run separately after the full slice:

| Factor | Ablation |
|---|---|
| Literal skeleton | Return to descriptive template |
| Exact grounded slots | Collapse to one generic grounded slot |
| Exact list counts | Retain keys but permit variable list length |
| Provider enforcement | Compare prompt-only skeleton with native structured output |
| Thinking | Compare disabled and enabled |

Stage B v3 cannot attribute package-level performance to one factor.
