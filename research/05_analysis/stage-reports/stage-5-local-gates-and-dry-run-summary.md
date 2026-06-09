# Stage 5 Summary: Local Gates And Dry-Run Manifests

## Stage Objective

Run local golden/bad validation, validate fixture structure, prepare artifact directories, export prompts, and confirm pending outputs cannot enter metrics before model execution.

## Result

Stage 5 is complete.

## Local Gates

Generic fixture validation:

```text
python research/04_methods/scripts/validate_harness_fixtures.py --fixtures-dir research/04_methods/mechanism-atoms
```

Result:

- 10/10 mechanism atom fixtures passed.

Mechanism atom specification validation:

```text
python research/04_methods/scripts/validate_mechanism_atoms.py --atoms-dir research/04_methods/mechanism-atoms
```

Result:

- 10/10 mechanism atom fixtures passed.

First-batch golden/bad validation:

```text
python research/04_methods/scripts/evaluate_mechanism_atom_artifacts.py --atoms-dir research/04_methods/mechanism-atoms --fixtures a1-schema-bound-extraction a3-constraint-safe-planning a4-state-inventory a8-evidence-type-separation a6-validator-repair --local-check --output-runs research/05_analysis/mechanism-atoms-first-batch-stage5-local-check.json --output-md research/05_analysis/mechanism-atoms-first-batch-stage5-local-check.md
```

Result:

- 10 cases evaluated.
- 0 expectation failures.
- Golden outputs passed.
- Known-bad outputs failed.

## Dry-Run Manifest And Prompt Export

Artifact preparation:

```text
python research/04_methods/scripts/prepare_real_run_artifacts.py --packets-jsonl research/05_analysis/benchmark-mechanism-atoms-first-batch-packets.jsonl --runs-dir research/05_analysis/real-run-artifacts/mechanism-atoms-first-batch --output-manifest research/05_analysis/real-run-artifacts/mechanism-atoms-first-batch-manifest.json
```

Result:

- 40 run artifact directories prepared.

Prompt export:

```text
python research/04_methods/scripts/export_model_prompts.py --packets-jsonl research/05_analysis/benchmark-mechanism-atoms-first-batch-packets.jsonl --manifest research/05_analysis/real-run-artifacts/mechanism-atoms-first-batch-manifest.json --output-manifest research/05_analysis/real-run-artifacts/mechanism-atoms-first-batch-manifest-with-prompts.json
```

Result:

- Prompts and adapter request files exported for 40 runs.

Preflight:

```text
python research/04_methods/scripts/preflight_real_model_pilot.py --manifest research/05_analysis/real-run-artifacts/mechanism-atoms-first-batch-manifest-with-prompts.json --config research/04_methods/provider-config.siliconflow-reviewed.json --output-md research/05_analysis/mechanism-atoms-first-batch-preflight.md --output-json research/05_analysis/mechanism-atoms-first-batch-preflight.json
```

Result:

- Status: PASS.
- Errors: 0.
- Warnings: 0.
- Runs: 40.
- API key present: yes.
- Network/API calls made: no.

## Pending-Output Stop Check

Command:

```text
python research/04_methods/scripts/postprocess_mechanism_atom_pilot.py --manifest research/05_analysis/real-run-artifacts/mechanism-atoms-first-batch-manifest-with-prompts.json --atoms-dir research/04_methods/mechanism-atoms --output-prefix research/05_analysis/mechanism-atoms-first-batch-pending-postprocess
```

Result:

- Completed runs collected: 0.
- Collection warnings: 40.
- Metrics computed: no.

This is the expected stop behavior before model outputs exist.

## Deviation Check

Two implementation deviations occurred and were resolved:

1. `prepare_real_run_artifacts.py` initially expected `task_type` at packet top level. Full packets store it inside `task_spec.task_type`. The script was updated to support both packet shapes.
2. Preflight was first launched in parallel with prompt export, creating a race where the manifest did not yet exist. Preflight was rerun serially and passed.

Both deviations were pipeline-ordering or compatibility issues. They do not require revising the experiment plan.

## Decision

Proceed to Stage 6.

Stage 6 should create a formal mechanism-atom pilot matrix. The Stage 5 40-run dry manifest is not empirical model evidence and is not the final Stage 6 pilot.
