# Submission Strategy and Revision Plan

Prepared 2026-08-27, based on the v5.1 draft (commits through `f63857f` + arXiv package).
This is a living document: update after each venue decision.

## 1. Asset Inventory (what we have now)

| Asset | State | Weight in review |
|---|---|---|
| Paper v5.1, 37 pp | Complete narrative: contract stack, repair loop, multi-model, oracle-coupling audit (§4.14 + Fig. 5), testing/RL-safety literature anchoring, table/figure caption discipline | High |
| Reproducibility package | Frozen artifacts, per-module SHA-256 closures, `verify_all.py` 6/6 on Windows+Linux, cross-platform eol fix, platform README | High (SE venues) |
| Reproduction rounds | 4 rounds, 1,458 API calls; Round 04 bit-exact (sim=1.0) | High |
| Claim-boundary discipline | Non-claims appendix, evidence traceability (App. C), AI-use disclosure, conflict-of-interest note | High |
| Experimental scale | **Single task family, 40 runs/cell, 5 low-cost CN-market models** | **Weakness — top-venue reviewers will attack** |

## 2. Venue Decision Tree

```
Now ──── arXiv v1 (timestamp; allowed by all target venues below; S&P caveat in checklist)
  │
  ├─ Path A (PRIMARY, SE):  ISSTA 2027 → fallback ASE 2027 → fallback TSE / EMSE
  │    Rationale: oracle-coupling + metamorphic relations + fixture-driven gates
  │    is native ISSTA language; §2.5/§4.14 literature anchoring already done.
  │
  ├─ Path B (SECONDARY, Security): USENIX Sec '27 / NDSS '27 → fallback TDSC / C&S
  │    Rationale: "who audits the auditor" (monitor trustworthiness) is a real gap
  │    in agent-security literature; 55 authority-perturbation checks read as
  │    access-control attack surface tests. BLOCKED on: explicit threat model +
  │    live adversary experiments (see §4, work item W-SEC).
  │
  └─ Path C (fast publication): IEEE Software magazine (2–4 mo) — only if speed
       dominates; requires rewrite to ~10 pp practitioner article. Not recommended
       before Path A has had one cycle.
```

## 3. Timeline (ISSTA 2027 dates verified from conf.researchr.org, 2026-08-27)

**ISSTA 2027 (Singapore): abstract 2027-01-08, full paper 2027-01-11, results 2027-04-20→06-17, conference 2027-09-07/10.**
Format: ACM `acmsmall` + `review,anonymous`, 18 pp incl. appendix (refs unlimited), mandatory Data Availability section, double-blind (arXiv posting allowed).

| When | Action |
|---|---|
| 2026-09 | Post arXiv v1; start W-A1–W-A3 conversion |
| 2026-09 → 12 | Complete **W-A4 (second task family)** — ~4 months available, no excuse to skip |
| 2026-12 | Freeze submission text; internal review pass against ISSTA review criteria |
| 2027-01-08 | ISSTA abstract deadline |
| 2027-01-11 | ISSTA full-paper deadline |
| 2027-03-22→25 | Author response period (reserve calendar) |
| 2027-04-20 | Initial notification |
| 2027-06-17 | Final notification (after major-revision round 2027-05-20) |
| if rejected 2027-06 | ASE 2027 deadline (typically ~April may have passed → FSE 2028 cycle ~Sept 2027, or TSE/EMSE immediately; attach ISSTA reviews) |
| parallel, optional | Path B (USENIX Sec '27 cycle 2 / NDSS '27 fall cycle) if W-B2 executed in 2027 Q1 |

## 4. Gap-to-Acceptance Work Items

### Path A (SE) — required before ISSTA 2027-01-11
| ID | Item | Effort | Notes |
|---|---|---|---|
| W-A1 | Convert to ACM `acmsmall` 2-column (`review,anonymous`); 18 pp incl. appendix, refs unlimited; move App. C–F matrices to supplementary; add required "Data Availability" section; anonymize for double-blind (Kimi/author rounds phrasing, repo links, **and the PEtFiSh self-citation — replace with "a skill-pack framework" + anonymous artifact link**) | 3–4 days | ISSTA artifact track submission is a major acceptance multiplier — freeze `verify_all.py` + closures into an anonymous Zenodo/GitHub snapshot |
| W-A2 | Promote §2.5 testing-theory paragraph into Introduction/§2 lead positioning (SE reviewers must see the lineage in the first 2 pages) | 0.5 day | Text already written, needs relocation + intro paragraph |
| W-A3 | References: switch to ACM numbered style via BibTeX during LaTeX conversion | 0.5 day | Bib ready (31 verified entries) |
| W-A4 (**mandatory** — 4 months available) | Second task family (different state-machine grammar) through the same repair-loop protocol; report as §4.x with same claim-boundary discipline | 3–5 weeks | Directly answers the #1 expected review: "one task family"; also feeds the metamorphic audit story (grammar transfer) |
| W-A5 | Threats-to-validity as a named section (ISSTA reviewers expect it; currently spread §5/App. A) | 0.5 day | Mostly rearrangement |
| W-A6 | Consider "Replicability Study" or "Experience Paper" category framing — our 4-round reproduction + freeze-and-verify artifacts fit ISSTA's explicit track | 1 day | Decide at freeze; Research Paper remains default |

### Path B (Security) — required to unlock
| ID | Item | Effort | Notes |
|---|---|---|---|
| W-B1 | Explicit adversary model: who poisons the answer channel / tampers authority, when, with what capability | 3–4 days | Material exists (§4.14 design), needs security framing |
| W-B2 | Live adversary experiments: prompt-injection attempts against the gate, measured ASR with/without contract | 4–6 weeks | **Hard blocker**; without numbers, security reviewers reject |
| W-B3 | Related work: prompt-injection defense lineage (AgentSpec, LlamaFirewall already cited; add 5–8 core agent-security works) | 3–4 days | Librarian verification pass needed (same discipline as §2.5 additions) |

### Continuous
| ID | Item | Effort |
|---|---|---|
| W-C1 | Record arXiv DOI after posting; keep README + this file in sync | minutes |
| W-C2 | Keep artifact `verify_all.py` green in CI if a repo CI is added later | ongoing |

## 5. Decision Rules

1. Primary commitment: **ISSTA 2027, full paper 2027-01-11**. Work backwards: submission freeze 2026-12-15; W-A4 must start no later than 2026-10-15.
2. W-A6 category decision (Research vs Replicability Study) at freeze — if W-A4 succeeds, Research Paper; if W-A4 slips, the freeze-and-verify + 4-round reproduction still supports a strong Replicability Study submission on schedule.
3. If ISSTA rejects (2027-06-17): major-revision-quality feedback → FSE 2028 (deadline ~Sept 2027, ~2.5 months turnaround) OR TSE/EMSE immediately with review-response letter. EMSE preferred if speed matters.
4. Path B only if W-B2 completes before the target CFP; otherwise it stays the journal fallback angle for TDSC.
5. Never submit to IEEE Access (reputation cost exceeds speed benefit).

## 6. Known Risks

| Risk | Mitigation |
|---|---|
| "Single task family" rejection | W-A4; non-claims already scoped; emphasize methodology over universality |
| LLM-executed experiments (Kimi) skepticism | AI-use disclosure + author verification rounds already in App. F; foreground in cover letter |
| CN-market models unfamiliar to reviewers | Frame as deliberate low-cost-tier claim, not oversight; SiliconFlow is OpenAI-compatible |
| arXiv posting vs double-blind venues | All Path A/B venues allow arXiv; only S&P restricts — excluded from tree |
