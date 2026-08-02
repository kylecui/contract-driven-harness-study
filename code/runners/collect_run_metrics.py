#!/usr/bin/env python3
"""Collect per-run metrics artifacts into a benchmark runs JSON file."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def collect(manifest: dict[str, Any]) -> tuple[list[dict[str, Any]], list[str]]:
    runs: list[dict[str, Any]] = []
    warnings: list[str] = []

    for run in manifest["runs"]:
        metrics_path = Path(run["paths"]["metrics"])
        validation_path = Path(run["paths"]["validation_report"])
        if not metrics_path.exists():
            warnings.append(f"{run['run_id']}: metrics file missing")
            continue
        if not validation_path.exists():
            warnings.append(f"{run['run_id']}: validation report missing")
            continue

        payload = load_json(metrics_path)
        validation = load_json(validation_path)
        if validation.get("status") != "complete":
            warnings.append(
                f"{run['run_id']}: validation status is {validation.get('status', 'unknown')}"
            )
            continue
        if payload.get("status") == "pending":
            warnings.append(f"{run['run_id']}: metrics still pending")
            continue
        if "metrics" not in payload:
            warnings.append(f"{run['run_id']}: metrics payload missing metrics object")
            continue

        runs.append(payload)

    return runs, warnings


def markdown_report(runs: list[dict[str, Any]], warnings: list[str]) -> str:
    lines = [
        "# Collected Run Metrics",
        "",
        f"- Completed metric payloads: {len(runs)}",
        f"- Warnings: {len(warnings)}",
        "",
    ]

    if runs:
        lines.extend(
            [
                "## Runs",
                "",
                "| Run | Fixture | Model | Arm | Task Success | Schema | Grounding |",
                "|---|---|---|---|---:|---:|---:|",
            ]
        )
        for run in runs:
            metrics = run["metrics"]
            lines.append(
                f"| `{run['run_id']}` | `{run['fixture']}` | `{run['model']}` | "
                f"`{run['harness_arm']}` | {metrics['task_success']:.3f} | "
                f"{metrics['schema_validity']:.3f} | {metrics['citation_grounding']:.3f} |"
            )

    lines.extend(["", "## Warnings", ""])
    if warnings:
        for warning in warnings:
            lines.append(f"- {warning}")
    else:
        lines.append("- None")

    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--output-json", required=True)
    parser.add_argument("--output-md", required=True)
    args = parser.parse_args()

    manifest = load_json(Path(args.manifest))
    runs, warnings = collect(manifest)
    payload = {
        "note": "Collected evaluated run metrics.",
        "run_count": len(runs),
        "warning_count": len(warnings),
        "warnings": warnings,
        "runs": runs,
    }
    Path(args.output_json).write_text(
        json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    Path(args.output_md).write_text(markdown_report(runs, warnings), encoding="utf-8")
    print(f"Collected {len(runs)} completed runs; warnings={len(warnings)}")


if __name__ == "__main__":
    main()
