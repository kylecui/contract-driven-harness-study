# Stage B Model And Reasoning Settings

Decided: 2026-06-13

Status: frozen before paid Stage B execution

## Decision

Stage B uses exactly one provider model:

```text
Qwen/Qwen3-8B
```

All 30 runs use:

- provider: SiliconFlow;
- model tier: low-cost model;
- harness arm: G9;
- `temperature`: 0;
- `max_tokens`: 2000;
- `enable_thinking`: false;
- `reasoning_effort`: not sent;
- `thinking_budget`: not sent.

The two macros and five representation conditions are experimental variables.
The model and inference mode are controlled variables.

## Why Stage B Is Single-Model

Stage B asks whether the admitted G9 macros survive representation-preserving
perturbations when executed repeatedly by the low-cost model. Adding another
model would mix model comparison with perturbation robustness and weaken the
cell-level diagnosis.

The strong-model comparison remains in Stage D, whose planned 2x2 matrix uses
`Qwen/Qwen3-8B` and `deepseek-ai/DeepSeek-V3.2` under G0 and G9.

## Why Thinking Is Disabled

SiliconFlow exposes `enable_thinking` for Qwen3-8B. It can change latency,
completion-token use, truncation risk, and possibly contract adherence, so it
cannot remain an implicit provider default.

Stage B fixes it to `false` because:

1. the primary question is contract robustness, not reasoning-mode quality;
2. the outputs are long structured artifacts with a 2000-token completion
   limit;
3. hidden reasoning can consume completion budget and make timeout or
   truncation a competing explanation;
4. non-thinking mode is cheaper in runtime terms and easier to audit.

This setting defines the Stage B protocol. It does not establish that
non-thinking mode is universally better.

Earlier Stage 7 adapter requests did not explicitly send `enable_thinking`.
Their provider-default inference mode is therefore not fully auditable from
the stored request artifacts. Stage B is a newly frozen protocol, not an exact
inference-mode replication of those historical runs.

## Meaning Of High, Medium, Low, Max, And Xhigh

These labels are not generic Qwen3-8B variants in SiliconFlow's documented
OpenAI-compatible API. The `reasoning_effort` field currently applies only to
`deepseek-ai/DeepSeek-V4-Flash`. Its documented options are `high` and `max`;
compatibility inputs `low` and `medium` map to `high`, while `xhigh` maps to
`max`.

Therefore Stage B must not send `reasoning_effort` to Qwen3-8B.

## Future Ablation

If Stage B passes, a separate paired ablation may compare Qwen3-8B with
`enable_thinking=false` and `enable_thinking=true` under otherwise identical
conditions. Those runs must be reported separately and must not be pooled into
the Stage B perturbation estimate.
