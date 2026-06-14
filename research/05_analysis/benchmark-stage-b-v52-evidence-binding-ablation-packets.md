# Benchmark Packet Dry-Run Report

## Summary

- Packets compiled: 30
- Failures: 0
- Packet JSONL: `research\05_analysis\benchmark-stage-b-v52-evidence-binding-ablation-packets.jsonl`

## Harness Arms

| Arm | Packets |
|---|---:|
| `G9` | 30 |

## Fixtures

| Fixture | Packets |
|---|---:|
| `stage-b-v52-r1--canonical` | 3 |
| `stage-b-v52-r1--distractor-evidence` | 3 |
| `stage-b-v52-r1--evidence-order-shuffled` | 3 |
| `stage-b-v52-r1--field-alias` | 3 |
| `stage-b-v52-r1--unknown-state-paraphrase` | 3 |
| `stage-b-v52-r2--canonical` | 3 |
| `stage-b-v52-r2--distractor-evidence` | 3 |
| `stage-b-v52-r2--evidence-order-shuffled` | 3 |
| `stage-b-v52-r2--field-alias` | 3 |
| `stage-b-v52-r2--unknown-state-paraphrase` | 3 |

## Models

| Model | Packets |
|---|---:|
| `budget_model` | 30 |

## Interpretation

This is a benchmark infrastructure dry-run, not a model evaluation. It proves the planned matrix can be compiled into consistent model-adapter packets.

## Failures

- None
