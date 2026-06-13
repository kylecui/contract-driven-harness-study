# Stage B v3 Post-Execution Integrity Check

Checked: 2026-06-14

| Check | Result |
|---|---:|
| Frozen files | 425 |
| Changed frozen files | 120 |
| Expected mutable changes | 120 |
| Unexpected changes | 0 |
| Evidence-ledger JSONL errors | 0 |
| Credential-pattern findings | 0 |

The 120 expected changes are four per-run artifacts across 30 runs:

- `output.md`;
- `tool_trace.jsonl`;
- `validation_report.json`;
- `metrics.json`.

No frozen prompt, adapter request, fixture, output contract, evaluator, matrix,
provider configuration, or preregistration file changed after execution began.
