# Second harness/backend audit v1

This experiment asks whether the finite FEC-v2 result survives a distinct
execution backend. It ports the compiled rules and state transition to a local
SQLite evaluator with transactional commit semantics.

## Independence criterion

A second model SDK, CLI, or framework wrapper is not a second harness when it
reuses the same authorization oracle and state write point. The backend is
assessed separately on four axes:

1. model-call path;
2. rule evaluator;
3. state representation and commit path;
4. task/policy authoring.

SQLite is independent on axes 2 and 3.  This offline audit makes no model call,
and the policy is derived from the same authored fixtures, so axes 1 and 4 are
not established.

The scientific status is **second-backend portability**, not external-harness
validation. The same authored task package and author-developed positive-control
compiler remain upstream of the SQL backend.

## What is tested

- The backend consumes contracts frozen by the separate
  `oracle_independent_compiler_v1` positive control. That compiler's allowlisted
  input excludes `expected_output`, preselected decision evidence, prose gate
  rules, and other label-bearing fields.
- A relational SQL evaluator replays the 392 frozen candidates.
- Editable `from` values and every declared preserved value are checked against
  live state inside the transaction.
- Replay, external live-state drift, single-writer contention, explicit
  rollback, and a symlink-path residual are characterised.

All six state-characterisation probes reuse the first applicable fixture,
`D-ST-01`. They are mechanism checks over one base case, not six independent
task samples. Corpus parity is assessed separately across all 392 candidates.

The upstream compiler is bounded to three known fixture families and one
editable path, and it was developed with knowledge of the benchmark.
Consequently, matching the authored outputs remains portability evidence, not
blind replication or external validation.

## Run

```bash
python code/runners/oracle-coupling/second_harness_audit_v1/run_audit.py

python -m unittest discover \
  -s code/runners/oracle-coupling/second_harness_audit_v1/tests -v

python code/runners/oracle-coupling/second_harness_audit_v1/verify_manifest.py
```

Primary outputs are written under
`data/reproduction/oracle-coupling/second_harness_audit_v1/artifacts/`.
