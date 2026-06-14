# Stage B v5.1 Controlled State-Transition Local Result

Completed: 2026-06-14

Decision: local repair gate passed; a separately authorized repair smoke is
admissible

Provider calls: 0

## Result

Stage B v5.1 repairs two defects identified after the failed v5 smoke:

1. the complete expected `transition_gate`, including `next_action`, is now
   model-visible; and
2. immutable slot-to-reference arrays are copied through a dedicated
   `evidence_bindings` section rather than attached to editable claim prose.

The strict semantic obligations were not reduced.

| Check | Result |
|---|---:|
| Transition fixtures | 2 |
| Golden outputs | 2/2 passed |
| Known-bad outputs | 36/36 rejected |
| Total local expectations | 38/38 met |
| New evaluator unit tests | 9/9 passed |
| Model-surface isolation violations | 0 |
| Repair-contract violations | 0 |
| Original Stage B v5 regression | 30/30 met |
| Stage B v4 atom regression | 32/32 met |
| Stage B v4 recomposition regression | 22/22 met |
| Stage B v3 macro regression | 110/110 met |

## Repair Boundary

The original Stage B v5 smoke remains a strict 0/4 failure. v5.1 is a new
protocol and does not replace, rescore, or pool with that result.

The repaired output still requires:

- four exact slot IDs;
- four exact reference arrays, including order and multiplicity;
- exact residual unknown-state and forbidden-inference labels;
- an exact event-backed known-state item and transition record;
- the exact post-transition gate;
- the exact retention attestation.

Claim prose remains in the evidence bundle as context. It is no longer an
editable output obligation, so evidence retention is measured independently
of prose rewriting.

## Targeted Diagnostics

The `v5_observed_semantic_remap` known-bad reproduces the main v5 evidence
failure: it removes `ev-11` from `claim_gamma` and moves it to
`claim_delta`.

For both fixtures, this output remained schema-valid and passed residual
state, transition, gate, and attestation checks. Only
`exact_evidence_array_preservation` failed. This confirms that the repaired
evaluator still rejects semantic evidence remapping.

The `wrong_gate_next_action` known-bad also remained schema-valid. Only
`transition_gate_accuracy` failed. Unlike v5, the correct `next_action` is now
present in the model-visible `required_transition_gate`.

The static pre-transition copy preserved evidence bindings and schema but
failed residual state, transition, and gate checks. The evaluator therefore
still requires mutation rather than static reproduction.

## Contract Audit

Both fixtures passed an independent repair audit:

- `required_transition_gate` contains all five scored fields;
- `editable_fields` is empty;
- `grounded_claims` does not appear in the output contract;
- four exact evidence bindings are declared;
- alternative evidence fields and state vocabularies do not appear on the
  wrong model surface.

Of the 36 known-bads, 32 remained schema-valid and were rejected by semantic
components. The four schema-invalid cases were the two undeclared-field
fallbacks and two omitted transition records.

## Regression

The v5.1 builder and evaluator are separate from all historical protocols.

- Original v5 remains 30/30 locally.
- Stage B v4 atoms remain 32/32.
- Stage B v4 bounded recomposition remains 22/22.
- Stage B v3 macros remain 110/110.
- Historical evaluator tests remain 8/8, 6/6, and 5/5.

No historical fixture or scoring rule changed.

## Evidence Record

- Local fixture and evaluator result: `P2-E154`
- Historical regression result: `P2-E155`
- Next-gate decision and claim boundary: `P2-E156`

## Deviation Review

The first historical regression attempt could not write result files to
`C:\tmp` under the active sandbox and stopped with `PermissionError`.
The same unchanged commands were rerun with project-local temporary outputs
and passed.

This was an execution-environment path restriction, not an experimental
failure or a change to the preregistered plan.

## Interpretation

The local result shows that both v5 defects can be removed while keeping exact
evidence retention and exact gate scoring. It establishes a fair,
deterministic model-facing contract and component-level failure attribution.

It does not show that Qwen3-8B satisfies the repaired contract. In particular,
removing editable prose may reduce a known source of remapping, but that causal
claim requires a model run.

## Claim Boundary

Supported:

> Stage B v5.1 expresses the evidence-binding and complete-gate obligations in
> a fully model-visible contract that passes local golden, known-bad,
> isolation, unit, and historical regression gates.

Not supported:

> Stage B v5.1 repairs Qwen3-8B performance.

Not supported:

> The harness supports general state machines, autonomous tool execution,
> rollback, concurrency, or production workflows.

## Next Gate

A Stage B v5.1 repair smoke may be prepared:

- model: `Qwen/Qwen3-8B`;
- harness: G9;
- fixtures: canonical and dual-surface stress;
- repetitions: two per fixture;
- planned provider calls: four.

Both fixtures must pass 2/2. Complete semantic failures are not retryable.
Provider failures or truncated invalid JSON may be retried only under the
existing declared rule. Execution requires separate user approval.
