# Stage B v5 State-Transition Smoke Result Quality Review

Reviewed: 2026-06-14

Overall rating: A for a negative-result debugging record

Blocking issues: none for publishing this stage record

## Reviewed Artifacts

- preregistered smoke plan and frozen matrix;
- adapter dry-run, preflight, execution, and event logs;
- four raw prompts, outputs, traces, validation reports, and metric records;
- strict evaluation output;
- failure audit;
- result summary.

## Nine-Dimension Review

| Dimension | Rating | Review |
|---|---|---|
| Question alignment | Pass | The record distinguishes transition execution from retention and gate obligations. |
| Evidence completeness | Pass | Raw outputs, usage, latency, retries, component metrics, and field-level audit are retained. |
| Citation coverage | Pass | Execution maps to P2-E151, strict evaluation to P2-E152, and attribution/decision to P2-E153. |
| Logic chain | Pass | The strict fail is preserved while posthoc analysis limits attribution rather than changing the verdict. |
| Counter-evidence | Pass | Four successful transition components are reported alongside the aggregate failure. |
| Method fit | Pass | Exact equality is appropriate for declared immutable arrays; the hidden gate field is separately identified as unfair. |
| Actionability | Pass | v5.1 local repairs are specific and provider rerun remains blocked. |
| Expression quality | Pass | The report avoids calling 0/4 a transition failure or 4/4 transition success a macro pass. |
| Risk disclosure | Pass | Small sample, editable-prose confound, and evaluator-contract mismatch are explicit. |

## Independent Numerical Checks

- Four execution records have status `executed`.
- No retry lineage exceeds attempt one.
- Four evaluated runs have `passed=false`.
- Schema, residual state, transition, and attestation each pass 4/4.
- Evidence and strict gate each pass 0/4.
- Nine of 16 grounded slot arrays are exact.
- Every gate mismatch is limited to `next_action`.
- Prompt tokens sum to 8,320.
- Completion tokens sum to 2,178.
- Total tokens sum to 10,498.
- Reasoning tokens sum to zero.
- Latency ranges from 21.422 to 26.500 seconds; median is 21.938 seconds.

## Residual Risks

The evidence failure may be amplified by allowing claim prose to change while
requiring evidence arrays to remain fixed. That is still a contract failure,
but it introduces a mechanism unrelated to the target state transition.

The gate field mismatch is a protocol defect. It must be repaired before the
gate metric can support any model-level claim.

Four runs reveal a repeatable pattern but do not estimate a stable failure
rate.

## Decision

Approve publication of Stage B v5-state-transition-smoke as a failed strict
protocol with successful transition subcomponents and a documented gate
fairness defect. Approve Stage B v5.1-local design. Do not approve another
provider run until the repaired local gate passes and the user separately
authorizes execution.
