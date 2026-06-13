# Stage B 30-Run Perturbation Pilot Summary

Completed: 2026-06-13

Decision: **FAIL; STOP BEFORE STAGE C**

## Protocol

- Provider: SiliconFlow
- Model: `Qwen/Qwen3-8B`
- Harness: G9
- Temperature: 0
- Maximum completion tokens: 2000
- Thinking: disabled
- Design: 2 macros x 5 conditions x 3 repetitions = 30 runs

No fixture, prompt, output contract, or evaluator threshold was changed during
provider execution.

## Provider Execution

All 30 requests returned:

| Measure | Result |
|---|---:|
| Executed runs | 30/30 |
| Provider errors | 0 |
| Timeout retries | 0 |
| Median latency | 60.344 s |
| P90 latency | 74.309 s |
| Latency range | 51.969-84.250 s |
| Prompt tokens | 129,249 |
| Completion tokens | 48,297 |
| Total tokens | 177,546 |
| Reasoning tokens | 0 |
| Completions at 2,000-token limit | 2 |
| Public-list token charge | ¥0.00 |

The two limit-reaching completions were invalid truncated JSON in the Stage 7e
v4 field-alias condition. [P2-E128]

## Evaluator Deviation

The frozen evaluator initially scored 0/30 runs as complete contract passes.
Twenty-four outputs used `satisfied` as the carried-obligation status. The
outputs preserved the required obligation text and evidence, but the evaluator
accepted only `preserved`, `active`, `fulfilled`, `excluded`, or `enforced`.

Neither the prompt nor the output contract declared that closed vocabulary.
This was an evaluator construct-validity defect, not a semantic model failure.

A post-execution evaluator correction added `satisfied` as an accepted synonym.
The correction:

- did not change prompts, outputs, fixtures, thresholds, or other metrics;
- preserved 28/28 perturbation golden/known-bad expectations;
- preserved 4/4 original macro regression expectations;
- produced a separate v2 evaluation;
- does not make the pilot eligible for Stage C pooling.

The raw frozen-evaluator result remains preserved separately.
[P2-E129]

## Corrected Results

| Macro | Condition | Passed | Cell gate |
|---|---|---:|---|
| Stage 7-next method-plan update | Canonical | 3/3 | PASS |
| Stage 7-next method-plan update | Distractor evidence | 3/3 | PASS |
| Stage 7-next method-plan update | Evidence order shuffled | 3/3 | PASS |
| Stage 7-next method-plan update | Field alias | 0/3 | FAIL |
| Stage 7-next method-plan update | Unknown-state paraphrase | 0/3 | FAIL |
| Stage 7e v4 evidence decision | Canonical | 1/3 | FAIL |
| Stage 7e v4 evidence decision | Distractor evidence | 3/3 | PASS |
| Stage 7e v4 evidence decision | Evidence order shuffled | 2/3 | PASS |
| Stage 7e v4 evidence decision | Field alias | 1/3 | FAIL |
| Stage 7e v4 evidence decision | Unknown-state paraphrase | 0/3 | FAIL |

Totals:

- run pass: 16/30;
- cell pass: 5/10;
- macro pass: neither macro passed all five conditions.

The preregistered rule requires every macro-condition cell to pass at least
2/3 runs. Five cells failed, so Stage B fails.
[P2-E129]

## Failure Review

All 14 corrected-evaluation failures were inspected.

### Declared Unknown-State Surface

Six runs failed the unknown-state paraphrase condition. The model reverted to
canonical labels such as `current_git_branch` or emitted undeclared hybrids
such as `do_not_infer_branch_currently_checked_out` instead of the required
declared paraphrases.

This is a real representation-portability failure. The underlying unknown
state was usually preserved, but the declared output surface was not.

### Evidence-Complete Decision Trace

Six runs failed evidence-combination completeness:

- all three Stage 7-next field-alias runs omitted a required evidence item from
  `selected_claim`, even though the decision trace contained a valid broader
  combination;
- two Stage 7e v4 canonical runs omitted a required Stage 7e evidence item from
  the selected claim;
- one Stage 7e v4 shuffled run used an inadmissible selected-claim evidence
  combination and failed both grounding and trace checks.

These are real contract failures. The selected option was correct, but the
claim-level evidence binding was incomplete.

### Output-Budget Truncation

Two Stage 7e v4 field-alias runs reached exactly 2,000 completion tokens and
ended with incomplete JSON. The longer alias surface increased repeated field
text and exposed an output-budget weakness.

These are execution-level contract failures, not provider errors.

## What The Pilot Supports

Positive evidence:

- provider execution was stable across all 30 requests;
- distractor evidence passed 6/6 across both macros;
- evidence-order shuffling passed 5/6;
- Stage 7-next canonical passed 3/3;
- explicit non-thinking mode produced zero reasoning tokens and no provider
  timeout.

Negative evidence:

- exact declared surface aliases are not robust;
- evidence-combination retention is not stable across both macros;
- a 2,000-token output budget is insufficient for some expanded alias outputs;
- the current Stage B protocol does not justify stability expansion.

## Decision And Next Gate

Do not start Stage C or Stage D.

The next experimental step is a fresh Stage B v2 preparation:

1. declare an explicit JSON schema or template for alias-bearing outputs;
2. make selected-claim evidence combinations explicit and locally testable;
3. define the carried-obligation status vocabulary in the contract;
4. reduce repeated output material or raise the completion budget with a new
   preregistration;
5. add known-bad cases for canonical fallback, hybrid aliases, incomplete
   selected-claim evidence, and output truncation;
6. run local gates before authorizing fresh provider calls.

Because the evaluator and protocol require repair, these 30 runs must not be
pooled into Stage C. [P2-E130]

## Artifacts

- execution:
  `research/05_analysis/post-freeze-perturbation-pilot-stage-b-execution.json`
- adapter events:
  `research/05_analysis/post-freeze-perturbation-pilot-stage-b-adapter-events.jsonl`
- raw frozen evaluation:
  `research/05_analysis/post-freeze-perturbation-pilot-stage-b-evaluation.md`
- corrected evaluation:
  `research/05_analysis/post-freeze-perturbation-pilot-stage-b-evaluation-v2.md`
- corrected local gates:
  `research/05_analysis/post-freeze-perturbation-posthoc-local-gates.md`
- corrected base regression:
  `research/05_analysis/post-freeze-base-macro-regression-posthoc.md`
