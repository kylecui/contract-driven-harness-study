# V5 Paper Update — Decisions Log

**Started**: 2026-07-27
**Plan reference**: `.sisyphus/plans/paper-update-plan-v2.1.md`
**Purpose**: Capture every upstream decision that affects downstream WPs. Each decision has rationale + date + status.

---

## D1: PEtFiSh treatment = Option C (locked)

**Date**: 2026-07-27
**Status**: LOCKED
**Decision**: Contract-driven-harness paper positions PEtFiSh as follows:
- **Body architecture**: framework-agnostic core (320 lines) + framework adapter layer
- **PEtFiSh positioning**: recommended implementation, NOT the only reference
- **Citation**: `petfishframework v1.0, PyPI, MIT License`
- **Appendix C**: PEtFiSh-specific pack/skill details remain in supplementary, not main body

**Rationale**:
- Kimi's cross-framework experiment (pf 40/40 vs LangChain 37/40) provides preliminary evidence that the contract stack is framework-independent
- The 320-line framework-agnostic core (authored during Kimi's reproduction) demonstrates the protocol is implementable without PEtFiSh
- Option C balances: (a) clean contribution claim (contract stack is the contribution), (b) practical reproducibility (PEtFiSh is a usable substrate), (c) reviewer defense (framework-independence is empirically supported)

**Implications for downstream WPs**:
- WP1 (narrative): body text uses "framework-agnostic core"; PEtFiSh appears in §4.10 and Appendix C only
- WP3 (repro): 320-line core gets independent GitHub repo + DOI
- WP6 (citations): references list includes `petfishframework v1.0` with PyPI link
- ContractBench-v1 (WP4): described as task family + evaluator release, not PEtFiSh-tied benchmark

---

## D2: Multi-model interchangeability claim wording (frozen)

**Date**: 2026-07-27
**Status**: FROZEN (pending verification)

**Above-floor claim** (used in §3.7, §4.11-appendix):
> "Within the above-floor models tested (Qwen3-8B, GLM-4-9B, Qwen3-14B, DeepSeek-V3.2), a frozen contract produced zero-shot pass rates of 40/40 (Wilson [0.912, 1.000]) on the controlled-state-mutation task family."

**Below-floor claim** (downgraded from v2's "floor is structural"):
> "In one below-floor model tested (Qwen2.5-7B), we observed structural-level failure (0/40) characterized by inability to produce syntactically valid JSON, suggesting a categorical capability threshold for this task family. We do not claim universality of this floor characterization; it is scoped to one model in one task family."

**Rationale for wording**:
- "Within above-floor models tested" — scoped to actual sample, not universal
- "Zero-shot" — explicit that no repair was applied to non-Qwen3-8B models
- "On the controlled-state-mutation task family" — task scope explicit
- Below-floor uses "in one model" + "do not claim universality" — honest about n=1

**Conditions for upgrade**:
- Add 2+ below-floor models with consistent structural failure → can claim "structural floor observed across N models"
- Currently: not in scope for v5 (per Executor kill list)

---

## D3: Body vs Appendix placement (BLOCKER-4 resolution)

**Date**: 2026-07-27
**Status**: LOCKED

**Body (main paper)**:
- §3.4 Failure Classification Rule + Obligation×Field Coverage Matrix
- §3.5 Frozen Protocol Specification
- §3.6 Repair-Loop Protocol (already in V4, elevated)
- §3.7 Model Admission Protocol (NEW, replaces v2 §4.12 probe methodology)
- §4.9 Automated Replication by an LLM Agent (Kimi data, with verification status)
- §4.10 Cross-Framework Transfer (subject to BLOCKER-3 TOST gate)

**Appendix**:
- Appendix C: PEtFiSh-specific details (kept in supplementary as before)
- Appendix D (NEW): Multi-model interchangeability full data (5×40 records)
- Appendix E (NEW): Contract evolution ledger (v1→v5 contract diffs)

**Rationale**:
- §3.7 (probe methodology) promoted to body because it is a portable methodological contribution (per Opportunity lever 2)
- §4.11/4.12 multi-model data demoted to appendix because: (a) subject to WP3-前置 verification; (b) detailed per-model data is reference material, not narrative
- GLM zero-repair case: appendix worked example only (per P5 patch — promotion to abstract requires a priori held-out prediction ≥2 failures)

---

## D4: Target venue strategy (open — requires author input)

**Date**: 2026-07-27
**Status**: OPEN (author to decide before WP1 final draft)

**Candidate venues analyzed**:

| Venue class | Examples | Fit | Notes |
|---|---|---|---|
| SE main track | ICSE, FSE, ASE | Medium | Strong on methodology + threats to validity; weak on small sample size; AgentSpec/ABC differentiation critical |
| Industry track | EMNLP industry, NAACL industry, ICSOC | **High** | Values working protocol + reproducible artifact + cost analysis; this paper could be best-in-class |
| NLP/ML methods | EMNLP main, ACL main | Low-Medium | Reviewers expect benchmarks; this paper offers methodology + case study |
| Agent workshop | AgentBench workshop, LLM Agents workshop | High (but lower prestige) | Strong fit, smaller audience |

**Recommendation**: EMNLP/NAACL Industry track or ICSOC. These venues:
- Value practitioner artifacts (ContractBench, 320-line reference core, 4-tier admission funnel)
- Tolerate single-task-family case studies if execution is rigorous
- Have AI Use Disclosure policies that align with our BLOCKER-1 mitigation
- Lower risk of desk-reject on sample size grounds

**Author to confirm**: This decision affects:
- WP1 emphasis (Industry: practitioner checklist prominent; SE: Threats to Validity prominent)
- WP5 priority (Industry: Stage D cost matrix is critical; SE: can defer to v5.1)
- WP6 final formatting

---

## D5: AI Use Disclosure required (BLOCKER-1)

**Date**: 2026-07-27
**Status**: LOCKED

**Decision**: Add `Use of AI Assistance` section near end of paper (before References).

**Minimum content**:
1. Kimi Agent (Moonshot AI) executed experiments: Stage B v5.4 replication, 5-model interchangeability, cross-framework, floor probes
2. Author provided SiliconFlow API key (compute paid by author)
3. Author did NOT author the paper text using Kimi; Kimi did not design the original contract
4. Verification status: author will re-run sanity check (Qwen3-8B single-model 40 runs); multi-model data pending confirmation
5. LLM-evaluating-LLM circularity: acknowledged as methodological limit
6. Label used throughout: `automated replication by an LLM agent (Kimi Agent)` (NOT `independent replication`)

**Draft**: `research/07_reviews/ai-use-disclosure.md` (in progress via deep agent)

---

## D6: Stage D in v5.1 only (kill from MVP)

**Date**: 2026-07-27
**Status**: LOCKED

**Decision**: Stage D matched overhead matrix is deferred to v5.1. Only the protocol preregistration is in v5.

**Rationale**:
- Critic's WP4-before-WP5 dependency is broken by scope-cutting GLM zero-repair (no longer load-bearing claim)
- v5 will have zero cost data — this is a known gap, acknowledged in Threats to Validity
- Industry track venues will ask about cost; we will preregister the protocol and note "results under preparation for v5.1"

**Implications**:
- WP5 contains only `stage-d-overhead-matrix-protocol.md` for v5
- §4.13 in paper draft becomes "Future Work: Stage D" instead of results

---

## D7: Killed items (per Executor kill list)

**Date**: 2026-07-27
**Status**: LOCKED

The following items are explicitly killed from v5 scope (will NOT be done for v5 release candidate):

| Item | Original location | Killed because |
|---|---|---|
| WP5 #2 G9 object ablation (5-arm suite) | v1 WP5 | One new Stage worth of work; not load-bearing for v5 claims |
| WP5 #3 adversarial perturbation extension | v1 WP5 | Speculative; evaluator-overfit partially addressed by known-bad anchor discipline |
| Add 1-2 more below-floor models | v1 risk register | n=1 scope acknowledged in D2 wording; diminishing returns |
| Expand sample size to 80-100 runs | v1 risk register | Wilson [0.912, 1.000] at 40 runs sufficient for current claim wording |
| "Floor is structural" strong claim | v2 implicit | Downgraded in D2 |
| Stage 7r-smoke last A8R run | existing backlog | 35/36 complete; last run repeatedly times out; explicitly permanent defer |
| Appendix C in main PDF | v1 WP6 | Moved to supplementary per Option C |

---

## Decision Log Maintenance

- New decisions append to this file with D{n} prefix
- Status transitions: OPEN → LOCKED (no reversal without explicit decision log entry)
- Each LOCKED decision is binding on all downstream WPs
- Author overrides require new D{n} entry explaining the override

---

## Status Summary

- **LOCKED**: D1, D2 (pending verification), D3, D5, D6, D7
- **OPEN**: D4 (target venue — author input required)

Once D4 is locked, WP1 narrative restructuring can begin in full.
