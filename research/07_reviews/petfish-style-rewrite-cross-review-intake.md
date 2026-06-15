# PEtFiSh Style Rewrite Cross-Review Intake

Review date: 2026-06-12

External review file: external attachment supplied by the author; machine-local
path omitted from the public repository.

Target: `research/06_outputs/contract-driven-harness-arxiv-draft.md`

## Decision

The review is accepted as a precision-calibration pass, not as a replacement rewrite.

Its central judgment is sound: the current draft already has a credible author voice, while a small number of phrases still read like lecture notes, blog transitions, or automatic paper summaries. The revision therefore keeps the existing short sentences and direct claims, while applying only local changes that improve academic precision.

## Adopted

- Replace `selected low-cost-model failures` with wording tied to failures observed in low-cost-model runs.
- Replace `The method that follows` with `The resulting method`.
- Move Stage 7e/Stage 7-next evidence to the final Abstract paragraph.
- Replace `The useful question is smaller` with `The question studied here is smaller`.
- Replace `This gives us smaller questions` with `This yields smaller evaluation questions`.
- Replace the broad `remaining gap` claim with a paper-scoped mechanism-level gap.
- Replace `The working assumption is simple` with a conservative working assumption.
- Add the nonzero-baseline condition to the Results overview gap-compression claim.
- Replace `The implication is simple` with a direct implication statement.

## Adopted With Different Wording

The review proposed `specific low-cost-model failures`. The revision uses `failures observed in low-cost-model runs` because it ties the scope to the experiments and avoids a possible cherry-picking reading.

The review proposed `Our contribution is narrower but operational`. The revision uses `Our contribution is operationally different` because the comparison concerns the unit and repair protocol, not only contribution breadth.

## Not Adopted

- The Abstract opening remains `Many agent failures in productivity tasks...`; it is more precise than `Many failures in productivity agents...`.
- The Conclusion does not receive another non-claim sentence. The existing repair-loop ending is cleaner and avoids repeated defensive framing.
- `gives the clearest positive gap-compression result` is not changed merely to sound more formal; the current verb is clear.
- The review's numerical writing scores are treated as editorial judgments, not reproducible metrics.

## Boundary

This revision changes presentation and claim precision only. It does not add model runs, alter experimental results, or close the outstanding citation pass.
