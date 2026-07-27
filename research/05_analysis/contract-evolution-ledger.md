# Contract Evolution Ledger (Appendix E)

**Source**: Author's Stage B v5.x repair-loop iterations (2026-06-12 to 2026-06-15) + Kimi Agent automated replication (2026-07-19)
**Verified**: Author re-ran Stage B v5.4 on 2026-07-27 confirming the endpoint (40/40 on Qwen3-8B)

This ledger documents how the controlled-state-mutation contract evolved through repair-loop iterations. Each entry records: the failure observed, the missing obligation identified, the contract change, and the resulting pass rate.

---

## Stage B Contract Versions

### v4 (baseline: exact retention)

**Prior to v5, the contract covered:**
- Exact evidence array preservation
- Exact closed-vocabulary retention
- Schema validity for output JSON

**Pass rate on Stage B v4 protocol**: 4/4 smoke (local gate only, no model test)

**Missing**: state transition semantics, transition gate, retention attestation.

---

### v5 (initial state transition — FAIL)

**New obligation added**: apply one supplied state transition (event-api-approval-001: unknown → approved for `network_api_approval`) while preserving evidence bindings and residual state.

**Contract additions**:
- `transition_event` field in OutputContract
- `required_postconditions` declaring final state
- `transition_record` section in output schema

**Model test (Qwen3-8B, 4 runs)**: **0/4 strict pass**

**Failure analysis (classified per §3.4)**:
- **Contract defect**: `transition_gate` was not model-visible; model had to infer the gate structure
- **Contract defect**: `next_action` values were not enumerated; model emitted free-form descriptions
- **Contract defect**: evidence citation policy was not stated in the model-visible contract

**Repair action**: Add explicit gate structure + enumerate `next_action` values + declare evidence citation policy → v5.1

---

### v5.1 (transition contract repair — PARTIAL)

**Contract changes**:
- `transition_gate` made fully model-visible (status, permitted_action, satisfied_prerequisite, next_action, support_slot_ids)
- `next_action` enumerated: `complete_stage_b_v53_explicit_transition_delta`
- Evidence citation policy declared: "Use `evidence_ids` as the only reference field"
- Immutable slot-to-reference arrays moved to `evidence_bindings` (separate from claim prose)

**Local gate**: PASS (all known-bad fixtures caught for expected reasons)

**Model smoke (Qwen3-8B, 4 runs)**: **4/4 strict pass**

**Implication**: The v5 failures were entirely contract defects, not model capability limits. Once the gate was made explicit and next_action was enumerated, the model conformed.

---

### v5.2 (evidence-binding ablation — NULL RESULT)

**Question**: Does the evidence-binding representation (slot-to-reference arrays) causally affect pass rate?

**Design**: 2 profiles (with/without explicit evidence bindings) × 5 conditions × 3 reps = 30 runs

**Result**: Risk difference 0.067 (below 0.20 threshold); McNemar p=0.500

**Classification**: NULL result — no engineering-scale evidence-representation effect detected. Do not pool with future repairs.

---

### v5.3 (explicit transition delta — PASS)

**Question**: Does making the transition delta explicit in the contract improve stability?

**Contract change**:
- Added `required_transition_delta` field declaring exact operations (remove from unknown, remove from forbidden, add to known, preserve residual)
- Made `required_transition_gate` and `required_attestation` fully explicit in the contract

**Model test (Qwen3-8B, 30 runs paired)**: Risk difference 0.133 (below 0.20 threshold)

**Classification**: MIXED — explicit delta does not significantly improve over v5.1 alone, but provides clearer contract structure for downstream verification.

---

### v5.4 (frozen stability — PASS, AUTHOR CONFIRMED)

**Question**: Does the frozen v5.3 delta protocol show bounded absolute stability?

**Protocol frozen**:
- temperature = 0
- provider = SiliconFlow
- model = `Qwen/Qwen3-8B`
- evaluator version = `evaluate_stage_b_v51_state_transition.py` (unchanged)
- known-bad set = v5.1 fixtures
- perturbation set = 5 conditions × 8 reps

**Original result (2026-06-15, 40 runs)**: **40/40 strict pass**, Wilson [0.912, 1.000]

**Author verification (2026-07-27, 40 runs)**: **40/40 strict pass**, Wilson [0.912, 1.000] — EXACT MATCH

---

## Kimi Agent Automated Replication (v1 → v5 trajectory)

**Date**: 2026-07-19
**Agent**: Kimi Agent (Moonshot AI), using author's SiliconFlow API key
**Model tested**: Qwen3-8B (same as author)

Kimi independently re-implemented the protocol and observed the same 0/40 → 40/40 trajectory over 4 repair-loop iterations, with failure modes structurally similar to the author's v5 → v5.1 transition.

**Kimi iteration summary** (from automated replication report):

| Iteration | Pass rate | Key obligation surfaced |
|---|---|---|
| v1 | 0/40 | (initial contract, same as author's v5) |
| v2 | single-point pass | Exact evidence array + next_action enumeration |
| v3 | 21/40 | transition_record full JSON structure |
| v4 | 33/40 | Field-required declarations + canonical-name obligation |
| v5 | 40/40 | Canonical-name obligation extended to attestation field |

**Author verification of Kimi's endpoint (2026-07-27)**: Qwen3-8B 40/40 confirmed ✅

---

## Summary: What the Repair-Loop Surfaced

Over the v5 → v5.4 trajectory, the repair-loop externalized these previously-implicit obligations:

1. **Transition gate visibility** — the gate structure (status, permitted_action, prerequisites, next_action) was implicit in the task description but not declared in the model-visible contract
2. **Action enumeration** — `next_action` values were free-form; the contract required exact enum values
3. **Evidence citation policy** — "use evidence_ids as the only reference field" was implicit
4. **Transition delta operations** — the exact set of state additions/removals/preservations was not enumerated
5. **Canonical name coverage** — global obligations like "use canonical names" were not bound to specific output fields (notably the attestation field)

Each of these was a **contract defect** per the §3.4 classification rule — the obligation existed in the author's intent but was not declared in the model-visible contract. The repair-loop's function was to surface and externalize these implicit obligations.

---

## Scope and Limitations

- This ledger covers ONE task family (controlled state mutation) and ONE primary model (Qwen3-8B)
- The Kimi v1→v5 trajectory uses Kimi's own contract implementation, not the author's exact fixtures; structural similarity of failure modes is the basis of comparison
- Author verification confirms the endpoint (v5.4 on Qwen3-8B = 40/40) but does not re-verify each intermediate iteration
- The multi-model verification (Section 4.11) confirms transferability to Qwen3-14B and DeepSeek-V3.2 but NOT to GLM-4-9B (30/40, paraphrase condition failure)
