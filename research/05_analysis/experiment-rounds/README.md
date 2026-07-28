# Experiment Rounds Index

This directory contains all author-executed experiment rounds for the contract-driven-harness paper. Each round is an independent execution of the same frozen protocol, with complete provenance where available.

## Rounds

| Round | Directory | Date | API Calls | Provenance | Purpose |
|---|---|---|---|---|---|
| 01 | `round-01-author-verification-20260727/` | 2026-07-27 | 200 (Stage B) + 40 (Stage D) | Partial (metrics + usage, no raw model outputs) | Initial author verification of Kimi's automated replication |
| 02 | `round-02-full-reproducibility/` | 2026-07-28 | 200 (Stage B) + 40 (Stage D) | **Complete** (prompt + raw response + parsed JSON + metrics + usage per run) | Full reproducibility verification with complete provenance |

## Protocol

Both rounds use the same frozen Stage B v5.4 explicit-transition-delta protocol:
- Temperature: 0
- Provider: SiliconFlow
- Models: Qwen3-8B, GLM-4-9B-0414, Qwen3-14B, DeepSeek-V3.2, Qwen2.5-7B-Instruct
- Conditions: canonical, field_alias, evidence_order_shuffled, distractor_evidence, unknown_state_paraphrase
- Reps per condition: 8 (Stage B), 4 (Stage D G0)
- Evaluator: 7 deterministic checks (schema, evidence array, unknown vocabulary, transition, gate, attestation, aggregate)

## Inter-Round Comparison

See `_comparison-round-01-vs-02.md` for the full cross-round analysis.

**Summary**: 4/5 models are exactly reproducible (Qwen3-8B, Qwen3-14B, DeepSeek-V3.2 at 40/40; Qwen2.5-7B at 0/40). GLM-4-9B is approximately reproducible (30/40 vs 29/40, within Wilson interval overlap), with the failure location (paraphrase condition) stable but individual failure count varying by ±1.

## Provenance Gap in Round 01

Round 01 runs (`verify_stage_b_v54_live.py`) saved metrics, pass/fail, and token usage, but did **not** save:
- The exact prompt text sent to the API
- The raw model response text
- The parsed JSON output

These can be partially retrofitted:
- Prompts are deterministic (loaded from frozen fixture files)
- Raw model outputs are **lost** (cannot be recovered)
- Round 02 closes this gap with complete per-run provenance

## Adding New Rounds

To run a new round:
```bash
# Stage B v5.4 (5 models × 40 runs ≈ 2-3 hours)
python research/04_methods/scripts/run_full_experiment.py stage-b \
    --all-models \
    --output-dir research/05_analysis/experiment-rounds/round-NN-description

# Stage D G0 (2 models × 20 runs ≈ 30-60 min)
python research/04_methods/scripts/run_full_experiment.py stage-d \
    --models qwen3-8b deepseek-v3.2 \
    --output-dir research/05_analysis/experiment-rounds/round-NN-description
```
