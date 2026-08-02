# Protocol: Topic-Aware Compaction Ablations

## Objective

Test whether topic-aware compaction saves tokens mainly by changing agent behavior, rather than by only shortening text.

## Current Baseline

Existing harness:

- `proposal/01-Topic-Aware-Compaction/scripts/ab_test_harness_v2.py`
- `proposal/01-Topic-Aware-Compaction/scripts/setup_ab_test.py`

Current task:

- 21 user messages.
- 3 interleaved topics: `python-setup`, `database`, `cicd`.
- 3 recall questions after the interaction.
- Baseline: chronological OpenCode compaction.
- Treatment: fish-trail topic-aware compaction.

## Experiment Arms

| Arm | Name | Purpose | Expected Result |
|---|---|---|---|
| A0 | Chronological baseline | Existing OpenCode compaction | Highest API-call churn |
| A1 | Topic-aware compaction | Existing fish-trail treatment | Lower calls/tokens, same recall |
| A2 | Compression-only | Topic-structured summary, but no behavioral freedom reduction | Smaller or weaker savings than A1 |
| A3 | Behavioral-only | Force fewer API calls without topic structure | Savings may appear, but quality should degrade |
| A4 | Single-topic control | Same length, one topic only | A1 advantage should shrink |
| A5 | Topic-count scaling | 2, 3, 5, 7 interleaved topics | A1 advantage should grow with topic count |

## Primary Metrics

- Total input tokens.
- Total output tokens.
- Total cache reads.
- API calls per user message.
- Wall time.
- Compaction count.
- Peak context window.
- Final context window.
- Recall success.

## Trajectory Labels

Add manual or scripted labels for tool/API-call reasons:

- `useful_progress`: call directly advances requested task.
- `state_rebuild`: call rereads files, schema, env, or history already available in topic state.
- `verification`: call checks prior work or validates generated output.
- `dead_end`: call produces no useful state.
- `error_recovery`: call follows timeout, tool error, or malformed output.
- `formatting_only`: call mostly changes presentation.

The paper's mechanism claim needs the `state_rebuild` rate to drop under topic-aware compaction.

## Quality Metrics

Recall-only quality is not enough. Add:

- Topic-specific factual recall.
- Task artifact completeness.
- Tool-call usefulness ratio.
- Unsupported claim count.
- Human reviewer preference, blind to condition.
- Regression against expected dependency/schema/pipeline facts.

## Minimum Replication Plan

Run each arm with:

- `n=5` repeated runs per arm.
- At least 2 models after mechanism is validated.
- Fixed conversation seed and fixed test workspace.
- Full raw session logs preserved.

## Acceptance Criteria

Topic-aware compaction supports the paper thesis if:

- A1 beats A0 on total tokens, cache reads, API calls, and wall time.
- A1 does not degrade recall or task completeness.
- A1 reduces `state_rebuild` calls materially.
- A2 does not explain most of A1's savings.
- A4 shows smaller gains than the multi-topic condition.

## Failure Interpretations

- If A1 saves tokens but `state_rebuild` does not drop, the mechanism is not behavioral change.
- If A1 only wins on one model, the claim must become model-specific.
- If A1 hurts task quality, the paper should frame this as cost/quality tradeoff rather than free savings.

