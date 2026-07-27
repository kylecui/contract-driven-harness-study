# Draft Methodology Sections for Contract-Driven Harness v2.1 WP2

## 3.4 Failure Classification Rule and Obligation×Field Coverage Matrix

### 3.4.1 A Three-Way Classification for Repair-Loop Failures

We classify each observed failure before repairing it, because contract defects, evaluator defects, and model failures have different repair actions and different implications for the claim boundary. The three types are mutually exclusive under the following decision procedure:

1. **Declaration check.** Was the violated obligation explicitly declared in the model-visible contract, and bound to the specific output field where the violation appeared?
   - If no, the failure is a **contract defect**.
2. **Surface-form check.** Was the obligation semantically satisfied, but rejected by the evaluator because of an unstated surface requirement (e.g., JSON formatting, token casing, or enum phrasing)?
   - If yes, the failure is an **evaluator defect**.
3. If the obligation was both declared and correctly checked, and the model still violated it, the failure is a **model failure**.

| Failure type | Definition | Repair action | Claim implication |
|---|---|---|---|
| Contract defect | The obligation was missing, ambiguous, or not visible to the model in the output field where it was violated. | Revise the contract and add a known-bad fixture that captures the missing obligation. | Not evidence of a model limitation. |
| Evaluator defect | The obligation was declared and the model output satisfied it semantically, but the deterministic check rejected a valid surface form. | Revise the evaluator or probe, then re-verify golden and known-bad anchors. | Does not change the model capability claim. |
| Model failure | The obligation was explicitly declared and the evaluator correctly checked it, yet the model still violated it. | Redesign the mechanism (e.g., add a lower harness layer such as JSON-schema-constrained decoding, or reduce scope) or exclude the model. | This is the only class that evidences a model limitation. |

### 3.4.2 Worked Examples

**Contract defect: missing `next_action` enumeration.** In the automated replication by an LLM agent, the initial v1 contract did not enumerate the exact expected values for `next_action` or state the evidence-citation policy in the model-visible gate. Under that contract, Qwen3-8B failed 0/40 controlled state-mutation runs, emitting a natural-language description for `next_action` and omitting the required E1 citation. The failure is a contract defect because the obligations were not explicitly declared. The repair was to add exact enum values and the evidence-citation rule to the contract.

**Evaluator defect: GLM-4-9B probe surface form.** The interchangeability probe contained a minimal-context enum check. GLM-4-9B emitted a bare token rather than a JSON object, while still passing the full frozen protocol 40/40. The probe's contract did not explicitly require JSON output. The output satisfied the semantic obligation but was rejected by an unstated surface rule, so the failure is an evaluator (probe) defect. The repair was to add the JSON-output requirement to the probe; after that change, above-floor anchors passed 8/8 Tier-1 checks and the below-floor anchor still failed all four structural checks.

**Model failure: Qwen2.5-7B structural floor.** Qwen2.5-7B-Instruct failed 0/40 on the unchanged frozen protocol with malformed JSON, dropped fields, and corrupted tokens. The contract required valid JSON and the evaluator checked schema validity, so the obligation was declared and correctly checked. This is a model failure. The repair is to route the model through JSON-schema-constrained decoding or exclude it from the task pool.

### 3.4.3 Obligation×Field Coverage Matrix

A global obligation does not automatically bind every output field. We record coverage in an obligation×field matrix that is part of the fixture schema. For each global obligation, the matrix lists the output fields it governs. Each cell must pass Gate A: the golden output satisfies the obligation at that field, and a known-bad output violates it there. An unmarked cell means the obligation is not asserted for that field, and any failure there is outside the contract scope.

**Worked example: canonical-name coverage from v4 to v5.** In the automated replication, v4 required canonical names for state identifiers. The matrix initially covered `state_inventory`, `transition_record`, and `residual_unknown_state`; those four conditions passed 8/8. Under the unknown-state-paraphrase condition, the model still used the paraphrased alias inside the `attestation` field. The matrix showed that the canonical-name obligation had not been bound to `attestation`. The failure is therefore a contract defect: the obligation was not declared to cover the field where it was violated. The repair was to extend the obligation to `attestation` and add a known-bad fixture that violates canonical naming only there. After the update, v5 passed 40/40 across all five perturbation conditions.

The matrix is scoped to contract-driven harness tasks with fixed output contracts and deterministic evaluators. It does not claim that the same field set generalizes to arbitrary agent outputs.

---

## 3.5 Frozen Protocol Specification

### 3.5.1 Frozen Items

A protocol is *frozen* when every variable that could invalidate a stability or transfer claim is pinned before execution and verified before the first model call. The frozen items are:

1. **Sampling parameters**, specifically `temperature` (set to 0 and recorded).
2. **Provider and model identifier**, including the exact model version snapshot.
3. **Prompt artifacts**, exported before execution and identified by content hashes.
4. **Evaluator version**, including the exact validator or probe code and fixture version.
5. **Known-bad set version**, identifying the set of regression fixtures defining the failure modes the protocol claims to avoid.
6. **Perturbation set version**, identifying the set of designed perturbations used to test stability.

### 3.5.2 Why Each Item Must Be Frozen

| Frozen item | Claim invalidated if the item is not pinned |
|---|---|
| Temperature | A non-zero or changed temperature can alter the sample distribution; the observed pass rate would no longer describe a fixed sampling process. |
| Provider and model version snapshot | Provider routing, model updates, or quantization changes can change behavior; a stability claim becomes unanchored. |
| Prompt hash | Any change to the model-visible prompt changes the task; results are not comparable across runs. |
| Evaluator version | A revised validator can reclassify passing outputs as failures; adherence metrics become uninterpretable. |
| Known-bad set version | Missing or altered regression fixtures change the meaning of "stable" for the repaired failure modes. |
| Perturbation set version | Different perturbations test different robustness boundaries; the claim no longer refers to the same test suite. |

A claim about a protocol is a claim about a specific, reproducible artifact stack. If any item changes, the claim is void unless re-established with a new freeze record.

### 3.5.3 Verification Method

Before each run batch, a pre-flight script computes the SHA-256 hash of each frozen artifact and compares it to the manifest recorded at freeze time. Any mismatch aborts execution or logs a deviation. The script writes the verified hashes, timestamp, and manifest version into the trace log. A frozen-protocol claim is void if the pre-flight check is not recorded.

### 3.5.4 Relation to the V4 Body

The V4 paper pinned provider settings and exported prompt artifacts before execution, but it did not explicitly list `temperature` among the frozen items. The automated replication across two frameworks showed that unpinned sampling parameters make cross-framework comparison impossible. This specification retroactively closes that gap: `temperature = 0` is now a pinned, verified, and logged item for every frozen-protocol claim.

The frozen-protocol artifact list is the basis for the standalone verification specification in `research/04_methods/frozen-protocol-spec-v1.md`.
