# Contract-Driven Harness Citation Metadata

Document scope: `research/06_outputs/contract-driven-harness-paper-draft.md`

Prepared on: 2026-06-09

Purpose: provide access dates, stable URLs, and local artifact locators for converting internal `[E:...]` and `[S:...]` citations into a target venue bibliography.

## Citation Style Status

The current paper draft uses internal citation tags:

- `[E:P2-E..]` for evidence-ledger entries.
- `[S:P2-...]` for source-index entries.

Target-venue formatting is not yet applied because no target venue or style has been selected. This metadata file is the venue-neutral citation base.

## External Sources

All external sources below were registered in `research/01_sources/source-index.md` and should be cited with access date `2026-06-09` for mutable documentation sources.

| Source ID | Type | Citation locator | Access/version note | Used for |
|---|---|---|---|---|
| P2-EXT-ANTHROPIC | Engineering post | https://www.anthropic.com/engineering/building-effective-agents | Accessed 2026-06-09 | Workflow vs agent distinction. |
| P2-EXT-LANGGRAPH | Official docs | https://docs.langchain.com/oss/python/langgraph | Accessed 2026-06-09; mutable docs | Durable execution, memory, HITL orchestration. |
| P2-EXT-DSPY | Paper | https://arxiv.org/abs/2310.03714 | arXiv abstract page; version should be checked before external submission | Declarative LM programs. |
| P2-EXT-AGENTSPEX | Paper | https://arxiv.org/abs/2604.13346 | arXiv abstract page; version should be checked before external submission | Explicit workflow specification and agent harness. |
| P2-EXT-AGENTSPEC | Paper | https://arxiv.org/abs/2510.04173 | arXiv abstract page; version should be checked before external submission | Portable declarative agent specification. |
| P2-EXT-GUARDRAILS | Official docs | https://guardrailsai.com/docs/concepts/validators/ | Accessed 2026-06-09; mutable docs | Validators and guardrails. |
| P2-EXT-OPENAI-STRUCTURED-OUTPUTS | Official docs | https://platform.openai.com/docs/guides/structured-outputs | Accessed 2026-06-09; mutable docs | Structured outputs and schema adherence. |
| P2-EXT-OUTLINES | Official docs | https://dottxt-ai.github.io/outlines/latest/ | Accessed 2026-06-09; mutable docs | Structured generation and constrained decoding. |
| P2-EXT-AUTOGEN | Official docs | https://microsoft.github.io/autogen/ | Accessed 2026-06-09; mutable docs | Multi-agent framework and orchestration. |
| P2-EXT-SEMANTIC-KERNEL | Official docs | https://learn.microsoft.com/en-us/semantic-kernel/ | Accessed 2026-06-09; mutable docs | Middleware, plugins, kernel, and function-calling workflows. |
| P2-EXT-RAG | Paper | https://arxiv.org/abs/2005.11401 | arXiv abstract page | Retrieval-augmented generation. |
| P2-EXT-REACT | Paper | https://arxiv.org/abs/2210.03629 | arXiv abstract page | Reasoning/action augmentation. |
| P2-EXT-TOOLFORMER | Paper | https://arxiv.org/abs/2302.04761 | arXiv abstract page | Tool/API use. |
| P2-EXT-GORILLA | Paper | https://arxiv.org/abs/2305.15334 | arXiv abstract page | API call generation. |
| P2-EXT-MEMGPT | Paper | https://arxiv.org/abs/2310.08560 | arXiv abstract page | Memory and virtual context management. |
| P2-EXT-LETTA | Official docs | https://docs.letta.com/guides/agents/overview/ | Accessed 2026-06-09; mutable docs | Stateful agents and persistent memory. |
| P2-EXT-OAGENTS | Paper | https://arxiv.org/abs/2506.15741 | arXiv abstract page; version should be checked before external submission | Agent evaluation variance and modular design. |
| P2-EXT-SIC | Paper | https://arxiv.org/abs/2503.00600 | arXiv abstract page | Semantic Integrity Constraints. |
| P2-EXT-AGENTPROOF | Paper | https://arxiv.org/abs/2603.20356 | arXiv abstract page; version should be checked before external submission | Static verification of agent workflows. |
| P2-EXT-LLAMAFIREWALL | Paper | https://arxiv.org/abs/2505.03574 | arXiv abstract page | Agent safety guardrails. |
| P2-EXT-SILICONFLOW-CHAT | Official docs | https://docs.siliconflow.cn/cn/api-reference/chat-completions/chat-completions and https://docs.siliconflow.cn/cn/userguide/models | Accessed 2026-06-09; mutable docs | Provider endpoint and model mapping. |

## Local Experiment And Method Sources

| Source ID | Primary local locator | Useful line/section locator | Used for |
|---|---|---|---|
| P2-SILICONFLOW-V2-FULL24 | `research/05_analysis/siliconflow-v2-full24-final-postprocess-metrics.md` | `:1` summary heading; `:7` G0 task_success row; `:14` G9 task_success row | Structured-extraction gap compression. |
| P2-SILICONFLOW-PROJECT-INIT-12 | `research/05_analysis/siliconflow-project-init-12-final-postprocess-metrics.md` | `:1` summary heading; `:7` G0 task_success row; `:14` G9 task_success row | Project-initialization mixed gap movement. |
| P2-SILICONFLOW-RESEARCH-WORKFLOW-12 | `research/05_analysis/siliconflow-research-workflow-12-execution-postprocess-metrics.md` | `:1` summary heading; `:7` G0 task_success row; `:14` G9 task_success row | Research-workflow mixed/undefined gap movement. |
| P2-STAGE6-PILOT48 | `research/05_analysis/stage-reports/stage-6-mechanism-atom-pilot48-summary.md` | `:48` completion; `:58` weak-model enablement; `:78` harnessed weak vs unconstrained strong; `:96` gap compression | Mechanism-atom pilot results. |
| P2-STAGE7P-PARTIAL-COMPOSITION | `research/05_analysis/stage7p-a10-a9-a6-evaluation.md` | `:1` evaluation summary; `:3` metric table header | Stage 7p v1 partial composition failure. |
| P2-STAGE7P-V2-COMPOSITION-RETENTION | `research/05_analysis/stage7p-v2-a10-a9-a6-evaluation.md` | `:1` evaluation summary; `:3` metric table header | Stage 7p v2 composition-retention repair. |
| P2-STAGE7R-REVISED-ATOMS | `research/05_analysis/stage-reports/stage-7r-revised-atoms-summary.md` | `:18` local gates; `:34` real smoke execution; `:53` results; `:66` atom-level interpretation; `:80` deviation review | Stage 7r boundary and timeout deviation. |
| P2-STAGE7R1-A2R-A7R-SMOKE | `research/05_analysis/stage7r1-a2r-a7r-targeted-evaluation.md` | `:1` evaluation summary | Stage 7r.1 targeted A2R1/A7R1 repair. |
| P2-STAGE7E-EVIDENCE-DECISION | `research/05_analysis/stage7e-evidence-bound-decision-evaluation-v3.md` | `:1` summary; `:5-10` run rows | Stage 7e v1 macro result and low-cost G9 miss. |
| P2-STAGE7E-V2-RETENTION | `research/05_analysis/stage7e-v2-retention-decision-evaluation.md` | `:1` summary; `:5-8` run rows | Stage 7e v2 trace/gate repair and remaining state omissions. |
| P2-STAGE7E-V3-STATE-RETENTION | `research/05_analysis/stage7e-v3-state-retention-decision-evaluation-v2.md` | `:1` summary; `:5-8` run rows | Stage 7e v3 unknown-state repair and one known-state provenance miss. |
| P2-STAGE7E-V4-KNOWN-STATE-PROVENANCE | `research/05_analysis/stage-reports/stage-7e-v4-known-state-provenance-summary.md` | `:57` execution; `:62-67` timeout/truncation/retry; `:83` results table; `:94-97` 4/4 pass summary; `:111` claim boundary | Stage 7e v4 final macro pass and runtime deviation. |
| P2-STAGE7-NEXT-METHOD-PLAN-LOCAL | `research/05_analysis/stage7-next-method-plan-update-local-check.md` | `:1` local-check summary | Stage 7-next local golden/bad validation. |
| P2-STAGE7-NEXT-METHOD-PLAN-SMOKE | `research/05_analysis/stage-reports/stage-7-next-method-plan-update-smoke-summary.md` | `:25` execution result; `:41` no retry; `:43` evaluation; `:67` interpretation; `:75` boundary; `:85` decision | Stage 7-next 4/4 transfer smoke. |
| P2-MECHANISM-ATOM-DEFINITION | `research/04_methods/mechanism-atom-definition.md` | Whole document; section headings should be converted to line anchors before external submission | Mechanism-atom definition. |
| P2-MECHANISM-ATOM-COVERAGE | `research/04_methods/mechanism-atom-coverage-framework.md` | Whole document; section headings should be converted to line anchors before external submission | Mechanism-atom coverage framework. |
| P2-CLAIM-BOUNDARY-MEMO | `research/05_analysis/contract-driven-claim-boundary-memo.md` | Whole document; section headings should be converted to line anchors before external submission | Claim boundaries and non-claims. |

## Evidence Ledger Coverage

The paper draft currently resolves:

- 60 distinct `[E:P2-E..]` evidence references.
- 40 distinct `[S:P2-...]` source references.

Last checked: 2026-06-09.

## Remaining Venue-Style Work

Before external submission:

1. Select target style, for example ACM numbered, IEEE numbered, APA author-year, or arXiv preprint style.
2. Convert `[S:...]` references to the target citation syntax.
3. Convert local artifact references into appendices, footnotes, or reproducibility-package references.
4. Add arXiv version numbers for preprints.
5. Add exact section anchors or line locators for method-definition documents currently marked as whole-document sources.
