# Synthesis: Contract-Driven Agent Harness Engineering

## Bottom Line

This proposal is academically and practically stronger than a generic "agent consistency" paper if it centers on a measurable construct:

> Model Capability Gap Compression under stable agent harnesses.

The proposal should not argue that model capability stops mattering. It should argue that for structured, toolable, verifiable productivity tasks, contracts and workflows move some work out of model free generation and into explicit system machinery (`P2-E01`).

## Core Framing

The best research object is not "better prompts." It is:

```text
Task contracts + capability registry + workflow runtime + memory policy + validation/evaluation harness
```

This creates a clean contrast:

- Baseline: prompt-only or weakly structured agent.
- Treatment: contract-driven harness with fixed task spec, tool contract, memory slice, output contract, validators, and trace logging.

The hypothesis is that the treatment reduces cross-model variance in success, schema adherence, tool trajectory, citation grounding, and human acceptance.

## Literature Positioning

Use Anthropic's workflow-vs-agent distinction to justify when harnessing is appropriate (`P2-E05`). Use LangGraph as the runtime comparator for durable state, memory, and human-in-the-loop orchestration (`P2-E06`). Use DSPy to position this as programming/optimizing LM pipelines rather than hand prompt craft (`P2-E07`). Use AgentSPEX and Open Agent Spec as the declarative workflow/specification line (`P2-E08`). Use Guardrails for the validation layer (`P2-E09`).

The research gap:

> Existing frameworks expose workflows, tools, validation, or memory, but the paper asks a narrower measurement question: how much do these harness layers compress cross-model capability gaps by task type?

## Experimental Design

Recommended model matrix:

- Strong model.
- Mid model.
- Budget model.
- Fast model.
- Long-context model.
- Optional local/quantized model.

Recommended task matrix:

- High-constraint tasks: structured extraction, project initialization, config generation, skill validation.
- Medium-constraint tasks: research workflow, code repair, documentation generation, repo analysis.
- Low-constraint tasks: open-ended planning, strategic judgment, creative synthesis.

Recommended harness arms:

1. G0: prompt-only.
2. G1: prompt + role + instruction.
3. G2: G1 + output schema.
4. G3: G2 + RAG / evidence bundle.
5. G4: G3 + tools / MCP.
6. G5: G4 + skills.
7. G6: G5 + workflow.
8. G7: G6 + memory policy.
9. G8: G7 + validator / eval.
10. G9: full harness + trace + regression.

Core metric:

```text
CompressionRatio = 1 - Gap_harness / Gap_baseline
```

Report separate compression ratios for success rate, schema validity, citation grounding, tool-call correctness, human acceptance, and cost efficiency (`P2-E02`).

## PEtFiSh-Specific Architecture Direction

The strongest local architecture proposal is to add four control objects (`P2-E03`):

- `TaskSpec`: task type, constraints, required skills, allowed tools, risk profile.
- `EvidenceBundle`: source/evidence IDs, evidence type, freshness, authority.
- `MemorySlice`: active topic/task, must-load/may-load/must-not-load context.
- `OutputContract`: schema, required sections, citation policy, style profile.

These should become machine-readable schemas and feed the router, skill registry, memory context builder, and quality gate.

## Main Weaknesses

The proposal currently risks being too broad. It should avoid trying to cover all agents. The publishable slice is: productivity tasks where task success can be externally measured.

The second risk is contract drift. If the registry, installer, docs, AGENTS rules, skill manifests, and tests disagree, the harness itself becomes unstable (`P2-E04`).

The third risk is that memory and workflow may be model-sensitive. A harness layer can improve one model and hurt another, so cross-model evaluation is not optional.

## Recommended Paper Shape

Recommended title:

**Can Agent Harnesses Compress Model Capability Gaps?**

Recommended contributions:

1. Define model capability gap compression.
2. Propose a contract-driven harness architecture.
3. Implement the architecture in PEtFiSh or a PEtFiSh-derived benchmark harness.
4. Measure compression across task classes, model classes, and harness strengths.
5. Identify boundaries where harnessing helps, plateaus, or harms.

## Pilot Metric Tool

I added `research/04_methods/scripts/harness_benchmark_metrics.py` and validated it on a synthetic sample run file. The helper computes per-metric cross-model gap compression as:

```text
1 - arm_gap / baseline_gap
```

The sample data is deliberately synthetic, so it should not be cited as empirical evidence. Its value is methodological: it confirms that the benchmark can report gap compression separately for task success, schema validity, tool-call correctness, citation grounding, human acceptance, cost efficiency, and safety consistency (`P2-E10`).

## Mock Benchmark Pipeline

I added a dry-run compiler and deterministic mock benchmark runner:

- `compile_benchmark_packets.py`
- `run_mock_harness_benchmark.py`
- `harness_benchmark_metrics.py`

The current benchmark matrix has 240 planned runs: 4 fixtures, 3 model tiers, 4 harness arms, and 5 repetitions. The pipeline compiles all 240 packets and produces a full mock metrics report with no failures (`P2-E11`).

This confirms the benchmark data path is coherent, but it is not evidence that harnesses compress real model gaps. The next research step is to replace the mock runner with a real model adapter while keeping the same packet and metrics format.

## First Real-Model Slice Prepared

The first model-backed slice is now concrete:

- Fixtures: `structured-extraction`, `project-initialization`.
- Model tiers: `strong_model`, `budget_model`.
- Arms: `G0`, `G9`.
- Repetitions: 3.
- Total planned runs: 24.

The slice compiles into packet summaries with no failures, and per-run artifact directories are prepared under `research/05_analysis/real-run-artifacts/first-slice` (`P2-E12`). The remaining work is to connect real model adapters and replace placeholder outputs with actual runs.

## Evaluator Validation

I added `evaluate_real_run_artifacts.py` for the first real-model slice. It currently supports:

- `structured-extraction`
- `project-initialization`

Golden outputs score as expected: structured extraction reaches 1.0 across the tracked metrics, while project initialization reaches 1.0 except citation grounding at 0.8 under the current heuristic (`P2-E13`). Pending first-slice outputs are correctly reported as pending with zero metrics. This gives us a ready scoring path before real model calls are added.

## Adapter Queue

The first 24-run slice now has rendered `prompt.md` and `adapter_request.json` files for every run, plus a queue at `research/05_analysis/first-slice-adapter-queue.md` (`P2-E14`). The G0 prompts contain only raw task input and minimal instructions; G9 prompts include TaskSpec, EvidenceBundle, MemorySlice, and OutputContract.

This is the last preparation step before provider-specific execution. The next missing component is a real adapter that maps `strong_model` and `budget_model` to concrete model IDs and writes raw outputs into the prepared artifact directories.

## Provider Adapter Dry-Run

I added:

- `provider-config.example.json`
- `validate_provider_config.py`
- `run_openai_adapter.py`

The provider config validates, and the OpenAI-compatible adapter dry-runs all 24 first-slice runs without calling the network (`P2-E15`). The example maps `strong_model` to `gpt-5.1` and `budget_model` to `gpt-5.1-mini`, but these are placeholders until the actual available model IDs and API budget are confirmed.

## Metrics Collection Guard

I added `collect_run_metrics.py` to aggregate only completed evaluated runs before the gap-compression metric step. The guard reads each run's `validation_report.json` and skips artifacts whose validation status is not `complete`.

The current first-slice artifact set correctly collects 0 completed runs and reports 24 pending warnings, while the golden-check fixture set collects 2 completed runs with 0 warnings (`P2-E16`). This prevents placeholder or pending model outputs from entering the benchmark metrics as if they were empirical results.

## Real-Run Preflight

I added `preflight_real_model_pilot.py` as a local-only execution gate before using `run_openai_adapter.py --execute`. It checks the manifest, required artifact paths, prompt and adapter request consistency, validation statuses, provider mappings, and API-key environment variable presence without calling a model.

The current preflight report covers all 24 first-slice runs and returns 0 errors with 2 warnings: the provider config is still an example file, and `OPENAI_API_KEY` is not set (`P2-E17`). This means the queue is structurally ready, but execution should wait for explicit approval, confirmed model IDs, credentials, and budget.

## Real-Run Postprocess Pipeline

I added `postprocess_real_model_pilot.py` and `first-slice-real-run-runbook.md` to make the real pilot reproducible after provider outputs are written. The postprocess script evaluates artifacts, collects only completed run metrics, and computes gap-compression summaries only if there are enough completed baseline and harness runs.

On the current pending first-slice artifacts, the postprocess summary reports 0 completed runs, 24 pending warnings, and `metrics_computed=false` (`P2-E18`). This is the desired stop behavior before real execution: no pending placeholder can become benchmark evidence.

## Smoke Manifest

I added `select_manifest_runs.py` and generated `first-slice-smoke-manifest.json`, a four-run subset of the first slice. It includes `structured-extraction` for `strong_model` and `budget_model` under `G0` and `G9`, repetition 1.

The smoke manifest gives the first provider-backed execution a lower-cost rehearsal path while still preserving the minimum comparison needed for a baseline-vs-harness and strong-vs-budget sanity check. Current smoke preflight has 0 structural errors, and smoke postprocess correctly reports 0 completed runs with 4 pending warnings because no model outputs exist yet (`P2-E19`).

## Reviewed OpenAI Smoke Config

I checked the official OpenAI model docs before moving from example configuration to execution configuration. The docs list `gpt-5.1` and `gpt-5-mini` as model IDs, and both model pages list Chat Completions as a supported endpoint (`P2-E20`).

I added `provider-config.openai-reviewed.json`, mapping `strong_model` to `gpt-5.1` and `budget_model` to `gpt-5-mini`. The config validates, and `run_openai_adapter.py` dry-runs all four smoke runs with `execute=false`. The execution gate is now narrowed to credentials and explicit budget/network approval: `preflight_real_model_pilot.py --require-keys` fails only because `OPENAI_API_KEY` is not set (`P2-E21`).

## Smoke Workflow Wrapper

I added `run_smoke_pilot_once.py` to run the smoke workflow in one command: preflight, adapter, and postprocess. The default mode is dry-run. Real provider execution requires both `--execute` and `--confirm-cost`, and the wrapper runs require-key preflight before any adapter call.

The wrapper dry-run completed over the four smoke runs without network calls. It produced adapter dry-run output and postprocess output with 0 completed runs and 4 pending warnings, preserving the stop condition until real outputs exist (`P2-E22`).

## SiliconFlow Execution Path

I added `provider-config.siliconflow-reviewed.json` after checking SiliconFlow's official Chat Completions docs and model guide. The config uses `https://api.siliconflow.cn/v1`, reads `SILICONFLOW_API_KEY`, maps `strong_model` to `deepseek-ai/DeepSeek-V3.2`, and maps `budget_model` to `Qwen/Qwen3-8B` (`P2-E23`).

The SiliconFlow config validates, the smoke adapter dry-runs all four selected runs with `execute=false`, and the guarded smoke workflow dry-run completes without network calls. Current preflight has 0 errors and 1 warning because `SILICONFLOW_API_KEY` is not set (`P2-E24`). This is now the recommended provider path for the first real smoke execution.

## SiliconFlow Smoke Execution

The first real model-backed smoke pilot completed successfully on SiliconFlow. It ran 4 structured-extraction cases:

- `deepseek-ai/DeepSeek-V3.2` as `strong_model`, arms `G0` and `G9`.
- `Qwen/Qwen3-8B` as `budget_model`, arms `G0` and `G9`.

All four runs executed, postprocess collected 4 completed metric payloads, and there were 0 collection warnings (`P2-E25`). G9 improved the observed output contract behavior: both model tiers reached schema validity 1.0 and citation grounding 1.0 under G9, while both G0 runs omitted the required `evidence_ids` and used `project_title` rather than `title`.

This smoke result should not be used as evidence that harnessing compresses cross-model gaps. The G0 baseline cross-model gap was 0.0 for all tracked metrics, making compression ratios `n/a`; under G9, task success differed between model tiers. The correct interpretation is narrower: the harness path can improve contract adherence on this fixture, and the execution/evaluation pipeline is now proven against real provider outputs (`P2-E26`).

## SiliconFlow V2 Full 24-Run Slice

After the smoke result, I added `structured-extraction-hard` and ran the v2 full slice on SiliconFlow:

- Fixtures: `structured-extraction`, `structured-extraction-hard`.
- Models: `deepseek-ai/DeepSeek-V3.2` as `strong_model`, `Qwen/Qwen3-8B` as `budget_model`.
- Arms: `G0`, `G9`.
- Repetitions: 3.
- Total: 24 model calls.

The final postprocess collected 24 completed runs with 0 warnings and computed gap-compression metrics (`P2-E27`). One budget-model hard/G0 run timed out on its first attempt and was rerun successfully before final postprocess.

The result is substantially more positive than the initial smoke pilot. For all non-n/a metrics with a nonzero G0 baseline gap, G9 reduced the measured cross-model gap to 0. The observed compression ratio is 1.000 for task success, schema validity, tool-call correctness, human acceptance, cost efficiency, and safety consistency (`P2-E28`). Citation grounding remains n/a for gap compression because the baseline gap was 0.

This supports a bounded empirical claim: on two structured-extraction fixtures under this evaluator and SiliconFlow model pair, the contract-rich G9 harness eliminated measured cross-model variance while improving absolute contract adherence. It still should not be generalized to all agent tasks until additional task classes are run.

## SiliconFlow Project-Initialization Slice

I then ran a second task class: `project-initialization`, using the same SiliconFlow model pair, `G0`/`G9`, and 3 repetitions per model/arm condition. The adapter executed all 12 runs. The outer wrapper timed out while waiting for postprocess, but the final manual postprocess collected 12 completed runs with 0 warnings and computed gap-compression metrics (`P2-E29`).

The result is mixed and useful. G9 compressed the task-success gap from 0.111 to 0 and safety-consistency gap from 0.200 to 0. Both model tiers improved in absolute terms under G9. However, schema-validity and related aggregate gaps widened because the budget model benefited more strongly from the harness than the strong model (`P2-E30`).

This refines the method claim. The harness does not simply "make weak and strong models equal" across all metrics. A better hypothesis is: contract-rich harnessing can raise absolute contract adherence and may reduce gaps on task-success/safety metrics, but gap movement depends on which model benefits more from explicit structure.

## SiliconFlow Research-Workflow Slice

I added a third task class, `research-workflow`, for evidence-backed synthesis. It asks the model to decide whether two proposal tracks should be combined or separated while separating extracted evidence from inference and citing evidence IDs.

The SiliconFlow run completed 12/12 calls, collected 12 completed metric payloads, produced 0 warnings, and computed metrics (`P2-E31`). G0 performed poorly on core research discipline: both model tiers had task_success 0.000 and citation_grounding 0.000. Under G9, the strong model reached 1.000 across task_success, schema_validity, citation_grounding, human_acceptance, cost_efficiency, and safety_consistency; the budget model reached 0.917 task_success and 1.000 on schema_validity, citation_grounding, human_acceptance-adjacent metrics, and safety_consistency (`P2-E32`).

This third task class clarifies the "proof but not proof" problem. The strongest repeated effect is not universal gap compression. The strongest repeated effect is absolute contract adherence lift. Gap compression is meaningful only when the G0 baseline gap is nonzero and when the harness does not help one model much more than the other.

## Claim Boundary

I added `contract-driven-claim-boundary-memo.md` to prevent overclaiming (`P2-E33`). The paper should not claim that harnesses generally make weak models equivalent to strong models. The defensible thesis is:

> Contract-driven harness engineering externalizes task constraints into explicit, verifiable control objects. Across three SiliconFlow task slices, this improves absolute contract adherence and sometimes compresses model gaps; gap compression is an empirical outcome, not a guaranteed property.
