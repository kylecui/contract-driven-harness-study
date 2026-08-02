```json
{
  "stage_status": {
    "research_brief": "complete",
    "source_index": "complete",
    "evidence_ledger": "incomplete",
    "citation_audit": "not_started"
  },
  "gate_decision": {
    "synthesis_allowed": false,
    "recommendation_allowed": false,
    "reason": "Missing required prerequisites for synthesis and recommendation."
  },
  "missing_prerequisites": [
    "evidence_ledger",
    "citation_audit"
  ],
  "blocked_outputs": [
    "synthesis",
    "final_recommendation"
  ],
  "next_required_actions": [
    "Complete evidence_ledger (required for synthesis)",
    "Complete citation_audit (required for final recommendation)"
  ],
  "evidence_ids": [
    "atom-a5r-e01",
    "atom-a5r-e02",
    "atom-a5r-e03"
  ]
}
```