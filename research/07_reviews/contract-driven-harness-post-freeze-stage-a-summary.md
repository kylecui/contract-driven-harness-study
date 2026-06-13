# Post-Freeze Stage A Summary

Completed: 2026-06-13

Scope: local instrumentation, perturbation fixtures, evaluator gates, and
30-run queue preparation

Paid provider calls: none

## Result

Stage A local gates passed. Stage B was subsequently authorized and executed
on 2026-06-13. Its outcome is recorded separately and does not change the
Stage A local-gate result.

## Perturbation Suite

The generated suite contains:

```text
2 macros x 5 conditions = 10 fixtures
```

Conditions:

1. canonical contract;
2. evidence order shuffled;
3. declared `evidence_ids` to `source_references` alias;
4. declared unknown-state paraphrases;
5. irrelevant but plausible distractor evidence.

Local evaluator result:

- 10/10 golden outputs passed;
- 18/18 known-bad outputs failed;
- 0 expectation failures;
- known-bad failures occurred on their predeclared target metrics.

The two extra known-bad cases verify that `source_references` is rejected when
the contract does not declare the alias.

## Evaluator Deviation And Repair

The first local run stopped with 2/22 expectation failures. Both involved the
undeclared field-alias negative case.

Cause:

- the known-state evaluator flattened keys and values into text;
- evidence IDs remained visible under the undeclared `source_references` key;
- `state_accuracy` therefore passed without a real `evidence_ids` field.

Repair:

- require `known_state` to be an object array;
- require every entry to contain `state_id`, `fact`, and a nonempty canonical
  `evidence_ids` list;
- canonicalize only aliases declared by the fixture contract.

After repair:

- 22/22 perturbation cases met expectations;
- 4/4 original Stage 7e v4 and Stage 7-next golden/known-bad regression cases
  preserved prior behavior.

The final surface-contract expansion added six more negative cases covering
fallback to canonical field names, fallback to canonical unknown-state labels,
and distractor evidence mixed with otherwise valid support. The final suite
passes 28/28 local cases.

This was an evaluator defect, not a model result. No paid execution had begun,
so no run was discarded or retroactively rescored.

## Stage B Queue

Prepared design:

```text
2 macros x 5 conditions x 3 repetitions = 30 runs
```

All runs use:

- model tier: low-cost model;
- provider model: `Qwen/Qwen3-8B`;
- harness: G9;
- temperature: 0;
- maximum output tokens: 2000;
- thinking mode: explicitly disabled.

Readiness:

- 30 packets compiled;
- 30 prompt/request artifacts generated;
- preflight: PASS, 0 errors, 0 warnings;
- adapter dry-run: 30/30 processed with `execute=false`;
- API key environment variable detected;
- no model request sent.

## Artifacts

- suite: `research/04_methods/macro-perturbations/`
- builder: `research/04_methods/scripts/build_macro_perturbation_suite.py`
- preregistration: `research/05_analysis/post-freeze-perturbation-pilot-preregistration.md`
- local gates: `research/05_analysis/post-freeze-perturbation-local-gates.md`
- base regression: `research/05_analysis/post-freeze-base-macro-regression.md`
- matrix: `research/04_methods/benchmark-matrix-post-freeze-perturbation-pilot.json`
- prompt manifest: `research/05_analysis/real-run-artifacts/post-freeze-perturbation-pilot-manifest-with-prompts.json`
- preflight: `research/05_analysis/post-freeze-perturbation-pilot-preflight.md`

## Decision

Stage A local work: **PASS**

Pricing snapshot: **COMPLETE**

Stage B paid execution: **COMPLETED; FAILED STAGE B STOP RULE**

See
`research/07_reviews/contract-driven-harness-stage-b-30-run-summary.md`.
