#!/usr/bin/env python3
"""Analyze the preregistered Stage B v5.4 stability confirmation."""

from __future__ import annotations

import argparse
import math
from collections import defaultdict
from pathlib import Path
from typing import Any

from analyze_stage_b_v52_evidence_binding_ablation import (
    dump_json,
    load_json,
    summarize_group,
)


CRITICAL_COMPONENTS = [
    "exact_evidence_array_preservation",
    "residual_unknown_vocabulary_accuracy",
    "state_transition_accuracy",
    "transition_gate_accuracy",
]


def percentile(values: list[int], proportion: float) -> float:
    ordered = sorted(values)
    if not ordered:
        return 0.0
    position = (len(ordered) - 1) * proportion
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return float(ordered[lower])
    weight = position - lower
    return ordered[lower] * (1 - weight) + ordered[upper] * weight


def analyze(evaluated: dict[str, Any], execution: dict[str, Any]) -> dict[str, Any]:
    runs = evaluated["runs"]
    overall = summarize_group(runs)
    by_condition: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for run in runs:
        by_condition[run["perturbation_condition"]].append(run)
    condition_summary = {
        condition: summarize_group(group)
        for condition, group in sorted(by_condition.items())
    }
    matrix_shape_valid = (
        len(runs) == 40
        and len(condition_summary) == 5
        and all(summary["run_count"] == 8 for summary in condition_summary.values())
    )

    strict = overall["components"]["controlled_state_mutation_success"]
    h1 = (
        matrix_shape_valid
        and strict["successes"] >= 38
        and all(
            summary["components"]["controlled_state_mutation_success"][
                "successes"
            ]
            >= 7
            for summary in condition_summary.values()
        )
    )
    h2 = all(
        overall["components"][component]["successes"] >= 39
        for component in CRITICAL_COMPONENTS
    ) and matrix_shape_valid

    execution_results = execution["results"]
    completed = sum(
        item["status"] == "executed" for item in execution_results
    )
    provider_errors = sum(
        item["error"] is not None for item in execution_results
    )
    retries = sum(
        item.get("retry_lineage", {}).get("attempt", 1) > 1
        for item in execution_results
    )
    semantic_retries = sum(
        item.get("retry_lineage", {}).get("attempt", 1) > 1
        and item["error"] is None
        for item in execution_results
    )
    h3 = (
        len(execution_results) == 40
        and completed == 40
        and provider_errors <= 4
        and semantic_retries == 0
    )

    if h1 and h2 and h3:
        decision = "bounded_stability_confirmed"
    elif h1:
        decision = "mixed_stability"
    else:
        decision = "stability_not_confirmed"

    latencies = [item["elapsed_ms"] for item in execution_results]
    usage = {
        "completed_calls": completed,
        "provider_errors": provider_errors,
        "retries": retries,
        "semantic_retries": semantic_retries,
        "matrix_shape_valid": matrix_shape_valid,
        "prompt_tokens": sum(
            item["provider_metadata"]["usage"]["prompt_tokens"]
            for item in execution_results
            if item.get("provider_metadata")
        ),
        "completion_tokens": sum(
            item["provider_metadata"]["usage"]["completion_tokens"]
            for item in execution_results
            if item.get("provider_metadata")
        ),
        "total_tokens": sum(
            item["provider_metadata"]["usage"]["total_tokens"]
            for item in execution_results
            if item.get("provider_metadata")
        ),
        "latency_min_ms": min(latencies) if latencies else 0,
        "latency_median_ms": percentile(latencies, 0.5),
        "latency_p90_ms": percentile(latencies, 0.9),
        "latency_max_ms": max(latencies) if latencies else 0,
    }
    return {
        "protocol": "stage_b_v54_explicit_delta_stability",
        "run_count": len(runs),
        "overall": overall,
        "condition_summary": condition_summary,
        "hypotheses": {
            "H1_absolute_stability": h1,
            "H2_critical_components": h2,
            "H3_execution_integrity": h3,
        },
        "decision": decision,
        "execution_integrity": usage,
    }


def render_markdown(payload: dict[str, Any]) -> str:
    components = payload["overall"]["components"]
    lines = [
        "# Stage B v5.4 Explicit-Delta Stability Analysis",
        "",
        f"- Runs: {payload['run_count']}",
        f"- Decision: `{payload['decision']}`",
        "",
        "## Overall",
        "",
        "| Metric | Pass | Rate | Wilson 95% |",
        "|---|---:|---:|---|",
    ]
    for component in [
        "controlled_state_mutation_success",
        *CRITICAL_COMPONENTS,
        "schema_validity",
        "retention_attestation_accuracy",
    ]:
        item = components[component]
        lines.append(
            f"| `{component}` | {item['successes']}/{item['total']} | "
            f"{item['rate']:.3f} | "
            f"[{item['wilson_95'][0]:.3f}, {item['wilson_95'][1]:.3f}] |"
        )
    lines.extend(
        [
            "",
            "## Conditions",
            "",
            "| Condition | Strict pass | State pass |",
            "|---|---:|---:|",
        ]
    )
    for condition, summary in payload["condition_summary"].items():
        items = summary["components"]
        lines.append(
            f"| `{condition}` | "
            f"{items['controlled_state_mutation_success']['successes']}/8 | "
            f"{items['residual_unknown_vocabulary_accuracy']['successes']}/8 |"
        )
    lines.extend(["", "## Hypotheses", ""])
    for name, passed in payload["hypotheses"].items():
        lines.append(f"- `{name}`: {str(passed).lower()}")
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--evaluated-runs", required=True)
    parser.add_argument("--execution", required=True)
    parser.add_argument("--output-json", required=True)
    parser.add_argument("--output-md", required=True)
    args = parser.parse_args()
    payload = analyze(
        load_json(Path(args.evaluated_runs)),
        load_json(Path(args.execution)),
    )
    dump_json(Path(args.output_json), payload)
    Path(args.output_md).write_text(
        render_markdown(payload), encoding="utf-8"
    )
    print(f"Analyzed {payload['run_count']} runs: {payload['decision']}")


if __name__ == "__main__":
    main()
