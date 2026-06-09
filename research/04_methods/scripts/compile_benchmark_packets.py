#!/usr/bin/env python3
"""Compile benchmark run matrix entries into executable prompt packets.

This dry-run compiler does not call models. It checks that every planned run can
load its fixture and emits the exact packet shape a future runner should send to
model adapters.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any


ARM_LAYERS = {
    "G0": ["prompt_only"],
    "G2": ["prompt", "role_instruction", "output_schema"],
    "G6": [
        "prompt",
        "role_instruction",
        "output_schema",
        "evidence_bundle",
        "tool_contracts",
        "skills",
        "workflow",
    ],
    "G8": [
        "prompt",
        "role_instruction",
        "output_schema",
        "evidence_bundle",
        "tool_contracts",
        "skills",
        "workflow",
        "memory_policy",
        "validator",
    ],
    "G9": [
        "prompt",
        "role_instruction",
        "output_schema",
        "evidence_bundle",
        "tool_contracts",
        "skills",
        "workflow",
        "memory_policy",
        "validator",
        "trace",
        "regression",
    ],
}


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def compile_packet(run: dict[str, Any], fixtures_dir: Path) -> dict[str, Any]:
    fixture_dir = fixtures_dir / run["fixture"]
    task_spec = read_json(fixture_dir / "task_spec.json")
    memory_slice = read_json(fixture_dir / "memory_slice.json")
    evidence_bundle = read_json(fixture_dir / "evidence_bundle.json")
    output_contract = read_json(fixture_dir / "output_contract.json")
    user_input = read_text(fixture_dir / "input.md")

    arm = str(run["harness_arm"])
    layers = ARM_LAYERS.get(arm, ["unknown"])

    packet: dict[str, Any] = {
        "run_id": run["run_id"],
        "fixture": run["fixture"],
        "model": run["model"],
        "harness_arm": arm,
        "repetition": run["repetition"],
        "layers": layers,
        "task_spec": task_spec,
        "input": user_input,
        "output_contract": output_contract if arm in {"G2", "G6", "G8", "G9"} else None,
        "evidence_bundle": evidence_bundle if arm in {"G6", "G8", "G9"} else None,
        "memory_slice": memory_slice if arm in {"G8", "G9"} else None,
        "trace_required": arm in {"G6", "G9"},
        "validator_required": arm in {"G8", "G9"},
    }
    return packet


def packet_summary(packet: dict[str, Any]) -> dict[str, Any]:
    return {
        "run_id": packet["run_id"],
        "fixture": packet["fixture"],
        "model": packet["model"],
        "harness_arm": packet["harness_arm"],
        "task_type": packet["task_spec"]["task_type"],
        "layers": packet["layers"],
        "has_output_contract": packet["output_contract"] is not None,
        "has_evidence_bundle": packet["evidence_bundle"] is not None,
        "has_memory_slice": packet["memory_slice"] is not None,
        "trace_required": packet["trace_required"],
        "validator_required": packet["validator_required"],
    }


def markdown_report(
    summaries: list[dict[str, Any]], output_jsonl: Path, failures: list[str]
) -> str:
    by_arm = Counter(item["harness_arm"] for item in summaries)
    by_fixture = Counter(item["fixture"] for item in summaries)
    by_model = Counter(item["model"] for item in summaries)

    lines = [
        "# Benchmark Packet Dry-Run Report",
        "",
        "## Summary",
        "",
        f"- Packets compiled: {len(summaries)}",
        f"- Failures: {len(failures)}",
        f"- Packet JSONL: `{output_jsonl}`",
        "",
        "## Harness Arms",
        "",
        "| Arm | Packets |",
        "|---|---:|",
    ]
    for arm, count in sorted(by_arm.items()):
        lines.append(f"| `{arm}` | {count} |")

    lines.extend(["", "## Fixtures", "", "| Fixture | Packets |", "|---|---:|"])
    for fixture, count in sorted(by_fixture.items()):
        lines.append(f"| `{fixture}` | {count} |")

    lines.extend(["", "## Models", "", "| Model | Packets |", "|---|---:|"])
    for model, count in sorted(by_model.items()):
        lines.append(f"| `{model}` | {count} |")

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "This is a benchmark infrastructure dry-run, not a model evaluation. It proves the planned matrix can be compiled into consistent model-adapter packets.",
            "",
            "## Failures",
            "",
        ]
    )
    if failures:
        for failure in failures:
            lines.append(f"- {failure}")
    else:
        lines.append("- None")

    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--matrix", required=True)
    parser.add_argument("--output-jsonl", required=True)
    parser.add_argument("--output-md", required=True)
    parser.add_argument("--full-packets", action="store_true")
    args = parser.parse_args()

    matrix_path = Path(args.matrix)
    matrix = read_json(matrix_path)
    fixtures_dir = Path(matrix["fixtures_dir"])
    if not fixtures_dir.is_absolute():
        fixtures_dir = matrix_path.parent.parent.parent / fixtures_dir
    fixtures_dir = fixtures_dir.resolve()

    output_jsonl = Path(args.output_jsonl)
    output_md = Path(args.output_md)
    output_jsonl.parent.mkdir(parents=True, exist_ok=True)
    output_md.parent.mkdir(parents=True, exist_ok=True)

    summaries: list[dict[str, Any]] = []
    failures: list[str] = []
    with output_jsonl.open("w", encoding="utf-8") as handle:
        for run in matrix["runs"]:
            try:
                packet = compile_packet(run, fixtures_dir)
                payload = packet if args.full_packets else packet_summary(packet)
                handle.write(json.dumps(payload, ensure_ascii=False) + "\n")
                summaries.append(packet_summary(packet))
            except Exception as exc:  # noqa: BLE001 - report all dry-run issues
                failures.append(f"{run.get('run_id', '<unknown>')}: {exc}")

    output_md.write_text(
        markdown_report(summaries, output_jsonl, failures), encoding="utf-8"
    )
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
