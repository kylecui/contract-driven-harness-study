# Benchmark Packet Dry-Run Report

## Summary

- Packets compiled: 36
- Failures: 0
- Packet JSONL: `research\05_analysis\benchmark-stage7r-revised-atoms-packets.jsonl`

## Harness Arms

| Arm | Packets |
|---|---:|
| `G0` | 12 |
| `G8` | 12 |
| `G9` | 12 |

## Fixtures

| Fixture | Packets |
|---|---:|
| `a2r-unsupported-claim-detection` | 6 |
| `a3r-constraint-safe-plan` | 6 |
| `a4r-strict-state-inventory` | 6 |
| `a5r-stage-gate-check` | 6 |
| `a7r-enumerated-claim-decision` | 6 |
| `a8r-evidence-type-rules` | 6 |

## Models

| Model | Packets |
|---|---:|
| `budget_model` | 18 |
| `strong_model` | 18 |

## Interpretation

This is a benchmark infrastructure dry-run, not a model evaluation. It proves the planned matrix can be compiled into consistent model-adapter packets.

## Failures

- None
