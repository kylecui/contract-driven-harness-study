# Adapter Usage Instrumentation Check

Check date: 2026-06-13

Scope: Stage A local instrumentation only

Provider calls: none

## Change

`research/04_methods/scripts/run_openai_adapter.py` now preserves, when
available:

- provider-reported prompt, completion, and total tokens;
- the raw provider usage object;
- response ID, response model, creation timestamp, and system fingerprint;
- the `x-request-id` response header;
- declared retry lineage (`lineage_id`, `attempt`, and `retry_of_run_id`);
- existing prompt/output byte and elapsed-time measurements.

When a provider omits usage metadata, the adapter records `usage: null`.
It does not estimate tokens from bytes.

## Local Verification

Commands:

```text
python -m unittest research/04_methods/scripts/test_run_openai_adapter.py
python -m py_compile research/04_methods/scripts/run_openai_adapter.py research/04_methods/scripts/test_run_openai_adapter.py
python research/04_methods/scripts/run_openai_adapter.py --manifest research/05_analysis/real-run-artifacts/first-slice-smoke-manifest.json --config research/04_methods/provider-config.siliconflow-reviewed.json --report C:/tmp/contract-harness-adapter-dry-run.json --event-log C:/tmp/contract-harness-adapter-dry-run-events.jsonl
```

Results:

- 3/3 unit tests passed;
- both Python modules compiled;
- 4/4 manifest entries were processed with `execute=false`;
- dry-run reports contain retry-lineage fields and null provider metadata;
- no network request or paid model call occurred.

## Remaining Stage A Work

- construct five representation-preserving variants for each selected macro;
- add golden and known-bad outputs for every variant;
- prove that aliases are accepted only when declared;
- prove that missing evidence obligations still fail;
- capture an official dated pricing snapshot immediately before Stage B.

Stage B remains blocked until these local gates pass and the user gives an
explicit go decision for 30 paid calls.
