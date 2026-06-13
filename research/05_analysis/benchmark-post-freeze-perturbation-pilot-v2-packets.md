# Benchmark Packet Dry-Run Report

## Summary

- Packets compiled: 30
- Failures: 0
- Packet JSONL: `research\05_analysis\benchmark-post-freeze-perturbation-pilot-v2-packets.jsonl`

## Harness Arms

| Arm | Packets |
|---|---:|
| `G9` | 30 |

## Fixtures

| Fixture | Packets |
|---|---:|
| `stage7-next-method-plan-update-v2--canonical` | 3 |
| `stage7-next-method-plan-update-v2--distractor-evidence` | 3 |
| `stage7-next-method-plan-update-v2--evidence-order-shuffled` | 3 |
| `stage7-next-method-plan-update-v2--field-alias` | 3 |
| `stage7-next-method-plan-update-v2--unknown-state-paraphrase` | 3 |
| `stage7e-v4-known-state-provenance-decision-v2--canonical` | 3 |
| `stage7e-v4-known-state-provenance-decision-v2--distractor-evidence` | 3 |
| `stage7e-v4-known-state-provenance-decision-v2--evidence-order-shuffled` | 3 |
| `stage7e-v4-known-state-provenance-decision-v2--field-alias` | 3 |
| `stage7e-v4-known-state-provenance-decision-v2--unknown-state-paraphrase` | 3 |

## Models

| Model | Packets |
|---|---:|
| `budget_model` | 30 |

## Interpretation

This is a benchmark infrastructure dry-run, not a model evaluation. It proves the planned matrix can be compiled into consistent model-adapter packets.

## Failures

- None
