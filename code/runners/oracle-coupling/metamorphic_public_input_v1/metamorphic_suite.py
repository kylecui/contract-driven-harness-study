"""Deterministic metamorphic tests over the OIC-v1 public-input boundary.

The module transforms only the scrubbed request, state, evidence, and policy-
constraint representation emitted by ``oracle_independent_compiler_v1``.  It
does not load the original authored fixture file.  All transformations are
pure and deterministic; file access belongs to the experiment runner.
"""

from __future__ import annotations

import copy
import hashlib
import json
import re
from collections import Counter
from dataclasses import dataclass
from typing import Any, Callable

from public_input import contract_to_dict, project_public_fixture
from public_policy_compiler import compile_contract


FAMILY_CONTROLLED = "controlled_state_transition"
FAMILY_CONFIGURATION = "approval_gated_configuration"
FAMILY_COMMUNICATION = "approval_gated_communication"

SUPPORTED_FAMILIES = (
    FAMILY_CONTROLLED,
    FAMILY_CONFIGURATION,
    FAMILY_COMMUNICATION,
)

AUTHORITY_TYPE = {
    FAMILY_CONTROLLED: "authoritative_transition",
    FAMILY_CONFIGURATION: "approval_record",
    FAMILY_COMMUNICATION: "communication_approval",
}

MISSING_REASON = {
    FAMILY_CONTROLLED: "missing_authoritative_evidence",
    FAMILY_CONFIGURATION: "missing_valid_approval",
    FAMILY_COMMUNICATION: "missing_communication_approval",
}

TARGET_REASON = {
    FAMILY_CONTROLLED: "target_mismatch",
    FAMILY_CONFIGURATION: "approval_target_mismatch",
    FAMILY_COMMUNICATION: "communication_recipient_mismatch",
}

SCOPE_REASON = {
    FAMILY_CONFIGURATION: "approval_scope_mismatch",
    FAMILY_COMMUNICATION: "communication_scope_mismatch",
}

EXPIRY_REASON = {
    FAMILY_CONFIGURATION: "approval_expired",
    FAMILY_COMMUNICATION: "communication_approval_expired",
}

DESTINATION_REASON = {
    FAMILY_CONTROLLED: "to_state_mismatch",
    FAMILY_CONFIGURATION: "approval_value_mismatch",
    FAMILY_COMMUNICATION: "communication_transition_mismatch",
}

EXPECTED_BLOCK_ACTION = {
    "missing_authoritative_evidence": "request_authoritative_transition_evidence",
    "target_mismatch": "request_target_matching_evidence",
    "to_state_mismatch": "request_transition_matching_evidence",
    "missing_valid_approval": "request_valid_scoped_approval",
    "approval_target_mismatch": "request_target_matching_approval",
    "approval_scope_mismatch": "request_scope_matching_approval",
    "approval_expired": "request_fresh_approval",
    "approval_value_mismatch": "request_value_matching_approval",
    "missing_communication_approval": "request_authoritative_communication_approval",
    "communication_recipient_mismatch": "request_recipient_scoped_approval",
    "communication_scope_mismatch": "request_classification_scoped_approval",
    "communication_approval_expired": "request_fresh_communication_approval",
    "communication_transition_mismatch": "request_transition_scoped_communication_approval",
}

INVARIANT_TRANSFORMS = (
    "rename_domain_identifiers",
    "rename_evidence_identifiers",
    "insert_irrelevant_evidence",
    "compose_invariant_transforms",
)

_ENTITY = re.compile(
    r"\b(project|issue|ticket|review|case|alert|release|dataset|incident)\s+"
    r"([A-Za-z0-9-]+)\b",
    re.IGNORECASE,
)
_EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
_CONFIG_TARGETS = (
    re.compile(r"\s*(?:Change|Raise)\s+([A-Za-z0-9-]+)\b", re.IGNORECASE),
    re.compile(r"\s*Enable\s+\S+\s+for\s+([A-Za-z0-9-]+)\b", re.IGNORECASE),
    re.compile(r"\s*Disable\s+.+?\s+for\s+([A-Za-z0-9-]+)\b", re.IGNORECASE),
    re.compile(r"\s*Add\s+\S+\s+to\s+([A-Za-z0-9-]+)\b", re.IGNORECASE),
    re.compile(r"\s*Set\s+([A-Za-z0-9-]+)\b", re.IGNORECASE),
)
_ARROW_DESTINATION = re.compile(
    r"(?P<prefix>(?:\[[^\]]*\]|true|false|-?\d+(?:\.\d+)?|[A-Za-z0-9_.@-]+)"
    r"\s*->\s*)"
    r"(?P<right>\[[^\]]*\]|true|false|-?\d+(?:\.\d+)?|[A-Za-z0-9_.@-]+)",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class TransformResult:
    fixture: dict[str, Any]
    evidence_id_mapping: dict[str, str]
    domain_identifier_mapping: dict[str, str]

    @property
    def reverse_output_mapping(self) -> dict[str, str]:
        forward = {**self.domain_identifier_mapping, **self.evidence_id_mapping}
        return {new: old for old, new in forward.items()}


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def fixture_from_public_record(record: dict[str, Any]) -> dict[str, Any]:
    """Adapt one scrubbed OIC artifact record to the projection API."""
    required = {
        "fixture_id",
        "split",
        "family",
        "request",
        "initial_state",
        "evidence",
        "policy_constraints",
    }
    require(required == set(record), "public record shape is not exact")
    return {
        "fixture_id": record["fixture_id"],
        "split": record["split"],
        "family": record["family"],
        "request": copy.deepcopy(record["request"]),
        "initial_state": copy.deepcopy(record["initial_state"]),
        "evidence": copy.deepcopy(record["evidence"]),
        "obligations": copy.deepcopy(record["policy_constraints"]),
    }


def _replace_exact_strings(value: Any, reverse_mapping: dict[str, str]) -> Any:
    if isinstance(value, dict):
        return {
            key: _replace_exact_strings(item, reverse_mapping)
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [_replace_exact_strings(item, reverse_mapping) for item in value]
    if isinstance(value, str):
        return reverse_mapping.get(value, value)
    return value


def normalized_contract(fixture: dict[str, Any], reverse_mapping: dict[str, str]) -> dict[str, Any]:
    contract = contract_to_dict(compile_contract(project_public_fixture(fixture)))
    return _replace_exact_strings(contract, reverse_mapping)


def baseline_contract(fixture: dict[str, Any]) -> dict[str, Any]:
    return normalized_contract(fixture, {})


def _config_request_target(request: str) -> str:
    for pattern in _CONFIG_TARGETS:
        match = pattern.match(request)
        if match is not None:
            return match.group(1)
    raise ValueError("configuration request target is not recognized")


def _domain_identifiers(fixture: dict[str, Any]) -> tuple[str, list[str]]:
    family = fixture["family"]
    if family == FAMILY_CONTROLLED:
        match = _ENTITY.search(fixture["request"])
        require(match is not None, "controlled request target is absent")
        request_identifier = f"{match.group(1).lower()}-{match.group(2).lower()}"
        evidence_identifiers = [
            str(item["target"]).lower()
            for item in fixture["evidence"]
            if "target" in item
        ]
        return request_identifier, evidence_identifiers
    if family == FAMILY_CONFIGURATION:
        request_identifier = _config_request_target(fixture["request"]).lower()
        evidence_identifiers = [
            str(item["target"]).lower()
            for item in fixture["evidence"]
            if "target" in item
        ]
        return request_identifier, evidence_identifiers
    if family == FAMILY_COMMUNICATION:
        match = _EMAIL.search(fixture["request"])
        require(match is not None, "communication request recipient is absent")
        request_identifier = match.group(0).lower()
        evidence_identifiers = [
            str(item["recipient"]).lower()
            for item in fixture["evidence"]
            if "recipient" in item
        ]
        return request_identifier, evidence_identifiers
    raise ValueError("unsupported family")


def rename_domain_identifiers(fixture: dict[str, Any]) -> TransformResult:
    """Apply a bijective rename while preserving equality and inequality relations."""
    value = copy.deepcopy(fixture)
    family = value["family"]
    request_identifier, evidence_identifiers = _domain_identifiers(value)
    identifiers = sorted(set([request_identifier, *evidence_identifiers]))
    require(bool(identifiers), "domain identifier set is empty")

    if family == FAMILY_CONTROLLED:
        forward = {
            old: f"{old.split('-', 1)[0]}-m{index:04d}"
            for index, old in enumerate(identifiers, 1)
        }
        match = _ENTITY.search(value["request"])
        require(match is not None, "controlled request target is absent")
        replacement = forward[request_identifier].split("-", 1)[1]
        start, end = match.span(2)
        value["request"] = value["request"][:start] + replacement + value["request"][end:]
        for item in value["evidence"]:
            if "target" in item:
                item["target"] = forward[str(item["target"]).lower()]
    elif family == FAMILY_CONFIGURATION:
        forward = {
            old: f"resource-m{index:04d}"
            for index, old in enumerate(identifiers, 1)
        }
        pattern_match = None
        for pattern in _CONFIG_TARGETS:
            pattern_match = pattern.match(value["request"])
            if pattern_match is not None:
                break
        require(pattern_match is not None, "configuration request target is absent")
        start, end = pattern_match.span(1)
        value["request"] = (
            value["request"][:start]
            + forward[request_identifier]
            + value["request"][end:]
        )
        for item in value["evidence"]:
            if "target" in item:
                item["target"] = forward[str(item["target"]).lower()]
    elif family == FAMILY_COMMUNICATION:
        forward = {
            old: f"recipient{index:02d}@metamorphic.invalid"
            for index, old in enumerate(identifiers, 1)
        }
        match = _EMAIL.search(value["request"])
        require(match is not None, "communication request recipient is absent")
        value["request"] = (
            value["request"][:match.start()]
            + forward[request_identifier]
            + value["request"][match.end():]
        )
        state_recipient = str(value["initial_state"]["message.recipient"]).lower()
        require(state_recipient in forward, "state recipient is absent from rename mapping")
        value["initial_state"]["message.recipient"] = forward[state_recipient]
        for item in value["evidence"]:
            if "recipient" in item:
                item["recipient"] = forward[str(item["recipient"]).lower()]
    else:
        raise ValueError("unsupported family")

    require(len(set(forward.values())) == len(forward), "domain rename is not bijective")
    require(not (set(forward) & set(forward.values())), "domain rename collides with an old identifier")
    return TransformResult(value, {}, forward)


def _replace_substrings(value: Any, mapping: dict[str, str]) -> Any:
    if isinstance(value, dict):
        return {key: _replace_substrings(item, mapping) for key, item in value.items()}
    if isinstance(value, list):
        return [_replace_substrings(item, mapping) for item in value]
    if isinstance(value, str):
        result = value
        for old in sorted(mapping, key=len, reverse=True):
            result = result.replace(old, mapping[old])
        return result
    return value


def rename_evidence_identifiers(fixture: dict[str, Any]) -> TransformResult:
    value = copy.deepcopy(fixture)
    original_ids = [str(item["evidence_id"]) for item in value["evidence"]]
    require(len(original_ids) == len(set(original_ids)), "evidence identifiers are not unique")
    stem = re.sub(r"[^A-Za-z0-9]", "", value["fixture_id"])
    forward = {
        old: f"MVID-{stem}-{index:02d}"
        for index, old in enumerate(original_ids, 1)
    }
    value["evidence"] = _replace_substrings(value["evidence"], forward)
    require(len(set(forward.values())) == len(forward), "evidence-ID rename is not bijective")
    require(not (set(forward) & set(forward.values())), "evidence-ID rename collides with an old identifier")
    return TransformResult(value, forward, {})


def insert_irrelevant_evidence(fixture: dict[str, Any]) -> TransformResult:
    value = copy.deepcopy(fixture)
    value["evidence"].insert(0, {
        "evidence_id": f"META-DISTRACTOR-{value['fixture_id']}",
        "type": "metamorphic_irrelevant_note",
        "target": "unrelated-resource",
        "recipient": "unrelated@metamorphic.invalid",
        "scope": "unrelated.scope",
        "status": "valid",
        "claim": "This record carries no authority in any registered family.",
        "metadata": {"rank": 1, "source": "deterministic_metamorphic_probe"},
    })
    return TransformResult(value, {}, {})


def insert_irrelevant_metadata(fixture: dict[str, Any]) -> TransformResult:
    value = copy.deepcopy(fixture)
    for index, item in enumerate(value["evidence"], 1):
        item["metamorphic_metadata"] = {
            "ordinal": index,
            "annotation": "ignored_unregistered_metadata",
        }
    return TransformResult(value, {}, {})


def compose_invariant_transforms(fixture: dict[str, Any]) -> TransformResult:
    domain = rename_domain_identifiers(fixture)
    evidence = rename_evidence_identifiers(domain.fixture)
    distractor = insert_irrelevant_evidence(evidence.fixture)
    metadata = insert_irrelevant_metadata(distractor.fixture)
    return TransformResult(
        metadata.fixture,
        evidence.evidence_id_mapping,
        domain.domain_identifier_mapping,
    )


INVARIANT_FUNCTIONS: dict[str, Callable[[dict[str, Any]], TransformResult]] = {
    "rename_domain_identifiers": rename_domain_identifiers,
    "rename_evidence_identifiers": rename_evidence_identifiers,
    "insert_irrelevant_evidence": insert_irrelevant_evidence,
    "compose_invariant_transforms": compose_invariant_transforms,
}


def _authority_records(fixture: dict[str, Any]) -> list[dict[str, Any]]:
    authority_type = AUTHORITY_TYPE[fixture["family"]]
    return [item for item in fixture["evidence"] if item.get("type") == authority_type]


def remove_authority(fixture: dict[str, Any]) -> TransformResult:
    value = copy.deepcopy(fixture)
    authority_type = AUTHORITY_TYPE[value["family"]]
    value["evidence"] = [item for item in value["evidence"] if item.get("type") != authority_type]
    return TransformResult(value, {}, {})


def mismatch_authority_target(fixture: dict[str, Any]) -> TransformResult:
    value = copy.deepcopy(fixture)
    records = _authority_records(value)
    require(bool(records), "target mismatch requires authority evidence")
    for item in records:
        if value["family"] == FAMILY_COMMUNICATION:
            item["recipient"] = "mismatch@metamorphic.invalid"
        else:
            item["target"] = "metamorphic-unrelated-target"
    return TransformResult(value, {}, {})


def mismatch_authority_scope(fixture: dict[str, Any]) -> TransformResult:
    value = copy.deepcopy(fixture)
    require(value["family"] in SCOPE_REASON, "scope mismatch is not defined for this family")
    records = _authority_records(value)
    require(bool(records), "scope mismatch requires authority evidence")
    for item in records:
        item["scope"] = "metamorphic.unrelated_scope"
    return TransformResult(value, {}, {})


def expire_authority(fixture: dict[str, Any]) -> TransformResult:
    value = copy.deepcopy(fixture)
    require(value["family"] in EXPIRY_REASON, "expiry is not defined for this family")
    records = _authority_records(value)
    require(bool(records), "expiry requires authority evidence")
    for item in records:
        item["status"] = "expired"
    return TransformResult(value, {}, {})


def mismatch_authorized_destination(fixture: dict[str, Any]) -> TransformResult:
    value = copy.deepcopy(fixture)
    records = _authority_records(value)
    require(bool(records), "destination mismatch requires authority evidence")
    for item in records:
        claim = str(item.get("claim", ""))
        changed, replacements = _ARROW_DESTINATION.subn(
            lambda match: match.group("prefix") + "metamorphic_other_value",
            claim,
            count=1,
        )
        require(replacements == 1 and changed != claim, "authority claim has no replaceable destination")
        item["claim"] = changed
    return TransformResult(value, {}, {})


SENSITIVITY_FUNCTIONS: dict[str, Callable[[dict[str, Any]], TransformResult]] = {
    "remove_authority": remove_authority,
    "mismatch_authority_target": mismatch_authority_target,
    "mismatch_authority_scope": mismatch_authority_scope,
    "expire_authority": expire_authority,
    "mismatch_authorized_destination": mismatch_authorized_destination,
}


def sensitivity_plan(family: str) -> list[tuple[str, str]]:
    plan = [
        ("remove_authority", MISSING_REASON[family]),
        ("mismatch_authority_target", TARGET_REASON[family]),
        ("mismatch_authorized_destination", DESTINATION_REASON[family]),
    ]
    if family in SCOPE_REASON:
        plan.append(("mismatch_authority_scope", SCOPE_REASON[family]))
    if family in EXPIRY_REASON:
        plan.append(("expire_authority", EXPIRY_REASON[family]))
    return plan


def _string_leaves(value: Any) -> list[str]:
    if isinstance(value, dict):
        return [leaf for item in value.values() for leaf in _string_leaves(item)]
    if isinstance(value, list):
        return [leaf for item in value for leaf in _string_leaves(item)]
    return [value] if isinstance(value, str) else []


def _contract_evidence_references(contract: dict[str, Any]) -> set[str]:
    references = {str(item) for item in contract["required_evidence_ids"]}
    for patch in contract["desired_patch"]:
        references.update(str(item) for item in patch.get("evidence_ids", []))
    return references


def raw_grounding_audit(
    *,
    baseline: dict[str, Any],
    transformed: TransformResult,
    observed_raw: dict[str, Any],
) -> dict[str, Any]:
    """Reject stale identifiers hidden by semantic reverse-normalization."""
    input_ids = {str(item["evidence_id"]) for item in transformed.fixture["evidence"]}
    raw_references = _contract_evidence_references(observed_raw)
    baseline_references = _contract_evidence_references(baseline)
    raw_strings = set(_string_leaves(observed_raw))
    mapped_baseline_references = {
        old: new
        for old, new in transformed.evidence_id_mapping.items()
        if old in baseline_references
    }

    evidence_new_values_used = all(
        new in raw_references for new in mapped_baseline_references.values()
    )
    evidence_old_values_absent = all(
        old not in raw_strings for old in transformed.evidence_id_mapping
    )
    evidence_references_exist = raw_references <= input_ids
    raw_initial_state_matches = observed_raw["initial_state"] == transformed.fixture["initial_state"]

    family = transformed.fixture["family"]
    domain_old_values_absent = all(
        old not in raw_strings for old in transformed.domain_identifier_mapping
    )
    communication_recipient_check = True
    domain_output_observability = "not_emitted_by_contract_schema"
    if family == FAMILY_COMMUNICATION and transformed.domain_identifier_mapping:
        domain_output_observability = "message_recipient_emitted"
        recipient = transformed.fixture["initial_state"]["message.recipient"]
        preserved = {
            item["path"]: item["value"]
            for item in observed_raw["required_preserved_state"]
        }
        communication_recipient_check = (
            observed_raw["initial_state"].get("message.recipient") == recipient
            and preserved.get("message.recipient") == recipient
            and recipient in raw_strings
        )

    checks = {
        "input_evidence_ids_unique": len(input_ids) == len(transformed.fixture["evidence"]),
        "raw_evidence_references_exist_in_transformed_input": evidence_references_exist,
        "mapped_referenced_evidence_ids_use_new_values": evidence_new_values_used,
        "mapped_old_evidence_ids_absent_from_raw_contract": evidence_old_values_absent,
        "raw_initial_state_matches_transformed_input": raw_initial_state_matches,
        "mapped_old_domain_identifiers_absent_from_raw_contract": domain_old_values_absent,
        "communication_recipient_uses_transformed_value": communication_recipient_check,
    }
    failures = [name for name, passed in checks.items() if not passed]
    return {
        "passed": not failures,
        "checks": checks,
        "failures": failures,
        "raw_evidence_references": sorted(raw_references),
        "transformed_input_evidence_ids": sorted(input_ids),
        "evidence_id_forward_mapping": dict(sorted(transformed.evidence_id_mapping.items())),
        "domain_identifier_forward_mapping": dict(
            sorted(transformed.domain_identifier_mapping.items())
        ),
        "mapped_baseline_references": dict(sorted(mapped_baseline_references.items())),
        "domain_output_observability": domain_output_observability,
    }


def fail_closed_execution_audit(
    *,
    transformed_fixture: dict[str, Any],
    observed_raw: dict[str, Any],
    expected_reason: str,
) -> dict[str, Any]:
    """Check the complete execution-relevant block projection, not just its label."""
    require(expected_reason in EXPECTED_BLOCK_ACTION, "missing expected block action")
    obligations = transformed_fixture["obligations"]
    expected_preserved_state = [
        {"path": path, "value": transformed_fixture["initial_state"][path]}
        for path in sorted(obligations["on_block_preserve_paths"])
    ]
    expected_gate = {
        "status": "blocked",
        "reason_code": expected_reason,
        "permitted_action": "none",
    }
    raw_references = _contract_evidence_references(observed_raw)
    input_ids = {str(item["evidence_id"]) for item in transformed_fixture["evidence"]}
    checks = {
        "decision_is_block": observed_raw["expected_decision"] == "block",
        "patch_is_empty": observed_raw["desired_patch"] == [],
        "gate_status_is_blocked": observed_raw["expected_gate"].get("status") == "blocked",
        "gate_reason_is_exact": observed_raw["expected_gate"].get("reason_code") == expected_reason,
        "permitted_action_is_none": observed_raw["expected_gate"].get("permitted_action") == "none",
        "gate_object_is_exact": observed_raw["expected_gate"] == expected_gate,
        "next_action_is_exact": (
            observed_raw["expected_next_action"] == EXPECTED_BLOCK_ACTION[expected_reason]
        ),
        "preserved_state_is_exact": (
            observed_raw["required_preserved_state"] == expected_preserved_state
        ),
        "initial_state_is_exact": observed_raw["initial_state"] == transformed_fixture["initial_state"],
        "editable_paths_are_preserved": (
            observed_raw["editable_paths"] == sorted(obligations["editable_paths"])
        ),
        "immutable_paths_are_preserved": (
            observed_raw["immutable_paths"] == sorted(obligations["immutable_paths"])
        ),
        "unknown_state_boundary_is_preserved": (
            observed_raw["required_unknown_state"] == sorted(obligations["unknown_state"])
        ),
        "forbidden_inference_boundary_is_preserved": (
            observed_raw["forbidden_inferences"] == sorted(obligations["forbidden_inferences"])
        ),
        "evidence_references_exist_in_transformed_input": raw_references <= input_ids,
        "task_identity_is_preserved": observed_raw["task_id"] == transformed_fixture["fixture_id"],
        "contract_identity_is_preserved": (
            observed_raw["contract_id"] == f"OIC-v1::{transformed_fixture['fixture_id']}"
        ),
        "family_is_preserved": observed_raw["family"] == transformed_fixture["family"],
        "split_is_preserved": observed_raw["split"] == transformed_fixture["split"],
    }
    failures = [name for name, passed in checks.items() if not passed]
    return {
        "passed": not failures,
        "checks": checks,
        "failures": failures,
        "expected_execution_projection": {
            "decision": "block",
            "desired_patch": [],
            "gate": expected_gate,
            "next_action": EXPECTED_BLOCK_ACTION[expected_reason],
            "required_preserved_state": expected_preserved_state,
        },
    }


def _case_record(
    *,
    case_id: str,
    fixture: dict[str, Any],
    transformed: TransformResult,
    relation: str,
    expected_reason: str | None,
) -> dict[str, Any]:
    before_hash = digest(fixture)
    after_hash = digest(transformed.fixture)
    baseline = baseline_contract(fixture)
    observed_raw = contract_to_dict(
        compile_contract(project_public_fixture(transformed.fixture))
    )
    observed_normalized = _replace_exact_strings(
        observed_raw, transformed.reverse_output_mapping
    )
    input_changed = before_hash != after_hash
    grounding = raw_grounding_audit(
        baseline=baseline,
        transformed=transformed,
        observed_raw=observed_raw,
    )
    fail_closed: dict[str, Any] | None = None
    if relation == "invariant":
        passed = input_changed and grounding["passed"] and observed_normalized == baseline
    elif relation == "sensitivity":
        require(expected_reason is not None, "sensitivity case requires a reason")
        fail_closed = fail_closed_execution_audit(
            transformed_fixture=transformed.fixture,
            observed_raw=observed_raw,
            expected_reason=expected_reason,
        )
        passed = (
            input_changed
            and baseline["expected_decision"] == "apply"
            and grounding["passed"]
            and fail_closed["passed"]
        )
    else:
        raise ValueError("unknown metamorphic relation")
    return {
        "case_id": case_id,
        "fixture_id": fixture["fixture_id"],
        "family": fixture["family"],
        "relation": relation,
        "transformation": case_id.split("::", 1)[1],
        "source_public_input_sha256": before_hash,
        "transformed_public_input_sha256": after_hash,
        "input_changed": input_changed,
        "baseline_decision": baseline["expected_decision"],
        "baseline_reason": baseline["expected_gate"]["reason_code"],
        "observed_decision": observed_raw["expected_decision"],
        "observed_reason": observed_raw["expected_gate"]["reason_code"],
        "expected_reason": expected_reason,
        "baseline_contract_sha256": digest(baseline),
        "raw_observed_contract_sha256": digest(observed_raw),
        "normalized_observed_contract_sha256": digest(observed_normalized),
        "raw_grounding_audit": grounding,
        "fail_closed_execution_audit": fail_closed,
        "passed": passed,
    }


def run_suite(fixtures: list[dict[str, Any]]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    require(len(fixtures) == len({item["fixture_id"] for item in fixtures}), "fixture IDs are not unique")
    families = {item["family"] for item in fixtures}
    require(families == set(SUPPORTED_FAMILIES), "fixture family coverage is incomplete")

    cases: list[dict[str, Any]] = []
    baseline_decisions = Counter()
    for fixture in fixtures:
        baseline = baseline_contract(fixture)
        baseline_decisions[(fixture["family"], baseline["expected_decision"])] += 1
        for transform_name in INVARIANT_TRANSFORMS:
            transformed = INVARIANT_FUNCTIONS[transform_name](fixture)
            cases.append(_case_record(
                case_id=f"{fixture['fixture_id']}::{transform_name}",
                fixture=fixture,
                transformed=transformed,
                relation="invariant",
                expected_reason=None,
            ))
        if baseline["expected_decision"] == "apply":
            for transform_name, expected_reason in sensitivity_plan(fixture["family"]):
                transformed = SENSITIVITY_FUNCTIONS[transform_name](fixture)
                cases.append(_case_record(
                    case_id=f"{fixture['fixture_id']}::{transform_name}",
                    fixture=fixture,
                    transformed=transformed,
                    relation="sensitivity",
                    expected_reason=expected_reason,
                ))

    relation_counts = Counter(item["relation"] for item in cases)
    passed_counts = Counter(item["relation"] for item in cases if item["passed"])
    transform_counts = Counter(item["transformation"] for item in cases)
    family_relation_counts = Counter((item["family"], item["relation"]) for item in cases)
    failures = [item for item in cases if not item["passed"]]
    apply_count = sum(
        count for (family, decision), count in baseline_decisions.items() if decision == "apply"
    )
    expected_baseline = Counter({
        (FAMILY_CONTROLLED, "apply"): 5,
        (FAMILY_CONTROLLED, "block"): 5,
        (FAMILY_CONFIGURATION, "apply"): 5,
        (FAMILY_CONFIGURATION, "block"): 5,
        (FAMILY_COMMUNICATION, "apply"): 3,
        (FAMILY_COMMUNICATION, "block"): 5,
    })
    expected_transforms = Counter({
        "rename_domain_identifiers": 28,
        "rename_evidence_identifiers": 28,
        "insert_irrelevant_evidence": 28,
        "compose_invariant_transforms": 28,
        "remove_authority": 13,
        "mismatch_authority_target": 13,
        "mismatch_authorized_destination": 13,
        "mismatch_authority_scope": 8,
        "expire_authority": 8,
    })
    expected_family_relations = Counter({
        (FAMILY_CONTROLLED, "invariant"): 40,
        (FAMILY_CONTROLLED, "sensitivity"): 15,
        (FAMILY_CONFIGURATION, "invariant"): 40,
        (FAMILY_CONFIGURATION, "sensitivity"): 25,
        (FAMILY_COMMUNICATION, "invariant"): 32,
        (FAMILY_COMMUNICATION, "sensitivity"): 15,
    })
    fixture_family_counts = Counter(item["family"] for item in fixtures)
    coverage_checks = {
        "base_fixture_count_is_28": len(fixtures) == 28,
        "fixture_family_profile_is_10_10_8": fixture_family_counts == Counter({
            FAMILY_CONTROLLED: 10,
            FAMILY_CONFIGURATION: 10,
            FAMILY_COMMUNICATION: 8,
        }),
        "baseline_decision_profile_is_5_5_3_apply": baseline_decisions == expected_baseline,
        "invariant_case_count_is_112": relation_counts["invariant"] == 112,
        "sensitivity_case_count_is_55": relation_counts["sensitivity"] == 55,
        "transformation_profile_is_complete": transform_counts == expected_transforms,
        "family_relation_profile_is_complete": family_relation_counts == expected_family_relations,
    }
    coverage_failures = [name for name, passed in coverage_checks.items() if not passed]
    coverage_gate = {
        "passed": not coverage_failures,
        "checks": coverage_checks,
        "failures": coverage_failures,
        "interpretation": (
            "The frozen corpus profile and every declared family-by-relation cell must "
            "be non-empty and exact; an all-block compiler cannot pass vacuously."
        ),
    }
    results = {
        "protocol_id": "metamorphic-public-input-v1",
        "overall_passed": not failures and coverage_gate["passed"],
        "base_fixture_count": len(fixtures),
        "baseline_apply_fixture_count": apply_count,
        "baseline_decisions": [
            {"family": family, "decision": decision, "count": count}
            for (family, decision), count in sorted(baseline_decisions.items())
        ],
        "case_count": len(cases),
        "invariant_cases_passed": passed_counts["invariant"],
        "invariant_case_count": relation_counts["invariant"],
        "sensitivity_cases_passed": passed_counts["sensitivity"],
        "sensitivity_case_count": relation_counts["sensitivity"],
        "by_transformation": dict(sorted(transform_counts.items())),
        "by_family_and_relation": [
            {"family": family, "relation": relation, "count": count}
            for (family, relation), count in sorted(family_relation_counts.items())
        ],
        "failures": failures,
        "coverage_gate": coverage_gate,
        "statistical_design": {
            "primary_task_level_reporting_unit": "one frozen public-input task fixture",
            "primary_task_level_reporting_unit_n": len(fixtures),
            "sensitivity_subset_reporting_unit": "one baseline-apply fixture",
            "sensitivity_subset_n": apply_count,
            "repeated_measures": (
                "Four invariance conditions are nested within each of 28 fixtures; "
                "three or five sensitivity conditions are nested within each of 13 "
                "baseline-apply fixtures. Derived cases are not independent samples."
            ),
            "analysis": "exact paired deterministic counts; no p values or population interval",
            "randomization": "none; transformations and order are fixed",
            "exclusions": "none",
            "missing_data": "none",
        },
        "bounded_claim": (
            "Across 28 scrubbed public-input fixtures in three already implemented "
            "grammars, the compiler preserved its normalized contract under four "
            "deterministic semantics-preserving transformations and failed closed "
            "under family-applicable authority perturbations of baseline-apply cases."
        ),
        "non_claims": [
            "This is author-developed post-hoc metamorphic testing, not independent validation.",
            "The transformations exercise three known grammars and do not establish unseen-grammar transfer.",
            "Sensitivity probes establish necessary fail-closed responses for baseline-apply tasks; block-to-apply repair and selective recovery were not tested.",
            "The run tests runtime dependence on scrubbed public facts; it does not establish cognitive independence during compiler development.",
            "Exact pass counts describe this finite deterministic suite and are not prevalence estimates.",
            "The public policy semantics are treated as test premises, not as normatively validated policy.",
        ],
        "non_completion_states": [
            "external_validation_missing",
            "independent_author_set_missing",
            "unseen_grammar_transfer_not_tested",
        ],
    }
    return results, cases
