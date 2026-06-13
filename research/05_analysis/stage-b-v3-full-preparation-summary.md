# Stage B v3 Full-Slice Preparation Summary

Prepared: 2026-06-13

Status: protocol frozen and ready for an execution decision; no paid Stage B
v3 full-slice calls made

## Decision Question

Stage B v3 tests whether the literal JSON skeleton and explicit grounded-claim
slots that repaired the three-run shape smoke remain reliable across both macro
tasks and all five representation perturbations.

This is a repair-confirmation experiment. Stage B v1, v2, and v3 are separate
protocols and must not be pooled.

## Frozen Run Design

- provider: SiliconFlow;
- model: `Qwen/Qwen3-8B`;
- model tier: low-cost model;
- harness: G9;
- macros: 2;
- representation conditions: 5;
- repetitions: 3 per cell;
- total planned calls: 30;
- temperature: 0;
- `enable_thinking`: false;
- maximum output tokens: 3000.

The price evidence remains recorded in
`research/01_sources/siliconflow-pricing-snapshot-2026-06-13.md`.

## v3 Repair Package

1. Preserve the complete JSON hierarchy through a literal output skeleton.
2. Keep `state_inventory` as an object containing `known_state`,
   `unknown_state`, and `forbidden_inferences`.
3. Preserve the exact number of grounded and unsupported claim slots.
4. Bind four required evidence IDs across the grounded-claim slots.
5. Reject flattened, root-promoted, and incomplete state structures.
6. Reject compressed grounded-claim arrays that remove required support.

The repair package deliberately gives the model a strong structural scaffold.
The experiment therefore measures reliable contract completion under
representation perturbation, not unconstrained schema induction or open-ended
writing quality.

## Completed Gates

| Gate | Result |
|---|---|
| Stage B v3 golden/known-bad | 110/110 expectations met |
| Stage B v2 regression | 70/70 expectations met |
| Stage B v3 shape-smoke regression | 10/10 expectations met |
| Packet compilation | 30/30 |
| Unique run IDs | 30/30 |
| Literal nested-state skeleton | 30/30 |
| Four-ID grounded support contract | 30/30 |
| Field-alias surface isolation | 6/6 prompts clean |
| Unknown-state paraphrase isolation | 6/6 prompts clean |
| Provider config | Pass |
| API-key preflight | 0 errors, 0 warnings |
| Adapter dry-run | 30/30, `execute=false` |
| Adapter unit tests | 5/5 |

The initial local gate exposed one fixture-spec mismatch: the Stage 7-next
grounded-support set named `stage7next-e04`, while the golden claim slot used
the bounded C2 support `stage7next-e06`. The generator was corrected and all
fixtures were rebuilt before the successful gates above. No model result was
changed or discarded.

## Cell Rule

Each of the ten macro-condition cells passes only if at least 2 of its 3 runs
pass the full deterministic contract.

The full slice stops for diagnosis if:

- any cell passes fewer than 2/3 runs;
- a provider failure, timeout, or truncation prevents a valid attempt;
- evaluator behavior is ambiguous;
- a prompt, fixture, evaluator, or provider setting changes after execution
  begins.

Every attempt and retry must remain in the evidence record. A successful retry
cannot replace a failed attempt.

## Expected Commands

Local evaluator gate:

```powershell
python -B research/04_methods/scripts/evaluate_stage7e_macro_artifacts.py `
  --fixtures-dir research/04_methods/macro-perturbations-v3 `
  --local-check `
  --output-runs research/05_analysis/stage-b-v3-full-local-gate.json `
  --output-md research/05_analysis/stage-b-v3-full-local-gate.md
```

Preflight:

```powershell
python -B research/04_methods/scripts/preflight_real_model_pilot.py `
  --manifest research/05_analysis/real-run-artifacts/stage-b-v3-full-manifest-with-prompts.json `
  --config research/04_methods/provider-config.siliconflow-stage-b-v3-full.json `
  --output-md research/05_analysis/stage-b-v3-full-preflight.md `
  --output-json research/05_analysis/stage-b-v3-full-preflight.json `
  --require-keys
```

Paid execution, only after explicit approval:

```powershell
python -B research/04_methods/scripts/run_openai_adapter.py `
  --manifest research/05_analysis/real-run-artifacts/stage-b-v3-full-manifest-with-prompts.json `
  --config research/04_methods/provider-config.siliconflow-stage-b-v3-full.json `
  --report research/05_analysis/stage-b-v3-full-execution.json `
  --event-log research/05_analysis/stage-b-v3-full-adapter-events.jsonl `
  --execute
```

## Next Decision

The protocol and 30-run queue are frozen. The next experimental action requires
explicit approval to spend the provider budget and execute the queue.
