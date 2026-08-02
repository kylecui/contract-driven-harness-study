# Stage7r.1 A7R1 Input: Rejection Trace Completeness

Choose exactly one claim option for the paper contribution statement.

Options:
- `C1`: Harness universally closes the performance gap between strong and weak models.
- `C2`: Harness improves absolute contract adherence and enables weak models on mechanism-bound tasks.
- `C3`: Harness mainly improves prose style.

Evidence:
- `atom-a7r1-e01`: Weak-model G8/G9 task success improved from 0.000 to 0.667 in Stage7p v2 composition retention.
- `atom-a7r1-e02`: Gap compression was observed in some metrics but is not universal across all tasks.
- `atom-a7r1-e03`: No evaluation measured prose style.

Rules:
- Select exactly one option ID.
- Every rejected option must be represented as an object with `option_id`, `reason`, and `evidence_ids`.
- The decision trace must include at least one evidence-linked step for the selected option and one evidence-linked step for every rejected option.
- Reject universal claims unless evidence covers all tested task classes.
- Reject claims about unmeasured outcomes.
