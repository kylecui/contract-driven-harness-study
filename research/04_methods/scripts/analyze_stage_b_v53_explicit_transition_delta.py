#!/usr/bin/env python3
"""Analyze the preregistered Stage B v5.3 30-run ablation."""

from __future__ import annotations

import argparse
import math
import re
from collections import defaultdict
from pathlib import Path
from typing import Any

from analyze_stage_b_v52_evidence_binding_ablation import (
    dump_json,
    fisher_two_sided,
    load_json,
    summarize_group,
)


def exact_mcnemar_two_sided(
    treatment_pass_control_fail: int,
    treatment_fail_control_pass: int,
) -> float:
    """Return the exact two-sided McNemar p-value for discordant pairs."""
    discordant = (
        treatment_pass_control_fail + treatment_fail_control_pass
    )
    if discordant == 0:
        return 1.0
    tail = min(
        treatment_pass_control_fail,
        treatment_fail_control_pass,
    )
    probability = sum(
        math.comb(discordant, value)
        for value in range(tail + 1)
    ) / (2**discordant)
    return min(1.0, 2 * probability)


def pair_key(run: dict[str, Any]) -> tuple[str, int]:
    condition = run["perturbation_condition"]
    if "repetition" in run:
        return condition, int(run["repetition"])
    match = re.search(r"__r(\d+)$", run.get("run_id", ""))
    if not match:
        raise ValueError(
            "Paired Stage B v5.3 runs require a repetition field or "
            f"an __rN run_id suffix: {run.get('run_id', '<missing>')}"
        )
    return condition, int(match.group(1))


def summarize_pairs(
    runs: list[dict[str, Any]],
    metric: str,
) -> dict[str, Any]:
    pairs: dict[tuple[str, int], dict[str, dict[str, Any]]] = defaultdict(dict)
    for run in runs:
        key = pair_key(run)
        arm = run["protocol_arm"]
        if arm in pairs[key]:
            raise ValueError(f"Duplicate {arm} run for pair {key}")
        pairs[key][arm] = run

    expected_arms = {"postcondition_only", "explicit_delta"}
    incomplete = {
        key: sorted(expected_arms - set(arms))
        for key, arms in pairs.items()
        if set(arms) != expected_arms
    }
    if incomplete or len(pairs) != 15:
        raise ValueError(
            "Stage B v5.3 requires 15 complete matched pairs; "
            f"found {len(pairs)} pairs with incomplete={incomplete}"
        )

    counts = {
        "treatment_pass_control_pass": 0,
        "treatment_pass_control_fail": 0,
        "treatment_fail_control_pass": 0,
        "treatment_fail_control_fail": 0,
    }
    pair_results = []
    for (condition, repetition), arms in sorted(pairs.items()):
        treatment_pass = (
            arms["explicit_delta"]["metrics"][metric] == 1.0
        )
        control_pass = (
            arms["postcondition_only"]["metrics"][metric] == 1.0
        )
        if treatment_pass and control_pass:
            bucket = "treatment_pass_control_pass"
        elif treatment_pass:
            bucket = "treatment_pass_control_fail"
        elif control_pass:
            bucket = "treatment_fail_control_pass"
        else:
            bucket = "treatment_fail_control_fail"
        counts[bucket] += 1
        pair_results.append(
            {
                "condition": condition,
                "repetition": repetition,
                "treatment_pass": treatment_pass,
                "control_pass": control_pass,
                "classification": bucket,
            }
        )

    counts["discordant_pairs"] = (
        counts["treatment_pass_control_fail"]
        + counts["treatment_fail_control_pass"]
    )
    counts["exact_mcnemar_two_sided_p"] = round(
        exact_mcnemar_two_sided(
            counts["treatment_pass_control_fail"],
            counts["treatment_fail_control_pass"],
        ),
        8,
    )
    counts["pairs"] = pair_results
    return counts


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
    paired = summarize_pairs(
        runs,
        "residual_unknown_vocabulary_accuracy",
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

    if h1 and h2 and paired["exact_mcnemar_two_sided_p"] < 0.05:
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
            "matched_pairs": paired,
            "exact_mcnemar_two_sided_p": paired[
                "exact_mcnemar_two_sided_p"
            ],
            "legacy_independent_groups_fisher_two_sided_p": round(
                fisher_p, 8
            ),
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
            "- Exact McNemar two-sided p: "
            f"{comparison['exact_mcnemar_two_sided_p']:.3f}"
        ),
        (
            "- Discordant pairs (treatment pass/control fail vs "
            "treatment fail/control pass): "
            f"{comparison['matched_pairs']['treatment_pass_control_fail']} "
            "vs "
            f"{comparison['matched_pairs']['treatment_fail_control_pass']}"
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
    lines.extend(
        [
            "",
            "## Matched-Pair Results",
            "",
            "| Condition | Repetition | Treatment | Control | Classification |",
            "|---|---:|---|---|---|",
        ]
    )
    for pair in comparison["matched_pairs"]["pairs"]:
        lines.append(
            f"| `{pair['condition']}` | {pair['repetition']} | "
            f"{'pass' if pair['treatment_pass'] else 'fail'} | "
            f"{'pass' if pair['control_pass'] else 'fail'} | "
            f"`{pair['classification']}` |"
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
