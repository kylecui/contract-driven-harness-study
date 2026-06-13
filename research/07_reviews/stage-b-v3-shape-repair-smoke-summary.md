# Stage B v3 Hierarchical Shape Repair Smoke Summary

Executed: 2026-06-13

Decision: pass at 2/3; full Stage B v3 preparation admitted

## Result

The literal JSON skeleton repaired the target hierarchy in all three completed
lineages:

```text
state_inventory
  known_state
  unknown_state
  forbidden_inferences
```

Full-contract results were 2/3, meeting the preregistered admission threshold.

| Lineage | Completed attempt | Shape | Full contract | Task success |
|---|---:|---:|---:|---:|
| r1 | 1 | pass | fail | 0.857 |
| r2 | 2 | pass | pass | 1.000 |
| r3 | 2 | pass | pass | 1.000 |

This is a positive mechanism result with a narrow boundary. It supports
preparing the full perturbation slice; it does not establish stable reliability
from three runs.

## Provider Lineage

Initial attempts r2 and r3 returned SiliconFlow HTTP 500 in 188 ms and 187 ms.
They produced no model output. One byte-identical retry was permitted for each:

- original failures remain in the initial event log and execution report;
- retry prompts have identical SHA-256 hashes to their originals;
- retries use new run IDs, `attempt=2`, and explicit `retry_of_run_id`;
- both retries completed successfully.

Five provider requests produced three completed model responses and two
provider errors.

## Mechanism Finding

Stage B v2 used a descriptive template and produced a flattened state hierarchy
in 3/3 runs. Stage B v3 replaced that one factor with a literal JSON skeleton.
All three completed v3 responses retained the nested state object.

This supports the bounded claim:

> For this macro and model, a literal copyable JSON skeleton repaired the
> observed hierarchical output-shape failure.

It does not prove arbitrary JSON-schema adherence or provider-native structured
output reliability.

## Remaining Failure

r1 passed schema and state metrics but failed `citation_grounding`. Its
`grounded_claims` used evidence e01, e07, and e06, omitting e04 and e08 from the
required grounded combination. r2 and r3 emitted four grounded claims covering
e01, e04, e07, and e08 and passed.

The literal skeleton currently contains one generic `grounded_claims` slot.
That can invite list compression even though the selected-claim evidence set is
explicit elsewhere.

Therefore the full Stage B v3 template should:

1. retain the literal nested state skeleton;
2. expand `grounded_claims` to explicit slots for e01, e04, e07, and e08;
3. retain a distinct selected C2 claim slot with e01, e06, e07, and e08;
4. add a known-bad fixture for compressed grounded evidence;
5. rerun local gates before any full-slice provider execution.

This is a pre-execution template refinement for the next protocol, not a
rescore of the smoke.

## Runtime

Completed responses:

| Lineage | Elapsed | Prompt tokens | Completion tokens | Total tokens |
|---|---:|---:|---:|---:|
| r1 | 51.375 s | 6350 | 1706 | 8056 |
| r2 | 29.234 s | 6350 | 1838 | 8188 |
| r3 | 22.531 s | 6350 | 1824 | 8174 |
| Total | 103.140 s | 19050 | 5368 | 24418 |

No completed response timed out, truncated, or approached the 3000-token output
limit. The dated public price snapshot listed Qwen3-8B token charges at CNY
0.00 per million tokens; account-specific billing is not asserted.

## Validity Boundary

- Three lineages form a repair gate, not a stability estimate.
- Only one macro was tested.
- Exact state IDs in the skeleton add guidance beyond abstract nesting.
- Two initial provider errors show runtime availability remains a separate
  reliability concern.
- The full contract passed only at the minimum admitted threshold.

## Decision

The `hierarchical_output_shape_preservation` atom passes this smoke. Prepare a
separately versioned full Stage B v3 perturbation protocol with explicit
grounded-claim slots. Do not pool v2 and v3 results, and do not execute the full
slice without a new approval.
