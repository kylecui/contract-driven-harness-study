# Stage B v2 Early-Stop Summary

Executed: 2026-06-13

Decision: failed stop rule; Stage B v2 terminated early

## Result

The first cell, `stage7-next-method-plan-update-v2--canonical`, passed 0/3
runs. The preregistered threshold was at least 2/3 for every cell. Once the
second run failed, the cell could no longer reach the threshold; the third
request had already started and completed before the process was stopped.

Execution accounting:

| State | Runs |
|---|---:|
| Completed provider responses | 3 |
| Completed contract passes | 0 |
| Provider request started but aborted without response | 1 |
| Never started | 26 |

Stage B v2 fails. Stage C and Stage D remain blocked.

## Completed-Run Metrics

| Run | Task success | Schema | State | Grounding | Evidence type | Trace | Gate | Context |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| r1 | 0.714 | 0 | 0 | 1 | 1 | 1 | 1 | 1 |
| r2 | 0.714 | 0 | 0 | 1 | 1 | 1 | 1 | 1 |
| r3 | 0.714 | 0 | 0 | 1 | 1 | 1 | 1 | 1 |

The failure is narrow and repeatable. Evidence binding, evidence typing,
decision trace, stage gate, and carried obligations passed in all three runs.
The required hierarchical state structure failed in all three.

## Runtime Review

| Run | Elapsed | Prompt tokens | Completion tokens | Total tokens | Output bytes |
|---|---:|---:|---:|---:|---:|
| r1 | 86.172 s | 5163 | 1740 | 6903 | 6905 |
| r2 | 75.484 s | 5163 | 1657 | 6820 | 6585 |
| r3 | 76.188 s | 5163 | 1610 | 6773 | 6431 |
| Total | 237.844 s | 15489 | 5007 | 20496 | 19921 |

All three responses were valid, complete JSON. No completed call timed out, hit
the 3000-token limit, or returned a provider error. The public price snapshot
listed Qwen3-8B input and output tokens at CNY 0.00 per million tokens on
2026-06-13; account-specific billing is not asserted.

The fourth request,
`stage7-next-method-plan-update-v2--distractor-evidence__budget_model__G9__r1`,
was sent but terminated before a response event. Its placeholder output was not
replaced. It is retained as an aborted in-flight attempt, not a model result.

## Failure Pattern

The contract required:

```text
state_inventory
  known_state
  unknown_state
  forbidden_inferences
```

Observed:

- all three runs emitted `state_inventory` as the known-state array itself;
- r1 and r2 emitted `unknown_state` and `forbidden_inferences` at the root;
- r3 omitted `unknown_state` and `forbidden_inferences`;
- the rest of the contract was largely preserved.

This is not an evaluator typo. The golden output uses the required hierarchy,
the known-bad suite rejects missing nested fields, and the prompt names the
nested paths repeatedly.

## Root-Cause Judgment

The v2 contract used an explicit but descriptive template:

```text
"state_inventory": {
  "known_state": "array of ...",
  "unknown_state": "array of ...",
  "forbidden_inferences": "array of ..."
}
```

That description was insufficient for this model. It correctly recovered the
content obligations but compressed the hierarchy while constructing the final
JSON object.

The rejected assumption is:

> A descriptive output template plus repeated dotted-path constraints is
> sufficient to preserve a nested JSON hierarchy in Qwen3-8B.

The evidence does not reject contract-driven harnessing as a whole. It shows
that output hierarchy must itself be treated as a mechanism atom rather than a
minor schema detail.

## Plan Adjustment

Do not resume the remaining Stage B v2 queue and do not relax the evaluator.

Prepare a separately versioned repair protocol:

1. define a `hierarchical_output_shape_preservation` mechanism atom;
2. replace descriptive shape strings with one literal JSON skeleton containing
   every required nesting level and placeholder arrays;
3. add known-bads for flattened, root-promoted, and omitted nested state;
4. run local golden/known-bad gates;
5. run a three-call canonical repair smoke on the failed macro;
6. require at least 2/3 passes before preparing another full perturbation slice;
7. keep Stage B v2 evidence separate from the successor protocol.

A provider-native structured-output mode may later be tested as a separate
ablation. It must not be introduced silently because it changes the harness and
provider contract.

## Evidence

- Raw event log:
  `research/05_analysis/post-freeze-perturbation-pilot-v2-adapter-events.jsonl`
- Partial adapter report:
  `research/05_analysis/post-freeze-perturbation-pilot-v2-execution.json`
- Partial evaluation:
  `research/05_analysis/post-freeze-perturbation-pilot-v2-partial-evaluation.md`
- Machine-readable stop decision:
  `research/05_analysis/post-freeze-perturbation-pilot-v2-early-stop-decision.json`
- Per-run outputs and traces:
  `research/05_analysis/real-run-artifacts/post-freeze-perturbation-pilot-v2/`
