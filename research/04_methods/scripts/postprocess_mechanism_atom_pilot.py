#!/usr/bin/env python3
"""Postprocess mechanism-atom pilot artifacts.

This is local-only. It evaluates mechanism atom outputs, collects completed
metrics, and computes gap, weak-model lift, and harnessed-weak-vs-strong-G0
summaries when enough completed runs exist.
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
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def run_step(args: list[str]) -> None:
    subprocess.run(args, check=True)


def metrics_ready(collected: dict[str, Any], baseline_arm: str) -> tuple[bool, str]:
    runs = collected.get("runs", [])
    if not runs:
        return False, "no completed mechanism-atom runs were collected"
    baseline_models = {
        str(run.get("model")) for run in runs if str(run.get("harness_arm")) == baseline_arm
    }
    if len(baseline_models) < 2:
        return False, f"baseline arm {baseline_arm} has fewer than two completed model groups"
    arms = {str(run.get("harness_arm")) for run in runs}
    if len(arms) < 2:
        return False, "fewer than two harness arms have completed runs"
    return True, "completed runs are sufficient for mechanism-atom metrics"


def write_summary(path: Path, report: dict[str, Any]) -> None:
    lines = [
        "# Mechanism Atom Pilot Postprocess Summary",
        "",
        "- Network/API calls made: no",
        f"- Manifest: `{report['manifest']}`",
        f"- Atoms dir: `{report['atoms_dir']}`",
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
    parser.add_argument("--atoms-dir", required=True)
    parser.add_argument("--output-prefix", required=True)
    parser.add_argument("--baseline-arm", default="G0")
    parser.add_argument("--strong-model", default="strong_model")
    parser.add_argument("--weak-model", default="budget_model")
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
        "summary_json": f"{prefix}-summary.json",
        "summary_md": f"{prefix}-summary.md",
    }

    run_step(
        [
            sys.executable,
            str(script_dir / "evaluate_mechanism_atom_artifacts.py"),
            "--manifest",
            args.manifest,
            "--atoms-dir",
            args.atoms_dir,
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
    ready, decision = metrics_ready(collected, args.baseline_arm)
    if ready:
        run_step(
            [
                sys.executable,
                str(script_dir / "harness_benchmark_metrics.py"),
                "--input",
                outputs["collected_runs_json"],
                "--baseline-arm",
                args.baseline_arm,
                "--strong-model",
                args.strong_model,
                "--weak-model",
                args.weak_model,
                "--output-json",
                outputs["metrics_json"],
                "--output-md",
                outputs["metrics_md"],
            ]
        )

    report = {
        "manifest": args.manifest,
        "atoms_dir": args.atoms_dir,
        "baseline_arm": args.baseline_arm,
        "strong_model": args.strong_model,
        "weak_model": args.weak_model,
        "completed_run_count": collected.get("run_count", 0),
        "warning_count": collected.get("warning_count", 0),
        "warnings": collected.get("warnings", []),
        "metrics_computed": ready,
        "decision": decision,
        "outputs": outputs,
    }
    dump_json(Path(outputs["summary_json"]), report)
    write_summary(Path(outputs["summary_md"]), report)
    print(
        "Mechanism atom postprocess complete: "
        f"completed_runs={report['completed_run_count']}; "
        f"metrics_computed={report['metrics_computed']}"
    )


if __name__ == "__main__":
    main()
