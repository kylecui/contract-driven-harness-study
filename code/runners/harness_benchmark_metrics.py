#!/usr/bin/env python3
"""Minimal metric helpers for contract-driven harness benchmark results."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from statistics import mean
from typing import Any


METRICS = [
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


def load_runs(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict) and "runs" in data:
        return list(data["runs"])
    if isinstance(data, list):
        return data
    raise ValueError("Input must be a list of runs or an object with a 'runs' key")


def gap(values_by_model: dict[str, list[float]]) -> float:
    model_means = [mean(values) for values in values_by_model.values() if values]
    if len(model_means) < 2:
        return 0.0
    return max(model_means) - min(model_means)


def group_runs(runs: list[dict[str, Any]]) -> dict[str, dict[str, dict[str, list[float]]]]:
    grouped: dict[str, dict[str, dict[str, list[float]]]] = {}
    for run in runs:
        arm = str(run["harness_arm"])
        model = str(run["model"])
        metrics = run.get("metrics", {})
        grouped.setdefault(arm, {})
        grouped[arm].setdefault(model, {})
        for metric in METRICS:
            if metric in metrics:
                grouped[arm][model].setdefault(metric, []).append(float(metrics[metric]))
    return grouped


def model_metric_mean(
    grouped: dict[str, dict[str, dict[str, list[float]]]],
    *,
    arm: str,
    model: str,
    metric: str,
) -> float | None:
    values = grouped.get(arm, {}).get(model, {}).get(metric, [])
    if not values:
        return None
    return mean(values)


def compute_summary(
    runs: list[dict[str, Any]],
    baseline_arm: str,
    strong_model: str,
    weak_model: str,
) -> dict[str, Any]:
    grouped = group_runs(runs)
    if baseline_arm not in grouped:
        raise ValueError(f"Baseline arm not found: {baseline_arm}")

    summary: dict[str, Any] = {
        "baseline_arm": baseline_arm,
        "strong_model": strong_model,
        "weak_model": weak_model,
        "arms": {},
    }
    baseline = grouped[baseline_arm]

    for arm, by_model in sorted(grouped.items()):
        arm_summary: dict[str, Any] = {"metrics": {}}
        for metric in METRICS:
            baseline_values = {
                model: values.get(metric, [])
                for model, values in baseline.items()
                if values.get(metric)
            }
            arm_values = {
                model: values.get(metric, [])
                for model, values in by_model.items()
                if values.get(metric)
            }
            baseline_gap = gap(baseline_values)
            arm_gap = gap(arm_values)
            if baseline_gap == 0:
                compression_ratio = None
            else:
                compression_ratio = 1 - (arm_gap / baseline_gap)
            weak_baseline = model_metric_mean(
                grouped,
                arm=baseline_arm,
                model=weak_model,
                metric=metric,
            )
            weak_arm = model_metric_mean(grouped, arm=arm, model=weak_model, metric=metric)
            strong_baseline = model_metric_mean(
                grouped,
                arm=baseline_arm,
                model=strong_model,
                metric=metric,
            )
            weak_model_enablement_lift = (
                None if weak_baseline is None or weak_arm is None else weak_arm - weak_baseline
            )
            harnessed_weak_vs_strong_baseline = (
                None if weak_arm is None or strong_baseline is None else weak_arm - strong_baseline
            )
            arm_summary["metrics"][metric] = {
                "baseline_gap": baseline_gap,
                "arm_gap": arm_gap,
                "compression_ratio": compression_ratio,
                "weak_model_enablement_lift": weak_model_enablement_lift,
                "harnessed_weak_vs_strong_baseline": harnessed_weak_vs_strong_baseline,
            }
        summary["arms"][arm] = arm_summary
    return summary


def markdown(summary: dict[str, Any]) -> str:
    lines = [
        "# Harness Benchmark Metric Summary",
        "",
        f"Baseline arm: `{summary['baseline_arm']}`",
        f"Strong model: `{summary['strong_model']}`",
        f"Weak model: `{summary['weak_model']}`",
        "",
        "| Arm | Metric | Baseline Gap | Arm Gap | Compression Ratio | Weak Lift | Weak vs Strong G0 |",
        "|---|---|---:|---:|---:|---:|---:|",
    ]
    for arm, arm_summary in summary["arms"].items():
        for metric, data in arm_summary["metrics"].items():
            ratio = data["compression_ratio"]
            ratio_text = "n/a" if ratio is None else f"{ratio:.3f}"
            weak_lift = data["weak_model_enablement_lift"]
            weak_lift_text = "n/a" if weak_lift is None else f"{weak_lift:.3f}"
            weak_vs_strong = data["harnessed_weak_vs_strong_baseline"]
            weak_vs_strong_text = "n/a" if weak_vs_strong is None else f"{weak_vs_strong:.3f}"
            lines.append(
                f"| `{arm}` | `{metric}` | {data['baseline_gap']:.3f} | "
                f"{data['arm_gap']:.3f} | {ratio_text} | {weak_lift_text} | {weak_vs_strong_text} |"
            )
    lines.extend(
        [
            "",
            "Compression ratio is `1 - arm_gap / baseline_gap`. Positive values mean the harness arm reduced cross-model gap for that metric.",
            "Weak lift is `weak_model_arm - weak_model_G0`.",
            "Weak vs Strong G0 is `weak_model_arm - strong_model_G0`.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="JSON run list or object with runs[]")
    parser.add_argument("--baseline-arm", default="G0")
    parser.add_argument("--strong-model", default="strong_model")
    parser.add_argument("--weak-model", default="budget_model")
    parser.add_argument("--output-json", required=True)
    parser.add_argument("--output-md", required=True)
    args = parser.parse_args()

    runs = load_runs(Path(args.input))
    summary = compute_summary(runs, args.baseline_arm, args.strong_model, args.weak_model)
    Path(args.output_json).write_text(
        json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    Path(args.output_md).write_text(markdown(summary), encoding="utf-8")


if __name__ == "__main__":
    main()
