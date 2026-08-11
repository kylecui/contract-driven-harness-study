#!/usr/bin/env python3
"""Run and bind the deterministic public-input metamorphic experiment."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


EXPERIMENT_ROOT = Path(__file__).resolve().parent
AUDIT_CODE_ROOT = EXPERIMENT_ROOT.parent
sys.path.insert(0, str(AUDIT_CODE_ROOT))

from layout import (  # noqa: E402
    BASE_SOURCE_COMMIT,
    DATA_ROOT,
    FIXTURE_ROOT,
    REPO_ROOT,
    base_snapshot_available,
    repo_relative,
    unexpected_worktree_paths,
)

OIC_ROOT = AUDIT_CODE_ROOT / "oracle_independent_compiler_v1"
OIC_DATA_ROOT = DATA_ROOT / "oracle_independent_compiler_v1"
PUBLIC_INPUT_PATH = OIC_DATA_ROOT / "artifacts" / "public_fixtures.json"
FEC_FIXTURES_PATH = FIXTURE_ROOT / "failure_to_executable_contract_v2.json"
ARTIFACT_ROOT = DATA_ROOT / "metamorphic_public_input_v1" / "artifacts"

sys.path.insert(0, str(OIC_ROOT))
sys.path.insert(0, str(EXPERIMENT_ROOT))

from metamorphic_suite import (  # noqa: E402
    INVARIANT_TRANSFORMS,
    SUPPORTED_FAMILIES,
    fixture_from_public_record,
    run_suite,
)
from verify_manifest import (  # noqa: E402
    EXPECTED_MANIFEST_PATHS,
    MANIFEST_VERSION,
)


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def build_manifest(source_commit: str) -> dict[str, Any]:
    entries = []
    for relative_path in sorted(EXPECTED_MANIFEST_PATHS):
        path = REPO_ROOT / relative_path
        if not path.is_file():
            raise FileNotFoundError(f"manifest input is missing: {relative_path}")
        entries.append({
            "path": relative_path,
            "sha256": sha256_path(path),
            "bytes": path.stat().st_size,
        })
    return {
        "manifest_version": MANIFEST_VERSION,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_snapshot_commit": source_commit,
        "entry_count": len(entries),
        "entries": entries,
    }


def main() -> None:
    source_payload = load_json(PUBLIC_INPUT_PATH)
    fixtures = [fixture_from_public_record(item) for item in source_payload["fixtures"]]
    source_commit = BASE_SOURCE_COMMIT
    base_available = base_snapshot_available()
    unexpected_before = unexpected_worktree_paths()

    test_command = [
        sys.executable,
        "-m",
        "unittest",
        "discover",
        "-s",
        str(EXPERIMENT_ROOT / "tests"),
        "-v",
    ]
    test_run = subprocess.run(
        test_command,
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    test_output = test_run.stdout + test_run.stderr
    test_count_match = re.search(r"Ran\s+(\d+)\s+tests?", test_output)
    reported_test_count = int(test_count_match.group(1)) if test_count_match else None

    protocol = {
        "protocol_id": "metamorphic-public-input-v1",
        "design_timing": "recorded_post_hoc_with_results_not_preregistered",
        "runtime": {
            "python_version": sys.version,
            "python_executable": Path(sys.executable).name,
        },
        "input_artifact": repo_relative(PUBLIC_INPUT_PATH),
        "input_artifact_sha256": sha256_path(PUBLIC_INPUT_PATH),
        "source_fixture_count": len(fixtures),
        "families": list(SUPPORTED_FAMILIES),
        "invariant_relations": list(INVARIANT_TRANSFORMS),
        "sensitivity_relations": {
            "all_baseline_apply_fixtures": [
                "remove_authority",
                "mismatch_authority_target",
                "mismatch_authorized_destination",
            ],
            "configuration_and_communication_baseline_apply_fixtures": [
                "mismatch_authority_scope",
                "expire_authority",
            ],
        },
        "input_boundary": (
            "Only the scrubbed OIC-v1 public-input artifact is loaded. The original "
            "authored fixture file is outside this experiment's runtime inputs."
        ),
        "evaluation_rule": (
            "Invariant cases require input change, exact normalized-contract equality, "
            "and raw grounding in transformed identifiers with no stale-value leakage. "
            "Sensitivity cases require an exact fail-closed execution projection, "
            "including blocked gate, no permitted action, family-specific next action, "
            "and exact state preservation."
        ),
        "analysis_unit": (
            "One base fixture is the primary task-level reporting unit; transformed "
            "cases are paired within-fixture deterministic repeated measures."
        ),
        "coverage_gate": (
            "The frozen 28-task, 5/5/3 apply, 112-invariant, 55-sensitivity, and "
            "family-by-relation profiles must all be exact and non-vacuous."
        ),
        "provenance_dependencies_not_runtime_inputs": [
            repo_relative(OIC_ROOT / "run_experiment.py"),
            repo_relative(OIC_DATA_ROOT / "artifacts" / "results.json"),
            repo_relative(OIC_DATA_ROOT / "artifacts" / "SHA256_MANIFEST.json"),
            repo_relative(FEC_FIXTURES_PATH),
        ],
    }
    results, cases = run_suite(fixtures)
    unexpected_after = unexpected_worktree_paths()
    results["generated_at_utc"] = datetime.now(timezone.utc).isoformat()
    results["source_public_input"] = {
        "path": repo_relative(PUBLIC_INPUT_PATH),
        "sha256": sha256_path(PUBLIC_INPUT_PATH),
    }
    results["source_snapshot"] = {
        "base_commit": source_commit,
        "base_commit_is_ancestor": base_available,
        "unexpected_paths_before": unexpected_before,
        "unexpected_paths_after": unexpected_after,
    }
    results["unit_test_execution"] = {
        "passed": test_run.returncode == 0 and reported_test_count == 12,
        "returncode": test_run.returncode,
        "reported_test_count": reported_test_count,
        "expected_test_count": 12,
        "command": [
            "python", "-m", "unittest", "discover", "-s",
            repo_relative(EXPERIMENT_ROOT / "tests"), "-v",
        ],
    }
    results["reproducibility_scope"] = (
        "Counts, case outcomes, and content hashes are deterministically recomputed. "
        "Generated timestamps mean regenerated JSON files are not claimed to be "
        "bit-for-bit identical across runs."
    )
    results["overall_passed"] = (
        results["overall_passed"]
        and results["unit_test_execution"]["passed"]
        and base_available
        and not unexpected_before
        and not unexpected_after
    )

    protocol_path = ARTIFACT_ROOT / "protocol.json"
    cases_path = ARTIFACT_ROOT / "cases.json"
    results_path = ARTIFACT_ROOT / "results.json"
    write_json(protocol_path, protocol)
    write_json(cases_path, {"protocol_id": protocol["protocol_id"], "cases": cases})
    write_json(results_path, results)

    manifest = build_manifest(source_commit)
    write_json(ARTIFACT_ROOT / "SHA256_MANIFEST.json", manifest)

    print(json.dumps({
        "overall_passed": results["overall_passed"],
        "base_fixture_count": results["base_fixture_count"],
        "baseline_apply_fixture_count": results["baseline_apply_fixture_count"],
        "invariant_cases_passed": results["invariant_cases_passed"],
        "invariant_case_count": results["invariant_case_count"],
        "sensitivity_cases_passed": results["sensitivity_cases_passed"],
        "sensitivity_case_count": results["sensitivity_case_count"],
        "coverage_gate_passed": results["coverage_gate"]["passed"],
        "unit_tests_passed": results["unit_test_execution"]["passed"],
        "unit_test_count": results["unit_test_execution"]["reported_test_count"],
        "manifest_entries": manifest["entry_count"],
    }, indent=2))
    if not results["overall_passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
