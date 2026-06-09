# First-Slice Real-Run Runbook

This runbook is for the first model-backed pilot of Project 2. It does not replace the evidence ledger; update the ledger only after real model outputs are produced, evaluated, and collected.

## Scope

- Manifest: `research/05_analysis/real-run-artifacts/first-slice-manifest-with-prompts.json`
- Planned runs: 24
- Fixtures: `structured-extraction`, `project-initialization`
- Model tiers: `strong_model`, `budget_model`
- Arms: `G0`, `G9`
- Repetitions: 3

## Hard Gates

Do not run `run_openai_adapter.py --execute` until all of these are true:

- Model IDs in the provider config have been confirmed against official docs and the actual provider account.
- API credentials are available in the configured environment variable.
- Budget and network/API execution have explicit approval.
- `preflight_real_model_pilot.py --require-keys` has 0 errors.
- The current artifact state is understood; non-placeholder outputs should not be overwritten accidentally.

## Provider Configs

- OpenAI reviewed config: `research/04_methods/provider-config.openai-reviewed.json`
- SiliconFlow reviewed config: `research/04_methods/provider-config.siliconflow-reviewed.json`

For SiliconFlow, set `SILICONFLOW_API_KEY` in the shell environment before real execution. The reviewed smoke config maps `strong_model` to `deepseek-ai/DeepSeek-V3.2` and `budget_model` to `Qwen/Qwen3-8B`.

## Step 1: Preflight

```powershell
python research/04_methods/scripts/preflight_real_model_pilot.py `
  --manifest research/05_analysis/real-run-artifacts/first-slice-manifest-with-prompts.json `
  --config research/04_methods/provider-config.siliconflow-reviewed.json `
  --output-md research/05_analysis/first-slice-real-run-preflight.md `
  --output-json research/05_analysis/first-slice-real-run-preflight.json `
  --require-keys
```

Expected before real execution:

- Errors: 0
- API key present: yes
- Config file is no longer merely an unreviewed example
- Validation statuses may still be pending

## Step 2: Optional One-Run Smoke Test

Use this only after approval. Prefer the four-run smoke manifest because it preserves the minimum strong/budget and G0/G9 comparison while avoiding the full 24-run cost.

Create or refresh the smoke manifest:

```powershell
python research/04_methods/scripts/select_manifest_runs.py `
  --manifest research/05_analysis/real-run-artifacts/first-slice-manifest-with-prompts.json `
  --output research/05_analysis/real-run-artifacts/first-slice-smoke-manifest.json `
  --fixtures structured-extraction `
  --models strong_model,budget_model `
  --arms G0,G9 `
  --repetitions 1 `
  --note "Four-run smoke subset for first-slice model-backed pilot."
```

Preflight the smoke manifest:

```powershell
python research/04_methods/scripts/preflight_real_model_pilot.py `
  --manifest research/05_analysis/real-run-artifacts/first-slice-smoke-manifest.json `
  --config research/04_methods/provider-config.siliconflow-reviewed.json `
  --output-md research/05_analysis/first-slice-smoke-preflight.md `
  --output-json research/05_analysis/first-slice-smoke-preflight.json `
  --require-keys
```

Then execute the four smoke runs:

```powershell
python research/04_methods/scripts/run_smoke_pilot_once.py `
  --config research/04_methods/provider-config.siliconflow-reviewed.json `
  --output-prefix research/05_analysis/smoke-pilot-once-execution `
  --execute `
  --confirm-cost
```

This wrapper runs preflight, adapter execution, and postprocess. For manual execution, the equivalent adapter and postprocess commands are:

```powershell
python research/04_methods/scripts/run_openai_adapter.py `
  --manifest research/05_analysis/real-run-artifacts/first-slice-smoke-manifest.json `
  --config research/04_methods/provider-config.siliconflow-reviewed.json `
  --report research/05_analysis/openai-adapter-smoke-run.json `
  --execute
python research/04_methods/scripts/postprocess_real_model_pilot.py `
  --manifest research/05_analysis/real-run-artifacts/first-slice-smoke-manifest.json `
  --output-prefix research/05_analysis/first-slice-postprocess-smoke `
  --baseline-arm G0
```

Stop if the output format, validation logic, or trace contract fails.

## Step 3: Full 24-Run Execution

Use this only after the smoke test has passed and full execution has approval.

```powershell
python research/04_methods/scripts/run_openai_adapter.py `
  --manifest research/05_analysis/real-run-artifacts/first-slice-manifest-with-prompts.json `
  --config research/04_methods/provider-config.siliconflow-reviewed.json `
  --report research/05_analysis/openai-adapter-execution.json `
  --execute
```

## Step 4: Postprocess

```powershell
python research/04_methods/scripts/postprocess_real_model_pilot.py `
  --manifest research/05_analysis/real-run-artifacts/first-slice-manifest-with-prompts.json `
  --output-prefix research/05_analysis/first-slice-postprocess `
  --baseline-arm G0
```

Expected after successful full execution:

- Completed runs collected: 24
- Metrics computed: yes
- Warnings: 0, or documented and explainable

## Step 5: Evidence Update

Only after Step 4 succeeds:

- Add a source-index row for the real execution report and postprocess metrics.
- Add evidence ledger entries as `EXTRACTED` for measured metrics and `INFERRED` only for bounded interpretation.
- Update `research/05_analysis/02-contract-driven-agent-harness-synthesis.md`.
- Update `research/06_outputs/two-proposal-research-report.md`.

## Stop Conditions

Stop and do not claim benchmark evidence if:

- Any run remains `pending`.
- Model IDs differ from the stated provider config.
- The adapter overwrites non-placeholder outputs unexpectedly.
- The evaluator marks a fixture unsupported.
- Fewer than two model tiers complete under the baseline arm.
- Gap-compression metrics are skipped by the postprocess summary.
