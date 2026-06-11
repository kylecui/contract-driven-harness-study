# Contract-Driven Harness Human Style Pass

Date: 2026-06-11

Target: `research/06_outputs/contract-driven-harness-arxiv-draft.md`

Skill: `petfish-style-rewriter`

Mode: strict academic rewrite

## Result

**PASS for a targeted human-style revision.**

The pass revised the arXiv-style working draft to reduce generic AI-like paper voice while preserving the empirical claims, claim boundaries, and citation structure.

## Problems Found

The pre-pass draft was already structurally sound, but several sections still read like a generated paper draft:

1. repeated self-description such as "this paper studies", "these results support", and defensive "not X but Y" boundary wording;
2. long abstract and introduction sentences that bundled several obligations into one line;
3. repeated claim-boundary language in Discussion and Conclusion;
4. formal-but-generic phrases such as "the strongest evidence", "important distinction", and "methodological assumption".

## Changes Made

- Rewrote the Abstract to use shorter sentences and a clearer problem statement.
- Reworked the Introduction to state the model/harness/workflow distinction in plainer terms.
- Reduced paper-self-reference in Related Work and Methods.
- Replaced several abstract method phrases with direct engineering language.
- Tightened Results and Discussion boundary wording without changing claim scope.
- Kept the metric-scope sentence that clarifies the metrics are not human preference scores.

## Style Check

The local `style_check.py` score stayed at **59/100** before and after the pass.

This score is not treated as a hard failure for this paper, for two reasons:

1. the checker flags `harness` as an English AI-high-frequency word, but `harness` is the technical term under study;
2. the long-sentence detector reports Markdown heading/title context and technical enumeration sentences that are acceptable in an academic abstract.

The actionable findings from the checker were addressed manually: long abstract sentences were split, self-describing paper voice was reduced, and generic AI-like phrasing was replaced with concrete claims.

## Boundary

This pass does not add new empirical evidence, change model-run results, or close the citation-normalization TODO. It is a presentation-quality revision for the current v3.1 working draft.

