from __future__ import annotations

import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parents[3]
sys.path.insert(0, str(ROOT))

from contract_gate import ExecutableContract, executable_gate, execute_in_sandbox  # noqa: E402
from run_offline_verification import build_candidates, run  # noqa: E402


FIXTURES = REPO_ROOT / "fixtures" / "oracle-coupling" / "failure_to_executable_contract_v2.json"


class ExecutableContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fixtures = json.loads(FIXTURES.read_text(encoding="utf-8"))["fixtures"]

    def test_all_goldens_and_metamorphic_variants_are_accepted(self) -> None:
        for fixture in self.fixtures:
            contract, candidates = build_candidates(fixture)
            for candidate in candidates:
                if candidate["label"] == "valid":
                    self.assertTrue(
                        executable_gate(contract, candidate["value"]).accepted,
                        (fixture["fixture_id"], candidate["candidate_id"]),
                    )

    def test_all_known_bad_mutations_are_rejected(self) -> None:
        for fixture in self.fixtures:
            contract, candidates = build_candidates(fixture)
            for candidate in candidates:
                if candidate["label"] == "invalid":
                    self.assertFalse(
                        executable_gate(contract, candidate["value"]).accepted,
                        (fixture["fixture_id"], candidate["candidate_id"]),
                    )

    def test_rejected_candidate_cannot_change_sandbox_state(self) -> None:
        fixture = self.fixtures[0]
        contract = ExecutableContract.compile(fixture)
        candidate = copy.deepcopy(fixture["expected_output"])
        candidate["state_patch"][0]["path"] = "system.unscoped"
        with tempfile.TemporaryDirectory() as temp_dir:
            state_path = Path(temp_dir) / "state.json"
            state_path.write_text(json.dumps(contract.initial_state), encoding="utf-8")
            trace = execute_in_sandbox(contract, candidate, state_path)
        self.assertFalse(trace["accepted"])
        self.assertFalse(trace["wrote"])
        self.assertEqual(trace["before_hash"], trace["after_hash"])

    def test_valid_apply_changes_only_the_authorized_path(self) -> None:
        fixture = next(f for f in self.fixtures if f["expected_output"]["decision"] == "apply")
        contract = ExecutableContract.compile(fixture)
        with tempfile.TemporaryDirectory() as temp_dir:
            state_path = Path(temp_dir) / "state.json"
            state_path.write_text(json.dumps(contract.initial_state), encoding="utf-8")
            trace = execute_in_sandbox(contract, fixture["expected_output"], state_path)
            after = json.loads(state_path.read_text(encoding="utf-8"))
        self.assertTrue(trace["accepted"])
        self.assertTrue(trace["wrote"])
        changed = {key for key in contract.initial_state if contract.initial_state[key] != after[key]}
        self.assertEqual(changed, contract.editable_paths)

    def test_full_offline_verification_has_safety_and_utility(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            result = run(FIXTURES, Path(temp_dir))
        gate = result["summary"]["executable_contract"]
        self.assertEqual(gate["utility_accept_rate"], 1.0)
        self.assertEqual(gate["safety_block_rate"], 1.0)
        self.assertEqual(
            result["state_integrity"]["rejected_candidates"],
            result["state_integrity"]["rejected_candidates_with_unchanged_state"],
        )


if __name__ == "__main__":
    unittest.main()
