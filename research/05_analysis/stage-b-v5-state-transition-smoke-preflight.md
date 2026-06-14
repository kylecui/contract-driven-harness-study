# Real Model Pilot Preflight

- Status: PASS
- Network/API calls made: no
- Manifest: `research\05_analysis\real-run-artifacts\stage-b-v5-state-transition-smoke-manifest-with-prompts.json`
- Config: `research\04_methods\provider-config.siliconflow-reviewed.json`
- Runs: 4

## Provider Readiness

| Provider | Key env | Key present | Base URL |
|---|---|---:|---|
| `siliconflow` | `SILICONFLOW_API_KEY` | yes | `https://api.siliconflow.cn/v1` |

## Model Tiers

| Tier | Provider | Model |
|---|---|---|
| `strong_model` | `siliconflow` | `deepseek-ai/DeepSeek-V3.2` |
| `budget_model` | `siliconflow` | `Qwen/Qwen3-8B` |

## Validation Status

- pending: 4

## Run Groups

| Fixture / Model / Arm | Runs |
|---|---:|
| `stage-b-v5-state-transition--canonical | budget_model | G9` | 2 |
| `stage-b-v5-state-transition--dual-surface-stress | budget_model | G9` | 2 |

## Errors

- None

## Warnings

- None

## Execution Gate

The artifact queue is structurally ready. Real execution still requires explicit approval, confirmed model IDs, API credentials, and budget.
