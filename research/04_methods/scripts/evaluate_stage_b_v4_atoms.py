#!/usr/bin/env python3
"""Evaluate the exact-retention mechanism atoms used by Stage B v4."""

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
    "exact_closed_vocabulary_retention",
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


def zero_metrics() -> dict[str, float]:
    return {metric: 0.0 for metric in METRIC_NAMES}


def exact_keys(value: Any, expected: set[str]) -> bool:
    return isinstance(value, dict) and set(value) == expected


def evidence_schema_valid(data: Any, reference_field: str) -> bool:
    if not exact_keys(data, {"grounded_claims", "immutability_check"}):
        return False
    claims = data["grounded_claims"]
    check = data["immutability_check"]
    if not isinstance(claims, list) or not exact_keys(
        check,
        {"status", "immutable_fields"},
    ):
        return False
    if check["status"] != "preserved" or check["immutable_fields"] != [
        "slot_id",
        reference_field,
    ]:
        return False
    for claim in claims:
        if not exact_keys(claim, {"slot_id", "claim", reference_field}):
            return False
        if not isinstance(claim["slot_id"], str):
            return False
        if not isinstance(claim["claim"], str) or not claim["claim"].strip():
            return False
        references = claim[reference_field]
        if not isinstance(references, list) or not all(
            isinstance(item, str) for item in references
        ):
            return False
    return True


def evidence_arrays_exact(
    data: Any,
    *,
    reference_field: str,
    expected_slots: list[dict[str, Any]],
) -> bool:
    if not evidence_schema_valid(data, reference_field):
        return False
    claims = data["grounded_claims"]
    if len(claims) != len(expected_slots):
        return False
    for actual, expected in zip(claims, expected_slots, strict=True):
        if actual["slot_id"] != expected["slot_id"]:
            return False
        if actual[reference_field] != expected["references"]:
            return False
    return True


def closed_vocab_schema_valid(data: Any) -> bool:
    if not exact_keys(data, {"state_inventory", "retention_status"}):
        return False
    inventory = data["state_inventory"]
    if not exact_keys(inventory, {"unknown_state", "forbidden_inferences"}):
        return False
    if data["retention_status"] != "preserved":
        return False
    for key in ["unknown_state", "forbidden_inferences"]:
        values = inventory[key]
        if not isinstance(values, list) or not all(
            isinstance(item, str) for item in values
        ):
            return False
    return True


def closed_vocab_exact(
    data: Any,
    *,
    expected_unknown_state: list[str],
    expected_forbidden_inferences: list[str],
) -> bool:
    if not closed_vocab_schema_valid(data):
        return False
    inventory = data["state_inventory"]
    return (
        inventory["unknown_state"] == expected_unknown_state
        and inventory["forbidden_inferences"] == expected_forbidden_inferences
    )


def evaluate_payload(
    *,
    fixture_dir: Path,
    output_text: str,
    run_id: str,
    model: str,
    arm: str,
    expect_pass: bool | None = None,
) -> tuple[dict[str, Any], dict[str, float]]:
    atom = load_json(fixture_dir / "mechanism_atom.json")
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

    atom_kind = spec["atom_kind"]
    if atom_kind == "exact_evidence_array_immutability":
        reference_field = spec["reference_field"]
        schema_valid = evidence_schema_valid(data, reference_field)
        exact = evidence_arrays_exact(
            data,
            reference_field=reference_field,
            expected_slots=spec["expected_slots"],
        )
        primary_metric = "exact_evidence_array_preservation"
    elif atom_kind == "exact_closed_vocabulary_retention":
        schema_valid = closed_vocab_schema_valid(data)
        exact = closed_vocab_exact(
            data,
            expected_unknown_state=spec["expected_unknown_state"],
            expected_forbidden_inferences=spec[
                "expected_forbidden_inferences"
            ],
        )
        primary_metric = "exact_closed_vocabulary_retention"
    else:
        raise ValueError(f"Unsupported atom_kind: {atom_kind}")

    metrics["schema_validity"] = 1.0 if schema_valid else 0.0
    metrics[primary_metric] = 1.0 if exact else 0.0
    metrics["atom_primary_metric"] = metrics[primary_metric]
    metrics["task_success"] = (
        metrics["schema_validity"] + metrics["atom_primary_metric"]
    ) / 2

    passed = metrics["schema_validity"] == 1.0 and metrics[primary_metric] == 1.0
    findings = []
    if not schema_valid:
        findings.append("schema_contract_failed")
    if not exact:
        findings.append(f"{primary_metric}_failed")
    report = {
        "status": "complete",
        "passed": passed,
        "expect_pass": expect_pass,
        "expectation_met": expect_pass is None or expect_pass == passed,
        "reason": "Output evaluated by exact Stage B v4 atom contract.",
        "findings": findings,
        "atom_id": atom["atom_id"],
        "atom_name": atom["atom_name"],
        "primary_metric": primary_metric,
        "parsed_output": data,
        "run_id": run_id,
        "model": model,
        "harness_arm": arm,
    }
    return report, metrics


def check_model_surface(fixture_dir: Path) -> list[dict[str, str]]:
    spec = load_json(fixture_dir / "evaluation_spec.json")
    violations: list[dict[str, str]] = []
    for filename in spec.get("model_surface_files", []):
        path = fixture_dir / filename
        text = path.read_text(encoding="utf-8")
        for forbidden in spec.get("forbidden_model_surface_values", []):
            if forbidden in text:
                violations.append(
                    {
                        "fixture": fixture_dir.name,
                        "file": filename,
                        "forbidden_value": forbidden,
                    }
                )
    return violations


def evaluate_local(
    *,
    atoms_dir: Path,
    fixtures: list[str] | None,
    output_json: Path,
    output_md: Path,
) -> None:
    fixture_dirs = sorted(path for path in atoms_dir.iterdir() if path.is_dir())
    if fixtures:
        selected = set(fixtures)
        fixture_dirs = [path for path in fixture_dirs if path.name in selected]

    cases: list[dict[str, Any]] = []
    expectation_failures = 0
    surface_violations: list[dict[str, str]] = []
    for fixture_dir in fixture_dirs:
        surface_violations.extend(check_model_surface(fixture_dir))
        golden_text = (fixture_dir / "golden_output.json").read_text(
            encoding="utf-8"
        )
        report, metrics = evaluate_payload(
            fixture_dir=fixture_dir,
            output_text=golden_text,
            run_id=f"{fixture_dir.name}__golden",
            model="golden",
            arm="local",
            expect_pass=True,
        )
        cases.append(
            {
                "fixture": fixture_dir.name,
                "case": "golden",
                "report": report,
                "metrics": metrics,
            }
        )
        if not report["expectation_met"]:
            expectation_failures += 1

        spec = load_json(fixture_dir / "evaluation_spec.json")
        expected_primary = float(
            spec.get("known_bad_primary_metric_must_equal", 0.0)
        )
        for bad_path in sorted((fixture_dir / "known_bad_outputs").glob("*.json")):
            report, metrics = evaluate_payload(
                fixture_dir=fixture_dir,
                output_text=bad_path.read_text(encoding="utf-8"),
                run_id=f"{fixture_dir.name}__{bad_path.stem}",
                model="known_bad",
                arm="local",
                expect_pass=False,
            )
            primary_expectation_met = (
                metrics["atom_primary_metric"] == expected_primary
            )
            report["primary_expectation_met"] = primary_expectation_met
            cases.append(
                {
                    "fixture": fixture_dir.name,
                    "case": bad_path.stem,
                    "report": report,
                    "metrics": metrics,
                }
            )
            if not report["expectation_met"] or not primary_expectation_met:
                expectation_failures += 1

    payload = {
        "suite": "stage_b_v4_local_mechanism_atoms",
        "case_count": len(cases),
        "fixture_count": len(fixture_dirs),
        "expectation_failure_count": expectation_failures,
        "model_surface_violation_count": len(surface_violations),
        "model_surface_violations": surface_violations,
        "cases": cases,
    }
    dump_json(output_json, payload)
    output_md.write_text(local_markdown(payload), encoding="utf-8")
    if expectation_failures or surface_violations:
        raise SystemExit(1)


def evaluate_manifest(
    *,
    manifest_path: Path,
    atoms_dir: Path,
    output_json: Path,
    output_md: Path,
) -> None:
    manifest = load_json(manifest_path)
    results = []
    for run in manifest["runs"]:
        fixture_dir = atoms_dir / run["fixture"]
        output_path = Path(run["paths"]["output"])
        report, metrics = evaluate_payload(
            fixture_dir=fixture_dir,
            output_text=output_path.read_text(encoding="utf-8"),
            run_id=run["run_id"],
            model=run["model"],
            arm=run["harness_arm"],
        )
        validation_path = Path(run["paths"]["validation_report"])
        metrics_path = Path(run["paths"]["metrics"])
        report["fixture"] = run["fixture"]
        metric_payload = {
            "run_id": run["run_id"],
            "fixture": run["fixture"],
            "task_class": run["task_type"],
            "model": run["model"],
            "harness_arm": run["harness_arm"],
            "validation_status": report["status"],
            "passed": report["passed"],
            "metrics": metrics,
            "mock": False,
        }
        dump_json(validation_path, report)
        dump_json(metrics_path, metric_payload)
        results.append(metric_payload)
    payload = {"runs": results}
    dump_json(output_json, payload)
    output_md.write_text(manifest_markdown(results), encoding="utf-8")


def local_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Stage B v4 Local Atom Evaluation",
        "",
        f"- Fixtures: {payload['fixture_count']}",
        f"- Cases: {payload['case_count']}",
        f"- Expectation failures: {payload['expectation_failure_count']}",
        f"- Model-surface isolation violations: {payload['model_surface_violation_count']}",
        "",
        "| Fixture | Case | Schema | Primary | Passed | Expectation met |",
        "|---|---|---:|---:|---:|---:|",
    ]
    for case in payload["cases"]:
        report = case["report"]
        metrics = case["metrics"]
        primary_met = report.get("primary_expectation_met", True)
        expectation_met = report["expectation_met"] and primary_met
        lines.append(
            f"| `{case['fixture']}` | `{case['case']}` | "
            f"{metrics['schema_validity']:.3f} | "
            f"{metrics['atom_primary_metric']:.3f} | "
            f"{str(report['passed']).lower()} | "
            f"{str(expectation_met).lower()} |"
        )
    return "\n".join(lines) + "\n"


def manifest_markdown(results: list[dict[str, Any]]) -> str:
    lines = [
        "# Stage B v4 Model Artifact Evaluation",
        "",
        "| Run | Fixture | Model | Arm | Schema | Primary | Passed |",
        "|---|---|---|---|---:|---:|---:|",
    ]
    for result in results:
        metrics = result["metrics"]
        lines.append(
            f"| `{result['run_id']}` | `{result['fixture']}` | "
            f"`{result['model']}` | `{result['harness_arm']}` | "
            f"{metrics['schema_validity']:.3f} | "
            f"{metrics['atom_primary_metric']:.3f} | "
            f"{str(result['passed']).lower()} |"
        )
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--atoms-dir", required=True)
    parser.add_argument("--fixtures", nargs="*", default=None)
    parser.add_argument("--manifest", default=None)
    parser.add_argument("--local-check", action="store_true")
    parser.add_argument("--output-runs", required=True)
    parser.add_argument("--output-md", required=True)
    args = parser.parse_args()

    atoms_dir = Path(args.atoms_dir)
    if args.local_check:
        evaluate_local(
            atoms_dir=atoms_dir,
            fixtures=args.fixtures,
            output_json=Path(args.output_runs),
            output_md=Path(args.output_md),
        )
    elif args.manifest:
        evaluate_manifest(
            manifest_path=Path(args.manifest),
            atoms_dir=atoms_dir,
            output_json=Path(args.output_runs),
            output_md=Path(args.output_md),
        )
    else:
        raise SystemExit("Use either --local-check or --manifest")


if __name__ == "__main__":
    main()
