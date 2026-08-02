# Glossary

**Scope**: This glossary covers terms used in the contract-driven-harness paper. Terms are listed in the order a reader encounters them. Each entry includes a one-line definition and, where useful, a contrast with related terms.

---

## Contract stack

The seven contract object types that together specify a bounded agent task:
1. **TaskSpec** — input shape, output shape, allowed operations
2. **MemorySlice** — bounded working memory snapshot
3. **EvidenceBundle** — referenced evidence with slot bindings
4. **OutputContract** — output schema + required fields + forbidden values
5. **WorkflowGate** — stage gate with pass criteria
6. **TraceLog** — event-sourced execution record
7. **Validator** — deterministic evaluator over the output contract

The contract stack is the contribution's central artifact. It is framework-agnostic.

---

## Mechanism atom

The smallest testable unit of agent behavior, defined by: one input contract, one output contract, one known-bad set, and one validator. Atoms are the analog of unit tests for agents. Composition of atoms into macros is gated by both atoms passing local golden/known-bad regression.

Contrast: **Macro** — a composed sequence of atoms admitted only after both atoms pass gates.

---

## Repair-loop

The seven-step development protocol for surfacing and externalizing implicit obligations:
1. Run real model under low-constraint arm; observe failure
2. Isolate the missing obligation
3. Write obligation into the relevant contract
4. Capture the failure as a known-bad fixture
5. Local golden/known-bad regression (Gate A)
6. Real-model targeted slice (Gate B)
7. Admission: update evidence ledger, declare scope, return to backlog

The loop converts implicit task conventions into explicit, testable contract obligations.

Contrast: **Prompt tuning** — undisciplined prompt edits without regression or known-bad capture.

---

## Gate A (local gate)

Deterministic pre-flight gate requiring:
- All golden outputs pass
- All known-bad outputs fail **for the expected reason** (not just any reason)

Gate A is zero-cost (no API calls). Failure of Gate A means the obligation was misidentified.

---

## Gate B (model gate)

Real-model verification gate requiring a targeted slice of model runs to meet a pass threshold. Gate B is more expensive (API calls). Failure of Gate B means the contract's expression is insufficient and another repair-loop iteration is needed.

---

## Known-bad fixture

A test fixture encoding a specific failure mode, with:
- The failing input or output
- The expected reason for failure (which validator should catch it)
- Provenance (which real-model run produced it)

Known-bad must fail for the **expected reason**. A known-bad that fails for an unrelated reason indicates a contract bug, not a model bug.

---

## Golden output

A reference output that satisfies all contract obligations. Used in Gate A to verify the validator does not produce false negatives.

---

## Failure Classification Rule (§3.4)

Three categories of failure, each with a distinct repair action:

| Failure type | Definition | Repair action |
|---|---|---|
| **Contract defect** | Obligation not declared in the model-visible contract | Add obligation to contract |
| **Evaluator defect** | Obligation declared but validator checks it too narrowly | Broaden or rewrite validator |
| **Model failure** | Obligation declared and validator is correct, but model still violates | Repair-loop iteration or model substitution |

Distinguishing these is essential because each demands a different action.

---

## Obligation×Field Coverage Matrix (§3.4)

A checklist ensuring each global obligation (e.g., "use canonical names") explicitly enumerates the output fields it covers (e.g., `residual_state`, `transition_record.added`, `attestation`). Without this matrix, global obligations silently leak through uncovered fields.

---

## Frozen Protocol Specification (§3.5)

A pre-experiment lock on all parameters that could affect result interpretability:
- `temperature` (e.g., 0)
- `provider` (e.g., SiliconFlow)
- `model_version_snapshot` (e.g., `Qwen/Qwen3-8B` as of YYYY-MM-DD)
- `prompt_hash` (SHA256 of the rendered prompt template)
- `evaluator_version` (git commit hash of validator code)
- `known_bad_set_version` (git commit hash of known-bad fixtures)
- `perturbation_set_version` (git commit hash of perturbation definitions)

Each item is hashed and checked at experiment start. Changes invalidate the frozen-protocol claim.

---

## Equivalence Testing (TOST)

Two One-Sided Tests — the correct statistical procedure for claiming "no meaningful difference" between two arms. Contrasts with failing-to-reject on McNemar, which only indicates insufficient power to detect a difference. TOST requires pre-specifying a minimum effect size δ (e.g., 0.10) and rejects the non-equivalence hypothesis if both one-sided tests are significant.

Used in §4.10 cross-framework comparison.

---

## Floor probe

A cheap probe used to determine if a candidate model is above or below the structural capability floor for a task family. Two tiers:

- **Tier-1 structural probe** (≈4 API calls): tests organ-level capabilities (valid JSON, literal copy, field retention, no fabrication). Failure = below floor; do not run full protocol.
- **Tier-2 semantic probe** (≈4 API calls): tests task-specific capabilities (enumeration compliance, canonical-name mapping, order sensitivity). Failure predicts repair-loop workload, not floor status.

Probes are derived from the task family's mechanism atoms. There is no universal floor test.

---

## Model Admission Protocol (§3.7)

Four-tier admission funnel for certifying a candidate model as compatible with a frozen contract:
1. Tier-1 structural probe (≈4 calls) — elimination line
2. Tier-2 semantic probe (≈4 calls) — repair-loop workload predictor
3. Tier-3 smoke (8 canonical runs) — repair-loop entry
4. Tier-4 full gate (5 conditions × 8 repeats = 40 runs) — admission

Total cost for a model that passes: ~$1 + 4-8 hours. Total cost for a model that fails Tier-1: ~$0.01 + seconds.

---

## ContractBench-v1

A task family + evaluator release accompanying this paper. Contains:
- Controlled-state-mutation task definition
- Frozen contract (v5)
- 5 models × 40 runs records
- 10 known-bad fixtures with provenance
- Golden outputs
- Evaluator source

**Scope**: NOT a general agent-reliability benchmark. It is a reproducibility artifact for this paper's experiments. Circular if used to validate the contract it was built from; transparent about this scope.

---

## Framework-agnostic core

A ~320-line Python module implementing the contract stack and validators without importing any agent framework (PEtFiSh, LangChain, LangGraph, etc.). Released as an independent GitHub repository with DOI. Adapters (e.g., 65-line PEtFiSh adapter, 57-line LangChain adapter) wrap the core for specific frameworks.

The framework-agnostic core is the artifact that makes the "contract stack is the contribution, not the framework" claim concrete.

---

## Automated replication (Kimi Agent)

Re-execution of the published protocol by an LLM agent (Kimi Agent by Moonshot AI) using the author's API key. Distinct from **independent replication**, which requires a separate human principal investigator, separate resources, and separate protocol interpretation. All Kimi-produced data in this paper is labeled `automated replication by an LLM agent` and subject to author verification (WP3-前置).

---

## Stage B v5.4 frozen protocol

The specific frozen protocol used for the headline 40/40 stability result:
- Task: controlled state mutation (one unknown→known transition, retain other obligations)
- Contract: v5 (after 4 repair-loop iterations)
- Perturbations: 5 conditions (canonical, field_alias, evidence_order, distractor_evidence, unknown_state_paraphrase) × 8 repeats
- Evaluator: 7 deterministic checks (schema, exact evidence array, residual state, transition accuracy, no inference, complete gate, retention declaration)
- Strict aggregation: AND of all 7 checks

Wilson [0.912, 1.000] on 40 runs.
