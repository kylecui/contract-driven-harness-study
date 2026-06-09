#!/usr/bin/env python3
"""Generate a benchmark run matrix from fixture directories."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


DEFAULT_MODELS = ["strong_model", "mid_model", "budget_model"]
DEFAULT_ARMS = ["G0", "G2", "G6", "G9"]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixtures-dir", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--repetitions", type=int, default=5)
    parser.add_argument("--models", nargs="*", default=DEFAULT_MODELS)
    parser.add_argument("--arms", nargs="*", default=DEFAULT_ARMS)
    parser.add_argument(
        "--fixtures",
        nargs="*",
        default=None,
        help="Optional fixture directory names to include. Defaults to all fixtures.",
    )
    args = parser.parse_args()

    root = Path(args.fixtures_dir)
    available_fixtures = sorted(p.name for p in root.iterdir() if p.is_dir())
    if args.fixtures:
        missing = sorted(set(args.fixtures) - set(available_fixtures))
        if missing:
            raise SystemExit(f"Unknown fixtures: {', '.join(missing)}")
        fixtures = list(args.fixtures)
    else:
        fixtures = available_fixtures
    runs = []
    for fixture in fixtures:
        for model in args.models:
            for arm in args.arms:
                for repetition in range(1, args.repetitions + 1):
                    runs.append(
                        {
                            "run_id": f"{fixture}__{model}__{arm}__r{repetition}",
                            "fixture": fixture,
                            "model": model,
                            "harness_arm": arm,
                            "repetition": repetition,
                            "status": "planned",
                        }
                    )

    matrix = {
        "fixtures_dir": str(root),
        "models": args.models,
        "harness_arms": args.arms,
        "fixtures": fixtures,
        "repetitions": args.repetitions,
        "run_count": len(runs),
        "runs": runs,
    }
    Path(args.output).write_text(
        json.dumps(matrix, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"Wrote {len(runs)} planned runs to {args.output}")


if __name__ == "__main__":
    main()
