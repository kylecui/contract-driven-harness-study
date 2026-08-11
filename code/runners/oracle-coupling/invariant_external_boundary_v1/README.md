# Invariant external evaluator boundary control v1

## Status

`bounded_complete_external_evaluator_control`

This directory contains a zero-model-call control using the external
[Invariant Guardrails](https://github.com/invariantlabs-ai/invariant) parser and
evaluator at commit `2340fe2d9cd619f73d5b67fa05bf8a08c7cad515`.

It tests a narrow causal property: when a public trace and policy are held fixed,
changing a separate answer-label payload from original to deleted or poisoned must
not alter the policy source, its SHA-256 hash, the external evaluator input, or the
external evaluator decision. Paired one-leaf public-trace edits and paired policy-source
mutations at a fixed public trace must each change the decision in the declared direction.
These controls rule out constant-output behavior and the audited trace-hash lookup mutant.

## Boundary

This is an **external evaluator boundary control**. It is:

- not an external replication of the audited FEC-v2 coupling pattern;
- not independently authored task evidence—the two cases and interventions were
  authored locally;
- not a check-to-commit, tool-execution, rollback, or atomic-enforcement experiment;
- not a prevalence or generalization claim.

The only projected decision is whether Invariant returns at least one policy error:
`violation_detected` or `no_violation_detected`. The experiment does not rename that
result as execution authorization.

## Frozen design

- Official policy 1: the README `Voldemort` / `Tom Riddle` `Message` policy.
- Official policy 2: the README `get_inbox -> send_email` `ToolCall` policy.
- Two locally authored base cases.
- Two official-policy public conditions per case: baseline and one declared one-leaf edit.
- One locally authored, syntactically valid policy-source mutation per case, evaluated
  against the unchanged baseline public trace.
- Three out-of-band answer-label conditions: original, deleted, poisoned.
- Eighteen deterministic `LocalPolicy.from_string(...).analyze(...)` calls.
- Every call runs in a `python -I` child process whose serialized request has exactly
  `policy_source` and `public_trace`; both the worker SHA-256 and the production parent
  dispatcher's function-source SHA-256 are frozen with separate AST/signature closure
  gates. The dispatcher gate requires the exact request dictionary, minimal environment,
  canonical JSON stdin, and `subprocess.run([sys.executable, "-I", ...])` path.
- Zero model calls. The child installs a socket-connect fail guard; this is a scoped
  runtime guard, not a proof covering every possible networking primitive.

Each base case keeps `public_trace` and `score_only_expected_label` as separate
fields. `evaluate_external` accepts only `policy_source` and `public_trace`; answer-label
payloads are excluded from the child request, and the recorded score join occurs after
the child returns. The labels may be constructed in the parent before dispatch, but are
not serialized to the evaluator.

The adversarial tests specifically kill (1) a worker mutant that imports caller-stack
introspection, (2) a parent-level stack-oracle mutant that forges all worker/isolation
metadata, and (3) a mutant that ignores policy source and looks up decisions only by
public-trace SHA-256. This is a bounded gate against those attacks, not a universal
complete-mediation theorem.

## Reproduce

The runner reads the pinned source and dependency locations from
`INVARIANT_SOURCE_ROOT` and `INVARIANT_DEPS_ROOT`. If unset, it uses:

- `/tmp/invariant-2340fe2d`
- `/tmp/invariant-deps-035`

One practical way to rebuild those locations is:

```bash
git clone https://github.com/invariantlabs-ai/invariant.git /tmp/invariant-2340fe2d
git -C /tmp/invariant-2340fe2d checkout --detach \
  2340fe2d9cd619f73d5b67fa05bf8a08c7cad515
python -m pip install --target /tmp/invariant-deps-035 \
  "invariant-ai==0.3.5"
```

The runner then verifies the source commit, source cleanliness, Apache-2.0
license hash, resolved implementation path, and direct package version. These
commands pin the source commit and direct package version but do not hash-lock
transitive wheels or constitute a from-scratch archival environment.

Run with Python 3.11 or newer:

```bash
python -m unittest discover \
  -s code/runners/oracle-coupling/invariant_external_boundary_v1/tests -v
python code/runners/oracle-coupling/invariant_external_boundary_v1/run_experiment.py
python code/runners/oracle-coupling/invariant_external_boundary_v1/verify_manifest.py
```

Run those commands from the repository root.
`external_boundary.py` places the pinned source ahead of the temporary dependency
target on `sys.path` and verifies the resolved `LocalPolicy` implementation path.
On macOS, `/tmp` normally canonicalizes to `/private/tmp`; the source evidence records
the resolved path and checks containment against that canonical snapshot root.

## Artifacts

- `data/reproduction/oracle-coupling/invariant_external_boundary_v1/artifacts/protocol.json`: frozen objective, success criteria, evaluator boundary,
  run matrix, and explicit non-completion states.
- `.../cases.json`: the two base cases and eighteen derived run identifiers.
- `.../run_records.json`: per-run policy source/hash, public trace/hash,
  answer-label payload, evaluator input hash, decision, and post-hoc score.
- `.../results.json`: label-invariance, public-fact sensitivity, fixed-trace
  policy-source sensitivity, coverage gates, test execution, and overall status.
- `.../source_snapshot.json`: source commit/cleanliness, official URLs, license
  hash, upstream file hashes, import resolution, and README line evidence.
- `.../package_versions.json`: Python, platform, source/dependency paths, and
  installed package versions.
- `.../SHA256_MANIFEST.json`: exact 14-path project-relative SHA-256 closure with
  fixed source/license/version/README-policy/worker/dispatcher headers and cross-file
  validation.

## Explicit non-completion states

- `external_defect_replication_not_tested`
- `independent_task_authorship_not_met`
- `check_to_commit_not_tested`
- `generalization_not_established`

If the pinned `/tmp` snapshot or dependency target is absent, reproduction is
`environment_not_reprovisioned`; the frozen artifacts remain inspectable, but a new
execution must not be claimed.
