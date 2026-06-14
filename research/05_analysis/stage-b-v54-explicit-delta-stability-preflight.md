# Real Model Pilot Preflight

- Status: PASS
- Network/API calls made: no
- Manifest: `research\05_analysis\real-run-artifacts\stage-b-v54-explicit-delta-stability-manifest-with-prompts.json`
- Config: `research\04_methods\provider-config.siliconflow-reviewed.json`
- Runs: 40

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

- pending: 40

## Run Groups

| Fixture / Model / Arm | Runs |
|---|---:|
| `stage-b-v53-p2--canonical | budget_model | G9` | 8 |
| `stage-b-v53-p2--distractor-evidence | budget_model | G9` | 8 |
| `stage-b-v53-p2--evidence-order-shuffled | budget_model | G9` | 8 |
| `stage-b-v53-p2--field-alias | budget_model | G9` | 8 |
| `stage-b-v53-p2--unknown-state-paraphrase | budget_model | G9` | 8 |

## Errors

- None

## Warnings

- None

## Execution Gate

The artifact queue is structurally ready. Real execution still requires explicit approval, confirmed model IDs, API credentials, and budget.
