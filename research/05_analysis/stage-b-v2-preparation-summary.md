# Stage B v2 Preparation Summary

Prepared: 2026-06-13

Status: ready for execution decision; no paid Stage B v2 calls made

## Decision Question

Stage B v2 tests whether the repaired G9 package allows `Qwen/Qwen3-8B` to pass
at least 2/3 runs in each of ten macro-condition cells.

The protocol is a repair confirmation after Stage B v1 failed. Stage B v1 and
v2 remain separate and cannot be pooled.

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

The current price evidence is preserved in
`research/01_sources/siliconflow-pricing-snapshot-2026-06-13.md`.

## Repairs From Stage B v1

1. Added an explicit compact JSON output template.
2. Fixed one required evidence combination for each selected C2 claim.
3. Closed carried-obligation status to `preserved`.
4. Required ID-only `typed_evidence` arrays.
5. Added exact array counts and nested-field checks.
6. Added canonical-fallback and hybrid-surface rejection.
7. Separated model-visible surface contracts from evaluator-only canonical maps.
8. Raised the completion budget from 2000 to 3000 tokens.

These changes are one repaired package. Stage B v2 cannot assign a causal effect
to any one repair.

## Completed Gates

| Gate | Result |
|---|---|
| Stage B v2 golden/known-bad | 70/70 expectations met |
| Stage B v1 regression | 28/28 expectations met |
| Provider config | Pass |
| API-key preflight | 0 errors, 0 warnings |
| Packet compilation | 30/30 |
| Unique run IDs | 30/30 |
| Adapter dry-run | 30/30, `execute=false` |
| Adapter unit tests | 5/5 |
| Prompt surface isolation | 12/12 alias prompts clean |
| Freeze manifest | Generated with SHA-256 hashes |

## Stop Rule

The stage fails if any cell passes fewer than 2/3 runs. Provider failure,
timeout, truncation, evaluator ambiguity, or any protocol edit after execution
starts also stops progression for diagnosis.

Every attempt and retry must be retained. A successful retry cannot replace a
failed attempt.

## Expected Commands

Local evaluator gate:

```powershell
python -B research/04_methods/scripts/evaluate_stage7e_macro_artifacts.py `
  --fixtures-dir research/04_methods/macro-perturbations-v2 `
  --local-check `
  --output-runs research/05_analysis/stage-b-v2-local-gate.json `
  --output-md research/05_analysis/stage-b-v2-local-gate.md
```

Preflight:

```powershell
python -B research/04_methods/scripts/preflight_real_model_pilot.py `
  --manifest research/05_analysis/real-run-artifacts/post-freeze-perturbation-pilot-v2-manifest-with-prompts.json `
  --config research/04_methods/provider-config.siliconflow-stage-b-v2.json `
  --output-md research/05_analysis/post-freeze-perturbation-pilot-v2-preflight.md `
  --output-json research/05_analysis/post-freeze-perturbation-pilot-v2-preflight.json `
  --require-keys
```

Paid execution, only after explicit approval:

```powershell
python -B research/04_methods/scripts/run_openai_adapter.py `
  --manifest research/05_analysis/real-run-artifacts/post-freeze-perturbation-pilot-v2-manifest-with-prompts.json `
  --config research/04_methods/provider-config.siliconflow-stage-b-v2.json `
  --report research/05_analysis/post-freeze-perturbation-pilot-v2-execution.json `
  --event-log research/05_analysis/post-freeze-perturbation-pilot-v2-adapter-events.jsonl `
  --execute
```

## Next Decision

The preparation is complete. The next action is not another protocol edit; it is
an explicit decision on whether to spend the provider budget and execute the
frozen 30-run Stage B v2 queue.
