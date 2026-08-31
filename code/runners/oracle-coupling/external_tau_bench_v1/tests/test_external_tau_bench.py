import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from run_audit import (  # noqa: E402
    AGENT_WRONG_CITY,
    GOLDEN_CITY,
    POISON_CITY,
    build_cases,
)


class ExternalTauBenchAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.results = build_cases()

    def test_six_cases_present(self) -> None:
        self.assertEqual(len(self.results["cases"]), 6)

    def test_baselines(self) -> None:
        cases = self.results["cases"]
        self.assertEqual(cases["baseline_matching_state"]["reward"], 1.0)
        self.assertEqual(cases["baseline_perturbed_state"]["reward"], 0.0)

    def test_golden_deletion_flips_correct_state(self) -> None:
        self.assertEqual(self.results["cases"]["golden_deletion"]["reward"], 0.0)

    def test_golden_poisoning_moves_policy(self) -> None:
        cases = self.results["cases"]
        self.assertEqual(
            cases["golden_poisoning_city_original_agent"]["reward"], 0.0
        )
        self.assertEqual(
            cases["golden_poisoning_city_matched_agent"]["reward"], 1.0
        )
        self.assertNotEqual(
            cases["golden_poisoning_city_original_agent"]["gt_data_hash"],
            cases["baseline_matching_state"]["gt_data_hash"],
        )

    def test_public_fact_counterfactual_still_passes(self) -> None:
        self.assertEqual(
            self.results["cases"]["public_fact_counterfactual"]["reward"], 1.0
        )

    def test_overall_passed_flag(self) -> None:
        self.assertTrue(self.results["overall_passed"])


if __name__ == "__main__":
    unittest.main()
