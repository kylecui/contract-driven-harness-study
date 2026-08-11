# Metamorphic public-input audit v1

This deterministic experiment asks whether the public-input compiler responds
to semantics rather than incidental identifiers, irrelevant evidence, or
unregistered metadata. It consumes only the scrubbed public-input artifact
produced by `oracle_independent_compiler_v1`; the original authored fixture file
is not a runtime input to this experiment.

## Design

Four invariant transformations are applied to every one of the 28 public-input
fixtures:

1. bijective renaming of domain identifiers while preserving match and mismatch
   relations;
2. bijective renaming of evidence identifiers, including references embedded in
   revocation claims;
3. insertion of one evidence record whose type has no registered authority;
4. a composition of domain renaming, evidence-ID renaming, irrelevant evidence,
   and unregistered metadata.

An invariant case passes only when the public input changes, the normalized
compiled contract remains exactly equal to the baseline contract, and the raw
contract is grounded in transformed identifiers. Referenced renamed evidence
IDs must appear in raw bindings and patches, old IDs must be absent, and every
raw evidence reference must exist in the transformed input. Communication
contracts must carry the transformed recipient in both initial and preserved
state. Controlled-transition and configuration targets are not emitted by the
contract schema; their raw audit therefore checks absence of stale values but
does not invent an output field.

Sensitivity probes are applied to the 13 fixtures whose public facts compile to
`apply`. Every family is tested by removing authority, changing the authority's
target or recipient, and changing the authorized destination. Configuration and
communication fixtures additionally receive scope-mismatch and expiry probes.
A sensitivity case passes only when it changes the public input and produces a
complete fail-closed execution projection: `decision=block`, an empty patch, a
blocked gate, `permitted_action=none`, the transformation-specified reason and
family-specific next action, exact preservation of every declared on-block
path, unchanged policy boundaries, and evidence bindings that reference only
records still present in the transformed input.

## Experimental unit

The primary task-level reporting unit is one frozen public-input task fixture
(`n = 28`; 10 controlled transitions, 10 configuration tasks, and 8
communication tasks). These author-developed fixtures are not claimed to be a random
or independent population sample. The 112 invariant cases are four paired repeated
conditions nested within those 28 tasks. The 55 sensitivity cases are three or
five paired conditions nested within 13 baseline-apply tasks. These 167 derived
cases are not independent Bernoulli samples. The report therefore uses exact
finite-suite counts and no p values or population confidence interval.

The composed condition is a stress composition of three primitive transforms
plus irrelevant metadata, not a fourth independent mechanism. A frozen
coverage gate requires the exact 28-task family profile, the 5/5/3 baseline
apply profile, all 112 invariant cases, all 55 sensitivity cases, and every
declared family-by-relation cell. Thus an all-block compiler cannot pass through
an empty sensitivity set. The runner also executes and binds all 12 unit and
mutant-killing tests before reporting overall success.

The transformations, order, inclusion rule, and evaluation rule are fixed and
deterministic. There is no randomization, exclusion, or missing-data handling.

## Run

From the repository root:

```bash
python -m unittest discover \
  -s code/runners/oracle-coupling/metamorphic_public_input_v1/tests -v

python code/runners/oracle-coupling/metamorphic_public_input_v1/run_experiment.py

python code/runners/oracle-coupling/metamorphic_public_input_v1/verify_manifest.py
```

The run writes a recorded post-hoc protocol, all per-case hashes and outcomes,
an aggregate result, and a SHA-256 manifest under
`data/reproduction/oracle-coupling/metamorphic_public_input_v1/`. It is not a
preregistration or pre-result commitment. Scientific
counts and outcomes are deterministic, but generated timestamps mean regenerated
JSON files are not claimed to be byte-identical across runs.

## Interpretation boundary

This is an author-developed, post-hoc metamorphic mechanism test over three known
grammars. It is not an independent-author experiment, a held-out grammar test,
or cross-harness external validation. It supports a narrow runtime claim:
within the finite scrubbed suite, incidental identifier changes and irrelevant
records were invariant, whereas policy-relevant changes to authority failed
closed as specified. It does not establish that the compiler was cognitively
independent during development or that its policy premises are normatively
correct. External validation, independent authoring, and unseen-grammar transfer
remain incomplete.

The sensitivity direction is authority removal or corruption from baseline
`apply` to `block`. Minimal repair from baseline `block` to `apply` and
selective-recovery tests are not included, so these results support necessary
fail-closed behavior rather than sufficiency of repair.
