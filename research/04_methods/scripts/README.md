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

For executed runs, the adapter preserves provider-reported token usage when
available, response/request identifiers, response model metadata, elapsed time,
payload bytes, and optional retry lineage declared in `adapter_request.json`.
Missing provider usage remains `null`; byte counts are not substituted for
tokens.

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

## `build_macro_perturbation_suite.py`

Builds the two-macro, five-condition representation-perturbation suite used by
the post-freeze Stage B pilot. The generated fixtures include golden outputs,
predeclared known-bad outputs, field/value alias contracts, distractor-support
rules, and condition metadata.

```powershell
python research/04_methods/scripts/build_macro_perturbation_suite.py `
  --base-dir research/04_methods/macro-tasks `
  --output-dir research/04_methods/macro-perturbations

python research/04_methods/scripts/evaluate_stage7e_macro_artifacts.py `
  --fixtures-dir research/04_methods/macro-perturbations `
  --local-check `
  --output-runs research/05_analysis/post-freeze-perturbation-local-gates.json `
  --output-md research/05_analysis/post-freeze-perturbation-local-gates.md
```

The local check must pass before compiling or executing the paid perturbation
pilot.

## Stage B v4 Exact-Retention Atoms

`build_stage_b_v4_local_atoms.py` creates four local mechanism fixtures that
separate exact evidence-array immutability from exact closed-vocabulary
retention. `evaluate_stage_b_v4_atoms.py` uses exact list equality, including
order and multiplicity, and checks that evaluator-only alternatives do not
leak into model-visible fixture files.

```powershell
python research/04_methods/scripts/build_stage_b_v4_local_atoms.py `
  --output-dir research/04_methods/mechanism-atoms-stage-b-v4

python research/04_methods/scripts/validate_mechanism_atoms.py `
  --atoms-dir research/04_methods/mechanism-atoms-stage-b-v4

python research/04_methods/scripts/test_evaluate_stage_b_v4_atoms.py

python research/04_methods/scripts/evaluate_stage_b_v4_atoms.py `
  --atoms-dir research/04_methods/mechanism-atoms-stage-b-v4 `
  --local-check `
  --output-runs research/05_analysis/stage-b-v4-local-check.json `
  --output-md research/05_analysis/stage-b-v4-local-check.md
```

Passing this local gate admits only a targeted model smoke. It is not model
performance evidence.

## Stage B v4 Bounded Recomposition

`build_stage_b_v4_recomposition.py` composes exact evidence-array retention and
exact closed-vocabulary retention into a bounded macro with one local-first
composition gate. The evaluator reports component metrics separately and
checks preregistered metric vectors for each known-bad output.

```powershell
python research/04_methods/scripts/build_stage_b_v4_recomposition.py `
  --output-dir research/04_methods/macro-recomposition-stage-b-v4

python research/04_methods/scripts/test_evaluate_stage_b_v4_recomposition.py

python research/04_methods/scripts/evaluate_stage_b_v4_recomposition.py `
  --fixtures-dir research/04_methods/macro-recomposition-stage-b-v4 `
  --local-check `
  --output-runs research/05_analysis/stage-b-v4-recomposition-local-check.json `
  --output-md research/05_analysis/stage-b-v4-recomposition-local-check.md
```

The local gate also requires the Stage B v4 atom regression and unchanged
Stage B v3 110-case regression before any provider call.

## Stage B v5 Controlled State Transition

`build_stage_b_v5_state_transition.py` adds one evidence-backed
unknown-to-known API-approval transition to the passed Stage B v4 bounded
recomposition. The model-visible contract declares the nested schema, initial
state, event, and postconditions without exposing the golden output.

```powershell
python research/04_methods/scripts/build_stage_b_v5_state_transition.py `
  --output-dir research/04_methods/macro-state-transition-stage-b-v5

python research/04_methods/scripts/test_evaluate_stage_b_v5_state_transition.py

python research/04_methods/scripts/evaluate_stage_b_v5_state_transition.py `
  --fixtures-dir research/04_methods/macro-state-transition-stage-b-v5 `
  --local-check `
  --output-runs research/05_analysis/stage-b-v5-state-transition-local-check.json `
  --output-md research/05_analysis/stage-b-v5-state-transition-local-check.md
```

The local gate requires all transition known-bads, the static-copy ablation,
surface-isolation checks, and the unchanged Stage B v4 atom, v4 recomposition,
and Stage B v3 regressions to pass before any provider call.

## Stage B v5.1 Transition Contract Repair

`build_stage_b_v51_state_transition.py` retains the v5 state mutation but
repairs two contract defects identified after the failed v5 smoke. Immutable
slot-to-reference arrays now live in `evidence_bindings`, separate from claim
prose, and the complete expected `transition_gate` is model-visible.

```powershell
python research/04_methods/scripts/build_stage_b_v51_state_transition.py `
  --output-dir research/04_methods/macro-state-transition-stage-b-v51

python research/04_methods/scripts/test_evaluate_stage_b_v51_state_transition.py

python research/04_methods/scripts/evaluate_stage_b_v51_state_transition.py `
  --fixtures-dir research/04_methods/macro-state-transition-stage-b-v51 `
  --local-check `
  --output-runs research/05_analysis/stage-b-v51-state-transition-local-check.json `
  --output-md research/05_analysis/stage-b-v51-state-transition-local-check.md
```

The v5.1 suite is a new repaired protocol. It does not replace, rescore, or
pool with the failed v5 smoke. Any provider smoke remains separately
authorized.

## Stage B v5.2 evidence-binding ablation

Build and locally validate the two-profile, five-condition ablation:

```powershell
python research/04_methods/scripts/build_stage_b_v52_evidence_binding_ablation.py `
  --output-dir research/04_methods/macro-evidence-binding-ablation-stage-b-v52 `
  --matrix-output research/04_methods/benchmark-matrix-stage-b-v52-evidence-binding-ablation.json

python research/04_methods/scripts/test_evaluate_stage_b_v52_evidence_binding_ablation.py

python research/04_methods/scripts/evaluate_stage_b_v52_evidence_binding_ablation.py `
  --fixtures-dir research/04_methods/macro-evidence-binding-ablation-stage-b-v52 `
  --local-check `
  --output-runs research/05_analysis/stage-b-v52-evidence-binding-ablation-local-check.json `
  --output-md research/05_analysis/stage-b-v52-evidence-binding-ablation-local-check.md
```

After separately authorized provider execution, evaluate and analyze the frozen
manifest:

```powershell
python research/04_methods/scripts/evaluate_stage_b_v52_evidence_binding_ablation.py `
  --fixtures-dir research/04_methods/macro-evidence-binding-ablation-stage-b-v52 `
  --manifest research/05_analysis/real-run-artifacts/stage-b-v52-evidence-binding-ablation-manifest-with-prompts.json `
  --output-runs research/05_analysis/stage-b-v52-evidence-binding-ablation-results.json `
  --output-md research/05_analysis/stage-b-v52-evidence-binding-ablation-results.md

python research/04_methods/scripts/analyze_stage_b_v52_evidence_binding_ablation.py `
  --evaluated-runs research/05_analysis/stage-b-v52-evidence-binding-ablation-results.json `
  --execution research/05_analysis/stage-b-v52-evidence-binding-ablation-execution.json `
  --output-json research/05_analysis/stage-b-v52-evidence-binding-ablation-analysis.json `
  --output-md research/05_analysis/stage-b-v52-evidence-binding-ablation-analysis.md
```

The frozen 30-run result found no engineering-scale evidence-representation
effect. Do not pool a future state-instruction repair with this protocol.

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
