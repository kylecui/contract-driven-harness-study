# Real Model Pilot Preflight

- Status: PASS
- Network/API calls made: no
- Manifest: `research\05_analysis\real-run-artifacts\smoke-v2-manifest-with-prompts.json`
- Config: `research\04_methods\provider-config.siliconflow-reviewed.json`
- Runs: 8

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

- pending: 8

## Run Groups

| Fixture / Model / Arm | Runs |
|---|---:|
| `structured-extraction | budget_model | G0` | 1 |
| `structured-extraction | budget_model | G9` | 1 |
| `structured-extraction | strong_model | G0` | 1 |
| `structured-extraction | strong_model | G9` | 1 |
| `structured-extraction-hard | budget_model | G0` | 1 |
| `structured-extraction-hard | budget_model | G9` | 1 |
| `structured-extraction-hard | strong_model | G0` | 1 |
| `structured-extraction-hard | strong_model | G9` | 1 |

## Errors

- None

## Warnings

- None

## Execution Gate

The artifact queue is structurally ready. Real execution still requires explicit approval, confirmed model IDs, API credentials, and budget.
