# Real Model Pilot Preflight

- Status: PASS
- Network/API calls made: no
- Manifest: `research\05_analysis\real-run-artifacts\mechanism-atoms-first-batch-manifest-with-prompts.json`
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
| `a1-schema-bound-extraction | budget_model | G0` | 1 |
| `a1-schema-bound-extraction | budget_model | G2` | 1 |
| `a1-schema-bound-extraction | budget_model | G8` | 1 |
| `a1-schema-bound-extraction | budget_model | G9` | 1 |
| `a1-schema-bound-extraction | strong_model | G0` | 1 |
| `a1-schema-bound-extraction | strong_model | G2` | 1 |
| `a1-schema-bound-extraction | strong_model | G8` | 1 |
| `a1-schema-bound-extraction | strong_model | G9` | 1 |
| `a3-constraint-safe-planning | budget_model | G0` | 1 |
| `a3-constraint-safe-planning | budget_model | G2` | 1 |
| `a3-constraint-safe-planning | budget_model | G8` | 1 |
| `a3-constraint-safe-planning | budget_model | G9` | 1 |
| `a3-constraint-safe-planning | strong_model | G0` | 1 |
| `a3-constraint-safe-planning | strong_model | G2` | 1 |
| `a3-constraint-safe-planning | strong_model | G8` | 1 |
| `a3-constraint-safe-planning | strong_model | G9` | 1 |
| `a4-state-inventory | budget_model | G0` | 1 |
| `a4-state-inventory | budget_model | G2` | 1 |
| `a4-state-inventory | budget_model | G8` | 1 |
| `a4-state-inventory | budget_model | G9` | 1 |
| `a4-state-inventory | strong_model | G0` | 1 |
| `a4-state-inventory | strong_model | G2` | 1 |
| `a4-state-inventory | strong_model | G8` | 1 |
| `a4-state-inventory | strong_model | G9` | 1 |
| `a6-validator-repair | budget_model | G0` | 1 |
| `a6-validator-repair | budget_model | G2` | 1 |
| `a6-validator-repair | budget_model | G8` | 1 |
| `a6-validator-repair | budget_model | G9` | 1 |
| `a6-validator-repair | strong_model | G0` | 1 |
| `a6-validator-repair | strong_model | G2` | 1 |
| `a6-validator-repair | strong_model | G8` | 1 |
| `a6-validator-repair | strong_model | G9` | 1 |
| `a8-evidence-type-separation | budget_model | G0` | 1 |
| `a8-evidence-type-separation | budget_model | G2` | 1 |
| `a8-evidence-type-separation | budget_model | G8` | 1 |
| `a8-evidence-type-separation | budget_model | G9` | 1 |
| `a8-evidence-type-separation | strong_model | G0` | 1 |
| `a8-evidence-type-separation | strong_model | G2` | 1 |
| `a8-evidence-type-separation | strong_model | G8` | 1 |
| `a8-evidence-type-separation | strong_model | G9` | 1 |

## Errors

- None

## Warnings

- None

## Execution Gate

The artifact queue is structurally ready. Real execution still requires explicit approval, confirmed model IDs, API credentials, and budget.
