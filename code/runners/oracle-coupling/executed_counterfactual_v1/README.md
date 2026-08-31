# Executed Counterfactual v1

Execution-level mechanism witnesses for the answer-field dependence of the
coupled FEC-v2 gate, regenerating the two counterfactuals described in the
oracle-coupling working paper (§3.2/§4.1, Supplementary Note 1) from frozen
repository inputs:

1. **Target counterfactual** — change only the answer-derived destination
   (`expected_output.state_patch[0].to`). The previously canonical proposal
   is rejected (`wrong_target_state`); a proposal writing the replacement
   destination is accepted and the sandbox write lands on the replacement
   value.
2. **Evidence counterfactual** — change only the answer-derived decision
   evidence binding. The canonical binding is rejected
   (`decision_evidence_mismatch`); a distractor-record binding is accepted.

Both use fixture `D-ST-01` only. They are mechanism witnesses that the
compile-time answer dependence reaches the write point — not task samples,
no prevalence, repair-direction, or cross-grammar claims.

## Run

```bash
python -m unittest discover \
  -s code/runners/oracle-coupling/executed_counterfactual_v1/tests -v

python code/runners/oracle-coupling/executed_counterfactual_v1/run_counterfactual.py
python code/runners/oracle-coupling/executed_counterfactual_v1/verify_manifest.py
```

## Evidence boundary

- Inputs: frozen FEC-v2 fixture file, frozen candidate corpus, the coupled
  `contract_gate.py` (unchanged, hash-ledgered by this module and by the
  FEC-v2 manifest).
- Outputs: `results.json` (five cases + checks) and a SHA-256 manifest.
- The runner is deterministic and offline; no model calls.
