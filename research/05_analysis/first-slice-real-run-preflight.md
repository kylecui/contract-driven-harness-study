# Real Model Pilot Preflight

- Status: WARN
- Network/API calls made: no
- Manifest: `research\05_analysis\real-run-artifacts\first-slice-manifest-with-prompts.json`
- Config: `research\04_methods\provider-config.example.json`
- Runs: 24

## Provider Readiness

| Provider | Key env | Key present | Base URL |
|---|---|---:|---|
| `openai` | `OPENAI_API_KEY` | no | `https://api.openai.com/v1` |

## Model Tiers

| Tier | Provider | Model |
|---|---|---|
| `strong_model` | `openai` | `gpt-5.1` |
| `budget_model` | `openai` | `gpt-5.1-mini` |

## Validation Status

- pending: 24

## Run Groups

| Fixture / Model / Arm | Runs |
|---|---:|
| `project-initialization | budget_model | G0` | 3 |
| `project-initialization | budget_model | G9` | 3 |
| `project-initialization | strong_model | G0` | 3 |
| `project-initialization | strong_model | G9` | 3 |
| `structured-extraction | budget_model | G0` | 3 |
| `structured-extraction | budget_model | G9` | 3 |
| `structured-extraction | strong_model | G0` | 3 |
| `structured-extraction | strong_model | G9` | 3 |

## Errors

- None

## Warnings

- config filename looks like an example; confirm model IDs before execution
- environment variable not set: OPENAI_API_KEY

## Execution Gate

The artifact queue is structurally ready. Real execution still requires explicit approval, confirmed model IDs, API credentials, and budget.
