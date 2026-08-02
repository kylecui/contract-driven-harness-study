#!/usr/bin/env python3
"""Analyze the preregistered Stage B v5.2 30-run ablation."""

from __future__ import annotations

import argparse
import json
import math
from collections import defaultdict
from pathlib import Path
from typing import Any


COMPONENTS = [
    "schema_validity",
    "exact_evidence_array_preservation",
    "residual_unknown_vocabulary_accuracy",
    "state_transition_accuracy",
    "transition_gate_accuracy",
    "retention_attestation_accuracy",
    "controlled_state_mutation_success",
]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def dump_json(path: Path, payload: Any) -> None:
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def wilson(successes: int, total: int, z: float = 1.96) -> list[float]:
    if total == 0:
        return [0.0, 0.0]
    rate = successes / total
    denominator = 1 + z * z / total
    center = (rate + z * z / (2 * total)) / denominator
    margin = (
        z
        * math.sqrt(
            rate * (1 - rate) / total + z * z / (4 * total * total)
        )
        / denominator
    )
    return [round(max(0.0, center - margin), 6), round(min(1.0, center + margin), 6)]


def hypergeom_probability(
    first_successes: int,
    first_total: int,
    total_successes: int,
    grand_total: int,
) -> float:
    return (
        math.comb(total_successes, first_successes)
        * math.comb(
            grand_total - total_successes,
            first_total - first_successes,
        )
        / math.comb(grand_total, first_total)
    )


def fisher_two_sided(a: int, b: int, c: int, d: int) -> float:
    first_total = a + b
    total_successes = a + c
    grand_total = a + b + c + d
    minimum = max(0, first_total - (grand_total - total_successes))
    maximum = min(first_total, total_successes)
    observed = hypergeom_probability(
        a, first_total, total_successes, grand_total
    )
    p_value = 0.0
    for candidate in range(minimum, maximum + 1):
        probability = hypergeom_probability(
            candidate, first_total, total_successes, grand_total
        )
        if probability <= observed + 1e-12:
            p_value += probability
    return min(1.0, p_value)


def summarize_group(runs: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(runs)
    components = {}
    for component in COMPONENTS:
        successes = sum(run["metrics"][component] == 1.0 for run in runs)
        components[component] = {
            "successes": successes,
            "total": total,
            "rate": round(successes / total, 6) if total else 0.0,
            "wilson_95": wilson(successes, total),
        }
    return {"run_count": total, "components": components}


def analyze(evaluated: dict[str, Any], execution: dict[str, Any]) -> dict[str, Any]:
    runs = evaluated["runs"]
    by_arm: dict[str, list[dict[str, Any]]] = defaultdict(list)
    by_cell: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for run in runs:
        arm = run["representation_arm"]
        condition = run["perturbation_condition"]
        by_arm[arm].append(run)
        by_cell[(arm, condition)].append(run)

    arm_summary = {
        arm: summarize_group(group) for arm, group in sorted(by_arm.items())
    }
    cell_summary = {}
    for (arm, condition), group in sorted(by_cell.items()):
        summary = summarize_group(group)
        aggregate = summary["components"]["controlled_state_mutation_success"]
        summary["cell_pass"] = aggregate["successes"] >= 2
        cell_summary[f"{arm}::{condition}"] = summary

    separated = arm_summary["binding_separated"]["components"]
    coupled = arm_summary["claim_coupled"]["components"]
    sep_evidence = separated["exact_evidence_array_preservation"]["successes"]
    coupled_evidence = coupled["exact_evidence_array_preservation"]["successes"]
    sep_total = separated["exact_evidence_array_preservation"]["total"]
    coupled_total = coupled["exact_evidence_array_preservation"]["total"]
    risk_difference = sep_evidence / sep_total - coupled_evidence / coupled_total
    fisher_p = fisher_two_sided(
        sep_evidence,
        sep_total - sep_evidence,
        coupled_evidence,
        coupled_total - coupled_evidence,
    )

    separated_cells = [
        summary
        for key, summary in cell_summary.items()
        if key.startswith("binding_separated::")
    ]
    h1 = (
        separated["controlled_state_mutation_success"]["successes"] >= 13
        and all(cell["cell_pass"] for cell in separated_cells)
    )
    h2 = risk_difference >= 0.20
    h3 = all(
        arm_summary[arm]["components"]["transition_gate_accuracy"]["successes"]
        >= 14
        for arm in ["claim_coupled", "binding_separated"]
    )
    h4 = all(
        arm_summary[arm]["components"]["state_transition_accuracy"]["successes"]
        >= 14
        for arm in ["claim_coupled", "binding_separated"]
    )
    h5 = all(cell["cell_pass"] for cell in separated_cells)

    if h1 and h2 and fisher_p < 0.05:
        decision = "directional_effect_with_strong_statistical_support"
    elif h1 and h2:
        decision = "directional_effect_supported"
    elif abs(risk_difference) < 0.20:
        decision = "no_engineering_scale_representation_effect_observed"
    else:
        decision = "mixed_result"

    execution_results = execution["results"]
    usage = {
        "completed_calls": sum(
            item["status"] == "executed" for item in execution_results
        ),
        "provider_errors": sum(item["error"] is not None for item in execution_results),
        "retries": sum(
            item["retry_lineage"]["attempt"] > 1 for item in execution_results
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
        "protocol": "stage_b_v52_evidence_binding_ablation",
        "run_count": len(runs),
        "arm_summary": arm_summary,
        "cell_summary": cell_summary,
        "primary_comparison": {
            "metric": "exact_evidence_array_preservation",
            "binding_separated_successes": sep_evidence,
            "binding_separated_total": sep_total,
            "claim_coupled_successes": coupled_evidence,
            "claim_coupled_total": coupled_total,
            "risk_difference": round(risk_difference, 6),
            "engineering_effect_threshold": 0.20,
            "fisher_exact_two_sided_p": round(fisher_p, 8),
        },
        "hypotheses": {
            "H1_separated_robustness": h1,
            "H2_representation_effect": h2,
            "H3_gate_control": h3,
            "H4_transition_control": h4,
            "H5_surface_transfer": h5,
        },
        "decision": decision,
        "execution_integrity": usage,
    }


def render_markdown(payload: dict[str, Any]) -> str:
    comparison = payload["primary_comparison"]
    lines = [
        "# Stage B v5.2 Evidence-Binding Ablation Analysis",
        "",
        f"- Runs: {payload['run_count']}",
        f"- Decision: `{payload['decision']}`",
        (
            "- Evidence risk difference: "
            f"{comparison['risk_difference']:.3f}"
        ),
        (
            "- Fisher exact two-sided p: "
            f"{comparison['fisher_exact_two_sided_p']:.8f}"
        ),
        "",
        "## Arm Results",
        "",
        "| Arm | Strict pass | Evidence pass | Gate pass | Transition pass |",
        "|---|---:|---:|---:|---:|",
    ]
    for arm, summary in payload["arm_summary"].items():
        components = summary["components"]
        lines.append(
            f"| `{arm}` | "
            f"{components['controlled_state_mutation_success']['successes']}/"
            f"{components['controlled_state_mutation_success']['total']} | "
            f"{components['exact_evidence_array_preservation']['successes']}/"
            f"{components['exact_evidence_array_preservation']['total']} | "
            f"{components['transition_gate_accuracy']['successes']}/"
            f"{components['transition_gate_accuracy']['total']} | "
            f"{components['state_transition_accuracy']['successes']}/"
            f"{components['state_transition_accuracy']['total']} |"
        )
    lines.extend(
        [
            "",
            "## Cell Results",
            "",
            "| Arm | Condition | Strict pass | Evidence pass | Cell decision |",
            "|---|---|---:|---:|---|",
        ]
    )
    for key, summary in payload["cell_summary"].items():
        arm, condition = key.split("::", 1)
        components = summary["components"]
        lines.append(
            f"| `{arm}` | `{condition}` | "
            f"{components['controlled_state_mutation_success']['successes']}/3 | "
            f"{components['exact_evidence_array_preservation']['successes']}/3 | "
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
    print(
        f"Analyzed {payload['run_count']} runs: {payload['decision']}"
    )


if __name__ == "__main__":
    main()
