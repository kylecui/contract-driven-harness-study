# Stage 7r Failure And Timeout Analysis

Date: 2026-06-08

## Question

After Stage 7r, there were 36 planned SiliconFlow smoke runs, 35 completed outputs, and 1 pending timeout. This memo reviews every non-passing or pending run and separates expected baseline failure, real mechanism failure, evaluator/contract implications, and execution timeout.

## Execution Logging Caveat

The current adapter does not write a full incremental execution log. It writes:

- model output files after each successful provider call,
- tool trace files after each successful provider call,
- one final adapter report only after the entire manifest finishes.

When an outer command timeout kills the adapter before it reaches final report writing, earlier successful output files remain, but the full adapter report is absent. Therefore, the available evidence is:

- per-run output files,
- per-run validation reports,
- retry adapter reports that completed,
- manifest order,
- file timestamps,
- adapter source behavior.

This is sufficient to identify the failed request and classify the visible failure mode, but it is not sufficient to reconstruct provider-side latency, queueing, token generation rate, or partial server responses.

## Pending Timeout

Pending run:

- `a8r-evidence-type-rules__budget_model__G8__r1`
- Provider/model: SiliconFlow `Qwen/Qwen3-8B`
- Initial state: left pending after the 36-run smoke reached the tail of the manifest.
- Retry 1: included the pending G8 and following G9 run; G9 completed, but G8 did not produce output before report completion was interrupted.
- Retry 2: single-run retry with default config failed with `The read operation timed out`.
- Retry 3: single-run controlled retry with `timeout_seconds=900` and `max_output_tokens=600` also failed with `The read operation timed out`.

Manifest order confirms A8R low-cost G8 is run 35/36 and A8R low-cost G9 is run 36/36. Since G9 eventually completed and passed, the fixture itself is not globally broken.

Prompt size is not a convincing explanation. A8R low-cost G8 has a 3179-byte prompt, while completed low-cost G8/G9 prompts include larger prompts such as A7R G8 at 3508 bytes and A7R G9 at 3613 bytes.

Most likely interpretation:

- provider/model long-tail timeout for this specific request path,
- possibly triggered by the interaction of `Qwen/Qwen3-8B`, G8 packet shape, and A8R evidence-type classification,
- not enough evidence to call it a model-quality failure.

Required instrumentation improvement:

- add an incremental adapter event log with `run_start`, `provider_request_start`, `provider_response_end`, `provider_error`, elapsed seconds, and status per run,
- write the report incrementally after each run,
- optionally add retry count and request hash to distinguish provider instability from deterministic prompt failure.

## Expected G0 Baseline Failures

All strong-model G0 failures were output-contract failures rather than semantic incompetence. The strong model often gave reasonable prose but did not return the strict JSON shape because G0 intentionally withholds output contracts.

Examples:

- A3R strong G0 produced a correct safe action plan in Markdown, but failed JSON schema.
- A4R strong G0 correctly separated known/unknown state in prose, but failed JSON schema.
- A5R strong G0 correctly blocked synthesis/recommendation in prose, but failed JSON schema.
- A7R strong G0 selected C2 and rejected C1/C3 in prose, but failed JSON schema.
- A8R strong G0 correctly classified items in prose, but failed JSON schema.

Low-cost G0 was mixed:

- A3R low-cost G0 was semantically good and primary mechanism passed, but schema was incomplete, so overall task_success stayed below threshold.
- A2R, A5R, A7R, and A8R low-cost G0 produced partial or wrong schema and failed the relevant mechanism criteria.

Interpretation:

- G0 failures are expected and useful as baseline contrast.
- They show that much of the harness benefit comes from explicit output contracts and mechanism-specific obligations.

## Real G8/G9 Mechanism Failures

The completed G8/G9 failures are concentrated in two low-cost-model mechanism obligations.

### A2R Unsupported Claim Detection

Failed runs:

- `a2r-unsupported-claim-detection__budget_model__G8__r1`
- `a2r-unsupported-claim-detection__budget_model__G9__r1`

Observed output:

- included required top-level fields,
- identified the two grounded claims,
- identified `production readiness` as unsupported,
- listed `atom-a2r-e01` and `atom-a2r-e02` globally,
- did not bind each grounded claim to its own evidence IDs.

Reason for failure:

- strict citation grounding requires claim-level evidence binding, not a global evidence list.

Interpretation:

- This is not a complete task failure.
- The low-cost model understood the unsupported claim boundary but did not satisfy the per-claim evidence contract.

Optimization target:

- strengthen output contract from "required sections + citation policy" to an explicit JSON schema:
  - `grounded_claims[] = {claim, evidence_ids[]}`,
  - `unsupported_claims[] = {claim, reason}`,
  - no bare strings allowed in `grounded_claims`.

### A7R Enumerated Claim Decision

Failed runs:

- `a7r-enumerated-claim-decision__budget_model__G8__r1`
- `a7r-enumerated-claim-decision__budget_model__G9__r1`

Observed output:

- selected the correct option `C2`,
- rejected `C1` and `C3`,
- cited evidence for C2 and C1,
- omitted an evidence-linked trace step for rejecting C3.

Reason for failure:

- strict trace completeness requires evidence-linked handling of both rejected options, especially C3 with `atom-a7r-e03`.

Interpretation:

- The low-cost model got the decision right but did not complete the full audit trace.
- This is a trace-completeness failure rather than a decision-choice failure.

Optimization target:

- revise A7R contract to require:
  - `selected_option_id`,
  - `rejected_options[] = {option_id, reason, evidence_ids[]}`,
  - `decision_trace[]` must include at least one step for selected option and one step per rejected option,
  - no rejected option may be listed without evidence.

## Passed Mechanisms

Clear positives:

- A3R constraint-safe plan: both model tiers pass under G8/G9.
- A5R stage-gate check: both model tiers pass under G8/G9.
- A4R strict state inventory: both model tiers pass under G8/G9 after evaluator normalization for structured key/value state output.
- A8R evidence-type rules: strong model passes under G8/G9; low-cost model passes under G9; G8 remains execution-timeout pending rather than model-failed.

Strong model:

- strong_model G8/G9 passed 6/6 completed revised atoms.

Low-cost model:

- low-cost G0 passed 0/6.
- low-cost G8 completed 5/6 and passed 3/5.
- low-cost G9 completed 6/6 and passed 4/6.

## Next Step Decision

Do not proceed directly into a broad project-initialization or research-workflow macro task.

Recommended next stage:

1. Add adapter instrumentation so future timeouts have complete per-run logs.
2. Create Stage 7r.1 contract revisions for A2R and A7R only.
3. Run local golden/bad regression for A2R/A7R revised contracts.
4. Run a small targeted real smoke:
   - A2R revised and A7R revised,
   - low-cost model only,
   - G8/G9,
   - 2 repetitions if budget permits.
5. Treat A8R G8 timeout as a documented execution deviation unless a later provider reroute is needed.

If A2R/A7R pass after contract tightening, the next composition candidate should be a narrow evidence-bound decision macro, not full project initialization or full research workflow.
