# Smoke Pilot Workflow Summary

- Execute mode: yes
- Cost confirmed: yes
- Workflow status: failed
- Manifest: `research/05_analysis/real-run-artifacts/siliconflow-v2-full24-manifest-with-prompts.json`
- Config: `research/04_methods/provider-config.siliconflow-reviewed.json`

## Steps

| Step | Return Code | Output |
|---|---:|---|
| preflight | 0 | `research\05_analysis\siliconflow-v2-full24-execution-preflight.md` |
| adapter | 1 | `research\05_analysis\siliconflow-v2-full24-execution-adapter.json` |

## Decision

Adapter failed; postprocess was not run.
