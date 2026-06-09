# Stage 3 Summary: First-Batch Mechanism Atom Fixtures

## Stage Objective

Build the first-batch atom fixtures for A1, A3, A4, A8, and A6, and confirm they can enter the benchmark matrix and packet compilation path.

## Result

Stage 3 is complete.

## First-Batch Atoms

- A1 Schema-Bound Extraction.
- A3 Constraint-Safe Planning.
- A4 State Inventory.
- A8 Evidence-Type Separation.
- A6 Validator Repair.

## Artifacts Used Or Created

- `research/04_methods/mechanism-atoms/a1-schema-bound-extraction/`
- `research/04_methods/mechanism-atoms/a3-constraint-safe-planning/`
- `research/04_methods/mechanism-atoms/a4-state-inventory/`
- `research/04_methods/mechanism-atoms/a8-evidence-type-separation/`
- `research/04_methods/mechanism-atoms/a6-validator-repair/`
- `research/04_methods/benchmark-matrix-mechanism-atoms-first-batch.json`
- `research/05_analysis/benchmark-mechanism-atoms-first-batch-packets.jsonl`
- `research/05_analysis/benchmark-mechanism-atoms-first-batch-packets.md`

## Pipeline Changes

`compile_benchmark_packets.py` now recognizes G8:

- G8 includes output schema, evidence bundle, memory policy, and validator.
- G8 requires validation.
- G8 receives OutputContract, EvidenceBundle, and MemorySlice in compiled packets.

## Validation Performed

Python compile check:

```text
python -m py_compile research/04_methods/scripts/compile_benchmark_packets.py
```

Result:

- Passed.

First-batch matrix generation:

```text
python research/04_methods/scripts/generate_benchmark_matrix.py --fixtures-dir research/04_methods/mechanism-atoms --output research/04_methods/benchmark-matrix-mechanism-atoms-first-batch.json --repetitions 1 --models strong_model budget_model --arms G0 G2 G8 G9 --fixtures a1-schema-bound-extraction a3-constraint-safe-planning a4-state-inventory a8-evidence-type-separation a6-validator-repair
```

Result:

- 40 planned runs generated.

Packet compilation:

```text
python research/04_methods/scripts/compile_benchmark_packets.py --matrix research/04_methods/benchmark-matrix-mechanism-atoms-first-batch.json --output-jsonl research/05_analysis/benchmark-mechanism-atoms-first-batch-packets.jsonl --output-md research/05_analysis/benchmark-mechanism-atoms-first-batch-packets.md --full-packets
```

Result:

- 40/40 packets compiled.
- 0 failures.

## Deviation Check

No major deviation was observed.

Minor implementation note:

- Stage 3 generated a 40-run one-repetition dry matrix to validate packet compilation. This is not the Stage 6 model pilot and should not be interpreted as an empirical run plan.

## Decision

Proceed to Stage 4.

Stage 4 must add atom-level evaluator metrics before any model execution.
