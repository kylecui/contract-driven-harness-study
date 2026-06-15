# Contract-Driven Harness Paper v4 Integration Plan

Prepared: 2026-06-14

Status: active

## Version Boundary

- v3.1.1 remains frozen.
- v4 is a separate evidence-extension draft.
- This pass does not alter the v3.1.1 Markdown source or frozen PDF.
- Stage D provider calls are outside this pass and require a separate
  preregistration and go decision.

## New Evidence

v4 integrates:

- Stage B v5.2 evidence-binding ablation;
- Stage B v5.3 explicit transition-delta ablation;
- Stage B v5.4 fresh 40-run explicit-delta stability confirmation;
- provider usage, latency, retry, perturbation, and freeze-integrity records.

## Required Paper Changes

1. Add the 40/40 fresh stability result to the Abstract.
2. Extend the Introduction's strongest-evidence paragraph.
3. Add controlled state mutation to the method and repair-loop account.
4. Add v5.2-v5.4 as a separate evaluation block rather than folding it into
   the earlier four-run macro smoke narrative.
5. Report the mixed v5.3 causal result beside the positive v5.4 absolute
   stability result.
6. Replace the outdated perturbation and small-sample limitation text.
7. Preserve overhead measurement as an unresolved limitation until Stage D.
8. Update contribution-evaluation alignment and evidence traceability.
9. Regenerate a separate v4 LaTeX/PDF package and run compile checks.
10. Run an independent quality and expression review before freezing v4.
11. Correct the v5.3 paired analysis to exact McNemar and report
    per-condition v5.4 Wilson intervals.

## Claim Rules

Supported:

> Under the frozen explicit-transition-delta G9 protocol, Qwen3-8B completed
> the tested controlled multi-array state mutation in 40/40 fresh runs across
> five perturbation conditions.

Not supported:

- a preregistered `0.20` causal advantage over exact postconditions;
- arbitrary state-machine reliability;
- task-family generalization;
- autonomous tool execution, rollback, or concurrency;
- production readiness;
- favorable cost or latency relative to a strong-model baseline.

## Acceptance Criteria

- v4 contains every new quantitative result with the correct evidence IDs;
- v5.3 remains labeled mixed;
- v5.4 remains labeled absolute bounded stability;
- the 15-run pilot is not pooled with the fresh 40-run confirmation;
- the v5.3 paired result reports discordant pairs and exact McNemar;
- the five v5.4 condition intervals are reported beside the pooled interval;
- v3.1.1 hashes remain unchanged;
- the v4 source compiles without undefined references or citations;
- independent review finds no blocking claim-boundary issue.
