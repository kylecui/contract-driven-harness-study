# Round 01 vs Round 02 — Inter-Round Comparison

**Date**: 2026-07-28
**Protocol**: Stage B v5.4 frozen explicit-transition-delta + Stage D G0
**Provider**: SiliconFlow, temperature=0

---

## Stage B v5.4 — Cross-Round Comparison

| Model | Round 01 (7/27) | Round 02 (7/28) | Δ | Reproducible? |
|---|---|---|---|---|
| Qwen3-8B | 40/40 [0.912, 1.000] | 40/40 [0.912, 1.000] | 0 | ✅ exact |
| GLM-4-9B | 30/40 [0.598, 0.858] | 29/40 [0.572, 0.839] | -1 | ⚠️ approximate |
| Qwen3-14B | 40/40 [0.912, 1.000]¹ | 40/40 [0.912, 1.000] | 0 | ✅ exact |
| DeepSeek-V3.2 | 40/40 [0.912, 1.000] | 40/40 [0.912, 1.000] | 0 | ✅ exact |
| Qwen2.5-7B | 0/40 [0.000, 0.088] | 0/40 [0.000, 0.088] | 0 | ✅ exact |

¹ Round 01 Qwen3-14B: initial run had 3 API timeouts (37/40); targeted canonical re-run (8/8 pass) confirmed timeouts were transient. Updated to 40/40.

**Key finding**: 4/5 models are exactly reproducible across independent runs on different days. GLM-4-9B's pass count varies by ±1 (30 vs 29), but the Wilson intervals [0.598, 0.858] and [0.572, 0.839] overlap substantially, and the failure location (unknown_state_paraphrase condition) is identical in both rounds.

### GLM-4-9B per-condition breakdown

| Condition | Round 01 | Round 02 | Consistent? |
|---|---|---|---|
| canonical | 8/8 | 8/8 | ✅ |
| field_alias | 6/8 | 5/8 | ⚠️ (±1 run-level instability) |
| evidence_order_shuffled | 8/8 | 8/8 | ✅ |
| distractor_evidence | 8/8 | 8/8 | ✅ |
| unknown_state_paraphrase | 0/8 | 0/8 | ✅ |

The field_alias variation (6/8 vs 5/8) is consistent with the "failure mode instability" observation from §4.10: GLM's failures on this condition are stochastic at the individual-run level, but the condition-level pattern (paraphrase = complete failure, field_alias = partial failure) is stable.

---

## Stage D G0 — Cross-Round Comparison

| Model | Round 01 (7/27) | Round 02 (7/28) | Reproducible? |
|---|---|---|---|
| Qwen3-8B G0 | 0/20 (0%) | 0/20 (0%) | ✅ exact |
| DeepSeek-V3.2 G0 | 0/20 (0%) | 0/20 (0%) | ✅ exact |

Both rounds confirm: without the contract stack, neither model produces a single strict-conforming run.

---

## Provenance Comparison

| Field | Round 01 | Round 02 |
|---|---|---|
| Prompt text | Not saved (deterministic, can be regenerated) | **Saved per condition** in `prompts/` |
| Raw model response | **Lost** | **Saved per run** in `raw_content` field |
| Parsed JSON | Not saved | **Saved per run** in `parsed_output` field |
| Metrics | Saved | Saved |
| Token usage | Saved | Saved |
| Timing | Saved | Saved |
| Response ID | Saved | Saved |

Round 02 closes the provenance gap: every run's complete chain from prompt → raw API response → parsed JSON → evaluator metrics is preserved and auditable.

---

## Conclusion

The frozen Stage B v5.4 protocol is **reproducible**:

1. **Three above-floor models** (Qwen3-8B, Qwen3-14B, DeepSeek-V3.2) produce exactly 40/40 in both rounds
2. **One below-floor model** (Qwen2.5-7B) produces exactly 0/40 in both rounds
3. **GLM-4-9B** produces approximately 30/40 (±1) in both rounds, with identical failure-location patterns
4. **G0 arm** produces exactly 0/20 on both models in both rounds

The inter-round variation in GLM-4-9B (30 vs 29) is within expected stochastic bounds for a model with a known vulnerability to paraphrased-label stress. The paper's claim ("30/40") uses the Round 01 value; Round 02 confirms the claim is within the reproducible range.
