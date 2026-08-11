#!/usr/bin/env python3
"""Verify the exact, cross-bound IEBV1 evidence closure."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any


EXPERIMENT_ROOT = Path(__file__).resolve().parent
AUDIT_CODE_ROOT = EXPERIMENT_ROOT.parent
sys.path.insert(0, str(AUDIT_CODE_ROOT))

from layout import DATA_ROOT, REPO_ROOT  # noqa: E402

MANIFEST_PATH = DATA_ROOT / "invariant_external_boundary_v1" / "artifacts" / "SHA256_MANIFEST.json"
CODE_RELATIVE_ROOT = "code/runners/oracle-coupling/invariant_external_boundary_v1"
DATA_RELATIVE_ROOT = "data/reproduction/oracle-coupling/invariant_external_boundary_v1"
CASE_DEFINITIONS_RELATIVE_PATH = "fixtures/oracle-coupling/invariant_external_boundary_v1.json"
PROTOCOL_ID = "invariant-external-boundary-v1"

EXPECTED_SOURCE_COMMIT = "2340fe2d9cd619f73d5b67fa05bf8a08c7cad515"
EXPECTED_REPOSITORY_URL = "https://github.com/invariantlabs-ai/invariant"
EXPECTED_LICENSE_URL = (
    "https://github.com/invariantlabs-ai/invariant/blob/"
    f"{EXPECTED_SOURCE_COMMIT}/LICENSE"
)
EXPECTED_LICENSE_SPDX = "Apache-2.0"
EXPECTED_LICENSE_SHA256 = (
    "90154031b70befefac025106f493124530e13c608b876cc1418b5f65ba945f14"
)
EXPECTED_INVARIANT_PACKAGE_VERSION = "0.3.5"
EXPECTED_README_SHA256 = (
    "3fadddc4e6e97a01d6db4255690675a74db4c5435195fe913bc3087ca84e408d"
)
EXPECTED_PYPROJECT_SHA256 = (
    "7a16bd7a2b5761c3e5ecface9a344a301a575d68678585166467ed3d3a1aedfd"
)
EXPECTED_CASE_DEFINITIONS_SHA256 = (
    "a1df49d729d2007c190162d1dcb1bd0545431e9a4abef437ec5f38f52f624567"
)
EXPECTED_ISOLATED_WORKER_SHA256 = (
    "f40b5ae078ee74e99298813b98779cb0c32ca8d82f2366a286ac4c109ac36f9f"
)
EXPECTED_DISPATCHER_SOURCE_SHA256 = (
    "5823c491c877a13844661724f561808fa62c8b93e4469314b1ea7e1beb2b4ac9"
)
EXPECTED_POLICY_EVIDENCE = [
    {
        "policy_id": "upstream-readme-voldemort-message",
        "upstream_file": "README.md",
        "upstream_line_span": {"start": 50, "end": 52},
        "policy_source_sha256": (
            "6a622221e5e17d44e4da1fba970aeb628956f75ccf84587a4eacdd51872d43d6"
        ),
        "verbatim_in_upstream_readme": True,
    },
    {
        "policy_id": "upstream-readme-external-email",
        "upstream_file": "README.md",
        "upstream_line_span": {"start": 28, "end": 38},
        "policy_source_sha256": (
            "38847d7f409b4e7bc20bdb05bc95cb739f02632090bdaabb6b596b3fc5847d74"
        ),
        "verbatim_in_upstream_readme": True,
    },
]

EXPECTED_RELATIVE_PATHS = (
    f"{CODE_RELATIVE_ROOT}/README.md",
    f"{CODE_RELATIVE_ROOT}/external_boundary.py",
    f"{CODE_RELATIVE_ROOT}/isolated_evaluator.py",
    f"{CODE_RELATIVE_ROOT}/run_experiment.py",
    f"{CODE_RELATIVE_ROOT}/tests/test_invariant_external_boundary.py",
    f"{CODE_RELATIVE_ROOT}/verify_manifest.py",
    "code/runners/oracle-coupling/layout.py",
    f"{DATA_RELATIVE_ROOT}/artifacts/cases.json",
    f"{DATA_RELATIVE_ROOT}/artifacts/package_versions.json",
    f"{DATA_RELATIVE_ROOT}/artifacts/protocol.json",
    f"{DATA_RELATIVE_ROOT}/artifacts/results.json",
    f"{DATA_RELATIVE_ROOT}/artifacts/run_records.json",
    f"{DATA_RELATIVE_ROOT}/artifacts/source_snapshot.json",
    CASE_DEFINITIONS_RELATIVE_PATH,
)

EXPECTED_HEADERS = {
    "protocol_id": PROTOCOL_ID,
    "source_commit": EXPECTED_SOURCE_COMMIT,
    "source_repository_url": EXPECTED_REPOSITORY_URL,
    "source_license_url": EXPECTED_LICENSE_URL,
    "source_license_spdx": EXPECTED_LICENSE_SPDX,
    "source_license_sha256": EXPECTED_LICENSE_SHA256,
    "invariant_package_version": EXPECTED_INVARIANT_PACKAGE_VERSION,
    "upstream_readme_sha256": EXPECTED_README_SHA256,
    "upstream_pyproject_sha256": EXPECTED_PYPROJECT_SHA256,
    "upstream_policy_evidence": EXPECTED_POLICY_EVIDENCE,
    "case_definitions_sha256": EXPECTED_CASE_DEFINITIONS_SHA256,
    "isolated_worker_sha256": EXPECTED_ISOLATED_WORKER_SHA256,
    "dispatcher_source_sha256": EXPECTED_DISPATCHER_SOURCE_SHA256,
    "results_schema_version": "IEBV1-results-2",
}


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _load_json(project_root: Path, relative_path: str, failures: list[str]) -> Any:
    path = project_root / relative_path
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        failures.append(f"cross_file_unreadable:{relative_path}:{type(error).__name__}")
        return None


def build_manifest_payload(project_root: Path = REPO_ROOT) -> dict[str, Any]:
    """Build only the frozen exact path set; verification still cross-binds it."""

    entries = []
    for relative_text in EXPECTED_RELATIVE_PATHS:
        path = project_root / relative_text
        entries.append(
            {
                "path": relative_text,
                "sha256": sha256_path(path),
                "bytes": path.stat().st_size,
            }
        )
    return {
        "manifest_version": "IEBV1-strict-3",
        "expected_headers": EXPECTED_HEADERS,
        "entry_count": len(entries),
        "entries_root_sha256": hashlib.sha256(
            canonical_json(entries).encode("utf-8")
        ).hexdigest(),
        "entries": entries,
    }


def verify_manifest_payload(
    manifest: Any,
    project_root: Path = REPO_ROOT,
) -> dict[str, Any]:
    failures: list[str] = []
    if not isinstance(manifest, dict):
        return {
            "entry_count": 0,
            "verified_entries": None,
            "failures": ["schema:manifest_object"],
            "passed": False,
        }

    expected_top_keys = {
        "manifest_version",
        "expected_headers",
        "entry_count",
        "entries_root_sha256",
        "entries",
    }
    if set(manifest) != expected_top_keys:
        failures.append("schema:exact_top_level_keys")
    if manifest.get("manifest_version") != "IEBV1-strict-3":
        failures.append("schema:manifest_version")

    headers = manifest.get("expected_headers")
    if not isinstance(headers, dict):
        failures.append("schema:expected_headers")
        headers = {}
    if set(headers) != set(EXPECTED_HEADERS):
        failures.append("schema:exact_expected_header_keys")
    for key, expected in EXPECTED_HEADERS.items():
        if headers.get(key) != expected:
            failures.append(f"expected_header:{key}")

    entries = manifest.get("entries")
    if not isinstance(entries, list):
        failures.append("schema:entries")
        entries = []
    if manifest.get("entry_count") != len(entries):
        failures.append("schema:entry_count_matches_entries")
    if manifest.get("entry_count") != len(EXPECTED_RELATIVE_PATHS):
        failures.append("schema:entry_count_expected")

    entry_paths: list[str] = []
    for entry in entries:
        if not isinstance(entry, dict) or set(entry) != {"path", "sha256", "bytes"}:
            failures.append("schema:entry_shape")
            continue
        if not isinstance(entry.get("path"), str):
            failures.append("schema:entry_path_type")
            continue
        entry_paths.append(entry["path"])
    if len(entry_paths) != len(set(entry_paths)):
        failures.append("schema:duplicate_path")
    if set(entry_paths) != set(EXPECTED_RELATIVE_PATHS):
        failures.append("schema:exact_path_set")

    expected_root = hashlib.sha256(canonical_json(entries).encode("utf-8")).hexdigest()
    if manifest.get("entries_root_sha256") != expected_root:
        failures.append("schema:entries_root_sha256")

    verified_file_count = 0
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
        path = (project_root / relative).resolve()
        try:
            path.relative_to(project_root.resolve())
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
            verified_file_count += 1

    source = _load_json(project_root, f"{DATA_RELATIVE_ROOT}/artifacts/source_snapshot.json", failures)
    packages = _load_json(project_root, f"{DATA_RELATIVE_ROOT}/artifacts/package_versions.json", failures)
    protocol = _load_json(project_root, f"{DATA_RELATIVE_ROOT}/artifacts/protocol.json", failures)
    cases = _load_json(project_root, f"{DATA_RELATIVE_ROOT}/artifacts/cases.json", failures)
    results = _load_json(project_root, f"{DATA_RELATIVE_ROOT}/artifacts/results.json", failures)
    run_records = _load_json(project_root, f"{DATA_RELATIVE_ROOT}/artifacts/run_records.json", failures)
    definitions = _load_json(project_root, CASE_DEFINITIONS_RELATIVE_PATH, failures)

    if isinstance(source, dict):
        source_checks = {
            "source_commit": source.get("source_commit") == EXPECTED_SOURCE_COMMIT,
            "repository_url": source.get("repository_url") == EXPECTED_REPOSITORY_URL,
            "observed_origin_url": source.get("observed_origin_url")
            in {EXPECTED_REPOSITORY_URL, f"{EXPECTED_REPOSITORY_URL}.git"},
            "license_url": source.get("license_url") == EXPECTED_LICENSE_URL,
            "license_spdx": source.get("license_spdx") == EXPECTED_LICENSE_SPDX,
            "license_sha256": source.get("license_sha256")
            == EXPECTED_LICENSE_SHA256,
            "readme_sha256": source.get("readme_sha256") == EXPECTED_README_SHA256,
            "pyproject_sha256": source.get("pyproject_sha256")
            == EXPECTED_PYPROJECT_SHA256,
            "upstream_policy_evidence": source.get("upstream_policy_evidence")
            == EXPECTED_POLICY_EVIDENCE,
            "isolated_worker_sha256": (
                source.get("isolated_worker", {}).get("worker_sha256")
                if isinstance(source.get("isolated_worker"), dict)
                else None
            )
            == EXPECTED_ISOLATED_WORKER_SHA256,
            "dispatcher_source_sha256": (
                source.get("production_dispatcher", {}).get(
                    "dispatcher_source_sha256"
                )
                if isinstance(source.get("production_dispatcher"), dict)
                else None
            )
            == EXPECTED_DISPATCHER_SOURCE_SHA256,
            "dispatcher_closure_passed": (
                source.get("production_dispatcher", {}).get("passed")
                if isinstance(source.get("production_dispatcher"), dict)
                else None
            )
            is True,
        }
        failures.extend(
            f"cross_file:source_snapshot:{key}"
            for key, passed in source_checks.items()
            if not passed
        )

    if not isinstance(packages, dict) or packages.get("packages", {}).get(
        "invariant-ai"
    ) != EXPECTED_INVARIANT_PACKAGE_VERSION:
        failures.append("cross_file:package_versions:invariant-ai")

    for name, payload in (
        ("protocol", protocol),
        ("cases", cases),
        ("results", results),
        ("run_records", run_records),
        ("case_definitions", definitions),
    ):
        if not isinstance(payload, dict) or payload.get("protocol_id") != PROTOCOL_ID:
            failures.append(f"cross_file:{name}:protocol_id")

    definitions_path = project_root / CASE_DEFINITIONS_RELATIVE_PATH
    worker_path = project_root / CODE_RELATIVE_ROOT / "isolated_evaluator.py"
    if definitions_path.is_file() and sha256_path(definitions_path) != EXPECTED_CASE_DEFINITIONS_SHA256:
        failures.append("cross_file:case_definitions:sha256")
    if worker_path.is_file() and sha256_path(worker_path) != EXPECTED_ISOLATED_WORKER_SHA256:
        failures.append("cross_file:isolated_worker:sha256")
    if isinstance(cases, dict):
        if cases.get("source_case_definitions_sha256") != EXPECTED_CASE_DEFINITIONS_SHA256:
            failures.append("cross_file:cases:source_case_definitions_sha256")
        if isinstance(definitions, dict) and cases.get("base_cases") != definitions.get(
            "base_cases"
        ):
            failures.append("cross_file:cases:base_cases")
    if isinstance(results, dict):
        if results.get("schema_version") != "IEBV1-results-2":
            failures.append("cross_file:results:schema_version")
        if results.get("source_commit") != EXPECTED_SOURCE_COMMIT:
            failures.append("cross_file:results:source_commit")
        if results.get("source_license_sha256") != EXPECTED_LICENSE_SHA256:
            failures.append("cross_file:results:source_license_sha256")
        dispatcher = results.get("production_dispatcher")
        if (
            not isinstance(dispatcher, dict)
            or dispatcher.get("dispatcher_source_sha256")
            != EXPECTED_DISPATCHER_SOURCE_SHA256
            or dispatcher.get("passed") is not True
        ):
            failures.append("cross_file:results:production_dispatcher")
    if isinstance(protocol, dict):
        boundary = protocol.get("external_evaluator_boundary")
        if (
            not isinstance(boundary, dict)
            or boundary.get("dispatcher_source_sha256")
            != EXPECTED_DISPATCHER_SOURCE_SHA256
        ):
            failures.append("cross_file:protocol:dispatcher_source_sha256")
    if isinstance(run_records, dict):
        runs = run_records.get("runs")
        if not isinstance(runs, list) or len(runs) != 18:
            failures.append("cross_file:run_records:exact_run_count")
        elif any(
            run.get("isolated_worker_sha256") != EXPECTED_ISOLATED_WORKER_SHA256
            for run in runs
            if isinstance(run, dict)
        ):
            failures.append("cross_file:run_records:isolated_worker_sha256")

    return {
        "entry_count": len(entries),
        "verified_entries": verified_file_count if not failures else None,
        "failures": sorted(set(failures)),
        "passed": not failures,
    }


def verify_manifest() -> dict[str, Any]:
    try:
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        return {
            "manifest": str(MANIFEST_PATH.relative_to(REPO_ROOT)),
            "entry_count": 0,
            "verified_entries": None,
            "failures": [f"manifest_unreadable:{type(error).__name__}"],
            "passed": False,
        }
    result = verify_manifest_payload(manifest)
    result["manifest"] = str(MANIFEST_PATH.relative_to(REPO_ROOT))
    return result


def main() -> None:
    result = verify_manifest()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if not result["passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
