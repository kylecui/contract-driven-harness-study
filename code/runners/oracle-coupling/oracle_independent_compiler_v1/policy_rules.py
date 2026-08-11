"""Family-level policy rules for the public-input compiler.

The catalogue contains no fixture identifiers or task-specific outcomes.  It
states which evidence type can authorize each family and how a derived decision
is represented at the gate boundary.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FamilyPolicy:
    family: str
    authority_type: str
    open_reason: str
    permitted_action: str
    apply_action: str


FAMILY_POLICIES = {
    "controlled_state_transition": FamilyPolicy(
        family="controlled_state_transition",
        authority_type="authoritative_transition",
        open_reason="authoritative_transition_confirmed",
        permitted_action="apply_patch",
        apply_action="apply_state_patch",
    ),
    "approval_gated_configuration": FamilyPolicy(
        family="approval_gated_configuration",
        authority_type="approval_record",
        open_reason="valid_scoped_approval",
        permitted_action="apply_patch",
        apply_action="apply_simulated_config_patch",
    ),
    "approval_gated_communication": FamilyPolicy(
        family="approval_gated_communication",
        authority_type="communication_approval",
        open_reason="valid_communication_approval",
        permitted_action="queue_message",
        apply_action="dispatch_approved_message",
    ),
}


BLOCK_ACTIONS = {
    "missing_authoritative_evidence": "request_authoritative_transition_evidence",
    "target_mismatch": "request_target_matching_evidence",
    "from_state_mismatch": "reconcile_current_state",
    "conflicting_authoritative_evidence": "resolve_evidence_conflict",
    "to_state_mismatch": "request_transition_matching_evidence",
    "malformed_authoritative_evidence": "request_well_formed_transition_evidence",
    "missing_valid_approval": "request_valid_scoped_approval",
    "approval_target_mismatch": "request_target_matching_approval",
    "approval_scope_mismatch": "request_scope_matching_approval",
    "approval_expired": "request_fresh_approval",
    "approval_revoked": "request_new_approval_after_revocation",
    "approval_value_mismatch": "request_value_matching_approval",
    "missing_communication_approval": "request_authoritative_communication_approval",
    "communication_recipient_mismatch": "request_recipient_scoped_approval",
    "communication_scope_mismatch": "request_classification_scoped_approval",
    "communication_approval_expired": "request_fresh_communication_approval",
    "communication_approval_revoked": "request_new_communication_approval",
    "communication_transition_mismatch": "request_transition_scoped_communication_approval",
    "request_from_state_mismatch": "reconcile_requested_from_state",
}
