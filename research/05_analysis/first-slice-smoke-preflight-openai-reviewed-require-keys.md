# Real Model Pilot Preflight

- Status: FAIL
- Network/API calls made: no
- Manifest: `research\05_analysis\real-run-artifacts\first-slice-smoke-manifest.json`
- Config: `research\04_methods\provider-config.openai-reviewed.json`
- Runs: 4

## Provider Readiness

| Provider | Key env | Key present | Base URL |
|---|---|---:|---|
| `openai` | `OPENAI_API_KEY` | no | `https://api.openai.com/v1` |

## Model Tiers

| Tier | Provider | Model |
|---|---|---|
| `strong_model` | `openai` | `gpt-5.1` |
| `budget_model` | `openai` | `gpt-5-mini` |

## Validation Status

- pending: 4

## Run Groups

| Fixture / Model / Arm | Runs |
|---|---:|
| `structured-extraction | budget_model | G0` | 1 |
| `structured-extraction | budget_model | G9` | 1 |
| `structured-extraction | strong_model | G0` | 1 |
| `structured-extraction | strong_model | G9` | 1 |

## Errors

- environment variable not set: OPENAI_API_KEY

## Warnings

- None

## Execution Gate

Do not run the adapter with `--execute` until errors are fixed.
