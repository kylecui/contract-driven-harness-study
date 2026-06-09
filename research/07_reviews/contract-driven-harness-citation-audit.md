# Citation Audit: Contract-Driven Harness Paper Draft

Document audited: `research/06_outputs/contract-driven-harness-paper-draft.md`

Audit date: 2026-06-09

Audit basis:

- `research/03_evidence/evidence-ledger.jsonl`
- `research/01_sources/source-index.md`
- `research/06_outputs/contract-driven-harness-claim-evaluation-map.md`
- `research/06_outputs/contract-driven-harness-paper-draft.md`

## Verdict

**CONDITIONAL PASS for internal research use.**

The central empirical claims are traceable to evidence IDs and source IDs after adding Appendix C to the paper draft and supplementing the source index with missing related-work sources. No critical claim currently needs to be removed.

The draft is **not yet publication-ready** because formal inline citations, exact source locators, and full bibliography entries have not been inserted. This is a formatting and traceability-depth gap, not a current contradiction in the evidence chain.

## Coverage Summary

| Claim class | Count audited | Complete chain | Needs formal citation work | Blocking unsupported |
|---|---:|---:|---:|---:|
| Class A: central empirical/method claims | 10 | 10 | 10 | 0 |
| Class B: related-work positioning claims | 7 | 7 | 7 | 0 |
| Class C: descriptive/background claims | 4 | 4 | 2 | 0 |

Minimum chain status:

```text
claim -> evidence_id -> source_id -> accessible local path or URL
```

Result: present for all audited Class A and Class B claims.

## Critical Claim Audit

| Claim | Evidence IDs | Source IDs | Audit result |
|---|---|---|---|
| Harnessing improves absolute contract adherence and can compress gaps only under constrained conditions. | P2-E28, P2-E30, P2-E32, P2-E33 | P2-SILICONFLOW-V2-FULL24, P2-SILICONFLOW-PROJECT-INIT-12, P2-SILICONFLOW-RESEARCH-WORKFLOW-12, P2-CLAIM-BOUNDARY-MEMO | Supported. Wording is appropriately conditional. |
| Structured extraction is the strongest positive gap-compression slice. | P2-E27, P2-E28 | P2-SILICONFLOW-V2-FULL24 | Supported for the tested SiliconFlow v2 slice. |
| Project initialization and research workflow do not support universal gap compression. | P2-E30, P2-E32, P2-E33 | P2-SILICONFLOW-PROJECT-INIT-12, P2-SILICONFLOW-RESEARCH-WORKFLOW-12, P2-CLAIM-BOUNDARY-MEMO | Supported. The draft correctly uses mixed/undefined framing. |
| Mechanism atoms make broad workflow failures interpretable. | P2-E35, P2-E36, P2-E56, P2-E60 | P2-MECHANISM-ATOM-DEFINITION, P2-MECHANISM-ATOM-COVERAGE, P2-STAGE7R-REVISED-ATOMS, P2-STAGE7R1-A2R-A7R-SMOKE | Supported as methodology plus targeted empirical repair evidence. |
| Atom success does not automatically imply macro success. | P2-E51, P2-E52 | P2-STAGE7P-PARTIAL-COMPOSITION | Supported by Stage 7p v1. |
| Explicit carried obligations repair the Stage 7p composition failure. | P2-E53, P2-E54 | P2-STAGE7P-V2-COMPOSITION-RETENTION | Supported for the A10 -> A9 -> A6 partial macro only. |
| Stage 7r.1 repaired low-cost-model A2R/A7R failures. | P2-E57, P2-E58, P2-E59, P2-E60 | P2-STAGE7R1-A2R-A7R-PREP, P2-STAGE7R1-A2R-A7R-SMOKE | Supported for targeted atoms only. |
| Stage 7e v1-v4 demonstrates the repair-loop protocol. | P2-E62, P2-E64, P2-E66, P2-E68, P2-E69, P2-E70 | P2-STAGE7E-EVIDENCE-DECISION, P2-STAGE7E-V2-RETENTION, P2-STAGE7E-V3-STATE-RETENTION, P2-STAGE7E-V4-KNOWN-STATE-PROVENANCE, P2-CLAIM-BOUNDARY-MEMO | Supported with fixed-input/no-tool boundary. |
| Stage 7-next transfers Stage 7e v4 obligations to a neighboring method-plan macro. | P2-E72, P2-E74, P2-E75 | P2-STAGE7-NEXT-METHOD-PLAN-LOCAL, P2-STAGE7-NEXT-METHOD-PLAN-SMOKE | Supported as narrow transfer evidence. |
| Full project initialization, full research workflow, production readiness, and general model equivalence remain non-claims. | P2-E33, P2-E63, P2-E69, P2-E70, P2-E75 | P2-CLAIM-BOUNDARY-MEMO, P2-STAGE7E-EVIDENCE-DECISION, P2-STAGE7E-V4-KNOWN-STATE-PROVENANCE, P2-STAGE7-NEXT-METHOD-PLAN-SMOKE | Supported and explicitly stated. |

## Related-Work Audit

Related-work coverage was initially incomplete because the full draft mentioned several systems and papers that were present in the local survey but not independently registered in `source-index.md`. This has been remediated by adding source IDs and evidence IDs for:

- OpenAI Structured Outputs: P2-E83
- Outlines: P2-E84
- AutoGen: P2-E85
- Semantic Kernel: P2-E86
- RAG: P2-E87
- ReAct: P2-E88
- Toolformer: P2-E89
- Gorilla: P2-E90
- MemGPT: P2-E91
- Letta: P2-E92
- OAgents: P2-E93
- Semantic Integrity Constraints: P2-E94
- Agentproof: P2-E95
- LlamaFirewall: P2-E96

Remaining related-work risk: the paper draft still uses source/evidence traceability rather than formal inline citation syntax. This is acceptable for the internal draft but must be fixed before external submission.

## Statistical Claim Audit

The statistical claims in the paper are traceable to generated metrics artifacts, but several are currently reported in compressed prose rather than tables.

Non-blocking improvements before submission:

- Add a compact result table for each main slice.
- Include run matrix for each stage: model tier, arm, repetitions, completed runs.
- Mark provider timeout retries separately from model-quality failures.
- Keep `n/a` gap-compression cases explicit when baseline gaps are zero.

No current statistical claim was found to contradict the ledger.

## Source Accessibility

Local source paths in `source-index.md` are accessible from the workspace. External URLs were checked at source-discovery level using official documentation or paper pages. For publication, add:

- access dates;
- version or release-channel notes for mutable documentation;
- arXiv version numbers where relevant;
- exact section anchors or page locators.

## Required Remediation Before External Submission

1. Convert Appendix C evidence mappings into formal citations or footnotes in the paper body.
2. Add a bibliography or reference list with external sources.
3. Add exact locators for local generated artifacts, especially metrics reports and stage summaries.
4. Add compact tables for numerical claims.
5. Keep the current non-claims appendix; it is necessary for claim-boundary integrity.

## Decision

The paper draft can proceed to the next internal stage: evidence-aware revision and citation insertion.

It should not be submitted externally until formal citation formatting and locator-level source verification are complete.
