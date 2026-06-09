# Stage 4 Summary: Atom Evaluator Metrics

## Stage Objective

Add atom-level evaluator metrics, weak-model enablement metrics, and harnessed-weak-vs-unconstrained-strong comparison support before any model API execution.

## Result

Stage 4 is complete.

## Artifacts Created Or Updated

- `research/04_methods/scripts/evaluate_mechanism_atom_artifacts.py`
- `research/04_methods/scripts/postprocess_mechanism_atom_pilot.py`
- `research/04_methods/scripts/harness_benchmark_metrics.py`
- `research/04_methods/scripts/generate_mechanism_atom_specs.py`
- `research/04_methods/mechanism-atoms/a8-evidence-type-separation/evidence_bundle.json`
- `research/05_analysis/mechanism-atoms-first-batch-local-check.json`
- `research/05_analysis/mechanism-atoms-first-batch-local-check.md`

## Metrics Added

Atom-level evaluator metrics now include:

- `atom_primary_metric`
- `constraint_consistency`
- `state_accuracy`
- `evidence_type_accuracy`
- `stage_completion`
- `repair_success`
- `trace_completeness`
- `context_relevance`

The benchmark metrics summary now also reports:

- `weak_model_enablement_lift`
- `harnessed_weak_vs_strong_baseline`

These are reported alongside existing gap compression metrics.

## Local Golden / Known-Bad Check

Command:

```text
python research/04_methods/scripts/evaluate_mechanism_atom_artifacts.py --atoms-dir research/04_methods/mechanism-atoms --fixtures a1-schema-bound-extraction a3-constraint-safe-planning a4-state-inventory a8-evidence-type-separation a6-validator-repair --local-check --output-runs research/05_analysis/mechanism-atoms-first-batch-local-check.json --output-md research/05_analysis/mechanism-atoms-first-batch-local-check.md
```

Result:

- Cases evaluated: 10.
- Expectation failures: 0.
- Golden outputs passed.
- Known-bad outputs failed.

## Deviation Check

One important evaluator deviation was found and fixed before proceeding:

- A3 `Constraint-Safe Planning` initially failed overall, but its primary metric `constraint_consistency` was incorrectly scored as 1.0 for a known-bad output that put `overwrite AGENTS.md` in allowed actions.
- This was a real construct-validity issue because the primary mechanism metric did not capture the intended failure mode.
- The evaluator was corrected to inspect allowed and blocked action buckets.
- After the fix, A3 known-bad output reports `constraint_consistency=0.000` and fails as expected.

One fixture consistency issue was also fixed:

- A8 golden output cited `atom-a8-e03`, but the generated EvidenceBundle initially contained only e01/e02.
- `atom-a8-e03` was added to the A8 evidence bundle and to the generation script.

Both deviations were reasonable implementation issues, not evidence against the experiment plan.

## Validation Performed

Python compile checks:

```text
python -m py_compile research/04_methods/scripts/evaluate_mechanism_atom_artifacts.py
python -m py_compile research/04_methods/scripts/harness_benchmark_metrics.py
python -m py_compile research/04_methods/scripts/postprocess_mechanism_atom_pilot.py
```

Result:

- All passed.

## Decision

Proceed to Stage 5.

Stage 5 must run the local golden/bad validation as a formal gate and compile dry-run manifests before any provider/model execution.
