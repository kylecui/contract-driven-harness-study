#!/usr/bin/env python3
"""Build a human-readable adapter execution queue from a prompt manifest."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def build_markdown(manifest: dict[str, Any]) -> str:
    lines = [
        "# First-Slice Adapter Queue",
        "",
        "Use this queue for the first real model-backed benchmark pilot. Each row points to a rendered prompt and the artifact files the adapter should fill.",
        "",
        "| Run | Fixture | Model | Arm | Prompt | Output | Metrics |",
        "|---|---|---|---|---|---|---|",
    ]
    for run in manifest["runs"]:
        paths = run["paths"]
        lines.append(
            f"| `{run['run_id']}` | `{run['fixture']}` | `{run['model']}` | "
            f"`{run['harness_arm']}` | `{paths.get('prompt', '')}` | "
            f"`{paths['output']}` | `{paths['metrics']}` |"
        )
    lines.extend(
        [
            "",
            "## Execution Notes",
            "",
            "- Fill `output.md` with the raw model response before any repair.",
            "- Fill `tool_trace.jsonl` when the harness arm requires tracing, or leave a no-tools event if no tools were used.",
            "- Run `evaluate_real_run_artifacts.py` after outputs are filled.",
            "- Run `harness_benchmark_metrics.py` after evaluated runs are aggregated.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    manifest = load_json(Path(args.manifest))
    Path(args.output).write_text(build_markdown(manifest), encoding="utf-8")
    print(f"Wrote adapter queue for {len(manifest['runs'])} runs")


if __name__ == "__main__":
    main()

