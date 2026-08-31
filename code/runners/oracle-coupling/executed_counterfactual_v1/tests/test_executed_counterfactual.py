import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from run_counterfactual import (  # noqa: E402
    FIXTURE_ID,
    REPLACEMENT_DESTINATION,
    build_cases,
)


class ExecutedCounterfactualTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.results = build_cases()

    def test_fixture_and_cases_present(self) -> None:
        self.assertEqual(self.results["fixture_id"], FIXTURE_ID)
        self.assertEqual(len(self.results["cases"]), 5)

    def test_baseline_canonical_writes_expected_destination(self) -> None:
        baseline = self.results["cases"][0]
        self.assertTrue(baseline["accepted"])
        self.assertTrue(baseline["wrote"])
        self.assertEqual(
            baseline["observed_project_status"],
            self.results["interventions"]["target_counterfactual"]["old"],
        )

    def test_target_counterfactual_redirects_accepted_write(self) -> None:
        rejected = self.results["cases"][1]
        adapted = self.results["cases"][2]
        self.assertFalse(rejected["accepted"])
        self.assertIn("wrong_target_state", rejected["reason_codes"])
        self.assertTrue(adapted["accepted"])
        self.assertTrue(adapted["wrote"])
        self.assertEqual(
            adapted["observed_project_status"], REPLACEMENT_DESTINATION
        )

    def test_evidence_counterfactual_requires_distractor(self) -> None:
        rejected = self.results["cases"][3]
        adapted = self.results["cases"][4]
        self.assertFalse(rejected["accepted"])
        self.assertIn("decision_evidence_mismatch", rejected["reason_codes"])
        self.assertTrue(adapted["accepted"])

    def test_overall_passed_flag(self) -> None:
        self.assertTrue(self.results["overall_passed"])


if __name__ == "__main__":
    unittest.main()
