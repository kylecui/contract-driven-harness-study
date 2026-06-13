# SiliconFlow Pricing Snapshot

Retrieved: 2026-06-13 (Asia/Shanghai)

Scope: public list prices and model availability relevant to the post-freeze
experiment plan.

## Sources

- Pricing page: <https://siliconflow.cn/pricing>
- Chat Completions API:
  <https://docs.siliconflow.cn/cn/api-reference/chat-completions/chat-completions>
- Authenticated model-list endpoint:
  `GET https://api.siliconflow.cn/v1/models?type=text`

No API key, account identifier, balance, or raw authenticated response is
stored in this snapshot.

## Price Snapshot

Prices are in CNY per one million tokens.

| Model | Input | Output | Cache | Intended use |
|---|---:|---:|---:|---|
| `Qwen/Qwen3-8B` | ¥0.00 | ¥0.00 | Not stated | Stage B and Stage C low-cost-model runs |
| `deepseek-ai/DeepSeek-V3.2` | ¥2.00 | ¥3.00 | ¥0.20 | Later Stage D strong-model comparison |

The public pricing page's embedded model record listed
`Qwen/Qwen3-8B` prompt and completion prices as zero at retrieval time. The
model was also present in the authenticated text-model list. The rendered
pricing table directly listed the DeepSeek-V3.2 prices above.

## Stage B Cost Interpretation

Stage B uses only `Qwen/Qwen3-8B`. At the public list price recorded above,
the token charge for the planned 30 calls is ¥0.00.

This is a dated public-list-price observation, not a guarantee about future
pricing, account-specific billing, quotas, rate limits, availability, or
provider policy. A zero token price also does not imply zero latency,
engineering effort, retry cost, or opportunity cost.

## Recheck Rule

Recheck the official pricing page and authenticated model list immediately
before any later Stage C or Stage D execution. Record a new dated snapshot if
the model, price, or availability changes.
