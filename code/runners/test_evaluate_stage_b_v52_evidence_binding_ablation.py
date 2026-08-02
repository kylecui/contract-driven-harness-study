#!/usr/bin/env python3
"""Unit tests for the Stage B v5.2 ablation evaluator."""

from __future__ import annotations

import copy
import unittest

from evaluate_stage_b_v52_evidence_binding_ablation import (
    attestation_exact,
    evidence_exact,
    gate_exact,
    residual_exact,
    schema_valid,
    transition_exact,
)


def base_spec(section: str) -> dict:
    return {
        "evidence_section": section,
        "reference_field": "evidence_ids",
        "expected_payload": [
            {"slot_id": "a", "references": ["e1"]},
            {"slot_id": "b", "references": ["e2", "e3"]},
        ],
        "expected_known_state": [
            {
                "state_id": "permission",
                "value": "approved",
                "evidence_ids": ["e4"],
            }
        ],
        "expected_unknown_state": ["branch", "ci"],
        "expected_forbidden_inferences": ["no_branch", "no_ci"],
        "expected_transition_record": {
            "event_id": "event",
            "state_id": "permission",
            "from_status": "unknown",
            "to_status": "approved",
            "evidence_ids": ["e4"],
            "applied": True,
        },
        "expected_gate": {
            "status": "open",
            "permitted_action": "provider_execution",
            "satisfied_prerequisite": "permission",
            "next_action": "complete",
            "support_slot_ids": ["a", "b"],
        },
        "expected_attestation": {
            "status": "preserved_after_transition",
            "immutable_fields": [f"{section}[].evidence_ids"],
        },
    }


def payload(section: str) -> dict:
    evidence = [
        {"slot_id": "a", "evidence_ids": ["e1"]},
        {"slot_id": "b", "evidence_ids": ["e2", "e3"]},
    ]
    if section == "grounded_claims":
        evidence[0]["claim"] = "A"
        evidence[1]["claim"] = "B"
        evidence = [
            {
                "slot_id": item["slot_id"],
                "claim": item["claim"],
                "evidence_ids": item["evidence_ids"],
            }
            for item in evidence
        ]
    spec = base_spec(section)
    return {
        "state_inventory": {
            "known_state": copy.deepcopy(spec["expected_known_state"]),
            "unknown_state": ["branch", "ci"],
            "forbidden_inferences": ["no_branch", "no_ci"],
        },
        section: evidence,
        "transition_record": copy.deepcopy(spec["expected_transition_record"]),
        "transition_gate": copy.deepcopy(spec["expected_gate"]),
        "retention_attestation": copy.deepcopy(spec["expected_attestation"]),
    }


class AblationEvaluatorTests(unittest.TestCase):
    def test_both_representations_pass(self) -> None:
        for section in ["grounded_claims", "evidence_bindings"]:
            spec = base_spec(section)
            data = payload(section)
            self.assertTrue(schema_valid(data, spec))
            self.assertTrue(evidence_exact(data, spec))
            self.assertTrue(residual_exact(data, spec))
            self.assertTrue(transition_exact(data, spec))
            self.assertTrue(gate_exact(data, spec))
            self.assertTrue(attestation_exact(data, spec))

    def test_claim_prose_is_editable(self) -> None:
        spec = base_spec("grounded_claims")
        data = payload("grounded_claims")
        data["grounded_claims"][0]["claim"] = "Rewritten but non-empty"
        self.assertTrue(schema_valid(data, spec))
        self.assertTrue(evidence_exact(data, spec))

    def test_evidence_omission_is_local(self) -> None:
        spec = base_spec("evidence_bindings")
        data = payload("evidence_bindings")
        data["evidence_bindings"][1]["evidence_ids"] = ["e2"]
        self.assertFalse(evidence_exact(data, spec))
        self.assertTrue(transition_exact(data, spec))
        self.assertTrue(gate_exact(data, spec))

    def test_wrong_next_action_is_local(self) -> None:
        spec = base_spec("grounded_claims")
        data = payload("grounded_claims")
        data["transition_gate"]["next_action"] = "wait"
        self.assertTrue(schema_valid(data, spec))
        self.assertFalse(gate_exact(data, spec))
        self.assertTrue(evidence_exact(data, spec))

    def test_wrong_reference_field_fails_schema_and_evidence(self) -> None:
        spec = base_spec("evidence_bindings")
        data = payload("evidence_bindings")
        item = data["evidence_bindings"][0]
        item["source_references"] = item.pop("evidence_ids")
        self.assertFalse(schema_valid(data, spec))
        self.assertFalse(evidence_exact(data, spec))

    def test_static_copy_fails_state_transition_and_gate(self) -> None:
        spec = base_spec("evidence_bindings")
        data = payload("evidence_bindings")
        data["state_inventory"]["known_state"] = []
        data["state_inventory"]["unknown_state"].append("permission")
        data["transition_record"]["to_status"] = "unknown"
        data["transition_gate"]["status"] = "blocked"
        self.assertFalse(residual_exact(data, spec))
        self.assertFalse(transition_exact(data, spec))
        self.assertFalse(gate_exact(data, spec))


if __name__ == "__main__":
    unittest.main()
