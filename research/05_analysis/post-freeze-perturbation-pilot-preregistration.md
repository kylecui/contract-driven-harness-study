# Post-Freeze Perturbation Pilot Preregistration

Prepared: 2026-06-13

Status: frozen before paid Stage B execution

## Hypothesis

H1: For each of the two admitted macros, Qwen3-8B with G9 will satisfy the
unchanged semantic contract in at least 2/3 runs under every predeclared
representation condition.

H1 is falsified for the pilot if any macro-condition cell passes fewer than
2/3 runs.

## Variables

Independent variables:

- macro: Stage 7e v4 evidence-bound decision or Stage 7-next method-plan update;
- condition: canonical, shuffled evidence order, declared field alias,
  unknown-state paraphrase, or distractor evidence.

Controlled variables:

- model: `Qwen/Qwen3-8B`;
- provider: SiliconFlow;
- harness: G9;
- temperature: 0;
- maximum output tokens: provider configuration value;
- evaluator thresholds and semantic obligations;
- three repetitions per macro-condition cell.

Dependent variables:

- binary contract pass;
- task and primary metric values;
- failure category;
- provider-reported prompt/completion/total tokens when available;
- prompt/output bytes;
- elapsed time;
- timeout, truncation, provider failure, and retry events.

## Baseline And Ablation

The canonical condition is the within-macro baseline.

Each noncanonical condition changes one factor:

| Condition | Isolated change |
|---|---|
| Evidence order shuffled | EvidenceBundle item order only |
| Field alias | Declared `evidence_ids` to `source_references` representation only |
| Unknown-state paraphrase | Declared equivalent state labels only |
| Distractor evidence | One irrelevant but plausible evidence item only |

No condition changes the selected option, required evidence set, stage gate,
negative obligations, or admission threshold.

## Evaluator Contract

- Declared aliases are canonicalized before semantic evaluation.
- Undeclared aliases are rejected.
- Known-state entries must remain structured objects with `state_id`, `fact`,
  and canonicalized `evidence_ids`.
- Every condition has a passing golden output.
- Every condition has a known-bad output tied to a predeclared failed metric.
- Evaluator or fixture changes after paid execution prevent pooling the affected
  runs into Stage C.

## Stop Rules

Stop paid execution and diagnose before continuing if:

- any cell passes fewer than 2/3 runs;
- provider failure exceeds 20%;
- timeout or truncation prevents a fair cell comparison;
- a declared perturbation changes the semantic obligation;
- evaluator behavior is ambiguous;
- generated outputs expose credentials or private provider metadata.

## Reporting

Report every run, including failures and retries. Do not replace failed attempts
with successful retries without preserving lineage. Pilot results support only
local representation-robustness claims over these two macros and five
conditions.

## Validity Threats

- Three repetitions provide a screening gate, not a precise stability estimate.
- The perturbations are predeclared but remain fixture-specific.
- Provider runtime variation may be correlated across sequential calls.
- Declared alias handling tests contract portability, not arbitrary schema
  interpretation.
- Deterministic evaluators can still miss semantically poor but contract-shaped
  outputs; qualitative failure review remains required.
