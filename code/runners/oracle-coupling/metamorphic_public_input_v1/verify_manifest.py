#!/usr/bin/env python3
"""Verify the exact MPIV1 release closure bound by its manifest."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


EXPERIMENT_ROOT = Path(__file__).resolve().parent
AUDIT_CODE_ROOT = EXPERIMENT_ROOT.parent
sys.path.insert(0, str(AUDIT_CODE_ROOT))

from layout import BASE_SOURCE_COMMIT, DATA_ROOT, REPO_ROOT  # noqa: E402


MANIFEST_VERSION = "MPIV1-strict-2"
MANIFEST_PATH = DATA_ROOT / "metamorphic_public_input_v1" / "artifacts" / "SHA256_MANIFEST.json"
EXPECTED_MANIFEST_PATHS = frozenset({
    "code/runners/oracle-coupling/layout.py",
    "code/runners/oracle-coupling/metamorphic_public_input_v1/README.md",
    "code/runners/oracle-coupling/metamorphic_public_input_v1/metamorphic_suite.py",
    "code/runners/oracle-coupling/metamorphic_public_input_v1/run_experiment.py",
    "code/runners/oracle-coupling/metamorphic_public_input_v1/tests/test_metamorphic_public_input.py",
    "code/runners/oracle-coupling/metamorphic_public_input_v1/verify_manifest.py",
    "code/runners/oracle-coupling/oracle_independent_compiler_v1/policy_rules.py",
    "code/runners/oracle-coupling/oracle_independent_compiler_v1/public_input.py",
    "code/runners/oracle-coupling/oracle_independent_compiler_v1/public_policy_compiler.py",
    "code/runners/oracle-coupling/oracle_independent_compiler_v1/run_experiment.py",
    "data/reproduction/oracle-coupling/metamorphic_public_input_v1/artifacts/cases.json",
    "data/reproduction/oracle-coupling/metamorphic_public_input_v1/artifacts/protocol.json",
    "data/reproduction/oracle-coupling/metamorphic_public_input_v1/artifacts/results.json",
    "data/reproduction/oracle-coupling/oracle_independent_compiler_v1/artifacts/SHA256_MANIFEST.json",
    "data/reproduction/oracle-coupling/oracle_independent_compiler_v1/artifacts/public_fixtures.json",
    "data/reproduction/oracle-coupling/oracle_independent_compiler_v1/artifacts/results.json",
    "fixtures/oracle-coupling/failure_to_executable_contract_v2.json",
})
EXPECTED_TOP_LEVEL_KEYS = {
    "manifest_version",
    "generated_at_utc",
    "source_snapshot_commit",
    "entry_count",
    "entries",
}
EXPECTED_ENTRY_KEYS = {"path", "sha256", "bytes"}
SHA256_PATTERN = re.compile(r"[0-9a-f]{64}\Z")


def verify_manifest_payload(manifest: Any) -> list[str]:
    """Return stable failure labels for any schema, closure, or content defect."""
    failures: list[str] = []
    if not isinstance(manifest, dict):
        return ["schema:manifest"]

    if set(manifest) != EXPECTED_TOP_LEVEL_KEYS:
        failures.append("schema:top_level_keys")
    if manifest.get("manifest_version") != MANIFEST_VERSION:
        failures.append("schema:manifest_version")
    if manifest.get("source_snapshot_commit") != BASE_SOURCE_COMMIT:
        failures.append("schema:source_snapshot_commit")
    generated_at = manifest.get("generated_at_utc")
    if not isinstance(generated_at, str):
        failures.append("schema:generated_at_utc")
    else:
        try:
            parsed = datetime.fromisoformat(generated_at)
            if parsed.tzinfo is None or parsed.utcoffset() is None:
                failures.append("schema:generated_at_utc")
        except ValueError:
            failures.append("schema:generated_at_utc")

    entries = manifest.get("entries")
    if not isinstance(entries, list):
        failures.append("schema:entries")
        entries = []
    if manifest.get("entry_count") != len(EXPECTED_MANIFEST_PATHS):
        failures.append("schema:entry_count_expected")
    if manifest.get("entry_count") != len(entries):
        failures.append("schema:entry_count_actual")

    observed_paths: list[str] = []
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict) or set(entry) != EXPECTED_ENTRY_KEYS:
            failures.append(f"schema:entry_shape:{index}")
            continue
        relative_text = entry["path"]
        sha256 = entry["sha256"]
        byte_count = entry["bytes"]
        if not isinstance(relative_text, str) or not relative_text:
            failures.append(f"schema:path:{index}")
            continue
        observed_paths.append(relative_text)
        if not isinstance(sha256, str) or SHA256_PATTERN.fullmatch(sha256) is None:
            failures.append(f"schema:sha256:{relative_text}")
        if not isinstance(byte_count, int) or isinstance(byte_count, bool) or byte_count < 0:
            failures.append(f"schema:bytes:{relative_text}")

        relative = Path(relative_text)
        if relative.is_absolute():
            failures.append(f"path:absolute:{relative_text}")
            continue
        if ".." in relative.parts:
            failures.append(f"path:parent:{relative_text}")
            continue
        path = (REPO_ROOT / relative).resolve()
        try:
            path.relative_to(REPO_ROOT.resolve())
        except ValueError:
            failures.append(f"path:outbound:{relative_text}")
            continue
        if not path.is_file():
            failures.append(f"missing:{relative_text}")
            continue
        observed = hashlib.sha256(path.read_bytes()).hexdigest()
        if observed != sha256:
            failures.append(f"sha256:{relative_text}")
        if path.stat().st_size != byte_count:
            failures.append(f"bytes:{relative_text}")

    if len(observed_paths) != len(set(observed_paths)):
        failures.append("schema:duplicate_path")
    observed_set = set(observed_paths)
    failures.extend(
        f"paths:missing:{path}" for path in sorted(EXPECTED_MANIFEST_PATHS - observed_set)
    )
    failures.extend(
        f"paths:unexpected:{path}" for path in sorted(observed_set - EXPECTED_MANIFEST_PATHS)
    )
    return failures


def main() -> None:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    failures = verify_manifest_payload(manifest)
    print(json.dumps({
        "manifest": str(MANIFEST_PATH.relative_to(REPO_ROOT)),
        "verified_entries": len(EXPECTED_MANIFEST_PATHS) if not failures else None,
        "entry_count": len(manifest.get("entries", [])) if isinstance(manifest, dict) else 0,
        "expected_entry_count": len(EXPECTED_MANIFEST_PATHS),
        "failures": failures,
        "passed": not failures,
    }, indent=2))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
