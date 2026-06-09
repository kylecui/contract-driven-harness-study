# Unsupported Claims Review: Contract-Driven Harness Paper Draft

Document audited: `research/06_outputs/contract-driven-harness-paper-draft.md`

Audit date: 2026-06-09

## Blocking Unsupported Claims

None found after source-index and evidence-ledger remediation.

## Non-Blocking Risk Claims

| Claim or phrase | Risk | Recommended action |
|---|---|---|
| "The strongest evidence in this study..." | Supported internally, but qualitative strength language should be tied to Stage 7e/Stage 7-next metrics. | Keep only with Appendix C mapping; add inline evidence citation before submission. |
| "These systems solve an important class of production problems..." | Broad related-work interpretation. | Downgrade to "These systems address..." or cite exact framework capabilities. |
| "models can become more capable when knowledge and action are externalized" | Broad synthesis across RAG/ReAct/Toolformer/Gorilla. | Keep as related-work synthesis; avoid implying current experiments tested live retrieval/tools. |
| "Semantic Kernel... observability..." | Product capability claim tied to mutable docs. | Add access date and docs locator before external submission. |
| "Letta... persistent memory, messages, tools, runs, and steps" | Product capability claim tied to mutable docs. | Add access date and docs locator before external submission. |
| Numeric improvements in Results section | Supported, but prose-only reporting is harder to audit. | Add tables with run counts, arms, model tiers, and source artifact IDs. |

## Claims That Must Not Be Added Without New Evidence

- The harness is production ready.
- Low-cost models are generally equivalent to strong models.
- Harnessing universally closes model gaps.
- Full project initialization is solved.
- Full research workflow is solved.
- Stage 7e or Stage 7-next proves open-ended tool-using workflow reliability.
- PEtFiSh-specific results generalize to all agent systems.

## Status

No deletion is required. The next revision should insert formal citations and slightly downgrade broad related-work language where exact framework evidence is not the point of the paper.
