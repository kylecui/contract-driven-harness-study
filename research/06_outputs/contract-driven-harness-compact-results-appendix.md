# Compact Results Appendix

Target paper: `research/06_outputs/contract-driven-harness-paper-draft.md`

Prepared on: 2026-06-09

Purpose: provide compact, citation-ready result tables for the contract-driven harness paper. These tables support venue-neutral review and can be moved into the main paper, appendix, or supplementary material after venue selection.

## Table 1. Broad Task Slices: Gap Compression Summary

| Slice | Runs | Arm | Metric highlights | Interpretation | Evidence |
|---|---:|---|---|---|---|
| Structured extraction v2 | 24 | G9 vs G0 | Nonzero G0 gaps compressed to 0.000 for task_success, schema_validity, tool_call_correctness, human_acceptance, cost_efficiency, and safety_consistency; compression ratio 1.000 on those metrics. Citation grounding baseline gap was 0.000 and is n/a. | Strongest positive gap-compression slice. | P2-E27, P2-E28 |
| Project initialization | 12 | G9 vs G0 | task_success gap 0.111 -> 0.000; safety_consistency gap 0.200 -> 0.000. schema_validity gap 0.250 -> 0.583; human_acceptance and cost_efficiency gaps also widened. | Absolute lift with mixed gap movement; not universal compression. | P2-E29, P2-E30 |
| Research workflow | 12 | G9 vs G0 | schema_validity gap 0.067 -> 0.000. Several G0 baseline gaps were 0.000, making compression n/a; task_success gap became 0.083 from zero baseline. | Broad research workflow is too coarse as primitive evidence for universal compression. | P2-E31, P2-E32 |

## Table 2. Stage 6 Mechanism-Atom Pilot

| Item | Value |
|---|---|
| Matrix | 2 models x 3 atoms x 4 arms x 2 repetitions |
| Planned/completed runs | 48/48 |
| Atoms | A1 schema-bound extraction; A3 constraint-safe planning; A8 evidence-type separation |
| Models | `deepseek-ai/DeepSeek-V3.2`; `Qwen/Qwen3-8B` |
| Key low-cost-model lift vs G0 | G9 task_success +0.576; schema_validity +0.833; atom_primary_metric +0.833 |
| Harnessed low-cost vs unconstrained strong | G9 task_success +0.743; schema_validity +1.000; atom_primary_metric +1.000 |
| Gap compression | G9 task_success 1.000; schema_validity 1.000; atom_primary_metric 0.000 |
| Interpretation | Strong weak-model enablement; gap compression positive on general contract metrics but not uniform on atom-primary metrics. |
| Evidence | P2-E43, P2-E44 |

## Table 3. Stage 7p Partial Composition And Retention Repair

| Stage | Macro | Runs | Result | Interpretation | Evidence |
|---|---|---:|---|---|---|
| Stage 7p v1 | A10 bounded context recall -> A9 no-overwrite action planning -> A6 validator repair | 6/6 completed | Strong model passed under G8/G9; low-cost model improved but failed full chain because stale-context exclusion was not preserved. | Atom success does not automatically imply macro composition success. | P2-E51, P2-E52 |
| Stage 7p v2 | Same chain with explicit composition-retention contract | 6/6 completed | Both model tiers passed under G8/G9 with task_success, context_relevance, safety, repair_success, and atom_primary_metric all 1.000. | Explicit carried obligations repaired the low-cost composition failure. | P2-E53, P2-E54 |

## Table 4. Stage 7r And Stage 7r.1 Targeted Atom Repairs

| Stage | Scope | Completion | Result | Interpretation | Evidence |
|---|---|---:|---|---|---|
| Stage 7r | Revised A2R, A3R, A4R, A5R, A7R, A8R | 35/36 real outputs; one A8R low-cost G8 provider-timeout deviation | Strong model passed all revised atoms under G8/G9. Low-cost model improved but still failed strict A2R evidence binding and A7R trace completeness. | Positive but not sufficient for broader composition. | P2-E55, P2-E56 |
| Stage 7r.1 | Tightened A2R1 and A7R1 contracts | 8/8 completed and passed | Low-cost model passed A2R1/A7R1 under G8/G9 with two reps each; all task_success and atom_primary_metric values were 1.000. | Claim-level evidence binding and rejected-option trace completeness were repairable by tightening output contracts. | P2-E57, P2-E58, P2-E59, P2-E60 |

## Table 5. Stage 7e Repair Loop

| Stage | Targeted obligation | Runs | Result | Remaining blocker after stage | Evidence |
|---|---|---:|---|---|---|
| Stage 7e v1 | Initial evidence-bound decision macro | 6/6 completed | Strong G8/G9 and low-cost G8 passed; low-cost G9 partially failed with task_success 0.714 due trace/gate miss. | Decision-trace and stage-gate retention. | P2-E62, P2-E63 |
| Stage 7e v2 | decision_trace, stage_gate, carried_obligations retention | 4/4 completed | trace_completeness and stage_completion reached 1.000 in all runs. | state_inventory omissions for Git/CI/network/API unknowns; full macro pass 1/4. | P2-E64, P2-E65 |
| Stage 7e v3 | Unknown-state retention | 4/4 completed | Required unknown-state and forbidden-inference fields preserved in all runs; full macro pass 3/4. | One G8 run compressed known-state provenance. | P2-E66, P2-E67 |
| Stage 7e v4 | Known-state provenance | 4/4 completed after retry | All runs passed with task_success and atom_primary_metric 1.000; state, grounding, evidence type, trace, and gate metrics all 1.000. | No blocker for this fixed macro; broader workflow still not admitted. | P2-E68, P2-E69 |

## Table 6. Stage 7-next Transfer Macro

| Item | Value |
|---|---|
| Macro | Evidence-bound method-plan update |
| New stressor | Select next admitted macro, specify admission criteria, preserve local and real-model gates, declare non-claims |
| Local gate | Golden passed with task_success 1.000 and atom_primary_metric 1.000; known-bad premature expansion failed with task_success 0.000 |
| Real smoke | `Qwen/Qwen3-8B` x G8/G9 x 2 repetitions = 4 runs |
| Execution | 4/4 completed; no provider error, timeout, or truncated-output retry |
| Evaluation | 4/4 passed; task_success, atom_primary_metric, schema_validity, citation_grounding, state_accuracy, evidence_type_accuracy, trace_completeness, stage_completion, and context_relevance all 1.000 |
| Interpretation | Narrow transfer claim: Stage 7e v4 obligations transfer to a neighboring fixed method-plan macro. |
| Evidence | P2-E72, P2-E74, P2-E75 |

## Table 7. Current Claim Boundary

| Claim type | Status | Support | Boundary |
|---|---|---|---|
| Absolute contract adherence lift | Supported | Broad task slices and mechanism/macro stages | Applies to tested conditions, not production readiness. |
| Gap compression | Conditional | Strong in structured extraction; mixed or n/a elsewhere | Only claim when baseline gaps are nonzero and arm gaps shrink. |
| Weak-model enablement | Strongest supported claim | Stage 6, Stage 7r.1, Stage 7e v4, Stage 7-next | Fixed or bounded contract-critical operations. |
| Full project initialization | Not supported | Earlier slice mixed; no admitted full workflow | Remains a non-claim. |
| Full research workflow | Not supported | Earlier slice mixed/n/a; no admitted full workflow | Remains a non-claim. |
| Production readiness | Not supported | No production deployment, live tool safety audit, or operational monitoring | Remains a non-claim. |

## Usage In Paper

Recommended placement:

- Table 1 in Results.
- Tables 2-6 in appendix or supplementary material.
- Table 7 near Discussion or Non-Claims appendix.

For page-limited ACM/IEEE submission, compress Tables 2-6 into one "Repair-loop evidence summary" table and move detailed rows to supplementary material.
