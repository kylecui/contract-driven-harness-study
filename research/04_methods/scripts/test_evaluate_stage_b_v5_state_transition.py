#!/usr/bin/env python3
"""Unit tests for the Stage B v5 controlled transition evaluator."""

from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from evaluate_stage_b_v5_state_transition import (
    attestation_exact,
    evidence_exact,
    evaluate_manifest,
    gate_exact,
    residual_vocabulary_exact,
    schema_valid,
    transition_exact,
)


class StateTransitionEvaluatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.spec = {
            "reference_field": "evidence_ids",
            "expected_slots": [
                {"slot_id": "a", "references": ["e1"]},
                {"slot_id": "b", "references": ["e2", "e3"]},
            ],
            "expected_known_state": [
                {
                    "state_id": "api_permission",
                    "value": "approved",
                    "evidence_ids": ["e4"],
                }
            ],
            "expected_unknown_state": ["branch", "ci"],
            "expected_forbidden_inferences": [
                "do_not_guess_branch",
                "do_not_guess_ci",
            ],
            "expected_transition_record": {
                "event_id": "event-1",
                "state_id": "api_permission",
                "from_status": "unknown",
                "to_status": "approved",
                "evidence_ids": ["e4"],
                "applied": True,
            },
            "expected_gate": {
                "status": "open",
                "permitted_action": "provider_execution",
                "satisfied_prerequisite": "api_permission",
                "next_action": "smoke",
                "support_slot_ids": ["a", "b"],
            },
            "expected_attestation": {
                "status": "preserved_after_transition",
                "immutable_fields": ["grounded_claims[].evidence_ids"],
            },
        }
        self.payload = {
            "state_inventory": {
                "known_state": copy.deepcopy(self.spec["expected_known_state"]),
                "unknown_state": ["branch", "ci"],
                "forbidden_inferences": [
                    "do_not_guess_branch",
                    "do_not_guess_ci",
                ],
            },
            "grounded_claims": [
                {"slot_id": "a", "claim": "A", "evidence_ids": ["e1"]},
                {"slot_id": "b", "claim": "B", "evidence_ids": ["e2", "e3"]},
            ],
            "transition_record": copy.deepcopy(
                self.spec["expected_transition_record"]
            ),
            "transition_gate": copy.deepcopy(self.spec["expected_gate"]),
            "retention_attestation": copy.deepcopy(
                self.spec["expected_attestation"]
            ),
        }

    def test_golden_components_pass(self) -> None:
        self.assertTrue(schema_valid(self.payload, self.spec))
        self.assertTrue(evidence_exact(self.payload, self.spec))
        self.assertTrue(residual_vocabulary_exact(self.payload, self.spec))
        self.assertTrue(transition_exact(self.payload, self.spec))
        self.assertTrue(gate_exact(self.payload, self.spec))
        self.assertTrue(attestation_exact(self.payload, self.spec))

    def test_evidence_corruption_is_component_local(self) -> None:
        self.payload["grounded_claims"][1]["evidence_ids"] = ["e9"]
        self.assertFalse(evidence_exact(self.payload, self.spec))
        self.assertTrue(residual_vocabulary_exact(self.payload, self.spec))
        self.assertTrue(transition_exact(self.payload, self.spec))

    def test_residual_vocabulary_corruption_is_component_local(self) -> None:
        self.payload["state_inventory"]["unknown_state"].reverse()
        self.assertTrue(evidence_exact(self.payload, self.spec))
        self.assertFalse(residual_vocabulary_exact(self.payload, self.spec))
        self.assertTrue(transition_exact(self.payload, self.spec))

    def test_transition_corruption_is_component_local(self) -> None:
        self.payload["transition_record"]["to_status"] = "denied"
        self.assertTrue(residual_vocabulary_exact(self.payload, self.spec))
        self.assertFalse(transition_exact(self.payload, self.spec))
        self.assertTrue(gate_exact(self.payload, self.spec))

    def test_gate_corruption_is_component_local(self) -> None:
        self.payload["transition_gate"]["status"] = "blocked"
        self.assertTrue(transition_exact(self.payload, self.spec))
        self.assertFalse(gate_exact(self.payload, self.spec))

    def test_attestation_corruption_is_component_local(self) -> None:
        self.payload["retention_attestation"]["immutable_fields"] = []
        self.assertTrue(transition_exact(self.payload, self.spec))
        self.assertTrue(gate_exact(self.payload, self.spec))
        self.assertFalse(attestation_exact(self.payload, self.spec))

    def test_wrong_reference_field_fails_schema_and_evidence(self) -> None:
        claim = self.payload["grounded_claims"][0]
        claim["source_references"] = claim.pop("evidence_ids")
        self.assertFalse(schema_valid(self.payload, self.spec))
        self.assertFalse(evidence_exact(self.payload, self.spec))

    def test_manifest_evaluation_writes_run_metrics(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            fixture_dir = root / "fixture"
            fixture_dir.mkdir()
            (fixture_dir / "evaluation_spec.json").write_text(
                json.dumps(self.spec), encoding="utf-8"
            )
            output_path = root / "output.md"
            output_path.write_text(json.dumps(self.payload), encoding="utf-8")
            validation_path = root / "validation.json"
            metrics_path = root / "metrics.json"
            manifest_path = root / "manifest.json"
            manifest_path.write_text(
                json.dumps(
                    {
                        "runs": [
                            {
                                "run_id": "run-1",
                                "fixture": "fixture",
                                "task_type": "state_transition",
                                "model": "budget_model",
                                "harness_arm": "G9",
                                "paths": {
                                    "output": str(output_path),
                                    "validation_report": str(validation_path),
                                    "metrics": str(metrics_path),
                                },
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            output_json = root / "runs.json"
            output_md = root / "runs.md"
            evaluate_manifest(
                manifest_path=manifest_path,
                fixtures_dir=root,
                output_json=output_json,
                output_md=output_md,
            )
            result = json.loads(output_json.read_text(encoding="utf-8"))
            self.assertTrue(result["runs"][0]["passed"])
            self.assertTrue(validation_path.exists())
            self.assertTrue(metrics_path.exists())


if __name__ == "__main__":
    unittest.main()
