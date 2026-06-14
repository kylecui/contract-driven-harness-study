#!/usr/bin/env python3
"""Evaluate Stage B v5.2 evidence-binding ablation fixtures."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from evaluate_stage_b_v5_state_transition import (
    dump_json,
    exact_keys,
    extract_json,
    load_json,
    metrics_match,
)


METRIC_NAMES = [
    "task_success",
    "schema_validity",
    "exact_evidence_array_preservation",
    "residual_unknown_vocabulary_accuracy",
    "state_transition_accuracy",
    "transition_gate_accuracy",
    "retention_attestation_accuracy",
    "controlled_state_mutation_success",
    "atom_primary_metric",
]


def zero_metrics() -> dict[str, float]:
    return {name: 0.0 for name in METRIC_NAMES}


def schema_valid(data: Any, spec: dict[str, Any]) -> bool:
    section = spec["evidence_section"]
    reference_field = spec["reference_field"]
    if not exact_keys(
        data,
        {
            "state_inventory",
            section,
            "transition_record",
            "transition_gate",
            "retention_attestation",
        },
    ):
        return False

    inventory = data["state_inventory"]
    if not exact_keys(
        inventory, {"known_state", "unknown_state", "forbidden_inferences"}
    ):
        return False
    if not isinstance(inventory["known_state"], list):
        return False
    for state in inventory["known_state"]:
        if not exact_keys(state, {"state_id", "value", reference_field}):
            return False
        if not isinstance(state["state_id"], str) or not isinstance(
            state["value"], str
        ):
            return False
        if not isinstance(state[reference_field], list) or not all(
            isinstance(item, str) for item in state[reference_field]
        ):
            return False
    if not all(
        isinstance(inventory[key], list)
        and all(isinstance(item, str) for item in inventory[key])
        for key in ["unknown_state", "forbidden_inferences"]
    ):
        return False

    payload = data[section]
    if not isinstance(payload, list):
        return False
    expected_keys = {"slot_id", reference_field}
    if section == "grounded_claims":
        expected_keys.add("claim")
    for item in payload:
        if not exact_keys(item, expected_keys):
            return False
        if not isinstance(item["slot_id"], str):
            return False
        if section == "grounded_claims" and (
            not isinstance(item["claim"], str) or not item["claim"].strip()
        ):
            return False
        if not isinstance(item[reference_field], list) or not all(
            isinstance(value, str) for value in item[reference_field]
        ):
            return False

    transition = data["transition_record"]
    if not exact_keys(
        transition,
        {
            "event_id",
            "state_id",
            "from_status",
            "to_status",
            reference_field,
            "applied",
        },
    ):
        return False
    if not all(
        isinstance(transition[key], str)
        for key in ["event_id", "state_id", "from_status", "to_status"]
    ):
        return False
    if not isinstance(transition[reference_field], list) or not all(
        isinstance(value, str) for value in transition[reference_field]
    ):
        return False
    if not isinstance(transition["applied"], bool):
        return False

    gate = data["transition_gate"]
    if not exact_keys(
        gate,
        {
            "status",
            "permitted_action",
            "satisfied_prerequisite",
            "next_action",
            "support_slot_ids",
        },
    ):
        return False
    if not all(
        isinstance(gate[key], str)
        for key in [
            "status",
            "permitted_action",
            "satisfied_prerequisite",
            "next_action",
        ]
    ):
        return False
    if not isinstance(gate["support_slot_ids"], list) or not all(
        isinstance(value, str) for value in gate["support_slot_ids"]
    ):
        return False

    attestation = data["retention_attestation"]
    return (
        exact_keys(attestation, {"status", "immutable_fields"})
        and isinstance(attestation["status"], str)
        and isinstance(attestation["immutable_fields"], list)
        and all(isinstance(value, str) for value in attestation["immutable_fields"])
    )


def evidence_exact(data: Any, spec: dict[str, Any]) -> bool:
    section = spec["evidence_section"]
    reference_field = spec["reference_field"]
    payload = data.get(section) if isinstance(data, dict) else None
    expected = spec["expected_payload"]
    if not isinstance(payload, list) or len(payload) != len(expected):
        return False
    for actual, required in zip(payload, expected, strict=True):
        if not isinstance(actual, dict):
            return False
        if actual.get("slot_id") != required["slot_id"]:
            return False
        if actual.get(reference_field) != required["references"]:
            return False
    return True


def residual_exact(data: Any, spec: dict[str, Any]) -> bool:
    inventory = data.get("state_inventory") if isinstance(data, dict) else None
    return isinstance(inventory, dict) and (
        inventory.get("unknown_state") == spec["expected_unknown_state"]
        and inventory.get("forbidden_inferences")
        == spec["expected_forbidden_inferences"]
    )


def transition_exact(data: Any, spec: dict[str, Any]) -> bool:
    inventory = data.get("state_inventory") if isinstance(data, dict) else None
    return isinstance(inventory, dict) and (
        inventory.get("known_state") == spec["expected_known_state"]
        and data.get("transition_record") == spec["expected_transition_record"]
    )


def gate_exact(data: Any, spec: dict[str, Any]) -> bool:
    return isinstance(data, dict) and data.get("transition_gate") == spec[
        "expected_gate"
    ]


def attestation_exact(data: Any, spec: dict[str, Any]) -> bool:
    return isinstance(data, dict) and data.get("retention_attestation") == spec[
        "expected_attestation"
    ]


def evaluate_payload(
    fixture_dir: Path,
    output_text: str,
    run_id: str,
    model: str,
    arm: str,
    expect_pass: bool | None = None,
) -> tuple[dict[str, Any], dict[str, float]]:
    spec = load_json(fixture_dir / "evaluation_spec.json")
    data = extract_json(output_text)
    metrics = zero_metrics()
    if data is None:
        report = {
            "status": "complete",
            "passed": False,
            "expect_pass": expect_pass,
            "expectation_met": expect_pass is None or expect_pass is False,
            "reason": "Output is not valid JSON.",
            "findings": ["json_parse_failed"],
            "run_id": run_id,
            "model": model,
            "harness_arm": arm,
        }
        return report, metrics

    checks = {
        "schema_validity": schema_valid(data, spec),
        "exact_evidence_array_preservation": evidence_exact(data, spec),
        "residual_unknown_vocabulary_accuracy": residual_exact(data, spec),
        "state_transition_accuracy": transition_exact(data, spec),
        "transition_gate_accuracy": gate_exact(data, spec),
        "retention_attestation_accuracy": attestation_exact(data, spec),
    }
    success = all(checks.values())
    for name, passed in checks.items():
        metrics[name] = float(passed)
    metrics["controlled_state_mutation_success"] = float(success)
    metrics["atom_primary_metric"] = float(success)
    metrics["task_success"] = round(
        sum(float(value) for value in checks.values()) / len(checks), 3
    )
    report = {
        "status": "complete",
        "passed": success,
        "expect_pass": expect_pass,
        "expectation_met": expect_pass is None or expect_pass == success,
        "reason": "Output evaluated against the v5.2 ablation contract.",
        "findings": [
            f"{name}_failed" for name, passed in checks.items() if not passed
        ],
        "primary_metric": "controlled_state_mutation_success",
        "representation_arm": spec["representation_arm"],
        "perturbation_condition": spec["perturbation_condition"],
        "parsed_output": data,
        "run_id": run_id,
        "model": model,
        "harness_arm": arm,
    }
    return report, metrics


def check_surface(fixture_dir: Path) -> list[dict[str, str]]:
    spec = load_json(fixture_dir / "evaluation_spec.json")
    violations = []
    for filename in spec["model_surface_files"]:
        text = (fixture_dir / filename).read_text(encoding="utf-8")
        for forbidden in spec["forbidden_model_surface_values"]:
            if forbidden in text:
                violations.append(
                    {
                        "fixture": fixture_dir.name,
                        "file": filename,
                        "forbidden_value": forbidden,
                    }
                )
    contract_text = (fixture_dir / "output_contract.json").read_text(
        encoding="utf-8"
    )
    if spec["evidence_section"] == "grounded_claims":
        if "evidence_bindings" in contract_text:
            violations.append(
                {
                    "fixture": fixture_dir.name,
                    "file": "output_contract.json",
                    "forbidden_value": "evidence_bindings",
                }
            )
    elif "grounded_claims" in contract_text:
        violations.append(
            {
                "fixture": fixture_dir.name,
                "file": "output_contract.json",
                "forbidden_value": "grounded_claims",
            }
        )
    return violations


def check_paired_gate(fixtures: list[Path]) -> list[dict[str, str]]:
    by_condition: dict[str, list[dict[str, Any]]] = {}
    for fixture in fixtures:
        spec = load_json(fixture / "evaluation_spec.json")
        by_condition.setdefault(spec["perturbation_condition"], []).append(spec)
    violations = []
    for condition, specs in by_condition.items():
        if len(specs) != 2:
            violations.append(
                {"condition": condition, "reason": "paired_fixture_missing"}
            )
            continue
        if specs[0]["expected_gate"] != specs[1]["expected_gate"]:
            violations.append(
                {"condition": condition, "reason": "paired_gate_mismatch"}
            )
    return violations


def evaluate_local(
    fixtures_dir: Path,
    output_json: Path,
    output_md: Path,
) -> None:
    fixtures = sorted(path for path in fixtures_dir.iterdir() if path.is_dir())
    cases = []
    failures = 0
    surface_violations = []
    for fixture in fixtures:
        surface_violations.extend(check_surface(fixture))
        report, metrics = evaluate_payload(
            fixture,
            (fixture / "golden_output.json").read_text(encoding="utf-8"),
            f"{fixture.name}__golden",
            "golden",
            "local",
            True,
        )
        cases.append(
            {
                "fixture": fixture.name,
                "case": "golden",
                "report": report,
                "metrics": metrics,
                "metric_expectation_met": True,
                "metric_mismatches": [],
            }
        )
        if not report["expectation_met"]:
            failures += 1

        spec = load_json(fixture / "evaluation_spec.json")
        for bad_path in sorted((fixture / "known_bad_outputs").glob("*.json")):
            report, metrics = evaluate_payload(
                fixture,
                bad_path.read_text(encoding="utf-8"),
                f"{fixture.name}__{bad_path.stem}",
                "known_bad",
                "local",
                False,
            )
            metric_met, mismatches = metrics_match(
                metrics,
                spec["known_bad_expectations"][bad_path.stem],
            )
            cases.append(
                {
                    "fixture": fixture.name,
                    "case": bad_path.stem,
                    "report": report,
                    "metrics": metrics,
                    "metric_expectation_met": metric_met,
                    "metric_mismatches": mismatches,
                }
            )
            if not report["expectation_met"] or not metric_met:
                failures += 1

    gate_violations = check_paired_gate(fixtures)
    payload = {
        "suite": "stage_b_v52_evidence_binding_ablation_local",
        "fixture_count": len(fixtures),
        "case_count": len(cases),
        "expectation_failure_count": failures,
        "model_surface_violation_count": len(surface_violations),
        "model_surface_violations": surface_violations,
        "paired_gate_violation_count": len(gate_violations),
        "paired_gate_violations": gate_violations,
        "cases": cases,
    }
    dump_json(output_json, payload)
    output_md.write_text(local_markdown(payload), encoding="utf-8")
    if failures or surface_violations or gate_violations:
        raise SystemExit(1)


def evaluate_manifest(
    manifest_path: Path,
    fixtures_dir: Path,
    output_json: Path,
    output_md: Path,
) -> None:
    manifest = load_json(manifest_path)
    results = []
    for run in manifest["runs"]:
        fixture = fixtures_dir / run["fixture"]
        report, metrics = evaluate_payload(
            fixture,
            Path(run["paths"]["output"]).read_text(encoding="utf-8"),
            run["run_id"],
            run["model"],
            run["harness_arm"],
        )
        spec = load_json(fixture / "evaluation_spec.json")
        report["fixture"] = run["fixture"]
        metric_payload = {
            "run_id": run["run_id"],
            "fixture": run["fixture"],
            "task_class": run["task_type"],
            "model": run["model"],
            "harness_arm": run["harness_arm"],
            "representation_arm": spec["representation_arm"],
            "perturbation_condition": spec["perturbation_condition"],
            "validation_status": report["status"],
            "passed": report["passed"],
            "metrics": metrics,
            "mock": False,
        }
        dump_json(Path(run["paths"]["validation_report"]), report)
        dump_json(Path(run["paths"]["metrics"]), metric_payload)
        results.append(metric_payload)
    dump_json(output_json, {"runs": results})
    output_md.write_text(manifest_markdown(results), encoding="utf-8")


def local_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Stage B v5.2 Evidence-Binding Ablation Local Evaluation",
        "",
        f"- Fixtures: {payload['fixture_count']}",
        f"- Cases: {payload['case_count']}",
        f"- Expectation failures: {payload['expectation_failure_count']}",
        f"- Surface violations: {payload['model_surface_violation_count']}",
        f"- Paired-gate violations: {payload['paired_gate_violation_count']}",
        "",
        "| Fixture | Case | Schema | Evidence | State | Transition | Gate | Attestation | Aggregate |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for case in payload["cases"]:
        metrics = case["metrics"]
        lines.append(
            f"| `{case['fixture']}` | `{case['case']}` | "
            f"{metrics['schema_validity']:.3f} | "
            f"{metrics['exact_evidence_array_preservation']:.3f} | "
            f"{metrics['residual_unknown_vocabulary_accuracy']:.3f} | "
            f"{metrics['state_transition_accuracy']:.3f} | "
            f"{metrics['transition_gate_accuracy']:.3f} | "
            f"{metrics['retention_attestation_accuracy']:.3f} | "
            f"{metrics['controlled_state_mutation_success']:.3f} |"
        )
    return "\n".join(lines) + "\n"


def manifest_markdown(results: list[dict[str, Any]]) -> str:
    lines = [
        "# Stage B v5.2 Evidence-Binding Ablation Model Evaluation",
        "",
        "| Run | Representation | Condition | Evidence | Gate | Aggregate | Passed |",
        "|---|---|---|---:|---:|---:|---:|",
    ]
    for result in results:
        metrics = result["metrics"]
        lines.append(
            f"| `{result['run_id']}` | `{result['representation_arm']}` | "
            f"`{result['perturbation_condition']}` | "
            f"{metrics['exact_evidence_array_preservation']:.3f} | "
            f"{metrics['transition_gate_accuracy']:.3f} | "
            f"{metrics['controlled_state_mutation_success']:.3f} | "
            f"{str(result['passed']).lower()} |"
        )
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixtures-dir", required=True)
    parser.add_argument("--manifest")
    parser.add_argument("--local-check", action="store_true")
    parser.add_argument("--output-runs", required=True)
    parser.add_argument("--output-md", required=True)
    args = parser.parse_args()

    if args.local_check:
        evaluate_local(
            Path(args.fixtures_dir),
            Path(args.output_runs),
            Path(args.output_md),
        )
    elif args.manifest:
        evaluate_manifest(
            Path(args.manifest),
            Path(args.fixtures_dir),
            Path(args.output_runs),
            Path(args.output_md),
        )
    else:
        raise SystemExit("Use --local-check or --manifest")


if __name__ == "__main__":
    main()
