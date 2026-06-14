# Stage B v5.2 Evidence-Binding Ablation Result

Executed: 2026-06-14

Decision: no engineering-scale evidence-representation effect observed

## Research Question

Stage B v5.1 bundled two repairs: complete gate disclosure and separation of
immutable evidence bindings from editable claim prose. Stage B v5.2 held the
complete gate constant and varied only the evidence representation.

The experiment asked whether binding separation independently produced a
large improvement in exact evidence retention.

## Execution Integrity

| Check | Result |
|---|---:|
| Planned calls | 30 |
| Completed calls | 30 |
| Provider errors | 0 |
| Retries | 0 |
| Invalid JSON | 0 |
| Prompt tokens | 59,007 |
| Completion tokens | 15,862 |
| Total tokens | 74,869 |
| Reasoning tokens | 0 |
| Mean latency | 21.543 seconds |
| Latency range | 17.687-28.532 seconds |

All calls used `Qwen/Qwen3-8B`, G9, temperature zero, disabled thinking, and
the frozen 2,000-token output limit. The 2026-06-13 public pricing snapshot
listed Qwen3-8B input and output tokens at CNY 0 per million tokens. This is not
an account-billing claim.

## Primary Result

| Representation | Exact evidence | Strict aggregate |
|---|---:|---:|
| Binding separated | 15/15 | 10/15 |
| Claim coupled | 14/15 | 10/15 |

The exact-evidence risk difference was `0.067` in favor of binding separation,
below the preregistered engineering threshold of `0.20`. The two-sided Fisher
exact result was `p=1.000`.

The experiment therefore did not show an engineering-scale independent effect
from separating evidence bindings.

## Component Result

| Component | Binding separated | Claim coupled |
|---|---:|---:|
| Schema | 15/15 | 15/15 |
| Exact evidence arrays | 15/15 | 14/15 |
| Residual state | 10/15 | 11/15 |
| Transition | 15/15 | 15/15 |
| Complete gate | 15/15 | 15/15 |
| Attestation | 15/15 | 15/15 |
| Strict aggregate | 10/15 | 10/15 |

H3 gate control and H4 transition control passed. H1 separated robustness, H2
representation effect, and H5 surface transfer did not pass their
preregistered thresholds.

## Failure Audit

Ten runs failed the strict aggregate:

- nine retained the transitioned API-permission label in
  `forbidden_inferences`;
- one R1 distractor run remapped two exact evidence arrays.

The nine residual-state failures shared one exact pattern. v5.2 kept the
required post-state visible but omitted the redundant direct instruction used
by v5.1 to remove the matching forbidden-inference label. The failures remain
valid under the frozen contract, but this instruction-salience regression
means the strict 20/30 result should not be treated as a direct reliability
estimate for the fully explicit v5.1 repair.

## Interpretation

Supported:

> With a complete model-visible gate and exact postconditions, both evidence
> representations achieved near-perfect exact evidence retention in this
> 30-run Qwen3-8B + G9 slice.

Supported:

> Binding separation did not produce the preregistered engineering-scale
> improvement over claim-coupled evidence in this bounded experiment.

Supported:

> Exact gate and transition objects were preserved in 30/30 runs.

Not supported:

> Binding separation was the causal reason that v5.1 improved over v5.

Not supported:

> The repaired controlled-transition macro has a stable 66.7% success rate.

Not supported:

> Evidence representation never matters, or a smaller effect is absent.

The 15 runs per arm were designed to detect a large engineering effect. They
do not rule out a small effect.

## Decision

No additional run is required to answer the immediate ablation question. The
large independent contribution hypothesized for binding separation was not
observed.

Additional experiments are required for a different claim: stable reliability
of the complete controlled-transition macro. That work should begin with a new
local protocol restoring the explicit forbidden-inference removal operation.
It must not pool new runs with v5.2.

Stage C and Stage D remain blocked.

## Evidence Record

- Frozen protocol and local readiness: `P2-E160`
- Provider execution: `P2-E161`
- Preregistered evaluation and statistics: `P2-E162`
- Failure audit: `P2-E163`
- Decision boundary: `P2-E164`

