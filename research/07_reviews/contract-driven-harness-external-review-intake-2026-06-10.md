# External Review Intake: Contract-Driven Harness Paper

Review file: `D:/Downloads/xwechat_files/kylecui_0b33/msg/file/2026-06/contract_driven_harness_analysis_report.md`

Intake date: 2026-06-10

Repository state at intake: `kylecui/contract-driven-harness-study` is public.

## Review Boundary

The external report evaluates the paper PDF, public repository artifacts, Companion Gateway follow-up context, and prior discussion. It does not claim to have locally rerun the repository scripts or reproduced the experiments.

The report's central judgment is that the work is credible as a bounded agent harness reliability paper, not as a proof of open-ended agent reliability or general low-cost-model equivalence.

## Main Accepted Findings

1. The strongest contribution is not inventing a harness, but turning agent reliability practices into a checkable methodology: contract stack, mechanism atoms, golden/known-bad fixtures, local gates, targeted smoke tests, repair loop, evidence ledger, and claim boundary.
2. The strongest empirical claim is weak-model enablement on bounded, contract-critical operations.
3. Gap compression remains conditional: strongest in structured extraction, mixed or undefined in project initialization and research workflow slices.
4. Stage 7e v1-v4 is valuable because it shows a repair loop, not because 4/4 runs establish broad reliability.
5. Stage 7-next supports narrow transfer to a neighboring fixed macro, not open-ended workflow readiness.
6. Public artifact availability strengthens the paper, but it creates a stricter need for security scanning, precise artifact locators, and public/private wording discipline.

## Accepted Revision Priorities

High-priority revisions:

- Sharpen the abstract around bounded contract-critical tasks, weak-model enablement, and repair-loop protocol.
- Introduce the distinction between model capability, harness specification, and workflow composition earlier in the paper.
- Add a related-work comparison table that states what adjacent systems externalize and what this paper adds.
- Add explicit atom-to-macro admission criteria in Methods.
- Move compact result summaries into the paper or formal appendix.
- Preserve and strengthen the non-claims appendix.
- Add public artifact availability wording and exact artifact locators.

Experiment priorities after paper revision:

- Run G9 object ablations: schema-only, evidence-only, trace-only, gate-only, and full contract.
- Build a fixture perturbation suite for Stage 7e and Stage 7-next.
- Design a controlled state-mutating macro before attempting full open-ended workflows.
- Add cross-provider replication only after the ablation and perturbation suites are defined.

## Current Decisions

- Do not expand immediately to full project initialization or full research workflow.
- Do not claim production readiness.
- Do not claim universal gap compression.
- Treat PEtFiSh as implementation context, not the paper's generalizable claim.
- Treat the public repository as an artifact package, while keeping "publication-ready" as a separate gate.

## Immediate Follow-Up

The first response to this review is a paper revision pass, not a new large experiment. The revision should update the arXiv working draft, source package, evidence ledger, source index, and backlog before any additional empirical slice.
