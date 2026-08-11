# Oracle-coupling audit runners

This directory contains the executable side of a bounded causal audit of policy
provenance and state-commit integrity. Fixed inputs live in
`fixtures/oracle-coupling/`; frozen results and manifests live in
`data/reproduction/oracle-coupling/`.

The dependency order is:

1. `failure_to_executable_contract_v2`: authored-oracle mechanism baseline.
2. `oracle_independent_compiler_v1`: public-input positive control.
3. `metamorphic_public_input_v1`: grounded invariance and authority sensitivity.
4. `hardened_state_adapter_v1`: file-backed check-to-commit controls and residuals.
5. `second_harness_audit_v1`: SQLite evaluator and transaction portability.
6. `invariant_external_boundary_v1`: pinned external evaluator boundary control.

`render_discriminating_audit.py` reads only frozen JSON evidence and generates
the PDF, PNG, and SVG under `paper/figures/` plus its source-data record under
`data/analysis/oracle-coupling/`.

After any rerun, verify every frozen component with:

```bash
python code/runners/oracle-coupling/verify_all.py
```

No item in this bundle establishes prevalence, independent task authorship,
unseen-grammar transfer, or universal complete mediation.
