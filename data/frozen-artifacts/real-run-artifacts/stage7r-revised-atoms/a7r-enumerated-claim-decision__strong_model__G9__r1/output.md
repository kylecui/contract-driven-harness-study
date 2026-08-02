```json
{
  "selected_option_id": "C2",
  "selected_claim": "Harness improves absolute contract adherence and enables weak models on mechanism-bound tasks.",
  "rejected_option_ids": ["C1", "C3"],
  "decision_trace": [
    {
      "step": 1,
      "action": "Evaluate C1 (universal gap closure) against evidence.",
      "reasoning": "Evidence atom-a7r-e02 explicitly states 'Gap compression is not universal across all tasks.' This directly contradicts the universal claim of C1. Therefore, C1 must be rejected.",
      "evidence_cited": ["atom-a7r-e02"]
    },
    {
      "step": 2,
      "action": "Evaluate C3 (prose style improvement) against evidence.",
      "reasoning": "Evidence atom-a7r-e03 states 'No evaluation measured prose style.' Since the claim is about an outcome that was not measured, it cannot be supported by the supplied evidence and must be rejected per the decision rule.",
      "evidence_cited": ["atom-a7r-e03"]
    },
    {
      "step": 3,
      "action": "Evaluate C2 (weak-model enablement on mechanism-bound tasks) against evidence.",
      "reasoning": "Evidence atom-a7r-e01 provides direct support: 'Weak-model G8/G9 task success improved from 0.000 to 0.667 in Stage7p v2 composition retention.' This demonstrates an absolute improvement in task success (contract adherence) for a weak model on a specific task type (G8/G9, which are mechanism-bound tasks). The claim is specific and aligns with the measured outcome.",
      "evidence_cited": ["atom-a7r-e01"]
    },
    {
      "step": 4,
      "action": "Apply decision rule to select the most specific supported claim.",
      "reasoning": "C1 and C3 are rejected. C2 is supported by specific evidence of performance improvement on a mechanism-bound task. It is the most specific claim among the options that is directly corroborated by the evidence bundle.",
      "evidence_cited": ["atom-a7r-e01", "atom-a7r-e02", "atom-a7r-e03"]
    }
  ],
  "evidence_ids": ["atom-a7r-e01", "atom-a7r-e02", "atom-a7r-e03"]
}
```