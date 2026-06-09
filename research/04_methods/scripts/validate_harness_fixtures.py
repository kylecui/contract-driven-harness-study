#!/usr/bin/env python3
"""Validate minimal harness benchmark fixture consistency."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


REQUIRED_FILES = [
    "task_spec.json",
    "memory_slice.json",
    "evidence_bundle.json",
    "output_contract.json",
    "input.md",
]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_fixture(fixture_dir: Path) -> list[str]:
    errors: list[str] = []
    for name in REQUIRED_FILES:
        if not (fixture_dir / name).exists():
            errors.append(f"missing {name}")

    if errors:
        return errors

    task = load_json(fixture_dir / "task_spec.json")
    memory = load_json(fixture_dir / "memory_slice.json")
    evidence = load_json(fixture_dir / "evidence_bundle.json")
    output = load_json(fixture_dir / "output_contract.json")

    task_id = task.get("task_id")
    if not task_id:
        errors.append("task_spec.task_id missing")

    if task.get("memory_slice_id") != memory.get("memory_slice_id"):
        errors.append("task_spec.memory_slice_id does not match memory_slice.memory_slice_id")
    if task.get("evidence_bundle_id") != evidence.get("evidence_bundle_id"):
        errors.append("task_spec.evidence_bundle_id does not match evidence_bundle.evidence_bundle_id")
    if task.get("output_contract_id") != output.get("output_contract_id"):
        errors.append("task_spec.output_contract_id does not match output_contract.output_contract_id")

    for filename, payload in [
        ("memory_slice.json", memory),
        ("evidence_bundle.json", evidence),
    ]:
        if payload.get("task_id") != task_id:
            errors.append(f"{filename}.task_id does not match task_spec.task_id")

    evidence_items = evidence.get("items", [])
    if not isinstance(evidence_items, list) or not evidence_items:
        errors.append("evidence_bundle.items must be a non-empty list")

    required_sections = output.get("required_sections", [])
    if not isinstance(required_sections, list) or not required_sections:
        errors.append("output_contract.required_sections must be a non-empty list")

    return errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixtures-dir", required=True)
    args = parser.parse_args()

    root = Path(args.fixtures_dir)
    fixture_dirs = [p for p in root.iterdir() if p.is_dir()]
    if not fixture_dirs:
        raise SystemExit(f"No fixture directories found under {root}")

    failed = False
    for fixture_dir in sorted(fixture_dirs):
        errors = validate_fixture(fixture_dir)
        if errors:
            failed = True
            print(f"FAIL {fixture_dir.name}")
            for error in errors:
                print(f"  - {error}")
        else:
            print(f"OK {fixture_dir.name}")

    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

