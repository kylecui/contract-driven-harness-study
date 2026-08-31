#!/usr/bin/env python3
"""Executed answer-field counterfactuals for the coupled FEC-v2 gate.

Follows the two answer-side interventions described in the working paper
(§3.2/§4.1, Supplementary Note 1) into execution on fixture D-ST-01:

1. Target counterfactual — change ONLY the answer-derived destination in
   ``expected_output.state_patch[0].to``; the accepted write redirects to
   the replacement destination and the previously canonical proposal is
   rejected with ``wrong_target_state``.
2. Evidence counterfactual — change ONLY the answer-derived decision
   evidence binding in ``expected_output.evidence_bindings``; the gate now
   requires the distractor record (``decision_evidence_mismatch`` for the
   canonical binding, acceptance for the distractor binding).

Both cases are mechanism witnesses on a single fixture: they establish that
the compile-time answer dependence reaches the write point. They are not
task samples and carry no prevalence claim. Public inputs (request, state,
evidence set, obligations) are held fixed; only ``expected_output`` fields
are edited, mirroring the poisoning interventions at execution level.
"""

from __future__ import annotations

import copy
import hashlib
import json
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

AUDIT_CODE_ROOT = Path(__file__).resolve().parents[1]
FEC_ROOT = AUDIT_CODE_ROOT / "failure_to_executable_contract_v2"
sys.path.insert(0, str(AUDIT_CODE_ROOT))
sys.path.insert(0, str(FEC_ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from layout import REPO_ROOT  # noqa: E402

from contract_gate import (  # noqa: E402
    ExecutableContract,
    execute_in_sandbox,
)

FIXTURES_PATH = REPO_ROOT / "fixtures/oracle-coupling/failure_to_executable_contract_v2.json"
CORPUS_PATH = REPO_ROOT / "data/reproduction/oracle-coupling/failure_to_executable_contract_v2/candidate_corpus.json"
OUTPUT_DIR = REPO_ROOT / "data/reproduction/oracle-coupling/executed_counterfactual_v1/artifacts"
FIXTURE_ID = "D-ST-01"
REPLACEMENT_DESTINATION = "on_hold"
MANIFEST_VERSION = "ECF-v1-exact-1"


def load_fixture() -> dict:
    data = json.loads(FIXTURES_PATH.read_text(encoding="utf-8"))
    for fixture in data["fixtures"]:
        if fixture["fixture_id"] == FIXTURE_ID:
            return fixture
    raise SystemExit(f"fixture {FIXTURE_ID} not found")


def load_canonical_candidate() -> dict:
    corpus = json.loads(CORPUS_PATH.read_text(encoding="utf-8"))
    for entry in corpus:
        if entry["fixture_id"] == FIXTURE_ID and entry["candidate_id"] == "valid_golden":
            return copy.deepcopy(entry["value"])
    raise SystemExit("canonical candidate not found")


def run_case(
    label: str,
    fixture: dict,
    candidate: dict,
    expected_accepted: bool,
    expected_reason_substring: str | None,
) -> dict:
    contract = ExecutableContract.compile(fixture)
    with tempfile.TemporaryDirectory() as tmp:
        state_path = Path(tmp) / "state.json"
        state_path.write_text(
            json.dumps(fixture["initial_state"], ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        trace = execute_in_sandbox(contract, candidate, state_path)
        after = json.loads(state_path.read_text(encoding="utf-8"))
    reasons = list(trace["reason_codes"])
    accepted = bool(trace["accepted"])
    ok = accepted == expected_accepted and (
        expected_reason_substring is None
        or any(expected_reason_substring in reason for reason in reasons)
    )
    return {
        "label": label,
        "accepted": accepted,
        "reason_codes": reasons,
        "wrote": bool(trace["wrote"]),
        "before_hash": trace["before_hash"],
        "after_hash": trace["after_hash"],
        "observed_project_status": after.get("project.status"),
        "passed": ok,
    }


def build_cases() -> dict:
    fixture = load_fixture()
    canonical = load_canonical_candidate()
    distractor_id = fixture["obligations"]["distractor_evidence_ids"][0]

    baseline = run_case(
        "baseline_canonical", fixture, canonical, True, None
    )

    target_fixture = copy.deepcopy(fixture)
    old_to = target_fixture["expected_output"]["state_patch"][0]["to"]
    target_fixture["expected_output"]["state_patch"][0]["to"] = REPLACEMENT_DESTINATION
    target_canonical = run_case(
        "target_cf_canonical_rejected",
        target_fixture,
        canonical,
        False,
        "wrong_target_state",
    )
    redirected = copy.deepcopy(canonical)
    redirected["state_patch"][0]["to"] = REPLACEMENT_DESTINATION
    target_adapted = run_case(
        "target_cf_adapted_writes_replacement",
        target_fixture,
        redirected,
        True,
        None,
    )

    evidence_fixture = copy.deepcopy(fixture)
    binding = evidence_fixture["expected_output"]["evidence_bindings"]
    old_binding = list(
        item["evidence_ids"]
        for item in binding
        if item["slot_id"] == "decision"
    )[0]
    for item in binding:
        if item["slot_id"] == "decision":
            item["evidence_ids"] = [distractor_id]
    evidence_canonical = run_case(
        "evidence_cf_canonical_rejected",
        evidence_fixture,
        canonical,
        False,
        "decision_evidence_mismatch",
    )
    distractor_proposal = copy.deepcopy(canonical)
    for item in distractor_proposal["evidence_bindings"]:
        if item["slot_id"] == "decision":
            item["evidence_ids"] = [distractor_id]
    evidence_adapted = run_case(
        "evidence_cf_distractor_binding_accepted",
        evidence_fixture,
        distractor_proposal,
        True,
        None,
    )

    checks = {
        "baseline_writes_expected_destination": baseline["passed"]
        and baseline["observed_project_status"] == old_to,
        "target_redirects_accepted_write": target_canonical["passed"]
        and target_adapted["passed"]
        and target_adapted["wrote"]
        and target_adapted["observed_project_status"] == REPLACEMENT_DESTINATION,
        "evidence_requires_distractor": evidence_canonical["passed"]
        and evidence_adapted["passed"]
        and evidence_adapted["accepted"],
    }
    return {
        "protocol_id": "ECF-v1",
        "fixture_id": FIXTURE_ID,
        "interventions": {
            "target_counterfactual": {
                "field": "expected_output.state_patch[0].to",
                "old": old_to,
                "new": REPLACEMENT_DESTINATION,
            },
            "evidence_counterfactual": {
                "field": "expected_output.evidence_bindings[decision].evidence_ids",
                "old": old_binding,
                "new": [distractor_id],
            },
        },
        "cases": [
            baseline,
            target_canonical,
            target_adapted,
            evidence_canonical,
            evidence_adapted,
        ],
        "checks": checks,
        "overall_passed": all(checks.values()) and all(
            case["passed"] for case in [baseline, target_canonical, target_adapted, evidence_canonical, evidence_adapted]
        ),
        "claim_boundary": (
            "Mechanism witnesses on one controlled-transition fixture: they "
            "establish that answer-derived fields reach the write point. Not "
            "task samples; no prevalence, repair-direction, or cross-grammar claim."
        ),
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
    }


def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_manifest(results_path: Path) -> dict:
    files = [
        "code/runners/oracle-coupling/executed_counterfactual_v1/README.md",
        "code/runners/oracle-coupling/executed_counterfactual_v1/run_counterfactual.py",
        "code/runners/oracle-coupling/executed_counterfactual_v1/verify_manifest.py",
        "code/runners/oracle-coupling/executed_counterfactual_v1/tests/test_executed_counterfactual.py",
        "code/runners/oracle-coupling/failure_to_executable_contract_v2/contract_gate.py",
        "code/runners/oracle-coupling/layout.py",
        "fixtures/oracle-coupling/failure_to_executable_contract_v2.json",
        "data/reproduction/oracle-coupling/failure_to_executable_contract_v2/candidate_corpus.json",
        "data/reproduction/oracle-coupling/executed_counterfactual_v1/artifacts/results.json",
    ]
    entries = [
        {
            "path": relative,
            "sha256": sha256_of(REPO_ROOT / relative),
            "bytes": (REPO_ROOT / relative).stat().st_size,
        }
        for relative in files
    ]
    return {
        "manifest_version": MANIFEST_VERSION,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "entry_count": len(entries),
        "entries_root_sha256": hashlib.sha256(
            json.dumps(entries, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest(),
        "entries": entries,
    }


def main() -> int:
    results = build_cases()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    results_path = OUTPUT_DIR / "results.json"
    results_path.write_text(
        json.dumps(results, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    manifest = build_manifest(results_path)
    manifest_path = OUTPUT_DIR.parent / "SHA256_MANIFEST.json"
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(
        json.dumps(
            {
                "overall_passed": results["overall_passed"],
                "checks": results["checks"],
                "results": results_path.relative_to(REPO_ROOT).as_posix(),
                "manifest": manifest_path.relative_to(REPO_ROOT).as_posix(),
            },
            indent=2,
        )
    )
    return 0 if results["overall_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
