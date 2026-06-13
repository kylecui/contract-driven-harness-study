# Stage B v2 Validity Threats

Prepared: 2026-06-13

| Type | Threat | Possible impact | Mitigation |
|---|---|---|---|
| Internal | Multiple repairs change together | A v2 improvement cannot be assigned to one mechanism | Treat v2 as package-level repair confirmation; defer single-factor ablations |
| Internal | Provider runtime variation across sequential calls | Correlated success, timeout, or latency | Preserve timestamps, request IDs, event logs, and all retries |
| Internal | Temperature 0 may still be nondeterministic | Repeated outputs may differ | Use three runs per cell and report all outcomes |
| Construct | Deterministic gates may reward contract shape over semantic quality | Passing output may still be awkward or shallow | Review every failure and a sample of passes; retain non-claim boundary |
| Construct | Closed `preserved` vocabulary is intentionally narrow | Measures compliance with a frozen protocol, not synonym understanding | State this as a contract choice, not a language-capability claim |
| Construct | 3000-token budget and compact template both target truncation | Runtime repair source is ambiguous | Record output bytes/tokens; isolate later in ablation |
| External | Two macros are not representative of arbitrary workflows | Generalization may be overstated | Limit claims to admitted macros and declared perturbations |
| External | One provider and one low-cost model | Results may not transfer across providers or model families | Reserve model comparison for Stage D |
| Conclusion | Three runs per cell produce wide uncertainty | A 2/3 cell may not be stably reliable | Use as a screening gate and report Wilson intervals |
| Conclusion | Ten cells share fixture and evaluator structure | Aggregate 30-run statistics are not fully independent | Make cell thresholds primary and aggregate values descriptive |
| Reproducibility | Public provider behavior can change | Later reruns may differ | Freeze config, prompts, checksums, date, and provider metadata |
| Reproducibility | Post-execution evaluator repair can bias interpretation | Outcome-driven rescoring | Freeze before calls; preserve raw and corrected views if a defect is found |
