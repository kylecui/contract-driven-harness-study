# External Tau-Bench Audit v1

Applies the paired-intervention oracle-coupling protocol to an external
public benchmark: **tau-bench** (sierra-research/tau-bench, MIT). The reward
function `tau_bench/envs/base.py::Env.calculate_reward` derives its
validation target (`gt_data_hash`) by **replaying the golden `task.actions`
field** against a fresh database — the `C = G(P, Y)` signature from the
working paper, now observed in a widely used third-party benchmark.

## Interventions (retail dev task 14)

| Case | Intervention | Expected |
|---|---|---|
| baseline_matching_state | none | reward 1 |
| baseline_perturbed_state | agent writes wrong city | reward 0 |
| golden_deletion | `task.actions = []` | previously-correct state scores 0 (target becomes initial-state hash) |
| golden_poisoning_city | golden `city` → Houston, public facts fixed | same agent state flips 1→0; state matching poisoned golden scores 1; `gt_data_hash` shifts |
| public_fact_counterfactual | another user's city changed in initial DB | matching run still scores 1 (symmetric public-fact response) |

Zero LLM calls: reward is deterministic tool execution + SHA-256 hashing.
Agent states are synthetic replays; this audits the reward function's
dependence structure, not agent behavior.

## Run

```bash
git clone https://github.com/sierra-research/tau-bench tmp/tau-bench
git -C tmp/tau-bench checkout 59a200c6d575d595120f1cb70fea53cef0632f6b
pip install --user litellm pydantic   # tau-bench import requirements

python -m unittest discover \
  -s code/runners/oracle-coupling/external_tau_bench_v1/tests -v

python code/runners/oracle-coupling/external_tau_bench_v1/run_audit.py
python code/runners/oracle-coupling/external_tau_bench_v1/verify_manifest.py
```

The runner fails closed unless the tau-bench working tree HEAD equals the
pinned commit. `TAU_BENCH_ROOT` overrides the source location.

## Evidence boundary

- One external benchmark, one retail task, one golden field class (a
  written literal); the replay signature is structural (all tasks score
  through the same `calculate_reward` path).
- The SHA-256 manifest closes over the audit code and frozen results; the
  tau-bench source is external and pinned by commit recorded in
  `results.json`.
- Related structural observations in tau2-bench are documented publicly
  (official evaluation docs; june.kim audit 2026-08-06; SABER
  arXiv:2512.07850); this module supplies the paired-intervention
  demonstration on the original tau-bench.
