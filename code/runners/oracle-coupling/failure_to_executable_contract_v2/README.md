# Failure-to-Executable-Contract v2

This experiment moves the guarantee from model output to a deterministic pre-execution gate. The model is an untrusted proposer. The only state-changing write point is reachable after an executable contract accepts the candidate.

## What is implemented now

- 28 frozen tasks: 4 discovery fixtures, 16 held-out-by-template fixtures in two seen families, and 8 family-held-out communication fixtures.
- 392 deterministic candidate artifacts: 56 valid/metamorphic and 336 known-bad mutations.
- Four enforcement baselines: no enforcement, schema-only, deny-all, and executable contract.
- Reversible file-backed sandbox execution with before/after state hashes.
- Unit tests for valid acceptance, mutation rejection, write confinement, and state integrity.

## Run

```bash
python -m unittest discover \
  -s code/runners/oracle-coupling/failure_to_executable_contract_v2/tests -v

python code/runners/oracle-coupling/failure_to_executable_contract_v2/run_offline_verification.py \
  --fixtures fixtures/oracle-coupling/failure_to_executable_contract_v2.json \
  --output-dir data/reproduction/oracle-coupling/failure_to_executable_contract_v2

python code/runners/oracle-coupling/failure_to_executable_contract_v2/build_artifact_manifest.py
python code/runners/oracle-coupling/failure_to_executable_contract_v2/verify_manifest.py
```

## Evidence boundary

The current result is **authored-oracle mechanism verification**, not independent authorization or an LLM comparison. Perfect finite-corpus safety/utility is expected of a gate that agrees with its authored oracle and must not be generalized beyond the enumerated mutations. A separate counterfactual audit showed that the compiler imports six authorization fields from `expected_output`; the 28/392 result is therefore retained as oracle-consistency evidence only.

Current non-completion states:

- `independent_author_set_missing`
- `unseen_grammar_transfer_missing`
- `external_validation_missing`

The post-hoc public-input compiler is implemented separately in
`code/runners/oracle-coupling/oracle_independent_compiler_v1/`. It reproduces
this finite corpus without runtime access to answer-bearing fields, but it was
developed after the three grammars were known and therefore does
not close the independence or transfer states above.
