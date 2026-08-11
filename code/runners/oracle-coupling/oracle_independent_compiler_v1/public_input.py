"""Allowlist projection and serialization for the experiment boundary."""

from __future__ import annotations

import copy
from collections.abc import Mapping
from typing import Any

from public_policy_compiler import DerivedContract, PublicFixture


PUBLIC_TOP_LEVEL_FIELDS = frozenset({
    "fixture_id",
    "split",
    "family",
    "request",
    "initial_state",
    "evidence",
    "obligations",
})

PUBLIC_OBLIGATION_FIELDS = frozenset({
    "editable_paths",
    "immutable_paths",
    "on_block_preserve_paths",
    "unknown_state",
    "forbidden_inferences",
})

FORBIDDEN_INPUT_KEYS = frozenset({
    "expected_output",
    "gold",
    "answer_key",
    "objective",
    "gate_rule",
    "required_decision_evidence_ids",
    "distractor_evidence_ids",
})


def project_public_fixture(raw: Mapping[str, Any]) -> PublicFixture:
    """Copy only the declared public-input fields into a typed object."""
    obligations = raw["obligations"]
    if not isinstance(obligations, Mapping):
        raise TypeError("obligations must be a mapping")
    return PublicFixture(
        fixture_id=str(raw["fixture_id"]),
        split=str(raw["split"]),
        family=str(raw["family"]),
        request=str(raw["request"]),
        initial_state=copy.deepcopy(dict(raw["initial_state"])),
        evidence=tuple(copy.deepcopy(list(raw["evidence"]))),
        editable_paths=tuple(copy.deepcopy(obligations["editable_paths"])),
        immutable_paths=tuple(copy.deepcopy(obligations["immutable_paths"])),
        on_block_preserve_paths=tuple(
            copy.deepcopy(obligations["on_block_preserve_paths"])
        ),
        unknown_state=tuple(copy.deepcopy(obligations["unknown_state"])),
        forbidden_inferences=tuple(
            copy.deepcopy(obligations["forbidden_inferences"])
        ),
    )


def public_fixture_to_dict(fixture: PublicFixture) -> dict[str, Any]:
    return {
        "fixture_id": fixture.fixture_id,
        "split": fixture.split,
        "family": fixture.family,
        "request": fixture.request,
        "initial_state": copy.deepcopy(fixture.initial_state),
        "evidence": copy.deepcopy(list(fixture.evidence)),
        "policy_constraints": {
            "editable_paths": list(fixture.editable_paths),
            "immutable_paths": list(fixture.immutable_paths),
            "on_block_preserve_paths": list(fixture.on_block_preserve_paths),
            "unknown_state": list(fixture.unknown_state),
            "forbidden_inferences": list(fixture.forbidden_inferences),
        },
    }


def contract_to_dict(contract: DerivedContract) -> dict[str, Any]:
    return {
        "contract_id": contract.contract_id,
        "split": contract.split,
        "family": contract.family,
        "task_id": contract.task_id,
        "initial_state": copy.deepcopy(contract.initial_state),
        "expected_decision": contract.expected_decision,
        "desired_patch": copy.deepcopy(list(contract.desired_patch)),
        "editable_paths": sorted(contract.editable_paths),
        "immutable_paths": sorted(contract.immutable_paths),
        "required_preserved_state": copy.deepcopy(
            list(contract.required_preserved_state)
        ),
        "required_evidence_ids": sorted(contract.required_evidence_ids),
        "required_unknown_state": sorted(contract.required_unknown_state),
        "forbidden_inferences": sorted(contract.forbidden_inferences),
        "expected_gate": copy.deepcopy(contract.expected_gate),
        "expected_next_action": contract.expected_next_action,
    }


def forbidden_paths(value: Any, prefix: str = "$") -> list[str]:
    """Return any forbidden key paths remaining after projection."""
    found: list[str] = []
    if isinstance(value, Mapping):
        for key, item in value.items():
            child = f"{prefix}.{key}"
            if str(key).lower() in FORBIDDEN_INPUT_KEYS:
                found.append(child)
            found.extend(forbidden_paths(item, child))
    elif isinstance(value, (list, tuple)):
        for index, item in enumerate(value):
            found.extend(forbidden_paths(item, f"{prefix}[{index}]"))
    return found
