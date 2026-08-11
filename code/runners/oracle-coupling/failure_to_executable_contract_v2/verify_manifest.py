#!/usr/bin/env python3
"""Verify the exact FEC-v2 source-to-result integrity closure."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
from typing import Any


CODE_ROOT = Path(__file__).resolve().parent
REPO_ROOT = Path(__file__).resolve().parents[4]
DATA_ROOT = REPO_ROOT / "data" / "reproduction" / "oracle-coupling" / "failure_to_executable_contract_v2"
MANIFEST_PATH = DATA_ROOT / "SHA256_MANIFEST.json"

EXPECTED_RELATIVE_PATHS = (
    "code/runners/oracle-coupling/failure_to_executable_contract_v2/README.md",
    "code/runners/oracle-coupling/failure_to_executable_contract_v2/build_artifact_manifest.py",
    "code/runners/oracle-coupling/failure_to_executable_contract_v2/contract_gate.py",
    "code/runners/oracle-coupling/failure_to_executable_contract_v2/run_offline_verification.py",
    "code/runners/oracle-coupling/failure_to_executable_contract_v2/tests/test_contract_gate.py",
    "code/runners/oracle-coupling/failure_to_executable_contract_v2/verify_manifest.py",
    "fixtures/oracle-coupling/failure_to_executable_contract_v2.json",
    "data/reproduction/oracle-coupling/failure_to_executable_contract_v2/candidate_corpus.json",
    "data/reproduction/oracle-coupling/failure_to_executable_contract_v2/candidate_gate_results.csv",
    "data/reproduction/oracle-coupling/failure_to_executable_contract_v2/execution_traces.json",
    "data/reproduction/oracle-coupling/failure_to_executable_contract_v2/offline_verification_summary.json",
)


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def build_manifest_payload() -> dict[str, Any]:
    entries = [
        {
            "path": relative,
            "sha256": sha256_path(REPO_ROOT / relative),
            "bytes": (REPO_ROOT / relative).stat().st_size,
        }
        for relative in EXPECTED_RELATIVE_PATHS
    ]
    return {
        "manifest_version": "FECV2-exact-1",
        "entry_count": len(entries),
        "entries_root_sha256": hashlib.sha256(
            canonical_json(entries).encode("utf-8")
        ).hexdigest(),
        "entries": entries,
    }


def load_json(relative: str, failures: list[str]) -> Any:
    try:
        return json.loads((REPO_ROOT / relative).read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        failures.append(f"unreadable:{relative}:{type(error).__name__}")
        return None


def verify_manifest_payload(payload: Any) -> dict[str, Any]:
    failures: list[str] = []
    if not isinstance(payload, dict):
        return {"entry_count": 0, "failures": ["schema:manifest_object"], "passed": False}
    if set(payload) != {
        "manifest_version",
        "entry_count",
        "entries_root_sha256",
        "entries",
    }:
        failures.append("schema:exact_top_level_keys")
    if payload.get("manifest_version") != "FECV2-exact-1":
        failures.append("schema:manifest_version")
    entries = payload.get("entries")
    if not isinstance(entries, list):
        failures.append("schema:entries")
        entries = []
    if payload.get("entry_count") != len(entries):
        failures.append("schema:entry_count")
    if payload.get("entry_count") != len(EXPECTED_RELATIVE_PATHS):
        failures.append("schema:expected_entry_count")

    paths: list[str] = []
    for entry in entries:
        if not isinstance(entry, dict) or set(entry) != {"path", "sha256", "bytes"}:
            failures.append("schema:entry_shape")
            continue
        if not isinstance(entry.get("path"), str):
            failures.append("schema:path_type")
            continue
        paths.append(entry["path"])
    if len(paths) != len(set(paths)):
        failures.append("schema:duplicate_path")
    if set(paths) != set(EXPECTED_RELATIVE_PATHS):
        failures.append("schema:exact_path_set")
    if payload.get("entries_root_sha256") != hashlib.sha256(
        canonical_json(entries).encode("utf-8")
    ).hexdigest():
        failures.append("schema:entries_root_sha256")

    verified = 0
    for entry in entries:
        if not isinstance(entry, dict) or set(entry) != {"path", "sha256", "bytes"}:
            continue
        relative_text = entry.get("path")
        if not isinstance(relative_text, str):
            continue
        relative = Path(relative_text)
        if relative.is_absolute() or ".." in relative.parts:
            failures.append(f"path:{relative_text}")
            continue
        path = (REPO_ROOT / relative).resolve()
        try:
            path.relative_to(REPO_ROOT.resolve())
        except ValueError:
            failures.append(f"containment:{relative_text}")
            continue
        if not path.is_file():
            failures.append(f"missing:{relative_text}")
            continue
        if sha256_path(path) != entry.get("sha256"):
            failures.append(f"sha256:{relative_text}")
        if path.stat().st_size != entry.get("bytes"):
            failures.append(f"bytes:{relative_text}")
        else:
            verified += 1

    fixture_payload = load_json(
        "fixtures/oracle-coupling/failure_to_executable_contract_v2.json", failures
    )
    corpus = load_json(
        "data/reproduction/oracle-coupling/failure_to_executable_contract_v2/candidate_corpus.json",
        failures,
    )
    traces = load_json(
        "data/reproduction/oracle-coupling/failure_to_executable_contract_v2/execution_traces.json",
        failures,
    )
    summary = load_json(
        "data/reproduction/oracle-coupling/failure_to_executable_contract_v2/offline_verification_summary.json",
        failures,
    )
    try:
        with (DATA_ROOT / "candidate_gate_results.csv").open(
            encoding="utf-8", newline=""
        ) as handle:
            row_count = sum(1 for _ in csv.DictReader(handle))
    except (OSError, UnicodeError, csv.Error) as error:
        failures.append(f"unreadable:candidate_gate_results.csv:{type(error).__name__}")
        row_count = None

    if not isinstance(fixture_payload, dict) or len(fixture_payload.get("fixtures", [])) != 28:
        failures.append("cross_file:fixture_count")
    if not isinstance(corpus, list) or len(corpus) != 392:
        failures.append("cross_file:candidate_count")
    if not isinstance(traces, list) or len(traces) != 392:
        failures.append("cross_file:trace_count")
    if row_count != 1568:
        failures.append("cross_file:gate_row_count")
    if not isinstance(summary, dict):
        failures.append("cross_file:summary_object")
    else:
        expected_summary = {
            "fixture_count": 28,
            "candidate_count": 392,
            "valid_candidate_count": 56,
            "invalid_candidate_count": 336,
        }
        for key, expected in expected_summary.items():
            if summary.get(key) != expected:
                failures.append(f"cross_file:summary:{key}")
        integrity = summary.get("state_integrity", {})
        if integrity.get("rejected_candidates") != 336:
            failures.append("cross_file:summary:rejected_candidates")
        if integrity.get("rejected_candidates_with_unchanged_state") != 336:
            failures.append("cross_file:summary:unchanged_rejections")

    return {
        "entry_count": len(entries),
        "verified_entries": verified if not failures else None,
        "failures": sorted(set(failures)),
        "passed": not failures,
    }


def verify_manifest() -> dict[str, Any]:
    try:
        payload = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        return {
            "manifest": str(MANIFEST_PATH.relative_to(REPO_ROOT)),
            "entry_count": 0,
            "verified_entries": None,
            "failures": [f"manifest_unreadable:{type(error).__name__}"],
            "passed": False,
        }
    result = verify_manifest_payload(payload)
    result["manifest"] = str(MANIFEST_PATH.relative_to(REPO_ROOT))
    return result


def main() -> None:
    result = verify_manifest()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if not result["passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
