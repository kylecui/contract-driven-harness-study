# Stage B v3 Provider-Retry Amendment

Recorded: 2026-06-13

Timing: after the first execution attempt and before retry calls

## Trigger

The initial three-run execution produced:

- r1: one completed model response;
- r2: SiliconFlow HTTP 500 after 188 ms;
- r3: SiliconFlow HTTP 500 after 187 ms.

The two HTTP 500 attempts produced no model output and no provider usage
metadata. They are provider failures, not contract failures.

## Decision

Retry r2 and r3 once each with:

- byte-identical prompts;
- unchanged fixture, evaluator, model, G9 harness, temperature, thinking mode,
  timeout, and output-token limit;
- new run IDs;
- `attempt=2`;
- `lineage_id` and `retry_of_run_id` pointing to the original failed run.

The original HTTP 500 attempts remain in the event log and execution report.
Retry success cannot replace or erase them.

## Admission Accounting

The repair-smoke decision uses the first completed model response for each of
the three preregistered lineages:

- r1 completed on attempt 1;
- r2 may complete on attempt 2;
- r3 may complete on attempt 2.

If a retry also fails at the provider layer, the smoke remains incomplete and
cannot pass. No third attempt is authorized by this amendment.

## Rationale

Both failures were immediate HTTP 500 responses. Their timing and lack of model
output distinguish them from prompt-length, timeout, truncation, or evaluator
failures. A single lineage-preserving retry is therefore a runtime recovery,
not an outcome-driven protocol change.
