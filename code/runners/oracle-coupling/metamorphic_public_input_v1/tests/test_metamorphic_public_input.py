from __future__ import annotations

import copy
import json
import sys
import unittest
from collections import Counter
from dataclasses import replace
from pathlib import Path
from unittest.mock import patch


EXPERIMENT_ROOT = Path(__file__).resolve().parents[1]
AUDIT_CODE_ROOT = EXPERIMENT_ROOT.parent
REPO_ROOT = AUDIT_CODE_ROOT.parents[2]
OIC_ROOT = AUDIT_CODE_ROOT / "oracle_independent_compiler_v1"
PUBLIC_INPUT_PATH = REPO_ROOT / "data" / "reproduction" / "oracle-coupling" / "oracle_independent_compiler_v1" / "artifacts" / "public_fixtures.json"
sys.path.insert(0, str(OIC_ROOT))
sys.path.insert(0, str(EXPERIMENT_ROOT))

import metamorphic_suite as suite  # noqa: E402
from metamorphic_suite import (  # noqa: E402
    INVARIANT_FUNCTIONS,
    baseline_contract,
    fixture_from_public_record,
    run_suite,
    sensitivity_plan,
)
from public_input import project_public_fixture  # noqa: E402
from run_experiment import BASE_SOURCE_COMMIT, build_manifest  # noqa: E402
from verify_manifest import (  # noqa: E402
    EXPECTED_MANIFEST_PATHS,
    verify_manifest_payload,
)


class MetamorphicPublicInputTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        payload = json.loads(PUBLIC_INPUT_PATH.read_text(encoding="utf-8"))
        cls.fixtures = [fixture_from_public_record(item) for item in payload["fixtures"]]
        cls.results, cls.cases = run_suite(cls.fixtures)
        cls.baseline_objects = {
            item["fixture_id"]: suite.compile_contract(project_public_fixture(item))
            for item in cls.fixtures
        }

    def test_public_input_fixture_count_and_family_coverage(self) -> None:
        self.assertEqual(28, len(self.fixtures))
        self.assertEqual(
            {
                "controlled_state_transition": 10,
                "approval_gated_configuration": 10,
                "approval_gated_communication": 8,
            },
            dict(Counter(item["family"] for item in self.fixtures)),
        )

    def test_each_invariant_transform_changes_every_public_input(self) -> None:
        for fixture in self.fixtures:
            for name, transform in INVARIANT_FUNCTIONS.items():
                transformed = transform(fixture)
                self.assertNotEqual(fixture, transformed.fixture, f"{fixture['fixture_id']}::{name}")

    def test_all_invariant_relations_hold(self) -> None:
        invariant = [item for item in self.cases if item["relation"] == "invariant"]
        self.assertEqual(112, len(invariant))
        self.assertTrue(all(item["input_changed"] for item in invariant))
        self.assertTrue(all(item["raw_grounding_audit"]["passed"] for item in invariant))
        self.assertTrue(all(item["passed"] for item in invariant))

    def test_baseline_apply_subset_is_derived_without_authored_labels(self) -> None:
        counts = Counter(
            (fixture["family"], baseline_contract(fixture)["expected_decision"])
            for fixture in self.fixtures
        )
        self.assertEqual(5, counts[("controlled_state_transition", "apply")])
        self.assertEqual(5, counts[("approval_gated_configuration", "apply")])
        self.assertEqual(3, counts[("approval_gated_communication", "apply")])

    def test_sensitivity_plan_has_family_specific_applicability(self) -> None:
        self.assertEqual(3, len(sensitivity_plan("controlled_state_transition")))
        self.assertEqual(5, len(sensitivity_plan("approval_gated_configuration")))
        self.assertEqual(5, len(sensitivity_plan("approval_gated_communication")))

    def test_all_sensitivity_relations_fail_closed_as_specified(self) -> None:
        sensitivity = [item for item in self.cases if item["relation"] == "sensitivity"]
        self.assertEqual(55, len(sensitivity))
        self.assertTrue(all(item["input_changed"] for item in sensitivity))
        self.assertTrue(all(item["observed_decision"] == "block" for item in sensitivity))
        self.assertTrue(all(item["observed_reason"] == item["expected_reason"] for item in sensitivity))
        self.assertTrue(all(item["raw_grounding_audit"]["passed"] for item in sensitivity))
        self.assertTrue(all(item["fail_closed_execution_audit"]["passed"] for item in sensitivity))
        self.assertTrue(all(item["passed"] for item in sensitivity))

    def test_exact_transformation_counts(self) -> None:
        self.assertEqual({
            "compose_invariant_transforms": 28,
            "expire_authority": 8,
            "insert_irrelevant_evidence": 28,
            "mismatch_authority_scope": 8,
            "mismatch_authority_target": 13,
            "mismatch_authorized_destination": 13,
            "remove_authority": 13,
            "rename_domain_identifiers": 28,
            "rename_evidence_identifiers": 28,
        }, self.results["by_transformation"])

    def test_experiment_reports_clustered_statistical_unit(self) -> None:
        design = self.results["statistical_design"]
        self.assertEqual(28, design["primary_task_level_reporting_unit_n"])
        self.assertEqual(13, design["sensitivity_subset_n"])
        self.assertIn("not independent", design["repeated_measures"])
        self.assertEqual("exact paired deterministic counts; no p values or population interval", design["analysis"])

    def test_suite_passes_with_no_case_failures(self) -> None:
        self.assertTrue(self.results["overall_passed"], self.results["failures"])
        self.assertTrue(self.results["coverage_gate"]["passed"])
        self.assertEqual([], self.results["failures"])
        self.assertEqual(167, self.results["case_count"])

    def test_stale_grounding_mutant_is_killed(self) -> None:
        real_compile = suite.compile_contract
        baselines = self.baseline_objects

        def stale_grounding(public):
            observed = real_compile(public)
            baseline = baselines[public.fixture_id]
            if (
                observed.expected_decision == baseline.expected_decision
                and observed.expected_gate["reason_code"]
                == baseline.expected_gate["reason_code"]
            ):
                return replace(
                    observed,
                    initial_state=baseline.initial_state,
                    desired_patch=baseline.desired_patch,
                    required_preserved_state=baseline.required_preserved_state,
                    required_evidence_ids=baseline.required_evidence_ids,
                )
            return observed

        with patch.object(suite, "compile_contract", side_effect=stale_grounding):
            results, cases = suite.run_suite(self.fixtures)
        self.assertFalse(results["overall_passed"])
        failures = [item for item in cases if not item["passed"]]
        self.assertTrue(any(
            item["transformation"] == "rename_evidence_identifiers"
            and not item["raw_grounding_audit"]["passed"]
            for item in failures
        ))
        self.assertTrue(any(
            item["family"] == "approval_gated_communication"
            and item["transformation"] == "rename_domain_identifiers"
            and not item["raw_grounding_audit"]["passed"]
            for item in failures
        ))

    def test_open_gate_fail_closed_mutant_is_killed(self) -> None:
        real_compile = suite.compile_contract
        baselines = self.baseline_objects

        def open_gate(public):
            observed = real_compile(public)
            baseline = baselines[public.fixture_id]
            if baseline.expected_decision == "apply" and observed.expected_decision == "block":
                return replace(
                    observed,
                    expected_gate={
                        "status": "open",
                        "reason_code": observed.expected_gate["reason_code"],
                        "permitted_action": "apply_patch",
                    },
                    expected_next_action="apply_state_patch",
                    required_preserved_state=(),
                )
            return observed

        with patch.object(suite, "compile_contract", side_effect=open_gate):
            results, cases = suite.run_suite(self.fixtures)
        self.assertFalse(results["overall_passed"])
        sensitivity = [item for item in cases if item["relation"] == "sensitivity"]
        self.assertEqual(55, len(sensitivity))
        self.assertTrue(all(not item["fail_closed_execution_audit"]["passed"] for item in sensitivity))

    def test_all_block_vacuity_and_manifest_mutants_are_killed(self) -> None:
        real_compile = suite.compile_contract
        authority_types = suite.AUTHORITY_TYPE

        def strip_authority(public):
            authority_type = authority_types[public.family]
            stripped = replace(
                public,
                evidence=tuple(
                    item for item in public.evidence if item.get("type") != authority_type
                ),
            )
            return real_compile(stripped)

        with patch.object(suite, "compile_contract", side_effect=strip_authority):
            results, _ = suite.run_suite(self.fixtures)
        self.assertFalse(results["overall_passed"])
        self.assertFalse(results["coverage_gate"]["passed"])
        self.assertEqual(0, results["sensitivity_case_count"])

        baseline = build_manifest(BASE_SOURCE_COMMIT)
        self.assertEqual(17, len(EXPECTED_MANIFEST_PATHS))
        self.assertEqual([], verify_manifest_payload(baseline))

        omitted = copy.deepcopy(baseline)
        omitted_path = omitted["entries"].pop()["path"]
        omitted["entry_count"] = len(omitted["entries"])
        with self.subTest(mutant="manifest_omission"):
            failures = verify_manifest_payload(omitted)
            self.assertIn(f"paths:missing:{omitted_path}", failures)

        duplicate = copy.deepcopy(baseline)
        duplicate["entries"][-1] = copy.deepcopy(duplicate["entries"][0])
        with self.subTest(mutant="manifest_duplicate"):
            self.assertIn("schema:duplicate_path", verify_manifest_payload(duplicate))

        parent_escape = copy.deepcopy(baseline)
        parent_escape["entries"][0]["path"] = "../manifest-escape"
        with self.subTest(mutant="manifest_parent_escape"):
            self.assertIn(
                "path:parent:../manifest-escape",
                verify_manifest_payload(parent_escape),
            )

        absolute = copy.deepcopy(baseline)
        absolute["entries"][0]["path"] = "/tmp/mpiv1-manifest-escape"
        with self.subTest(mutant="manifest_absolute_path"):
            self.assertIn(
                "path:absolute:/tmp/mpiv1-manifest-escape",
                verify_manifest_payload(absolute),
            )

        changed_hash = copy.deepcopy(baseline)
        changed_hash["entries"][0]["sha256"] = "0" * 64
        with self.subTest(mutant="manifest_hash"):
            self.assertTrue(any(
                failure.startswith("sha256:")
                for failure in verify_manifest_payload(changed_hash)
            ))

        changed_bytes = copy.deepcopy(baseline)
        changed_bytes["entries"][0]["bytes"] += 1
        with self.subTest(mutant="manifest_bytes"):
            self.assertTrue(any(
                failure.startswith("bytes:")
                for failure in verify_manifest_payload(changed_bytes)
            ))

        wrong_version = copy.deepcopy(baseline)
        wrong_version["manifest_version"] = "MPIV1"
        with self.subTest(mutant="manifest_version"):
            self.assertIn(
                "schema:manifest_version",
                verify_manifest_payload(wrong_version),
            )


if __name__ == "__main__":
    unittest.main()
