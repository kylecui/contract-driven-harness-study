#!/usr/bin/env python3
"""Unit tests for the Stage B v5.3 protocol checks."""

from __future__ import annotations

import copy
import tempfile
import unittest
from pathlib import Path

from build_stage_b_v53_explicit_transition_delta import write_fixture
from analyze_stage_b_v53_explicit_transition_delta import (
    analyze,
    exact_mcnemar_two_sided,
)
from evaluate_stage_b_v52_evidence_binding_ablation import (
    evidence_exact,
    residual_exact,
    schema_valid,
    transition_exact,
)
from evaluate_stage_b_v5_state_transition import load_json
from evaluate_stage_b_v53_explicit_transition_delta import check_pairs


class TransitionDeltaTests(unittest.TestCase):
    def test_paired_outputs_and_contracts_match(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            write_fixture(root, "postcondition-only", "canonical")
            write_fixture(root, "explicit-delta", "canonical")
            fixtures = sorted(path for path in root.iterdir() if path.is_dir())
            self.assertEqual(check_pairs(fixtures), [])

    def test_delta_exists_only_in_treatment(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            baseline = write_fixture(
                root, "postcondition-only", "canonical"
            )
            treatment = write_fixture(root, "explicit-delta", "canonical")
            baseline_contract = load_json(
                root / baseline / "output_contract.json"
            )
            treatment_contract = load_json(
                root / treatment / "output_contract.json"
            )
            self.assertNotIn(
                "required_transition_delta", baseline_contract
            )
            self.assertIn(
                "required_transition_delta", treatment_contract
            )

    def test_obsolete_forbidden_inference_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            fixture = write_fixture(root, "explicit-delta", "canonical")
            fixture_dir = root / fixture
            spec = load_json(fixture_dir / "evaluation_spec.json")
            golden = load_json(fixture_dir / "golden_output.json")
            bad = copy.deepcopy(golden)
            bad["state_inventory"]["forbidden_inferences"].append(
                "do_not_infer_network_api_approval"
            )
            self.assertTrue(schema_valid(bad, spec))
            self.assertTrue(evidence_exact(bad, spec))
            self.assertFalse(residual_exact(bad, spec))
            self.assertTrue(transition_exact(bad, spec))

    def test_delta_preserves_same_expected_output(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            baseline = write_fixture(
                root, "postcondition-only", "field-alias"
            )
            treatment = write_fixture(
                root, "explicit-delta", "field-alias"
            )
            self.assertEqual(
                load_json(root / baseline / "golden_output.json"),
                load_json(root / treatment / "golden_output.json"),
            )

    def test_analysis_detects_engineering_scale_effect(self) -> None:
        evaluated = {"runs": synthetic_runs(delta_state=15, baseline_state=9)}
        result = analyze(evaluated, synthetic_execution())
        self.assertEqual(
            result["decision"],
            "delta_effect_with_strong_statistical_support",
        )
        self.assertAlmostEqual(
            result["primary_comparison"]["risk_difference"], 0.4
        )

    def test_analysis_marks_robust_but_small_effect_as_mixed(self) -> None:
        evaluated = {"runs": synthetic_runs(delta_state=15, baseline_state=14)}
        result = analyze(evaluated, synthetic_execution())
        self.assertEqual(
            result["decision"],
            "mixed_result",
        )

    def test_exact_mcnemar_uses_discordant_pairs(self) -> None:
        self.assertEqual(exact_mcnemar_two_sided(2, 0), 0.5)
        self.assertEqual(exact_mcnemar_two_sided(0, 0), 1.0)
        self.assertAlmostEqual(exact_mcnemar_two_sided(6, 0), 0.03125)

    def test_analysis_reports_matched_pair_table(self) -> None:
        evaluated = {"runs": synthetic_runs(delta_state=15, baseline_state=13)}
        result = analyze(evaluated, synthetic_execution())
        pairs = result["primary_comparison"]["matched_pairs"]
        self.assertEqual(pairs["treatment_pass_control_fail"], 2)
        self.assertEqual(pairs["treatment_fail_control_pass"], 0)
        self.assertEqual(pairs["discordant_pairs"], 2)
        self.assertEqual(pairs["exact_mcnemar_two_sided_p"], 0.5)
        self.assertEqual(len(pairs["pairs"]), 15)


def synthetic_runs(delta_state: int, baseline_state: int) -> list[dict]:
    runs = []
    for arm, state_successes in [
        ("postcondition_only", baseline_state),
        ("explicit_delta", delta_state),
    ]:
        for index in range(15):
            state_pass = float(index < state_successes)
            metrics = {
                "schema_validity": 1.0,
                "exact_evidence_array_preservation": 1.0,
                "residual_unknown_vocabulary_accuracy": state_pass,
                "state_transition_accuracy": 1.0,
                "transition_gate_accuracy": 1.0,
                "retention_attestation_accuracy": 1.0,
                "controlled_state_mutation_success": state_pass,
            }
            runs.append(
                {
                    "run_id": (
                        f"synthetic-{arm}-{index // 3}"
                        f"__budget_model__G9__r{index % 3 + 1}"
                    ),
                    "protocol_arm": arm,
                    "perturbation_condition": f"cell_{index // 3}",
                    "repetition": index % 3 + 1,
                    "metrics": metrics,
                }
            )
    return runs


def synthetic_execution() -> dict:
    return {
        "results": [
            {
                "status": "executed",
                "error": None,
                "elapsed_ms": 1,
                "retry_lineage": {"attempt": 1},
                "provider_metadata": {
                    "usage": {
                        "prompt_tokens": 1,
                        "completion_tokens": 1,
                        "total_tokens": 2,
                        "raw": {},
                    }
                },
            }
            for _ in range(30)
        ]
    }


if __name__ == "__main__":
    unittest.main()
