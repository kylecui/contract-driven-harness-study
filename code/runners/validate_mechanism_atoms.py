#!/usr/bin/env python3
"""Validate mechanism atom fixture specifications."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


REQUIRED_FILES = [
    "mechanism_atom.json",
    "task_spec.json",
    "memory_slice.json",
    "evidence_bundle.json",
    "output_contract.json",
    "input.md",
    "golden_output.json",
]

MECHANISMS = {
    "OutputContract",
    "EvidenceBundle",
    "TaskSpec",
    "MemorySlice",
    "WorkflowGraph",
    "ValidatorGate",
    "TraceLog",
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_atom(atom_dir: Path) -> list[str]:
    errors: list[str] = []
    for name in REQUIRED_FILES:
        if not (atom_dir / name).exists():
            errors.append(f"missing {name}")
    bad_dir = atom_dir / "known_bad_outputs"
    if not bad_dir.exists() or not any(bad_dir.glob("*.json")):
        errors.append("known_bad_outputs must contain at least one JSON fixture")
    if errors:
        return errors

    atom = load_json(atom_dir / "mechanism_atom.json")
    task = load_json(atom_dir / "task_spec.json")
    output = load_json(atom_dir / "output_contract.json")

    primary = atom.get("primary_mechanism")
    if primary not in MECHANISMS:
        errors.append("mechanism_atom.primary_mechanism is invalid")

    supporting = atom.get("supporting_mechanisms")
    if not isinstance(supporting, list):
        errors.append("mechanism_atom.supporting_mechanisms must be a list")
    elif any(item not in MECHANISMS for item in supporting):
        errors.append("mechanism_atom.supporting_mechanisms contains invalid mechanism")

    if task.get("task_type") != "mechanism_atom":
        errors.append("task_spec.task_type must be mechanism_atom")

    if atom.get("output_contract_id") != output.get("output_contract_id"):
        errors.append("mechanism_atom.output_contract_id does not match output_contract")

    if not atom.get("known_failure_modes"):
        errors.append("mechanism_atom.known_failure_modes must be non-empty")

    pass_criteria = atom.get("pass_criteria", [])
    if not isinstance(pass_criteria, list) or not pass_criteria:
        errors.append("mechanism_atom.pass_criteria must be non-empty")
    else:
        for index, criterion in enumerate(pass_criteria, start=1):
            if not criterion.get("metric"):
                errors.append(f"pass_criteria[{index}].metric missing")
            threshold = criterion.get("threshold")
            if not isinstance(threshold, (int, float)) or not 0 <= float(threshold) <= 1:
                errors.append(f"pass_criteria[{index}].threshold must be between 0 and 1")

    interface = atom.get("composition_interface", {})
    for key in [
        "input_from_previous",
        "output_to_next",
        "state_dependencies",
        "evidence_dependencies",
        "failure_signal",
        "repair_policy",
    ]:
        if key not in interface:
            errors.append(f"composition_interface.{key} missing")
    if not interface.get("output_to_next"):
        errors.append("composition_interface.output_to_next must be non-empty")

    return errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--atoms-dir", required=True)
    args = parser.parse_args()

    root = Path(args.atoms_dir)
    atom_dirs = [path for path in root.iterdir() if path.is_dir()]
    if not atom_dirs:
        raise SystemExit(f"No atom directories found under {root}")

    failed = False
    for atom_dir in sorted(atom_dirs):
        errors = validate_atom(atom_dir)
        if errors:
            failed = True
            print(f"FAIL {atom_dir.name}")
            for error in errors:
                print(f"  - {error}")
        else:
            print(f"OK {atom_dir.name}")

    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
