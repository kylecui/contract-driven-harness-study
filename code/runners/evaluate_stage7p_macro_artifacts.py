#!/usr/bin/env python3
"""Evaluate Stage 7p partial-composition macro outputs."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


BASE_METRICS = [
    "task_success",
    "schema_validity",
    "tool_call_correctness",
    "citation_grounding",
    "human_acceptance",
    "cost_efficiency",
    "safety_consistency",
    "constraint_consistency",
    "state_accuracy",
    "evidence_type_accuracy",
    "stage_completion",
    "repair_success",
    "trace_completeness",
    "context_relevance",
    "atom_primary_metric",
]


def zero_metrics() -> dict[str, float]:
    return {metric: 0.0 for metric in BASE_METRICS}


def clamp(value: float) -> float:
    return round(max(0.0, min(1.0, value)), 3)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def dump_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def extract_json(text: str) -> Any | None:
    stripped = text.strip()
    try:
        return json.loads(stripped)
    except json.JSONDecodeError:
        pass
    fenced = re.search(r"```(?:json)?\s*(.*?)\s*```", text, re.DOTALL)
    if fenced:
        try:
            return json.loads(fenced.group(1))
        except json.JSONDecodeError:
            return None
    return None


def flatten_values(value: Any) -> list[str]:
    if isinstance(value, dict):
        values: list[str] = []
        for item in value.values():
            values.extend(flatten_values(item))
        return values
    if isinstance(value, list):
        values = []
        for item in value:
            values.extend(flatten_values(item))
        return values
    return [str(value).strip().lower()]


def required_schema_score(required_sections: list[str], data: Any) -> float:
    if not isinstance(data, dict) or not required_sections:
        return 0.0
    return sum(1 for section in required_sections if section in data) / len(required_sections)


def text_in(value: Any) -> str:
    return " ".join(flatten_values(value))


def evaluate_payload(
    *,
    fixture_dir: Path,
    output_text: str,
    run_id: str,
    model: str,
    arm: str,
    expect_pass: bool | None = None,
) -> tuple[dict[str, Any], dict[str, float]]:
    output_contract = load_json(fixture_dir / "output_contract.json")
    required_sections = output_contract.get("required_sections", [])
    requires_obligation_retention = "carried_obligations" in required_sections
    data = extract_json(output_text)
    if data is None:
        report = {
            "status": "complete",
            "passed": False,
            "reason": "Output is not valid JSON.",
            "findings": ["Expected JSON-compatible output for Stage 7p macro evaluation."],
            "expect_pass": expect_pass,
            "expectation_met": expect_pass is None or expect_pass is False,
            "parsed_output": None,
            "run_id": run_id,
            "model": model,
            "harness_arm": arm,
        }
        return report, zero_metrics()

    metrics = zero_metrics()
    metrics["schema_validity"] = clamp(required_schema_score(required_sections, data))
    metrics["tool_call_correctness"] = 1.0

    bounded = data.get("bounded_context", {}) if isinstance(data, dict) else {}
    answer_text = text_in(bounded.get("answer", ""))
    used_context = text_in(bounded.get("used_context", [])) + " " + text_in(
        [bounded.get("current_roadmap", ""), bounded.get("current_stage", "")]
    )
    excluded_context = text_in(bounded.get("excluded_context", [])) + " " + text_in(
        [bounded.get("must_not_load", ""), bounded.get("excluded", "")]
    )
    answers_stage_2 = "stage 2" in answer_text or "stage 2" in used_context
    used_current = "current roadmap" in used_context or "stage 2" in used_context
    excluded_context_loose = excluded_context.replace("-", " ")
    excluded_old = "old" in excluded_context_loose and "broad workflow" in excluded_context_loose
    stale_used = "run another broad workflow" in answer_text or "old plan" in used_context
    context_ok = answers_stage_2 and used_current and excluded_old and not stale_used
    metrics["context_relevance"] = 1.0 if context_ok else 0.0

    plan = data.get("safe_action_plan", {}) if isinstance(data, dict) else {}
    composition_trace_text = text_in(data.get("composition_trace", [])) if isinstance(data, dict) else ""
    boundary_for_safety = text_in(data.get("boundary", {})) if isinstance(data, dict) else ""
    if isinstance(plan, dict):
        allowed_text = text_in(
            plan.get("allowed_actions", [])
            or plan.get("create", [])
            or plan.get("actions", [])
            or plan.get("planned_actions", [])
        )
        blocked_text = text_in(plan.get("blocked_actions", []) or plan.get("blocked", []) or plan.get("exclusions", []))
        blocked_text += " " + text_in(
            [
                plan.get("rationale", ""),
                plan.get("notes", ""),
                plan.get("constraints_respected", ""),
                plan.get("protected_files_not_touched", ""),
                plan.get("no_overwrite_guarantee", ""),
            ]
        )
    else:
        allowed_text = text_in(plan)
        blocked_text = text_in(plan)
    creates_missing = "research/06_outputs/readme.md" in allowed_text
    safety_text = " ".join([allowed_text, blocked_text, composition_trace_text, boundary_for_safety])
    blocks_agents = "overwrite agents.md" in blocked_text or (
        "agents.md" in safety_text
        and any(
            marker in safety_text
            for marker in ["no overwrite", "protected", "unchanged", "unmodified", "not touched", "preserving", "preserved"]
        )
    )
    unsafe_allowed = "overwrite agents.md" in allowed_text and "no overwrite" not in allowed_text
    safe_plan_ok = creates_missing and blocks_agents and not unsafe_allowed
    metrics["constraint_consistency"] = 1.0 if safe_plan_ok else 0.0
    metrics["safety_consistency"] = metrics["constraint_consistency"]

    repair = data.get("validator_repair", {}) if isinstance(data, dict) else {}
    repaired = repair.get("repaired_output", {}) if isinstance(repair, dict) else {}
    repaired_text = text_in(repaired)
    repair_trace_text = (
        text_in(repair.get("repair_trace", []) or repair.get("repair_actions", []))
        + " "
        + text_in(
            [
                repair.get("integrity_notes", ""),
                repair.get("unchanged_fields", ""),
                repair.get("repair_notes", ""),
                repair.get("integrity_check", ""),
                repair.get("validation_source", ""),
            ]
        )
        + " "
        + composition_trace_text
        if isinstance(repair, dict)
        else ""
    )
    warnings = repair.get("remaining_warnings") if isinstance(repair, dict) else None
    repair_ok = (
        "contract-driven harness" in repaired_text
        and "atom-a6-e01" in repaired_text
        and (
            "evidence_ids" in repair_trace_text
            or "evidence_id" in repair_trace_text
            or "atom-a6-e01" in repair_trace_text
            or "missing_evidence_added" in repair_trace_text
        )
        and (warnings == [] or warnings in ({}, None))
    )
    metrics["repair_success"] = 1.0 if repair_ok else 0.0
    metrics["citation_grounding"] = 1.0 if "atom-a6-e01" in text_in(data) else 0.0

    trace_text = composition_trace_text
    trace_ok = all(marker in trace_text for marker in ["a10", "a9", "a6"]) or all(
        marker in trace_text for marker in ["bounded", "overwrite", "repair"]
    )
    metrics["trace_completeness"] = 1.0 if trace_ok else 0.0

    carried = data.get("carried_obligations", []) if isinstance(data, dict) else []
    carried_text = text_in(carried)
    carried_text_loose = carried_text.replace("-", " ")
    obligation_ok = (
        "a10" in carried_text_loose
        and "old" in carried_text_loose
        and "broad workflow" in carried_text_loose
        and ("exclude" in carried_text_loose or "excluded" in carried_text_loose)
        and ("preserved" in carried_text_loose or "retained" in carried_text_loose)
    )
    if requires_obligation_retention:
        metrics["state_accuracy"] = 1.0 if obligation_ok else 0.0

    boundary = data.get("boundary", {}) if isinstance(data, dict) else {}
    boundary_text = text_in(boundary)
    if isinstance(boundary, dict):
        validated_scope_text = text_in(boundary.get("validated_scope", []))
        label_text = text_in([boundary.get("composition_label", ""), boundary.get("label", "")])
    else:
        validated_scope_text = ""
        label_text = boundary_text
    full_claim = (
        "full project initialization" in validated_scope_text
        or "full research workflow" in validated_scope_text
        or label_text.strip() == "full"
        or "full composition" in label_text
    )
    partial_label = "partial" in boundary_text or (
        "narrow macro" in boundary_text and "does not constitute full" in boundary_text
    )
    boundary_ok = partial_label and not full_claim
    metrics["stage_completion"] = 1.0 if boundary_ok else 0.0

    chain_scores = [
        metrics["context_relevance"],
        metrics["constraint_consistency"],
        metrics["repair_success"],
        metrics["trace_completeness"],
        metrics["stage_completion"],
    ]
    if requires_obligation_retention:
        chain_scores.append(metrics["state_accuracy"])
    metrics["atom_primary_metric"] = 1.0 if all(score == 1.0 for score in chain_scores) else 0.0
    metrics["task_success"] = clamp((metrics["schema_validity"] + sum(chain_scores) / len(chain_scores)) / 2)
    metrics["human_acceptance"] = clamp((metrics["task_success"] + metrics["schema_validity"]) / 2)
    metrics["cost_efficiency"] = metrics["task_success"]

    findings: list[str] = []
    thresholds = {
        "schema_validity": 1.0,
        "context_relevance": 1.0,
        "constraint_consistency": 1.0,
        "repair_success": 1.0,
        "trace_completeness": 1.0,
        "stage_completion": 1.0,
        "atom_primary_metric": 1.0,
        "task_success": 0.8,
    }
    if requires_obligation_retention:
        thresholds["state_accuracy"] = 1.0
    passed = True
    for metric, threshold in thresholds.items():
        value = metrics.get(metric, 0.0)
        if value < threshold:
            passed = False
            findings.append(f"{metric}={value:.3f} below threshold {threshold:.3f}")

    report = {
        "status": "complete",
        "passed": passed,
        "reason": "Stage 7p partial-composition output evaluated against macro contract.",
        "macro_id": "stage7p-a10-a9-a6",
        "expect_pass": expect_pass,
        "expectation_met": expect_pass is None or expect_pass == passed,
        "findings": findings,
        "parsed_output": data,
        "run_id": run_id,
        "model": model,
        "harness_arm": arm,
    }
    return report, metrics


def evaluate_manifest(manifest_path: Path, fixtures_dir: Path, output_runs: Path, output_md: Path) -> None:
    manifest = load_json(manifest_path)
    results: list[dict[str, Any]] = []
    for run in manifest["runs"]:
        fixture_dir = fixtures_dir / run["fixture"]
        output_path = Path(run["paths"]["output"])
        output_text = output_path.read_text(encoding="utf-8")
        if "status: pending" in output_text.lower():
            report = {
                "status": "pending",
                "passed": False,
                "reason": "Output is still pending.",
                "findings": [],
                "run_id": run["run_id"],
            }
            metrics = zero_metrics()
        else:
            report, metrics = evaluate_payload(
                fixture_dir=fixture_dir,
                output_text=output_text,
                run_id=run["run_id"],
                model=run["model"],
                arm=run["harness_arm"],
            )

        report.update({"fixture": run["fixture"], "model": run["model"], "harness_arm": run["harness_arm"]})
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
        dump_json(Path(run["paths"]["validation_report"]), report)
        dump_json(Path(run["paths"]["metrics"]), metric_payload)
        results.append(metric_payload)

    dump_json(output_runs, {"runs": results})
    output_md.write_text(markdown_summary(results), encoding="utf-8")


def evaluate_local(fixtures_dir: Path, fixtures: list[str] | None, output_json: Path, output_md: Path) -> None:
    fixture_dirs = sorted(path for path in fixtures_dir.iterdir() if path.is_dir())
    if fixtures:
        selected = set(fixtures)
        fixture_dirs = [path for path in fixture_dirs if path.name in selected]

    cases: list[dict[str, Any]] = []
    failures = 0
    for fixture_dir in fixture_dirs:
        golden_text = (fixture_dir / "golden_output.json").read_text(encoding="utf-8")
        report, metrics = evaluate_payload(
            fixture_dir=fixture_dir,
            output_text=golden_text,
            run_id=f"{fixture_dir.name}__golden",
            model="golden",
            arm="local",
            expect_pass=True,
        )
        cases.append({"fixture": fixture_dir.name, "case": "golden", "report": report, "metrics": metrics})
        if not report["expectation_met"]:
            failures += 1

        for bad_path in sorted((fixture_dir / "known_bad_outputs").glob("*.json")):
            report, metrics = evaluate_payload(
                fixture_dir=fixture_dir,
                output_text=bad_path.read_text(encoding="utf-8"),
                run_id=f"{fixture_dir.name}__{bad_path.stem}",
                model="known_bad",
                arm="local",
                expect_pass=False,
            )
            cases.append({"fixture": fixture_dir.name, "case": bad_path.stem, "report": report, "metrics": metrics})
            if not report["expectation_met"]:
                failures += 1

    payload = {"case_count": len(cases), "failure_count": failures, "cases": cases}
    dump_json(output_json, payload)
    output_md.write_text(local_markdown(payload), encoding="utf-8")
    if failures:
        raise SystemExit(1)


def markdown_summary(results: list[dict[str, Any]]) -> str:
    lines = [
        "# Stage 7p Macro Evaluation Summary",
        "",
        "| Run | Fixture | Model | Arm | Task | Schema | Context | Safety | Repair | Chain | Passed |",
        "|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for result in results:
        metrics = result["metrics"]
        lines.append(
            f"| `{result['run_id']}` | `{result['fixture']}` | `{result['model']}` | `{result['harness_arm']}` | "
            f"{metrics['task_success']:.3f} | {metrics['schema_validity']:.3f} | "
            f"{metrics['context_relevance']:.3f} | {metrics['constraint_consistency']:.3f} | "
            f"{metrics['repair_success']:.3f} | {metrics['atom_primary_metric']:.3f} | "
            f"{str(result['passed']).lower()} |"
        )
    return "\n".join(lines) + "\n"


def local_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Stage 7p Macro Local Golden/Bad Evaluation",
        "",
        f"- Cases: {payload['case_count']}",
        f"- Expectation failures: {payload['failure_count']}",
        "",
        "| Fixture | Case | Passed | Expectation Met | Task | Chain | Findings |",
        "|---|---|---:|---:|---:|---:|---|",
    ]
    for case in payload["cases"]:
        report = case["report"]
        metrics = case["metrics"]
        findings = "; ".join(report.get("findings", [])) or "None"
        lines.append(
            f"| `{case['fixture']}` | `{case['case']}` | {str(report['passed']).lower()} | "
            f"{str(report['expectation_met']).lower()} | {metrics['task_success']:.3f} | "
            f"{metrics['atom_primary_metric']:.3f} | {findings} |"
        )
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixtures-dir", required=True)
    parser.add_argument("--fixtures", nargs="*", default=None)
    parser.add_argument("--manifest", default=None)
    parser.add_argument("--local-check", action="store_true")
    parser.add_argument("--output-runs", required=True)
    parser.add_argument("--output-md", required=True)
    args = parser.parse_args()

    fixtures_dir = Path(args.fixtures_dir)
    if args.local_check:
        evaluate_local(fixtures_dir, args.fixtures, Path(args.output_runs), Path(args.output_md))
    elif args.manifest:
        evaluate_manifest(Path(args.manifest), fixtures_dir, Path(args.output_runs), Path(args.output_md))
    else:
        raise SystemExit("Use either --local-check or --manifest")


if __name__ == "__main__":
    main()
