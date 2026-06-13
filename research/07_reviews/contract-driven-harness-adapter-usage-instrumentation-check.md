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
- the official `x-siliconcloud-trace-id` response header, with
  `x-request-id` retained as a compatibility fallback;
- declared retry lineage (`lineage_id`, `attempt`, and `retry_of_run_id`);
- the explicit `enable_thinking` request setting;
- existing prompt/output byte and elapsed-time measurements.

When a provider omits usage metadata, the adapter records `usage: null`.
It does not estimate tokens from bytes.

## Local Verification

Commands:

```text
python -B -m unittest research/04_methods/scripts/test_run_openai_adapter.py
python -m py_compile research/04_methods/scripts/run_openai_adapter.py research/04_methods/scripts/test_run_openai_adapter.py
python research/04_methods/scripts/run_openai_adapter.py --manifest research/05_analysis/real-run-artifacts/first-slice-smoke-manifest.json --config research/04_methods/provider-config.siliconflow-reviewed.json --report C:/tmp/contract-harness-adapter-dry-run.json --event-log C:/tmp/contract-harness-adapter-dry-run-events.jsonl
```

Results:

- 5/5 unit tests passed, including explicit non-thinking payload inclusion and
  unspecified-thinking omission;
- both Python modules compiled;
- 4/4 manifest entries were processed with `execute=false`;
- dry-run reports contain retry-lineage fields and null provider metadata;
- no network request or paid model call occurred.

## Stage A Completion

- five representation-preserving variants were constructed for each selected
  macro;
- golden and known-bad outputs pass their local expectations;
- aliases are accepted only when declared;
- missing evidence obligations still fail;
- the official dated pricing snapshot was captured on 2026-06-13;
- Stage B inference mode is frozen to `enable_thinking=false`.

Stage B remains blocked only until the user gives an explicit go decision for
30 provider calls.
