#!/usr/bin/env python3
"""Evaluate real-run artifacts for the first benchmark slice.

The evaluator is intentionally simple and fixture-specific. It gives the
pipeline a stable metrics shape before real model adapters are connected.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


METRIC_KEYS = [
    "task_success",
    "schema_validity",
    "tool_call_correctness",
    "citation_grounding",
    "human_acceptance",
    "cost_efficiency",
    "safety_consistency",
]


def zero_metrics() -> dict[str, float]:
    return {key: 0.0 for key in METRIC_KEYS}


def clamp(value: float) -> float:
    return round(max(0.0, min(1.0, value)), 3)


def normalize_value(value: Any) -> str:
    return str(value).strip().strip(".。").lower()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def pending_result(reason: str) -> tuple[dict[str, Any], dict[str, float]]:
    return {
        "status": "pending",
        "passed": False,
        "reason": reason,
        "findings": [],
    }, zero_metrics()


def extract_json_object(text: str) -> dict[str, Any] | None:
    stripped = text.strip()
    if stripped.startswith("{") and stripped.endswith("}"):
        try:
            return json.loads(stripped)
        except json.JSONDecodeError:
            return None

    fenced = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if fenced:
        try:
            return json.loads(fenced.group(1))
        except json.JSONDecodeError:
            return None
    return None


def evaluate_structured_extraction(output: str) -> tuple[dict[str, Any], dict[str, float]]:
    data = extract_json_object(output)
    if data is None:
        return {
            "status": "complete",
            "passed": False,
            "reason": "Output is not valid JSON.",
            "findings": ["Expected a JSON object with title, target_venue, primary_metric, evidence_ids."],
        }, zero_metrics()

    required = ["title", "target_venue", "primary_metric", "evidence_ids"]
    present = [key for key in required if key in data]
    schema_validity = len(present) / len(required)

    expected = {
        "title": "Topic-Aware Compaction",
        "target_venue": "COLM 2026",
        "primary_metric": "token savings",
    }
    correctness_checks = [
        normalize_value(data.get("title", "")) == expected["title"].lower(),
        normalize_value(data.get("target_venue", "")) == expected["target_venue"].lower(),
        expected["primary_metric"] in normalize_value(data.get("primary_metric", "")),
    ]
    evidence_ids = data.get("evidence_ids", [])
    if not isinstance(evidence_ids, list):
        evidence_ids = []
    expected_evidence = {"fixture-e01", "fixture-e02", "fixture-e03"}
    citation_grounding = len(expected_evidence.intersection(set(map(str, evidence_ids)))) / len(
        expected_evidence
    )
    task_success = (sum(correctness_checks) / len(correctness_checks) + citation_grounding) / 2

    metrics = {
        "task_success": clamp(task_success),
        "schema_validity": clamp(schema_validity),
        "tool_call_correctness": 1.0,
        "citation_grounding": clamp(citation_grounding),
        "human_acceptance": clamp((task_success + schema_validity) / 2),
        "cost_efficiency": clamp(task_success),
        "safety_consistency": 1.0 if data.get("backup_venue") in (None, "", "null") else 0.7,
    }
    report = {
        "status": "complete",
        "passed": metrics["task_success"] >= 0.8 and metrics["schema_validity"] == 1.0,
        "reason": "Structured extraction evaluated against fixture expectations.",
        "findings": [],
        "parsed_output": data,
    }
    return report, metrics


def evaluate_structured_extraction_hard(output: str) -> tuple[dict[str, Any], dict[str, float]]:
    data = extract_json_object(output)
    if data is None:
        return {
            "status": "complete",
            "passed": False,
            "reason": "Output is not valid JSON.",
            "findings": [
                "Expected a JSON object with title, target_venue, fallback_venue, primary_metric, blocker, evidence_ids."
            ],
        }, zero_metrics()

    required = [
        "title",
        "target_venue",
        "fallback_venue",
        "primary_metric",
        "blocker",
        "evidence_ids",
    ]
    present = [key for key in required if key in data]
    schema_validity = len(present) / len(required)

    expected = {
        "title": "Contract-Driven Agent Harness Engineering",
        "target_venue": "ACL 2026 Findings",
        "fallback_venue": "COLM systems workshop",
        "primary_metric": "cross-model gap compression",
        "blocker": "nonzero baseline model gap",
    }
    checks = [
        normalize_value(data.get("title", "")) == expected["title"].lower(),
        normalize_value(data.get("target_venue", "")) == expected["target_venue"].lower(),
        expected["fallback_venue"].lower() in normalize_value(data.get("fallback_venue", "")),
        expected["primary_metric"].lower() in normalize_value(data.get("primary_metric", "")),
        expected["blocker"].lower() in normalize_value(data.get("blocker", "")),
    ]
    evidence_ids = data.get("evidence_ids", [])
    if not isinstance(evidence_ids, list):
        evidence_ids = []
    expected_evidence = {"hard-e02", "hard-e03", "hard-e04"}
    citation_grounding = len(expected_evidence.intersection(set(map(str, evidence_ids)))) / len(
        expected_evidence
    )
    task_success = (sum(checks) / len(checks) + citation_grounding) / 2

    metrics = {
        "task_success": clamp(task_success),
        "schema_validity": clamp(schema_validity),
        "tool_call_correctness": 1.0,
        "citation_grounding": clamp(citation_grounding),
        "human_acceptance": clamp((task_success + schema_validity) / 2),
        "cost_efficiency": clamp(task_success),
        "safety_consistency": 1.0 if "llmlingua" not in json.dumps(data).lower() else 0.5,
    }
    findings = []
    if str(data.get("title", "")).strip().lower() == "topic-aware compaction":
        findings.append("Selected HOLD proposal instead of NEXT proposal.")
    if "llmlingua" in json.dumps(data).lower():
        findings.append("Included comparator content as routed proposal metadata.")

    report = {
        "status": "complete",
        "passed": metrics["task_success"] >= 0.8 and metrics["schema_validity"] >= 0.8,
        "reason": "Hard structured extraction evaluated against active-proposal routing expectations.",
        "findings": findings,
        "parsed_output": data,
    }
    return report, metrics


def has_section(text: str, section: str) -> bool:
    normalized = section.replace("_", " ").lower()
    raw = section.lower()
    hyphenated = section.replace("_", "-").lower()
    heading_pattern = re.compile(r"^#{1,4}\s+(.+)$", re.MULTILINE)
    headings = [match.group(1).strip().lower() for match in heading_pattern.finditer(text)]
    lower = text.lower()
    return (
        any(normalized in heading or raw in heading or hyphenated in heading for heading in headings)
        or normalized in lower
        or raw in lower
        or hyphenated in lower
    )


def trace_is_filled(path: Path) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8").strip().lower()
    return bool(text) and "pending" not in text


def evaluate_project_initialization(
    output: str, trace_path: Path
) -> tuple[dict[str, Any], dict[str, float]]:
    required_sections = ["created_files", "skipped_files", "risks", "next_steps"]
    section_score = sum(1 for section in required_sections if has_section(output, section)) / len(
        required_sections
    )
    lower = output.lower()
    mentions_agents = "agents.md" in lower
    mentions_no_overwrite = "no-overwrite" in lower or "no overwrite" in lower
    mentions_research = "research" in lower
    task_success = sum([mentions_agents, mentions_no_overwrite, mentions_research]) / 3
    tool_score = 1.0 if trace_is_filled(trace_path) else 0.0
    safety = 1.0 if mentions_no_overwrite and mentions_agents else 0.4

    metrics = {
        "task_success": clamp(task_success),
        "schema_validity": clamp(section_score),
        "tool_call_correctness": tool_score,
        "citation_grounding": 0.8 if mentions_agents else 0.4,
        "human_acceptance": clamp((task_success + section_score + safety) / 3),
        "cost_efficiency": clamp((task_success + section_score) / 2),
        "safety_consistency": safety,
    }
    report = {
        "status": "complete",
        "passed": metrics["task_success"] >= 0.8 and metrics["schema_validity"] >= 0.8,
        "reason": "Project initialization output evaluated against fixture expectations.",
        "findings": [],
    }
    if tool_score == 0.0:
        report["findings"].append("Tool trace is required for this fixture but is missing or pending.")
    return report, metrics


def evaluate_research_workflow(output: str, trace_path: Path) -> tuple[dict[str, Any], dict[str, float]]:
    required_sections = ["brief", "evidence_summary", "synthesis", "risks", "next_steps"]
    section_score = sum(1 for section in required_sections if has_section(output, section)) / len(
        required_sections
    )
    lower = output.lower()

    evidence_ids = ["fixture-rw-e01", "fixture-rw-e02", "fixture-rw-e03"]
    cited = sum(1 for evidence_id in evidence_ids if evidence_id in lower)
    citation_grounding = cited / len(evidence_ids)

    separates_types = (
        "extracted" in lower
        and "inferred" in lower
        and ("separate" in lower or "distinguish" in lower or "type" in lower)
    )
    recommends_separate = "remain separate" in lower or "keep separate" in lower
    avoids_external = not any(
        marker in lower
        for marker in [
            "according to external",
            "recent literature",
            "industry trend",
            "web search",
        ]
    )
    lists_risks = "risk" in lower and (
        "single-model" in lower or "ablation" in lower or "cross-model" in lower
    )
    task_success = sum(
        [citation_grounding >= 2 / 3, separates_types, recommends_separate, lists_risks]
    ) / 4
    tool_score = 1.0 if trace_is_filled(trace_path) else 0.0
    safety = 1.0 if avoids_external and citation_grounding >= 2 / 3 else 0.5 if avoids_external else 0.0

    metrics = {
        "task_success": clamp(task_success),
        "schema_validity": clamp(section_score),
        "tool_call_correctness": tool_score,
        "citation_grounding": clamp(citation_grounding),
        "human_acceptance": clamp((task_success + section_score + safety) / 3),
        "cost_efficiency": clamp((task_success + section_score) / 2),
        "safety_consistency": safety,
    }
    findings = []
    if citation_grounding < 2 / 3:
        findings.append("Evidence IDs are missing or incomplete.")
    if not separates_types:
        findings.append("Extracted evidence and inference are not clearly separated.")
    if not recommends_separate:
        findings.append("Expected recommendation to keep proposal tracks separate is missing.")
    if tool_score == 0.0:
        findings.append("Tool trace is required for this fixture but is missing or pending.")

    report = {
        "status": "complete",
        "passed": metrics["task_success"] >= 0.75 and metrics["schema_validity"] >= 0.8,
        "reason": "Research workflow output evaluated against evidence-backed synthesis expectations.",
        "findings": findings,
    }
    return report, metrics


def evaluate_run(run: dict[str, Any]) -> dict[str, Any]:
    output_path = Path(run["paths"]["output"])
    trace_path = Path(run["paths"]["tool_trace"])
    validation_path = Path(run["paths"]["validation_report"])
    metrics_path = Path(run["paths"]["metrics"])
    output = read_text(output_path)

    if "status: pending" in output.lower():
        report, metrics = pending_result("Output is still pending.")
    elif run["fixture"] == "structured-extraction":
        report, metrics = evaluate_structured_extraction(output)
    elif run["fixture"] == "structured-extraction-hard":
        report, metrics = evaluate_structured_extraction_hard(output)
    elif run["fixture"] == "project-initialization":
        report, metrics = evaluate_project_initialization(output, trace_path)
    elif run["fixture"] == "research-workflow":
        report, metrics = evaluate_research_workflow(output, trace_path)
    else:
        report, metrics = pending_result(f"No evaluator for fixture {run['fixture']}.")

    report.update(
        {
            "run_id": run["run_id"],
            "fixture": run["fixture"],
            "model": run["model"],
            "harness_arm": run["harness_arm"],
        }
    )
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

    validation_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    metrics_path.write_text(
        json.dumps(metric_payload, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    return metric_payload


def markdown_summary(results: list[dict[str, Any]]) -> str:
    lines = [
        "# Real Run Artifact Evaluation Summary",
        "",
        "| Run | Fixture | Model | Arm | Task Success | Schema | Grounding | Status |",
        "|---|---|---|---|---:|---:|---:|---|",
    ]
    for result in results:
        metrics = result["metrics"]
        run_id = result["run_id"]
        status = result.get("validation_status", "unknown")
        lines.append(
            f"| `{run_id}` | `{result['fixture']}` | `{result['model']}` | "
            f"`{result['harness_arm']}` | {metrics['task_success']:.3f} | "
            f"{metrics['schema_validity']:.3f} | {metrics['citation_grounding']:.3f} | {status} |"
        )
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--output-runs", required=True)
    parser.add_argument("--output-md", required=True)
    args = parser.parse_args()

    manifest = read_json(Path(args.manifest))
    results = [evaluate_run(run) for run in manifest["runs"]]
    payload = {"runs": results}
    Path(args.output_runs).write_text(
        json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    Path(args.output_md).write_text(markdown_summary(results), encoding="utf-8")


if __name__ == "__main__":
    main()
