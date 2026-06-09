# Smoke Pilot Workflow Summary

- Execute mode: yes
- Cost confirmed: yes
- Workflow status: failed
- Manifest: `research/05_analysis/real-run-artifacts/siliconflow-project-init-12-manifest-with-prompts.json`
- Config: `research/04_methods/provider-config.siliconflow-reviewed.json`

## Steps

| Step | Return Code | Output |
|---|---:|---|
| preflight | 0 | `research\05_analysis\siliconflow-project-init-12-execution-preflight.md` |
| adapter | 0 | `research\05_analysis\siliconflow-project-init-12-execution-adapter.json` |
| postprocess | 120 | `research\05_analysis\siliconflow-project-init-12-execution-postprocess-summary.md` |

## Decision

Execution workflow completed; inspect postprocess outputs before updating evidence.
