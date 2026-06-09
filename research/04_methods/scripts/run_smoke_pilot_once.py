#!/usr/bin/env python3
"""Run the first-slice smoke pilot workflow.

Default mode is dry-run only. Real provider execution requires both:

- --execute
- --confirm-cost

The workflow always runs preflight first. When execution is enabled, preflight
requires configured API keys before the adapter is called.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def dump_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def run_step(args: list[str]) -> int:
    completed = subprocess.run(args, check=False)
    return completed.returncode


def write_summary(path: Path, report: dict[str, Any]) -> None:
    lines = [
        "# Smoke Pilot Workflow Summary",
        "",
        f"- Execute mode: {'yes' if report['execute'] else 'no'}",
        f"- Cost confirmed: {'yes' if report['confirm_cost'] else 'no'}",
        f"- Workflow status: {report['status']}",
        f"- Manifest: `{report['manifest']}`",
        f"- Config: `{report['config']}`",
        "",
        "## Steps",
        "",
        "| Step | Return Code | Output |",
        "|---|---:|---|",
    ]
    for step in report["steps"]:
        lines.append(f"| {step['name']} | {step['return_code']} | `{step['output']}` |")
    if report.get("decision"):
        lines.extend(["", "## Decision", "", report["decision"]])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--manifest",
        default="research/05_analysis/real-run-artifacts/first-slice-smoke-manifest.json",
    )
    parser.add_argument(
        "--config",
        default="research/04_methods/provider-config.openai-reviewed.json",
    )
    parser.add_argument(
        "--output-prefix",
        default="research/05_analysis/smoke-pilot-once",
    )
    parser.add_argument("--baseline-arm", default="G0")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--confirm-cost", action="store_true")
    args = parser.parse_args()

    if args.execute and not args.confirm_cost:
        print("Refusing execution: --execute requires --confirm-cost")
        raise SystemExit(2)

    script_dir = Path(__file__).resolve().parent
    prefix = Path(args.output_prefix)
    outputs = {
        "preflight_md": f"{prefix}-preflight.md",
        "preflight_json": f"{prefix}-preflight.json",
        "adapter_report": f"{prefix}-adapter.json",
        "postprocess_prefix": f"{prefix}-postprocess",
        "summary_md": f"{prefix}-summary.md",
        "summary_json": f"{prefix}-summary.json",
    }

    steps: list[dict[str, Any]] = []
    preflight_args = [
        sys.executable,
        str(script_dir / "preflight_real_model_pilot.py"),
        "--manifest",
        args.manifest,
        "--config",
        args.config,
        "--output-md",
        outputs["preflight_md"],
        "--output-json",
        outputs["preflight_json"],
    ]
    if args.execute:
        preflight_args.append("--require-keys")

    preflight_code = run_step(preflight_args)
    steps.append(
        {
            "name": "preflight",
            "return_code": preflight_code,
            "output": outputs["preflight_md"],
        }
    )
    if preflight_code != 0:
        report = {
            "execute": args.execute,
            "confirm_cost": args.confirm_cost,
            "status": "blocked",
            "manifest": args.manifest,
            "config": args.config,
            "steps": steps,
            "decision": "Preflight failed; adapter was not called.",
        }
        dump_json(Path(outputs["summary_json"]), report)
        write_summary(Path(outputs["summary_md"]), report)
        raise SystemExit(preflight_code)

    adapter_args = [
        sys.executable,
        str(script_dir / "run_openai_adapter.py"),
        "--manifest",
        args.manifest,
        "--config",
        args.config,
        "--report",
        outputs["adapter_report"],
    ]
    if args.execute:
        adapter_args.append("--execute")

    adapter_code = run_step(adapter_args)
    steps.append(
        {
            "name": "adapter",
            "return_code": adapter_code,
            "output": outputs["adapter_report"],
        }
    )
    if adapter_code != 0:
        report = {
            "execute": args.execute,
            "confirm_cost": args.confirm_cost,
            "status": "failed",
            "manifest": args.manifest,
            "config": args.config,
            "steps": steps,
            "decision": "Adapter failed; postprocess was not run.",
        }
        dump_json(Path(outputs["summary_json"]), report)
        write_summary(Path(outputs["summary_md"]), report)
        raise SystemExit(adapter_code)

    postprocess_code = run_step(
        [
            sys.executable,
            str(script_dir / "postprocess_real_model_pilot.py"),
            "--manifest",
            args.manifest,
            "--output-prefix",
            outputs["postprocess_prefix"],
            "--baseline-arm",
            args.baseline_arm,
        ]
    )
    steps.append(
        {
            "name": "postprocess",
            "return_code": postprocess_code,
            "output": f"{outputs['postprocess_prefix']}-summary.md",
        }
    )
    status = "complete" if postprocess_code == 0 else "failed"
    decision = (
        "Dry-run workflow completed without provider calls."
        if not args.execute
        else "Execution workflow completed; inspect postprocess outputs before updating evidence."
    )
    report = {
        "execute": args.execute,
        "confirm_cost": args.confirm_cost,
        "status": status,
        "manifest": args.manifest,
        "config": args.config,
        "steps": steps,
        "decision": decision,
    }
    dump_json(Path(outputs["summary_json"]), report)
    write_summary(Path(outputs["summary_md"]), report)
    print(f"Smoke pilot workflow {status}; execute={args.execute}")
    if postprocess_code != 0:
        raise SystemExit(postprocess_code)


if __name__ == "__main__":
    main()
