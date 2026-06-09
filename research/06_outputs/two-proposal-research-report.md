# Research Report: Two Proposal Tracks

## Executive Summary

The two proposals are related but should become two separate papers.

**Project 1, Topic-Aware Compaction**, is a focused systems paper. It studies a concrete mechanism: preserving topic boundaries during compaction changes an LLM coding agent's trajectory. The current local evidence is promising: the fish-trail A/B test reports 20.3% total token savings, 36.4% fewer API calls, 49.9% fewer cache reads, 39.4% lower wall time, and no measured recall loss (`P1-E01`). The main missing piece is causal ablation.

**Project 2, Contract-Driven Agent Harness Engineering**, is a broader methodology and evaluation paper. It should study whether external contracts, tools, memory policy, workflows, validators, and regression evals compress cross-model capability gaps in productivity tasks. Its strongest measurable construct is `Model Capability Gap Compression` (`P2-E02`).

## Project 1: Topic-Aware Compaction

### Research Judgment

This is the more immediately executable paper because it already has data, scripts, a draft, and a clear intervention.

The best claim is:

> Topic-aware compaction reduces agent cost by changing behavior, especially redundant tool-call trajectories, in multi-topic sessions.

This claim is narrower and stronger than "better compression." It explains why a 36.4% API-call reduction can drive larger operational savings than raw context shortening.

### Evidence

The local experiment used 21 interleaved messages across three topics and three recall questions (`P1-E02`). Both baseline and plugin completed recall, while the plugin used fewer calls and less token/cache budget (`P1-E01`). This supports the idea that topic structure preserved enough state while reducing exploratory rebuilding.

External work helps position the paper:

- LLMLingua represents prompt compression focused on compacting text (`P1-E05`).
- ACON and SWE-Pruner show that agent-context optimization is an active research area with large token-reduction results (`P1-E06`, `P1-E07`).
- Membox and Context-Agent support the representational point: flat chronological history is weak for topic-shifting dialogue (`P1-E08`, `P1-E09`).

### Recommended Next Step

Run three ablations before expanding prose:

1. Compression-only.
2. Behavioral-only.
3. Single-topic control.

These three tests would make the paper much harder to dismiss, because they directly test the mechanism.

## Project 2: Contract-Driven Agent Harness Engineering

### Research Judgment

This is the more ambitious and potentially more important paper, but it needs a narrower evaluation spine.

The best claim is:

> Harnesses compress model capability gaps in tasks whose success can be constrained, tooled, and verified.

Do not claim that harnesses make model capability irrelevant. The local proposal already correctly rejects that overclaim (`P2-E01`).

### Evidence

The existing local materials are already strong as a theory base:

- The revised plan defines the main thesis and metric (`P2-E01`, `P2-E02`).
- The PEtFiSh analysis proposes TaskSpec, EvidenceBundle, MemorySlice, and OutputContract as a control-plane architecture (`P2-E03`).
- The survey identifies contract drift as the central engineering risk (`P2-E04`).

External work supports the direction:

- Anthropic's workflow/agent distinction supports using workflows when task structure is stable (`P2-E05`).
- LangGraph provides a reference point for durable execution, persistence, memory, and human-in-the-loop orchestration (`P2-E06`).
- DSPy supports the move from prompt craft to declarative, optimizable LM programs (`P2-E07`).
- AgentSPEX and Agent Spec support explicit workflow specification as a research direction (`P2-E08`).
- Guardrails supports the validation layer (`P2-E09`).

### Recommended Next Step

Build a small benchmark before writing the full manifesto:

- 3 model tiers.
- 3 task classes: high, medium, low constraint.
- 4 harness arms: prompt-only, schema, workflow+tools, full harness.
- 5 repeated runs per task/model/arm.

Measure whether cross-model gaps shrink and where they do not.

## Relationship Between the Two Projects

Project 1 can become an empirical case study inside Project 2 later, but it should not be swallowed by Project 2 now.

Project 1 asks:

> Can topic-aware compaction change agent behavior and reduce cost?

Project 2 asks:

> Can contract-driven harnesses reduce cross-model performance variance across task classes?

They share a worldview, but their evidence standards differ.

## Recommended Publishing Strategy

1. Push Project 1 first as a concrete systems paper or workshop paper.
2. Use Project 1's trajectory metrics as one motivating example for Project 2.
3. Develop Project 2 as a benchmark/methodology paper with PEtFiSh as the system artifact.

## Immediate To-Do List

- For Project 1: preserve full session messages and convert token-only trajectory screening into semantic tool-call labels.
- For Project 1: run the three core ablations.
- For Project 1: add cross-model replication only after ablations confirm mechanism.
- For Project 2: turn the minimal `TaskSpec`, `EvidenceBundle`, `MemorySlice`, and `OutputContract` schemas into runnable benchmark fixtures.
- For Project 2: replace the synthetic metric sample with real multi-model runs.
- For both: keep evidence ledgers updated before claims enter drafts.

## Progress Update

Two methodological pilot tools now exist:

- `label_token_trajectory.py` screens existing Topic-Aware A/B token traces and flags candidate state-rebuild calls.
- `harness_benchmark_metrics.py` computes gap-compression ratios from benchmark run metrics.
- `compile_benchmark_packets.py` and `run_mock_harness_benchmark.py` validate the full 240-run benchmark data path with deterministic mock models.

The first real next step is to capture richer raw traces. Current Topic-Aware data is enough for aggregate token analysis but not enough for full semantic trajectory claims.

For the harness paper, the first real next step is to connect the benchmark packets to actual model adapters. The mock pipeline has validated data shape, not the research hypothesis.

The first real-model slice is ready: 24 runs covering two fixtures, two model tiers, two harness arms, and three repetitions. Artifact directories are prepared, so a real adapter can now fill `output.md`, `tool_trace.jsonl`, `validation_report.json`, and `metrics.json` for each run.

The first-slice evaluator is also in place. It can score golden outputs for the two current fixtures and leaves pending run artifacts clearly marked as pending, so the next real model run has an automatic validation path.

Rendered prompts and adapter requests are now exported for all 24 first-slice runs. A human-readable adapter queue is available, so the remaining step is provider execution rather than benchmark design.

The provider layer now has an OpenAI-compatible dry-run adapter. It validates the config and processes all 24 runs without network calls, which means the real execution path is now gated mainly on confirmed model IDs, API credentials, and budget.

The metrics collection guard is also in place. It skips the 24 pending first-slice artifacts and only aggregates completed golden-check artifacts, so placeholder outputs cannot silently become benchmark evidence (`P2-E16`).

A local-only real-run preflight now checks the 24-run queue before any paid/provider execution. It reports no structural errors, while correctly warning that the config is still an example file and `OPENAI_API_KEY` is absent (`P2-E17`).

The postprocess path is now scripted as well. On the current pending artifacts it produces 0 completed runs and skips gap-compression metrics, which gives the benchmark a clear stop condition before any real model evidence is claimed (`P2-E18`).

A four-run smoke manifest now exists for the first provider-backed rehearsal. It covers one structured-extraction repetition across strong/budget models and G0/G9 arms, giving a cheaper sanity check before the full 24-run slice (`P2-E19`).

The OpenAI provider config has been revised against official model docs: `strong_model` now maps to `gpt-5.1`, and `budget_model` maps to `gpt-5-mini`. The four-run smoke adapter dry-run succeeds without network calls; the remaining execution blocker is the missing `OPENAI_API_KEY` plus explicit cost/network approval (`P2-E20`, `P2-E21`).

A one-command smoke workflow wrapper now runs preflight, adapter, and postprocess in sequence. It defaults to dry-run and requires both `--execute` and `--confirm-cost` for real provider calls, so the next execution step is guarded against accidental spend (`P2-E22`).

Because OpenAI credentials are unavailable, the smoke path now targets SiliconFlow. The reviewed SiliconFlow config uses `deepseek-ai/DeepSeek-V3.2` as the strong model and `Qwen/Qwen3-8B` as the budget model. Config validation, adapter dry-run, and guarded workflow dry-run all pass; the remaining blocker is setting `SILICONFLOW_API_KEY` and approving the four real API calls (`P2-E23`, `P2-E24`).

The four-run SiliconFlow smoke pilot has now executed successfully. It produced 4 completed structured-extraction runs and 0 collection warnings. The result supports the pipeline and output-contract direction: G9 reached full schema validity and citation grounding for both model tiers, while G0 did not. It does not yet support the main gap-compression claim because the G0 cross-model baseline gap was zero, so compression ratios were not interpretable (`P2-E25`, `P2-E26`).

The follow-up SiliconFlow v2 full slice has now completed 24 runs across `structured-extraction` and `structured-extraction-hard`, with 3 repetitions per model/arm condition. Final postprocess collected all 24 runs with 0 warnings. In this slice, G9 compressed all measured nonzero G0 cross-model gaps to 0, yielding compression ratio 1.000 for task success, schema validity, tool-call correctness, human acceptance, cost efficiency, and safety consistency (`P2-E27`, `P2-E28`). This is now real positive evidence for the Project 2 hypothesis, bounded to structured extraction and the current evaluator.

A second SiliconFlow task class, `project-initialization`, has also completed 12 runs with 0 collection warnings. This result is more nuanced. G9 compressed task-success and safety-consistency gaps to 0 and improved absolute performance for both models, but schema-validity and related aggregate gaps widened because the budget model gained more from the harness than the strong model (`P2-E29`, `P2-E30`). The broader conclusion should therefore be framed as harnesses improving contract adherence and sometimes compressing model gaps, rather than always reducing every gap metric.

A third SiliconFlow task class, `research-workflow`, has completed 12 runs with 0 collection warnings. This slice strongly supports absolute harness benefit: G9 raised both model tiers from near-zero evidence-grounded research discipline under G0 to high task success, schema validity, and citation grounding under G9. It also shows why gap compression cannot be the only headline: some G0 gaps were zero because both models failed, making compression n/a even though G9 was practically valuable (`P2-E31`, `P2-E32`).

The recommended paper thesis is now sharper: contract-driven harness engineering improves explicit contract adherence across tested task classes and sometimes compresses cross-model gaps. Gap compression should be framed as a measured outcome with boundary conditions, not as a universal guarantee (`P2-E33`).
