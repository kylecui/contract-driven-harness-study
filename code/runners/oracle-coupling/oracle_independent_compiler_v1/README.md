# Public-input compiler positive control v1

This experiment asks a deliberately narrow question: can the frozen
single-transition tasks be compiled without consulting the authored answer?
It implements a separate, pure compiler for the three existing task grammars
and leaves both the upstream source snapshot and the manuscript untouched.

## Task contract

The experiment succeeds only if all of the following hold:

1. The compiler accepts an allowlisted typed input containing the request,
   current state, evidence, and structural policy constraints.
2. The projection excludes `expected_output`, the objective sentence, natural-
   language gate rule, preselected decision-evidence IDs, distractor IDs, and
   any newly injected answer-key aliases.
3. Static analysis finds no label-related tokens, fixture IDs, I/O imports,
   dynamic-code calls, or direct file/environment/network/process access in the
   compiler core and generic family policy catalogue.
4. Deleting or poisoning all excluded fields leaves every compiled contract
   byte-equivalent under canonical serialization.
5. The deliberately answer-coupled reference compiler fails the same deletion
   and poisoning probes as a same-run negative control.
6. Policy-relevant changes to public evidence or the public request change the
   derived decision in the expected direction.
7. The derived contracts reproduce the frozen task-level labels and deterministic
   candidate-corpus classifications.
8. The original upstream checkout remains clean.

A partial pass is not reported as completion. A mismatch, forbidden access,
unsupported grammar, ambiguous editable path, or duplicate evidence identifier
is a blocker and causes a non-zero experiment exit.

## Input boundary

The compiler receives only:

- task ID, split, family, and public request;
- current state and structured evidence;
- editable, immutable, and block-preservation paths;
- unknown-state and forbidden-inference boundaries.

It does **not** receive the authored answer, objective sentence, expected gate
object, expected next action, preselected evidence IDs, distractor IDs, or the
fixture's prose gate rule. `artifacts/public_fixtures.json` materializes this
boundary so it can be inspected independently of the original fixture file.

## Run

From the repository root:

```bash
python -m unittest discover \
  -s code/runners/oracle-coupling/oracle_independent_compiler_v1/tests -v

python code/runners/oracle-coupling/oracle_independent_compiler_v1/run_experiment.py

python code/runners/oracle-coupling/oracle_independent_compiler_v1/verify_manifest.py
```

The run writes:

- `data/reproduction/oracle-coupling/oracle_independent_compiler_v1/artifacts/public_fixtures.json`: scrubbed compiler inputs;
- `.../compiled_contracts.json`: derived contracts;
- `.../counterfactual_results.json`: public-input sensitivity tests;
- `.../results.json`: full test outcomes and claim boundary;
- `.../SHA256_MANIFEST.json`: hashes for code, frozen inputs, and results.

## Statistical unit and interpretation

The primary unit is one authored task fixture (`n = 28`), stratified across
three supported families. The 392 candidate artifacts are deterministic
mutations nested within those tasks; they are mechanism checks, not independent
Bernoulli samples. Results are exact descriptive counts without a population
confidence interval.

This is an **author-developed, post-hoc runtime-input-independence positive control**.
Its implementer had inspected the original fixtures. It can show that direct
runtime answer dependence is unnecessary for these frozen grammars. It cannot
show that the compiler was cognitively independent of tasks inspected during
development, that a new author would specify the same policy, or that the rules
transfer to another harness or unseen grammar. Matching the authored answer also
does not prove that the allowlisted public policy itself is correct, complete,
or normatively justified. Independent authoring and cross-harness prospective
validation remain required before a general claim.

## Frozen result

The completed run on 9 August 2026 passed all 11 unit tests. The primary
task-level result was 28/28 exact derived-contract matches: 13 apply fixtures and
15 block fixtures. Deleting the answer object preserved 28/28 contract hashes;
poisoning the answer object, objective, prose rule, preselected decision-evidence
IDs, and distractor IDs also preserved 28/28. The secondary mutation check
accepted 56/56 valid candidates and rejected 336/336 invalid mutations. All
seven public-input counterfactuals produced their specified blocking reason.

The same-run negative control behaved oppositely: the deliberately coupled
reference compiler failed to compile 28/28 fixtures after answer deletion, and
changing only two answer fields changed 28/28 compiled-contract hashes. Static
scanning covers exactly `public_policy_compiler.py` and `policy_rules.py`; it
found no forbidden answer-label token, fixture ID literal, I/O import, dynamic-
code call, or file/environment/network/process access.

Representative public-input counterfactuals were exact and family-spanning:

- removing authoritative transition evidence from `D-ST-01` changed apply to
  block with `missing_authoritative_evidence`;
- expiring the approval in `D-CFG-01` changed apply to block with
  `approval_expired`;
- changing the approved recipient in `H-COMM-01` changed apply to block with
  `communication_recipient_mismatch`.

The bounded result is therefore mechanistic: within the three implemented,
already-inspected grammars, a compiler can reconstruct the frozen contracts
without runtime access to answer labels. This closes the implementation-missing
blocker for a post-hoc positive control only. It does not close independent
authoring, unseen-family transfer, or cross-harness validation.
