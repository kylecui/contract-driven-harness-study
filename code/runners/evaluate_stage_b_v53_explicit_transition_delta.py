#!/usr/bin/env python3
"""Evaluate Stage B v5.3 explicit transition-delta fixtures."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from evaluate_stage_b_v5_state_transition import dump_json, load_json, metrics_match
from evaluate_stage_b_v52_evidence_binding_ablation import evaluate_payload


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


def check_pairs(fixtures: list[Path]) -> list[dict[str, str]]:
    by_condition: dict[str, list[tuple[Path, dict[str, Any]]]] = {}
    for fixture in fixtures:
        spec = load_json(fixture / "evaluation_spec.json")
        by_condition.setdefault(
            spec["perturbation_condition"], []
        ).append((fixture, spec))

    violations = []
    equal_fields = [
        "expected_payload",
        "expected_known_state",
        "expected_unknown_state",
        "expected_forbidden_inferences",
        "expected_transition_record",
        "expected_gate",
        "expected_attestation",
        "expected_postconditions",
        "reference_field",
    ]
    for condition, entries in by_condition.items():
        if len(entries) != 2:
            violations.append(
                {"condition": condition, "reason": "paired_fixture_missing"}
            )
            continue
        by_arm = {spec["protocol_arm"]: (path, spec) for path, spec in entries}
        if set(by_arm) != {"postcondition_only", "explicit_delta"}:
            violations.append(
                {"condition": condition, "reason": "paired_arm_mismatch"}
            )
            continue
        baseline_path, baseline = by_arm["postcondition_only"]
        delta_path, delta = by_arm["explicit_delta"]
        for field in equal_fields:
            if baseline[field] != delta[field]:
                violations.append(
                    {
                        "condition": condition,
                        "reason": f"paired_{field}_mismatch",
                    }
                )
        if baseline["expected_transition_delta"] is not None:
            violations.append(
                {
                    "condition": condition,
                    "reason": "baseline_delta_present",
                }
            )
        if not isinstance(delta["expected_transition_delta"], dict):
            violations.append(
                {
                    "condition": condition,
                    "reason": "treatment_delta_missing",
                }
            )
        baseline_contract = load_json(
            baseline_path / "output_contract.json"
        )
        delta_contract = load_json(delta_path / "output_contract.json")
        delta_object = delta_contract.pop("required_transition_delta", None)
        baseline_contract.pop("protocol_profile", None)
        delta_contract.pop("protocol_profile", None)
        baseline_contract["output_contract_id"] = "normalized"
        delta_contract["output_contract_id"] = "normalized"
        if baseline_contract != delta_contract:
            violations.append(
                {
                    "condition": condition,
                    "reason": "non_delta_contract_difference",
                }
            )
        if delta_object != delta["expected_transition_delta"]:
            violations.append(
                {
                    "condition": condition,
                    "reason": "delta_object_mismatch",
                }
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

    pair_violations = check_pairs(fixtures)
    payload = {
        "suite": "stage_b_v53_explicit_transition_delta_local",
        "fixture_count": len(fixtures),
        "case_count": len(cases),
        "expectation_failure_count": failures,
        "model_surface_violation_count": len(surface_violations),
        "model_surface_violations": surface_violations,
        "paired_protocol_violation_count": len(pair_violations),
        "paired_protocol_violations": pair_violations,
        "cases": cases,
    }
    dump_json(output_json, payload)
    output_md.write_text(local_markdown(payload), encoding="utf-8")
    if failures or surface_violations or pair_violations:
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
        report["protocol_arm"] = spec["protocol_arm"]
        metric_payload = {
            "run_id": run["run_id"],
            "fixture": run["fixture"],
            "task_class": run["task_type"],
            "model": run["model"],
            "harness_arm": run["harness_arm"],
            "protocol_arm": spec["protocol_arm"],
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
        "# Stage B v5.3 Explicit Transition-Delta Local Evaluation",
        "",
        f"- Fixtures: {payload['fixture_count']}",
        f"- Cases: {payload['case_count']}",
        f"- Expectation failures: {payload['expectation_failure_count']}",
        f"- Surface violations: {payload['model_surface_violation_count']}",
        f"- Paired-protocol violations: {payload['paired_protocol_violation_count']}",
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
        "# Stage B v5.3 Explicit Transition-Delta Model Evaluation",
        "",
        "| Run | Protocol | Condition | State | Evidence | Aggregate | Passed |",
        "|---|---|---|---:|---:|---:|---:|",
    ]
    for result in results:
        metrics = result["metrics"]
        lines.append(
            f"| `{result['run_id']}` | `{result['protocol_arm']}` | "
            f"`{result['perturbation_condition']}` | "
            f"{metrics['residual_unknown_vocabulary_accuracy']:.3f} | "
            f"{metrics['exact_evidence_array_preservation']:.3f} | "
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

