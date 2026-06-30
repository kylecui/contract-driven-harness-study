# v4.1 Draft Change Log

Generated: 2026-06-30
Branch: `review/2026-06-internal-audit`
Base: `research/06_outputs/contract-driven-harness-arxiv-v4-frozen.md`
Target: `research/06_outputs/contract-driven-harness-arxiv-v4-1-draft.md`

## Scope

This revision applies three classes of change identified during the 2026-06 internal audit and LangChain differentiation review:

1. W2 structural power admission (Section 4.8 and 5.1).
2. LangChain industrial-work framing and citation (Abstract, Section 1, Section 2.1, and `references.bib`).
3. Self-evaluation language trim at 10 locations.

No frozen file, PDF, `.py` script, data JSON, or frozen body file was modified.

---

## 1. Header line update

**Where:** First line after title in v4.1 draft.

**Before (v4 frozen):**

```text
Version 4 evidence-extension draft derived from the frozen v3.1.1 body. External literature citations use BibTeX keys; empirical evidence traceability is preserved in Appendix C and the reproducibility package.
```

**After (v4.1 draft):**

```text
Version 4.1 internal-audit revision draft (unfrozen; derived from v4 frozen at commit f01d658). External literature citations use BibTeX keys; empirical evidence traceability is preserved in Appendix C and the reproducibility package.
```

**Rationale:** Mark the new file as an unfrozen derivative and preserve freeze-policy traceability.

---

## 2. W2 structural power admission

### 2.1 New paragraph at end of Section 4.8 (after Stage B v5.4 result)

**Before:**

```text
It does not convert the mixed v5.3 ablation into a causal-effect result. It also does not establish arbitrary state-machine reliability, tool execution, rollback, concurrency, task-family generalization, or production readiness.

## 5. Discussion And Limitations
```

**After:**

```text
It does not convert the mixed v5.3 ablation into a causal-effect result. It also does not establish arbitrary state-machine reliability, tool execution, rollback, concurrency, task-family generalization, or production readiness.

A design-level caveat applies to the v5.3 paired comparison. With fifteen matched pairs and only two observed discordant pairs, the exact McNemar test has a structural two-sided floor of p=0.5; no effect of any size could have reached alpha=0.05 in this design. Similarly, the preregistered 0.20 absolute risk-difference threshold required at least three additional treatment passes over control; once the control arm achieved 13/15, the maximum achievable difference was capped at two passes regardless of treatment performance. The v5.3 design as preregistered therefore could not have produced a threshold-positive result at the observed control strength. The v5.4 stability question is independent of this power limit, but the v5.3 result should be read as design-blocked rather than as evidence of no effect.

## 5. Discussion And Limitations
```

### 2.2 Added sentence at end of Section 5.1

**Before:**

```text
The v5.4 result is therefore evidence of bounded absolute stability, not proof that explicit delta is universally necessary or sufficient.
```

**After:**

```text
The v5.4 result is therefore evidence of bounded absolute stability, not proof that explicit delta is universally necessary or sufficient. The v5.3 paired design was additionally underpowered in a structural sense: with at most two discordant pairs and a strong control baseline, neither the McNemar threshold nor the 0.20 engineering gate was reachable regardless of the treatment's true effect.
```

**Rationale:** Convert the W2 reviewer attack into an explicitly stated design boundary, using neutral engineering language rather than an apology.

---

## 3. LangChain framing and citation

### 3.1 New `references.bib` entry

**Where:** `research/06_outputs/contract-driven-harness-references.bib`, before `P2_LOCAL_ARTIFACTS`.

**Added:**

```bibtex
@misc{P2_EXT_LANGCHAIN_HARNESS,
  author       = {{LangChain}},
  title        = {Improving Deep Agents with Harness Engineering},
  year         = {2026},
  howpublished = {\url{https://www.langchain.com/blog/improving-deep-agents-with-harness-engineering}},
  note         = {Industrial blog post, published 2026-02-17; accessed 2026-06-30}
}
```

### 3.2 Abstract

**Before:**

```text
The evidence therefore supports bounded protocol stability and weak-model enablement, not a large independent causal effect, production readiness, or open-ended workflow reliability.
```

**After:**

```text
The evidence therefore supports bounded protocol stability and weak-model enablement, not a large independent causal effect, production readiness, or open-ended workflow reliability. Recent industrial work uses the same term for strong-model prompt/tool/middleware optimization on Terminal Bench \cite{P2_EXT_LANGCHAIN_HARNESS}; this paper studies a different problem---obligation externalization for low-cost-model bounded reliability.
```

### 3.3 Introduction (Section 1)

**Before:**

```text
The current evidence covers harness specification and bounded composition. It does not cover open-ended workflow autonomy.
```

**After:**

```text
The current evidence covers harness specification and bounded composition. It does not cover open-ended workflow autonomy. Concurrent industrial practice uses the term harness engineering for prompt, tool, and middleware optimization around a strong frontier model \cite{P2_EXT_LANGCHAIN_HARNESS}; we use it in a narrower, contract-driven sense targeted at bounded reliability for low-cost models.
```

### 3.4 Section 2.1 (Agent Workflows And Orchestration)

**Before:**

```text
Contract-driven harness engineering overlaps with workflow orchestration but treats the graph as only one layer. The unit of interest is the obligation that must survive the graph: state inventory, evidence binding, evidence type separation, trace completeness, stage-gate retention, excluded-context preservation, and repairability.

### 2.2 Declarative LM Programs And Agent Specifications
```

**After:**

```text
Contract-driven harness engineering overlaps with workflow orchestration but treats the graph as only one layer. The unit of interest is the obligation that must survive the graph: state inventory, evidence binding, evidence type separation, trace completeness, stage-gate retention, excluded-context preservation, and repairability.

Adjacent industrial practice. LangChain's harness-engineering account \cite{P2_EXT_LANGCHAIN_HARNESS} optimizes a strong coding agent on Terminal Bench 2.0 by tuning system prompts, tools, and middleware hooks; it does not externalize obligations as contract objects, does not use known-bad fixtures, and does not target low-cost-model enablement. Their result and ours are therefore incommensurable rather than conflicting: theirs is benchmark-rank movement on a frontier model; ours is bounded contract-adherence stability on a low-cost model.

### 2.2 Declarative LM Programs And Agent Specifications
```

**Rationale:** Frame LangChain as adjacent industrial work without denigrating it; prevent readers from conflating strong-model benchmark tuning with low-cost-model contract-driven reliability.

---

## 4. Self-evaluation language trim

### 4.1 L30 (Abstract)

**Before:**

```text
The strongest evidence in this study comes from the repair loop created after broad workflow tests exposed unstable behavior.
```

**After:**

```text
The repair loop created after broad workflow tests exposed unstable behavior produced the most interpretable evidence in this study.
```

### 4.2 L187 (Section 3.6)

**Before:**

```text
The main methodological contribution is the repair-loop protocol:
```

**After:**

```text
The repair-loop protocol is the primary methodological proposal:
```

### 4.3 L233 (Section 4.1)

**Before:**

```text
The results support a bounded version of the original hypothesis.
```

**After:**

```text
The results are consistent with a bounded version of the original hypothesis.
```

### 4.4 L262 (Section 4.2)

**Before:**

```text
The structured-extraction v2 slice provides the clearest positive gap-compression result.
```

**After:**

```text
The structured-extraction v2 slice is the only task slice with positive gap compression on all nonzero-baseline metrics.
```

### 4.5 L274 (Section 4.3)

**Before:**

```text
The harnessed low-cost model also outperformed the unconstrained strong model on contract-critical metrics.
```

**After:**

```text
The harnessed low-cost model scored higher than the unharnessed strong model on contract-critical metrics; this comparison conflates harness strength with model strength and is reported as such.
```

### 4.6 L298 (Section 4.5)

**Before:**

```text
This supports the mechanism-first repair hypothesis:
```

**After:**

```text
This is consistent with the mechanism-first repair hypothesis:
```

### 4.7 L326 (Section 4.7)

**Before:**

```text
This supports a narrow transfer claim:
```

**After:**

```text
This is consistent with a narrow transfer claim:
```

### 4.8 L371 (Section 5.1)

**Before:**

```text
Stage B adds an important qualification.
```

**After:**

```text
Stage B adds a structural qualification.
```

### 4.9 L375 (Section 5.2)

**Before:**

```text
The original research motivation was model capability gap compression. The results support that idea in structured settings, but not as a general law.
```

**After:**

```text
The original research motivation was model capability gap compression. The results are consistent with that idea in structured settings, but not as a general law.
```

### 4.10 L429 (Section 6)

**Before:**

```text
The practical value is the repair loop.
```

**After:**

```text
The operational artifact is the repair loop.
```

**Rationale:** Remove authorial verdicts on own evidence and replace them with factual statements, consistent with the internal audit's presentation critique.

---

## 5. Files changed and untouched

### Created

- `research/06_outputs/contract-driven-harness-arxiv-v4-1-draft.md`
- `research/07_reviews/2026-06-v4-1-draft-change-log.md`

### Modified

- `research/06_outputs/contract-driven-harness-references.bib` (added `P2_EXT_LANGCHAIN_HARNESS` entry)

### Explicitly not modified

- `research/06_outputs/contract-driven-harness-arxiv-v4-frozen.md`
- `research/06_outputs/contract-driven-harness-paper-v4-frozen.pdf`
- `research/07_reviews/contract-driven-harness-v4-body-freeze.md`
- No `.py` scripts were modified.
- No data JSON files were modified.
