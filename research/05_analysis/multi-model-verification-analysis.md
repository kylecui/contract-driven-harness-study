# Multi-Model Verification Analysis (Author Confirmed)

**Date**: 2026-07-27
**Verifier**: Author (live API via `verify_stage_b_v54_live.py`)
**Protocol**: Stage B v5.4 frozen explicit-transition-delta, temperature=0, direct SiliconFlow API
**Status**: COMPLETED — Kimi's automated replication partially confirmed, with one material discrepancy

---

## Summary Table

| Model | Family | Kimi Report | Author Verified | Wilson 95% CI | Match |
|---|---|---|---|---|---|
| Qwen3-8B | Qwen3 8B | 40/40 | **40/40** | [0.9124, 1.0000] | ✅ exact |
| GLM-4-9B | GLM 9B | 40/40 ("zero-repair") | **30/40** | [0.5981, 0.8581] | ❌ **discrepancy** |
| Qwen3-14B | Qwen3 14B | 40/40 | **40/40** | [0.9124, 1.0000] | ✅ exact (after re-run) |
| DeepSeek-V3.2 | DeepSeek MoE | 40/40 | **40/40** | [0.9124, 1.0000] | ✅ exact |
| Qwen2.5-7B | Qwen2.5 7B | 0/40 | **0/40** | [0.0000, 0.0876] | ✅ exact |

\* Qwen3-14B: Initial run had 3 API read timeouts in canonical (37/40). Targeted re-run of canonical (8 reps, 0 timeouts, avg 7.1s latency) confirmed timeouts were transient infrastructure issues. Updated to 40/40 [0.912, 1.000].

---

## Per-Model Breakdown

### Qwen3-8B (primary model) — CONFIRMED 40/40

All 5 conditions × 8 reps passed. No caveats. Matches V4 frozen result and Kimi's report exactly.

### GLM-4-9B (THUDM/GLM-4-9B-0414) — DISCREPANCY 30/40

**What failed**:
- `unknown_state_paraphrase`: 0/8 (all 8 runs failed `residual_unknown_vocabulary_accuracy`)
- `field_alias`: 6/8 (2 runs failed `state_transition_accuracy`)

**What passed**:
- `canonical`: 8/8
- `evidence_order_shuffled`: 8/8
- `distractor_evidence`: 8/8

**Hypothesis for discrepancy with Kimi**:
1. GLM may have been updated between Kimi's run (2026-07-19) and author verification (2026-07-27) — `THUDM/GLM-4-9B-0414` is a dated snapshot, but routing/quantization may differ
2. Kimi may have used a different prompt variant or evaluator configuration for `unknown_state_paraphrase`
3. The `unknown_state_paraphrase` condition paraphrases state labels (e.g., "current_git_branch" → "active development branch"); GLM-4-9B may map these differently than Qwen3 models

**Impact on claims**:
- ❌ "GLM zero-repair one-pass" claim is DROPPED from v5
- ❌ GLM cannot be used as the "cross-architecture zero-repair" headline
- ✅ GLM still demonstrates above-floor capability on 3/5 conditions (canonical, evidence_order, distractor)
- ✅ The contract is still partially transferable to GLM, but requires additional repair-loop iterations to handle paraphrased state labels

### Qwen3-14B — CONFIRMED with infra noise 37/40

3 failures were API read timeouts on the first 3 calls of `canonical`. After the API warmed up, all subsequent 37 calls passed. The model itself shows no capability gap. **Treating as 37/37 valid = 100%** for claim purposes, with infrastructure noise noted.

### DeepSeek-V3.2 — CONFIRMED 40/40

All 40 runs passed. Different model family (MoE architecture) from Qwen3. Strongest cross-family transfer evidence after Qwen3-8B.

### Qwen2.5-7B — CONFIRMED 0/40 structural floor

All 40 runs failed at JSON parsing (model could not produce syntactically valid JSON for this task). Structural floor confirmed exactly as Kimi reported.

---

## Revised Multi-Model Claims (replacing D2 wording)

### Above-floor interchangeability (revised)

> "Within the above-floor models tested, a frozen contract produced strict-conforming pass rates of:
> - 40/40 (Wilson [0.912, 1.000]) on Qwen3-8B and DeepSeek-V3.2
> - 37/40 on Qwen3-14B (3 API timeouts excluded; 37/37 valid calls passed)
> - 30/40 (Wilson [0.598, 0.858]) on GLM-4-9B, with failures concentrated in the `unknown_state_paraphrase` condition
>
> The contract transfers zero-shot to Qwen3-8B, Qwen3-14B, and DeepSeek-V3.2. GLM-4-9B requires additional repair-loop iterations to handle paraphrased state labels. We do not claim universal interchangeability."

### Below-floor (unchanged)

> "In one below-floor model tested (Qwen2.5-7B), we observed structural-level failure (0/40) characterized by inability to produce syntactically valid JSON."

### Dropped claims

- ❌ "GLM-4-9B zero-repair one-pass" — not supported by author verification
- ❌ "4 models at 40/40" — only 2-3 models reach 40/40 (depending on how infra noise is treated)
- ❌ Figure 1 "Contract Portability Matrix" showing 4 models at 40/40 — needs revision to show actual distribution

---

## Implications for v5 Paper Structure

1. **Figure 1** must show the actual distribution: 2 models at 40/40 + 1 at 37/40 + 1 at 30/40 + 1 at 0/40. This is a MORE INTERESTING story than "4 models at 40/40" — it shows that contract transfer is real but not universal, and identifies a specific failure mode (paraphrase sensitivity in GLM).

2. **§4.11 (Appendix D)** now has richer data: the contract transfers perfectly to same-family models (Qwen3-8B, Qwen3-14B) and to a different MoE family (DeepSeek-V3.2), but shows partial transfer to GLM-4-9B. This is a more honest and more interesting finding than "all models pass."

3. **GLM failure analysis** becomes a valuable contribution: it identifies `unknown_state_paraphrase` as a stress test that reveals model-specific contract-interpretation gaps. This feeds directly into §3.4 (failure classification) — GLM's paraphrase failures are classified as **contract defects** (the contract's handling of paraphrased labels needs strengthening for GLM).

4. **AI Use Disclosure** now has a stronger justification: "Author verification caught a material discrepancy between Kimi's automated replication and live API results, demonstrating the value of independent verification even when the automated replication appears correct."

---

## Data Provenance

- All raw records: `research/05_analysis/author-confirmation-records/{model}-confirmed.json`
- Runner script: `research/04_methods/scripts/verify_stage_b_v54_live.py`
- API: SiliconFlow `https://api.siliconflow.cn/v1`, temperature=0, max_tokens=2048
- Models verified: `Qwen/Qwen3-8B`, `THUDM/GLM-4-9B-0414`, `Qwen/Qwen3-14B`, `deepseek-ai/DeepSeek-V3.2`, `Qwen/Qwen2.5-7B-Instruct`
- Verification date: 2026-07-27
- Total API calls: 200 (5 models × 5 conditions × 8 reps)
- Total elapsed: ~3 hours (including API timeouts and rate-limit cooldowns)
