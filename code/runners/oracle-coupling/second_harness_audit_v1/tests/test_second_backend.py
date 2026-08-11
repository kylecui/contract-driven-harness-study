from __future__ import annotations

import copy
import hashlib
import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUDIT_CODE_ROOT = ROOT.parent
REPO_ROOT = AUDIT_CODE_ROOT.parents[2]
sys.path.insert(0, str(ROOT))

from run_audit import canonical, load_oic_policies, policy_as_candidate, run_corpus  # noqa: E402
from sqlite_backend import SQLitePolicyBackend  # noqa: E402
from verify_manifest import (  # noqa: E402
    EXPECTED_RELATIVE_PATHS,
    canonical_json,
    verify_manifest_payload,
)


FIXTURES = json.loads(
    (REPO_ROOT / "fixtures/oracle-coupling/failure_to_executable_contract_v2.json")
    .read_text(encoding="utf-8")
)["fixtures"]
CORPUS = json.loads(
    (
        REPO_ROOT
        / "data/reproduction/oracle-coupling/failure_to_executable_contract_v2/candidate_corpus.json"
    ).read_text(encoding="utf-8")
)


def current_manifest_payload() -> dict:
    entries = [
        {
            "path": relative,
            "sha256": hashlib.sha256((REPO_ROOT / relative).read_bytes()).hexdigest(),
            "bytes": (REPO_ROOT / relative).stat().st_size,
        }
        for relative in EXPECTED_RELATIVE_PATHS
    ]
    return {
        "manifest_version": "SHAV1-exact-1",
        "generated_at_utc": "test-only",
        "entry_count": len(entries),
        "entries_root_sha256": hashlib.sha256(
            canonical_json(entries).encode("utf-8")
        ).hexdigest(),
        "files": entries,
    }


class OICPolicySourceTests(unittest.TestCase):
    def test_compiler_evidence_reports_expected_output_excluded(self) -> None:
        _policies, _parity, boundary = load_oic_policies(FIXTURES)
        self.assertTrue(boundary["compiler_overall_passed"])
        self.assertIn(
            "expected_output", boundary["input_boundary"]["explicitly_excluded_keys"]
        )
        self.assertTrue(boundary["static_leakage_audit_passed"])
        self.assertTrue(boundary["dynamic_leakage_audit_passed"])

    def test_all_compiled_policies_match_authored_candidate_semantics(self) -> None:
        policies, _parity, _boundary = load_oic_policies(FIXTURES)
        for fixture in FIXTURES:
            with self.subTest(fixture=fixture["fixture_id"]):
                policy = policies[fixture["fixture_id"]]
                self.assertEqual(
                    canonical(policy_as_candidate(policy)),
                    canonical(fixture["expected_output"]),
                )


class SQLiteBackendTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.policies, _parity, _boundary = load_oic_policies(FIXTURES)

    def test_frozen_corpus_classification(self) -> None:
        rows = run_corpus(self.policies, CORPUS)
        self.assertEqual(len(rows), 392)
        self.assertTrue(all(row["classification_matches_label"] for row in rows))
        self.assertTrue(
            all(row["rejected_state_unchanged"] for row in rows if not row["accepted"])
        )

    def test_replay_and_external_drift_are_rejected(self) -> None:
        fixture = next(
            item for item in FIXTURES if item["expected_output"]["decision"] == "apply"
        )
        policy = self.policies[fixture["fixture_id"]]
        backend = SQLitePolicyBackend(policy)
        try:
            first = backend.evaluate_and_commit(copy.deepcopy(fixture["expected_output"]))
            second = backend.evaluate_and_commit(copy.deepcopy(fixture["expected_output"]))
            self.assertTrue(first["accepted"])
            self.assertFalse(second["accepted"])
            self.assertIn("stale_live_state", second["reason_codes"])

            backend.reset_state()
            path = policy["patches"][0]["path"]
            backend.set_live_value(path, "external-update")
            stale = backend.evaluate_and_commit(copy.deepcopy(fixture["expected_output"]))
            self.assertFalse(stale["accepted"])
            self.assertEqual(backend.state()[path], "external-update")
        finally:
            backend.close()

    def test_preserved_live_state_drift_is_rejected(self) -> None:
        fixture = next(
            item for item in FIXTURES if item["expected_output"]["decision"] == "apply"
        )
        policy = self.policies[fixture["fixture_id"]]
        preserved_path = policy["preserved_state"][0]["path"]
        backend = SQLitePolicyBackend(policy)
        try:
            backend.set_live_value(preserved_path, "attacker-value")
            result = backend.evaluate_and_commit(copy.deepcopy(fixture["expected_output"]))
            self.assertFalse(result["accepted"])
            self.assertFalse(result["wrote"])
            self.assertIn("preserved_live_state_mismatch", result["reason_codes"])
            self.assertEqual(backend.state()[preserved_path], "attacker-value")
        finally:
            backend.close()


class ManifestClosureTests(unittest.TestCase):
    def test_exact_path_set_kills_omission(self) -> None:
        payload = current_manifest_payload()
        payload["files"].pop()
        payload["entry_count"] = len(payload["files"])
        payload["entries_root_sha256"] = hashlib.sha256(
            canonical_json(payload["files"]).encode("utf-8")
        ).hexdigest()
        observed = verify_manifest_payload(payload)
        self.assertFalse(observed["passed"])
        self.assertIn("schema:exact_path_set", observed["failures"])

    def test_duplicate_and_outbound_paths_are_rejected(self) -> None:
        duplicate = current_manifest_payload()
        duplicate["files"][-1] = copy.deepcopy(duplicate["files"][0])
        duplicate["entries_root_sha256"] = hashlib.sha256(
            canonical_json(duplicate["files"]).encode("utf-8")
        ).hexdigest()
        duplicate_observed = verify_manifest_payload(duplicate)
        self.assertFalse(duplicate_observed["passed"])
        self.assertIn("schema:duplicate_path", duplicate_observed["failures"])

        outbound = current_manifest_payload()
        outbound["files"][-1]["path"] = "../outside"
        outbound["entries_root_sha256"] = hashlib.sha256(
            canonical_json(outbound["files"]).encode("utf-8")
        ).hexdigest()
        outbound_observed = verify_manifest_payload(outbound)
        self.assertFalse(outbound_observed["passed"])
        self.assertIn("path:../outside", outbound_observed["failures"])


if __name__ == "__main__":
    unittest.main()
