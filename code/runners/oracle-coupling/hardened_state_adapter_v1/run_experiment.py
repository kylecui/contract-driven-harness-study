#!/usr/bin/env python3
"""Run the hardened-adapter adversarial suite and bind its local artifacts."""

from __future__ import annotations

import hashlib
import json
import platform
import sys
import time
import unittest
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
AUDIT_CODE_ROOT = ROOT.parent
sys.path.insert(0, str(AUDIT_CODE_ROOT))

from layout import DATA_ROOT, FIXTURE_ROOT, REPO_ROOT, repo_relative  # noqa: E402
from hardened_state_adapter_v1.verify_manifest import (  # noqa: E402
    build_manifest_payload,
)

ARTIFACTS = DATA_ROOT / "hardened_state_adapter_v1" / "artifacts"
RESULTS_PATH = ARTIFACTS / "hardened_adapter_results.json"
MANIFEST_PATH = ARTIFACTS / "SHA256_MANIFEST.json"
FIXTURES_PATH = FIXTURE_ROOT / "failure_to_executable_contract_v2.json"
CONTRACT_GATE_PATH = (
    AUDIT_CODE_ROOT / "failure_to_executable_contract_v2" / "contract_gate.py"
)
FEC_RUNNER_PATH = (
    AUDIT_CODE_ROOT
    / "failure_to_executable_contract_v2"
    / "run_offline_verification.py"
)
LAYOUT_PATH = AUDIT_CODE_ROOT / "layout.py"


SCENARIO_BY_METHOD = {
    "test_valid_transition_updates_state_version_and_nonce_ledger": "positive_control",
    "test_version_cas_rejects_stale_overwrite": "live_state_drift_version_cas",
    "test_live_from_check_rejects_stale_candidate_at_current_version": "live_state_drift_from_value",
    "test_snapshot_hash_cas_rejects_same_version_uncovered_state_change": "exact_snapshot_hash_cas",
    "test_candidate_is_json_normalized_and_deep_frozen": "candidate_snapshot_freeze",
    "test_frozen_gate_matches_reference_on_full_authored_corpus": "frozen_gate_reference_parity_392",
    "test_phased_candidate_cannot_switch_patch_after_validation": "mutable_candidate_toctou_phased_list",
    "test_mutating_original_candidate_before_replace_has_no_effect": "mutable_candidate_toctou_hook",
    "test_final_hash_cas_detects_noncooperating_pre_replace_change": "noncooperating_pre_replace_cas",
    "test_accepted_action_nonce_cannot_be_replayed": "accepted_action_replay",
    "test_accepted_block_consumes_nonce_and_replay_is_rejected": "accepted_block_replay",
    "test_symlink_state_target_is_rejected_without_following": "symlink_state_target",
    "test_symlink_parent_component_is_rejected_without_following": "symlink_parent_component",
    "test_group_or_world_writable_parent_is_rejected": "trusted_parent_permission_gate",
    "test_pre_replace_exception_leaves_valid_old_state": "interrupted_accepted_write",
    "test_post_replace_directory_fsync_failure_is_explicit_commit_unknown": "post_replace_commit_unknown",
    "test_hostile_same_user_replace_window_remains_a_known_boundary": "residual_check_replace_window",
    "test_same_user_can_split_advisory_lock_inode_in_trusted_parent": "residual_sidecar_lock_inode_split",
    "test_unauthorized_alias_traversal_and_reserved_paths_are_rejected": "path_and_metadata_confusion",
    "test_cooperating_processes_serialize_and_only_one_cas_wins": "cooperating_multiprocess_contention",
    "test_invalid_nonce_fails_closed_before_state_write": "nonce_input_validation",
    "test_manifest_omission_and_duplicate_mutants_are_rejected": "manifest_path_closure",
    "test_manifest_schema_injection_is_rejected": "manifest_schema_closure",
}

RESIDUAL_METHODS = {
    "test_hostile_same_user_replace_window_remains_a_known_boundary",
    "test_same_user_can_split_advisory_lock_inode_in_trusted_parent",
}


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class RecordingResult(unittest.TextTestResult):
    """Retain one structured row for every executed unittest method."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.rows: list[dict[str, Any]] = []
        self._started: dict[str, float] = {}

    def startTest(self, test: unittest.TestCase) -> None:  # noqa: N802
        self._started[test.id()] = time.perf_counter()
        super().startTest(test)

    def _row(self, test: unittest.TestCase, status: str, detail: str | None = None) -> None:
        method = test.id().rsplit(".", 1)[-1]
        row: dict[str, Any] = {
            "test_id": test.id(),
            "scenario": SCENARIO_BY_METHOD.get(method, "unmapped"),
            "status": status,
            "evidence_role": (
                "known_residual_characterization"
                if method in RESIDUAL_METHODS
                else "control_verification"
            ),
            "duration_seconds": round(
                time.perf_counter() - self._started.get(test.id(), time.perf_counter()),
                6,
            ),
        }
        if detail:
            row["detail"] = detail
        self.rows.append(row)

    def addSuccess(self, test: unittest.TestCase) -> None:  # noqa: N802
        self._row(test, "pass")
        super().addSuccess(test)

    def addFailure(self, test: unittest.TestCase, err: Any) -> None:  # noqa: N802
        self._row(test, "fail", self._exc_info_to_string(err, test))
        super().addFailure(test, err)

    def addError(self, test: unittest.TestCase, err: Any) -> None:  # noqa: N802
        self._row(test, "error", self._exc_info_to_string(err, test))
        super().addError(test, err)

    def addSkip(self, test: unittest.TestCase, reason: str) -> None:  # noqa: N802
        self._row(test, "skip", reason)
        super().addSkip(test, reason)

    def addSubTest(  # noqa: N802
        self,
        test: unittest.TestCase,
        subtest: unittest.TestCase,
        err: Any,
    ) -> None:
        if err is not None:
            status = "fail" if issubclass(err[0], test.failureException) else "error"
            self._row(test, status, self._exc_info_to_string(err, subtest))
        super().addSubTest(test, subtest, err)


def run_suite() -> RecordingResult:
    loader = unittest.TestLoader()
    suite = loader.discover(str(ROOT / "tests"), pattern="test_*.py")
    runner = unittest.TextTestRunner(
        verbosity=2,
        resultclass=RecordingResult,
    )
    result = runner.run(suite)
    if not isinstance(result, RecordingResult):
        raise AssertionError("unexpected unittest result type")
    return result


def write_json(path: Path, value: Any) -> None:
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def build_results(result: RecordingResult) -> dict[str, Any]:
    counts = {
        "pass": result.testsRun
        - len(result.failures)
        - len(result.errors)
        - len(result.skipped),
        "fail": len(result.failures),
        "error": len(result.errors),
        "skip": len(result.skipped),
    }
    all_passed = result.wasSuccessful() and counts["skip"] == 0
    return {
        "experiment_id": "hardened_state_adapter_v1",
        "executed_at_utc": datetime.now(timezone.utc).isoformat(),
        "invocation": "python code/runners/oracle-coupling/hardened_state_adapter_v1/run_experiment.py",
        "runtime": {
            "python": sys.version.split()[0],
            "platform": platform.platform(),
            "posix": sys.platform != "win32",
        },
        "status": "bounded_pass_with_known_residual" if all_passed else "fail",
        "all_tests_passed": all_passed,
        "counts": counts,
        "scenarios": sorted(result.rows, key=lambda row: row["scenario"]),
        "tested_mechanisms": [
            "live-state read plus monotonically increasing version/CAS",
            "caller-observed exact envelope hash bound into commit CAS",
            "one-shot JSON normalization plus recursively frozen candidate containers",
            "SHA-256 accepted-action nonce ledger",
            "no-follow regular-file checks for state and lock targets",
            "user-controlled component symlink rejection and same-user non-writable parent gate",
            "same-directory tempfile, file fsync, pre-replace CAS, os.replace, directory fsync",
            "canonical logical paths and reserved envelope-metadata rejection",
            "POSIX advisory lock for cooperating processes",
        ],
        "claim_boundary": {
            "gold_oracle_coupling": "not addressed by this adapter",
            "semantic_authority": "delegated unchanged to the authored FEC-v2 contract",
            "process_scope": (
                "single host and cooperating same-user processes using a stable sidecar lock path"
            ),
            "filesystem_scope": (
                "requires a trusted parent directory and filesystem support for same-directory "
                "atomic replace and fsync durability"
            ),
            "fault_scope": (
                "pre-replace exception and post-replace directory-fsync failure injected; "
                "no power-loss, kernel-crash, or filesystem-fault campaign"
            ),
            "nonce_scope": (
                "nonces are consumed by accepted apply and accepted block decisions; rejected "
                "proposals do not change state"
            ),
        },
        "known_residuals": [
            {
                "id": "same_user_namespace_race_after_final_hash_check",
                "observed": True,
                "effect": (
                    "a same-user process that ignores the lock and can rewrite directory entries "
                    "inside the final hash-check to os.replace window can still lose its update"
                ),
                "required_boundary": (
                    "stable parent namespace plus cooperative same-user writers, or a stronger "
                    "transactional/storage primitive outside this standard-library file adapter"
                ),
            },
            {
                "id": "sidecar_flock_is_advisory",
                "observed": True,
                "effect": (
                    "unlinking and recreating the lock path can split lock inodes when a same-user "
                    "actor can mutate the trusted parent"
                ),
                "required_boundary": "stable trusted parent and cooperating writers",
            },
        ],
        "external_inputs": [
            {"path": repo_relative(path), "sha256": sha256_path(path)}
            for path in (
                FIXTURES_PATH,
                CONTRACT_GATE_PATH,
                FEC_RUNNER_PATH,
                LAYOUT_PATH,
            )
        ],
    }


def write_manifest() -> None:
    write_json(MANIFEST_PATH, build_manifest_payload())


def main() -> int:
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    result = run_suite()
    results = build_results(result)
    write_json(RESULTS_PATH, results)
    write_manifest()
    print(json.dumps(results, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if results["all_tests_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
