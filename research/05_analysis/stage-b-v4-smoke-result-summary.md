# Stage B v4 Targeted Smoke Result

Executed: 2026-06-14

Decision: pass

## Result

Qwen3-8B under G9 passed all eight isolated exact-retention runs:

| Fixture | Passes | Decision |
|---|---:|---|
| B4A canonical `evidence_ids` | 2/2 | Pass |
| B4A declared `source_references` alias | 2/2 | Pass |
| B4B canonical vocabulary | 2/2 | Pass |
| B4B paraphrased vocabulary | 2/2 | Pass |
| Total | 8/8 | Pass |

Every run received:

- `schema_validity=1.000`;
- `atom_primary_metric=1.000`;
- `task_success=1.000`.

The preregistered rule required every fixture to pass both repetitions, so the
smoke passed.

## Execution Integrity

| Check | Result |
|---|---:|
| Planned calls | 8 |
| Completed calls | 8 |
| Provider errors | 0 |
| Retries | 0 |
| Invalid JSON | 0 |
| Prompt tokens | 8,348 |
| Completion tokens | 1,110 |
| Total tokens | 9,458 |
| Reasoning tokens | 0 |
| Completion-token range | 84-191 / 2,000 |
| Latency range | 3.407-8.454 seconds |
| Median latency | 5.765 seconds |

The dated 2026-06-13 SiliconFlow list-price snapshot recorded
`Qwen/Qwen3-8B` input and output token prices as CNY 0 per million tokens.
This does not make engineering or runtime cost zero.

## Output Audit

All eight raw outputs were inspected.

B4A preserved:

- all three slot IDs;
- the singleton arrays `["ev-01"]` and `["ev-06"]`;
- the ordered pair `["ev-07", "ev-08"]`;
- the declared field name in both canonical and alias fixtures;
- the `immutability_check` declaration.

B4B preserved:

- all three unknown-state labels;
- all three forbidden-inference labels;
- declared order and multiplicity;
- the exact `do_not_guess_*` prefix in both paraphrased repetitions.

No semantic failure, fallback field, synonym substitution, additional value,
omission, or array reordering was found.

## Interpretation

This smoke changes the diagnosis of the Stage B v3 failures.

The model can perform both exact-retention operations under small, isolated G9
contracts. The earlier failures therefore should not be described as proof
that Qwen3-8B cannot preserve evidence arrays or unfamiliar state labels.
Instead, the current evidence points to a composition or attention-allocation
problem: the obligations failed inside a larger contract but passed when made
the sole primary mechanism.

The result also supports the mechanism-first experimental strategy. Atomization
turned a vague macro failure into two independently testable capabilities and
showed that both are locally achievable.

## Claim Boundary

Supported:

> Under G9, Qwen3-8B completed four isolated exact-retention fixtures in two
> repetitions each.

Supported as a diagnosis:

> The Stage B v3 failures are not sufficient evidence of an irreducible model
> capability limit, because the same preservation obligations passed when
> isolated.

Not supported:

> The Stage B v3 macros have been repaired.

Not supported:

> The harness is generally robust to schema perturbations or long-contract
> attention pressure.

Not supported:

> Eight isolated runs provide a stable production reliability estimate.

## Next Decision

Do not spend the next calls on more identical atom repetitions. They would
measure isolated repeatability but would not test transfer.

The next experiment is Stage B v4-recomposition:

1. compose B4A and B4B into one bounded macro;
2. keep unrelated obligations fixed and minimal;
3. add known-bads that independently corrupt evidence arrays and vocabulary;
4. pass local golden/known-bad and Stage B v3 regression gates;
5. run a small targeted smoke before considering another 30-run slice.

This preserves the mechanism-first sequence:

`macro failure -> isolated atoms -> atom smoke -> bounded recomposition`.
