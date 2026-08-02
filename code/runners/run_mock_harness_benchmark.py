#!/usr/bin/env python3
"""Run a deterministic mock benchmark over compiled harness packets.

This is an infrastructure pilot, not evidence about real model behavior. It
creates plausible metric-shaped outputs so the benchmark pipeline can be tested
end-to-end before model adapters are connected.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


MODEL_BASE = {
    "strong_model": 0.88,
    "mid_model": 0.72,
    "budget_model": 0.56,
}

ARM_BOOST = {
    "G0": 0.00,
    "G2": 0.10,
    "G6": 0.20,
    "G9": 0.28,
}

TASK_DIFFICULTY = {
    "structured_extraction": 0.05,
    "project_initialization": 0.08,
    "research_workflow": 0.16,
    "strategic_judgment": 0.26,
}

METRIC_WEIGHTS = {
    "task_success": 1.00,
    "schema_validity": 1.08,
    "tool_call_correctness": 0.92,
    "citation_grounding": 0.88,
    "human_acceptance": 0.95,
    "cost_efficiency": 0.72,
    "safety_consistency": 1.04,
}


def clamp(value: float) -> float:
    return round(max(0.0, min(1.0, value)), 3)


def repetition_noise(repetition: int, metric: str) -> float:
    # Deterministic, tiny variation to test aggregation without randomness.
    direction = 1 if (len(metric) + repetition) % 2 == 0 else -1
    return direction * (0.005 * (repetition - 3))


def score(packet: dict[str, Any]) -> dict[str, float]:
    model = str(packet["model"])
    arm = str(packet["harness_arm"])
    task_type = str(packet["task_type"])
    repetition = int(packet.get("repetition", 1))

    base = MODEL_BASE.get(model, 0.65)
    boost = ARM_BOOST.get(arm, 0.0)
    difficulty = TASK_DIFFICULTY.get(task_type, 0.12)

    # Harness helps high-constraint tasks more than low-constraint tasks.
    harness_multiplier = max(0.35, 1.15 - difficulty * 2.2)
    model_gap_retention = {
        "G0": 1.00,
        "G2": 0.78,
        "G6": 0.52,
        "G9": 0.34,
    }.get(arm, 1.0)

    # Pull weaker models upward as harness strength increases while preserving
    # some task/model differences.
    model_delta_from_mid = base - MODEL_BASE["mid_model"]
    normalized = MODEL_BASE["mid_model"] + model_delta_from_mid * model_gap_retention
    arm_score = normalized + boost * harness_multiplier - difficulty

    return {
        metric: clamp(arm_score * weight + repetition_noise(repetition, metric))
        for metric, weight in METRIC_WEIGHTS.items()
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--packets-jsonl", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    runs = []
    with Path(args.packets_jsonl).open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            packet = json.loads(line)
            runs.append(
                {
                    "run_id": packet["run_id"],
                    "fixture": packet["fixture"],
                    "task_class": packet["task_type"],
                    "model": packet["model"],
                    "harness_arm": packet["harness_arm"],
                    "repetition": packet.get("repetition", 1),
                    "metrics": score(packet),
                    "mock": True,
                }
            )

    payload = {
        "note": "Synthetic mock benchmark output for pipeline validation only.",
        "runs": runs,
    }
    Path(args.output).write_text(
        json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"Wrote {len(runs)} mock runs to {args.output}")


if __name__ == "__main__":
    main()

