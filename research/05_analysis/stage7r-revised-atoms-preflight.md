# Real Model Pilot Preflight

- Status: PASS
- Network/API calls made: no
- Manifest: `research\05_analysis\real-run-artifacts\stage7r-revised-atoms-manifest-with-prompts.json`
- Config: `research\04_methods\provider-config.siliconflow-reviewed.json`
- Runs: 36

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

- pending: 36

## Run Groups

| Fixture / Model / Arm | Runs |
|---|---:|
| `a2r-unsupported-claim-detection | budget_model | G0` | 1 |
| `a2r-unsupported-claim-detection | budget_model | G8` | 1 |
| `a2r-unsupported-claim-detection | budget_model | G9` | 1 |
| `a2r-unsupported-claim-detection | strong_model | G0` | 1 |
| `a2r-unsupported-claim-detection | strong_model | G8` | 1 |
| `a2r-unsupported-claim-detection | strong_model | G9` | 1 |
| `a3r-constraint-safe-plan | budget_model | G0` | 1 |
| `a3r-constraint-safe-plan | budget_model | G8` | 1 |
| `a3r-constraint-safe-plan | budget_model | G9` | 1 |
| `a3r-constraint-safe-plan | strong_model | G0` | 1 |
| `a3r-constraint-safe-plan | strong_model | G8` | 1 |
| `a3r-constraint-safe-plan | strong_model | G9` | 1 |
| `a4r-strict-state-inventory | budget_model | G0` | 1 |
| `a4r-strict-state-inventory | budget_model | G8` | 1 |
| `a4r-strict-state-inventory | budget_model | G9` | 1 |
| `a4r-strict-state-inventory | strong_model | G0` | 1 |
| `a4r-strict-state-inventory | strong_model | G8` | 1 |
| `a4r-strict-state-inventory | strong_model | G9` | 1 |
| `a5r-stage-gate-check | budget_model | G0` | 1 |
| `a5r-stage-gate-check | budget_model | G8` | 1 |
| `a5r-stage-gate-check | budget_model | G9` | 1 |
| `a5r-stage-gate-check | strong_model | G0` | 1 |
| `a5r-stage-gate-check | strong_model | G8` | 1 |
| `a5r-stage-gate-check | strong_model | G9` | 1 |
| `a7r-enumerated-claim-decision | budget_model | G0` | 1 |
| `a7r-enumerated-claim-decision | budget_model | G8` | 1 |
| `a7r-enumerated-claim-decision | budget_model | G9` | 1 |
| `a7r-enumerated-claim-decision | strong_model | G0` | 1 |
| `a7r-enumerated-claim-decision | strong_model | G8` | 1 |
| `a7r-enumerated-claim-decision | strong_model | G9` | 1 |
| `a8r-evidence-type-rules | budget_model | G0` | 1 |
| `a8r-evidence-type-rules | budget_model | G8` | 1 |
| `a8r-evidence-type-rules | budget_model | G9` | 1 |
| `a8r-evidence-type-rules | strong_model | G0` | 1 |
| `a8r-evidence-type-rules | strong_model | G8` | 1 |
| `a8r-evidence-type-rules | strong_model | G9` | 1 |

## Errors

- None

## Warnings

- None

## Execution Gate

The artifact queue is structurally ready. Real execution still requires explicit approval, confirmed model IDs, API credentials, and budget.
