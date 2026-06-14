#!/usr/bin/env python3
"""Evaluate Stage B v5 controlled state-transition fixtures."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


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


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def dump_json(path: Path, payload: Any) -> None:
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def extract_json(text: str) -> Any | None:
    stripped = text.strip()
    try:
        return json.loads(stripped)
    except json.JSONDecodeError:
        pass
    fenced = re.fullmatch(r"```(?:json)?\s*(.*?)\s*```", stripped, re.DOTALL)
    if not fenced:
        return None
    try:
        return json.loads(fenced.group(1))
    except json.JSONDecodeError:
        return None


def exact_keys(value: Any, expected: set[str]) -> bool:
    return isinstance(value, dict) and set(value) == expected


def zero_metrics() -> dict[str, float]:
    return {name: 0.0 for name in METRIC_NAMES}


def schema_valid(data: Any, spec: dict[str, Any]) -> bool:
    if not exact_keys(
        data,
        {
            "state_inventory",
            "grounded_claims",
            "transition_record",
            "transition_gate",
            "retention_attestation",
        },
    ):
        return False

    reference_field = spec["reference_field"]
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

    claims = data["grounded_claims"]
    if not isinstance(claims, list):
        return False
    for claim in claims:
        if not exact_keys(claim, {"slot_id", "claim", reference_field}):
            return False
        if not isinstance(claim["slot_id"], str):
            return False
        if not isinstance(claim["claim"], str) or not claim["claim"].strip():
            return False
        if not isinstance(claim[reference_field], list) or not all(
            isinstance(item, str) for item in claim[reference_field]
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
        isinstance(item, str) for item in transition[reference_field]
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
        isinstance(item, str) for item in gate["support_slot_ids"]
    ):
        return False

    attestation = data["retention_attestation"]
    if not exact_keys(attestation, {"status", "immutable_fields"}):
        return False
    return (
        isinstance(attestation["status"], str)
        and isinstance(attestation["immutable_fields"], list)
        and all(isinstance(item, str) for item in attestation["immutable_fields"])
    )


def evidence_exact(data: Any, spec: dict[str, Any]) -> bool:
    reference_field = spec["reference_field"]
    claims = data.get("grounded_claims") if isinstance(data, dict) else None
    if not isinstance(claims, list) or len(claims) != len(spec["expected_slots"]):
        return False
    for actual, expected in zip(claims, spec["expected_slots"], strict=True):
        if not isinstance(actual, dict):
            return False
        if actual.get("slot_id") != expected["slot_id"]:
            return False
        if actual.get(reference_field) != expected["references"]:
            return False
    return True


def residual_vocabulary_exact(data: Any, spec: dict[str, Any]) -> bool:
    inventory = data.get("state_inventory") if isinstance(data, dict) else None
    if not isinstance(inventory, dict):
        return False
    return (
        inventory.get("unknown_state") == spec["expected_unknown_state"]
        and inventory.get("forbidden_inferences")
        == spec["expected_forbidden_inferences"]
    )


def transition_exact(data: Any, spec: dict[str, Any]) -> bool:
    if not isinstance(data, dict):
        return False
    inventory = data.get("state_inventory")
    if not isinstance(inventory, dict):
        return False
    return (
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
    *,
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

    schema = schema_valid(data, spec)
    evidence = evidence_exact(data, spec)
    vocabulary = residual_vocabulary_exact(data, spec)
    transition = transition_exact(data, spec)
    gate = gate_exact(data, spec)
    attestation = attestation_exact(data, spec)
    success = schema and evidence and vocabulary and transition and gate and attestation

    metrics["schema_validity"] = float(schema)
    metrics["exact_evidence_array_preservation"] = float(evidence)
    metrics["residual_unknown_vocabulary_accuracy"] = float(vocabulary)
    metrics["state_transition_accuracy"] = float(transition)
    metrics["transition_gate_accuracy"] = float(gate)
    metrics["retention_attestation_accuracy"] = float(attestation)
    metrics["controlled_state_mutation_success"] = float(success)
    metrics["atom_primary_metric"] = metrics["controlled_state_mutation_success"]
    metrics["task_success"] = round(
        sum(
            metrics[name]
            for name in [
                "schema_validity",
                "exact_evidence_array_preservation",
                "residual_unknown_vocabulary_accuracy",
                "state_transition_accuracy",
                "transition_gate_accuracy",
                "retention_attestation_accuracy",
            ]
        )
        / 6,
        3,
    )
    findings = [
        name
        for name, passed in [
            ("schema_contract_failed", schema),
            ("exact_evidence_array_preservation_failed", evidence),
            ("residual_unknown_vocabulary_failed", vocabulary),
            ("state_transition_failed", transition),
            ("transition_gate_failed", gate),
            ("retention_attestation_failed", attestation),
        ]
        if not passed
    ]
    report = {
        "status": "complete",
        "passed": success,
        "expect_pass": expect_pass,
        "expectation_met": expect_pass is None or expect_pass == success,
        "reason": "Output evaluated against the controlled transition contract.",
        "findings": findings,
        "primary_metric": "controlled_state_mutation_success",
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
    return violations


def metrics_match(
    metrics: dict[str, float], expected: dict[str, float]
) -> tuple[bool, list[str]]:
    mismatches = []
    for name, value in expected.items():
        actual = metrics.get(name)
        if actual != value:
            mismatches.append(f"{name}: expected {value:.3f}, got {actual:.3f}")
    return not mismatches, mismatches


def evaluate_local(
    *,
    fixtures_dir: Path,
    output_json: Path,
    output_md: Path,
) -> None:
    fixture_dirs = sorted(path for path in fixtures_dir.iterdir() if path.is_dir())
    cases = []
    failures = 0
    surface_violations = []
    for fixture_dir in fixture_dirs:
        surface_violations.extend(check_surface(fixture_dir))
        golden_report, golden_metrics = evaluate_payload(
            fixture_dir=fixture_dir,
            output_text=(fixture_dir / "golden_output.json").read_text(
                encoding="utf-8"
            ),
            run_id=f"{fixture_dir.name}__golden",
            model="golden",
            arm="local",
            expect_pass=True,
        )
        cases.append(
            {
                "fixture": fixture_dir.name,
                "case": "golden",
                "report": golden_report,
                "metrics": golden_metrics,
                "metric_expectation_met": True,
                "metric_mismatches": [],
            }
        )
        if not golden_report["expectation_met"]:
            failures += 1

        spec = load_json(fixture_dir / "evaluation_spec.json")
        for bad_path in sorted((fixture_dir / "known_bad_outputs").glob("*.json")):
            report, metrics = evaluate_payload(
                fixture_dir=fixture_dir,
                output_text=bad_path.read_text(encoding="utf-8"),
                run_id=f"{fixture_dir.name}__{bad_path.stem}",
                model="known_bad",
                arm="local",
                expect_pass=False,
            )
            metric_met, mismatches = metrics_match(
                metrics,
                spec["known_bad_expectations"][bad_path.stem],
            )
            cases.append(
                {
                    "fixture": fixture_dir.name,
                    "case": bad_path.stem,
                    "report": report,
                    "metrics": metrics,
                    "metric_expectation_met": metric_met,
                    "metric_mismatches": mismatches,
                }
            )
            if not report["expectation_met"] or not metric_met:
                failures += 1

    payload = {
        "suite": "stage_b_v5_controlled_state_transition_local",
        "fixture_count": len(fixture_dirs),
        "case_count": len(cases),
        "expectation_failure_count": failures,
        "model_surface_violation_count": len(surface_violations),
        "model_surface_violations": surface_violations,
        "cases": cases,
    }
    dump_json(output_json, payload)
    output_md.write_text(local_markdown(payload), encoding="utf-8")
    if failures or surface_violations:
        raise SystemExit(1)


def local_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Stage B v5 Controlled State-Transition Local Evaluation",
        "",
        f"- Fixtures: {payload['fixture_count']}",
        f"- Cases: {payload['case_count']}",
        f"- Expectation failures: {payload['expectation_failure_count']}",
        f"- Model-surface isolation violations: {payload['model_surface_violation_count']}",
        "",
        "| Fixture | Case | Schema | Evidence | Residual state | Transition | Gate | Attestation | Aggregate | Expected metrics |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|",
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
            f"{metrics['controlled_state_mutation_success']:.3f} | "
            f"{str(case['metric_expectation_met']).lower()} |"
        )
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixtures-dir", required=True)
    parser.add_argument("--local-check", action="store_true")
    parser.add_argument("--output-runs", required=True)
    parser.add_argument("--output-md", required=True)
    args = parser.parse_args()

    if not args.local_check:
        raise SystemExit("Stage B v5 currently supports --local-check only")
    evaluate_local(
        fixtures_dir=Path(args.fixtures_dir),
        output_json=Path(args.output_runs),
        output_md=Path(args.output_md),
    )


if __name__ == "__main__":
    main()
