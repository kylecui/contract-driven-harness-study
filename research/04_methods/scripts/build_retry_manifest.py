#!/usr/bin/env python3
"""Build retry artifacts while preserving original attempt lineage."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path
from typing import Any


PLACEHOLDER_OUTPUT = """# Model Output

Status: pending

This file should be replaced by the real model adapter.
"""


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def dump_json(path: Path, payload: Any) -> None:
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-manifest", required=True)
    parser.add_argument("--run-ids", nargs="+", required=True)
    parser.add_argument("--runs-dir", required=True)
    parser.add_argument("--output-manifest", required=True)
    parser.add_argument("--attempt", type=int, required=True)
    args = parser.parse_args()

    source_manifest = load_json(Path(args.source_manifest))
    by_id = {run["run_id"]: run for run in source_manifest["runs"]}
    missing = [run_id for run_id in args.run_ids if run_id not in by_id]
    if missing:
        raise SystemExit("Unknown run IDs: " + ", ".join(missing))

    runs_dir = Path(args.runs_dir)
    runs_dir.mkdir(parents=True, exist_ok=True)
    retry_runs: list[dict[str, Any]] = []

    for original_id in args.run_ids:
        source_run = by_id[original_id]
        retry_id = f"{original_id}__retry{args.attempt - 1}"
        run_dir = runs_dir / retry_id
        run_dir.mkdir(parents=True, exist_ok=True)

        prompt_path = run_dir / "prompt.md"
        shutil.copyfile(Path(source_run["paths"]["prompt"]), prompt_path)

        adapter_request = load_json(Path(source_run["paths"]["adapter_request"]))
        adapter_request.update(
            {
                "run_id": retry_id,
                "prompt_path": str(prompt_path),
                "lineage_id": original_id,
                "attempt": args.attempt,
                "retry_of_run_id": original_id,
            }
        )
        request_path = run_dir / "adapter_request.json"
        dump_json(request_path, adapter_request)

        paths = {
            "output": str(run_dir / "output.md"),
            "tool_trace": str(run_dir / "tool_trace.jsonl"),
            "validation_report": str(run_dir / "validation_report.json"),
            "metrics": str(run_dir / "metrics.json"),
            "prompt": str(prompt_path),
            "adapter_request": str(request_path),
        }
        retry_run = {
            "run_id": retry_id,
            "fixture": source_run["fixture"],
            "task_type": source_run["task_type"],
            "model": source_run["model"],
            "harness_arm": source_run["harness_arm"],
            "status": "pending",
            "paths": paths,
            "retry_lineage": {
                "lineage_id": original_id,
                "attempt": args.attempt,
                "retry_of_run_id": original_id,
            },
        }
        dump_json(run_dir / "manifest.json", retry_run)
        (run_dir / "output.md").write_text(PLACEHOLDER_OUTPUT, encoding="utf-8")
        (run_dir / "tool_trace.jsonl").write_text(
            '{"status":"pending","note":"Retry adapter should write trace events here."}\n',
            encoding="utf-8",
        )
        dump_json(run_dir / "validation_report.json", {"status": "pending"})
        dump_json(run_dir / "metrics.json", {"status": "pending"})
        retry_runs.append(retry_run)

    dump_json(
        Path(args.output_manifest),
        {
            "note": "Retry manifest preserving original failed attempt lineage.",
            "run_count": len(retry_runs),
            "runs_dir": str(runs_dir),
            "source_manifest": args.source_manifest,
            "attempt": args.attempt,
            "runs": retry_runs,
        },
    )
    print(f"Prepared {len(retry_runs)} retry runs under {runs_dir}")


if __name__ == "__main__":
    main()
