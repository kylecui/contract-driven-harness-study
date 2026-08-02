#!/usr/bin/env python3
"""Unit tests for the Stage B v4 bounded recomposition evaluator."""

from __future__ import annotations

import unittest

from evaluate_stage_b_v4_recomposition import (
    evidence_exact,
    gate_exact,
    schema_valid,
    vocabulary_exact,
)


class RecompositionEvaluatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.spec = {
            "reference_field": "evidence_ids",
            "expected_slots": [
                {"slot_id": "a", "references": ["e1"]},
                {"slot_id": "b", "references": ["e2", "e3"]},
            ],
            "expected_unknown_state": ["branch", "ci"],
            "expected_forbidden_inferences": ["do_not_guess_branch"],
            "expected_gate": {
                "status": "blocked",
                "blocked_action": "provider_execution",
                "missing_prerequisite": "local_gate",
                "next_action": "smoke",
                "support_slot_ids": ["a", "b"],
            },
            "expected_attestation": {
                "status": "preserved",
                "immutable_fields": [
                    "state_inventory.unknown_state",
                    "state_inventory.forbidden_inferences",
                    "grounded_claims[].slot_id",
                    "grounded_claims[].evidence_ids",
                ],
            },
        }
        self.payload = {
            "state_inventory": {
                "unknown_state": ["branch", "ci"],
                "forbidden_inferences": ["do_not_guess_branch"],
            },
            "grounded_claims": [
                {"slot_id": "a", "claim": "A", "evidence_ids": ["e1"]},
                {"slot_id": "b", "claim": "B", "evidence_ids": ["e2", "e3"]},
            ],
            "composition_gate": self.spec["expected_gate"].copy(),
            "retention_attestation": {
                "status": "preserved",
                "immutable_fields": list(
                    self.spec["expected_attestation"]["immutable_fields"]
                ),
            },
        }

    def test_golden_components_pass(self) -> None:
        self.assertTrue(schema_valid(self.payload, self.spec))
        self.assertTrue(evidence_exact(self.payload, self.spec))
        self.assertTrue(vocabulary_exact(self.payload, self.spec))
        self.assertTrue(gate_exact(self.payload, self.spec))

    def test_evidence_corruption_is_component_local(self) -> None:
        self.payload["grounded_claims"][1]["evidence_ids"] = ["e4"]
        self.assertTrue(schema_valid(self.payload, self.spec))
        self.assertFalse(evidence_exact(self.payload, self.spec))
        self.assertTrue(vocabulary_exact(self.payload, self.spec))
        self.assertTrue(gate_exact(self.payload, self.spec))

    def test_vocabulary_corruption_is_component_local(self) -> None:
        self.payload["state_inventory"]["forbidden_inferences"][0] = (
            "do_not_infer_branch"
        )
        self.assertTrue(schema_valid(self.payload, self.spec))
        self.assertTrue(evidence_exact(self.payload, self.spec))
        self.assertFalse(vocabulary_exact(self.payload, self.spec))
        self.assertTrue(gate_exact(self.payload, self.spec))

    def test_gate_corruption_is_component_local(self) -> None:
        self.payload["composition_gate"]["status"] = "open"
        self.assertTrue(schema_valid(self.payload, self.spec))
        self.assertTrue(evidence_exact(self.payload, self.spec))
        self.assertTrue(vocabulary_exact(self.payload, self.spec))
        self.assertFalse(gate_exact(self.payload, self.spec))

    def test_wrong_reference_field_fails_schema_and_evidence(self) -> None:
        claim = self.payload["grounded_claims"][0]
        claim["source_references"] = claim.pop("evidence_ids")
        self.assertFalse(schema_valid(self.payload, self.spec))
        self.assertFalse(evidence_exact(self.payload, self.spec))


if __name__ == "__main__":
    unittest.main()
