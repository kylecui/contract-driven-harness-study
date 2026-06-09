# Real Model Pilot Preflight

- Status: PASS
- Network/API calls made: no
- Manifest: `research\05_analysis\real-run-artifacts\siliconflow-v2-full24-manifest-with-prompts.json`
- Config: `research\04_methods\provider-config.siliconflow-reviewed.json`
- Runs: 24

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

- pending: 24

## Run Groups

| Fixture / Model / Arm | Runs |
|---|---:|
| `structured-extraction | budget_model | G0` | 3 |
| `structured-extraction | budget_model | G9` | 3 |
| `structured-extraction | strong_model | G0` | 3 |
| `structured-extraction | strong_model | G9` | 3 |
| `structured-extraction-hard | budget_model | G0` | 3 |
| `structured-extraction-hard | budget_model | G9` | 3 |
| `structured-extraction-hard | strong_model | G0` | 3 |
| `structured-extraction-hard | strong_model | G9` | 3 |

## Errors

- None

## Warnings

- None

## Execution Gate

The artifact queue is structurally ready. Real execution still requires explicit approval, confirmed model IDs, API credentials, and budget.
