# Stage B v2 Benchmark And Ablation Plan

Prepared: 2026-06-13

## Benchmark Question

Does the repaired G9 contract remain executable by Qwen3-8B across the same two
macros and five representation conditions that exposed Stage B v1 failures?

The answer is operational: advance only if every cell passes at least 2/3 runs.

## Repair-To-Failure Mapping

| Stage B v1 failure | Stage B v2 repair | Direct local control |
|---|---|---|
| Unknown-state surface drift | Exact required and forbidden surface values | Canonical fallback and hybrid-surface known-bads |
| Missing selected-claim evidence combination | One explicit required combination | Incomplete selected-support known-bad |
| Open interpretation of status values | Closed `preserved` vocabulary | Open-vocabulary status known-bad |
| Verbose repeated evidence | ID-only `typed_evidence` shape | Expanded-object known-bad |
| Output truncation | Compact template plus 3000-token budget | Golden-size check and runtime truncation review |

## What Stage B v2 Can Attribute

The five representation conditions isolate fixture changes while holding the v2
harness package fixed. They can identify which representation cells remain
fragile.

Stage B v2 cannot attribute improvement to one repair because template,
evidence-combination, vocabulary, compactness, and token-budget changes are
introduced together.

## Deferred Single-Factor Ablations

Run these only after Stage B v2 and keep them separate from its 30 runs:

| Contribution | Single-factor ablation | Expected diagnostic |
|---|---|---|
| Explicit output template | Remove template, retain all other v2 rules | Tests schema/shape contribution |
| Fixed selected evidence | Restore alternative valid combinations | Tests evidence-combination ambiguity |
| Closed status vocabulary | Permit v1 synonym set | Tests evaluator/prompt vocabulary coupling |
| Compact typed evidence | Permit object-expanded typed evidence | Tests prompt length and truncation pressure |
| 3000-token budget | Return to 2000 tokens | Tests budget contribution to truncation |
| Thinking disabled | Enable Qwen3 thinking with all else fixed | Tests inference-mode sensitivity |

Each ablation must change one factor, use paired fixtures, preserve all attempts,
and receive a separate preregistration and budget approval.

## Fairness Rules

- identical model and inference settings across v2 cells;
- identical repetition count and sequential-run policy;
- no fixture-specific prompt repair after execution begins;
- no selective retries or successful-run replacement;
- no comparison to Stage B v1 without disclosing protocol changes;
- no strong-model comparison inside Stage B v2.
