# Hardened state adapter v1

This experiment is a minimal standard-library repair for trusted JSON-file
adapter failures. It leaves the FEC-v2 compiler and gate unchanged.

## Question

Can a narrow, auditable state adapter preserve the old JSON state across the
same stale-state, mutable-object, replay, symlink, interrupted-write, and path
confusion attacks while retaining one authorized write path?

## Implemented controls

1. The state file is an envelope containing logical state, a monotonic version,
   and SHA-256 digests of nonces used by accepted apply and block decisions.
2. Each execution reads live state under a sidecar `fcntl.flock`, compares the
   caller's expected version **and exact snapshot hash**, and validates patch
   `from` values against the live state.
3. Candidate input is JSON-normalized exactly once and recursively frozen
   before validation. The caller's original object is not reused.
4. Every path component is checked. User-controlled symlink components fail
   closed; root-owned links below a root-owned non-writable system namespace
   (for example macOS `/var`) are allowed. State and lock files must be
   same-user regular files and are opened with `O_NOFOLLOW` where available.
5. Writes stage canonical JSON in the same directory, `fsync` the temporary
   file, recheck the pre-state hash, call `os.replace`, and `fsync` the parent
   directory.
6. The immediate parent must be owned by the effective user and have no
   group/world write bits. Logical paths must be canonical dot-separated ASCII
   identifiers. Traversal,
   slash aliases, reserved envelope roots, and candidate-supplied adapter
   metadata are rejected.

## Run

```bash
python code/runners/oracle-coupling/hardened_state_adapter_v1/run_experiment.py
```

The runner executes all tests, streams the unittest report to the console, and
writes:

- `data/reproduction/oracle-coupling/hardened_state_adapter_v1/artifacts/hardened_adapter_results.json`: machine-readable per-scenario
  outcomes, runtime, input hashes, and claim boundaries;
- `.../SHA256_MANIFEST.json`: the exact six-file package closure (README,
  adapter, runner, tests, verifier, and results) plus four external inputs: the
  fixture, gate, shared candidate generator, and repository-layout helper.

## Scope boundary

This package produces a **bounded pass with a known residual**, not an
unqualified security pass. It hardens one local JSON-file commit adapter. It
does **not** repair
gold-oracle coupling, derive authority from public evidence, improve model
competence, or establish transfer. The lock is advisory and coordinates only
processes that use the same stable lock inode. Ownership/mode checks reject a
cross-user or writable parent, but a hostile process running as the same user
can still unlink the lock or write in the final hash-check-to-`os.replace`
window; the suite reproduces that residual explicitly. The filesystem must
provide normal same-directory `os.replace` and `fsync` semantics. The injected
interruption occurs before replacement; this is not a power-loss or disk-failure
campaign. A post-replace directory-`fsync` failure is surfaced distinctly as
`CommitOutcomeUnknownError` and requires state/nonce reconciliation before any
retry.
