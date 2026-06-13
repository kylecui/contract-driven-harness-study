# Real Model Pilot Preflight

- Status: PASS
- Network/API calls made: no
- Manifest: `research\05_analysis\real-run-artifacts\post-freeze-perturbation-pilot-v2-manifest-with-prompts.json`
- Config: `research\04_methods\provider-config.siliconflow-stage-b-v2.json`
- Runs: 30

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

- pending: 30

## Run Groups

| Fixture / Model / Arm | Runs |
|---|---:|
| `stage7-next-method-plan-update-v2--canonical | budget_model | G9` | 3 |
| `stage7-next-method-plan-update-v2--distractor-evidence | budget_model | G9` | 3 |
| `stage7-next-method-plan-update-v2--evidence-order-shuffled | budget_model | G9` | 3 |
| `stage7-next-method-plan-update-v2--field-alias | budget_model | G9` | 3 |
| `stage7-next-method-plan-update-v2--unknown-state-paraphrase | budget_model | G9` | 3 |
| `stage7e-v4-known-state-provenance-decision-v2--canonical | budget_model | G9` | 3 |
| `stage7e-v4-known-state-provenance-decision-v2--distractor-evidence | budget_model | G9` | 3 |
| `stage7e-v4-known-state-provenance-decision-v2--evidence-order-shuffled | budget_model | G9` | 3 |
| `stage7e-v4-known-state-provenance-decision-v2--field-alias | budget_model | G9` | 3 |
| `stage7e-v4-known-state-provenance-decision-v2--unknown-state-paraphrase | budget_model | G9` | 3 |

## Errors

- None

## Warnings

- None

## Execution Gate

The artifact queue is structurally ready. Real execution still requires explicit approval, confirmed model IDs, API credentials, and budget.
