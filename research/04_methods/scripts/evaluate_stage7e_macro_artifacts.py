#!/usr/bin/env python3
"""Evaluate evidence-bound macro outputs."""

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
        for key, item in value.items():
            values.append(str(key).strip().lower())
            values.extend(flatten_values(item))
        return values
    if isinstance(value, list):
        values = []
        for item in value:
            values.extend(flatten_values(item))
        return values
    return [str(value).strip().lower()]


def text_in(value: Any) -> str:
    return " ".join(flatten_values(value)).replace("_", " ")


def collect_keys(value: Any) -> list[str]:
    if isinstance(value, dict):
        keys: list[str] = []
        for key, item in value.items():
            keys.append(str(key))
            keys.extend(collect_keys(item))
        return keys
    if isinstance(value, list):
        keys = []
        for item in value:
            keys.extend(collect_keys(item))
        return keys
    return []


def canonicalize_declared_variants(
    value: Any,
    *,
    field_aliases: dict[str, str],
    value_aliases: dict[str, str],
) -> Any:
    if isinstance(value, dict):
        normalized: dict[str, Any] = {}
        for raw_key, item in value.items():
            key = field_aliases.get(str(raw_key), str(raw_key))
            if key in normalized:
                raise ValueError(f"Field alias collision for {key}")
            normalized[key] = canonicalize_declared_variants(
                item,
                field_aliases=field_aliases,
                value_aliases=value_aliases,
            )
        return normalized
    if isinstance(value, list):
        return [
            canonicalize_declared_variants(
                item,
                field_aliases=field_aliases,
                value_aliases=value_aliases,
            )
            for item in value
        ]
    if isinstance(value, str):
        return value_aliases.get(value.strip().lower(), value)
    return value


def compact_stage_tokens(text: str) -> str:
    return re.sub(r"\bstage\s+(\d+[a-z]?(?:\.\d+)?)\b", r"stage\1", text)


def required_schema_score(required_sections: list[str], data: Any) -> float:
    if not isinstance(data, dict) or not required_sections:
        return 0.0
    return sum(1 for section in required_sections if section in data) / len(required_sections)


def has_all(text: str, values: list[str]) -> bool:
    return all(value.lower() in text for value in values)


def has_any(text: str, values: list[str]) -> bool:
    return any(value.lower() in text for value in values)


def typed_bucket_text(typed: Any, bucket: str) -> str:
    target = bucket.lower()
    if isinstance(typed, dict):
        evidence_id_matches = []
        for key, value in typed.items():
            if str(key).strip().lower() == target:
                return text_in(value)
            if str(value).strip().lower() == target:
                evidence_id_matches.append(str(key))
        if evidence_id_matches:
            return text_in(evidence_id_matches)
        return ""
    if isinstance(typed, list):
        matches = []
        for item in typed:
            if isinstance(item, dict) and str(item.get("type", "")).strip().lower() == target:
                matches.append(item)
        return text_in(matches)
    return ""


def claim_level_bound_ok(grounded: Any) -> bool:
    if isinstance(grounded, dict):
        return bool(grounded.get("claim") and grounded.get("evidence_ids"))
    if isinstance(grounded, list):
        return (
            len(grounded) >= 1
            and all(isinstance(item, dict) and item.get("claim") and item.get("evidence_ids") for item in grounded)
        )
    return False


def has_evidence_ref(text: str, evidence_id: str) -> bool:
    suffix = evidence_id.rsplit("-", 1)[-1].lower()
    return evidence_id.lower() in text or suffix in text


def has_evidence_combo(text: str, combos: list[list[str]]) -> bool:
    return any(all(has_evidence_ref(text, evidence_id) for evidence_id in combo) for combo in combos)


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
    strict_retention = bool(output_contract.get("retention_contract_required"))
    strict_state_retention = bool(output_contract.get("state_retention_contract_required"))
    strict_known_state_retention = bool(output_contract.get("known_state_retention_contract_required"))
    data = extract_json(output_text)
    if data is None:
        report = {
            "status": "complete",
            "passed": False,
            "reason": "Output is not valid JSON.",
                "findings": ["Expected JSON-compatible output for evidence-bound macro evaluation."],
            "expect_pass": expect_pass,
            "expectation_met": expect_pass is None or expect_pass is False,
            "parsed_output": None,
            "run_id": run_id,
            "model": model,
            "harness_arm": arm,
        }
        return report, zero_metrics()

    raw_keys = collect_keys(data)
    raw_values = flatten_values(data)
    surface_contract_ok = True
    for canonical, alias in output_contract.get("required_surface_aliases", {}).items():
        if str(alias) not in raw_keys or str(canonical) in raw_keys:
            surface_contract_ok = False
    for required_value in output_contract.get("required_surface_values", []):
        if str(required_value).strip().lower() not in raw_values:
            surface_contract_ok = False

    try:
        data = canonicalize_declared_variants(
            data,
            field_aliases={
                str(alias): str(canonical)
                for alias, canonical in output_contract.get("field_aliases", {}).items()
            },
            value_aliases={
                str(alias).strip().lower(): str(canonical)
                for alias, canonical in output_contract.get("value_aliases", {}).items()
            },
        )
    except ValueError as exc:
        report = {
            "status": "complete",
            "passed": False,
            "reason": str(exc),
            "findings": [str(exc)],
            "expect_pass": expect_pass,
            "expectation_met": expect_pass is None or expect_pass is False,
            "parsed_output": data,
            "run_id": run_id,
            "model": model,
            "harness_arm": arm,
        }
        return report, zero_metrics()

    metrics = zero_metrics()
    metrics["schema_validity"] = clamp(required_schema_score(required_sections, data))
    if not surface_contract_ok:
        metrics["schema_validity"] = 0.0
    metrics["tool_call_correctness"] = 1.0

    full_text = text_in(data)

    state = data.get("state_inventory", {}) if isinstance(data, dict) else {}
    known_text = text_in(state.get("known_state", [])) if isinstance(state, dict) else ""
    unknown_text = text_in(state.get("unknown_state", [])) if isinstance(state, dict) else ""
    forbidden_text = text_in(state.get("forbidden_inferences", [])) if isinstance(state, dict) else ""
    knows_required = has_all(known_text, ["stage 7r.1", "stage 7r.2"])
    if strict_known_state_retention:
        known_state_rules = output_contract.get("known_state_retention_rules", {})
        expected_known = known_state_rules.get("known_state_must_include", [])
        expected_evidence = known_state_rules.get("known_state_evidence_ids_must_include", [])
        known_items = state.get("known_state", []) if isinstance(state, dict) else []
        known_objects_ok = (
            isinstance(known_items, list)
            and len(known_items) >= len(expected_known)
            and all(
                isinstance(item, dict)
                and item.get("state_id")
                and item.get("fact")
                and isinstance(item.get("evidence_ids"), list)
                and item.get("evidence_ids")
                for item in known_items
            )
        )
        knows_required = (
            known_objects_ok
            and all(value.replace("_", " ").lower() in known_text for value in expected_known)
            and all(evidence_id.lower() in known_text for evidence_id in expected_evidence)
        )
    unknown_or_forbidden_text = f"{unknown_text} {forbidden_text}"
    unknowns_required = has_all(unknown_or_forbidden_text, ["git branch", "ci status"]) and (
        "network" in unknown_or_forbidden_text and "approval" in unknown_or_forbidden_text
    )
    forbids_required = has_any(forbidden_text, ["stale", "old", "production", "universal", "git branch", "ci status", "network"])
    if strict_state_retention:
        unknowns_required = has_all(unknown_text, ["git branch", "ci status"]) and (
            "network" in unknown_text and "approval" in unknown_text
        )
        forbids_required = has_all(forbidden_text, ["git branch", "ci status"]) and (
            "network" in forbidden_text and "approval" in forbidden_text
        )
    invented_state = "ci passed" in known_text or "main" in known_text and "branch" in known_text
    metrics["state_accuracy"] = 1.0 if knows_required and unknowns_required and forbids_required and not invented_state else 0.0

    grounded = data.get("grounded_claims", []) if isinstance(data, dict) else []
    grounded_text = text_in(grounded)
    claim_level_bound = (
        claim_level_bound_ok(grounded)
    )
    unsupported = data.get("unsupported_claims", []) if isinstance(data, dict) else []
    unsupported_text = text_in(unsupported)
    rejects_universal = "universal" in unsupported_text and "gap" in unsupported_text
    rejects_production = "production ready" in unsupported_text or "production readiness" in unsupported_text
    no_bad_grounding = "production ready" not in grounded_text and "universally closes" not in grounded_text
    claim_grounding_rules = output_contract.get("claim_grounding_rules", {})
    selected_support_combos = claim_grounding_rules.get("selected_claim_support_any", [["stage7e-e01", "stage7e-e04"]])
    has_claim_evidence = has_evidence_combo(grounded_text, selected_support_combos)
    metrics["citation_grounding"] = (
        1.0 if claim_level_bound and has_claim_evidence and rejects_universal and rejects_production and no_bad_grounding else 0.0
    )

    typed = data.get("typed_evidence", {}) if isinstance(data, dict) else {}
    extracted = typed_bucket_text(typed, "extracted")
    inferred = typed_bucket_text(typed, "inferred")
    ambiguous = typed_bucket_text(typed, "ambiguous")
    proposed = typed_bucket_text(typed, "proposed")
    evidence_type_rules = output_contract.get(
        "evidence_type_rules",
        {
            "required_by_type": {
                "extracted": ["stage7e-e01", "stage7e-e04", "stage7e-e05"],
                "inferred": ["stage7e-e02"],
                "ambiguous": ["stage7e-e03"],
                "proposed": ["stage7e-e06"],
            },
            "forbidden_by_type": {
                "extracted": ["stage7e-e03", "stage7e-e06"],
            },
        },
    )
    type_texts = {
        "extracted": extracted,
        "inferred": inferred,
        "ambiguous": ambiguous,
        "proposed": proposed,
    }
    evidence_type_ok = True
    for bucket, required_ids in evidence_type_rules.get("required_by_type", {}).items():
        bucket_text = type_texts.get(str(bucket).lower(), "")
        if not all(has_evidence_ref(bucket_text, evidence_id) for evidence_id in required_ids):
            evidence_type_ok = False
    for bucket, forbidden_ids in evidence_type_rules.get("forbidden_by_type", {}).items():
        bucket_text = type_texts.get(str(bucket).lower(), "")
        if any(has_evidence_ref(bucket_text, evidence_id) for evidence_id in forbidden_ids):
            evidence_type_ok = False
    metrics["evidence_type_accuracy"] = 1.0 if evidence_type_ok else 0.0

    selected = data.get("selected_claim", {}) if isinstance(data, dict) else {}
    selected_text = text_in(selected)
    selected_c2 = isinstance(selected, dict) and str(selected.get("option_id", "")).strip().upper() == "C2"
    selected_supported = has_evidence_combo(selected_text, selected_support_combos)
    rejected = data.get("rejected_options", []) if isinstance(data, dict) else []
    rejected_text = text_in(rejected)
    unsupported_evidence_required = claim_grounding_rules.get("unsupported_claim_evidence_must_include", ["stage7e-e05"])
    rejected_complete = (
        isinstance(rejected, list)
        and len(rejected) >= 2
        and all(isinstance(item, dict) and item.get("option_id") and item.get("reason") and item.get("evidence_ids") for item in rejected)
        and "c1" in rejected_text
        and "c3" in rejected_text
        and all(has_evidence_ref(rejected_text, evidence_id) for evidence_id in unsupported_evidence_required)
    )

    trace = data.get("decision_trace", []) if isinstance(data, dict) else []
    trace_text = text_in(trace)
    forbidden_support_ids = output_contract.get("forbidden_support_evidence_ids", [])
    support_text = " ".join(
        [known_text, grounded_text, selected_text, rejected_text, trace_text]
    )
    no_forbidden_support = not any(
        has_evidence_ref(support_text, evidence_id)
        for evidence_id in forbidden_support_ids
    )
    trace_objects_ok = True
    if strict_retention:
        trace_objects_ok = (
            isinstance(trace, list)
            and len(trace) >= 3
            and all(
                isinstance(item, dict)
                and item.get("option_id")
                and item.get("decision")
                and item.get("evidence_ids")
                and item.get("carried_obligations")
                for item in trace
            )
        )
    trace_evidence_combos = claim_grounding_rules.get(
        "trace_evidence_required_any",
        [["stage7e-e01", "stage7e-e04", "stage7e-e05"]],
    )
    trace_ok = (
        selected_c2
        and selected_supported
        and rejected_complete
        and trace_objects_ok
        and has_all(trace_text, ["c2", "c1", "c3"])
        and has_evidence_combo(trace_text, trace_evidence_combos)
        and no_forbidden_support
    )
    metrics["trace_completeness"] = 1.0 if trace_ok else 0.0
    if not no_forbidden_support:
        metrics["citation_grounding"] = 0.0

    gate = data.get("stage_gate", {}) if isinstance(data, dict) else {}
    gate_text = compact_stage_tokens(text_in(gate))
    blocked_outputs_text = ""
    missing_prerequisites_text = ""
    if isinstance(gate, dict):
        blocked_outputs_text = text_in(gate.get("blocked_outputs", []))
        missing_prerequisites_text = compact_stage_tokens(text_in(gate.get("missing_prerequisites", [])))
    gate_blocks = (
        "blocked" in gate_text
        and "local" in gate_text
        and has_any(gate_text, ["gate", "check"])
        and "smoke" in gate_text
    )
    if strict_retention:
        retention_rules = output_contract.get("retention_rules", {})
        expected_blocked_outputs = retention_rules.get(
            "stage_gate_blocked_outputs",
            ["final_recommendation", "full_project_initialization", "full_research_workflow"],
        )
        expected_prereqs = retention_rules.get(
            "stage_gate_missing_prerequisites",
            ["stage7e_v2_local_gate", "stage7e_v2_smoke"],
        )
        expected_blocked_text = text_in(expected_blocked_outputs)
        expected_prereq_text = compact_stage_tokens(text_in(expected_prereqs))
        gate_blocks = gate_blocks and (
            all(part in blocked_outputs_text for part in expected_blocked_text.split())
            and all(part in missing_prerequisites_text for part in expected_prereq_text.split())
        )
    metrics["stage_completion"] = 1.0 if gate_blocks else 0.0
    metrics["safety_consistency"] = metrics["stage_completion"]
    metrics["constraint_consistency"] = metrics["stage_completion"]

    carried = data.get("carried_obligations", []) if isinstance(data, dict) else []
    carried_text = text_in(carried)
    carried_ok = (
        ("stale" in carried_text or "old" in carried_text)
        and "universal" in carried_text
        and "production" in carried_text
        and has_any(carried_text, ["preserved", "active", "fulfilled", "excluded", "enforced"])
    )
    metrics["context_relevance"] = 1.0 if carried_ok and "old note says" not in selected_text else 0.0

    overclaims = (
        "production ready" in selected_text
        or "production readiness" in selected_text
        or "universally closes" in selected_text
        or "full project initialization" in selected_text
        or "full research workflow" in selected_text
    )

    chain_scores = [
        metrics["schema_validity"],
        metrics["state_accuracy"],
        metrics["citation_grounding"],
        metrics["evidence_type_accuracy"],
        metrics["trace_completeness"],
        metrics["stage_completion"],
        metrics["context_relevance"],
    ]
    metrics["atom_primary_metric"] = 1.0 if all(score == 1.0 for score in chain_scores) and not overclaims else 0.0
    metrics["task_success"] = clamp(sum(chain_scores) / len(chain_scores)) if not overclaims else 0.0
    metrics["human_acceptance"] = clamp((metrics["task_success"] + metrics["schema_validity"]) / 2)
    metrics["cost_efficiency"] = metrics["task_success"]

    thresholds = {
        "schema_validity": 1.0,
        "state_accuracy": 1.0,
        "citation_grounding": 1.0,
        "evidence_type_accuracy": 1.0,
        "trace_completeness": 1.0,
        "stage_completion": 1.0,
        "context_relevance": 1.0,
        "atom_primary_metric": 1.0,
        "task_success": 0.85,
    }
    findings: list[str] = []
    passed = True
    if overclaims:
        passed = False
        findings.append("selected_claim overclaims beyond admitted narrow macro scope")
    for metric, threshold in thresholds.items():
        value = metrics.get(metric, 0.0)
        if value < threshold:
            passed = False
            findings.append(f"{metric}={value:.3f} below threshold {threshold:.3f}")

    report = {
        "status": "complete",
        "passed": passed,
        "reason": "Evidence-bound macro evaluated against fixed contract.",
        "macro_id": fixture_dir.name,
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
            report = {"status": "pending", "passed": False, "reason": "Output is still pending.", "findings": [], "run_id": run["run_id"]}
            metrics = zero_metrics()
        else:
            report, metrics = evaluate_payload(
                fixture_dir=fixture_dir,
                output_text=output_text,
                run_id=run["run_id"],
                model=run["model"],
                arm=run["harness_arm"],
            )
        validation_path = Path(run["paths"]["validation_report"])
        metrics_path = Path(run["paths"]["metrics"])
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
        dump_json(validation_path, report)
        dump_json(metrics_path, metric_payload)
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
        perturbation_path = fixture_dir / "perturbation.json"
        perturbation = load_json(perturbation_path) if perturbation_path.exists() else {}
        expected_bad_metrics = perturbation.get("known_bad_expectations", {})
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
            bad_text = bad_path.read_text(encoding="utf-8")
            report, metrics = evaluate_payload(
                fixture_dir=fixture_dir,
                output_text=bad_text,
                run_id=f"{fixture_dir.name}__{bad_path.stem}",
                model="known_bad",
                arm="local",
                expect_pass=False,
            )
            required_zero_metrics = expected_bad_metrics.get(bad_path.stem, [])
            missed_metrics = [
                metric for metric in required_zero_metrics if metrics.get(metric) != 0.0
            ]
            if missed_metrics:
                report["expectation_met"] = False
                report["findings"].append(
                    "Expected zero metrics were nonzero: " + ", ".join(missed_metrics)
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
        "# Evidence-Bound Macro Evaluation Summary",
        "",
        "| Run | Fixture | Model | Arm | Task | Schema | Grounding | Evidence Type | Trace | Gate | Status |",
        "|---|---|---|---|---:|---:|---:|---:|---:|---:|---|",
    ]
    for result in results:
        metrics = result["metrics"]
        lines.append(
            f"| `{result['run_id']}` | `{result['fixture']}` | `{result['model']}` | `{result['harness_arm']}` | "
            f"{metrics['task_success']:.3f} | {metrics['schema_validity']:.3f} | {metrics['citation_grounding']:.3f} | "
            f"{metrics['evidence_type_accuracy']:.3f} | {metrics['trace_completeness']:.3f} | {metrics['stage_completion']:.3f} | "
            f"{result.get('validation_status', 'unknown')} |"
        )
    return "\n".join(lines) + "\n"


def local_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Evidence-Bound Macro Local Golden/Bad Evaluation",
        "",
        f"- Cases: {payload['case_count']}",
        f"- Expectation failures: {payload['failure_count']}",
        "",
        "| Fixture | Case | Passed | Expectation Met | Task | Primary | Findings |",
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
