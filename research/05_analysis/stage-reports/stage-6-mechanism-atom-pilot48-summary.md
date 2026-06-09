# Stage 6 Summary: Mechanism Atom Pilot 48

## Stage Objective

Run the first real mechanism-atom pilot after local gates passed.

The pilot tests whether mechanism arms improve budget-model reliability and whether cross-model gaps shrink on selected mechanism atoms.

## Result

Stage 6 first pilot is complete.

## Pilot Matrix

Formal matrix:

```text
2 models x 3 atoms x 4 arms x 2 repetitions = 48 runs
```

Models:

- `strong_model`: `deepseek-ai/DeepSeek-V3.2`
- `budget_model`: `Qwen/Qwen3-8B`

Atoms:

- A1 `a1-schema-bound-extraction`
- A3 `a3-constraint-safe-planning`
- A8 `a8-evidence-type-separation`

Arms:

- G0
- G2
- G8
- G9

## Execution Artifacts

- Matrix: `research/04_methods/benchmark-matrix-mechanism-atoms-pilot48.json`
- Packets: `research/05_analysis/benchmark-mechanism-atoms-pilot48-packets.jsonl`
- Manifest: `research/05_analysis/real-run-artifacts/mechanism-atoms-pilot48-manifest-with-prompts.json`
- Final postprocess summary: `research/05_analysis/mechanism-atoms-pilot48-final-postprocess-summary.md`
- Final collected runs: `research/05_analysis/mechanism-atoms-pilot48-final-postprocess-collected-runs.md`
- Final metrics: `research/05_analysis/mechanism-atoms-pilot48-final-postprocess-metrics.md`

## Completion

Final postprocess result:

- Completed runs: 48/48.
- Collection warnings: 0.
- Metrics computed: yes.

## Main Results

### Weak-Model Enablement

The strongest result is weak-model enablement.

Aggregate weak-model lift versus G0:

- G2 task_success: +0.521
- G8 task_success: +0.549
- G9 task_success: +0.576
- G2 schema_validity: +0.833
- G8 schema_validity: +0.833
- G9 schema_validity: +0.833
- G2 atom_primary_metric: +0.833
- G8 atom_primary_metric: +0.833
- G9 atom_primary_metric: +0.833

This supports the weaker but important claim:

> Mechanism arms make the budget model substantially more reliable on bounded contract-critical operations.

### Harnessed Weak vs Unconstrained Strong

Aggregate `budget_model + harness` advantage over `strong_model + G0` is positive on key metrics:

- G2 task_success: +0.688
- G8 task_success: +0.715
- G9 task_success: +0.743
- G2 schema_validity: +1.000
- G8 schema_validity: +1.000
- G9 schema_validity: +1.000
- G2 atom_primary_metric: +1.000
- G8 atom_primary_metric: +1.000
- G9 atom_primary_metric: +1.000

This supports the product-methodology claim:

> On contract-critical metrics, a harnessed budget model can outperform an unconstrained strong model.

### Gap Compression

Gap compression is mixed but mostly positive on general contract metrics:

- G2 task_success compression: 0.625
- G8 task_success compression: 0.958
- G9 task_success compression: 1.000
- G2 schema_validity compression: 1.000
- G8 schema_validity compression: 1.000
- G9 schema_validity compression: 1.000
- G2 safety_consistency compression: 1.000
- G8 safety_consistency compression: 1.000
- G9 safety_consistency compression: 1.000

However, `atom_primary_metric` is mixed:

- G2 atom_primary_metric compression: -1.000
- G8 atom_primary_metric compression: -1.000
- G9 atom_primary_metric compression: 0.000

Interpretation:

- The harness strongly improves absolute weak-model capability.
- It often compresses gaps on general contract metrics.
- It does not uniformly compress atom-primary gaps because some mechanisms help the budget model more or leave a residual atom-specific difference.

## Execution Deviations And Recovery

### Deviation 1: Initial 48-run adapter timeout

The first full adapter execution timed out after 15 minutes. Artifact audit showed:

- 42 runs had written non-pending outputs.
- 6 runs remained pending.
- Adapter report was not written because the outer process timed out.

Resolution:

- Ran partial postprocess.
- Confirmed 42 completed runs and 6 pending warnings.
- Did not proceed to Stage 7.
- Created rerun manifests for pending runs only.

### Deviation 2: Non-placeholder outputs in rerun subset

The first 6-run rerun preflight warned that two output files were non-placeholder.

Audit showed:

- A8 budget G2 r1 and r2 had completed during the timed-out run.
- Only A8 budget G8/G9 remained pending.

Resolution:

- Re-ran postprocess, collecting 44 completed runs.
- Reduced rerun manifest to only the remaining pending runs.

### Deviation 3: Provider read timeout on A8 budget G8 r2

Single-run retry failed with:

```text
The read operation timed out
```

Resolution:

- Increased SiliconFlow provider `timeout_seconds` from 180 to 420.
- Re-ran the same prompt/model/arm without changing the experimental content.
- Retry succeeded.

This is an execution-parameter adjustment, not a change to the hypothesis, fixture, model mapping, or evaluator.

## Deviation Judgment

The deviations are reasonable and do not require revising the research assumptions.

They do require this operational lesson:

> Mechanism-atom pilots with longer G8/G9 prompts should be executed in smaller batches or with a longer provider timeout.

## Stage 7 Gate

Do not immediately compose full macro workflows from this pilot alone.

Reason:

- Stage 6 pilot tested A1, A3, and A8.
- Full project-initialization composition also requires A4, A9, A10, A6, and A7.
- Full research-workflow composition also requires A2, A5, A7, and A6.

Therefore, Stage 7 must either:

1. compose only a partial workflow using passing atoms, or
2. run an additional composition-critical atom pilot before full workflow composition.

The strict roadmap favors option 2.
