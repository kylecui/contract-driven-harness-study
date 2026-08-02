# V5 Update — Blocked Items and Required Author Actions

**Purpose**: Track every work item that cannot be completed without author input, external resources, or API access. Each item lists what blocks it and what the author needs to do.

**Status as of**: 2026-07-27

---

## B1: SiliconFlow API access (BLOCKS WP3-前置, WP5)

**What's blocked**:
- WP3-前置 sanity check (Qwen3-8B single-model 40 runs)
- WP3-前置 multi-model full verification (5 models × 40 runs)
- WP3-前置 TOST equivalence test (pf vs LangChain paired, temperature=0)
- WP5 Stage D matched overhead matrix

**What agent needs**:
- SiliconFlow API key with quota for ~800-2000 API calls (~¥30 cost estimate)
- Confirmation that the 5 model IDs are still active on SiliconFlow:
  - `Qwen/Qwen3-8B`
  - `THUDM/glm-4-9b-chat` (or current GLM-4-9B ID)
  - `Qwen/Qwen3-14B`
  - `deepseek-ai/DeepSeek-V3.2` (verify exact ID)
  - `Qwen/Qwen2.5-7B-Instruct` (verify exact ID)

**What agent will do once unblocked**:
1. Run `equivalence_pf_vs_lc.py` on freshly collected records
2. Run multi-model sanity check + full 5×40
3. Populate `research/05_analysis/author-confirmation-records/`
4. Update `v5-decisions-log.md` D2 with verification status

**Author action**: Set environment variables and run sanity check, OR delegate back to agent with API key.

---

## B2: 320-line framework-agnostic core (BLOCKS WP3 subtask 3)

**What's blocked**:
- Verification of zero PEtFiSh coupling (script exists but no core to scan)
- Independent GitHub repo + Zenodo DOI release

**What agent needs**:
- Access to the 320-line core Kimi built during reproduction. Currently lives at `Kimi sandbox: /mnt/agents/work/repro/contract_core.py` — not in this repo.
- OR: author reconstructs the core from the contract spec in `research/04_methods/`

**What agent will do once unblocked**:
1. Copy 320-line core to `reference-core/contract_core.py`
2. Run `verify_zero_petfish_dep.py --core-path reference-core/`
3. Resolve any BLOCKER findings
4. Create README + setup.py for independent release
5. Author creates GitHub repo + Zenodo DOI (auth required, cannot automate)

**Author action**: Provide the 320-line core file, OR confirm it should be reconstructed from spec.

---

## B3: Target venue decision (BLOCKS WP1 final draft, WP6 formatting)

**What's blocked**:
- Final narrative emphasis (Industry track vs SE main vs Workshop)
- Final paper formatting (LaTeX template)
- AI Use Disclosure placement (some venues require specific sections)

**What agent needs**:
- Author decision on D4 (venue strategy). Candidates analyzed in `v5-decisions-log.md`:
  - **Recommended**: EMNLP/NAACL Industry track or ICSOC (best-in-class fit)
  - Alternative: SE main track (ICSE/FSE/ASE) — requires stronger Threats to Validity
  - Alternative: Agent workshop — lower prestige, faster turnaround

**What agent will do once unblocked**:
1. Lock D4 in decisions log
2. Adjust WP1 narrative emphasis accordingly
3. Choose LaTeX template for target venue
4. Finalize AI Use Disclosure section placement

**Author action**: Review D4 analysis and lock venue.

---

## B4: Zenodo / HuggingFace accounts (BLOCKS ContractBench-v1 + 320-line DOI)

**What's blocked**:
- ContractBench-v1 artifact publication (HuggingFace datasets or Zenodo)
- 320-line core DOI assignment (Zenodo)

**What agent needs**:
- Author Zenodo account (for DOI minting)
- Author HuggingFace account (for dataset publication, alternative to Zenodo)
- OR: GitHub repo with Zenodo integration enabled (auto-DOI on release)

**What agent will do once unblocked**:
1. Package ContractBench-v1 datasheet + records
2. Create GitHub release for 320-line core (triggers Zenodo DOI)
3. Mint DOIs and reference them in paper

**Author action**: Create accounts OR confirm GitHub+Zenodo integration approach.

---

## B5: Contract evolution ledger data (BLOCKS Appendix E)

**What's blocked**:
- Appendix E: Contract v1→v5 diff archive
- Requires Kimi's per-iteration contract snapshots OR reconstruction from session logs

**What agent needs**:
- Kimi sandbox path: `/mnt/agents/work/repro/` (contract snapshots v1-v5)
- OR: author's own repair-loop iteration records from `research/04_methods/`

**What agent will do once unblocked**:
1. Extract contract diffs v1→v2→v3→v4→v5
2. Cross-reference each diff with the failure that triggered it
3. Render as Appendix E (chronological table)

**Author action**: Provide Kimi's contract snapshots OR confirm reconstruction approach.

---

## B6: Stage D cost data (BLOCKS §4.13 / Future Work)

**What's blocked**:
- Stage D matched overhead matrix execution
- Author's actual contract-authoring time logs (for calibration)

**What agent needs**:
- API access (same as B1)
- Author's actual time-on-task for one repair-loop iteration (Kimi estimate exists but needs calibration)

**What agent will do once unblocked**:
1. Run G0 vs G9 × 2 models × {cost, latency, retry, per-pass cost}
2. Calibrate against author's actual hours
3. Write §4.13 or "Future Work: Stage D" depending on whether v5 or v5.1

**Note**: Stage D is deferred to v5.1 per D6. Only the protocol preregistration is in v5 scope.

**Author action**: Confirm defer to v5.1 OR provide time logs for v5 inclusion.

---

## Summary of Completed Autonomous Work

Despite the blockers above, the following v2.1 plan items are **complete**:

| Plan item | Status | Artifact |
|---|---|---|
| WP0-1 PEtFiSh decision | ✅ | `research/06_outputs/v5-decisions-log.md` (D1) |
| WP0-2 venue analysis | ✅ | `research/06_outputs/v5-decisions-log.md` (D4, OPEN for author) |
| WP0-4 claim wording freeze | ✅ | `research/06_outputs/v5-decisions-log.md` (D2) |
| WP0-5 body/appendix placement | ✅ | `research/06_outputs/v5-decisions-log.md` (D3) |
| WP0-6 AI Use Disclosure | ✅ | `research/07_reviews/ai-use-disclosure.md` |
| WP0-3 AgentSpec/ABC differentiation | ⏳ in progress | (deep agent running) |
| WP1-1 reframe + P1 scope-limit | ✅ | `research/06_outputs/v5-reframe-and-scope-limit.md` |
| WP1-3 Figure 2 convergence CSV | ✅ | `research/05_analysis/figure-2-convergence-data.csv` |
| WP1-4 Table 2 experiment overview | ✅ | `research/05_analysis/table-2-experiment-overview.csv` |
| WP1-7 Glossary | ✅ | `research/06_outputs/glossary.md` |
| WP2 methodology sections | ⏳ in progress | (deep agent running) |
| WP3-前置-2 TOST equivalence script | ✅ | `research/04_methods/scripts/equivalence_pf_vs_lc.py` |
| WP3-3 320-line verification script | ✅ | `research/04_methods/scripts/verify_zero_petfish_dep.py` |
| WP6-1 citation key audit | ✅ | V4 has no bare `\cite{}` keys (already prose-style) |
| WP6 kill list applied | ✅ | `v5-decisions-log.md` (D7) |

## What author should do next (priority order)

1. **Lock D4 (venue)** — unblocks WP1 final emphasis + WP6 formatting
2. **Provide Kimi 320-line core OR confirm reconstruction** — unblocks WP3 subtask 3
3. **Run WP3-前置 sanity check** — unblocks §4.9, §4.10, §4.11 data confirmation
4. **Set up Zenodo/GitHub integration** — unblocks ContractBench + 320-line DOI

Once items 1-3 are resolved, the agent can produce a complete v5 draft in ~1 week of part-time work. Items 4 is parallel/optional for v5 release candidate.

---

## v5 MVP feasibility without unblocking

If the author chooses NOT to unblock any items (e.g., time-constrained), the achievable v5 is:
- New methodology sections (§3.4, §3.5, §3.7) — fully written
- Reframed abstract + intro (Essence reframe + scope-limit)
- Glossary + Table 2 + Figure 2 data
- AI Use Disclosure section
- Related Work differentiation table (vs AgentSpec/ABC)
- v4 frozen body preserved

The v5 draft would **NOT include** §4.9-§4.13 (data unverified) — those would be stubs pointing to "external replication reported by Kimi Agent; author verification pending". This is the absolute MVP that maintains academic honesty.
