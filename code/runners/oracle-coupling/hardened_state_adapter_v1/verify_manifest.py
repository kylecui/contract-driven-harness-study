#!/usr/bin/env python3
"""Verify the exact hardened-adapter source-to-result closure."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
AUDIT_CODE_ROOT = ROOT.parent
REPO_ROOT = AUDIT_CODE_ROOT.parents[2]
ARTIFACT_ROOT = (
    REPO_ROOT
    / "data"
    / "reproduction"
    / "oracle-coupling"
    / "hardened_state_adapter_v1"
    / "artifacts"
)
MANIFEST_PATH = ARTIFACT_ROOT / "SHA256_MANIFEST.json"

EXPECTED_ENTRY_PATHS = (
    "code/runners/oracle-coupling/hardened_state_adapter_v1/README.md",
    "code/runners/oracle-coupling/hardened_state_adapter_v1/hardened_adapter.py",
    "code/runners/oracle-coupling/hardened_state_adapter_v1/run_experiment.py",
    "code/runners/oracle-coupling/hardened_state_adapter_v1/tests/test_hardened_adapter.py",
    "code/runners/oracle-coupling/hardened_state_adapter_v1/verify_manifest.py",
    "data/reproduction/oracle-coupling/hardened_state_adapter_v1/artifacts/hardened_adapter_results.json",
)
EXPECTED_EXTERNAL_INPUT_PATHS = (
    "fixtures/oracle-coupling/failure_to_executable_contract_v2.json",
    "code/runners/oracle-coupling/failure_to_executable_contract_v2/contract_gate.py",
    "code/runners/oracle-coupling/failure_to_executable_contract_v2/run_offline_verification.py",
    "code/runners/oracle-coupling/layout.py",
)


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _entries(relative_paths: tuple[str, ...]) -> list[dict[str, Any]]:
    return [
        {
            "path": relative,
            "bytes": (REPO_ROOT / relative).stat().st_size,
            "sha256": sha256_path(REPO_ROOT / relative),
        }
        for relative in relative_paths
    ]


def build_manifest_payload() -> dict[str, Any]:
    entries = _entries(EXPECTED_ENTRY_PATHS)
    external_inputs = _entries(EXPECTED_EXTERNAL_INPUT_PATHS)
    return {
        "manifest_version": "HSAV1-exact-1",
        "experiment_id": "hardened_state_adapter_v1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "manifest_self_excluded": True,
        "entry_count": len(entries),
        "external_input_count": len(external_inputs),
        "entries_root_sha256": hashlib.sha256(
            canonical_json(entries).encode("utf-8")
        ).hexdigest(),
        "external_inputs_root_sha256": hashlib.sha256(
            canonical_json(external_inputs).encode("utf-8")
        ).hexdigest(),
        "entries": entries,
        "external_inputs": external_inputs,
    }


def _verify_list(
    entries: Any,
    expected_paths: tuple[str, ...],
    label: str,
    failures: list[str],
) -> int:
    if not isinstance(entries, list):
        failures.append(f"schema:{label}")
        return 0
    paths: list[str] = []
    for entry in entries:
        if not isinstance(entry, dict) or set(entry) != {"path", "sha256", "bytes"}:
            failures.append(f"schema:{label}:entry_shape")
            continue
        if not isinstance(entry.get("path"), str):
            failures.append(f"schema:{label}:path_type")
            continue
        paths.append(entry["path"])
    if len(paths) != len(set(paths)):
        failures.append(f"schema:{label}:duplicate_path")
    if len(entries) != len(expected_paths):
        failures.append(f"schema:{label}:expected_count")
    if set(paths) != set(expected_paths):
        failures.append(f"schema:{label}:exact_path_set")

    verified = 0
    for entry in entries:
        if not isinstance(entry, dict) or set(entry) != {"path", "sha256", "bytes"}:
            continue
        relative_text = entry.get("path")
        if not isinstance(relative_text, str):
            continue
        relative = Path(relative_text)
        if relative.is_absolute() or ".." in relative.parts:
            failures.append(f"path:{label}:{relative_text}")
            continue
        path = (REPO_ROOT / relative).resolve()
        try:
            path.relative_to(REPO_ROOT.resolve())
        except ValueError:
            failures.append(f"containment:{label}:{relative_text}")
            continue
        if not path.is_file():
            failures.append(f"missing:{label}:{relative_text}")
            continue
        if sha256_path(path) != entry.get("sha256"):
            failures.append(f"sha256:{label}:{relative_text}")
        if path.stat().st_size != entry.get("bytes"):
            failures.append(f"bytes:{label}:{relative_text}")
        else:
            verified += 1
    return verified


def verify_manifest_payload(payload: Any) -> dict[str, Any]:
    failures: list[str] = []
    if not isinstance(payload, dict):
        return {"entry_count": 0, "failures": ["schema:manifest_object"], "passed": False}
    expected_keys = {
        "manifest_version",
        "experiment_id",
        "generated_at_utc",
        "manifest_self_excluded",
        "entry_count",
        "external_input_count",
        "entries_root_sha256",
        "external_inputs_root_sha256",
        "entries",
        "external_inputs",
    }
    if set(payload) != expected_keys:
        failures.append("schema:exact_top_level_keys")
    if payload.get("manifest_version") != "HSAV1-exact-1":
        failures.append("schema:manifest_version")
    if payload.get("experiment_id") != "hardened_state_adapter_v1":
        failures.append("schema:experiment_id")
    if payload.get("manifest_self_excluded") is not True:
        failures.append("schema:manifest_self_excluded")

    entries = payload.get("entries")
    external_inputs = payload.get("external_inputs")
    verified_entries = _verify_list(
        entries, EXPECTED_ENTRY_PATHS, "entries", failures
    )
    verified_external = _verify_list(
        external_inputs,
        EXPECTED_EXTERNAL_INPUT_PATHS,
        "external_inputs",
        failures,
    )
    if payload.get("entry_count") != (
        len(entries) if isinstance(entries, list) else None
    ):
        failures.append("schema:entry_count")
    if payload.get("external_input_count") != (
        len(external_inputs) if isinstance(external_inputs, list) else None
    ):
        failures.append("schema:external_input_count")
    if payload.get("entries_root_sha256") != hashlib.sha256(
        canonical_json(entries if isinstance(entries, list) else []).encode("utf-8")
    ).hexdigest():
        failures.append("schema:entries_root_sha256")
    if payload.get("external_inputs_root_sha256") != hashlib.sha256(
        canonical_json(
            external_inputs if isinstance(external_inputs, list) else []
        ).encode("utf-8")
    ).hexdigest():
        failures.append("schema:external_inputs_root_sha256")

    try:
        results = json.loads(
            (ARTIFACT_ROOT / "hardened_adapter_results.json").read_text(
                encoding="utf-8"
            )
        )
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        failures.append(f"cross_file:results_unreadable:{type(error).__name__}")
        results = None
    if not isinstance(results, dict):
        failures.append("cross_file:results_object")
    else:
        if results.get("experiment_id") != "hardened_state_adapter_v1":
            failures.append("cross_file:results:experiment_id")
        if results.get("all_tests_passed") is not True:
            failures.append("cross_file:results:all_tests_passed")
        counts = results.get("counts", {})
        if any(counts.get(key) != 0 for key in ("fail", "error", "skip")):
            failures.append("cross_file:results:test_failures")
        result_inputs = results.get("external_inputs")
        if not isinstance(result_inputs, list) or {
            item.get("path") for item in result_inputs if isinstance(item, dict)
        } != set(EXPECTED_EXTERNAL_INPUT_PATHS):
            failures.append("cross_file:results:external_input_paths")
        elif isinstance(external_inputs, list):
            manifest_hashes = {
                item.get("path"): item.get("sha256")
                for item in external_inputs
                if isinstance(item, dict)
            }
            if any(
                item.get("sha256") != manifest_hashes.get(item.get("path"))
                for item in result_inputs
                if isinstance(item, dict)
            ):
                failures.append("cross_file:results:external_input_hashes")

    return {
        "entry_count": len(entries) if isinstance(entries, list) else 0,
        "external_input_count": (
            len(external_inputs) if isinstance(external_inputs, list) else 0
        ),
        "verified_entries": verified_entries if not failures else None,
        "verified_external_inputs": verified_external if not failures else None,
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
            "external_input_count": 0,
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
