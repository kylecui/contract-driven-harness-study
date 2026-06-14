#!/usr/bin/env python3
"""Unit tests for Stage B v4 exact-retention evaluator primitives."""

from __future__ import annotations

import unittest

from evaluate_stage_b_v4_atoms import (
    closed_vocab_exact,
    closed_vocab_schema_valid,
    evidence_arrays_exact,
    evidence_schema_valid,
)


class EvidenceArrayTests(unittest.TestCase):
    def setUp(self) -> None:
        self.payload = {
            "grounded_claims": [
                {
                    "slot_id": "a",
                    "claim": "A",
                    "evidence_ids": ["e1"],
                },
                {
                    "slot_id": "b",
                    "claim": "B",
                    "evidence_ids": ["e2", "e3"],
                },
            ],
            "immutability_check": {
                "status": "preserved",
                "immutable_fields": ["slot_id", "evidence_ids"],
            },
        }
        self.slots = [
            {"slot_id": "a", "references": ["e1"]},
            {"slot_id": "b", "references": ["e2", "e3"]},
        ]

    def test_exact_payload_passes(self) -> None:
        self.assertTrue(evidence_schema_valid(self.payload, "evidence_ids"))
        self.assertTrue(
            evidence_arrays_exact(
                self.payload,
                reference_field="evidence_ids",
                expected_slots=self.slots,
            )
        )

    def test_order_change_is_schema_valid_but_not_exact(self) -> None:
        self.payload["grounded_claims"][1]["evidence_ids"] = ["e3", "e2"]
        self.assertTrue(evidence_schema_valid(self.payload, "evidence_ids"))
        self.assertFalse(
            evidence_arrays_exact(
                self.payload,
                reference_field="evidence_ids",
                expected_slots=self.slots,
            )
        )

    def test_field_fallback_fails_schema(self) -> None:
        claim = self.payload["grounded_claims"][0]
        claim["source_references"] = claim.pop("evidence_ids")
        self.assertFalse(evidence_schema_valid(self.payload, "evidence_ids"))


class ClosedVocabularyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.unknown = ["branch", "ci", "network"]
        self.forbidden = ["do_not_guess_branch", "do_not_guess_ci"]
        self.payload = {
            "state_inventory": {
                "unknown_state": list(self.unknown),
                "forbidden_inferences": list(self.forbidden),
            },
            "retention_status": "preserved",
        }

    def test_exact_payload_passes(self) -> None:
        self.assertTrue(closed_vocab_schema_valid(self.payload))
        self.assertTrue(
            closed_vocab_exact(
                self.payload,
                expected_unknown_state=self.unknown,
                expected_forbidden_inferences=self.forbidden,
            )
        )

    def test_prefix_substitution_is_schema_valid_but_not_exact(self) -> None:
        self.payload["state_inventory"]["forbidden_inferences"][0] = (
            "do_not_infer_branch"
        )
        self.assertTrue(closed_vocab_schema_valid(self.payload))
        self.assertFalse(
            closed_vocab_exact(
                self.payload,
                expected_unknown_state=self.unknown,
                expected_forbidden_inferences=self.forbidden,
            )
        )

    def test_extra_value_is_not_exact(self) -> None:
        self.payload["state_inventory"]["unknown_state"].append("region")
        self.assertFalse(
            closed_vocab_exact(
                self.payload,
                expected_unknown_state=self.unknown,
                expected_forbidden_inferences=self.forbidden,
            )
        )


if __name__ == "__main__":
    unittest.main()
