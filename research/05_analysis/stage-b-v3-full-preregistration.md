# Stage B v3 Full Perturbation Slice Preregistration

Prepared: 2026-06-13

Status: preparation only; no Stage B v3 full-slice provider calls made

## Purpose

Stage B v3 tests the repaired literal-skeleton G9 package across the same two
macros and five representation conditions used in Stage B v2.

Stage B v2 failed its first canonical cell at 0/3 because the model flattened
the required state hierarchy. The Stage B v3 repair smoke preserved that
hierarchy in 3/3 completed lineages and passed the full contract in 2/3.

The full v3 protocol adds one predeclared refinement before execution:
explicit grounded-claim slots. This addresses the smoke's single full-contract
failure, where one generic grounded-claim placeholder invited evidence-slot
compression.

## Hypothesis

H1: Qwen3-8B with the Stage B v3 G9 contract will pass at least 2/3 runs in
every macro-condition cell.

H1 is falsified if any of the ten cells passes fewer than 2/3 runs.

Passing supports only a bounded claim over these macros, conditions, model, and
contract. It does not prove arbitrary schema robustness, production readiness,
or strong-model equivalence.

## Variables

Independent variables:

- macro: Stage 7e v4 evidence-bound decision or Stage 7-next method-plan update;
- condition: canonical, evidence-order shuffled, declared field alias,
  unknown-state paraphrase, or distractor evidence.

Controlled variables:

- provider: SiliconFlow;
- model: `Qwen/Qwen3-8B`;
- harness: G9;
- temperature: 0;
- maximum output tokens: 3000;
- `enable_thinking=false`;
- three repetitions per cell;
- evaluator thresholds and semantic obligations;
- frozen literal skeleton, prompts, fixtures, and config.

Dependent variables:

- binary full-contract pass;
- schema, state, grounding, evidence-type, trace, stage-gate, context, and
  atom-primary metrics;
- provider status, retry lineage, latency, tokens, output bytes, and truncation.

## Repaired Contract

Each model-visible output contract contains a literal JSON skeleton that fixes:

- the complete key hierarchy;
- the number of top-level list slots;
- state IDs and unknown/forbidden labels;
- field aliases for the field-alias condition;
- evidence-reference arrays for grounded, selected, rejected, trace, gate, and
  carried-obligation slots;
- exactly four carried obligations with status `preserved`.

The model replaces placeholder prose strings but must not move, merge, omit, or
add contract slots.

## Baselines

- Within-protocol baseline: each macro's v3 canonical cell.
- Historical diagnostic: Stage B v2 canonical method-plan cell, 0/3.
- Repair admission evidence: Stage B v3 shape smoke, hierarchy 3/3 and full
  contract 2/3.
- Local deterministic control: v3 golden and known-bad suite.

Historical runs are not pooled with Stage B v3.

## Local Gates

Every fixture must:

1. pass its golden output;
2. reject all inherited v2 known-bads;
3. reject flattened, root-promoted, and omitted nested state;
4. reject compressed grounded-claim slots;
5. preserve field-alias and state-paraphrase surface isolation;
6. compile into a unique 30-run queue;
7. pass required-key preflight and adapter dry-run.

## Stop And Retry Rules

Stop and diagnose if:

- any completed cell falls below 2/3;
- provider failures exceed 20%;
- timeout or truncation prevents fair comparison;
- evaluator behavior becomes ambiguous;
- any frozen protocol file changes after execution starts.

Immediate HTTP 5xx failures with no model output may receive one
lineage-preserving, byte-identical retry. Original failures remain recorded.
No retry may silently replace a completed contract failure.

## Statistical Reporting

Report each cell's pass count, proportion, and 95% Wilson interval. Three runs
per cell remain a screening sample. Aggregate values are descriptive and must
not be treated as 30 independent observations for broad inference.

## Ablation Boundary

Stage B v3 evaluates the repaired package. It does not isolate:

- literal skeleton versus provider-native structured output;
- exact evidence slots versus exact list counts;
- thinking mode;
- token limit;
- model family.

Those require separate single-factor protocols.

## Validity Threats

- The skeleton supplies substantial structure and exact evidence slots, so the
  result measures execution under a strong contract rather than independent
  plan synthesis.
- Three runs per cell provide limited uncertainty resolution.
- Only two admitted macros are represented.
- Exact slot scaffolding may overfit these fixture families.
- Provider availability can introduce HTTP 5xx failures independent of model
  behavior.
- Deterministic gates do not measure human writing preference.

## Pooling Policy

Do not pool Stage B v1, v2, v3 smoke, or v3 full runs. Preserve each protocol's
lineage and interpret them as sequential repair evidence.
