# Post-Freeze Perturbation Pilot Stage B v2 Preregistration

Prepared: 2026-06-13

Status: prepared; no paid Stage B v2 calls made

## Purpose

Stage B v2 is a repair-confirmation experiment after the failed Stage B v1
pilot. It asks whether a revised, more explicit G9 contract restores stable
contract adherence for the same two macros and five representation conditions.

Stage B v2 does not replace, erase, or rescore Stage B v1. The protocols differ
and their runs must not be pooled.

## Hypothesis

H1: For each admitted macro, Qwen3-8B with the Stage B v2 G9 contract will pass
at least 2/3 runs in every predeclared representation condition.

H1 is falsified if any of the ten macro-condition cells passes fewer than 2/3
runs.

Passing H1 supports only the claim that the repaired contract is stable enough
to advance to the next planned evaluation gate over these fixtures. It does not
prove arbitrary schema robustness, production readiness, or model equivalence.

## Variables

Independent variables:

- macro: Stage 7e v4 evidence-bound decision or Stage 7-next method-plan update;
- condition: canonical, evidence-order shuffled, declared field alias,
  unknown-state paraphrase, or distractor evidence.

Controlled variables:

- provider: SiliconFlow;
- model: `Qwen/Qwen3-8B`;
- model tier: low-cost model;
- harness arm: G9;
- temperature: 0;
- maximum output tokens: 3000;
- thinking mode: `enable_thinking=false`;
- `reasoning_effort` and `thinking_budget`: not sent;
- three repetitions per macro-condition cell;
- frozen fixtures, evaluator, prompts, provider config, and admission threshold.

Dependent variables:

- binary contract pass;
- task and atom-primary metrics;
- failed metric and qualitative failure category;
- provider-reported token use when available;
- prompt and output bytes;
- elapsed time;
- provider failure, timeout, truncation, and retry lineage.

## Stage B v2 Repairs

The repaired contract applies all of the following to every cell:

1. an explicit compact output template;
2. one fixed required evidence combination for the selected C2 claim;
3. a closed carried-obligation status vocabulary containing only `preserved`;
4. ID-only arrays for `typed_evidence`;
5. exact counts for rejected options, decision-trace entries, and carried
   obligations;
6. exact surface requirements for declared field and state-label variants;
7. a uniform 3000-token completion limit.

These changes form one repaired harness package. Stage B v2 can test the package
but cannot identify the independent effect of each repair.

## Baselines And Perturbations

The canonical condition is the within-macro v2 baseline. Each noncanonical
condition changes one representation factor:

| Condition | Isolated fixture change |
|---|---|
| Evidence order shuffled | EvidenceBundle item order only |
| Field alias | Declared `evidence_ids` to `source_references` surface only |
| Unknown-state paraphrase | Declared equivalent state labels only |
| Distractor evidence | One irrelevant but plausible evidence item only |

Stage B v1 is a historical diagnostic baseline, not a poolable statistical
control. Its 16/30 corrected run pass rate and 5/10 passing cells remain
reported as the outcome of the earlier protocol.

## Evaluator Contract

- Every v2 fixture has one passing golden output.
- Every fixture has known-bad outputs for missing evidence, compact-shape
  violations, open status vocabulary, and condition-specific failures.
- Declared aliases are canonicalized only after their required surface form is
  checked.
- The model-visible contract omits evaluator-only canonicalization maps. The
  evaluator contract retains them for scoring, so alias conditions do not show
  the model conflicting canonical output names.
- Undeclared, canonical-fallback, and hybrid surface forms are rejected where
  the condition requires an alias.
- Grounded-claim evidence and selected-claim evidence are separate evaluator
  obligations.
- Evaluator or fixture changes after paid execution invalidate pooling within
  Stage B v2 and require an amendment or a new version.

## Admission And Stop Rules

Stage B v2 advances only if all ten cells pass at least 2/3 runs.

Stop paid execution and diagnose before continuing if:

- provider failures exceed 20%;
- timeout or truncation prevents fair comparison;
- a perturbation changes the semantic obligation;
- evaluator behavior becomes ambiguous;
- prompts, fixtures, config, or evaluator change after the first paid call;
- generated artifacts expose credentials or private provider metadata.

All attempts and retries must remain in the evidence record. A successful retry
cannot silently replace a failed attempt.

## Statistical Reporting

Report the pass count and pass proportion for every three-run cell, plus a 95%
Wilson interval with an explicit warning that three repetitions are a screening
sample. Aggregate results are descriptive because fixture runs share prompts,
provider conditions, and evaluator structure.

No claim of statistical equivalence or broad generalization is permitted from
this 30-run slice.

## Reproducibility

- Fixture suite:
  `research/04_methods/macro-perturbations-v2/`
- Matrix:
  `research/04_methods/benchmark-matrix-post-freeze-perturbation-pilot-v2.json`
- Provider config:
  `research/04_methods/provider-config.siliconflow-stage-b-v2.json`
- Local gate:
  `research/05_analysis/stage-b-v2-local-gate.json`
- Price snapshot:
  `research/01_sources/siliconflow-pricing-snapshot-2026-06-13.md`
- Freeze manifest:
  `research/05_analysis/post-freeze-perturbation-pilot-v2-freeze-manifest.json`

The repository README and method scripts provide the current local gate,
packet-generation, preflight, dry-run, evaluation, and inspection entry points.

## Current Non-Claims

- No low-cost/strong-model equivalence claim.
- No production-readiness claim.
- No arbitrary schema-renaming claim.
- No general robustness claim beyond the declared fixtures.
- No causal attribution to a single Stage B v2 repair.
- No Stage C or Stage D admission before the Stage B v2 stop rule is evaluated.
