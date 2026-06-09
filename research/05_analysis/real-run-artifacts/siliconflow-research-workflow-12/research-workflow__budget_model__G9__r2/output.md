

```markdown
# Research Workflow Synthesis Report

## Brief
This synthesis evaluates the relationship between two proposal tracks: the topic-aware compaction paper and the harness engineering paper. Based on the evidence bundle, the analysis concludes that these tracks should remain separate due to differing evidence requirements and unresolved research risks. The compaction paper currently lacks robust ablation evidence, while the harness paper requires cross-model benchmarking, necessitating distinct development paths.

## Evidence Summary
1. **Evidence ID**: `fixture-rw-e01`  
   **Claim**: The topic-aware compaction paper has a single-model A/B result.  
   **Source**: `fixture-research-notes`  
   **Freshness**: Snapshot  

2. **Evidence ID**: `fixture-rw-e02`  
   **Claim**: The harness engineering paper requires cross-model benchmark evidence.  
   **Source**: `fixture-research-notes`  
   **Freshness**: Snapshot  

3. **Evidence ID**: `fixture-rw-e03`  
   **Claim**: The two papers should remain separate until the compaction work has stronger ablation evidence.  
   **Source**: `fixture-research-notes`  
   **Freshness**: Snapshot  
   **Type**: Inferred  

## Synthesis
The two tracks must be treated as separate entities due to their divergent evidence needs. The compaction paper (e01) is currently limited to single-model A/B testing, which does not establish generalizability across different model architectures. In contrast, the harness paper (e02) explicitly requires cross-model benchmarking to validate its approach. The inferred claim (e03) aligns with this analysis, emphasizing that combining the tracks would risk conflating these distinct evidence requirements. Without additional ablation studies for compaction (to address e03), merging the tracks would compromise the rigor of both proposals.

## Risks
- **Incomplete validation**: The compaction paper lacks ablation evidence (e03), making its effectiveness uncertain.  
- **Evidence mismatch**: The harness paper requires cross-model benchmarks (e02), which the compaction paper does not yet provide.  
- **Premature integration**: Combining the tracks without resolving these gaps could dilute the focus of both proposals.  

## Next Steps
1. Conduct ablation studies for the compaction paper to strengthen its evidence base (addressing e03).  
2. Collect cross-model benchmark data for the harness paper (e02) to ensure its claims are validated.  
3. Reassess the relationship between the tracks once both evidence requirements are satisfied.  

**Tool Trace**:  
- `filesystem` used to access and verify the evidence bundle items (`fixture-rw-e01`, `fixture-rw-e02`, `fixture-rw-e03`) and ensure no external claims were introduced.  
```