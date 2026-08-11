"""Reference implementation of a failure-derived executable contract gate.

The language model is deliberately outside the trusted computing base.  It may
propose a candidate transition, but only this deterministic gate may mutate the
sandbox state.  The implementation is intentionally small enough to audit.
"""

from __future__ import annotations

import copy
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


REQUIRED_FIELDS = {
    "task_id",
    "decision",
    "state_patch",
    "preserved_state",
    "evidence_bindings",
    "unknown_state",
    "forbidden_inferences",
    "gate",
    "next_action",
}


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class ExecutableContract:
    contract_id: str
    split: str
    family: str
    task_id: str
    initial_state: dict[str, Any]
    expected_decision: str
    desired_patch: tuple[dict[str, Any], ...]
    editable_paths: frozenset[str]
    immutable_paths: frozenset[str]
    required_preserved_state: tuple[dict[str, Any], ...]
    required_evidence_ids: frozenset[str]
    required_unknown_state: frozenset[str]
    forbidden_inferences: frozenset[str]
    expected_gate: dict[str, Any]
    expected_next_action: str

    @classmethod
    def compile(cls, fixture: dict[str, Any]) -> "ExecutableContract":
        """Compile an authored fixture into an executable, model-independent gate.

        The expected output is the frozen semantic oracle for this benchmark.  It
        is not generated from a model response.  Production use would author the
        same fields directly in a contract DSL.
        """
        expected = fixture["expected_output"]
        obligations = fixture["obligations"]
        binding = next(
            item for item in expected["evidence_bindings"] if item["slot_id"] == "decision"
        )
        return cls(
            contract_id=f"FEC-v2::{fixture['fixture_id']}",
            split=fixture["split"],
            family=fixture["family"],
            task_id=fixture["fixture_id"],
            initial_state=copy.deepcopy(fixture["initial_state"]),
            expected_decision=expected["decision"],
            desired_patch=tuple(copy.deepcopy(expected["state_patch"])),
            editable_paths=frozenset(obligations["editable_paths"]),
            immutable_paths=frozenset(obligations["immutable_paths"]),
            required_preserved_state=tuple(copy.deepcopy(expected["preserved_state"])),
            required_evidence_ids=frozenset(binding["evidence_ids"]),
            required_unknown_state=frozenset(obligations["unknown_state"]),
            forbidden_inferences=frozenset(obligations["forbidden_inferences"]),
            expected_gate=copy.deepcopy(expected["gate"]),
            expected_next_action=expected["next_action"],
        )


@dataclass(frozen=True)
class GateDecision:
    accepted: bool
    reason_codes: tuple[str, ...]


def _is_list_of_dicts(value: Any) -> bool:
    return isinstance(value, list) and all(isinstance(item, dict) for item in value)


def schema_gate(candidate: Any) -> GateDecision:
    reasons: list[str] = []
    if not isinstance(candidate, dict):
        return GateDecision(False, ("not_an_object",))
    missing = sorted(REQUIRED_FIELDS - set(candidate))
    extra = sorted(set(candidate) - REQUIRED_FIELDS)
    if missing:
        reasons.append("missing_fields:" + ",".join(missing))
    if extra:
        reasons.append("unexpected_fields:" + ",".join(extra))
    if candidate.get("decision") not in {"apply", "block"}:
        reasons.append("invalid_decision_enum")
    for field in ("state_patch", "preserved_state", "evidence_bindings"):
        if not _is_list_of_dicts(candidate.get(field)):
            reasons.append(f"invalid_{field}_shape")
    for field in ("unknown_state", "forbidden_inferences"):
        if not isinstance(candidate.get(field), list) or not all(
            isinstance(item, str) for item in candidate.get(field, [])
        ):
            reasons.append(f"invalid_{field}_shape")
    if not isinstance(candidate.get("gate"), dict):
        reasons.append("invalid_gate_shape")
    return GateDecision(not reasons, tuple(reasons))


def executable_gate(contract: ExecutableContract, candidate: Any) -> GateDecision:
    shape = schema_gate(candidate)
    if not shape.accepted:
        return shape

    reasons: list[str] = []
    if candidate["task_id"] != contract.task_id:
        reasons.append("task_identity_mismatch")
    if candidate["decision"] != contract.expected_decision:
        reasons.append("decision_mismatch")

    patches = candidate["state_patch"]
    desired_by_path = {item["path"]: item for item in contract.desired_patch}
    seen_paths: set[str] = set()
    for patch in patches:
        path = patch.get("path")
        seen_paths.add(path)
        if path not in contract.editable_paths:
            reasons.append("unauthorized_write_path")
            continue
        if path not in desired_by_path:
            reasons.append("unrequested_write")
            continue
        desired = desired_by_path[path]
        if patch.get("from") != contract.initial_state.get(path):
            reasons.append("stale_or_fabricated_from_state")
        if patch.get("to") != desired.get("to"):
            reasons.append("wrong_target_state")
        if set(patch.get("evidence_ids", [])) != set(desired.get("evidence_ids", [])):
            reasons.append("patch_evidence_mismatch")

    if contract.expected_decision == "apply":
        if seen_paths != set(desired_by_path):
            reasons.append("incomplete_requested_patch")
    elif patches:
        reasons.append("write_attempt_under_block_decision")

    preserved = {item.get("path"): item.get("value") for item in candidate["preserved_state"]}
    expected_preserved = {
        item["path"]: item["value"] for item in contract.required_preserved_state
    }
    if preserved != expected_preserved:
        reasons.append("preserved_state_mismatch")
    if set(preserved) & contract.editable_paths and contract.expected_decision == "apply":
        reasons.append("edited_path_reported_as_preserved")

    decision_bindings = [
        item for item in candidate["evidence_bindings"] if item.get("slot_id") == "decision"
    ]
    if len(decision_bindings) != 1:
        reasons.append("decision_binding_cardinality")
    elif set(decision_bindings[0].get("evidence_ids", [])) != contract.required_evidence_ids:
        reasons.append("decision_evidence_mismatch")

    if set(candidate["unknown_state"]) != contract.required_unknown_state:
        reasons.append("unknown_state_not_preserved")
    if set(candidate["forbidden_inferences"]) != contract.forbidden_inferences:
        reasons.append("forbidden_inference_boundary_changed")
    if candidate["gate"] != contract.expected_gate:
        reasons.append("gate_attestation_mismatch")
    if candidate["next_action"] != contract.expected_next_action:
        reasons.append("next_action_mismatch")

    return GateDecision(not reasons, tuple(dict.fromkeys(reasons)))


def apply_patch_to_state(state: dict[str, Any], patches: Iterable[dict[str, Any]]) -> dict[str, Any]:
    next_state = copy.deepcopy(state)
    for patch in patches:
        next_state[patch["path"]] = patch["to"]
    return next_state


def execute_in_sandbox(
    contract: ExecutableContract,
    candidate: Any,
    state_path: Path,
) -> dict[str, Any]:
    """Validate before the only write point and return an auditable trace."""
    before = json.loads(state_path.read_text(encoding="utf-8"))
    before_hash = digest(before)
    decision = executable_gate(contract, candidate)
    wrote = False
    if decision.accepted and candidate["decision"] == "apply":
        after = apply_patch_to_state(before, candidate["state_patch"])
        state_path.write_text(
            json.dumps(after, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        wrote = True
    after = json.loads(state_path.read_text(encoding="utf-8"))
    return {
        "contract_id": contract.contract_id,
        "accepted": decision.accepted,
        "reason_codes": list(decision.reason_codes),
        "wrote": wrote,
        "before_hash": before_hash,
        "after_hash": digest(after),
        "state_integrity_preserved": decision.accepted or before_hash == digest(after),
    }
