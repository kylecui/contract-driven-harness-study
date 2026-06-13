# Security And Systems Peer-Review Intake

Review date: 2026-06-13

Target: frozen v3.1.1 body

Review perspective: network security, systems architecture, agent constraints, and decoupled design

## Overall Decision

The review is directionally strong, but its `Strong Accept` recommendation is more favorable than the current evidence warrants for ASE, ISSTA, or FSE.

The body remains frozen. The review activates a separate evidence-extension track for robustness, run stability, and overhead. Successful results may support a later v4 draft; they will not be inserted silently into v3.1.1.

## Six-Dimension Review

| Dimension | Assessment | Decision |
|---|---|---|
| Novelty | Mechanism atoms and the repair-loop protocol form a coherent engineering contribution, but the final novelty position still depends on the citation pass and closest-work comparison. | Continue citation normalization; do not strengthen novelty wording yet. |
| Soundness | The contract model and local golden/known-bad gates are internally coherent. Deterministic-gate overfitting remains a valid threat. | Add perturbation testing before broader claims. |
| Evaluation | The broad slices are useful, but Stage 7e v4 and Stage 7-next have only four targeted runs each. | Treat current evidence as repair smoke evidence, not population-level stability evidence. |
| Presentation | The frozen v3.1.1 body is clear, bounded, and unusually explicit about non-claims. | No body rewrite. |
| Reproducibility | Fixtures, evaluators, event logs, evidence IDs, and source links are strong. Token usage and exact request cost are not captured by the current adapter. | Extend instrumentation before new paid runs. |
| Ethics And Security | The experiments are bounded and do not demonstrate autonomous network defense. Security-domain applicability is plausible but untested. | Do not add autonomous-defense or production-security claims. |

## Comment Classification And Response

### 1. Small Sample Size And Runtime Variance

Classification: **valid criticism, accepted with design correction**

Four successful runs cannot establish a stable success probability. For 4/4 successes, the two-sided 95% Wilson lower bound is approximately 0.510.

However, repeating one identical fixture 30-50 times would measure provider/run stability, not task generalization. The revision plan combines repetitions with controlled perturbations. If a macro passes 40/40 runs distributed across five predeclared conditions, the corresponding descriptive Wilson lower bound is approximately 0.912.

### 2. Deterministic-Gate Overfitting

Classification: **valid criticism, high priority**

The paper already discloses this threat, but disclosure does not close the evidence gap. The next evaluation will vary field names, evidence order, unknown-state wording, and distractor evidence while preserving the underlying obligation.

The evaluator must distinguish a true semantic failure from a permitted representation variant. Any evaluator ambiguity stops the paid expansion until local golden/known-bad cases are repaired.

### 3. Harness Overhead

Classification: **valid criticism, partially answerable from current artifacts**

Current event logs support prompt-byte, output-byte, latency, timeout, and retry analysis. They do not contain provider-reported prompt/completion token usage or exact per-request cost. The existing `cost_efficiency` metric is a task heuristic and must not be presented as an API billing measurement.

New runs should capture provider usage fields and report:

- prompt and completion tokens;
- median and P90 latency;
- provider failure and retry rate;
- estimated provider cost per attempt;
- estimated provider cost per successful contract pass.

Historical harness-design labor cannot be reconstructed reliably. Future engineering effort should be logged prospectively rather than guessed.

## Scope Corrections

- The review's security and autonomous-defense applications are plausible motivations, not evidence-backed claims of this paper.
- The `Strong Accept` label is reviewer judgment, not a substitute for robustness evidence.
- The paper's current narrow claims remain valid without the new experiments; the new experiments determine whether a stronger venue-facing evaluation is justified.

## Disposition

| Action | Status |
|---|---|
| Keep v3.1.1 body frozen | ACCEPT |
| Complete citation pass | PROCEED |
| Add perturbation and stability evaluation | REQUIRED for stronger venue submission |
| Add measured overhead analysis | REQUIRED for engineering adoption claims |
| Repeat identical fixtures 30-50 times without perturbation | REJECT |
| Add autonomous network-defense claims | REJECT |
