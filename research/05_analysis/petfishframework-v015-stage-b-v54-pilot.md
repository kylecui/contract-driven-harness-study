# petfishframework 0.1.5 Pilot: Stage B v5.4 Offline Recheck

## Research Task Plan

- research_type: Scientific / reliability evaluation
- complexity_level: light pilot
- recommended_skill_chain: research-router -> scientific-experiment-planner -> anti-sycophancy-calibration
- expected_artifacts: JSON result, Markdown report
- key_risks: offline replay does not test new model calls; one fixture family does not prove broad data reliability

## Setup

- framework_version: `0.1.5`
- input_results: `research\05_analysis\stage-b-v54-explicit-delta-stability-results.json`
- artifact_root: `research\05_analysis\real-run-artifacts\stage-b-v54-explicit-delta-stability`
- workload: 40 completed Stage B v5.4 explicit-delta runs, five perturbation conditions, eight repetitions each

## Pass^8 Recheck

- overall_pass: `True`
- pass_rate: `1.000`

| Condition | Pass | Agreed |
|---|---:|---:|
| canonical | 8/8 | true |
| field_alias | 8/8 | true |
| evidence_order_shuffled | 8/8 | true |
| distractor_evidence | 8/8 | true |
| unknown_state_paraphrase | 8/8 | true |

## Structured Output And Audit

- structured_parse: 40/40
- complete_artifact_sets: 40/40
- metrics_files_matching_results: 40/40
- validation_json_successes: 40/40

## Interpretation

This pilot supports using petfishframework as a thin reliability/audit wrapper for existing benchmark artifacts.
It reproduced the Stage B v5.4 stability signal as Pass^8 over the five designed perturbation conditions and found no structured parsing, artifact completeness, metric consistency, or validation JSON failures in this slice.

It does not prove that underlying source data became more truthful. The result is evidence for process reliability on one frozen controlled-transition workload, not broad data-quality or production-readiness evidence.
