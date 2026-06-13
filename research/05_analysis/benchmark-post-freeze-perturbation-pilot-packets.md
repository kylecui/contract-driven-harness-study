# Benchmark Packet Dry-Run Report

## Summary

- Packets compiled: 30
- Failures: 0
- Packet JSONL: `research\05_analysis\benchmark-post-freeze-perturbation-pilot-packets.jsonl`

## Harness Arms

| Arm | Packets |
|---|---:|
| `G9` | 30 |

## Fixtures

| Fixture | Packets |
|---|---:|
| `stage7-next-method-plan-update--canonical` | 3 |
| `stage7-next-method-plan-update--distractor-evidence` | 3 |
| `stage7-next-method-plan-update--evidence-order-shuffled` | 3 |
| `stage7-next-method-plan-update--field-alias` | 3 |
| `stage7-next-method-plan-update--unknown-state-paraphrase` | 3 |
| `stage7e-v4-known-state-provenance-decision--canonical` | 3 |
| `stage7e-v4-known-state-provenance-decision--distractor-evidence` | 3 |
| `stage7e-v4-known-state-provenance-decision--evidence-order-shuffled` | 3 |
| `stage7e-v4-known-state-provenance-decision--field-alias` | 3 |
| `stage7e-v4-known-state-provenance-decision--unknown-state-paraphrase` | 3 |

## Models

| Model | Packets |
|---|---:|
| `budget_model` | 30 |

## Interpretation

This is a benchmark infrastructure dry-run, not a model evaluation. It proves the planned matrix can be compiled into consistent model-adapter packets.

## Failures

- None
