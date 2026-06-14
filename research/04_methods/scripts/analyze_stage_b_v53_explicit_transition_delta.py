#!/usr/bin/env python3
"""Analyze the preregistered Stage B v5.3 30-run ablation."""

from __future__ import annotations

import argparse
from collections import defaultdict
from pathlib import Path
from typing import Any

from analyze_stage_b_v52_evidence_binding_ablation import (
    dump_json,
    fisher_two_sided,
    load_json,
    summarize_group,
)


def analyze(evaluated: dict[str, Any], execution: dict[str, Any]) -> dict[str, Any]:
    runs = evaluated["runs"]
    by_arm: dict[str, list[dict[str, Any]]] = defaultdict(list)
    by_cell: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for run in runs:
        arm = run["protocol_arm"]
        condition = run["perturbation_condition"]
        by_arm[arm].append(run)
        by_cell[(arm, condition)].append(run)

    arm_summary = {
        arm: summarize_group(group) for arm, group in sorted(by_arm.items())
    }
    cell_summary = {}
    for (arm, condition), group in sorted(by_cell.items()):
        summary = summarize_group(group)
        strict = summary["components"]["controlled_state_mutation_success"]
        summary["cell_pass"] = strict["successes"] >= 2
        cell_summary[f"{arm}::{condition}"] = summary

    delta = arm_summary["explicit_delta"]["components"]
    baseline = arm_summary["postcondition_only"]["components"]
    delta_state = delta["residual_unknown_vocabulary_accuracy"]["successes"]
    baseline_state = baseline["residual_unknown_vocabulary_accuracy"]["successes"]
    delta_total = delta["residual_unknown_vocabulary_accuracy"]["total"]
    baseline_total = baseline["residual_unknown_vocabulary_accuracy"]["total"]
    risk_difference = (
        delta_state / delta_total - baseline_state / baseline_total
    )
    fisher_p = fisher_two_sided(
        delta_state,
        delta_total - delta_state,
        baseline_state,
        baseline_total - baseline_state,
    )

    delta_cells = [
        summary
        for key, summary in cell_summary.items()
        if key.startswith("explicit_delta::")
    ]
    h1 = (
        delta_state >= 14
        and delta["controlled_state_mutation_success"]["successes"] >= 13
        and all(cell["cell_pass"] for cell in delta_cells)
    )
    h2 = risk_difference >= 0.20
    h3 = all(
        delta[component]["successes"] >= 14
        for component in [
            "exact_evidence_array_preservation",
            "state_transition_accuracy",
            "transition_gate_accuracy",
            "retention_attestation_accuracy",
        ]
    )
    h4 = all(
        arm_summary[arm]["components"]["schema_validity"]["successes"] >= 14
        for arm in ["postcondition_only", "explicit_delta"]
    )

    if h1 and h2 and fisher_p < 0.05:
        decision = "delta_effect_with_strong_statistical_support"
    elif h1 and h2:
        decision = "delta_effect_supported"
    elif h1 != h2:
        decision = "mixed_result"
    elif abs(risk_difference) < 0.20:
        decision = "no_engineering_scale_delta_effect_observed"
    else:
        decision = "mixed_result"

    execution_results = execution["results"]
    usage = {
        "completed_calls": sum(
            item["status"] == "executed" for item in execution_results
        ),
        "provider_errors": sum(
            item["error"] is not None for item in execution_results
        ),
        "retries": sum(
            item["retry_lineage"]["attempt"] > 1
            for item in execution_results
        ),
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
        "reasoning_tokens": sum(
            item["provider_metadata"]["usage"]["raw"]
            .get("completion_tokens_details", {})
            .get("reasoning_tokens", 0)
            for item in execution_results
            if item.get("provider_metadata")
        ),
        "latency_ms": [
            item["elapsed_ms"] for item in execution_results
        ],
    }
    return {
        "protocol": "stage_b_v53_explicit_transition_delta",
        "run_count": len(runs),
        "arm_summary": arm_summary,
        "cell_summary": cell_summary,
        "primary_comparison": {
            "metric": "residual_unknown_vocabulary_accuracy",
            "explicit_delta_successes": delta_state,
            "explicit_delta_total": delta_total,
            "postcondition_only_successes": baseline_state,
            "postcondition_only_total": baseline_total,
            "risk_difference": round(risk_difference, 6),
            "engineering_effect_threshold": 0.20,
            "fisher_exact_two_sided_p": round(fisher_p, 8),
        },
        "hypotheses": {
            "H1_delta_robustness": h1,
            "H2_delta_effect": h2,
            "H3_obligation_preservation": h3,
            "H4_no_regression": h4,
        },
        "decision": decision,
        "execution_integrity": usage,
    }


def render_markdown(payload: dict[str, Any]) -> str:
    comparison = payload["primary_comparison"]
    lines = [
        "# Stage B v5.3 Explicit Transition-Delta Analysis",
        "",
        f"- Runs: {payload['run_count']}",
        f"- Decision: `{payload['decision']}`",
        f"- Residual-state risk difference: {comparison['risk_difference']:.3f}",
        (
            "- Fisher exact two-sided p: "
            f"{comparison['fisher_exact_two_sided_p']:.8f}"
        ),
        "",
        "## Arm Results",
        "",
        "| Arm | Strict pass | State pass | Evidence pass | Gate pass |",
        "|---|---:|---:|---:|---:|",
    ]
    for arm, summary in payload["arm_summary"].items():
        components = summary["components"]
        lines.append(
            f"| `{arm}` | "
            f"{components['controlled_state_mutation_success']['successes']}/15 | "
            f"{components['residual_unknown_vocabulary_accuracy']['successes']}/15 | "
            f"{components['exact_evidence_array_preservation']['successes']}/15 | "
            f"{components['transition_gate_accuracy']['successes']}/15 |"
        )
    lines.extend(
        [
            "",
            "## Cell Results",
            "",
            "| Arm | Condition | Strict pass | State pass | Cell decision |",
            "|---|---|---:|---:|---|",
        ]
    )
    for key, summary in payload["cell_summary"].items():
        arm, condition = key.split("::", 1)
        components = summary["components"]
        lines.append(
            f"| `{arm}` | `{condition}` | "
            f"{components['controlled_state_mutation_success']['successes']}/3 | "
            f"{components['residual_unknown_vocabulary_accuracy']['successes']}/3 | "
            f"{'pass' if summary['cell_pass'] else 'fail'} |"
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
