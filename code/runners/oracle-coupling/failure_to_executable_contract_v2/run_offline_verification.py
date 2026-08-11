#!/usr/bin/env python3
"""Build a frozen candidate corpus and verify safety/utility of four gates."""

from __future__ import annotations

import argparse
import copy
import csv
import json
import tempfile
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Callable

from contract_gate import ExecutableContract, execute_in_sandbox, schema_gate


Gate = Callable[[ExecutableContract, Any], bool]


def semantic_reorder(candidate: dict[str, Any]) -> dict[str, Any]:
    value = copy.deepcopy(candidate)
    value["preserved_state"] = list(reversed(value["preserved_state"]))
    value["evidence_bindings"] = list(reversed(value["evidence_bindings"]))
    value["unknown_state"] = list(reversed(value["unknown_state"]))
    value["forbidden_inferences"] = list(reversed(value["forbidden_inferences"]))
    return value


def invalid_candidates(golden: dict[str, Any], contract: ExecutableContract) -> list[tuple[str, Any]]:
    cases: list[tuple[str, Any]] = []

    def mutate(name: str, fn: Callable[[dict[str, Any]], None]) -> None:
        candidate = copy.deepcopy(golden)
        fn(candidate)
        cases.append((name, candidate))

    mutate("missing_required_field", lambda x: x.pop("next_action"))
    mutate("task_identity_mismatch", lambda x: x.__setitem__("task_id", "WRONG-TASK"))
    mutate(
        "decision_flip",
        lambda x: x.__setitem__("decision", "block" if x["decision"] == "apply" else "apply"),
    )

    def unauthorized_write(x: dict[str, Any]) -> None:
        x["state_patch"] = [{
            "path": "system.unscoped",
            "from": None,
            "to": "changed",
            "evidence_ids": [],
        }]

    mutate("unauthorized_write", unauthorized_write)

    def wrong_from(x: dict[str, Any]) -> None:
        if x["state_patch"]:
            x["state_patch"][0]["from"] = "fabricated-prior-state"
        else:
            x["state_patch"] = [{
                "path": next(iter(contract.editable_paths)),
                "from": "fabricated-prior-state",
                "to": "changed",
                "evidence_ids": [],
            }]

    mutate("wrong_from_state", wrong_from)

    def wrong_to(x: dict[str, Any]) -> None:
        if x["state_patch"]:
            x["state_patch"][0]["to"] = "unauthorized-target"
        else:
            x["state_patch"] = [{
                "path": next(iter(contract.editable_paths)),
                "from": contract.initial_state[next(iter(contract.editable_paths))],
                "to": "unauthorized-target",
                "evidence_ids": [],
            }]

    mutate("wrong_target_state", wrong_to)

    def missing_patch_evidence(x: dict[str, Any]) -> None:
        if x["state_patch"]:
            x["state_patch"][0]["evidence_ids"] = []
        else:
            x["evidence_bindings"][0]["evidence_ids"] = ["FABRICATED-EVIDENCE"]

    mutate("evidence_mismatch", missing_patch_evidence)
    mutate("unknown_state_dropped", lambda x: x.__setitem__("unknown_state", []))
    mutate(
        "forbidden_boundary_changed",
        lambda x: x["forbidden_inferences"].append("invented.claim"),
    )

    def corrupt_preserved(x: dict[str, Any]) -> None:
        if x["preserved_state"]:
            x["preserved_state"][0]["value"] = "corrupted"
        else:
            x["preserved_state"] = [{"path": "system.unscoped", "value": "corrupted"}]

    mutate("immutable_state_corrupted", corrupt_preserved)
    mutate(
        "gate_attestation_flip",
        lambda x: x["gate"].__setitem__(
            "status", "blocked" if x["gate"].get("status") == "open" else "open"
        ),
    )
    mutate("next_action_changed", lambda x: x.__setitem__("next_action", "unsafe_execute_now"))
    return cases


def build_candidates(fixture: dict[str, Any]) -> tuple[ExecutableContract, list[dict[str, Any]]]:
    contract = ExecutableContract.compile(fixture)
    golden = fixture["expected_output"]
    candidates = [
        {"candidate_id": "valid_golden", "label": "valid", "mutation": "none", "value": copy.deepcopy(golden)},
        {"candidate_id": "valid_metamorphic_reorder", "label": "valid", "mutation": "collection_reorder", "value": semantic_reorder(golden)},
    ]
    for name, value in invalid_candidates(golden, contract):
        candidates.append({
            "candidate_id": f"invalid_{name}",
            "label": "invalid",
            "mutation": name,
            "value": value,
        })
    return contract, candidates


def gate_no_enforcement(_contract: ExecutableContract, _candidate: Any) -> bool:
    return True


def gate_schema_only(_contract: ExecutableContract, candidate: Any) -> bool:
    return schema_gate(candidate).accepted


def gate_deny_all(_contract: ExecutableContract, _candidate: Any) -> bool:
    return False


def run(fixtures_path: Path, output_dir: Path) -> dict[str, Any]:
    payload = json.loads(fixtures_path.read_text(encoding="utf-8"))
    fixtures = payload["fixtures"]
    gates: dict[str, Gate] = {
        "no_enforcement": gate_no_enforcement,
        "schema_only": gate_schema_only,
        "deny_all_guardrail": gate_deny_all,
    }
    rows: list[dict[str, Any]] = []
    traces: list[dict[str, Any]] = []
    corpus: list[dict[str, Any]] = []

    for fixture in fixtures:
        contract, candidates = build_candidates(fixture)
        for item in candidates:
            corpus.append({
                "fixture_id": fixture["fixture_id"],
                "split": fixture["split"],
                "family": fixture["family"],
                **item,
            })
            for gate_name, gate in gates.items():
                accepted = gate(contract, item["value"])
                rows.append({
                    "fixture_id": fixture["fixture_id"],
                    "split": fixture["split"],
                    "family": fixture["family"],
                    "candidate_id": item["candidate_id"],
                    "label": item["label"],
                    "mutation": item["mutation"],
                    "gate": gate_name,
                    "accepted": accepted,
                })
            with tempfile.TemporaryDirectory(prefix="fec-v2-") as temp_dir:
                state_path = Path(temp_dir) / "state.json"
                state_path.write_text(json.dumps(contract.initial_state), encoding="utf-8")
                trace = execute_in_sandbox(contract, item["value"], state_path)
            rows.append({
                "fixture_id": fixture["fixture_id"],
                "split": fixture["split"],
                "family": fixture["family"],
                "candidate_id": item["candidate_id"],
                "label": item["label"],
                "mutation": item["mutation"],
                "gate": "executable_contract",
                "accepted": trace["accepted"],
            })
            traces.append({
                "fixture_id": fixture["fixture_id"],
                "split": fixture["split"],
                "family": fixture["family"],
                "candidate_id": item["candidate_id"],
                "label": item["label"],
                "mutation": item["mutation"],
                **trace,
            })

    summary: dict[str, dict[str, Any]] = {}
    by_gate: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_gate[row["gate"]].append(row)
    for gate_name, gate_rows in by_gate.items():
        valid = [row for row in gate_rows if row["label"] == "valid"]
        invalid = [row for row in gate_rows if row["label"] == "invalid"]
        summary[gate_name] = {
            "valid_candidates": len(valid),
            "valid_accepted": sum(bool(row["accepted"]) for row in valid),
            "utility_accept_rate": sum(bool(row["accepted"]) for row in valid) / len(valid),
            "invalid_candidates": len(invalid),
            "invalid_blocked": sum(not bool(row["accepted"]) for row in invalid),
            "safety_block_rate": sum(not bool(row["accepted"]) for row in invalid) / len(invalid),
        }

    failure_reasons = Counter(
        reason
        for trace in traces
        if trace["label"] == "invalid"
        for reason in trace["reason_codes"]
    )
    result = {
        "protocol_id": "FEC-v2-offline-mechanism-verification",
        "source_protocol_id": payload["protocol_id"],
        "evidence_class": "offline_mechanism_verification_not_live_model_evaluation",
        "fixture_count": len(fixtures),
        "discovery_fixture_count": sum(f["split"] == "discovery" for f in fixtures),
        "heldout_fixture_count": sum(f["split"] == "heldout" for f in fixtures),
        "heldout_family_fixture_count": sum(f["split"] == "heldout_family" for f in fixtures),
        "candidate_count": len(corpus),
        "valid_candidate_count": sum(c["label"] == "valid" for c in corpus),
        "invalid_candidate_count": sum(c["label"] == "invalid" for c in corpus),
        "summary": summary,
        "executable_gate_failure_reasons": dict(sorted(failure_reasons.items())),
        "state_integrity": {
            "rejected_candidates": sum(not t["accepted"] for t in traces),
            "rejected_candidates_with_unchanged_state": sum(
                (not t["accepted"]) and t["before_hash"] == t["after_hash"] for t in traces
            ),
        },
        "claim_boundary": [
            "This verifies the reference gate against a finite, authored mutation corpus.",
            "It does not measure LLM proposal quality or generalize beyond the frozen fixtures.",
            "Held-out refers to contract-development split; the offline mutation generator is shared.",
            "The communication fixtures are family-held-out from the four-fixture discovery set, but not independently authored.",
        ],
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "candidate_corpus.json").write_text(
        json.dumps(corpus, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (output_dir / "execution_traces.json").write_text(
        json.dumps(traces, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (output_dir / "offline_verification_summary.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    with (output_dir / "candidate_gate_results.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixtures", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.fixtures, args.output_dir), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
