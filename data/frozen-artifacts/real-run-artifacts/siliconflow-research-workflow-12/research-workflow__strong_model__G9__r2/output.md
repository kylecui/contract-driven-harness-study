# Research Workflow Synthesis Report

## Brief

This report synthesizes evidence regarding two proposed systems paper tracks: a topic-aware compaction paper and a harness engineering paper. The goal is to determine whether these research tracks should be combined into a single paper or remain separate based on the current state of evidence.

## Evidence Summary

The evidence bundle contains three items, all sourced from local fixture research notes:

1.  **fixture-rw-e01 (EXTRACTED)**: The proposed topic-aware compaction paper currently has a single-model A/B result.
2.  **fixture-rw-e02 (EXTRACTED)**: The proposed harness engineering paper requires cross-model benchmark evidence.
3.  **fixture-rw-e03 (INFERRED)**: The two papers should remain separate until the compaction work has stronger ablation evidence.

**Tool Trace**: No external tools (e.g., filesystem) were used, as the analysis was conducted solely on the provided evidence bundle (`ev_research_workflow_001`). The task constraints prohibited adding outside claims.

## Synthesis

Based on the provided evidence, the two proposal tracks should remain as separate papers at this stage.

The primary reason for separation is the **mismatch in evidence maturity** between the two tracks. The topic-aware compaction work is in an early validation phase, supported only by a "single-model A/B result" (fixture-rw-e01). This is insufficient foundation for a robust systems paper and falls short of the evidence standard implied as necessary for the harness engineering paper, which "requires cross-model benchmark evidence" (fixture-rw-e02).

The inferred claim (fixture-rw-e03) directly supports this conclusion, stating the papers should be separate until the compaction work develops "stronger ablation evidence." Combining an early-stage idea (compaction) with a methodology that demands rigorous, generalizable proof (harness engineering) would weaken the overall contribution. A combined paper would either dilute the harness engineering claims or overstate the compaction results.

Therefore, the logical research path is to pursue them independently: the compaction track must first strengthen its evidentiary basis through ablation studies and multi-model validation, while the harness engineering track can proceed with its required cross-model benchmarking.

## Risks

1.  **Resource Dilution Risk**: Attempting to combine the papers could divert effort from the core requirement of each track—developing ablation evidence for compaction and cross-model benchmarks for harness engineering.
2.  **Publication Viability Risk**: A combined paper with a weak evidence chain for one of its core contributions (compaction) risks rejection from rigorous systems conferences.
3.  **Scope Creep Risk**: The harness engineering paper's requirement for cross-model evidence (fixture-rw-e02) is a significant undertaking. Merging it with an under-developed compaction idea could blur the paper's focus and exceed a manageable scope.
4.  **Inference Reliance Risk**: The key synthesizing claim (fixture-rw-e03) is marked as `INFERRED`. Its authority is derived from the `local_fixture`, but the underlying reasoning or context for this inference is not available in the extracted evidence.

## Next Steps

1.  **Validate Inference**: Seek the source or rationale behind the inferred claim (fixture-rw-e03) to confirm the assessment that ablation evidence is the critical gap for the compaction paper.
2.  **Parallel Development**:
    *   **For the compaction track**: Design and execute ablation studies to isolate the contribution of the topic-aware mechanism and expand validation beyond a single model.
    *   **For the harness engineering track**: Proceed with the design of cross-model benchmark experiments as required.
3.  **Re-evaluation Point**: Once the compaction track has produced the stronger ablation evidence, re-assess the potential for a combined paper. At that stage, the synergy between a robust compaction strategy and a harness built to evaluate it cross-model could form a compelling, unified narrative.
4.  **Evidence Tracking**: Maintain a clear ledger separating newly extracted evidence from future inferences as both research tracks progress.