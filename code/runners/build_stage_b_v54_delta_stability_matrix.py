#!/usr/bin/env python3
"""Build the fresh 40-run v5.4 matrix from frozen v5.3 P2 fixtures."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from build_stage_b_v5_state_transition import dump_json
from build_stage_b_v52_evidence_binding_ablation import CONDITIONS


def build_matrix(fixtures_dir: Path) -> dict[str, Any]:
    fixtures = [
        f"stage-b-v53-p2--{condition}" for condition in CONDITIONS
    ]
    runs = []
    for condition, fixture in zip(CONDITIONS, fixtures, strict=True):
        for repetition in range(1, 9):
            runs.append(
                {
                    "run_id": (
                        "stage-b-v54-delta-stability--"
                        f"{condition}__budget_model__G9__r{repetition}"
                    ),
                    "fixture": fixture,
                    "model": "budget_model",
                    "harness_arm": "G9",
                    "repetition": repetition,
                    "status": "planned",
                }
            )
    return {
        "protocol": "stage_b_v54_explicit_delta_stability",
        "fixtures_dir": str(fixtures_dir),
        "models": ["budget_model"],
        "harness_arms": ["G9"],
        "conditions": CONDITIONS,
        "fixtures": fixtures,
        "repetitions": 8,
        "run_count": len(runs),
        "pooling_policy": "fresh_v54_runs_only",
        "runs": runs,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixtures-dir", required=True)
    parser.add_argument("--matrix-output", required=True)
    args = parser.parse_args()
    fixtures_dir = Path(args.fixtures_dir)
    missing = [
        fixture
        for fixture in [
            f"stage-b-v53-p2--{condition}" for condition in CONDITIONS
        ]
        if not (fixtures_dir / fixture).is_dir()
    ]
    if missing:
        raise SystemExit(f"Missing frozen fixtures: {missing}")
    payload = build_matrix(fixtures_dir)
    dump_json(Path(args.matrix_output), payload)
    print(f"Built {payload['run_count']}-run v5.4 stability matrix")


if __name__ == "__main__":
    main()

