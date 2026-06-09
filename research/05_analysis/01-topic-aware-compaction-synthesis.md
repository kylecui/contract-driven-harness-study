# Synthesis: Topic-Aware Compaction

## Bottom Line

This proposal is strong enough to develop into a systems paper, but the central claim should be narrowed and sharpened:

> Topic-aware compaction reduces cost primarily by altering agent trajectories in multi-topic sessions, not by achieving a higher text compression ratio.

The current evidence supports this as a plausible mechanism, especially because API calls drop from 140 to 89 while recall remains intact (`P1-E01`, `P1-E03`). The next step is not more prose. It is trajectory-level ablation.

## What Is Already Strong

The proposal has a clear operational phenomenon: multi-topic sessions make chronological compaction brittle because unrelated topics are flattened into one timeline. The fish-trail intervention preserves topic boundaries, which appears to reduce redundant context rebuilding. This is more interesting than ordinary prompt compression because it treats compaction as an active control surface.

The local A/B result is promising:

- Total tokens: 857,115 baseline vs. 683,522 plugin.
- API calls: 140 baseline vs. 89 plugin.
- Cache reads: 10,631,340 baseline vs. 5,330,527 plugin.
- Wall time: 2,938s baseline vs. 1,781s plugin.
- Recall: all three topic recall checks passed in both variants.

The best interpretation is that topic structure changes the agent's next-step choices (`P1-E03`).

## Literature Positioning

The related work should be organized into three buckets:

1. Passive prompt compression: LLMLingua and related methods compress text while trying to preserve semantic content (`P1-E05`).
2. Agent context optimization: ACON and SWE-Pruner optimize long-horizon or coding-agent contexts and show large token reductions under agent workloads (`P1-E06`, `P1-E07`).
3. Topic / tree-structured memory: Membox and Context-Agent argue that linear histories are a poor representation for topic-shifting dialogue (`P1-E08`, `P1-E09`).

The novelty claim should sit between buckets 2 and 3:

> Prior work compresses agent context or stores topic-contiguous memories; fish-trail intervenes at compaction time to restructure immediate working context, then measures downstream trajectory change.

Avoid claiming "first" too broadly unless a full literature search confirms it. A safer phrase is "we study compaction-time topic injection as a behavioral control mechanism."

## Main Weaknesses

The current design is underpowered statistically. N=21 messages and one model are good for discovery, not yet for a COLM/EMNLP-level causal claim.

The quality metric is too narrow. Recall checks show retained factual information, but they do not measure task correctness, patch quality, unnecessary tool calls by category, or whether the plugin suppresses useful exploration.

The hook is platform-specific. The paper should name this as a limitation and frame OpenCode as the experimental environment, not as a universal agent runtime.

## Recommended Experiments

1. Run the compression-only ablation to separate smaller summaries from trajectory change.
2. Run the behavioral-only ablation to see whether fewer calls without topic structure harms quality.
3. Add a single-topic control to confirm the mechanism is topic-switch specific.
4. Add topic-count scaling, because the thesis predicts larger effects as topic interleaving increases.
5. Add cross-model replication, because context structure may be model-sensitive.
6. Add trajectory labels: redundant file read, repeated env check, repeated git/status check, repeated schema lookup, useful tool call, failed tool call.

## Pilot Trajectory Screen

I added `research/04_methods/scripts/label_token_trajectory.py` and ran it against the existing `ab_test_results.json`. Because the JSON lacks full message and tool-call text, the output is only a token-trajectory screen.

The screen reports:

- Baseline: 140 API calls, average effective context 81,127.24.
- Plugin: 89 API calls, average effective context 66,366.03.
- `large_tool_or_state_rebuild` candidates: 17 baseline vs. 11 plugin (`P1-E10`).

This is directionally consistent with the behavioral-change thesis, but it is not enough to prove it. The next harness run should preserve full session messages so these candidate calls can be labeled semantically.

## Paper Shape

Recommended title:

**Topic-Aware Compaction as Behavioral Control for Multi-Topic LLM Agent Sessions**

Recommended contributions:

1. Define multi-topic compaction failure as a source of agent trajectory inefficiency.
2. Introduce topic-aware compaction through fish-trail.
3. Show lower token/call/cache/wall-time costs without recall loss in a controlled OpenCode setup.
4. Provide ablation evidence that behavioral trajectory change, not raw text compression, drives the gain.
