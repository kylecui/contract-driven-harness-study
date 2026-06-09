# Research Method Scripts

## `label_token_trajectory.py`

Reads an existing `ab_test_results.json` and produces token-only trajectory labels. This is a screening tool, not a substitute for full message/tool-call inspection.

Example:

```powershell
python research/04_methods/scripts/label_token_trajectory.py `
  --input proposal/01-Topic-Aware-Compaction/data/experiment-2-fishtrial-ab/ab_test_results.json `
  --output-json research/05_analysis/token-trajectory-labels.json `
  --output-md research/05_analysis/token-trajectory-label-report.md
```

## `harness_benchmark_metrics.py`

Reads benchmark run metrics and computes cross-model gap compression ratios by harness arm.

Example:

```powershell
python research/04_methods/scripts/harness_benchmark_metrics.py `
  --input research/04_methods/sample-harness-runs.json `
  --baseline-arm G0 `
  --output-json research/05_analysis/sample-harness-metrics.json `
  --output-md research/05_analysis/sample-harness-metrics.md
```

## `export_opencode_session_messages.py`

Exports raw OpenCode session messages for a preserved session. Use this after A/B harness runs so trajectory labels can be based on actual message/tool text rather than token-only heuristics.

Example:

```powershell
python research/04_methods/scripts/export_opencode_session_messages.py `
  --port 3100 `
  --session-id ses_xxx `
  --password test `
  --output research/02_notes/baseline-session-messages.json
```

## `validate_harness_fixtures.py`

Checks that each benchmark fixture directory has the required JSON files and that IDs link correctly.

Example:

```powershell
python research/04_methods/scripts/validate_harness_fixtures.py `
  --fixtures-dir research/04_methods/benchmark-fixtures
```

## `generate_benchmark_matrix.py`

Expands fixtures, model tiers, harness arms, and repetitions into a planned run matrix.

Example:

```powershell
python research/04_methods/scripts/generate_benchmark_matrix.py `
  --fixtures-dir research/04_methods/benchmark-fixtures `
  --output research/04_methods/benchmark-matrix.json
```

First real-run slice:

```powershell
python research/04_methods/scripts/generate_benchmark_matrix.py `
  --fixtures-dir research/04_methods/benchmark-fixtures `
  --fixtures structured-extraction project-initialization `
  --models strong_model budget_model `
  --arms G0 G9 `
  --repetitions 3 `
  --output research/04_methods/benchmark-matrix-first-real-slice.json
```

## `compile_benchmark_packets.py`

Dry-runs the benchmark matrix by compiling each planned run into a model-adapter packet summary. It does not call a model.

Example:

```powershell
python research/04_methods/scripts/compile_benchmark_packets.py `
  --matrix research/04_methods/benchmark-matrix.json `
  --output-jsonl research/05_analysis/benchmark-packet-dry-run.jsonl `
  --output-md research/05_analysis/benchmark-packet-dry-run.md
```

## `run_mock_harness_benchmark.py`

Runs a deterministic mock benchmark over compiled packet summaries. This is only for pipeline validation; it is not evidence about real models.

Example:

```powershell
python research/04_methods/scripts/run_mock_harness_benchmark.py `
  --packets-jsonl research/05_analysis/benchmark-packet-dry-run.jsonl `
  --output research/05_analysis/mock-harness-runs.json
```

## `prepare_real_run_artifacts.py`

Prepares per-run artifact directories for a real model-backed benchmark slice. It does not call a model.

Example:

```powershell
python research/04_methods/scripts/prepare_real_run_artifacts.py `
  --packets-jsonl research/05_analysis/benchmark-first-real-slice-packets.jsonl `
  --runs-dir research/05_analysis/real-run-artifacts/first-slice `
  --output-manifest research/05_analysis/real-run-artifacts/first-slice-manifest.json
```

## `evaluate_real_run_artifacts.py`

Evaluates filled run artifacts for the first benchmark slice and writes `validation_report.json` plus `metrics.json` per run. Placeholder outputs score as pending.

Example:

```powershell
python research/04_methods/scripts/evaluate_real_run_artifacts.py `
  --manifest research/05_analysis/real-run-artifacts/first-slice-manifest.json `
  --output-runs research/05_analysis/first-slice-evaluated-runs.json `
  --output-md research/05_analysis/first-slice-evaluation-summary.md
```

Golden fixture examples:

- `research/04_methods/benchmark-fixtures/structured-extraction/golden_output.json`
- `research/04_methods/benchmark-fixtures/project-initialization/golden_output.md`

## `export_model_prompts.py`

Renders each compiled full packet into `prompt.md` and `adapter_request.json` files inside prepared run artifact directories. It does not call a model.

Example:

```powershell
python research/04_methods/scripts/export_model_prompts.py `
  --packets-jsonl research/05_analysis/benchmark-first-real-slice-full-packets.jsonl `
  --manifest research/05_analysis/real-run-artifacts/first-slice-manifest.json `
  --output-manifest research/05_analysis/real-run-artifacts/first-slice-manifest-with-prompts.json
```

## `build_adapter_queue.py`

Creates a human-readable queue from a prompt manifest.

Example:

```powershell
python research/04_methods/scripts/build_adapter_queue.py `
  --manifest research/05_analysis/real-run-artifacts/first-slice-manifest-with-prompts.json `
  --output research/05_analysis/first-slice-adapter-queue.md
```

## `select_manifest_runs.py`

Selects a subset of runs from a prepared manifest for smoke tests or partial reruns. It does not copy artifacts; selected runs still point to the original per-run artifact directories.

Example:

```powershell
python research/04_methods/scripts/select_manifest_runs.py `
  --manifest research/05_analysis/real-run-artifacts/first-slice-manifest-with-prompts.json `
  --output research/05_analysis/real-run-artifacts/first-slice-smoke-manifest.json `
  --fixtures structured-extraction `
  --models strong_model,budget_model `
  --arms G0,G9 `
  --repetitions 1
```

## `validate_provider_config.py`

Checks the provider/model-tier mapping before real model calls.

Example:

```powershell
python research/04_methods/scripts/validate_provider_config.py `
  --config research/04_methods/provider-config.siliconflow-reviewed.json
```

## `run_openai_adapter.py`

OpenAI-compatible adapter for the first real slice. It defaults to dry-run mode and does not call a model unless `--execute` is passed.

Dry run:

```powershell
python research/04_methods/scripts/run_openai_adapter.py `
  --manifest research/05_analysis/real-run-artifacts/first-slice-manifest-with-prompts.json `
  --config research/04_methods/provider-config.openai-reviewed.json `
  --report research/05_analysis/openai-adapter-dry-run.json
```

Real execution:

```powershell
$env:OPENAI_API_KEY = "<redacted>"
python research/04_methods/scripts/validate_provider_config.py `
  --config research/04_methods/provider-config.openai-reviewed.json `
  --require-keys
python research/04_methods/scripts/run_openai_adapter.py `
  --manifest research/05_analysis/real-run-artifacts/first-slice-manifest-with-prompts.json `
  --config research/04_methods/provider-config.openai-reviewed.json `
  --report research/05_analysis/openai-adapter-execution.json `
  --execute
```

## `preflight_real_model_pilot.py`

Runs local-only readiness checks before model-backed execution. It verifies manifest paths, adapter requests, validation statuses, provider mappings, and API-key environment variable presence without calling a model.

Example:

```powershell
python research/04_methods/scripts/preflight_real_model_pilot.py `
  --manifest research/05_analysis/real-run-artifacts/first-slice-manifest-with-prompts.json `
  --config research/04_methods/provider-config.openai-reviewed.json `
  --output-md research/05_analysis/first-slice-real-run-preflight.md `
  --output-json research/05_analysis/first-slice-real-run-preflight.json
```

Use `--require-keys` when checking a real execution environment.

## `collect_run_metrics.py`

Collects per-run `metrics.json` files into one runs payload for `harness_benchmark_metrics.py`.

Example:

```powershell
python research/04_methods/scripts/collect_run_metrics.py `
  --manifest research/05_analysis/real-run-artifacts/first-slice-manifest-with-prompts.json `
  --output-json research/05_analysis/first-slice-collected-runs.json `
  --output-md research/05_analysis/first-slice-collected-runs.md
```

## `postprocess_real_model_pilot.py`

Runs the local-only post-execution pipeline after provider outputs have been written. It evaluates artifacts, collects only completed metrics, and computes gap-compression metrics only when enough completed baseline and harness runs exist.

Example:

```powershell
python research/04_methods/scripts/postprocess_real_model_pilot.py `
  --manifest research/05_analysis/real-run-artifacts/first-slice-manifest-with-prompts.json `
  --output-prefix research/05_analysis/first-slice-postprocess `
  --baseline-arm G0
```

## `run_smoke_pilot_once.py`

Runs the four-run smoke workflow end to end: preflight, adapter, and postprocess. By default it is dry-run only. Real provider execution requires both `--execute` and `--confirm-cost`.

Dry run:

```powershell
python research/04_methods/scripts/run_smoke_pilot_once.py `
  --output-prefix research/05_analysis/smoke-pilot-once-dry-run
```

Real execution after key and budget approval:

```powershell
python research/04_methods/scripts/run_smoke_pilot_once.py `
  --config research/04_methods/provider-config.siliconflow-reviewed.json `
  --output-prefix research/05_analysis/smoke-pilot-once-execution `
  --execute `
  --confirm-cost
```
