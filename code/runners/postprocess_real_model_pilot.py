#!/usr/bin/env python3
"""Postprocess real model-backed pilot artifacts.

This orchestrates local evaluation after provider outputs have been written:

1. Evaluate run artifacts into validation reports and per-run metrics.
2. Collect only completed run metrics.
3. Compute harness gap-compression metrics when enough completed data exists.

The script does not call model providers.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def dump_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def run_step(args: list[str]) -> None:
    subprocess.run(args, check=True)


def has_metric_ready_runs(collected: dict[str, Any], baseline_arm: str) -> tuple[bool, str]:
    runs = collected.get("runs", [])
    if not runs:
        return False, "no completed runs were collected"

    baseline_models = {
        str(run.get("model"))
        for run in runs
        if str(run.get("harness_arm")) == baseline_arm
    }
    if len(baseline_models) < 2:
        return False, f"baseline arm {baseline_arm} has fewer than two completed model groups"

    arms = {str(run.get("harness_arm")) for run in runs}
    if len(arms) < 2:
        return False, "fewer than two harness arms have completed runs"

    return True, "completed runs are sufficient for gap-compression metrics"


def write_summary(path: Path, report: dict[str, Any]) -> None:
    lines = [
        "# Real Model Pilot Postprocess Summary",
        "",
        "- Network/API calls made: no",
        f"- Manifest: `{report['manifest']}`",
        f"- Completed runs collected: {report['completed_run_count']}",
        f"- Collection warnings: {report['warning_count']}",
        f"- Metrics computed: {'yes' if report['metrics_computed'] else 'no'}",
        "",
        "## Outputs",
        "",
        f"- Evaluation JSON: `{report['outputs']['evaluated_runs_json']}`",
        f"- Evaluation Markdown: `{report['outputs']['evaluation_md']}`",
        f"- Collected runs JSON: `{report['outputs']['collected_runs_json']}`",
        f"- Collected runs Markdown: `{report['outputs']['collected_runs_md']}`",
    ]
    if report["metrics_computed"]:
        lines.extend(
            [
                f"- Metrics JSON: `{report['outputs']['metrics_json']}`",
                f"- Metrics Markdown: `{report['outputs']['metrics_md']}`",
            ]
        )
    lines.extend(["", "## Decision", "", report["decision"]])
    if report.get("warnings"):
        lines.extend(["", "## Warnings", ""])
        for warning in report["warnings"]:
            lines.append(f"- {warning}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--output-prefix", required=True)
    parser.add_argument("--baseline-arm", default="G0")
    args = parser.parse_args()

    script_dir = Path(__file__).resolve().parent
    prefix = Path(args.output_prefix)
    outputs = {
        "evaluated_runs_json": f"{prefix}-evaluated-runs.json",
        "evaluation_md": f"{prefix}-evaluation.md",
        "collected_runs_json": f"{prefix}-collected-runs.json",
        "collected_runs_md": f"{prefix}-collected-runs.md",
        "metrics_json": f"{prefix}-metrics.json",
        "metrics_md": f"{prefix}-metrics.md",
        "summary_md": f"{prefix}-summary.md",
    }

    run_step(
        [
            sys.executable,
            str(script_dir / "evaluate_real_run_artifacts.py"),
            "--manifest",
            args.manifest,
            "--output-runs",
            outputs["evaluated_runs_json"],
            "--output-md",
            outputs["evaluation_md"],
        ]
    )
    run_step(
        [
            sys.executable,
            str(script_dir / "collect_run_metrics.py"),
            "--manifest",
            args.manifest,
            "--output-json",
            outputs["collected_runs_json"],
            "--output-md",
            outputs["collected_runs_md"],
        ]
    )

    collected = load_json(Path(outputs["collected_runs_json"]))
    metrics_ready, decision = has_metric_ready_runs(collected, args.baseline_arm)
    if metrics_ready:
        run_step(
            [
                sys.executable,
                str(script_dir / "harness_benchmark_metrics.py"),
                "--input",
                outputs["collected_runs_json"],
                "--baseline-arm",
                args.baseline_arm,
                "--output-json",
                outputs["metrics_json"],
                "--output-md",
                outputs["metrics_md"],
            ]
        )

    report = {
        "manifest": args.manifest,
        "baseline_arm": args.baseline_arm,
        "completed_run_count": collected.get("run_count", 0),
        "warning_count": collected.get("warning_count", 0),
        "warnings": collected.get("warnings", []),
        "metrics_computed": metrics_ready,
        "decision": decision,
        "outputs": outputs,
    }
    dump_json(Path(f"{prefix}-summary.json"), report)
    write_summary(Path(outputs["summary_md"]), report)
    print(
        "Postprocess complete: "
        f"completed_runs={report['completed_run_count']}; "
        f"metrics_computed={report['metrics_computed']}"
    )


if __name__ == "__main__":
    main()
