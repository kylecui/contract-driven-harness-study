"""Derive executable contracts from explicitly bounded public policy inputs.

This module is intentionally pure: it performs no file, environment, network,
or process access.  Family rules are generic and contain no fixture-specific
branches.  Callers must construct :class:`PublicFixture` through an audited
projection boundary before invoking :func:`compile_contract`.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

from policy_rules import BLOCK_ACTIONS, FAMILY_POLICIES


class CompilationError(ValueError):
    """Raised when public inputs do not define a deterministic policy decision."""


@dataclass(frozen=True)
class PublicFixture:
    fixture_id: str
    split: str
    family: str
    request: str
    initial_state: dict[str, Any]
    evidence: tuple[dict[str, Any], ...]
    editable_paths: tuple[str, ...]
    immutable_paths: tuple[str, ...]
    on_block_preserve_paths: tuple[str, ...]
    unknown_state: tuple[str, ...]
    forbidden_inferences: tuple[str, ...]


@dataclass(frozen=True)
class DerivedContract:
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


@dataclass(frozen=True)
class Intent:
    target: str
    current_value: Any
    requested_value: Any


@dataclass(frozen=True)
class Outcome:
    decision: str
    reason: str
    evidence_ids: tuple[str, ...]


_ATOM = r"(?:\[[^\]]*\]|true|false|-?\d+(?:\.\d+)?|[A-Za-z0-9_.@-]+)"
_ARROW = re.compile(rf"(?P<left>{_ATOM})\s*->\s*(?P<right>{_ATOM})", re.IGNORECASE)
_FROM_TO = re.compile(
    rf"\bfrom\s+(?P<left>{_ATOM})\s+to\s+(?P<right>{_ATOM})",
    re.IGNORECASE,
)
_ENTITY = re.compile(
    r"\b(project|issue|ticket|review|case|alert|release|dataset|incident)\s+"
    r"([A-Za-z0-9-]+)\b",
    re.IGNORECASE,
)
_EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")


def _parse_atom(text: str) -> Any:
    value = text.strip().rstrip(".,")
    lower = value.lower()
    if lower == "true":
        return True
    if lower == "false":
        return False
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    if re.fullmatch(r"-?\d+\.\d+", value):
        return float(value)
    if value.startswith("[") and value.endswith("]"):
        body = value[1:-1].strip()
        return [] if not body else [_parse_atom(item.strip()) for item in body.split(",")]
    return value


def _arrow_values(text: str) -> tuple[Any, Any] | None:
    match = _ARROW.search(text)
    if match is None:
        return None
    return _parse_atom(match.group("left")), _parse_atom(match.group("right"))


def _request_values(text: str) -> tuple[Any | None, Any]:
    match = _FROM_TO.search(text)
    if match is not None:
        return _parse_atom(match.group("left")), _parse_atom(match.group("right"))
    enable = re.match(r"\s*Enable\b", text, re.IGNORECASE)
    if enable is not None:
        return None, True
    disable = re.match(r"\s*Disable\b", text, re.IGNORECASE)
    if disable is not None:
        return None, False
    addition = re.match(r"\s*Add\s+(\S+)\s+to\b", text, re.IGNORECASE)
    if addition is not None:
        return None, ("append", _parse_atom(addition.group(1)))
    for pattern in (
        r"\bas\s+([A-Za-z0-9_.-]+)\b",
        r"\bto\s+([A-Za-z0-9_.-]+)\b",
    ):
        match = re.search(pattern, text, re.IGNORECASE)
        if match is not None:
            return None, _parse_atom(match.group(1))
    if re.match(r"\s*Resolve\b", text, re.IGNORECASE):
        return None, "resolved"
    if re.match(r"\s*Close\b", text, re.IGNORECASE):
        return None, "closed"
    raise CompilationError("request does not expose a supported transition")


def _single_editable(fixture: PublicFixture) -> tuple[str, Any]:
    if len(fixture.editable_paths) != 1:
        raise CompilationError("exactly one editable path is required")
    path = fixture.editable_paths[0]
    if path not in fixture.initial_state:
        raise CompilationError("editable path is absent from current state")
    return path, fixture.initial_state[path]


def _validate_fixture(fixture: PublicFixture) -> None:
    if fixture.family not in FAMILY_POLICIES:
        raise CompilationError("unsupported family")
    if not fixture.fixture_id or not fixture.request:
        raise CompilationError("task identity and request are required")
    editable = set(fixture.editable_paths)
    immutable = set(fixture.immutable_paths)
    if editable & immutable:
        raise CompilationError("editable and immutable paths overlap")
    _single_editable(fixture)
    missing = (editable | immutable | set(fixture.on_block_preserve_paths)) - set(
        fixture.initial_state
    )
    if missing:
        raise CompilationError("policy paths are absent from current state")
    identifiers = [str(item.get("evidence_id", "")) for item in fixture.evidence]
    if any(not item for item in identifiers) or len(identifiers) != len(set(identifiers)):
        raise CompilationError("evidence identifiers must be non-empty and unique")


def _controlled_intent(fixture: PublicFixture) -> Intent:
    _, current = _single_editable(fixture)
    entity = _ENTITY.search(fixture.request)
    if entity is None:
        raise CompilationError("controlled transition request has no target identity")
    target = f"{entity.group(1).lower()}-{entity.group(2).lower()}"
    stated_from, requested = _request_values(fixture.request)
    if stated_from is not None and stated_from != current:
        return Intent(target, current, ("from_mismatch", requested))
    return Intent(target, current, requested)


def _configuration_target(request: str) -> str:
    patterns = (
        r"\s*(?:Change|Raise)\s+([A-Za-z0-9-]+)\b",
        r"\s*Enable\s+\S+\s+for\s+([A-Za-z0-9-]+)\b",
        r"\s*Disable\s+.+?\s+for\s+([A-Za-z0-9-]+)\b",
        r"\s*Add\s+\S+\s+to\s+([A-Za-z0-9-]+)\b",
        r"\s*Set\s+([A-Za-z0-9-]+)\b",
    )
    for pattern in patterns:
        match = re.match(pattern, request, re.IGNORECASE)
        if match is not None:
            return match.group(1).lower()
    raise CompilationError("configuration request has no target identity")


def _configuration_intent(fixture: PublicFixture) -> Intent:
    _, current = _single_editable(fixture)
    stated_from, requested = _request_values(fixture.request)
    if isinstance(requested, tuple) and requested[0] == "append":
        if not isinstance(current, list):
            raise CompilationError("append intent requires a list-valued current state")
        requested = list(current) + [requested[1]]
    if stated_from is not None and stated_from != current:
        return Intent(_configuration_target(fixture.request), current, ("from_mismatch", requested))
    return Intent(_configuration_target(fixture.request), current, requested)


def _communication_intent(fixture: PublicFixture) -> Intent:
    path, current = _single_editable(fixture)
    if path != "message.status":
        raise CompilationError("communication policy requires the message status path")
    email = _EMAIL.search(fixture.request)
    scope = fixture.initial_state.get("message.classification")
    recipient = fixture.initial_state.get("message.recipient")
    if email is None or not isinstance(scope, str) or not isinstance(recipient, str):
        raise CompilationError("communication request lacks recipient or classification")
    if email.group(0).lower() != recipient.lower():
        raise CompilationError("request recipient disagrees with current message recipient")
    target = f"{recipient.lower()}|{scope.lower()}"
    return Intent(target, current, "queued")


def _controlled_outcome(fixture: PublicFixture, intent: Intent) -> Outcome:
    policy = FAMILY_POLICIES[fixture.family]
    records = [item for item in fixture.evidence if item.get("type") == policy.authority_type]
    all_ids = tuple(str(item["evidence_id"]) for item in records)
    if not records:
        return Outcome("block", "missing_authoritative_evidence", ())
    if isinstance(intent.requested_value, tuple) and intent.requested_value[0] == "from_mismatch":
        return Outcome("block", "request_from_state_mismatch", all_ids)
    target_records = [item for item in records if str(item.get("target", "")).lower() == intent.target]
    if not target_records:
        return Outcome("block", "target_mismatch", all_ids)
    parsed = [(item, _arrow_values(str(item.get("claim", "")))) for item in target_records]
    if any(values is None for _, values in parsed):
        return Outcome(
            "block",
            "malformed_authoritative_evidence",
            tuple(str(item["evidence_id"]) for item in target_records),
        )
    from_records = [
        (item, values)
        for item, values in parsed
        if values is not None and values[0] == intent.current_value
    ]
    if not from_records:
        return Outcome(
            "block",
            "from_state_mismatch",
            tuple(str(item["evidence_id"]) for item in target_records),
        )
    destinations = {repr(values[1]) for _, values in from_records}
    if len(destinations) > 1:
        return Outcome(
            "block",
            "conflicting_authoritative_evidence",
            tuple(str(item["evidence_id"]) for item, _ in from_records),
        )
    matching = [
        item for item, values in from_records if values[1] == intent.requested_value
    ]
    if not matching:
        return Outcome(
            "block",
            "to_state_mismatch",
            tuple(str(item["evidence_id"]) for item, _ in from_records),
        )
    return Outcome(
        "apply",
        policy.open_reason,
        tuple(str(item["evidence_id"]) for item in matching),
    )


def _configuration_outcome(fixture: PublicFixture, intent: Intent) -> Outcome:
    policy = FAMILY_POLICIES[fixture.family]
    approvals = [item for item in fixture.evidence if item.get("type") == policy.authority_type]
    all_ids = tuple(str(item["evidence_id"]) for item in approvals)
    if not approvals:
        return Outcome("block", "missing_valid_approval", ())
    if isinstance(intent.requested_value, tuple) and intent.requested_value[0] == "from_mismatch":
        return Outcome("block", "request_from_state_mismatch", all_ids)
    target = [item for item in approvals if str(item.get("target", "")).lower() == intent.target]
    if not target:
        return Outcome("block", "approval_target_mismatch", all_ids)
    path = fixture.editable_paths[0]
    scoped = [item for item in target if item.get("scope") == path]
    if not scoped:
        return Outcome(
            "block", "approval_scope_mismatch", tuple(str(item["evidence_id"]) for item in target)
        )
    parsed = [(item, _arrow_values(str(item.get("claim", "")))) for item in scoped]
    matching_values = [
        item
        for item, values in parsed
        if values is not None
        and values[0] == intent.current_value
        and values[1] == intent.requested_value
    ]
    if not matching_values:
        return Outcome(
            "block", "approval_value_mismatch", tuple(str(item["evidence_id"]) for item in scoped)
        )
    valid = [item for item in matching_values if item.get("status") == "valid"]
    if not valid:
        statuses = {str(item.get("status", "")) for item in matching_values}
        reason = "approval_expired" if "expired" in statuses else "approval_revoked"
        return Outcome(
            "block", reason, tuple(str(item["evidence_id"]) for item in matching_values)
        )
    revocations = [
        item
        for item in fixture.evidence
        if item.get("type") == "approval_revocation"
        and item.get("status") == "active"
        and str(item.get("target", "")).lower() == intent.target
        and item.get("scope") == path
        and any(str(approval["evidence_id"]) in str(item.get("claim", "")) for approval in valid)
    ]
    if revocations:
        return Outcome(
            "block",
            "approval_revoked",
            tuple(str(item["evidence_id"]) for item in valid + revocations),
        )
    return Outcome(
        "apply", policy.open_reason, tuple(str(item["evidence_id"]) for item in valid)
    )


def _communication_outcome(fixture: PublicFixture, intent: Intent) -> Outcome:
    policy = FAMILY_POLICIES[fixture.family]
    approvals = [item for item in fixture.evidence if item.get("type") == policy.authority_type]
    all_ids = tuple(str(item["evidence_id"]) for item in approvals)
    if not approvals:
        return Outcome("block", "missing_communication_approval", ())
    recipient, scope = intent.target.split("|", 1)
    recipient_matches = [
        item for item in approvals if str(item.get("recipient", "")).lower() == recipient
    ]
    if not recipient_matches:
        return Outcome("block", "communication_recipient_mismatch", all_ids)
    scoped = [item for item in recipient_matches if str(item.get("scope", "")).lower() == scope]
    if not scoped:
        return Outcome(
            "block",
            "communication_scope_mismatch",
            tuple(str(item["evidence_id"]) for item in recipient_matches),
        )
    expired = [item for item in scoped if item.get("status") == "expired"]
    if expired:
        return Outcome(
            "block",
            "communication_approval_expired",
            tuple(str(item["evidence_id"]) for item in expired),
        )
    revoked = [item for item in scoped if item.get("status") == "revoked"]
    if revoked:
        return Outcome(
            "block",
            "communication_approval_revoked",
            tuple(str(item["evidence_id"]) for item in revoked),
        )
    transition = [
        item
        for item in scoped
        if item.get("status") == "valid"
        and _arrow_values(str(item.get("claim", "")))
        == (intent.current_value, intent.requested_value)
    ]
    if not transition:
        return Outcome(
            "block",
            "communication_transition_mismatch",
            tuple(str(item["evidence_id"]) for item in scoped),
        )
    return Outcome(
        "apply", policy.open_reason, tuple(str(item["evidence_id"]) for item in transition)
    )


def _intent_and_outcome(fixture: PublicFixture) -> tuple[Intent, Outcome]:
    if fixture.family == "controlled_state_transition":
        intent = _controlled_intent(fixture)
        return intent, _controlled_outcome(fixture, intent)
    if fixture.family == "approval_gated_configuration":
        intent = _configuration_intent(fixture)
        return intent, _configuration_outcome(fixture, intent)
    if fixture.family == "approval_gated_communication":
        intent = _communication_intent(fixture)
        return intent, _communication_outcome(fixture, intent)
    raise CompilationError("unsupported family")


def compile_contract(fixture: PublicFixture) -> DerivedContract:
    """Compile a deterministic contract from the bounded input object."""
    _validate_fixture(fixture)
    path, current = _single_editable(fixture)
    intent, outcome = _intent_and_outcome(fixture)
    policy = FAMILY_POLICIES[fixture.family]
    apply = outcome.decision == "apply"
    desired_patch = (
        ({
            "path": path,
            "from": current,
            "to": intent.requested_value,
            "evidence_ids": list(outcome.evidence_ids),
        },)
        if apply
        else ()
    )
    preserved_paths = fixture.immutable_paths if apply else fixture.on_block_preserve_paths
    preserved = tuple(
        {"path": item, "value": fixture.initial_state[item]}
        for item in sorted(preserved_paths)
    )
    gate = {
        "status": "open" if apply else "blocked",
        "reason_code": outcome.reason,
        "permitted_action": policy.permitted_action if apply else "none",
    }
    next_action = policy.apply_action if apply else BLOCK_ACTIONS[outcome.reason]
    return DerivedContract(
        contract_id=f"OIC-v1::{fixture.fixture_id}",
        split=fixture.split,
        family=fixture.family,
        task_id=fixture.fixture_id,
        initial_state=dict(fixture.initial_state),
        expected_decision=outcome.decision,
        desired_patch=desired_patch,
        editable_paths=frozenset(fixture.editable_paths),
        immutable_paths=frozenset(fixture.immutable_paths),
        required_preserved_state=preserved,
        required_evidence_ids=frozenset(outcome.evidence_ids),
        required_unknown_state=frozenset(fixture.unknown_state),
        forbidden_inferences=frozenset(fixture.forbidden_inferences),
        expected_gate=gate,
        expected_next_action=next_action,
    )


def canonical_candidate(contract: DerivedContract) -> dict[str, Any]:
    """Materialize the canonical proposal that satisfies a derived contract."""
    return {
        "task_id": contract.task_id,
        "decision": contract.expected_decision,
        "state_patch": [dict(item) for item in contract.desired_patch],
        "preserved_state": [dict(item) for item in contract.required_preserved_state],
        "evidence_bindings": [{
            "slot_id": "decision",
            "evidence_ids": sorted(contract.required_evidence_ids),
        }],
        "unknown_state": sorted(contract.required_unknown_state),
        "forbidden_inferences": sorted(contract.forbidden_inferences),
        "gate": dict(contract.expected_gate),
        "next_action": contract.expected_next_action,
    }
