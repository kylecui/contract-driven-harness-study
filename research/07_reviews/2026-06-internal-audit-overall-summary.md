# Internal Audit Overall Summary (2026-06-30)

Branch: `review/2026-06-internal-audit`
Scope: comprehensive review of project quality and paper quality, with explicit anti-sycophancy posture per user request. Also assesses whether the 2026-02-17 LangChain "harness engineering" blog reduces the paper's significance.

This document is a cross-cutting summary. The three underlying reports must be read for full detail:

- `2026-06-internal-audit-critical-review.md` - six-dimensional critical review of V4 paper
- `2026-06-langchain-blog-differentiation-analysis.md` - LangChain blog overlap/conflict/differentiation
- `2026-06-engineering-quality-audit.md` - project-level engineering quality audit

## Headline Verdicts

| Question | Answer |
|---|---|
| Will the LangChain blog make our paper lose meaning? | **No.** Risk is in naming/visibility, not in scientific meaning. In one dimension (motivation) LC actually reinforces the paper. |
| Is the V4 paper internally sound? | **Mostly yes, with one structurally underpowered statistical design.** All five headline numbers are arithmetically correct; the issue is interpretation. |
| Is the project engineering healthy enough to support the paper? | **Grade B.** Reproducibility chain is real; README/source-index/threshold-centralization gaps must be closed before external submission. |
| What is the realistic venue outcome today? | ICML/NeurIPS main track: Reject. ACL/EMNLP main: Weak Reject to Borderline. Systems venue (ICSE/FSE/ASE) or workshop: Weak Accept after the W2 wording fix. |

## 1. LangChain Blog vs This Paper (Task 3 summary)

Detailed report: `2026-06-langchain-blog-differentiation-analysis.md`.

The two pieces share the phrase "harness engineering" but address incommensurable problems.

| Dimension | LangChain blog | This paper V4 |
|---|---|---|
| Problem | Single strong-model benchmark optimization | Low-cost-model bounded-reliability enablement |
| Model | gpt-5.2-codex (frontier) | Qwen/Qwen3-8B (low-cost) |
| Benchmark | Terminal Bench 2.0, score 52.8 -> 66.5 | Frozen explicit-transition-delta G9 protocol, 40/40 strict |
| Mechanism | System Prompt / Tools / Middleware (hooks) | TaskSpec / MemorySlice / EvidenceBundle / OutputContract / WorkflowGate / TraceLog / ValidatorGate |
| Method loop | Trace analysis skill -> harness tweak | Repair-loop protocol + mechanism atom + stability confirmation |
| Evidence type | Benchmark rank movement | Deterministic contract adherence, fresh-run stability |

Method overlap is **orthogonal**, not subset/superset. LangChain's Middleware is procedural runtime hooks; this paper's ValidatorGate is a deterministic contract checker over author-declared obligations. LangChain does not introduce obligation externalization, known-bad fixtures, or repair-loop protocols. This paper does not optimize benchmark rank.

Evidence does not conflict. The two results answer different questions on different model tiers and can coexist without mutual weakening.

**Real risk is communication, not science.** LangChain published 2026-02-17, four months before V4 freeze. Readers searching "harness engineering" will find LangChain first, and may assume this paper is an academic restatement. The paper's title qualifier "Contract-Driven" mitigates this but does not eliminate it.

**Action.** In V4.1 or V5, explicitly cite the LangChain blog in three positions:
- Abstract: one clause noting that industrial harness-engineering work optimizes strong-model benchmark performance, while this paper studies obligation externalization for low-cost-model bounded reliability.
- Introduction: paragraph distinguishing "benchmark-oriented harness engineering" from "contract-driven harness engineering".
- Related Work Section 2.1 or a new Section 2.6: position LC as adjacent industrial practice, not prior art that subsumes the contribution.

Do not treat LC as a threat to ignore; treat it as converging industrial evidence that harness engineering matters, which this paper formalizes for a different model tier with a different mechanism.

## 2. Critical Paper Review (Task 2 summary)

Detailed report: `2026-06-internal-audit-critical-review.md`.

### 2.1 Numbers independently verified

All five headline statistics are arithmetically correct.

| Number | Paper value | Recomputed | Status |
|---|---|---|---|
| 40/40 Wilson | [0.912, 1.000] | [0.912, 1.000] | exact |
| 8/8 Wilson | [0.676, 1.000] | [0.676, 1.000] | exact |
| McNemar p (b=2,c=0) | 0.500 | 0.500 | exact |
| Risk difference | 0.133 | 0.133 | exact |
| Threshold 0.20 on n=15 | >=3 passes | 3.0 | exact |

The issue is not arithmetic. It is interpretation and design.

### 2.2 Sharpest finding (W2): the design closed off the preregistered positive result before any data was read

This is the most attackable weakness and the internal A-grade review did not surface it.

- **McNemar floor.** With `n_discordant=2`, the two-sided exact McNemar p-value has a hard lower bound of 0.5. The test cannot reject at alpha=0.05 no matter how large the true effect is. The paper says "little power for small effects"; the correct statement is "zero power for any effect detectable at conventional alpha".
- **Threshold unreachable after control=13/15.** The 0.20 absolute risk-difference threshold on n=15 requires `treatment - control >= 3` passes. Once control achieved 13/15, the maximum achievable difference was capped at 2 (if treatment went 15/15). The threshold became structurally unreachable regardless of treatment performance.
- Both preregistered positive analyses were therefore closed off by the observed control strength. The paper frames v5.3 as "did not meet threshold"; the deeper truth is "the design as preregistered could not have produced the threshold result once the control reached its observed level".

This is a design-level finding, not a post-hoc critique of the outcome. A proper power analysis on expected discordant pairs should have been part of the preregistration. The paper concedes "no separate utility analysis for the cutoff" (line 227) but understates the consequence.

**Highest-leverage fix.** Add two sentences to Section 4.8 and Section 5.1 stating the structural power limit proactively. Zero additional runs required. Converts W2 from a hidden reviewer-attack surface into an author-declared boundary.

### 2.3 Six-dimensional scores

Novelty 4 / Soundness 5 / Evaluation 3 / Presentation 6 / Reproducibility 7 / Ethics 7.

Weakest dimension is Evaluation: N=1 task, single model, single provider, author-designed perturbations, deterministic author-written evaluators, G9-vs-G0 bundle comparison without isolating which harness component does the work.

### 2.4 AI-slop scan: the prior review scanned too narrow

The prior `contract-driven-harness-v4-ai-slop-review.md` only checked four keywords (`robust`, `novel`, `comprehensive`, `effective`) and passed. It missed the residue class that actually exists: **author self-evaluation language** rather than empty authority language.

Concrete residues (line numbers from V4 frozen markdown):
- L30 "The strongest evidence in this study comes from the repair loop"
- L187 "The main methodological contribution is"
- L371 "Stage B adds an important qualification"
- L429 "The practical value is the repair loop"
- L262, L375 "clearest positive gap-compression result" (used twice)

Each is individually defensible. The pattern is the issue: the paper tells the reader how to weight its own evidence. A stricter rewrite would let the reader do the weighting.

### 2.5 Other attack surfaces (full list in the critical review)

- Single fixture family (N=1 task, 5 cosmetic perturbations).
- Single provider (SiliconFlow) and single model (Qwen3-8B); provider-independent claim explicitly disclaimed but the abstract still reads as a general finding.
- Stage 7e v4 and Stage 7-next use n=4 targeted smoke runs; Wilson interval [0.51, 1.0] carries almost no statistical information.
- Survivorship / retry-as-data: "after retry", "after documented timeout recovery", retry policy underspecified.
- Stage 6 "outperformed the unconstrained strong model" framing is a harness-vs-no-harness confound, not a model-vs-model result.
- The 0.20 threshold is not power-derived; the paper concedes this.
- Fisher vs McNemar primary-analysis switch post-hoc; Fisher value retained in audit record but not reported in the paper body.
- PEtFiSh specificity: fixtures deeply project-specific; "transferable constructs" asserted, not shown.
- Gap compression thesis downgraded to "weak-model enablement" after compression failed on harder slices; transparent but a reviewer can call this reverse HARKing.

## 3. Engineering Quality (Task 2 auxiliary)

Detailed report: `2026-06-engineering-quality-audit.md`. Grade: **B**.

Healthy:
- 52 unit tests pass.
- Stage B v5.4 reproduction chain runnable end-to-end; reproduced `bounded_stability_confirmed` matches frozen record with zero metric diff.
- Evidence ledger 188 entries, structurally consistent, IDs unique.
- All V4 PDFs and source packages listed in README exist.
- V3 -> V4 git history coherent.

Risks:
- README reproduction command fails as written (PYTHONPATH/cwd not documented).
- 28 source_ids used in the ledger are missing from `source-index.md`.
- Statistical thresholds hard-coded across multiple scripts; no machine-readable experiment spec.
- No `requirements.txt` / `pyproject.toml`.
- `02_notes/` and `qa/` remain in template state.
- Backlog retains WIP items despite V4 freeze.

## 4. Prioritized Action List

Ordered by leverage-to-effort ratio. Items 1-3 are wording-only or index-only; item 4+ is engineering.

1. **W2 wording fix** (Section 4.8 and 5.1). Two sentences acknowledging the structural power limit. Converts the sharpest reviewer attack into an author-declared boundary. Zero additional runs.
2. **LangChain citation** in Abstract / Intro / Related Work. Three short additions. Eliminates the first-mover-advantage risk.
3. **Self-evaluation language trim**. Remove "strongest evidence", "main methodological contribution", "practical value is", "important qualification", or rephrase as factual claims about what the data shows.
4. **Backfill source-index.md** with the 28 missing Stage B source IDs.
5. **Fix README reproduction command** (PYTHONPATH/cwd).
6. **Centralize thresholds** into a YAML/TOML experiment spec.
7. **Add environment declaration** (`pyproject.toml` or README section).
8. **Replace `qa/` templates** with actual V4 review records; close or move WIP backlog items.
9. **Optional, larger investment**: a second fixture family or a second provider, to lift the Evaluation dimension from 3 to 5+. This is the only path to a main-track accept.

## 5. What This Audit Did Not Do

- Did not re-run any provider calls (no API key, no cost spend).
- Did not modify the paper body or any code.
- Did not attempt a literature scan beyond LangChain, DSPy, Outlines, Guardrails, MCP, PEtFiSh (already in related work). A full related-work freshness audit for 2026 publications is out of scope but recommended before external submission.
- Did not convert Appendix C evidence IDs to formal inline citations; that remains the known pre-submission formatting task from the prior citation audit.

## 6. Bottom Line

The V4 paper is internally honest and the engineering is real, but the paper has one structural statistical-design flaw (W2) that the internal review missed, and one external communication risk (LangChain) that the paper does not yet address. Both are fixable with wording changes alone. The evaluation dimension (single fixture, single model, single provider, author-as-evaluator) is the genuine ceiling on venue outcome and cannot be lifted without new experimental work.
