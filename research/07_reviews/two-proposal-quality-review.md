# Quality Review: Two Proposal Research

## Review Result

Conditional pass.

The two research tracks are promising and now have separate briefs, source index, evidence ledger, synthesis notes, and a combined report. The current artifacts are useful for planning and paper direction, but they should not yet be treated as final literature reviews.

## Strengths

- The two projects are now separated by research question and evidence standard.
- Claims are tied to local evidence IDs and external source IDs.
- The strongest thesis for each project is narrower than the original broad framing.
- Key risks are explicit: small-N / single-model for Project 1, and overbreadth / contract drift for Project 2.

## Unsupported Or Under-Supported Claims To Avoid

- Do not claim topic-aware compaction universally improves agent quality.
- Do not claim behavioral change is proven until trajectory-level labels and ablations are complete.
- Do not claim harnesses make weak models equivalent to strong models.
- Do not claim cross-model portability before a fixed benchmark matrix is run.

## Evidence Gaps

- Project 1 needs trajectory annotations and repeated runs.
- Project 1 needs cross-model replication.
- Project 2 has a validated mock benchmark data path, but still needs actual model-backed benchmark data.
- Project 2 needs a concrete implementation of TaskSpec / EvidenceBundle / MemorySlice / OutputContract.

## Recommended Next Review Gate

Run the next review after:

1. Project 1 has completed at least compression-only, behavioral-only, and single-topic ablations.
2. Project 2 has replaced the mock benchmark runner with at least one real model-backed matrix slice.

## Update: 2026-06-07

### Review Result

Conditional pass, still not publication-ready as empirical evidence.

The main improvement since the first review is that Project 2 now has a much stronger execution scaffold: benchmark fixtures, schema contracts, packet compilation, prompt export, provider dry-run, preflight, postprocess, metrics collection, and a four-run smoke manifest. This materially reduces the risk of accidentally treating placeholder outputs as benchmark data.

### Dimension Check

| Dimension | Rating | Notes |
|---|---|---|
| Question alignment | pass | The two research questions remain separated and appropriately scoped. |
| Evidence completeness | partial | Local pipeline evidence is tracked through `P2-E24`, smoke evidence through `P2-E25`/`P2-E26`, structured-extraction evidence through `P2-E27`/`P2-E28`, and project-initialization evidence through `P2-E29`/`P2-E30`; more task classes are still absent. |
| Citation coverage | pass for current report | The current empirical claims cite measured execution outputs, not dry-runs. |
| Logic chain | partial for broader claim | Structured extraction strongly supports gap compression; project initialization shows mixed gap movement but absolute harness benefit. The broader claim should be softened. |
| Counter-evidence | partial | Stop conditions are documented, but no adverse real-run cases exist yet. |
| Method fit | pass | The planned benchmark and gap-compression metric match the Project 2 research question. |
| Actionability | pass | The runbook defines preflight, smoke execution, full execution, postprocess, and stop conditions. |
| Expression quality | pass | The current report generally avoids overclaiming; the key distinction is "pipeline validation" versus "model evidence." |
| Risk disclosure | pass | Missing API credentials, example model IDs, pending artifacts, and no-network status are explicit. |

### Current Blockers

- Project 1 still lacks full semantic trajectory labels and ablation results.
- Project 2 now has structured-extraction and project-initialization SiliconFlow slices, but still lacks research workflow/tool-heavy task classes and independent evaluator validation.
- A reviewed OpenAI config now maps `strong_model` to `gpt-5.1` and `budget_model` to `gpt-5-mini`, but actual account access still needs runtime confirmation.
- A reviewed SiliconFlow config now maps `strong_model` to `deepseek-ai/DeepSeek-V3.2` and `budget_model` to `Qwen/Qwen3-8B`; actual key permissions and quota still need runtime confirmation.
- Neither `OPENAI_API_KEY` nor `SILICONFLOW_API_KEY` is present in the current environment.
- The smoke and first-slice postprocess reports correctly skip metrics because all selected model outputs are still pending.

### Do Not Claim Yet

- Do not claim that contract-driven harnesses always reduce every cross-model gap. The project-initialization slice shows some gaps widening when the budget model benefits more from the harness.
- Do not cite mock or dry-run results as empirical benchmark results.
- Do not claim model-specific conclusions from `gpt-5.1` / `gpt-5-mini` until account access and execution outputs are confirmed.
- Do not claim SiliconFlow model-specific conclusions until `deepseek-ai/DeepSeek-V3.2` and `Qwen/Qwen3-8B` have completed real smoke runs under the same fixture and evaluator.
- Do not treat the four-run smoke manifest as a statistically meaningful benchmark; it is a rehearsal and sanity check only.

### Next Review Gate

Run the next review after one of these is complete:

1. A second task class, such as project initialization or research workflow, has real provider outputs, successful postprocess, and a documented interpretation of gap-compression metrics.
2. Project 1 has semantic trajectory labels for the existing A/B traces and at least one ablation result.
