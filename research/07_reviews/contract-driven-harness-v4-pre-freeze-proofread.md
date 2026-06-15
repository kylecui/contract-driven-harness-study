# Contract-Driven Harness v4 Pre-Freeze Proofread

Reviewed: 2026-06-15

Result: **PASS**

## Corrections Applied

1. McNemar results are reported as `p=0.500` in human-facing artifacts.
2. Table 4 reports `40` in the Stage B v5.4 Runs column.
3. Methods defines the `0.20` gate as an absolute risk difference fixed
   before execution. With 15 runs per arm, it requires at least three
   additional passes.
4. The paper states that this cutoff is an engineering decision gate, not a
   significance threshold, equivalence margin, or power-derived minimum
   detectable effect. The original preregistration did not provide a separate
   utility analysis.
5. Discussion states that two discordant pairs provide little power for small
   effects and establish neither equivalence nor absence of a modest benefit.

## Scope Decision

No further structural revision is required for the arXiv evidence draft.
Venue-length adaptation remains deferred until a target venue is selected.
The venue pass should retain the matched-pair result and 40-run condition
table in the main paper, while considering the detailed Stage B audit trail,
most artifact IDs, and most of Appendix C for supplementary placement.

## Freeze Recommendation

The regenerated 23-page PDF passed compile and sampled-page layout checks with
zero LaTeX errors and zero unresolved citations or references. All 52 method
tests passed. The paper's 60 evidence references, 25 project source
references, and 22 external citation keys resolve without gaps. The V3.1.1
frozen hashes remain unchanged, and the public-tree scan found no credential
or private-path leak.

The V4 body is ready to freeze.
