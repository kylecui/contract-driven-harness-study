#!/usr/bin/env python3
"""Preflight checks before running the first real model-backed pilot.

This script is local-only. It reads manifests, provider config, prompts,
adapter requests, and validation artifacts, then writes a readiness report. It
does not call any provider API.
"""

from __future__ import annotations

import argparse
import json
import os
from collections import Counter
from pathlib import Path
from typing import Any


REQUIRED_PATHS = [
    "output",
    "tool_trace",
    "validation_report",
    "metrics",
    "prompt",
    "adapter_request",
]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def dump_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def resolve(path_text: str) -> Path:
    return Path(path_text)


def is_pending_placeholder(path: Path) -> bool:
    if not path.exists() or path.stat().st_size == 0:
        return False
    text = path.read_text(encoding="utf-8", errors="replace")
    return "Status: pending" in text and "replaced by the real model adapter" in text


def validate_config(
    config: dict[str, Any],
    *,
    config_path: Path,
    required_tiers: set[str],
    require_keys: bool,
) -> tuple[list[str], list[str], dict[str, Any]]:
    errors: list[str] = []
    warnings: list[str] = []
    summary: dict[str, Any] = {
        "providers": {},
        "model_tiers": {},
        "config_path": str(config_path),
    }

    if "example" in config_path.name.lower():
        warnings.append("config filename looks like an example; confirm model IDs before execution")

    providers = config.get("providers")
    model_tiers = config.get("model_tiers")
    if not isinstance(providers, dict) or not providers:
        errors.append("providers must be a non-empty object")
        providers = {}
    if not isinstance(model_tiers, dict) or not model_tiers:
        errors.append("model_tiers must be a non-empty object")
        model_tiers = {}

    for tier in sorted(required_tiers):
        if tier not in model_tiers:
            errors.append(f"missing model tier mapping: {tier}")

    for tier, mapping in model_tiers.items():
        if not isinstance(mapping, dict):
            errors.append(f"model_tiers.{tier} must be an object")
            continue
        provider_name = mapping.get("provider")
        model_name = mapping.get("model")
        summary["model_tiers"][tier] = {
            "provider": provider_name,
            "model": model_name,
        }
        if not provider_name:
            errors.append(f"model_tiers.{tier}.provider missing")
        elif provider_name not in providers:
            errors.append(f"model_tiers.{tier}.provider references unknown provider: {provider_name}")
        if not model_name:
            errors.append(f"model_tiers.{tier}.model missing")

    for provider_name, provider in providers.items():
        if not isinstance(provider, dict):
            errors.append(f"providers.{provider_name} must be an object")
            continue
        key_env = provider.get("api_key_env")
        key_present = bool(key_env and os.environ.get(str(key_env)))
        summary["providers"][provider_name] = {
            "api_key_env": key_env,
            "api_key_present": key_present,
            "base_url": provider.get("base_url"),
        }
        if not key_env:
            errors.append(f"providers.{provider_name}.api_key_env missing")
        elif require_keys and not key_present:
            errors.append(f"environment variable not set: {key_env}")
        elif not key_present:
            warnings.append(f"environment variable not set: {key_env}")

    return errors, warnings, summary


def validate_runs(manifest: dict[str, Any]) -> tuple[list[str], list[str], dict[str, Any]]:
    errors: list[str] = []
    warnings: list[str] = []
    runs = manifest.get("runs")
    if not isinstance(runs, list) or not runs:
        return ["manifest.runs must be a non-empty list"], warnings, {}

    seen: set[str] = set()
    status_counts: Counter[str] = Counter()
    validation_status_counts: Counter[str] = Counter()
    group_counts: Counter[str] = Counter()
    non_placeholder_outputs: list[str] = []
    missing_paths: list[str] = []
    required_tiers: set[str] = set()

    for run in runs:
        run_id = str(run.get("run_id", ""))
        if not run_id:
            errors.append("run missing run_id")
            continue
        if run_id in seen:
            errors.append(f"duplicate run_id: {run_id}")
        seen.add(run_id)

        status_counts[str(run.get("status", "unknown"))] += 1
        fixture = str(run.get("fixture", "unknown"))
        model_tier = str(run.get("model", "unknown"))
        harness_arm = str(run.get("harness_arm", "unknown"))
        required_tiers.add(model_tier)
        group_counts[f"{fixture} | {model_tier} | {harness_arm}"] += 1

        paths = run.get("paths")
        if not isinstance(paths, dict):
            errors.append(f"{run_id}: paths must be an object")
            continue
        for key in REQUIRED_PATHS:
            raw_path = paths.get(key)
            if not raw_path:
                errors.append(f"{run_id}: missing paths.{key}")
                continue
            path = resolve(str(raw_path))
            if not path.exists():
                missing_paths.append(f"{run_id}: {key} -> {path}")

        validation_path = resolve(str(paths.get("validation_report", "")))
        if validation_path.exists():
            validation = load_json(validation_path)
            validation_status_counts[str(validation.get("status", "unknown"))] += 1
        else:
            validation_status_counts["missing"] += 1

        request_path = resolve(str(paths.get("adapter_request", "")))
        if request_path.exists():
            adapter_request = load_json(request_path)
            if adapter_request.get("run_id") != run_id:
                errors.append(f"{run_id}: adapter_request.run_id mismatch")
            if adapter_request.get("model_tier") != model_tier:
                errors.append(f"{run_id}: adapter_request.model_tier mismatch")

        output_path = resolve(str(paths.get("output", "")))
        if output_path.exists() and output_path.stat().st_size > 0:
            if not is_pending_placeholder(output_path):
                non_placeholder_outputs.append(run_id)

    if missing_paths:
        errors.extend(missing_paths)
    if non_placeholder_outputs:
        warnings.append(
            f"{len(non_placeholder_outputs)} output files are non-placeholder and may be overwritten"
        )

    summary = {
        "run_count": len(runs),
        "required_model_tiers": sorted(required_tiers),
        "manifest_status_counts": dict(sorted(status_counts.items())),
        "validation_status_counts": dict(sorted(validation_status_counts.items())),
        "group_counts": dict(sorted(group_counts.items())),
        "non_placeholder_outputs": non_placeholder_outputs,
    }
    return errors, warnings, summary


def write_markdown(path: Path, report: dict[str, Any]) -> None:
    lines: list[str] = []
    status = "FAIL" if report["errors"] else "WARN" if report["warnings"] else "PASS"
    lines.append("# Real Model Pilot Preflight")
    lines.append("")
    lines.append(f"- Status: {status}")
    lines.append("- Network/API calls made: no")
    lines.append(f"- Manifest: `{report['manifest_path']}`")
    lines.append(f"- Config: `{report['config_path']}`")
    lines.append(f"- Runs: {report['runs'].get('run_count', 0)}")
    lines.append("")

    lines.append("## Provider Readiness")
    lines.append("")
    providers = report["config"].get("providers", {})
    if providers:
        lines.append("| Provider | Key env | Key present | Base URL |")
        lines.append("|---|---|---:|---|")
        for provider_name, provider in providers.items():
            key_present = "yes" if provider.get("api_key_present") else "no"
            lines.append(
                f"| `{provider_name}` | `{provider.get('api_key_env')}` | {key_present} | `{provider.get('base_url')}` |"
            )
    else:
        lines.append("- No provider summary available.")
    lines.append("")

    lines.append("## Model Tiers")
    lines.append("")
    model_tiers = report["config"].get("model_tiers", {})
    if model_tiers:
        lines.append("| Tier | Provider | Model |")
        lines.append("|---|---|---|")
        for tier, mapping in model_tiers.items():
            lines.append(f"| `{tier}` | `{mapping.get('provider')}` | `{mapping.get('model')}` |")
    else:
        lines.append("- No model-tier summary available.")
    lines.append("")

    lines.append("## Validation Status")
    lines.append("")
    validation_counts = report["runs"].get("validation_status_counts", {})
    if validation_counts:
        for key, value in validation_counts.items():
            lines.append(f"- {key}: {value}")
    else:
        lines.append("- No validation status counts available.")
    lines.append("")

    lines.append("## Run Groups")
    lines.append("")
    lines.append("| Fixture / Model / Arm | Runs |")
    lines.append("|---|---:|")
    for key, value in report["runs"].get("group_counts", {}).items():
        lines.append(f"| `{key}` | {value} |")
    lines.append("")

    lines.append("## Errors")
    lines.append("")
    if report["errors"]:
        for error in report["errors"]:
            lines.append(f"- {error}")
    else:
        lines.append("- None")
    lines.append("")

    lines.append("## Warnings")
    lines.append("")
    if report["warnings"]:
        for warning in report["warnings"]:
            lines.append(f"- {warning}")
    else:
        lines.append("- None")
    lines.append("")

    lines.append("## Execution Gate")
    lines.append("")
    if report["errors"]:
        lines.append("Do not run the adapter with `--execute` until errors are fixed.")
    else:
        lines.append(
            "The artifact queue is structurally ready. Real execution still requires explicit approval, confirmed model IDs, API credentials, and budget."
        )
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--config", required=True)
    parser.add_argument("--output-md", required=True)
    parser.add_argument("--output-json", default=None)
    parser.add_argument("--require-keys", action="store_true")
    args = parser.parse_args()

    manifest_path = Path(args.manifest)
    config_path = Path(args.config)
    manifest = load_json(manifest_path)
    config = load_json(config_path)

    run_errors, run_warnings, run_summary = validate_runs(manifest)
    config_errors, config_warnings, config_summary = validate_config(
        config,
        config_path=config_path,
        required_tiers=set(run_summary.get("required_model_tiers", [])),
        require_keys=args.require_keys,
    )
    report = {
        "manifest_path": str(manifest_path),
        "config_path": str(config_path),
        "require_keys": args.require_keys,
        "errors": run_errors + config_errors,
        "warnings": run_warnings + config_warnings,
        "runs": run_summary,
        "config": config_summary,
    }

    output_md = Path(args.output_md)
    write_markdown(output_md, report)
    if args.output_json:
        dump_json(Path(args.output_json), report)

    status = "FAIL" if report["errors"] else "WARN" if report["warnings"] else "PASS"
    print(f"Preflight {status}: errors={len(report['errors'])}; warnings={len(report['warnings'])}")
    if report["errors"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
