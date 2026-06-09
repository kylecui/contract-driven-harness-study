# Results: From Gap Compression To Mechanism-Bound Enablement

## 1. Overview

The results support a bounded version of the original hypothesis. Contract-rich harnessing improves absolute contract adherence across several productivity-task settings, and it can compress cross-model gaps in highly constrained tasks. However, gap compression is not universal. The stronger and more stable result is weak-model enablement on bounded, contract-critical operations: when task obligations are made explicit and evaluated deterministically, the low-cost model can reach pass-level behavior on tasks where weaker harnessing or broader prompts were unstable.

The evidence falls into five result blocks:

1. broad task slices show where gap compression works and where it becomes mixed;
2. mechanism-atom pilots show that harness mechanisms can improve low-cost-model contract adherence;
3. partial macro composition shows that atom success does not automatically imply composition success;
4. the Stage 7e repair loop shows that specific low-cost-model failures can be converted into explicit, testable obligations;
5. Stage 7-next shows that the repaired obligation set transfers to a neighboring fixed macro.

## 2. Task Slices: Strong Absolute Lift, Conditional Gap Compression

The first task-slice results show that harnessing improves absolute behavior, but cross-model gap movement depends on task structure and baseline gaps.

### Structured Extraction

The structured-extraction v2 slice is the clearest positive gap-compression result. Under G0, nonzero baseline gaps existed on task success, schema validity, tool-call correctness, human acceptance, cost efficiency, and safety consistency. Under G9, all measured nonzero gaps compressed to 0.000, producing compression ratios of 1.000 on those metrics. Citation grounding had a baseline gap of 0.000 and is therefore reported as n/a rather than as compression.

This supports the narrow claim that high-constraint structured extraction can show full measured gap compression under a contract-rich harness.

### Project Initialization

The project-initialization slice shows why gap compression cannot be the universal claim. G9 compressed the task-success gap from 0.111 to 0.000 and the safety-consistency gap from 0.200 to 0.000. However, schema validity moved from a baseline gap of 0.250 to an arm gap of 0.583, yielding a negative compression ratio of -1.333. Human acceptance and cost efficiency also showed negative compression ratios.

This does not mean the harness was useless. It means the low-cost model and strong model benefited unevenly across metrics. The practical interpretation is absolute lift with mixed gap movement, not universal gap compression.

### Research Workflow

The research-workflow slice further weakens a universal gap-compression story. Several G0 baseline gaps were already 0.000, making compression undefined. G9 compressed schema-validity gap from 0.067 to 0.000, but task-success gap became 0.083 from a 0.000 baseline and human-acceptance/cost-efficiency gap movement was slightly negative.

This result is best read as evidence that broad research workflow prompts are too coarse as primitive benchmarks. The harness improves some contract dimensions, but the broad task mixes evidence grounding, synthesis, schema, stage discipline, and recommendation quality into one unstable unit.

## 3. Mechanism Atoms: Broad Workflows Need Smaller Units

The Stage 6 mechanism-atom pilot tested 48 real model runs:

```text
2 models x 3 atoms x 4 arms x 2 repetitions = 48 runs
```

The pilot completed 48/48 runs after documented timeout recovery. Its strongest result was weak-model enablement. For the low-cost model relative to G0:

- G2 task_success lift: +0.521
- G8 task_success lift: +0.549
- G9 task_success lift: +0.576
- G2/G8/G9 schema_validity lift: +0.833
- G2/G8/G9 atom_primary_metric lift: +0.833

The harnessed low-cost model also outperformed the unconstrained strong model on contract-critical metrics. Relative to strong_model + G0:

- low-cost model + G9 task_success advantage: +0.743
- low-cost model + G9 schema_validity advantage: +1.000
- low-cost model + G9 atom_primary_metric advantage: +1.000

Gap compression was mostly positive on general contract metrics, including G9 task_success compression of 1.000 and G9 schema_validity compression of 1.000. But atom_primary_metric remained mixed, with G9 compression of 0.000 and G2/G8 negative values. This supports the conclusion that harnesses can substantially raise low-cost-model reliability on bounded operations even when atom-specific gap compression is not uniform.

## 4. Composition: Atom Success Is Not Enough

Stage 7p tested whether passing atoms could compose into a narrow partial macro:

```text
A10 bounded context recall -> A9 no-overwrite action planning -> A6 validator repair
```

The execution completed cleanly with 6/6 real SiliconFlow runs. Strong_model G8 and G9 passed the full partial-composition chain with task_success=1.000 and chain=1.000. The low-cost model improved strongly under G8/G9, reaching task_success=0.800 under G8 and 0.900 under G9, with schema_validity=1.000 and safety=1.000. Yet it failed the full chain because context_relevance stayed 0.000: the composed output did not explicitly carry forward the stale-context exclusion.

This is a key negative result. The input context did contain the exclusion, but the macro output did not preserve it. Therefore, isolated atom success did not guarantee low-cost-model composition success. Composition introduced a cross-step retention obligation that the atom tests had not fully enforced.

Stage 7p v2 then added an explicit composition-retention contract. The same partial chain passed for both model tiers under G8/G9. For the low-cost model:

- G8/G9 task_success: 1.000
- G8/G9 schema_validity: 1.000
- G8/G9 context_relevance: 1.000
- G8/G9 safety and constraint consistency: 1.000
- G8/G9 repair_success: 1.000
- G8/G9 atom_primary_metric: 1.000

The gap-compression ratios on nonzero G0 baseline gaps for task_success and schema_validity were 1.000 under both G8 and G9.

This result supports a composition-layer mechanism claim: cross-step obligation retention is necessary when a macro must preserve negative context constraints across multiple atom outputs.

## 5. Revised Atoms And Targeted Repairs

Stage 7r redesigned six boundary-prone atoms: A2R, A3R, A4R, A5R, A7R, and A8R. Local gates passed: 6/6 fixture structures, 12/12 local golden/bad expectations, 36/36 packet compilation, and preflight with 0 errors and 0 warnings.

The real-model smoke completed 35/36 outputs. The single missing output was A8R low-cost G8, which repeatedly timed out under SiliconFlow and was treated as an execution deviation rather than a model-quality score. On completed runs:

| Model tier | Arm | Complete | Passed | Avg task success | Avg atom primary |
|---|---:|---:|---:|---:|---:|
| strong_model | G0 | 6 | 0 | 0.000 | 0.000 |
| strong_model | G8 | 6 | 6 | 1.000 | 1.000 |
| strong_model | G9 | 6 | 6 | 1.000 | 1.000 |
| low_cost_model | G0 | 6 | 0 | 0.228 | 0.167 |
| low_cost_model | G8 | 5 | 3 | 0.800 | 0.600 |
| low_cost_model | G9 | 6 | 4 | 0.833 | 0.667 |

This result was positive but not sufficient for broad workflow composition. The low-cost model still failed strict A2R citation grounding and A7R trace completeness. Stage 7r.1 targeted exactly those failures by tightening the contracts:

- A2R1 required every grounded claim to be an object with non-empty `evidence_ids`.
- A7R1 required rejected-option objects with evidence IDs and trace steps for C2 support, C1 rejection, and C3 rejection.

The targeted 8-run low-cost-model smoke passed 8/8:

| Fixture | Arm | Completed | Passed | Avg task success | Avg atom primary |
|---|---:|---:|---:|---:|---:|
| A2R1 | G8 | 2 | 2 | 1.000 | 1.000 |
| A2R1 | G9 | 2 | 2 | 1.000 | 1.000 |
| A7R1 | G8 | 2 | 2 | 1.000 | 1.000 |
| A7R1 | G9 | 2 | 2 | 1.000 | 1.000 |

This supports the mechanism-first repair hypothesis: low-cost-model failures on claim-level evidence binding and rejection-trace completeness can be repaired by narrowing the output contract.

## 6. Stage 7e: Iterative Repair Of A Fixed Evidence-Decision Macro

Stage 7e composed a narrow evidence-bound decision macro from state inventory, evidence grounding, evidence-type separation, traceable decision, and stage-gated synthesis mechanisms. The first Stage 7e smoke completed 6/6 runs. Strong_model G8/G9 and low-cost-model G8 passed with task_success=1.000 and atom_primary_metric=1.000. G0 failed for both model tiers. Low-cost-model G9 partially failed with task_success=0.714 because it missed complete decision-trace and stage-gate retention.

Instead of expanding to broader workflows, the next stages repaired the specific miss.

### Stage 7e v2

Stage 7e v2 added explicit retention requirements for decision_trace, stage_gate, and carried_obligations. The targeted low-cost-model G8/G9 smoke completed 4/4 runs, and all 4/4 achieved:

- trace_completeness=1.000
- stage_completion=1.000

However, full macro stability was not established. Only 1/4 runs fully passed; the remaining runs failed strict atom_primary_metric because they omitted Git branch, CI status, or network/API approval unknowns from state_inventory.

### Stage 7e v3

Stage 7e v3 targeted unknown-state retention. The low-cost-model smoke completed 4/4 runs. All 4/4 preserved the required Git/CI/network unknown-state fields and forbidden-inference fields. Full strict macro pass improved to 3/4. The remaining failure was narrower: one G8 run compressed known-state provenance into generic labels.

### Stage 7e v4

Stage 7e v4 made known-state provenance explicit. It required `state_inventory.known_state[]` entries with `state_id`, `fact`, and `evidence_ids`. After retrying one provider timeout and one truncated-output retry, the final evaluation completed 4/4 runs, and all 4/4 passed:

- task_success=1.000
- atom_primary_metric=1.000
- state_accuracy=1.000
- citation_grounding=1.000
- evidence_type_accuracy=1.000
- trace_completeness=1.000
- stage_completion=1.000

This sequence is the clearest evidence for the repair-loop protocol. The low-cost model did not become generally stronger. The harness made the missing obligations explicit, then verified that the model could satisfy them under a fixed macro contract.

## 7. Stage 7-next: Transfer To A Neighboring Macro

Stage 7-next tested whether the Stage 7e v4 obligation set was only a fixture-specific patch. The new macro was an evidence-bound method-plan update. It reused Stage 7e v4 obligations and added one new stressor: the output had to select the next admitted macro, specify admission criteria, preserve local and real-model gates, and declare non-claims.

The local gate passed with 2/2 expectations met:

- golden output passed with task_success=1.000 and atom_primary_metric=1.000;
- known-bad premature broader-workflow expansion failed with task_success=0.000.

The real smoke used the low-cost model only:

```text
Qwen/Qwen3-8B x G8/G9 x 2 repetitions = 4 runs
```

All 4/4 runs executed without provider errors, timeout, or truncated-output retry. All 4/4 runs passed with:

- task_success=1.000
- atom_primary_metric=1.000
- schema_validity=1.000
- citation_grounding=1.000
- state_accuracy=1.000
- evidence_type_accuracy=1.000
- trace_completeness=1.000
- stage_completion=1.000
- context_relevance=1.000

This supports a narrow transfer claim: the Stage 7e v4 obligations can be reused to make the low-cost model complete a closely related fixed method-plan macro with one new explicit stressor.

## 8. Claim Boundary

The strongest supported claim is not that harnesses universally close model gaps. The evidence supports a more precise claim:

> Contract-driven harnesses can externalize specific reliability obligations and enable low-cost models on bounded, contract-critical operations.

Gap compression remains an important but conditional result. It is strongest in structured extraction and present on some contract metrics in mechanism and partial macro tests. It is mixed or undefined in broader project-initialization and research-workflow slices.

The current evidence does not support:

- production readiness;
- full project initialization readiness;
- full research workflow readiness;
- open-ended tool-using workflow execution;
- general equivalence between low-cost and strong models.

The positive result is nevertheless meaningful. The harness converts some failures from opaque model weakness into named, testable engineering obligations. This is the core empirical support for the paper's methodology claim.
