#!/usr/bin/env python3
"""Run a bounded second-backend audit using SQLite transaction semantics."""

from __future__ import annotations

import copy
import csv
import hashlib
import json
import platform
import sqlite3
import subprocess
import sys
import tempfile
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from sqlite_backend import SQLitePolicyBackend


ROOT = Path(__file__).resolve().parent
AUDIT_CODE_ROOT = ROOT.parent
sys.path.insert(0, str(AUDIT_CODE_ROOT))

from layout import (  # noqa: E402
    BASE_SOURCE_COMMIT,
    DATA_ROOT,
    FIXTURE_ROOT,
    REPO_ROOT,
    base_snapshot_available,
)

FIXTURES_PATH = FIXTURE_ROOT / "failure_to_executable_contract_v2.json"
CORPUS_PATH = DATA_ROOT / "failure_to_executable_contract_v2" / "candidate_corpus.json"
ARTIFACT_ROOT = DATA_ROOT / "second_harness_audit_v1" / "artifacts"
OIC_ROOT = AUDIT_CODE_ROOT / "oracle_independent_compiler_v1"
OIC_DATA_ROOT = DATA_ROOT / "oracle_independent_compiler_v1" / "artifacts"
OIC_CONTRACTS_PATH = OIC_DATA_ROOT / "compiled_contracts.json"
OIC_RESULTS_PATH = OIC_DATA_ROOT / "results.json"


def canonical(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: canonical(item) for key, item in sorted(value.items())}
    if isinstance(value, list):
        normalised = [canonical(item) for item in value]
        return sorted(
            normalised,
            key=lambda item: json.dumps(item, ensure_ascii=False, sort_keys=True),
        )
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def policy_as_candidate(policy: dict[str, Any]) -> dict[str, Any]:
    return {
        "task_id": policy["fixture_id"],
        "decision": policy["decision"],
        "state_patch": copy.deepcopy(policy["patches"]),
        "preserved_state": copy.deepcopy(policy["preserved_state"]),
        "evidence_bindings": [
            {
                "slot_id": "decision",
                "evidence_ids": list(policy["decision_evidence_ids"]),
            }
        ],
        "unknown_state": list(policy["unknown_state"]),
        "forbidden_inferences": list(policy["forbidden_inferences"]),
        "gate": copy.deepcopy(policy["gate"]),
        "next_action": policy["next_action"],
    }


def load_oic_policies(
    fixtures: list[dict[str, Any]],
) -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    compiler_results = json.loads(OIC_RESULTS_PATH.read_text(encoding="utf-8"))
    if not compiler_results.get("overall_passed"):
        raise RuntimeError("oracle_independent_compiler_v1 is not in a passed state")
    compiled_payload = json.loads(OIC_CONTRACTS_PATH.read_text(encoding="utf-8"))
    compiled = compiled_payload["contracts"]
    if len(compiled) != len(fixtures):
        raise RuntimeError("OIC contract count does not match the frozen fixture count")

    policies: dict[str, dict[str, Any]] = {}
    parity: list[dict[str, Any]] = []
    fixtures_by_id = {fixture["fixture_id"]: fixture for fixture in fixtures}
    for contract in compiled:
        fixture = fixtures_by_id[contract["task_id"]]
        policy = {
            "fixture_id": contract["task_id"],
            "family": contract["family"],
            "initial_state": copy.deepcopy(contract["initial_state"]),
            "decision": contract["expected_decision"],
            "patches": copy.deepcopy(contract["desired_patch"]),
            "preserved_state": copy.deepcopy(contract["required_preserved_state"]),
            "decision_evidence_ids": list(contract["required_evidence_ids"]),
            "unknown_state": list(contract["required_unknown_state"]),
            "forbidden_inferences": list(contract["forbidden_inferences"]),
            "gate": copy.deepcopy(contract["expected_gate"]),
            "next_action": contract["expected_next_action"],
        }
        policies[fixture["fixture_id"]] = policy
        derived_candidate = policy_as_candidate(policy)
        matches = canonical(derived_candidate) == canonical(fixture["expected_output"])
        parity.append(
            {
                "fixture_id": fixture["fixture_id"],
                "family": fixture["family"],
                "split": fixture["split"],
                "policy_source": "oracle_independent_compiler_v1/compiled_contracts.json",
                "expected_output_available_to_selected_compiler": False,
                "semantic_parity_with_authored_expected_output": matches,
            }
        )
    boundary = {
        "compiler_protocol_id": compiler_results["protocol_id"],
        "compiler_overall_passed": compiler_results["overall_passed"],
        "compiled_contracts_sha256": sha256(OIC_CONTRACTS_PATH),
        "compiler_results_sha256": sha256(OIC_RESULTS_PATH),
        "input_boundary": compiler_results["input_boundary"],
        "static_leakage_audit_passed": compiler_results["static_leakage_audit"]["passed"],
        "dynamic_leakage_audit_passed": compiler_results["dynamic_leakage_audit"]["passed"],
        "not_blinded": True,
        "not_independently_authored": True,
    }
    return policies, parity, boundary


def run_corpus(
    policies: dict[str, dict[str, Any]], corpus: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    by_fixture: dict[str, list[dict[str, Any]]] = {}
    for item in corpus:
        by_fixture.setdefault(item["fixture_id"], []).append(item)

    for fixture_id, items in sorted(by_fixture.items()):
        backend = SQLitePolicyBackend(policies[fixture_id])
        try:
            for item in items:
                backend.reset_state()
                result = backend.evaluate_and_commit(item["value"])
                predicted_valid = result["accepted"]
                labelled_valid = item["label"] == "valid"
                rows.append(
                    {
                        "fixture_id": fixture_id,
                        "family": item["family"],
                        "split": item["split"],
                        "candidate_id": item["candidate_id"],
                        "mutation": item["mutation"],
                        "label": item["label"],
                        "accepted": predicted_valid,
                        "classification_matches_label": predicted_valid == labelled_valid,
                        "state_changed": result["state_changed"],
                        "rejected_state_unchanged": result["accepted"] or not result["state_changed"],
                        "reason_codes": ";".join(result["reason_codes"]),
                    }
                )
        finally:
            backend.close()
    return rows


def state_characterisation(policy: dict[str, Any], golden: dict[str, Any]) -> dict[str, Any]:
    apply_patch = policy["patches"][0]
    path = apply_patch["path"]
    backend = SQLitePolicyBackend(policy)
    try:
        first = backend.evaluate_and_commit(copy.deepcopy(golden))
        second = backend.evaluate_and_commit(copy.deepcopy(golden))

        backend.reset_state()
        external_value = "__concurrent_live_value__"
        backend.set_live_value(path, external_value)
        stale = backend.evaluate_and_commit(copy.deepcopy(golden))
        stale_after = backend.state()[path]

        backend.reset_state()
        preserved_path = policy["preserved_state"][0]["path"]
        preserved_live_value = "__modified_preserved_value__"
        backend.set_live_value(preserved_path, preserved_live_value)
        preserved_drift = backend.evaluate_and_commit(copy.deepcopy(golden))
        preserved_after = backend.state()[preserved_path]
    finally:
        backend.close()

    with tempfile.TemporaryDirectory(prefix="sqlite-backend-lock-") as temp_dir:
        database = Path(temp_dir) / "state.db"
        file_backend = SQLitePolicyBackend(policy, database)
        contender = sqlite3.connect(database, isolation_level=None, timeout=0.0)
        contender.execute("PRAGMA busy_timeout = 0")
        file_backend.connection.execute("BEGIN IMMEDIATE")
        lock_error = None
        try:
            contender.execute("BEGIN IMMEDIATE")
        except sqlite3.OperationalError as exc:
            lock_error = str(exc)
        finally:
            if contender.in_transaction:
                contender.execute("ROLLBACK")
            file_backend.connection.execute("ROLLBACK")
            contender.close()
            file_backend.close()

    with tempfile.TemporaryDirectory(prefix="sqlite-backend-rollback-") as temp_dir:
        database = Path(temp_dir) / "state.db"
        rollback_backend = SQLitePolicyBackend(policy, database)
        rollback_before = rollback_backend.state()
        rollback_backend.connection.execute("BEGIN IMMEDIATE")
        rollback_backend.connection.execute(
            "UPDATE state_kv SET value_json = ?, version = version + 1 WHERE path = ?",
            (json.dumps(apply_patch["to"]), path),
        )
        rollback_backend.connection.execute("ROLLBACK")
        rollback_after = rollback_backend.state()
        integrity_check = rollback_backend.connection.execute("PRAGMA integrity_check").fetchone()[0]
        rollback_backend.close()

    with tempfile.TemporaryDirectory(prefix="sqlite-backend-namespace-") as temp_dir:
        temp_root = Path(temp_dir)
        target = temp_root / "target.db"
        symlink = temp_root / "state-link.db"
        symlink_backend = SQLitePolicyBackend(policy, target)
        symlink_backend.close()
        symlink.symlink_to(target)
        linked_backend = SQLitePolicyBackend(policy, symlink, initialise=False)
        linked_result = linked_backend.evaluate_and_commit(copy.deepcopy(golden))
        linked_backend.close()
        target_reopen = SQLitePolicyBackend(policy, target, initialise=False)
        target_value = target_reopen.state()[path]
        target_reopen.close()

    return {
        "base_fixture_id": policy["fixture_id"],
        "probe_unit": (
            "All six state-characterisation probes reuse this single apply fixture; "
            "they are named mechanism checks, not independent task samples."
        ),
        "accepted_action_replay": {
            "first_accepted": first["accepted"],
            "first_wrote": first["wrote"],
            "second_accepted": second["accepted"],
            "second_reasons": second["reason_codes"],
            "replay_rejected_by_live_state_check": (
                first["accepted"]
                and not second["accepted"]
                and "stale_live_state" in second["reason_codes"]
            ),
        },
        "external_live_state_drift": {
            "candidate_accepted": stale["accepted"],
            "reasons": stale["reason_codes"],
            "external_value_preserved": stale_after == external_value,
        },
        "immutable_live_state_drift": {
            "candidate_accepted": preserved_drift["accepted"],
            "reasons": preserved_drift["reason_codes"],
            "modified_preserved_value_retained": (
                preserved_after == preserved_live_value
            ),
            "rejected_by_preserved_live_state_check": (
                not preserved_drift["accepted"]
                and "preserved_live_state_mismatch" in preserved_drift["reason_codes"]
            ),
        },
        "single_writer_serialization": {
            "second_begin_immediate_error": lock_error,
            "second_writer_blocked": lock_error is not None,
            "boundary": "same database inode and cooperative SQLite writers",
        },
        "exception_before_commit": {
            "rollback_preserved_state": rollback_before == rollback_after,
            "integrity_check": integrity_check,
            "boundary": "explicit rollback after an injected pre-commit interruption; not a power-loss test",
        },
        "symlink_database_path": {
            "candidate_accepted": linked_result["accepted"],
            "symlink_followed_to_target": target_value == apply_patch["to"],
            "boundary": "the database pathname remains trusted; same-user namespace attacks are not eliminated",
        },
    }


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def sqlite_cli_version() -> str | None:
    try:
        return subprocess.check_output(
            ["sqlite3", "--version"], text=True, stderr=subprocess.DEVNULL
        ).strip()
    except (FileNotFoundError, subprocess.CalledProcessError):
        return None


def main() -> int:
    ARTIFACT_ROOT.mkdir(parents=True, exist_ok=True)
    fixture_payload = json.loads(FIXTURES_PATH.read_text(encoding="utf-8"))
    fixtures = fixture_payload["fixtures"]
    corpus = json.loads(CORPUS_PATH.read_text(encoding="utf-8"))

    policies, parity, compiler_boundary = load_oic_policies(fixtures)
    rows = run_corpus(policies, corpus)
    apply_fixture = next(
        fixture for fixture in fixtures if fixture["expected_output"]["decision"] == "apply"
    )
    state_tests = state_characterisation(
        policies[apply_fixture["fixture_id"]], apply_fixture["expected_output"]
    )

    classification = Counter(
        (row["label"], bool(row["accepted"])) for row in rows
    )
    reason_counts = Counter(
        reason
        for row in rows
        for reason in row["reason_codes"].split(";")
        if reason
    )
    summary = {
        "protocol_id": "second-harness-audit-v1-sqlite-transactional-backend",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "evidence_class": "offline_backend_portability_and_transaction_characterisation",
        "backend": "SQLite transactional policy backend",
        "runtime": {
            "python": platform.python_version(),
            "python_sqlite": sqlite3.sqlite_version,
            "sqlite_cli": sqlite_cli_version(),
            "platform": platform.platform(),
        },
        "source_snapshot": {
            "base_commit": BASE_SOURCE_COMMIT,
            "base_commit_is_ancestor": base_snapshot_available(),
            "boundary": "The audit is additive relative to the frozen publication-support base.",
        },
        "compiler_boundary": {
            **compiler_boundary,
            "fixture_count": len(fixtures),
            "expected_output_available_to_selected_compiler": False,
            "semantic_parity_count": sum(
                item["semantic_parity_with_authored_expected_output"] for item in parity
            ),
        },
        "finite_corpus": {
            "candidate_count": len(rows),
            "valid_accepted": classification[("valid", True)],
            "valid_rejected": classification[("valid", False)],
            "invalid_accepted": classification[("invalid", True)],
            "invalid_rejected": classification[("invalid", False)],
            "classification_matches_label": sum(
                row["classification_matches_label"] for row in rows
            ),
            "rejected_state_unchanged": sum(
                (not row["accepted"]) and row["rejected_state_unchanged"] for row in rows
            ),
            "reason_counts": dict(sorted(reason_counts.items())),
            "boundary": "The candidate labels and mutation corpus originate from the same authored FEC-v2 package; parity is portability evidence, not external validation.",
        },
        "state_characterisation": state_tests,
        "independence_assessment": {
            "model_call_path_independent": "not_tested_no_model_calls",
            "rule_evaluator_independent": True,
            "state_representation_independent": True,
            "transaction_commit_path_independent": True,
            "task_authoring_independent": False,
            "human_investigator_independent": False,
            "external_system_independent": False,
        },
        "claim": (
            "The FEC-v2 rules can be ported to a distinct relational evaluator and transactional "
            "state backend without reading expected_output at runtime, and SQLite rejects stale "
            "replay under the tested cooperative-writer conditions. This does not close the "
            "independent-author, independent-task, or external-harness validation gaps."
        ),
        "non_completion_states": [
            "independent_author_set_missing",
            "external_harness_validation_missing",
            "blind_policy_implementation_missing",
            "hostile_same_user_namespace_residual",
            "fresh_model_execution_not_part_of_this_audit",
        ],
    }

    outputs = {
        "compiler_parity.json": parity,
        "state_characterisation.json": state_tests,
        "audit_summary.json": summary,
    }
    for name, payload in outputs.items():
        (ARTIFACT_ROOT / name).write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
    write_csv(ARTIFACT_ROOT / "per_candidate_results.csv", rows)

    manifest_paths = [
        ROOT / "README.md",
        ROOT / "policy.sql",
        ROOT / "sqlite_backend.py",
        ROOT / "run_audit.py",
        ROOT / "tests/test_second_backend.py",
        ROOT / "verify_manifest.py",
        FIXTURES_PATH,
        CORPUS_PATH,
        OIC_CONTRACTS_PATH,
        OIC_RESULTS_PATH,
        OIC_DATA_ROOT / "SHA256_MANIFEST.json",
        *(ARTIFACT_ROOT / name for name in outputs),
        ARTIFACT_ROOT / "per_candidate_results.csv",
        AUDIT_CODE_ROOT / "layout.py",
    ]
    manifest = {
        "manifest_version": "SHAV1-exact-1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "entry_count": len(manifest_paths),
        "files": [
            {
                "path": path.relative_to(REPO_ROOT).as_posix(),
                "sha256": sha256(path),
                "bytes": path.stat().st_size,
            }
            for path in manifest_paths
        ],
    }
    manifest["entries_root_sha256"] = hashlib.sha256(
        json.dumps(
            manifest["files"],
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()
    (ARTIFACT_ROOT / "SHA256_MANIFEST.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
