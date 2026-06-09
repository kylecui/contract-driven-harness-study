#!/usr/bin/env python3
"""Prepare artifact directories for real model-backed benchmark runs.

This script does not call a model. It expands compiled packet summaries into
per-run directories with a manifest and placeholder files that a future adapter
can fill.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


PLACEHOLDER_OUTPUT = """# Model Output

Status: pending

This file should be replaced by the real model adapter.
"""


PLACEHOLDER_TRACE = """{"status":"pending","note":"Real adapter should write tool trace events here."}
"""


def load_packets(path: Path) -> list[dict[str, Any]]:
    packets: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                packets.append(json.loads(line))
    return packets


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--packets-jsonl", required=True)
    parser.add_argument("--runs-dir", required=True)
    parser.add_argument("--output-manifest", required=True)
    args = parser.parse_args()

    packets = load_packets(Path(args.packets_jsonl))
    runs_dir = Path(args.runs_dir)
    runs_dir.mkdir(parents=True, exist_ok=True)

    manifest_runs = []
    for packet in packets:
        run_id = packet["run_id"]
        run_dir = runs_dir / run_id
        run_dir.mkdir(parents=True, exist_ok=True)
        task_type = packet.get("task_type")
        if task_type is None and isinstance(packet.get("task_spec"), dict):
            task_type = packet["task_spec"].get("task_type")
        if task_type is None:
            raise KeyError(f"{run_id}: missing task_type")

        manifest = {
            "run_id": run_id,
            "fixture": packet["fixture"],
            "task_type": task_type,
            "model": packet["model"],
            "harness_arm": packet["harness_arm"],
            "status": "pending",
            "paths": {
                "output": str(run_dir / "output.md"),
                "tool_trace": str(run_dir / "tool_trace.jsonl"),
                "validation_report": str(run_dir / "validation_report.json"),
                "metrics": str(run_dir / "metrics.json"),
            },
        }
        (run_dir / "manifest.json").write_text(
            json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        (run_dir / "output.md").write_text(PLACEHOLDER_OUTPUT, encoding="utf-8")
        (run_dir / "tool_trace.jsonl").write_text(PLACEHOLDER_TRACE, encoding="utf-8")
        (run_dir / "validation_report.json").write_text(
            json.dumps({"status": "pending"}, indent=2), encoding="utf-8"
        )
        (run_dir / "metrics.json").write_text(
            json.dumps({"status": "pending"}, indent=2), encoding="utf-8"
        )
        manifest_runs.append(manifest)

    output_manifest = {
        "note": "Prepared artifact directories for real model-backed benchmark runs.",
        "run_count": len(manifest_runs),
        "runs_dir": str(runs_dir),
        "runs": manifest_runs,
    }
    Path(args.output_manifest).write_text(
        json.dumps(output_manifest, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"Prepared {len(manifest_runs)} run artifact directories under {runs_dir}")


if __name__ == "__main__":
    main()
