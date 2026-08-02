#!/usr/bin/env python3
"""Unit tests for the Stage B v5.4 stability analysis."""

from __future__ import annotations

import unittest

from analyze_stage_b_v54_delta_stability import analyze, render_markdown


COMPONENTS = [
    "schema_validity",
    "exact_evidence_array_preservation",
    "residual_unknown_vocabulary_accuracy",
    "state_transition_accuracy",
    "transition_gate_accuracy",
    "retention_attestation_accuracy",
    "controlled_state_mutation_success",
]


def synthetic_runs(strict_successes: int = 40) -> list[dict]:
    runs = []
    conditions = [
        "canonical",
        "field_alias",
        "evidence_order_shuffled",
        "distractor_evidence",
        "unknown_state_paraphrase",
    ]
    for index in range(40):
        passed = float(index < strict_successes)
        metrics = {component: 1.0 for component in COMPONENTS}
        if not passed:
            metrics["residual_unknown_vocabulary_accuracy"] = 0.0
            metrics["controlled_state_mutation_success"] = 0.0
        runs.append(
            {
                "perturbation_condition": conditions[index // 8],
                "metrics": metrics,
            }
        )
    return runs


def synthetic_execution(count: int = 40) -> dict:
    return {
        "results": [
            {
                "status": "executed",
                "error": None,
                "elapsed_ms": 100 + index,
                "retry_lineage": {"attempt": 1},
                "provider_metadata": {
                    "usage": {
                        "prompt_tokens": 10,
                        "completion_tokens": 5,
                        "total_tokens": 15,
                    }
                },
            }
            for index in range(count)
        ]
    }


class StabilityAnalysisTests(unittest.TestCase):
    def test_perfect_matrix_confirms_bounded_stability(self) -> None:
        result = analyze(
            {"runs": synthetic_runs()},
            synthetic_execution(),
        )
        self.assertEqual(result["decision"], "bounded_stability_confirmed")
        self.assertTrue(all(result["hypotheses"].values()))
        for summary in result["condition_summary"].values():
            strict = summary["components"]["controlled_state_mutation_success"]
            self.assertEqual(strict["wilson_95"], [0.675584, 1.0])
        rendered = render_markdown(result)
        self.assertIn("[0.676, 1.000]", rendered)

    def test_below_strict_threshold_does_not_confirm(self) -> None:
        result = analyze(
            {"runs": synthetic_runs(strict_successes=37)},
            synthetic_execution(),
        )
        self.assertEqual(result["decision"], "stability_not_confirmed")
        self.assertFalse(result["hypotheses"]["H1_absolute_stability"])

    def test_condition_floor_is_enforced(self) -> None:
        runs = synthetic_runs()
        for index in (0, 1):
            runs[index]["metrics"]["controlled_state_mutation_success"] = 0.0
            runs[index]["metrics"]["residual_unknown_vocabulary_accuracy"] = 0.0
        result = analyze({"runs": runs}, synthetic_execution())
        self.assertEqual(result["decision"], "stability_not_confirmed")
        self.assertFalse(result["hypotheses"]["H1_absolute_stability"])

    def test_incomplete_matrix_cannot_confirm(self) -> None:
        runs = synthetic_runs()[:-1]
        result = analyze({"runs": runs}, synthetic_execution(count=39))
        self.assertEqual(result["decision"], "stability_not_confirmed")
        self.assertFalse(result["hypotheses"]["H3_execution_integrity"])

    def test_semantic_retry_blocks_execution_integrity(self) -> None:
        execution = synthetic_execution()
        execution["results"][0]["retry_lineage"]["attempt"] = 2
        result = analyze({"runs": synthetic_runs()}, execution)
        self.assertEqual(result["decision"], "mixed_stability")
        self.assertFalse(result["hypotheses"]["H3_execution_integrity"])


if __name__ == "__main__":
    unittest.main()
