# Contract-Driven Harness v4 — Second-Round Independent Critical Audit

Reviewed: 2026-06-30
Branch: `review/2026-06-internal-audit`
Auditor role: independent, adversarial (anti-sycophancy)
Artifact: `research/06_outputs/contract-driven-harness-arxiv-v4-frozen.md` (frozen 2026-06-15)
Prior reviews read: `contract-driven-harness-v4-quality-review.md` (A grade), `contract-driven-harness-v4-ai-slop-review.md` (PASS)

## 0. Bottom Line

The internal A-grade review is defensible on the narrow question it asked ("does the draft support its bounded stability claim?"). It is **not defensible** as a pre-submission readiness check. The paper carries six classes of weakness that a competent external reviewer will surface and that the existing keyword-based AI-slop scan did not catch. The most damaging is not the writing — it is the statistical design: the two preregistered analyses on Stage B v5.3 were **structurally closed off** by the observed control performance, and this is presented as "missed threshold" rather than as a design flaw.

All headline numbers reproduce (Section 3). The interpretation is where the paper is softest.

## 1. Six-Dimension Scoring

Scale: 0–10. A score of 5 means "a sharp reviewer can credibly argue this invalidates the central claim."

| Dimension | Score | One-line verdict |
|---|---:|---|
| Novelty | 4 | Re-bundling of DSPy / guardrails / schema validators / regression testing under a new label. |
| Soundness | 5 | Numbers compute, but two preregistered tests were structurally underpowered/blocked. |
| Evaluation | 3 | One fixture family, one model, one provider, author-as-evaluator, author-as-adversary. |
| Presentation | 6 | Mostly clean hedging, but residual self-evaluative language and abstract/foreground bias. |
| Reproducibility | 7 | Artifacts and manifests are public; runtime layer (provider, retry policy) is underspecified. |
| Ethics | 7 | No subject-safety risk; main concern is PEtFiSh self-citation and evaluator-side COI. |

Composite read: **Borderline**. Not an A in the sense a top-tier venue uses the letter.

### 1.1 Novelty (4/10)

The paper claims five contributions (lines 40–46). Decomposed honestly:

- "Contract-driven harness engineering" is a relabel of structured prompting + validators + workflow gates + trace requirements. Every component listed in the Table at lines 142–150 exists in production form in DSPy (signatures, modules), Guardrails/Outlines (validators, constrained generation), LangGraph (workflow + state), and OpenAI structured outputs.
- "Mechanism atoms" = unit testing with golden and known-bad fixtures. The admission criteria at lines 172–183 are stricter than typical prompt eval, but they are standard software-engineering regression gates restated for LLM outputs.
- "Repair-loop protocol" (lines 186–196) = observe-fail-isolate-fix-regress-rerun. This is the test-fix cycle in any regression-driven development workflow.
- The only candidate for genuine novelty is the *claim-boundary update step* (step 7: update evidence ledger and non-claims before expanding scope). Even that is close to pre-registration + registered-report discipline.

The related-work table (lines 54–62) is constructed so that every prior family is missing the paper's exact combination. That is a difference-of-combination, not a difference-of-mechanism. A reviewer will say: "What is the smallest unit of this paper that is not already in DSPy + Guardrails + a known-bad test suite?" The honest answer is: the evaluation discipline, which is procedural, not technical.

### 1.2 Soundness (5/10)

Internal arithmetic is correct (verified in Section 3 below). The soundness problem is the **design** that produced those numbers, not their computation. Three load-bearing issues:

1. **The McNemar comparison was uninformative by construction.** With n_disc = 2 discordant pairs, the exact two-sided McNemar p-value has a hard floor of 0.5 (verified: `2 * C(2,2)*0.25 = 0.5`). No effect size, however large, could have reached α = 0.05 in this experiment. The paper writes "little power for small effects" (line 371). The accurate statement is "no power for any effect detectable by this test at conventional α." Once n_disc = 2, the test result is a foregone conclusion; it does not update beliefs about the treatment effect in either direction.
2. **The 0.20 engineering threshold was unreachable in the realized data.** Risk difference 0.20 on n = 15 requires treatment − control ≥ 3 passes. The control arm reached 13/15. The treatment ceiling is 15/15. Maximum achievable difference in the realized experiment = 2. The threshold was therefore unreachable from the moment the control passed its 13th run, regardless of treatment performance. This is a power calculation that should have appeared in the preregistration and did not. The paper concedes "no utility analysis for the cutoff" (line 227); it does not concede that the cutoff was unreachable given the control baseline.
3. **n = 4 smoke runs are promoted into the evidence chain.** Stage 7e v4 (line 308) and Stage 7-next (line 324) each contribute "4/4 targeted smoke" to the "weak-model enablement" claim row in Table 3. The 4/4 Wilson interval is [0.510, 1.000] (verified). A pass rate whose lower bound is a coin flip carries essentially no inferential weight. Listing these alongside Stage B v5.4 in the same claim cell inflates the perceived support.

The claim that survives is narrow and the paper states it narrowly. The soundness deduction is for treating structurally uninformative experiments as if they added evidence rather than as if they consumed runtime.

### 1.3 Evaluation (3/10) — the weakest dimension

This is where an external reviewer will concentrate fire. The convergent constraints:

- **One task family.** The headline 40/40 is one controlled state mutation (network-API-approval unknown → known) with five author-designed perturbations: canonical, field-alias, evidence-order, distractor, unknown-paraphrase. These are cosmetic variations on one fixture, not five tasks. The claim "five perturbation conditions" (abstract, line 14; line 342) foregrounds a number that sounds like breadth and is not.
- **One model.** Qwen3-8B only, for every headline result. DeepSeek-V3.2 appears only in earlier, non-headline slices.
- **One provider.** SiliconFlow for every run. The paper explicitly disclaims a provider-independent claim (line 409), but the abstract does not carry that disclaimer.
- **Author-as-evaluator.** The deterministic evaluators, golden outputs, known-bad outputs, and pass thresholds are all authored by the same party that authored the contracts and the perturbations. The metric `atom_primary_metric` is defined per-atom by the author (line 216). This is a tautology-prone loop: the contract specifies the field, the model fills the field, the evaluator (author) checks the field. A reviewer will frame this as "schema-following under another name."
- **Author-as-adversary.** The five perturbations were designed by the author after iterating the contract through v1 → v4. The contract was tuned until the perturbations passed. This is regression testing against the author's own known-bad set, not OOD evaluation. The paper concedes the suite is "designed" (line 403) but does not concession that the designer and the evaluator are the same agent.
- **No isolation of the active harness component.** G9 vs G0 is a bundle comparison (task spec + memory + evidence + output contract + workflow + trace + validators). Stage B v5.2 isolated only one component (evidence binding) and found no large effect. The paper therefore cannot say which part of G9 is doing the reliability work; it can only say the bundle beats nothing.
- **No second task family to test transfer.** Stage 7-next is claimed as "narrow transfer" (line 326). It is the same author reusing the same obligations on a neighboring macro they also designed. That is reuse, not transfer.

### 1.4 Presentation (6/10)

The hedging discipline is real and mostly consistent. The deducts are specific:

- **Self-evaluative superlatives the AI-slop scan missed.** The keyword scan checked `robust / novel / comprehensive / effective`. It did not check evaluative self-assessment phrases, which are the actual residue:
  - "The strongest evidence in this study comes from the repair loop" (line 30)
  - "strongest in structured extraction" (lines 240, 375, 427)
  - "The clearest positive gap-compression result" (line 262); "clearest compression result" (line 375)
  - "Stage B adds an important qualification" (line 371)
  - "The main methodological contribution is" (line 187)
  - "The practical value is the repair loop" (line 429)
  - "The more useful question is" (line 377)

  These are not hollow authority claims, but they are authorial verdicts on the author's own evidence. A neutral reviewer reads "the strongest evidence" as lobbying.
- **Abstract/foreground bias.** The abstract leads with "40/40 … 95% Wilson interval [0.912, 1.000]" and buries "one frozen protocol, model, provider" in the second paragraph. The 40/40 is one task; the abstract does not say so until line 14's tail clause. A reader who reads only the abstract will overestimate the breadth.
- **Passive voice masking agency.** "were treated as an execution deviation rather than a model-quality score" (line 294), "was treated as an execution deviation" (reused) — passive constructions that hide the author's decision to drop a failing run from the quality accounting. The decision may be defensible; the passive hides that it was a decision.
- **"Can" as hedge that is also a claim.** "They can raise the usable floor" (line 36), "low-cost models can satisfy bounded tasks" (line 367). Modal "can" is technically bounded (existence) but reads as a general capability statement. The boundary is in surrounding sentences, not in the verb.

### 1.5 Reproducibility (7/10)

Above average. Public repo, evidence ledger, prompt manifests, per-run artifact directories, deterministic evaluator scripts, and a four-step reviewer audit recipe (lines 482–489). The README reproducer path is concrete. The deducts:

- **Retry policy is underspecified.** Lines 30, 272, 308 reference retries ("after retry", "after documented timeout recovery", "retrying one provider timeout and one truncated-output retry"). The stopping rule is not stated: retry until success? fixed N retries? The reader cannot compute how many total provider calls were made, only that the final state had zero provider errors. This matters because the smoke-test passes are conditioned on reaching a valid output, which introduces survivorship into the pass counts.
- **Provider-side state is not controlled.** Line 407 concedes the study "does not control provider-side batching, hardware, or service changes." A re-run on a different SiliconFlow deployment may not reproduce. The paper says this; it does not say how a reviewer should weight it.
- **Fisher value retained but not reported.** Line 225 states Fisher's exact was the preregistered primary test, switched post-hoc to McNemar (more appropriate for paired data), with Fisher "retained in the audit record." The Fisher value is not reported in the paper body. A reader cannot judge whether the switch was benign. This is a transparency gap even if the switch is methodologically correct.

### 1.6 Ethics (7/10)

No human-subject or safety-critical-deployment risk. The two ethics-adjacent concerns:

- **Self-citation / evaluator-side conflict of interest.** The experimental setting is the author's own PEtFiSh ecosystem (line 96). The fixtures, skills, and macros are the author's. The paper says PEtFiSh "should be read as the implementation context" (line 413). That disclaimer is necessary but not sufficient: the evaluator, the perturbation designer, the contract author, and the ecosystem owner are the same party. This is not financial COI but it is methodological COI and should be stated as such.
- **No dual-use or harm assessment is needed** for this task class; the non-claims list (Appendix A) handles production-readiness boundary honestly.

---

## 2. The Seven Most Attackable Weaknesses

Ordered by likely reviewer impact, not by severity in the abstract.

### W1. N = 1 task family presented as a stability result
**Attack.** "You have 40 runs of one controlled state mutation with five cosmetic perturbations. That is N = 1 task, not N = 40 independent observations. The Wilson interval [0.912, 1.000] is a repeated-run rate on one fixture, not a stability estimate over a protocol class. Calling this 'controlled-transition stability' generalizes from a single instance."
**Current defense strength.** Moderate. The paper does state "one frozen protocol" (line 242) and "pooled interval describes repeated success under the frozen fixture family; it is not a population estimate over agent tasks" (line 405). The claim is correctly bounded in the body.
**Why the defense still leaks.** The abstract, Table 3, and Conclusion foreground "40/40 across five perturbation conditions" without the N = 1 caveat in the same sentence. A reviewer who reads only the abstract and Section 4.8 will miss the fixture-family caveat.
**Hardening.** Add one sentence in the abstract: "five perturbations of one controlled state mutation." Replace "stability" with "repeated-run pass rate on one frozen protocol" in the claim row of Table 3.

### W2. Both preregistered v5.3 analyses were structurally uninformative
**Attack.** "The McNemar test has a floor p = 0.5 at n_disc = 2; it cannot reject any null at α = 0.05. The 0.20 risk-difference threshold requires ≥ 3 pass difference; the control reached 13/15, so the maximum achievable difference was 2 and the threshold was unreachable in this experiment. Your two primary outcome analyses were decided by the design, not by the data. The 'mixed' framing understates this: the experiment was incapable of producing the preregistered positive result once the control performed as it did."
**Current defense strength.** Weak. The paper says "little power for small effects" (line 371) and "no utility analysis for the cutoff" (line 227). Neither concedes the structural floor.
**Why the defense leaks.** "Little power" implies the test was weak but still informative. It was not informative. The minimum achievable p-value is 0.5; the result is fully determined by n_disc, independent of the direction or size of any true effect.
**Hardening.** State explicitly: "With n_disc = 2, the exact McNemar p-value is bounded below at 0.5; the test could not have rejected the null at α = 0.05 for any realized outcome." Add: "The 0.20 threshold was unreachable in the realized experiment because the control arm achieved 13/15, capping the achievable difference at 2/15 = 0.133." Then either (a) preregister a larger n for the next iteration, or (b) reframe v5.3 as a pilot that motivates v5.4, not as a standalone causal comparison.

### W3. harnessed-weak vs unharnessed-strong is an apples-to-oranges confound
**Attack.** "Section 4.3 reports 'low-cost model + G9 showed task_success advantage of +0.743' over 'strong model + G0' (line 274). This compares a harnessed arm against an unharnessed arm. The advantage is the harness, not the model. Presenting this as weak-model enablement invites the inference that the weak model became competitive with the strong model, when the data only show that adding a harness beats not adding one."
**Current defense strength.** Moderate. The paper does not literally say "weak beats strong"; it reports the arithmetic difference and labels it "contract-critical metrics."
**Why the defense leaks.** The framing "weak-model enablement" + the +0.743 number in the same sentence will be read as a head-to-head model comparison. The honest comparison (weak + G9 vs strong + G9) is not reported and would likely erase the advantage.
**Hardening.** Report weak + G9 vs strong + G9 on the same atoms. If that is not available, strike the +0.743-vs-strong framing and report only weak + G0 vs weak + G9, which is the clean within-model harness effect.

### W4. n = 4 smoke tests elevated to evidence
**Attack.** "Stage 7e v4 and Stage 7-next each report 4/4 targeted smoke runs (lines 308, 324). The 4/4 Wilson interval is [0.510, 1.000]. A lower bound of 0.51 carries no inferential information. Listing these in the 'weak-model enablement' claim row alongside Stage B v5.4 (which has real n) inflates the perceived evidence base."
**Current defense strength.** Weak. The paper labels them "targeted smoke" but still lists them as evidence cells in Table 3 and Table 4.
**Why the defense leaks.** The label "smoke" is doing all the boundary work; the table placement is doing all the rhetorical work.
**Hardening.** Separate "exploratory smoke" from "confirmatory runs" in a dedicated table column. State that smoke runs do not enter any claim that is reported with a Wilson interval.

### W5. Author-as-evaluator and author-as-adversary
**Attack.** "The contracts, the golden outputs, the known-bad outputs, the perturbations, the deterministic evaluators, and the per-atom primary metric are all authored by the paper's authors. The contract is tuned through v1 → v4 until the author-designed perturbations pass against the author-written evaluator. This is a regression test of the author's own specification, not evidence of model reliability."
**Current defense strength.** Weak. The paper concedes the suite is "designed" (line 403) and that the evaluator can overfit (line 402). It does not address the shared-authorship problem.
**Why the defense leaks.** "Designed" and "can overfit" are general admissions. The specific problem is that the same agent controls both sides of the spec/check loop, which makes the pass count a measure of self-consistency, not of model capability.
**Hardening.** Add a third-party perturbation set (held-out, authored by someone who did not write the contract). Report the pass rate on that set as a separate row. If unavailable, state this as a non-claim and as the first item of future work.

### W6. Survivorship from retry-until-valid on provider timeouts
**Attack.** "Stage 7e v4 'passed 4/4 targeted smoke runs after retry' (line 308). Stage 6 'completed 48/48 after documented timeout recovery' (line 272). A8R low-cost G8 'was treated as an execution deviation rather than a model-quality score' (line 294) because it repeatedly timed out. The retry stopping rule is not stated. Pass counts are conditioned on reaching a valid output, so a run that the model could not complete is excluded from the denominator. The reported pass rates are upper bounds."
**Current defense strength.** Moderate for v5.3 / v5.4 (zero retries, line 407). Weak for the earlier stages that feed the repair-loop narrative.
**Why the defense leaks.** The repair-loop story (Section 3.6, 4.6) is the methodological contribution. If the repair-loop evidence is itself subject to retry survivorship, the contribution's empirical anchor is softer than stated.
**Hardening.** State the retry stopping rule explicitly. Report denominators as "total calls" and "valid outputs" separately for every stage with a retry. Explain the A8R exclusion with a sensitivity check (does the weak-model-enablement claim survive if A8R is scored as a fail?).

### W7. Hypothesis downgrade reads as reverse HARKing
**Attack.** "The project began with a gap-compression hypothesis (line 26). Compression failed or was undefined on project-init and research-workflow. The thesis then shifted to 'weak-model enablement' (line 36), which is the residue of the original hypothesis after removing the slices where it failed. The framing is transparent, but the result is a hypothesis that is constructed to be unfalsifiable by the slices you have."
**Current defense strength.** Moderate-to-strong. The paper is unusually explicit about the downgrade (lines 26, 36, 373–377).
**Why the defense leaks.** Transparency about a downgrade does not make the downgraded hypothesis as informative as the original. "Weak-model enablement on bounded contract-critical operations" is defined post-hoc by the set of operations where the model passed.
**Hardening.** Pre-register the next task family before running it. Define "bounded contract-critical operation" with criteria that do not reference the observed pass set.

### Optional W8. Compression-ratio metric is unbounded and hard to interpret
**Attack.** "Schema-validity compression in project init is reported as −1.333 (line 264). The metric `(baseline − arm)/baseline` is unbounded below and asymmetric around zero. A reviewer cannot compare −1.333 to +1.000 on the same scale. Why not report absolute gaps with confidence intervals instead of a ratio that breaks when the baseline is small?"
**Current defense strength.** The paper does handle baseline = 0 correctly (reports n/a, line 262). It does not defend the ratio definition.
**Why the defense leaks.** The metric choice makes negative results look like large-magnitude numbers, which can read as either dramatic failure or dramatic reversal depending on the reader's intuition.
**Hardening.** Replace the ratio column with absolute gaps and a sign. Keep the ratio only as a secondary display.

---

## 3. Independent Statistical Re-Verification

All five numbers the audit was asked to check reproduce exactly. Interpretation is the soft spot, not arithmetic.

| Quantity | Paper value | Independent recompute | Match | Interpretation note |
|---|---|---|---|---|
| 40/40 Wilson 95% CI | [0.912, 1.000] | [0.912, 1.000] | ✓ | Lower bound 0.912 means up to 8.8% residual failure rate cannot be ruled out. Decent, not airtight. |
| 8/8 per-condition Wilson 95% CI | [0.676, 1.000] | [0.676, 1.000] | ✓ | Lower bound 0.676 is wide. Per-condition intervals are individually uninformative; only the pooled interval carries weight. |
| McNemar exact, b = 2, c = 0 | p = 0.500 | p = 0.500 | ✓ | **Floor effect**: at n_disc = 2 the minimum possible two-sided p is 0.5. Test was uninformative by construction, not by outcome. |
| Risk difference (15/15 vs 13/15) | 0.133 | 0.133 | ✓ | Correct. But: threshold 0.20 × 15 = 3.0 → requires ≥ 3 pass difference. Control = 13 caps achievable diff at 2. Threshold was unreachable in the realized experiment. |
| Engineering threshold 0.20 | "≥ 3 additional passes" | 3.0 passes | ✓ | Correctly stated. Not power-derived; the paper concedes this (line 227). Does not concede the unreachability given control = 13/15. |

Cross-checks that also reproduce:
- v5.2 risk difference (15/15 vs 14/15) = 0.067 ✓ (line 336)
- Compression ratio project-init schema validity (0.250 → 0.583) = −1.332 ✓ (line 264). Metric is unbounded below; see W8.
- Token totals: 83,312 + 19,672 = 102,984 ✓ (lines 355, 417). Reading "for 40 G9 runs" as total, per-run ≈ 2,575 tokens. Paper does not state total-vs-per-run explicitly; clarify.
- 4/4 Wilson 95% CI = [0.510, 1.000] (used in W4; not reported in paper but should be).

---

## 4. Over-Claim and Boundary-Softness Map

These are passages that read as stronger than the bounded claim technically permits, even after the existing hedging.

| Location | Phrase | Risk |
|---|---|---|
| Abstract, line 12 | "harnessing improves absolute contract adherence" | Present-tense general verb before the boundary clause. Reads as universal. |
| Abstract, line 14 | "Qwen3-8B … passed 40/40 … across five perturbation conditions" | Omits "of one controlled state mutation." Foregrounds breadth number that is cosmetic. |
| Line 30 | "The strongest evidence in this study comes from the repair loop" | Authorial verdict on own evidence; sets the reader's emphasis. |
| Line 233 | "The results support a bounded version of the original hypothesis" | "Support" is doing real work given that compression was undefined/negative on two of three slices. |
| Line 274 | "low-cost model + G9 showed task_success advantage of +0.743" over strong + G0 | Confound (harness vs no-harness). See W3. |
| Line 298, 326 | "This supports the … hypothesis" / "This supports a narrow transfer claim" | "Support" with n = 4 or n = 8 smoke data. |
| Line 326 | "narrow transfer claim" | Reuse of own obligations on own neighboring macro. Not transfer in the usual sense. |
| Line 367 | "low-cost models can satisfy bounded tasks that were unstable under weaker or broader prompts" | "Can" is existence-bounded but reads as general capability. |
| Line 429 | "The practical value is the repair loop" | Authorial verdict; lobbying language. |

Pattern: the verbs are hedged, the nouns are not. "Supports", "can", "shows" are bounded; "strongest", "clearest", "practical value" are not. A reviewer who scans verbs will find the paper disciplined; a reviewer who scans evaluative nouns will find it self-promoting.

---

## 5. AI-Slop / Rhetorical-Softness Residue

The existing AI-slop review (`contract-driven-harness-v4-ai-slop-review.md`) scanned four keywords (`robust / novel / comprehensive / effective`) and passed the paper. That scan is too narrow. It missed the residue class that actually exists in this draft: **authorial self-evaluation rather than hollow authority**.

Residue found (with line numbers):

- Line 30: "The strongest evidence in this study comes from the repair loop"
- Lines 240, 375, 427: "strongest in structured extraction" (used three times)
- Lines 262, 375: "clearest positive gap-compression result" / "clearest compression result"
- Line 371: "Stage B adds an important qualification"
- Line 187: "The main methodological contribution is the repair-loop protocol"
- Line 377: "The more useful question is"
- Line 381: "Several negative or partial results carry real information"
- Line 429: "The practical value is the repair loop"
- Line 96: "a useful experimental setting for studying harness design"
- Line 369: "These are not just weaker answers" (rhetorical contrast structure)

None of these are hollow-authority slop ("in today's rapidly evolving …"). All are evaluative self-assessment. They are the harder class to catch because each is individually defensible; the pattern is the issue. A neutral rewriter would convert "the strongest evidence is X" to "the evidence for X is N runs at rate R with interval I" and let the reader rank.

Reverse-AI-slop signal: the paper also over-hedges in places, which is a different flavor of the same problem. "It establishes neither equivalence nor the absence of a modest benefit" (line 371) is technically correct but syntactically dense enough that a reader may miss that the test was structurally uninformative (W2). Over-hedging can obscure as effectively as under-hedging.

---

## 6. Realistic Venue Expectations

Assuming the body is not materially expanded beyond v4, and assuming a competent but not hostile reviewer:

| Venue class | Likely outcome | Dominant reason |
|---|---|---|
| ICML / NeurIPS main track | **Reject** | Single fixture, single model, underpowered stats, novelty-as-rebundle. Will not clear the bar as an empirical methods paper. |
| ACL / EMNLP main track (NLP methodology framing) | **Weak Reject to Borderline** | The repair-loop protocol is methodologically interesting but the evaluation surface (N = 1 task) is below NLP-methods norms. |
| ACL / EMNLP system demonstrations or industry track | **Weak Accept possible** | The reproducibility package and the engineering discipline are above the bar for a systems/demo track. |
| ICSE / FSE / ASE (software engineering for ML) | **Weak Accept possible** | The regression-test framing maps cleanly to SE norms; the deterministic evaluator story is a fit. |
| ARR-with-resubmission (any *ACL sub) | **Borderline, revise and resubmit** | Will receive "needs more task families, second model, power analysis." |
| Workshop (e.g., on agent evaluation, reliable LLM systems) | **Accept** | The bounded claim and the repair-loop narrative are workshop-appropriate. |

The honest internal expectation is: this is a **solid workshop paper and a borderline-to-reject main-conference paper**. The internal A-grade reads as the grade for "does the draft meet its own stated boundary," not as the grade for "will a top-tier program committee accept this."

---

## 7. Minimum Changes to Move One Tier

Ordered by return-on-effort, highest first. None require new provider calls except the first.

1. **Add the structural-power admission to Section 4.8 and 5.1.** Two sentences: n_disc = 2 caps McNemar p at 0.5; control = 13/15 caps achievable risk difference at 0.133. Cost: one paragraph, zero new runs. This is the single highest-leverage change because it converts W2 from a hidden flaw into a stated boundary, which is the difference between "caught by reviewer" and "conceded by author."
2. **Reframe the abstract.** "five perturbations of one controlled state mutation" instead of "five perturbation conditions." Strike "strongest evidence" from line 30. Cost: three lines of text.
3. **Separate exploratory smoke from confirmatory runs in Tables 3 and 4.** Add a column or split the table. Cost: table edit.
4. **Report the Fisher value retained in the audit record.** One number, one sentence. Cost: zero new runs.
5. **State the retry stopping rule and report total calls vs valid outputs for every stage that retried.** Cost: recomputation from existing logs.
6. **Add a held-out third-party perturbation set for one atom.** Cost: one external collaborator + one round of runs. This is the change most likely to convert the evaluation score from 3 to 5.
7. **Add a second model on the headline protocol.** Cost: 40 more provider calls. Converts the single-model objection.
8. **Add a second task family.** Cost: design + 40+ runs. Converts the N = 1 objection. Largest cost, largest novelty gain.

Items 1–5 are text/log changes and should be done before any resubmission regardless of venue. Items 6–8 are the empirical lifts that move the paper from borderline to weak-accept at a main track.

---

## 8. What This Audit Did Not Find

To avoid manufacturing criticism:

- No arithmetic error was found in any headline statistic. All five audited numbers reproduce exactly.
- No claim in the body exceeds what the evidence supports *if the boundary clauses are read literally*. The problem is foreground/background emphasis, not false statements.
- No fabricated data, no misattributed citation, no missing evidence ID was found. Appendix C traceability is internally consistent.
- No hollow-authority slop ("comprehensive", "robust", etc.) was found. The AI-slop review's keyword pass is correct on its narrow scope; this audit’s objection is that the scope was too narrow.
- The repair-loop protocol as a *methodological proposal* is coherent and arguably useful. The objection is to its empirical support, not its conceptual content.

The paper is honest. It is also weaker than its internal grade suggests, because the internal grade was given for honesty rather than for strength of evidence.

---

## 9. Final Rating

**Borderline.**

- As an internal evidence-extension draft that freezes a bounded stability claim: acceptable. The existing A-grade stands for that purpose.
- As a submission to a top-tier ML/NLP main track: **Weak Reject** on current evidence, with a clear revision path (Section 7, items 6–8).
- As a submission to a workshop, demo track, or SE-for-ML venue: **Weak Accept** with the text-only changes in Section 7 items 1–5.

The difference between "A" and "Borderline" is the difference between "does this draft say what you proved?" (yes) and "is what you proved enough for the venue you are targeting?" (not yet for the top tier).

The single most important action before any external submission is to write the two-sentence structural-power admission (Section 7, item 1). It is free, and it removes the strongest attack a reviewer has.
