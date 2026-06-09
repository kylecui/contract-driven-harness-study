# Brief: Topic-Aware Compaction

## Research Type

Scientific / engineering systems research.

## One-Line Goal

Evaluate whether topic-aware compaction changes LLM agent behavior in multi-topic sessions, reducing cost and latency without degrading recall.

## Core Research Question

Does structuring compaction by topic, rather than chronology, reduce redundant agent behavior such as repeated tool calls and exploratory context rebuilding?

## Working Thesis

The strongest thesis is not merely "topic summaries are shorter." The more publishable claim is:

> Topic-aware compaction acts as a behavioral control mechanism: by preserving topic boundaries at compaction time, it changes the agent trajectory and reduces API-call churn.

## Existing Local Evidence

- `proposal/01-Topic-Aware-Compaction/README.md` reports 20.3% token savings, 36.4% fewer API calls, 49.9% fewer cache reads, and zero measured recall loss.
- `proposal/01-Topic-Aware-Compaction/data/experiment-2-fishtrial-ab/ANALYSIS.md` gives the strongest current A/B result: same 21-message task, same 3 interleaved topics, same model, same 2 compactions, but fewer calls and lower wall time under fish-trail.
- `proposal/01-Topic-Aware-Compaction/data/experiment-1-sysprompt/REPORT.md` shows a separate mechanism: moving rule text into the cached system prompt can reduce compaction pressure compared with tiered rule reads.

## Scope

Included:

- Long-running coding-agent sessions.
- Multi-topic / topic-switching interactions.
- Compaction-time intervention, especially topic-structured summaries.
- Token, cache, API-call, wall-time, recall, and trajectory metrics.

Excluded:

- Claims about all LLM conversations.
- Claims that topic-aware compaction improves reasoning quality in general.
- Claims of model-independent effectiveness before cross-model replication.

## Recommended Next Experiments

1. Compression-only ablation: topic structure but fixed API-call count.
2. Behavioral-only ablation: fewer calls without topic structure.
3. Single-topic control: verify benefits vanish or shrink when topic switching is absent.
4. Topic-count scaling: 2, 3, 5, 7 interleaved topics.
5. Cross-model replication: at least one Claude, one OpenAI, one Gemini or local/budget model.

## Key Risks

- Current main result is single-model and small-N.
- Quality evaluation is recall-focused; it may miss subtler task-quality differences.
- OpenCode hook behavior may be platform-specific.
- "Behavioral change" needs trajectory-level evidence, not just aggregate token deltas.

