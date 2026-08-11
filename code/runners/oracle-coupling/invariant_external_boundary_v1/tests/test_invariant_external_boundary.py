#!/usr/bin/env python3
"""Acceptance and adversarial tests for the external-boundary control."""

from __future__ import annotations

import copy
import hashlib
import inspect
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


EXPERIMENT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(EXPERIMENT_ROOT))

import external_boundary as eb  # noqa: E402
import verify_manifest as vm  # noqa: E402


class InvariantExternalBoundaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.definitions = eb.load_case_definitions()
        cls.results, cls.runs = eb.run_suite(cls.definitions)

    def _run(
        self,
        base_case_id: str,
        policy_condition: str,
        public_condition: str,
        label_condition: str = "original",
    ) -> dict:
        return next(
            run
            for run in self.runs
            if run["base_case_id"] == base_case_id
            and run["policy_condition"] == policy_condition
            and run["public_condition"] == public_condition
            and run["label_condition"] == label_condition
        )

    def _manifest_fixture(self, root: Path) -> dict:
        for relative_text in vm.EXPECTED_RELATIVE_PATHS:
            path = root / relative_text
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(f"fixture:{relative_text}\n", encoding="utf-8")

        fixture_code_root = root / vm.CODE_RELATIVE_ROOT
        fixture_data_root = root / vm.DATA_RELATIVE_ROOT
        fixture_case_path = root / vm.CASE_DEFINITIONS_RELATIVE_PATH
        shutil.copyfile(eb.CASE_DEFINITIONS_PATH, fixture_case_path)
        shutil.copyfile(
            eb.ISOLATED_WORKER_PATH,
            fixture_code_root / "isolated_evaluator.py",
        )
        definitions = eb.load_case_definitions()

        artifacts = {
            "source_snapshot.json": {
                "source_commit": vm.EXPECTED_SOURCE_COMMIT,
                "repository_url": vm.EXPECTED_REPOSITORY_URL,
                "observed_origin_url": f"{vm.EXPECTED_REPOSITORY_URL}.git",
                "license_url": vm.EXPECTED_LICENSE_URL,
                "license_spdx": vm.EXPECTED_LICENSE_SPDX,
                "license_sha256": vm.EXPECTED_LICENSE_SHA256,
                "readme_sha256": vm.EXPECTED_README_SHA256,
                "pyproject_sha256": vm.EXPECTED_PYPROJECT_SHA256,
                "upstream_policy_evidence": vm.EXPECTED_POLICY_EVIDENCE,
                "isolated_worker": {
                    "worker_sha256": vm.EXPECTED_ISOLATED_WORKER_SHA256
                },
                "production_dispatcher": {
                    "dispatcher_source_sha256": (
                        vm.EXPECTED_DISPATCHER_SOURCE_SHA256
                    ),
                    "passed": True,
                },
            },
            "package_versions.json": {
                "packages": {"invariant-ai": vm.EXPECTED_INVARIANT_PACKAGE_VERSION}
            },
            "protocol.json": {
                "protocol_id": vm.PROTOCOL_ID,
                "external_evaluator_boundary": {
                    "dispatcher_source_sha256": (
                        vm.EXPECTED_DISPATCHER_SOURCE_SHA256
                    )
                },
            },
            "cases.json": {
                "protocol_id": vm.PROTOCOL_ID,
                "source_case_definitions_sha256": (
                    vm.EXPECTED_CASE_DEFINITIONS_SHA256
                ),
                "base_cases": definitions["base_cases"],
            },
            "results.json": {
                "protocol_id": vm.PROTOCOL_ID,
                "schema_version": "IEBV1-results-2",
                "source_commit": vm.EXPECTED_SOURCE_COMMIT,
                "source_license_sha256": vm.EXPECTED_LICENSE_SHA256,
                "production_dispatcher": {
                    "dispatcher_source_sha256": (
                        vm.EXPECTED_DISPATCHER_SOURCE_SHA256
                    ),
                    "passed": True,
                },
            },
            "run_records.json": {
                "protocol_id": vm.PROTOCOL_ID,
                "runs": [
                    {"isolated_worker_sha256": vm.EXPECTED_ISOLATED_WORKER_SHA256}
                    for _ in range(18)
                ],
            },
        }
        for name, payload in artifacts.items():
            (fixture_data_root / "artifacts" / name).write_text(
                json.dumps(payload, ensure_ascii=False) + "\n", encoding="utf-8"
            )
        return vm.build_manifest_payload(root)

    @staticmethod
    def _rehash_manifest_entries(manifest: dict) -> None:
        manifest["entries_root_sha256"] = hashlib.sha256(
            vm.canonical_json(manifest["entries"]).encode("utf-8")
        ).hexdigest()

    def test_case_schema_separates_public_trace_policy_and_score_label(self) -> None:
        for case in self.definitions["base_cases"]:
            self.assertIn("public_trace", case)
            self.assertIn("score_only_expected_label", case)
            self.assertIn("paired_policy_source_mutation", case)
            self.assertNotIn("expected_label", eb.canonical_json(case["public_trace"]))
            mutation = case["paired_policy_source_mutation"]
            self.assertEqual(mutation["fixed_public_trace_ref"], "public_trace")
            self.assertNotEqual(
                mutation["policy_source"], eb.POLICIES[case["policy_id"]]["policy_source"]
            )

    def test_upstream_policy_sources_and_correct_readme_spans(self) -> None:
        observed = eb.validate_upstream_environment()
        self.assertEqual(
            observed["upstream_policy_evidence"], vm.EXPECTED_POLICY_EVIDENCE
        )

    def test_message_policy_expected_public_pair(self) -> None:
        baseline = self._run(
            "readme-message-policy", "official_upstream_policy", "baseline_public_trace"
        )
        edited = self._run(
            "readme-message-policy", "official_upstream_policy", "paired_public_fact_edit"
        )
        self.assertEqual(baseline["decision"], "no_violation_detected")
        self.assertEqual(edited["decision"], "violation_detected")

    def test_tool_policy_expected_public_pair(self) -> None:
        baseline = self._run(
            "readme-tool-chain-policy",
            "official_upstream_policy",
            "baseline_public_trace",
        )
        edited = self._run(
            "readme-tool-chain-policy",
            "official_upstream_policy",
            "paired_public_fact_edit",
        )
        self.assertEqual(baseline["decision"], "violation_detected")
        self.assertEqual(edited["decision"], "no_violation_detected")

    def test_policy_source_mutations_change_both_decision_directions(self) -> None:
        directions = {
            (
                relation["pair_checks"][0]["official_decision"],
                relation["pair_checks"][0]["mutated_decision"],
            )
            for relation in self.results["policy_source_relations"]
        }
        self.assertEqual(
            directions,
            {
                ("no_violation_detected", "violation_detected"),
                ("violation_detected", "no_violation_detected"),
            },
        )
        self.assertTrue(
            all(relation["passed"] for relation in self.results["policy_source_relations"])
        )

    def test_evaluator_interface_and_worker_closure_are_narrow(self) -> None:
        self.assertEqual(
            list(inspect.signature(eb.evaluate_external).parameters),
            ["policy_source", "public_trace"],
        )
        closure = eb.validate_isolated_worker_source()
        self.assertTrue(all(closure["checks"].values()))
        self.assertEqual(closure["worker_sha256"], vm.EXPECTED_ISOLATED_WORKER_SHA256)

    def test_stack_oracle_worker_mutant_is_killed(self) -> None:
        mutant = '''import inspect
def evaluate_request(request):
    if set(request) != {"policy_source", "public_trace"}:
        raise ValueError
    score_oracle = inspect.currentframe().f_back.f_locals["score_oracle"]
    return {"decision": score_oracle}
'''
        with self.assertRaisesRegex(RuntimeError, "forbidden_"):
            eb.validate_isolated_worker_source(mutant)

    def test_forged_metadata_parent_stack_oracle_mutant_is_killed(self) -> None:
        def forged_parent_stack_mutant(
            policy_source: str, public_trace: list[dict]
        ) -> dict:
            del policy_source
            score_oracle = inspect.currentframe().f_back.f_locals["score_oracle"]
            trace_sha = eb.sha256_json(public_trace)
            return {
                "worker_protocol": "IEBV1-isolated-evaluator-1",
                "request_keys": ["policy_source", "public_trace"],
                "network_connect_guard": True,
                "decision": score_oracle,
                "error_count": int(score_oracle == "violation_detected"),
                "errors": [],
                "public_trace_sha256_before": trace_sha,
                "public_trace_sha256_after": trace_sha,
                "public_trace_unmodified": True,
                "isolation_mode": "python_-I_subprocess_with_minimal_environment",
                "child_environment_keys": [
                    "INVARIANT_DEPS_ROOT",
                    "INVARIANT_SOURCE_ROOT",
                    "PYTHONDONTWRITEBYTECODE",
                    "PYTHONHASHSEED",
                    "PYTHONUTF8",
                ],
                "isolated_worker_sha256": vm.EXPECTED_ISOLATED_WORKER_SHA256,
                "evaluator_request_sha256": eb.sha256_json(
                    {"policy_source": "forged", "public_trace": public_trace}
                ),
            }

        mutant_results, _ = eb._run_suite_with_evaluator(
            self.definitions, forged_parent_stack_mutant
        )
        non_dispatcher_gates = {
            key: value
            for key, value in mutant_results["coverage_gate"].items()
            if key != "production_dispatcher_closure_passed"
        }
        self.assertTrue(all(non_dispatcher_gates.values()))
        self.assertFalse(
            mutant_results["coverage_gate"]["production_dispatcher_closure_passed"]
        )
        self.assertIn(
            "source_sha256_mismatch",
            mutant_results["production_dispatcher"]["violations"],
        )
        self.assertFalse(mutant_results["overall_passed"])

    def test_label_interventions_are_distinct_and_excluded(self) -> None:
        self.assertTrue(self.results["overall_passed"])
        for group in self.results["label_invariance_groups"]:
            self.assertTrue(group["passed"])
        self.assertTrue(
            all(run["answer_label_excluded_from_evaluator_input"] for run in self.runs)
        )

    def test_label_invariance_all_six_groups(self) -> None:
        self.assertEqual(len(self.results["label_invariance_groups"]), 6)
        self.assertTrue(
            all(group["passed"] for group in self.results["label_invariance_groups"])
        )

    def test_public_fact_edits_are_non_vacuous_and_bidirectional(self) -> None:
        self.assertEqual(len(self.results["public_fact_relations"]), 2)
        self.assertTrue(
            all(relation["passed"] for relation in self.results["public_fact_relations"])
        )

    def test_trace_hash_lookup_mutant_is_killed_by_policy_mediation(self) -> None:
        trace_lookup = {}
        for case in self.definitions["base_cases"]:
            trace_lookup[eb.sha256_json(case["public_trace"])] = case[
                "score_only_expected_label"
            ]
            edit = case["paired_public_fact_edit"]
            trace_lookup[eb.sha256_json(edit["public_trace"])] = edit[
                "score_only_expected_label"
            ]

        def trace_only_mutant(
            policy_source: str, public_trace: list[dict]
        ) -> dict:
            del policy_source
            decision = trace_lookup[eb.sha256_json(public_trace)]
            trace_sha = eb.sha256_json(public_trace)
            return {
                "worker_protocol": "IEBV1-isolated-evaluator-1",
                "request_keys": ["policy_source", "public_trace"],
                "network_connect_guard": True,
                "decision": decision,
                "error_count": int(decision == "violation_detected"),
                "errors": [],
                "public_trace_sha256_before": trace_sha,
                "public_trace_sha256_after": trace_sha,
                "public_trace_unmodified": True,
                "isolation_mode": "python_-I_subprocess_with_minimal_environment",
                "child_environment_keys": [],
                "isolated_worker_sha256": vm.EXPECTED_ISOLATED_WORKER_SHA256,
                "evaluator_request_sha256": "trace-lookup-mutant",
            }

        mutant_results, _ = eb._run_suite_with_evaluator(
            self.definitions, trace_only_mutant
        )
        self.assertTrue(
            all(relation["passed"] for relation in mutant_results["public_fact_relations"])
        )
        self.assertFalse(
            mutant_results["coverage_gate"]["all_policy_source_relations_pass"]
        )
        self.assertFalse(mutant_results["overall_passed"])

    def test_isolated_worker_metadata_and_zero_model_calls(self) -> None:
        self.assertEqual(self.results["model_call_count"], 0)
        self.assertTrue(
            self.results["coverage_gate"]["all_calls_used_narrow_isolated_worker"]
        )
        self.assertTrue(all(run["network_connect_guard"] for run in self.runs))

    def test_source_commit_license_package_and_import_resolution(self) -> None:
        observed = eb.validate_upstream_environment()
        self.assertEqual(observed["source_commit"], eb.EXPECTED_SOURCE_COMMIT)
        self.assertEqual(observed["license_sha256"], eb.EXPECTED_LICENSE_SHA256)
        self.assertEqual(observed["license_url"], vm.EXPECTED_LICENSE_URL)
        self.assertTrue(all(observed["checks"].values()))
        versions = eb.runtime_package_versions()
        self.assertEqual(
            versions["packages"]["invariant-ai"], eb.EXPECTED_PACKAGE_VERSION
        )

    def test_manifest_exact_closure_kills_omitted_case_definitions(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            manifest = self._manifest_fixture(root)
            self.assertTrue(vm.verify_manifest_payload(manifest, root)["passed"])
            mutant = copy.deepcopy(manifest)
            mutant["entries"] = [
                entry
                for entry in mutant["entries"]
                if entry["path"] != vm.CASE_DEFINITIONS_RELATIVE_PATH
            ]
            mutant["entry_count"] = len(mutant["entries"])
            self._rehash_manifest_entries(mutant)
            observed = vm.verify_manifest_payload(mutant, root)
            self.assertFalse(observed["passed"])
            self.assertIn("schema:exact_path_set", observed["failures"])
            self.assertIn("schema:entry_count_expected", observed["failures"])

    def test_manifest_kills_forged_headers_duplicate_and_outbound_paths(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            manifest = self._manifest_fixture(root)

            forged = copy.deepcopy(manifest)
            forged["expected_headers"]["source_commit"] = "0" * 40
            observed = vm.verify_manifest_payload(forged, root)
            self.assertIn("expected_header:source_commit", observed["failures"])

            duplicate = copy.deepcopy(manifest)
            duplicate["entries"][-1]["path"] = duplicate["entries"][0]["path"]
            self._rehash_manifest_entries(duplicate)
            observed = vm.verify_manifest_payload(duplicate, root)
            self.assertIn("schema:duplicate_path", observed["failures"])

            outbound = copy.deepcopy(manifest)
            outbound["entries"][-1]["path"] = "../outside"
            self._rehash_manifest_entries(outbound)
            observed = vm.verify_manifest_payload(outbound, root)
            self.assertIn("path:../outside", observed["failures"])


if __name__ == "__main__":
    unittest.main()
