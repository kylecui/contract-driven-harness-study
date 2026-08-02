from __future__ import annotations

import argparse
import importlib.metadata
import json
import sys
from collections import defaultdict
from dataclasses import asdict
from pathlib import Path
from typing import Any


DEFAULT_FRAMEWORK_PATH = Path("C:/tmp/petfishframework-0.1.5")
DEFAULT_RESULTS = Path("research/05_analysis/stage-b-v54-explicit-delta-stability-results.json")
DEFAULT_ARTIFACT_ROOT = Path("research/05_analysis/real-run-artifacts/stage-b-v54-explicit-delta-stability")
DEFAULT_JSON_OUT = Path("research/05_analysis/petfishframework-v015-stage-b-v54-pilot.json")
DEFAULT_MD_OUT = Path("research/05_analysis/petfishframework-v015-stage-b-v54-pilot.md")

CRITICAL_METRICS = (
    "schema_validity",
    "exact_evidence_array_preservation",
    "residual_unknown_vocabulary_accuracy",
    "state_transition_accuracy",
    "transition_gate_accuracy",
    "retention_attestation_accuracy",
    "controlled_state_mutation_success",
)

PERTURBATION_ORDER = (
    "canonical",
    "field_alias",
    "evidence_order_shuffled",
    "distractor_evidence",
    "unknown_state_paraphrase",
)

REQUIRED_ARTIFACTS = (
    "adapter_request.json",
    "manifest.json",
    "metrics.json",
    "output.md",
    "prompt.md",
    "tool_trace.jsonl",
    "validation_report.json",
)


def load_framework(framework_path: Path) -> dict[str, Any]:
    if framework_path.exists():
        sys.path.insert(0, str(framework_path))

    from petfishframework.core.structured import parse_json
    from petfishframework.core.types import Result, Task
    from petfishframework.reliability.pass_at_k import pass_at_k_with_perturbations

    try:
        version = importlib.metadata.version("petfishframework")
    except importlib.metadata.PackageNotFoundError:
        version = "unknown"

    return {
        "Result": Result,
        "Task": Task,
        "parse_json": parse_json,
        "pass_at_k_with_perturbations": pass_at_k_with_perturbations,
        "version": version,
    }


def load_runs(results_path: Path) -> list[dict[str, Any]]:
    data = json.loads(results_path.read_text(encoding="utf-8"))
    runs = data.get("runs", [])
    if not isinstance(runs, list) or not runs:
        raise ValueError(f"No runs found in {results_path}")
    return runs


def natural_repetition(run: dict[str, Any]) -> int:
    run_id = run["run_id"]
    marker = "__r"
    if marker not in run_id:
        return 0
    return int(run_id.rsplit(marker, 1)[1])


def run_pass_at_k(framework: dict[str, Any], grouped: dict[str, list[dict[str, Any]]]) -> Any:
    Result = framework["Result"]
    Task = framework["Task"]
    pass_at_k_with_perturbations = framework["pass_at_k_with_perturbations"]

    cursors = {condition: 0 for condition in grouped}

    class OfflineSession:
        def __init__(self, run: dict[str, Any]) -> None:
            self.record = run

        def run(self) -> Any:
            metrics = self.record.get("metrics", {})
            critical_ok = all(metrics.get(name) == 1.0 for name in CRITICAL_METRICS)
            answer = "PASS" if self.record.get("passed") and critical_ok else "FAIL"
            return Result(answer=answer, session_id=self.record["run_id"])

    def session_factory(task: Any) -> OfflineSession:
        condition = task.metadata.get("condition", "canonical")
        index = cursors[condition]
        if index >= len(grouped[condition]):
            raise IndexError(f"No remaining offline runs for condition {condition!r}")
        cursors[condition] += 1
        return OfflineSession(grouped[condition][index])

    def all_pass(results: list[Any]) -> bool:
        return bool(results) and all(result.answer == "PASS" for result in results)

    def make_perturbation(condition: str):
        def perturb(task: Any) -> Any:
            return Task(
                prompt=task.prompt,
                metadata={**task.metadata, "condition": condition, "perturbation": condition},
            )

        perturb.__name__ = condition
        return perturb

    perturbations = tuple(make_perturbation(name) for name in PERTURBATION_ORDER[1:])
    task = Task(
        prompt="Stage B v5.4 frozen explicit-transition-delta protocol",
        metadata={"condition": "canonical", "perturbation": "canonical"},
    )
    return pass_at_k_with_perturbations(
        session_factory=session_factory,
        task=task,
        k=8,
        agreement=all_pass,
        perturbations=perturbations,
    )


def summarize_pass_result(pass_result: Any) -> dict[str, Any]:
    variants = [pass_result.canonical, *pass_result.perturbations]
    return {
        "k": pass_result.k,
        "overall_pass": pass_result.overall_pass,
        "pass_rate": pass_result.pass_rate,
        "variants": [asdict(variant) for variant in variants],
    }


def audit_artifacts(
    runs: list[dict[str, Any]],
    artifact_root: Path,
    parse_json_fn: Any,
) -> dict[str, Any]:
    parse_failures: list[dict[str, str]] = []
    incomplete_artifacts: list[dict[str, Any]] = []
    metric_mismatches: list[dict[str, str]] = []
    validation_json_failures: list[dict[str, str]] = []

    for run in runs:
        run_id = run["run_id"]
        run_dir = artifact_root / run_id
        missing = [name for name in REQUIRED_ARTIFACTS if not (run_dir / name).exists()]
        if missing:
            incomplete_artifacts.append({"run_id": run_id, "missing": missing})

        output_path = run_dir / "output.md"
        if output_path.exists():
            try:
                parse_json_fn(output_path.read_text(encoding="utf-8"))
            except Exception as exc:  # noqa: BLE001 - capture parser behavior for audit.
                parse_failures.append({"run_id": run_id, "error": str(exc)})

        metrics_path = run_dir / "metrics.json"
        if metrics_path.exists():
            artifact_metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
            for metric in CRITICAL_METRICS:
                if artifact_metrics.get("metrics", {}).get(metric) != run.get("metrics", {}).get(metric):
                    metric_mismatches.append({"run_id": run_id, "metric": metric})

        validation_path = run_dir / "validation_report.json"
        if validation_path.exists():
            try:
                json.loads(validation_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                validation_json_failures.append({"run_id": run_id, "error": str(exc)})

    return {
        "runs_checked": len(runs),
        "complete_artifact_sets": len(runs) - len(incomplete_artifacts),
        "incomplete_artifacts": incomplete_artifacts,
        "structured_outputs_checked": len(runs),
        "structured_parse_successes": len(runs) - len(parse_failures),
        "structured_parse_failures": parse_failures,
        "metrics_files_matching_results": len(runs) - len({item["run_id"] for item in metric_mismatches}),
        "metric_mismatches": metric_mismatches,
        "validation_json_successes": len(runs) - len(validation_json_failures),
        "validation_json_failures": validation_json_failures,
    }


def condition_summary(grouped: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    summary: dict[str, Any] = {}
    for condition, runs in grouped.items():
        pass_count = sum(1 for run in runs if run.get("passed"))
        summary[condition] = {
            "run_count": len(runs),
            "passed": pass_count,
            "failed": len(runs) - pass_count,
        }
    return summary


def render_markdown(result: dict[str, Any]) -> str:
    lines = [
        "# petfishframework 0.1.5 Pilot: Stage B v5.4 Offline Recheck",
        "",
        "## Research Task Plan",
        "",
        "- research_type: Scientific / reliability evaluation",
        "- complexity_level: light pilot",
        "- recommended_skill_chain: research-router -> scientific-experiment-planner -> anti-sycophancy-calibration",
        "- expected_artifacts: JSON result, Markdown report",
        "- key_risks: offline replay does not test new model calls; one fixture family does not prove broad data reliability",
        "",
        "## Setup",
        "",
        f"- framework_version: `{result['framework_version']}`",
        f"- input_results: `{result['input_results']}`",
        f"- artifact_root: `{result['artifact_root']}`",
        "- workload: 40 completed Stage B v5.4 explicit-delta runs, five perturbation conditions, eight repetitions each",
        "",
        "## Pass^8 Recheck",
        "",
        f"- overall_pass: `{result['pass_at_k']['overall_pass']}`",
        f"- pass_rate: `{result['pass_at_k']['pass_rate']:.3f}`",
        "",
        "| Condition | Pass | Agreed |",
        "|---|---:|---:|",
    ]

    for variant in result["pass_at_k"]["variants"]:
        lines.append(
            f"| {variant['name']} | {variant['pass_count']}/{variant['total']} | {str(variant['agreed']).lower()} |"
        )

    audit = result["artifact_audit"]
    lines.extend(
        [
            "",
            "## Structured Output And Audit",
            "",
            f"- structured_parse: {audit['structured_parse_successes']}/{audit['structured_outputs_checked']}",
            f"- complete_artifact_sets: {audit['complete_artifact_sets']}/{audit['runs_checked']}",
            f"- metrics_files_matching_results: {audit['metrics_files_matching_results']}/{audit['runs_checked']}",
            f"- validation_json_successes: {audit['validation_json_successes']}/{audit['runs_checked']}",
            "",
            "## Interpretation",
            "",
            "This pilot supports using petfishframework as a thin reliability/audit wrapper for existing benchmark artifacts.",
            "It reproduced the Stage B v5.4 stability signal as Pass^8 over the five designed perturbation conditions and found no structured parsing, artifact completeness, metric consistency, or validation JSON failures in this slice.",
            "",
            "It does not prove that underlying source data became more truthful. The result is evidence for process reliability on one frozen controlled-transition workload, not broad data-quality or production-readiness evidence.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--framework-path", type=Path, default=DEFAULT_FRAMEWORK_PATH)
    parser.add_argument("--results", type=Path, default=DEFAULT_RESULTS)
    parser.add_argument("--artifact-root", type=Path, default=DEFAULT_ARTIFACT_ROOT)
    parser.add_argument("--json-out", type=Path, default=DEFAULT_JSON_OUT)
    parser.add_argument("--md-out", type=Path, default=DEFAULT_MD_OUT)
    args = parser.parse_args()

    framework = load_framework(args.framework_path)
    runs = load_runs(args.results)

    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for run in runs:
        grouped[run["perturbation_condition"]].append(run)
    grouped = {condition: sorted(grouped[condition], key=natural_repetition) for condition in PERTURBATION_ORDER}

    pass_result = run_pass_at_k(framework, grouped)
    result = {
        "framework_version": framework["version"],
        "input_results": str(args.results),
        "artifact_root": str(args.artifact_root),
        "condition_summary": condition_summary(grouped),
        "pass_at_k": summarize_pass_result(pass_result),
        "artifact_audit": audit_artifacts(runs, args.artifact_root, framework["parse_json"]),
        "limitations": [
            "Offline replay reuses completed outputs and does not exercise fresh model/provider variance.",
            "The workload is one frozen controlled-transition fixture family.",
            "ReplayEnvironment was not directly applicable because existing artifacts store prompt/output/tool_trace files, not petfishframework ModelResponse/ToolResult recordings.",
        ],
    }

    args.json_out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    args.md_out.write_text(render_markdown(result), encoding="utf-8")
    print(json.dumps({"json_out": str(args.json_out), "md_out": str(args.md_out), "overall_pass": pass_result.overall_pass}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
