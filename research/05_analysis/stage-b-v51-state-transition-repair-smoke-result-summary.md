# Stage B v5.1 State-Transition Repair Smoke Result

Executed: 2026-06-14

Decision: pass under the preregistered repair-smoke protocol

## Strict Result

Qwen3-8B under G9 passed all four complete runs:

| Fixture | Passes | Decision |
|---|---:|---|
| Canonical state transition | 2/2 | Pass |
| Dual-surface stress | 2/2 | Pass |
| Total | 4/4 | Pass |

The preregistered rule required both fixtures to pass 2/2 and every component
metric to equal `1.000`.

## Component Result

| Metric | Passing runs |
|---|---:|
| `schema_validity` | 4/4 |
| `exact_evidence_array_preservation` | 4/4 |
| `residual_unknown_vocabulary_accuracy` | 4/4 |
| `state_transition_accuracy` | 4/4 |
| `transition_gate_accuracy` | 4/4 |
| `retention_attestation_accuracy` | 4/4 |
| `controlled_state_mutation_success` | 4/4 |

No failed component requires a failure audit.

## Execution Integrity

| Check | Result |
|---|---:|
| Planned calls | 4 |
| Completed calls | 4 |
| Provider errors | 0 |
| Retries | 0 |
| Invalid JSON | 0 |
| Prompt tokens | 8,340 |
| Completion tokens | 1,968 |
| Total tokens | 10,308 |
| Reasoning tokens | 0 |
| Completion-token range | 490-494 / 2,000 |
| Latency range | 18.266-23.219 seconds |
| Median latency | 19.907 seconds |

All calls used `Qwen/Qwen3-8B`, temperature zero, disabled thinking, and the
frozen G9 packets.

The dated 2026-06-13 SiliconFlow public-price snapshot listed Qwen3-8B input
and output tokens at CNY 0 per million tokens. This does not assert current or
account-specific billing.

## Raw-Output Audit

All four raw outputs were inspected.

Every output:

- used exactly the fixture-specific evidence field;
- preserved all four binding slot IDs and arrays in order;
- retained both entries in the `claim_gamma` evidence array;
- moved only the API-permission state from unknown to approved;
- preserved branch and CI as the two residual unknown states;
- preserved the two matching forbidden-inference labels;
- recorded the exact event, transition value, and `ev-09` support;
- copied the complete declared gate, including `next_action`;
- copied the complete retention attestation;
- returned valid JSON with no extra prose.

The two repetitions within each fixture were byte-equivalent after provider
output capture. This is an observation from this smoke, not a general
determinism claim.

## Comparison With Stage B v5

The original v5 smoke remains a strict 0/4 result:

| Protocol | Evidence | Gate | Aggregate |
|---|---:|---:|---:|
| Stage B v5 | 0/4 | 0/4 | 0/4 |
| Stage B v5.1 | 4/4 | 4/4 | 4/4 |

The v5.1 protocol changed two model-facing surfaces:

1. immutable slot-to-reference arrays moved into `evidence_bindings`, separate
   from editable claim prose;
2. the complete exact gate, including `next_action`, became model-visible.

The state transition, residual state, evidence arrays, gate, and attestation
remained exact obligations. v5.1 therefore demonstrates successful transfer of
the repaired contract, not a relaxed evaluator.

## Interpretation

The result supports a bounded mechanism-repair claim:

> After the evidence-binding and gate-disclosure defects were repaired,
> Qwen3-8B under G9 satisfied the complete controlled-transition contract in
> both representation variants and both repetitions.

The comparison is useful because the failed v5 components are exactly the
components that pass in v5.1. The local known-bads also confirm that semantic
evidence remapping and wrong `next_action` would still be rejected.

However, the two repairs were bundled. This experiment cannot determine
whether separating evidence bindings, exposing the complete gate, or their
combination caused the observed change. Four runs also do not estimate a
stable success probability.

## Claim Boundary

Supported:

> A low-cost Qwen3-8B model completed one repaired, fully model-visible,
> event-driven state-transition macro under G9 in 4/4 targeted smoke runs.

Supported:

> The repair retained strict exact-array and exact-gate evaluation rather than
> converting the task into approximate semantic scoring.

Not supported:

> Either individual repair is independently sufficient.

Not supported:

> Qwen3-8B is generally reliable on state machines, autonomous workflows, or
> tool execution.

Not supported:

> The Stage B v5 failure should be rescored, discarded, or pooled with v5.1.

## Evidence Record

- Provider execution: `P2-E157`
- Strict evaluation and raw-output audit: `P2-E158`
- Repair comparison and decision boundary: `P2-E159`

## Next Decision

Do not immediately expand to another broad macro.

The next scientifically useful choice is between:

1. a small repair ablation separating `evidence_bindings` from complete gate
   disclosure; or
2. a larger repetition set of the frozen v5.1 protocol if the immediate goal
   is a reliability estimate.

The current four-run gate is complete. Either next experiment requires a new
preregistered protocol and separate provider authorization.
