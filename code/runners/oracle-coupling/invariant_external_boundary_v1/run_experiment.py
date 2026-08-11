#!/usr/bin/env python3
"""Test, run, and freeze the pinned Invariant boundary-control evidence."""

from __future__ import annotations

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

from layout import DATA_ROOT, REPO_ROOT, repo_relative  # noqa: E402

ARTIFACT_ROOT = DATA_ROOT / "invariant_external_boundary_v1" / "artifacts"
EXPECTED_TEST_COUNT = 16

sys.path.insert(0, str(EXPERIMENT_ROOT))

from external_boundary import (  # noqa: E402
    CASE_DEFINITIONS_PATH,
    EXPECTED_SOURCE_COMMIT,
    LABEL_CONDITIONS,
    POLICIES,
    UPSTREAM_SOURCE_ROOT,
    git_output,
    load_case_definitions,
    run_suite,
    runtime_package_versions,
    sha256_path,
    validate_upstream_environment,
)
from verify_manifest import build_manifest_payload, verify_manifest  # noqa: E402


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def main() -> None:
    source_status_before = git_output("status", "--porcelain")
    definitions = load_case_definitions()
    source_snapshot = validate_upstream_environment()

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
    tests_passed = (
        test_run.returncode == 0 and reported_test_count == EXPECTED_TEST_COUNT
    )
    if not tests_passed:
        print(test_output)
        raise SystemExit("tests failed; artifacts were not frozen")

    results, runs = run_suite(definitions)
    source_status_after = git_output("status", "--porcelain")
    source_snapshot["source_clean_before_run"] = source_status_before == ""
    source_snapshot["source_clean_after_run"] = source_status_after == ""
    source_snapshot["source_status_after_porcelain"] = source_status_after
    source_snapshot["source_root_is_external_temp_snapshot"] = True

    protocol = {
        "schema_version": "IEBV1-protocol-2",
        "protocol_id": definitions["protocol_id"],
        "task_contract": {
            "objective": (
                "Test whether the pinned external Invariant parser/evaluator produces "
                "the same policy source hash and decision when a separate answer-label "
                "payload is original, deleted, or poisoned, while still responding in "
                "both directions to paired public-trace and fixed-trace policy-source edits."
            ),
            "deliverable": (
                "A deterministic, zero-model-call external evaluator boundary control "
                "with cases, results, source evidence, tests, and SHA closure."
            ),
            "scope": (
                "Two verbatim official README policies, two locally authored public-trace "
                "pairs, and two locally authored policy-source mediation controls. No "
                "model calls are made; the control remains bounded to the declared "
                "evaluator interface."
            ),
            "success_criteria": [
                "Pinned source commit, Apache-2.0 license hash, package version, and import path validate.",
                "Sixteen acceptance and adversarial tests pass before artifact freeze.",
                "Eighteen isolated external-evaluator calls complete with zero model calls.",
                "All six label-invariance groups preserve policy source, hash, evaluator input, and decision.",
                "Both paired public-fact edits change the decision in opposite expected directions under all label conditions.",
                "Both fixed-trace policy-source mutations change the decision in opposite expected directions under all label conditions.",
                "The evaluator child receives only policy source and public trace; answer-label payloads remain outside its process and scoring occurs afterward.",
                "The exact 14-path manifest and all frozen source headers pass cross-file verification.",
            ],
            "non_completion_states": [
                "external_defect_replication_not_tested",
                "independent_task_authorship_not_met",
                "check_to_commit_not_tested",
                "generalization_not_established",
            ],
        },
        "external_evaluator_boundary": {
            "parent_call": "python -I isolated_evaluator.py",
            "worker_call": "LocalPolicy.from_string(policy_source).analyze(public_trace)",
            "accepted_arguments": ["policy_source", "public_trace"],
            "excluded_argument": "answer_label_payload",
            "worker_sha256": source_snapshot["isolated_worker"]["worker_sha256"],
            "closure_gate": source_snapshot["isolated_worker"]["checks"],
            "dispatcher_source_sha256": source_snapshot["production_dispatcher"][
                "dispatcher_source_sha256"
            ],
            "dispatcher_closure_gate": source_snapshot["production_dispatcher"][
                "checks"
            ],
            "decision_projection": (
                "one or more external AnalysisResult.errors -> violation_detected; "
                "zero errors -> no_violation_detected"
            ),
        },
        "run_matrix": {
            "base_cases": 2,
            "official_policy_public_conditions_per_case": 2,
            "fixed_trace_policy_source_mutations_per_case": 1,
            "label_conditions": list(LABEL_CONDITIONS),
            "external_evaluator_calls": 18,
            "model_calls": 0,
        },
        "upstream_policy_ids": sorted(POLICIES),
        "paired_control_rule": (
            "Within each public trace, original/deleted/poisoned label payloads must "
            "change payload hashes but not evaluator inputs or decisions. Within each "
            "label condition, the declared one-leaf public edit must change the decision; "
            "with the baseline public trace fixed, the declared policy-source mutation "
            "must also change the decision."
        ),
        "analysis_unit": (
            "One locally authored base case is the primary descriptive unit; the eighteen "
            "runs are nested deterministic checks, not independent statistical samples."
        ),
        "claim_boundary": (
            "This is an external evaluator boundary control. It is not an external "
            "replication of the original defect, not independently authored task evidence, "
            "and not evidence of atomic enforcement or check-to-commit integrity."
        ),
    }

    cases_artifact = {
        "schema_version": "IEBV1-expanded-cases-2",
        "protocol_id": definitions["protocol_id"],
        "source_case_definitions": repo_relative(CASE_DEFINITIONS_PATH),
        "source_case_definitions_sha256": sha256_path(CASE_DEFINITIONS_PATH),
        "base_cases": definitions["base_cases"],
        "expanded_run_ids": [run["run_id"] for run in runs],
    }
    package_versions = runtime_package_versions()
    results["generated_at_utc"] = datetime.now(timezone.utc).isoformat()
    results["source_commit"] = source_snapshot["source_commit"]
    results["source_license_sha256"] = source_snapshot["license_sha256"]
    results["unit_test_execution"] = {
        "passed": tests_passed,
        "expected_test_count": EXPECTED_TEST_COUNT,
        "reported_test_count": reported_test_count,
        "returncode": test_run.returncode,
        "command": [
            "python", "-m", "unittest", "discover", "-s",
            repo_relative(EXPERIMENT_ROOT / "tests"), "-v",
        ],
    }
    results["source_snapshot_clean"] = (
        source_snapshot["source_clean_before_run"]
        and source_snapshot["source_clean_after_run"]
    )
    results["overall_passed"] = (
        results["overall_passed"]
        and tests_passed
        and results["source_snapshot_clean"]
        and source_snapshot["source_commit"] == EXPECTED_SOURCE_COMMIT
    )

    artifact_paths = {
        "protocol": ARTIFACT_ROOT / "protocol.json",
        "cases": ARTIFACT_ROOT / "cases.json",
        "results": ARTIFACT_ROOT / "results.json",
        "run_records": ARTIFACT_ROOT / "run_records.json",
        "source_snapshot": ARTIFACT_ROOT / "source_snapshot.json",
        "package_versions": ARTIFACT_ROOT / "package_versions.json",
    }
    write_json(artifact_paths["protocol"], protocol)
    write_json(artifact_paths["cases"], cases_artifact)
    write_json(artifact_paths["results"], results)
    write_json(
        artifact_paths["run_records"],
        {
            "schema_version": "IEBV1-run-records-2",
            "protocol_id": definitions["protocol_id"],
            "runs": runs,
        },
    )
    write_json(artifact_paths["source_snapshot"], source_snapshot)
    write_json(artifact_paths["package_versions"], package_versions)

    summary = {
        "overall_passed": results["overall_passed"],
        "source_commit": source_snapshot["source_commit"],
        "license_sha256": source_snapshot["license_sha256"],
        "package_version": package_versions["packages"]["invariant-ai"],
        "base_case_count": results["base_case_count"],
        "external_evaluator_call_count": results["external_evaluator_call_count"],
        "model_call_count": results["model_call_count"],
        "label_invariance_groups_passed": sum(
            group["passed"] for group in results["label_invariance_groups"]
        ),
        "label_invariance_group_count": len(results["label_invariance_groups"]),
        "public_fact_relations_passed": sum(
            relation["passed"] for relation in results["public_fact_relations"]
        ),
        "public_fact_relation_count": len(results["public_fact_relations"]),
        "policy_source_relations_passed": sum(
            relation["passed"] for relation in results["policy_source_relations"]
        ),
        "policy_source_relation_count": len(results["policy_source_relations"]),
        "unit_tests_passed": tests_passed,
        "unit_test_count": reported_test_count,
    }
    manifest = build_manifest_payload(REPO_ROOT)
    write_json(ARTIFACT_ROOT / "SHA256_MANIFEST.json", manifest)
    manifest_check = verify_manifest()
    if not manifest_check["passed"]:
        raise SystemExit(f"manifest verification failed: {manifest_check['failures']}")
    summary["manifest_entry_count"] = manifest["entry_count"]
    summary["manifest_entries_root_sha256"] = manifest["entries_root_sha256"]
    summary["manifest_verified"] = True
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if not results["overall_passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
