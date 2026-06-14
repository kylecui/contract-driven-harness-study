# Stage B v4 Local Result Summary

Completed: 2026-06-14

Decision: local gate passed; targeted smoke preparation is admissible

Provider calls: 0

## Result

Stage B v4-local isolated the two exact-content failures found in Stage B v3:

1. B4A tests exact evidence-array immutability;
2. B4B tests exact closed-vocabulary retention.

Each atom has a canonical fixture and one declared representation variant,
producing four fixtures in total.

| Check | Result |
|---|---:|
| Fixture structure validation | 4/4 passed |
| Golden outputs | 4/4 passed |
| Known-bad outputs | 28/28 rejected |
| Total local expectations | 32/32 met |
| Evaluator unit tests | 6/6 passed |
| Model-surface isolation violations | 0 |
| Stage B v3 regression expectations | 110/110 met |

## Mechanism Separation

The main local result is not merely that known-bads failed. Twenty-four of the
28 known-bads remained structurally valid JSON with
`schema_validity=1.000`, while the relevant exact-retention metric was
`0.000`.

This distinction demonstrates that the v4 evaluator can reject:

- evidence ID substitution;
- array reordering;
- duplicate or added references;
- slot merge or rename;
- undeclared evidence-field fallback;
- guess-to-infer prefix substitution;
- canonical or paraphrased vocabulary fallback;
- omission, addition, reordering, or mixed state labels.

Four additional known-bads intentionally changed the schema and received both
schema and primary-metric failure.

## Model-Surface Isolation

Each declared representation variant hides its evaluator-only alternative:

- the `evidence_ids` fixture does not expose `source_references`;
- the `source_references` fixture does not expose `evidence_ids`;
- the canonical vocabulary fixture does not expose the paraphrased labels;
- the paraphrased vocabulary fixture does not expose the canonical labels.

The automated scan found zero forbidden-value leaks across the model-visible
input, task, memory, evidence, and output-contract files.

## Regression

The existing Stage B v3 macro evaluator was rerun without modification against
the full v3 local suite. All 110 golden and known-bad expectations still
passed. The v4 evaluator therefore adds a narrower measurement layer without
changing the historical v3 record.

## Interpretation

RQ-B4A and RQ-B4B are answered positively at the fixture level: both failure
mechanisms can be represented as single-mechanism atoms with deterministic
exact-equality evaluators.

This result does not show that Qwen3-8B, G9, or any other model can satisfy the
atoms. It shows that the next model test can identify exactly which
preservation obligation failed without the confounding demands of the full
macro.

## Deviation Review

No scientific deviation occurred. A first regression attempt could not write
its report to `C:\tmp` under the active sandbox. The same unchanged command was
rerun with workspace-local temporary outputs and passed 110/110 expectations.
The temporary files were removed after inspection.

## Next Gate

Stage B v4-smoke may now be prepared as an eight-run debugging slice:

- model: `Qwen/Qwen3-8B`;
- harness: G9;
- inference mode: unchanged Stage B settings;
- fixtures: all four v4 atoms;
- repetitions: two per fixture;
- total provider calls: eight.

Every fixture must pass both repetitions before macro recomposition is
considered. Complete semantic failures are not retryable. Provider failures or
truncated outputs may be retried only under the existing declared retry rule.

The smoke must remain separate from Stage B v1, v2, and v3 data. Passing it
would justify a recomposition test, not a broad robustness claim.
