# Benchmark Packet Dry-Run Report

## Summary

- Packets compiled: 30
- Failures: 0
- Packet JSONL: `research\05_analysis\benchmark-stage-b-v53-explicit-transition-delta-packets.jsonl`

## Harness Arms

| Arm | Packets |
|---|---:|
| `G9` | 30 |

## Fixtures

| Fixture | Packets |
|---|---:|
| `stage-b-v53-p1--canonical` | 3 |
| `stage-b-v53-p1--distractor-evidence` | 3 |
| `stage-b-v53-p1--evidence-order-shuffled` | 3 |
| `stage-b-v53-p1--field-alias` | 3 |
| `stage-b-v53-p1--unknown-state-paraphrase` | 3 |
| `stage-b-v53-p2--canonical` | 3 |
| `stage-b-v53-p2--distractor-evidence` | 3 |
| `stage-b-v53-p2--evidence-order-shuffled` | 3 |
| `stage-b-v53-p2--field-alias` | 3 |
| `stage-b-v53-p2--unknown-state-paraphrase` | 3 |

## Models

| Model | Packets |
|---|---:|
| `budget_model` | 30 |

## Interpretation

This is a benchmark infrastructure dry-run, not a model evaluation. It proves the planned matrix can be compiled into consistent model-adapter packets.

## Failures

- None
