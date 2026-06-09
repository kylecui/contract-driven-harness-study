#!/usr/bin/env python3
"""Select a subset of benchmark runs from a prepared manifest."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def split_csv(value: str | None) -> set[str] | None:
    if not value:
        return None
    return {item.strip() for item in value.split(",") if item.strip()}


def repetition(run_id: str) -> str | None:
    match = re.search(r"__r(\d+)$", run_id)
    if not match:
        return None
    return match.group(1)


def matches(run: dict[str, Any], filters: dict[str, set[str] | None]) -> bool:
    checks = {
        "fixture": str(run.get("fixture", "")),
        "model": str(run.get("model", "")),
        "harness_arm": str(run.get("harness_arm", "")),
        "repetition": repetition(str(run.get("run_id", ""))) or "",
    }
    for key, allowed in filters.items():
        if allowed is not None and checks[key] not in allowed:
            return False
    return True


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--fixtures", default=None, help="Comma-separated fixture names")
    parser.add_argument("--models", default=None, help="Comma-separated model tiers")
    parser.add_argument("--arms", default=None, help="Comma-separated harness arms")
    parser.add_argument("--repetitions", default=None, help="Comma-separated repetition numbers")
    parser.add_argument("--note", default="Selected benchmark manifest subset.")
    args = parser.parse_args()

    manifest = load_json(Path(args.manifest))
    filters = {
        "fixture": split_csv(args.fixtures),
        "model": split_csv(args.models),
        "harness_arm": split_csv(args.arms),
        "repetition": split_csv(args.repetitions),
    }
    selected = [run for run in manifest["runs"] if matches(run, filters)]
    output = dict(manifest)
    output["note"] = args.note
    output["parent_manifest"] = args.manifest
    output["selection_filters"] = {
        key: sorted(value) if value is not None else None for key, value in filters.items()
    }
    output["run_count"] = len(selected)
    output["runs"] = selected
    Path(args.output).write_text(
        json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"Selected {len(selected)} runs")
    if not selected:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
