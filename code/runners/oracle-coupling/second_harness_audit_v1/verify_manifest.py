#!/usr/bin/env python3
"""Verify the exact second-backend source-to-result integrity closure."""

from __future__ import annotations

import csv
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
AUDIT_CODE_ROOT = ROOT.parent
sys.path.insert(0, str(AUDIT_CODE_ROOT))

from layout import DATA_ROOT, REPO_ROOT  # noqa: E402

MANIFEST = DATA_ROOT / "second_harness_audit_v1" / "artifacts" / "SHA256_MANIFEST.json"
ARTIFACT_ROOT = DATA_ROOT / "second_harness_audit_v1" / "artifacts"
EXPECTED_RELATIVE_PATHS = (
    "code/runners/oracle-coupling/second_harness_audit_v1/README.md",
    "code/runners/oracle-coupling/second_harness_audit_v1/policy.sql",
    "code/runners/oracle-coupling/second_harness_audit_v1/sqlite_backend.py",
    "code/runners/oracle-coupling/second_harness_audit_v1/run_audit.py",
    "code/runners/oracle-coupling/second_harness_audit_v1/tests/test_second_backend.py",
    "code/runners/oracle-coupling/second_harness_audit_v1/verify_manifest.py",
    "fixtures/oracle-coupling/failure_to_executable_contract_v2.json",
    "data/reproduction/oracle-coupling/failure_to_executable_contract_v2/candidate_corpus.json",
    "data/reproduction/oracle-coupling/oracle_independent_compiler_v1/artifacts/compiled_contracts.json",
    "data/reproduction/oracle-coupling/oracle_independent_compiler_v1/artifacts/results.json",
    "data/reproduction/oracle-coupling/oracle_independent_compiler_v1/artifacts/SHA256_MANIFEST.json",
    "data/reproduction/oracle-coupling/second_harness_audit_v1/artifacts/compiler_parity.json",
    "data/reproduction/oracle-coupling/second_harness_audit_v1/artifacts/state_characterisation.json",
    "data/reproduction/oracle-coupling/second_harness_audit_v1/artifacts/audit_summary.json",
    "data/reproduction/oracle-coupling/second_harness_audit_v1/artifacts/per_candidate_results.csv",
    "code/runners/oracle-coupling/layout.py",
)


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def load_json(path: Path, failures: list[str]) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        failures.append(f"unreadable:{path.name}:{type(error).__name__}")
        return None


def verify_manifest_payload(payload: Any) -> dict[str, Any]:
    failures: list[str] = []
    if not isinstance(payload, dict):
        return {"entry_count": 0, "failures": ["schema:manifest_object"], "passed": False}
    expected_keys = {
        "manifest_version",
        "generated_at_utc",
        "entry_count",
        "entries_root_sha256",
        "files",
    }
    if set(payload) != expected_keys:
        failures.append("schema:exact_top_level_keys")
    if payload.get("manifest_version") != "SHAV1-exact-1":
        failures.append("schema:manifest_version")
    entries = payload.get("files")
    if not isinstance(entries, list):
        failures.append("schema:files")
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

    summary = load_json(ARTIFACT_ROOT / "audit_summary.json", failures)
    parity = load_json(ARTIFACT_ROOT / "compiler_parity.json", failures)
    states = load_json(ARTIFACT_ROOT / "state_characterisation.json", failures)
    oic = load_json(
        DATA_ROOT / "oracle_independent_compiler_v1" / "artifacts" / "results.json",
        failures,
    )
    try:
        with (ARTIFACT_ROOT / "per_candidate_results.csv").open(
            encoding="utf-8", newline=""
        ) as handle:
            candidate_rows = list(csv.DictReader(handle))
    except (OSError, UnicodeError, csv.Error) as error:
        failures.append(f"unreadable:per_candidate_results.csv:{type(error).__name__}")
        candidate_rows = []

    if not isinstance(summary, dict) or summary.get("protocol_id") != (
        "second-harness-audit-v1-sqlite-transactional-backend"
    ):
        failures.append("cross_file:summary:protocol_id")
    else:
        finite = summary.get("finite_corpus", {})
        expected = {
            "candidate_count": 392,
            "valid_accepted": 56,
            "invalid_rejected": 336,
            "classification_matches_label": 392,
            "rejected_state_unchanged": 336,
        }
        for key, value in expected.items():
            if finite.get(key) != value:
                failures.append(f"cross_file:summary:{key}")
    if not isinstance(parity, list) or len(parity) != 28 or not all(
        isinstance(row, dict)
        and row.get("semantic_parity_with_authored_expected_output") is True
        for row in parity
    ):
        failures.append("cross_file:compiler_parity")
    if (
        not isinstance(states, dict)
        or states.get("base_fixture_id") != "D-ST-01"
        or states.get("immutable_live_state_drift", {}).get(
            "rejected_by_preserved_live_state_check"
        )
        is not True
    ):
        failures.append("cross_file:state_characterisation")
    if not isinstance(oic, dict) or oic.get("overall_passed") is not True:
        failures.append("cross_file:oic_overall")
    if len(candidate_rows) != 392:
        failures.append("cross_file:candidate_row_count")

    return {
        "entry_count": len(entries),
        "verified_entries": verified if not failures else None,
        "failures": sorted(set(failures)),
        "passed": not failures,
    }


def verify_manifest() -> dict[str, Any]:
    try:
        payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        return {
            "manifest": str(MANIFEST.relative_to(REPO_ROOT)),
            "entry_count": 0,
            "verified_entries": None,
            "failures": [f"manifest_unreadable:{type(error).__name__}"],
            "passed": False,
        }
    result = verify_manifest_payload(payload)
    result["manifest"] = str(MANIFEST.relative_to(REPO_ROOT))
    return result


def main() -> int:
    result = verify_manifest()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
