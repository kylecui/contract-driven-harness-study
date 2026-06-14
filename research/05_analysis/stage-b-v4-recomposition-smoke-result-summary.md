# Stage B v4 Bounded Recomposition Smoke Result

Executed: 2026-06-14

Decision: pass

## Result

Qwen3-8B under G9 passed all four bounded recomposition runs:

| Fixture | Passes | Decision |
|---|---:|---|
| Canonical recomposition | 2/2 | Pass |
| Dual-surface stress | 2/2 | Pass |
| Total | 4/4 | Pass |

Every run received:

- `schema_validity=1.000`;
- `exact_evidence_array_preservation=1.000`;
- `exact_closed_vocabulary_retention=1.000`;
- `composition_gate_accuracy=1.000`;
- `composition_retention=1.000`;
- `task_success=1.000`.

The preregistered rule required both fixtures to pass both repetitions, so the
smoke passed.

## Execution Integrity

| Check | Result |
|---|---:|
| Planned calls | 4 |
| Completed calls | 4 |
| Provider errors | 0 |
| Retries | 0 |
| Invalid JSON | 0 |
| Prompt tokens | 6,110 |
| Completion tokens | 1,479 |
| Total tokens | 7,589 |
| Reasoning tokens | 0 |
| Completion-token range | 367-372 / 2,000 |
| Latency range | 13.750-17.343 seconds |
| Median latency | 15.813 seconds |

All four calls used `Qwen/Qwen3-8B`, temperature zero, disabled thinking, and
the frozen G9 packets. No output approached the token limit.

## Output Audit

All four raw outputs were inspected after deterministic evaluation.

Every output preserved:

- all three unknown-state labels in the declared vocabulary;
- all three forbidden-inference labels in the declared vocabulary;
- all three claim slot IDs;
- the singleton evidence arrays and the ordered two-item evidence array;
- the fixture-specific evidence field name;
- the blocked `provider_execution` gate and its missing prerequisite;
- the ordered support-slot list;
- the fixture-specific immutable-field attestation.

The free-text claim wording varied slightly across repetitions. That field was
not an immutable payload in this experiment. No required identifier, array,
closed-vocabulary value, gate value, or attestation value changed.

## Interpretation

The two mechanisms that passed as isolated atoms also survived this bounded
composition. The result therefore narrows the Stage B v3 diagnosis again:
Qwen3-8B can preserve the exact evidence arrays and unfamiliar state labels
when both obligations appear together with one fixed gate under G9.

This is evidence of bounded composition transfer, not repair of the larger
Stage B v3 macros. The packet remains mostly copy-oriented, the gate is fixed,
and only two fixture variants were run twice.

## Claim Boundary

Supported:

> Under G9, Qwen3-8B retained exact evidence arrays, exact state vocabularies,
> and the fixed local-first gate in two bounded recomposition variants with two
> repetitions each.

Supported as a diagnosis:

> The Stage B v3 evidence and vocabulary failures are not inevitable when the
> two mechanisms are composed under a smaller explicit contract.

Not supported:

> The full Stage B v3 macros are repaired.

Not supported:

> Four runs estimate production reliability or general perturbation
> robustness.

Not supported:

> The model can preserve these obligations while also performing a genuine
> state transition or open-ended synthesis.

## Next Decision

Do not proceed directly to a 30-run confirmation slice. More repetitions of
the same static packet would mainly measure repeatability of a narrow copying
task.

The next stage is a controlled state-mutating macro:

1. retain the exact evidence and state-vocabulary obligations;
2. introduce one explicit state transition with a deterministic expected
   result;
3. require the output gate and attestation to reflect the post-transition
   state;
4. add known-bads that preserve the copied inputs but fail the transition;
5. pass local golden, known-bad, surface-isolation, and historical regression
   gates before any provider call.

This tests whether the retained obligations remain usable during a small
piece of work, rather than only during static reproduction.
