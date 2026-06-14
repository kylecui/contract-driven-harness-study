# Stage B v5.4 Explicit-Delta Stability Result

Executed: 2026-06-14

Decision: bounded stability confirmed

## Result

The frozen explicit-transition-delta protocol passed all preregistered gates.

| Metric | Pass | Rate | Wilson 95% |
|---|---:|---:|---|
| Strict controlled mutation | 40/40 | 1.000 | [0.912, 1.000] |
| Schema | 40/40 | 1.000 | [0.912, 1.000] |
| Evidence arrays | 40/40 | 1.000 | [0.912, 1.000] |
| Residual state | 40/40 | 1.000 | [0.912, 1.000] |
| Transition | 40/40 | 1.000 | [0.912, 1.000] |
| Complete gate | 40/40 | 1.000 | [0.912, 1.000] |
| Attestation | 40/40 | 1.000 | [0.912, 1.000] |

Every perturbation condition passed 8/8: canonical, field alias, evidence
order shuffled, distractor evidence, and unknown-state paraphrase.
[E:P2-E171]

## Execution

- completed calls: 40/40;
- provider errors: 0;
- retries: 0;
- valid JSON outputs: 40/40;
- prompt tokens: 83,312;
- completion tokens: 19,672;
- total tokens: 102,984;
- latency: 15.172-25.047 seconds;
- median latency: 19.500 seconds;
- P90 latency: 22.183 seconds.

[E:P2-E170]

## Freeze Integrity

The pre-execution manifest recorded 384 files. After execution, 160 files
changed: one output, metrics file, trace, and validation report for each of 40
runs. No frozen prompt, fixture, contract, evaluator, threshold, analysis
script, provider configuration, or manifest changed. [E:P2-E169; E:P2-E171]

## Combined Interpretation

Stage B v5.3 remains a mixed causal result. Explicit delta passed 15/15 while
the exact-postcondition baseline passed 13/15, but the `0.133` risk difference
did not reach the preregistered `0.20` threshold. [E:P2-E167; E:P2-E168]

Stage B v5.4 answers a separate question. It confirms that the frozen
explicit-delta protocol maintained exact contract adherence over 40 fresh
runs and five bounded perturbations. [E:P2-E172]

Supported claim:

> Under the frozen explicit-transition-delta G9 protocol, Qwen3-8B completed
> this controlled multi-array state mutation in 40/40 fresh runs across five
> tested perturbations.

Not supported:

- a large causal advantage over exact postconditions;
- arbitrary state-machine reliability;
- autonomous tool execution;
- rollback or concurrent transition correctness;
- workflow or production readiness;
- task-family generalization.

## Next Decision

The positive stability attachment is complete. The next provider experiment,
if pursued, should be a separately preregistered matched overhead matrix.
Otherwise, v5.3 and v5.4 should enter a new v4 paper draft while v3.1.1 remains
frozen.
