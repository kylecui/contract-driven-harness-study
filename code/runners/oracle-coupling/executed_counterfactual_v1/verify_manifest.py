#!/usr/bin/env python3
"""Verify the executed_counterfactual_v1 SHA-256 manifest (house pattern)."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path, PurePosixPath

AUDIT_CODE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(AUDIT_CODE_ROOT))

from layout import REPO_ROOT  # noqa: E402

MODULE = "executed_counterfactual_v1"
MANIFEST_VERSION = "ECF-v1-exact-1"
DATA_ROOT = (
    REPO_ROOT / "data/reproduction/oracle-coupling" / MODULE
)
MANIFEST_PATH = DATA_ROOT / "SHA256_MANIFEST.json"

EXPECTED_RELATIVE_PATHS = frozenset(
    {
        "code/runners/oracle-coupling/executed_counterfactual_v1/README.md",
        "code/runners/oracle-coupling/executed_counterfactual_v1/run_counterfactual.py",
        "code/runners/oracle-coupling/executed_counterfactual_v1/verify_manifest.py",
        "code/runners/oracle-coupling/executed_counterfactual_v1/tests/test_executed_counterfactual.py",
        "code/runners/oracle-coupling/failure_to_executable_contract_v2/contract_gate.py",
        "code/runners/oracle-coupling/layout.py",
        "fixtures/oracle-coupling/failure_to_executable_contract_v2.json",
        "data/reproduction/oracle-coupling/failure_to_executable_contract_v2/candidate_corpus.json",
        "data/reproduction/oracle-coupling/executed_counterfactual_v1/artifacts/results.json",
    }
)


def canonical_json(value: object) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    failures: list[str] = []
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

    if manifest.get("manifest_version") != MANIFEST_VERSION:
        failures.append(
            f"manifest_version:{manifest.get('manifest_version')}"
        )
    if not re.match(
        r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}", str(manifest.get("generated_at_utc", ""))
    ):
        failures.append("generated_at_utc:not ISO-8601")

    entries = manifest.get("entries", [])
    if manifest.get("entry_count") != len(entries):
        failures.append("entry_count_mismatch")
    if manifest.get("entries_root_sha256") != hashlib.sha256(
        canonical_json(entries)
    ).hexdigest():
        failures.append("entries_root_sha256_mismatch")
    if manifest.get("entry_count") != len(EXPECTED_RELATIVE_PATHS):
        failures.append("entry_count_unexpected")

    seen: set[str] = set()
    for entry in entries:
        relative_text = entry.get("path", "")
        relative = PurePosixPath(relative_text)
        if relative_text in seen:
            failures.append(f"paths:duplicate:{relative_text}")
        seen.add(relative_text)
        if relative_text not in EXPECTED_RELATIVE_PATHS:
            failures.append(f"paths:unexpected:{relative_text}")
            continue
        if relative.is_absolute():
            failures.append(f"path:absolute:{relative_text}")
            continue
        if ".." in relative.parts:
            failures.append(f"path:parent:{relative_text}")
            continue
        path = (REPO_ROOT / relative_text).resolve()
        try:
            path.relative_to(REPO_ROOT.resolve())
        except ValueError:
            failures.append(f"path:outbound:{relative_text}")
            continue
        if not path.is_file():
            failures.append(f"missing:{relative_text}")
            continue
        if entry.get("sha256") != sha256(path):
            failures.append(f"sha256:{relative_text}")
        if entry.get("bytes") != path.stat().st_size:
            failures.append(f"bytes:{relative_text}")

    for expected in sorted(EXPECTED_RELATIVE_PATHS - seen):
        failures.append(f"paths:missing:{expected}")

    results = json.loads(
        (DATA_ROOT / "artifacts/results.json").read_text(encoding="utf-8")
    )
    if results.get("protocol_id") != "ECF-v1":
        failures.append("results:protocol_id")
    if results.get("overall_passed") is not True:
        failures.append("results:overall_passed_not_true")

    if failures:
        print(json.dumps({"verified": False, "failures": failures}, indent=2))
        return 1
    print(
        json.dumps(
            {
                "verified": True,
                "manifest_version": MANIFEST_VERSION,
                "entries": len(entries),
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
