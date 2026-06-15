# Contract-Driven Harness v4 Quality Review

Reviewed: 2026-06-15

Artifact:
`research/06_outputs/contract-driven-harness-arxiv-v4-draft.md`

Overall grade: **A**

Blocking issues: none

## Dimension Review

| Dimension | Rating | Review |
|---|---|---|
| Question alignment | Pass | The draft answers the bounded reliability question and separates absolute stability from causal advantage, task breadth, and production economics. |
| Evidence completeness | Pass | The paper contains 60 unique project evidence references; every referenced ID exists in the evidence ledger. |
| Citation coverage | Pass | All 25 project source references resolve in the source index, and all 22 external citation keys resolve to used BibTeX entries. |
| Logic chain | Pass | The sequence from observed failure to explicit repair, ablation, mixed causal result, frozen protocol, fresh stability confirmation, and bounded claim is intact. |
| Counter-evidence | Pass | Stage B v5.2 remains a bounded null result and v5.3 remains mixed; neither is displaced by the v5.4 40/40 result. |
| Method fit | Pass | The draft distinguishes paired ablation from absolute stability, uses exact McNemar for the 15 matched v5.3 pairs, does not pool the pilot, reports pooled and per-condition Wilson intervals, and preserves the preregistered engineering threshold. |
| Actionability | Pass | The next decision is explicit: freeze the v4 evidence draft or preregister a separate matched Stage D overhead matrix before further provider calls. |
| Expression quality | Pass | Quantitative statements are attached to counts, thresholds, intervals, and non-claims. The draft avoids unsupported superiority language. |
| Risk disclosure | Pass | Model, provider, fixture, perturbation, task-family, causal, runtime, evaluator, overhead, tool, rollback, concurrency, and production limits are stated. |

## Quantitative Consistency

- Stage B v5.2 remains `15/15` versus `14/15` on exact evidence arrays and
  `10/15` versus `10/15` on the strict aggregate.
- Stage B v5.3 remains `15/15` versus `13/15`, risk difference `0.133`, with
  13 pass/pass pairs, 2 treatment-pass/control-fail pairs, 0 reverse pairs,
  and exact McNemar two-sided `p=0.500`.
- The preregistered `0.20` gate is an absolute risk-difference threshold,
  equivalent to at least three additional passes in a 15-run arm. It is not a
  significance threshold, equivalence margin, or power-derived effect bound.
- The two-discordant-pair result establishes neither equivalence nor the
  absence of a modest benefit.
- Stage B v5.4 uses only 40 fresh runs, reports `40/40`, and gives the Wilson
  interval `[0.912, 1.000]`.
- Each v5.4 perturbation condition reports `8/8` with Wilson interval
  `[0.676, 1.000]`.
- The v5.3 pilot is not pooled into the v5.4 stability estimate.
- V5.4 usage remains `83,312 + 19,672 = 102,984` tokens.
- Provider errors and retries remain zero for v5.3 and v5.4.

## Claim Boundary

Supported:

> Under the frozen explicit-transition-delta G9 protocol, Qwen3-8B completed
> the tested controlled multi-array state mutation in 40/40 fresh runs across
> five perturbation conditions.

Not supported:

- a preregistered `0.20` causal advantage over exact postconditions;
- arbitrary state-machine or workflow reliability;
- autonomous tool execution, rollback, or concurrency;
- provider-independent or task-family-independent reliability;
- lower cost per successful task than a strong-model baseline;
- production readiness.

## Repository Debt

The complete evidence ledger contains 28 historical Stage B v3-v5.1 source
IDs that do not yet have dedicated source-index rows. The v4 paper references
none of those IDs: every source ID used by v4 is indexed. This is a
nonblocking repository-normalization task, not a gap in the v4 claim chain.

## Publication Decision

V4 is suitable as the reviewed evidence-extension draft. It is not yet a
release-ready venue package because citation-format normalization, formal
Figure 1 conversion, final Appendix C placement, and venue-template layout
remain open. No additional provider run is required to support the current
bounded stability statement.
