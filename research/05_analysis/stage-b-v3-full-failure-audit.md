# Stage B v3 Failure Audit

Audited: 2026-06-14

Scope: all 12 failed semantic evaluations

## Failure Classification

| Failure class | Runs | Evidence |
|---|---:|---|
| Grounding only | 6 | Required evidence support absent from `grounded_claims` |
| Surface/state only | 3 | Required paraphrased forbidden-inference labels rewritten |
| Both | 3 | Grounding support absent and paraphrased labels rewritten |
| Provider/runtime | 0 | All calls returned `executed` |
| JSON/truncation | 0 | All outputs parsed; maximum completion was 2,013 tokens |

## Missing Grounded Support

Nine runs failed the exact grounded-support union:

- Stage 7-next canonical r1-r3 omitted `stage7next-e06`;
- Stage 7-next field-alias r1 omitted `stage7next-e06`;
- Stage 7-next unknown-state-paraphrase r1-r3 omitted `stage7next-e06`;
- Stage 7e v4 canonical r2-r3 omitted `stage7e-e08`.

The outputs retained the required number of grounded-claim objects but replaced
the frozen evidence arrays with other valid evidence IDs. This is a true
content-preservation miss: the model preserved the container while rewriting
the slot.

## Paraphrased State Labels

All six unknown-state-paraphrase runs emitted the required unknown-state values
but changed the required forbidden-inference prefix:

Required:

- `do_not_guess_branch_currently_checked_out`
- `do_not_guess_continuous_integration_result`
- `do_not_guess_permission_to_use_external_model_api`

Emitted:

- `do_not_infer_branch_currently_checked_out`
- `do_not_infer_continuous_integration_result`
- `do_not_infer_permission_to_use_external_model_api`

The emitted labels are semantically plausible but undeclared. The evaluator
correctly rejected them because this condition tests exact declared surface
retention, not semantic similarity.

## Evaluator Audit

The failed runs were checked against:

- the model-visible literal skeleton;
- the evaluator-only canonical and alias maps;
- the exact array-count rules;
- the required surface values;
- the raw model outputs.

No evaluator correction is warranted:

- the expected labels are present in the model-visible contract;
- the expected evidence arrays are present in the literal skeleton;
- local golden outputs pass;
- known-bad substitutions are rejected;
- passing real outputs satisfy the same evaluator.

Unlike Stage B v1, this result does not depend on a post-execution evaluator
repair.

## Mechanism Diagnosis

The v3 package combined two mechanisms:

1. hierarchical shape preservation;
2. exact content-slot preservation.

The first mechanism largely worked. The second did not. A literal example is
therefore insufficient to make arrays or closed-vocabulary tokens immutable
for Qwen3-8B in these macros.

The next repair should not add more prose to the same large contract. It should
test smaller copy-preservation atoms:

- fixed evidence arrays with prose fields as the only editable positions;
- enumerated closed-vocabulary labels with substitution known-bads;
- a validator-visible distinction between editable and immutable fields;
- targeted smoke runs before recomposition.

## Retry Decision

No retries are authorized for these 12 failures. Each call produced a complete
semantic answer, and retrying would change the sampling record rather than
recover a failed provider attempt.
