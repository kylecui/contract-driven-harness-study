# Stage B v5.2 Failure Audit

Executed: 2026-06-14

## Audit Scope

The 30-run slice produced 20 strict passes and 10 strict failures. All 30
provider responses were complete, valid JSON. No provider error, timeout,
truncation, or retry occurred.

Every failed output was compared with its frozen prompt, output contract,
golden output, validation report, and component metrics.

## Failure Classification

| Failure class | Runs | Retry eligible | Interpretation |
|---|---:|---:|---|
| Residual forbidden-inference label retained | 9 | No | Complete semantic output that missed an exact postcondition |
| Evidence binding remapped | 1 | No | Complete semantic output that changed required slot-to-evidence arrays |
| Provider/runtime/parse failure | 0 | N/A | Execution integrity remained complete |

## Residual-State Pattern

Nine outputs performed the main transition correctly:

- the API-permission state was removed from `unknown_state`;
- the state was added to `known_state` with the correct approved value and
  evidence;
- the transition record was exact;
- the transition gate was exact.

They nevertheless retained the matching API-permission entry in
`forbidden_inferences`. The expected post-state contains only the branch and CI
inference restrictions. All nine failures had this same shape.

This is a real exact-contract miss under the frozen evaluator. It is not a
reasonable field alias, ordering variation, or parser artifact. The raw score
therefore remains failed.

The prompt audit also found an instruction-salience regression relative to
Stage B v5.1. The v5.1 prompt explicitly said:

> Remove only the matching API-permission forbidden inference.

The v5.2 prompt retained the exact `required_postconditions` object and told
the model to preserve the other forbidden-inference values, but it did not
repeat the removal operation as a direct task constraint. The obligation was
visible, so the protocol is not invalid. However, strict aggregate reliability
is no longer a clean replication of v5.1 state-transition control.

This regression affected both representation profiles and therefore does not
invalidate the primary R1/R2 evidence-representation comparison. It does limit
the interpretation of the 20/30 strict aggregate result.

## Evidence-Remapping Pattern

One R1 distractor-evidence output changed two required bindings:

- `claim_gamma` returned `["ev-10"]` instead of `["ev-10", "ev-11"]`;
- `claim_delta` returned `["ev-11"]` instead of `["ev-09"]`.

The output remained valid JSON and satisfied the state, transition, gate, and
attestation checks. This is the only observed evidence-array failure and is a
genuine semantic remapping, not an evaluator false positive.

## Audit Decision

- Keep all 10 strict failures unchanged.
- Do not retry any failed run.
- Do not rescore the residual-state pattern as a pass.
- Use the frozen exact-evidence metric for the representation ablation.
- Do not use the strict aggregate rate as a clean estimate of the fully
  explicit v5.1 repair's reliability.
- Any restoration of the explicit removal instruction creates a new protocol
  and requires fresh runs.

