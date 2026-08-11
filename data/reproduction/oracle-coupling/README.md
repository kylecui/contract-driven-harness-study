# Oracle-coupling audit evidence

This directory stores frozen machine-readable inputs, per-case outcomes, and
SHA-256 manifests for the runners in
`code/runners/oracle-coupling/`. The primary task-level unit is one of 28 fixed
fixtures. Candidate actions, metamorphic transformations, and repeated external
evaluator calls are nested deterministic checks rather than independent
statistical samples.

The evidence supports a narrow contrast: the authored-oracle FEC-v2 compiler is
coupled to answer-derived policy fields, whereas the author-developed
public-input compiler and pinned external evaluator exclude score labels at
their tested runtime boundaries while remaining sensitive to declared public
or policy changes.

Only executable experimental inputs, structured results, and integrity metadata
are included.
