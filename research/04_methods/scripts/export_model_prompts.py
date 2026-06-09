#!/usr/bin/env python3
"""Export model prompts for compiled benchmark packets.

This does not call a model. It renders the exact prompt/request payload a future
adapter can send to a provider, and attaches those paths to each run manifest.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load_packets(path: Path) -> dict[str, dict[str, Any]]:
    packets: dict[str, dict[str, Any]] = {}
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                packet = json.loads(line)
                packets[packet["run_id"]] = packet
    return packets


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def dump_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def fenced_json(title: str, payload: Any) -> str:
    return f"## {title}\n\n```json\n{json.dumps(payload, indent=2, ensure_ascii=False)}\n```\n"


def render_prompt(packet: dict[str, Any]) -> str:
    arm = packet["harness_arm"]
    task_spec = packet["task_spec"]
    output_contract = packet.get("output_contract")
    evidence_bundle = packet.get("evidence_bundle")
    memory_slice = packet.get("memory_slice")

    lines = [
        f"# Benchmark Run: {packet['run_id']}",
        "",
        "You are completing a benchmark task. Follow the instructions for the assigned harness arm.",
        "",
        f"- Fixture: `{packet['fixture']}`",
        f"- Model tier: `{packet['model']}`",
        f"- Harness arm: `{arm}`",
        f"- Task type: `{task_spec['task_type']}`",
        "",
    ]

    if arm == "G0":
        lines.extend(
            [
                "## Harness Arm G0",
                "",
                "Use only the task input below. Do not assume extra schemas, memory, tools, or evidence beyond what is present in the task text.",
                "",
            ]
        )
    elif arm == "G9":
        lines.extend(
            [
                "## Harness Arm G9",
                "",
                "Use the full harness packet. Obey the task spec, preserve evidence IDs for important claims, respect memory boundaries, and satisfy the output contract.",
                "",
            ]
        )
    else:
        lines.extend(
            [
                f"## Harness Arm {arm}",
                "",
                "Use the harness layers provided in this packet.",
                "",
            ]
        )

    lines.append(fenced_json("TaskSpec", task_spec))

    if evidence_bundle is not None:
        lines.append(fenced_json("EvidenceBundle", evidence_bundle))
    if memory_slice is not None:
        lines.append(fenced_json("MemorySlice", memory_slice))
    if output_contract is not None:
        lines.append(fenced_json("OutputContract", output_contract))

    lines.extend(["## Task Input", "", packet["input"].strip(), "", "## Output Requirements", ""])
    if output_contract is None:
        lines.append("Return the best answer for the task in a concise, reviewable form.")
    else:
        required = ", ".join(f"`{section}`" for section in output_contract["required_sections"])
        lines.append(
            f"Return `{output_contract['format']}` and include these required fields/sections: {required}."
        )
        if output_contract["citation_policy"] != "none":
            lines.append(f"Citation policy: `{output_contract['citation_policy']}`.")
        if output_contract.get("tool_trace_required"):
            lines.append("If tools are used, preserve a trace of what was used and why.")

    lines.append("")
    return "\n".join(lines)


def adapter_request(packet: dict[str, Any], prompt_path: Path) -> dict[str, Any]:
    return {
        "run_id": packet["run_id"],
        "provider": "manual_or_future_adapter",
        "model_tier": packet["model"],
        "harness_arm": packet["harness_arm"],
        "prompt_path": str(prompt_path),
        "temperature": 0,
        "tools_enabled": packet.get("trace_required", False),
        "expects_validation": True,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--packets-jsonl", required=True)
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--output-manifest", required=True)
    args = parser.parse_args()

    packets = load_packets(Path(args.packets_jsonl))
    manifest = load_json(Path(args.manifest))

    missing: list[str] = []
    for run in manifest["runs"]:
        run_id = run["run_id"]
        packet = packets.get(run_id)
        if packet is None:
            missing.append(run_id)
            continue

        run_dir = Path(run["paths"]["output"]).parent
        prompt_path = run_dir / "prompt.md"
        request_path = run_dir / "adapter_request.json"
        prompt_path.write_text(render_prompt(packet), encoding="utf-8")
        dump_json(request_path, adapter_request(packet, prompt_path))

        run["paths"]["prompt"] = str(prompt_path)
        run["paths"]["adapter_request"] = str(request_path)

        run_manifest_path = run_dir / "manifest.json"
        run_manifest = load_json(run_manifest_path)
        run_manifest["paths"]["prompt"] = str(prompt_path)
        run_manifest["paths"]["adapter_request"] = str(request_path)
        dump_json(run_manifest_path, run_manifest)

    if missing:
        raise SystemExit(f"Missing packets for run IDs: {', '.join(missing)}")

    dump_json(Path(args.output_manifest), manifest)
    print(f"Exported prompts for {len(manifest['runs'])} runs")


if __name__ == "__main__":
    main()

