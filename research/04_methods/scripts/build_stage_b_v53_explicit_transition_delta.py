#!/usr/bin/env python3
"""Build Stage B v5.3 explicit transition-delta ablation fixtures."""

from __future__ import annotations

import argparse
import copy
from pathlib import Path
from typing import Any

from build_stage_b_v5_state_transition import (
    CANONICAL_FORBIDDEN,
    CANONICAL_UNKNOWN,
    EVIDENCE_SLOTS,
    PARAPHRASED_FORBIDDEN,
    PARAPHRASED_UNKNOWN,
    dump_json,
    reset_dir,
)
from build_stage_b_v52_evidence_binding_ablation import (
    CONDITIONS,
    attestation,
    condition_config,
    evidence_items,
    evidence_payload,
    expectation,
)


PROTOCOL_ARMS = ["postcondition-only", "explicit-delta"]
PROFILE_BY_ARM = {
    "postcondition-only": "P1",
    "explicit-delta": "P2",
}


def expected_gate(target_state: str) -> dict[str, Any]:
    return {
        "status": "open",
        "permitted_action": "provider_execution",
        "satisfied_prerequisite": target_state,
        "next_action": "complete_stage_b_v53_explicit_transition_delta",
        "support_slot_ids": [
            "claim_alpha",
            "claim_beta",
            "claim_gamma",
            "claim_delta",
        ],
    }


def transition_delta(
    reference_field: str,
    unknown_state: list[str],
    forbidden_inferences: list[str],
) -> dict[str, Any]:
    target_state = unknown_state[-1]
    return {
        "remove_from_unknown_state": [target_state],
        "remove_from_forbidden_inferences": [forbidden_inferences[-1]],
        "add_to_known_state": [
            {
                "state_id": target_state,
                "value": "approved",
                reference_field: ["ev-09"],
            }
        ],
        "preserve_unknown_state": copy.deepcopy(unknown_state[:-1]),
        "preserve_forbidden_inferences": copy.deepcopy(
            forbidden_inferences[:-1]
        ),
    }


def golden_output(
    reference_field: str,
    unknown_state: list[str],
    forbidden_inferences: list[str],
) -> dict[str, Any]:
    target_state = unknown_state[-1]
    return {
        "state_inventory": {
            "known_state": [
                {
                    "state_id": target_state,
                    "value": "approved",
                    reference_field: ["ev-09"],
                }
            ],
            "unknown_state": copy.deepcopy(unknown_state[:-1]),
            "forbidden_inferences": copy.deepcopy(forbidden_inferences[:-1]),
        },
        "evidence_bindings": evidence_payload(
            "binding-separated", reference_field
        ),
        "transition_record": {
            "event_id": "event-api-approval-001",
            "state_id": target_state,
            "from_status": "unknown",
            "to_status": "approved",
            reference_field: ["ev-09"],
            "applied": True,
        },
        "transition_gate": expected_gate(target_state),
        "retention_attestation": attestation(
            "binding-separated", reference_field
        ),
    }


def known_bads(
    golden: dict[str, Any],
    reference_field: str,
    unknown_state: list[str],
    forbidden_inferences: list[str],
) -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, float]]]:
    alternate_field = (
        "source_references"
        if reference_field == "evidence_ids"
        else "evidence_ids"
    )
    bads: dict[str, dict[str, Any]] = {}
    expectations: dict[str, dict[str, float]] = {}

    bad = copy.deepcopy(golden)
    bad["state_inventory"]["forbidden_inferences"].append(
        forbidden_inferences[-1]
    )
    bads["obsolete_forbidden_inference_retained"] = bad
    expectations["obsolete_forbidden_inference_retained"] = expectation(
        vocabulary=0.0
    )

    bad = copy.deepcopy(golden)
    bad["state_inventory"]["unknown_state"].append(unknown_state[-1])
    bads["transitioned_state_retained_as_unknown"] = bad
    expectations["transitioned_state_retained_as_unknown"] = expectation(
        vocabulary=0.0
    )

    bad = copy.deepcopy(golden)
    bad["state_inventory"]["unknown_state"].reverse()
    bads["residual_unknown_reordered"] = bad
    expectations["residual_unknown_reordered"] = expectation(vocabulary=0.0)

    bad = copy.deepcopy(golden)
    bad["state_inventory"]["forbidden_inferences"].reverse()
    bads["residual_forbidden_reordered"] = bad
    expectations["residual_forbidden_reordered"] = expectation(vocabulary=0.0)

    bad = copy.deepcopy(golden)
    bad["evidence_bindings"][2][reference_field] = ["ev-10"]
    bads["evidence_omission"] = bad
    expectations["evidence_omission"] = expectation(evidence=0.0)

    bad = copy.deepcopy(golden)
    bad["evidence_bindings"][2][reference_field] = ["ev-10"]
    bad["evidence_bindings"][3][reference_field] = ["ev-11"]
    bads["semantic_evidence_remap"] = bad
    expectations["semantic_evidence_remap"] = expectation(evidence=0.0)

    bad = copy.deepcopy(golden)
    for item in bad["evidence_bindings"]:
        item[alternate_field] = item.pop(reference_field)
    bads["undeclared_reference_field"] = bad
    expectations["undeclared_reference_field"] = expectation(
        schema=0.0, evidence=0.0
    )

    bad = copy.deepcopy(golden)
    bad["state_inventory"]["known_state"][0]["value"] = "denied"
    bad["transition_record"]["to_status"] = "denied"
    bads["wrong_transition_value"] = bad
    expectations["wrong_transition_value"] = expectation(transition=0.0)

    bad = copy.deepcopy(golden)
    bad["transition_gate"]["next_action"] = "await_api_approval"
    bads["wrong_gate_next_action"] = bad
    expectations["wrong_gate_next_action"] = expectation(gate=0.0)

    bad = copy.deepcopy(golden)
    bad["retention_attestation"]["immutable_fields"].pop()
    bads["incomplete_retention_attestation"] = bad
    expectations["incomplete_retention_attestation"] = expectation(
        attestation_score=0.0
    )

    return bads, expectations


def write_fixture(root: Path, arm: str, condition: str) -> str:
    config = condition_config(condition)
    reference_field = config["reference_field"]
    unknown_state = config["unknown_state"]
    forbidden_inferences = config["forbidden_inferences"]
    target_state = unknown_state[-1]
    profile = PROFILE_BY_ARM[arm]
    fixture_name = f"stage-b-v53-{profile.lower()}--{condition}"
    fixture_dir = root / fixture_name
    reset_dir(fixture_dir, root)
    bad_dir = fixture_dir / "known_bad_outputs"
    bad_dir.mkdir()

    golden = golden_output(
        reference_field, unknown_state, forbidden_inferences
    )
    bads, bad_expectations = known_bads(
        golden, reference_field, unknown_state, forbidden_inferences
    )

    postconditions = {
        "known_state": copy.deepcopy(golden["state_inventory"]["known_state"]),
        "residual_unknown_state": copy.deepcopy(unknown_state[:-1]),
        "residual_forbidden_inferences": copy.deepcopy(
            forbidden_inferences[:-1]
        ),
    }
    delta = transition_delta(
        reference_field, unknown_state, forbidden_inferences
    )

    arm_constraint = (
        "Execute every operation in `required_transition_delta` exactly."
        if arm == "explicit-delta"
        else "Satisfy `required_postconditions` exactly."
    )
    task_spec = {
        "task_id": fixture_name.replace("-", "_"),
        "task_type": "stage_b_v53_explicit_transition_delta_ablation",
        "objective": (
            "Apply one supplied state transition while preserving exact "
            "evidence bindings, residual state, the complete gate, and the "
            "retention attestation."
        ),
        "protocol_profile": profile,
        "perturbation_condition": condition.replace("-", "_"),
        "constraints": [
            "Use only the supplied fixture event.",
            f"Use `{reference_field}` as the only reference field.",
            "Copy every `evidence_bindings` slot and array exactly.",
            arm_constraint,
            "Copy the complete required transition gate exactly.",
            "Return exactly one JSON object with no extra prose.",
        ],
        "success_conditions": [
            "Schema validity passes.",
            "Residual state exactly matches the declared result.",
            "All four evidence arrays remain exact.",
            "The transition, complete gate, and attestation remain exact.",
        ],
    }

    output_contract = {
        "output_contract_id": f"out_{fixture_name.replace('-', '_')}_001",
        "format": "json",
        "required_sections": [
            "state_inventory",
            "evidence_bindings",
            "transition_record",
            "transition_gate",
            "retention_attestation",
        ],
        "reference_field": reference_field,
        "protocol_profile": profile,
        "output_shape": {
            "state_inventory": {
                "known_state": f"array of {{state_id, value, {reference_field}}}",
                "unknown_state": "array of exact declared labels",
                "forbidden_inferences": "array of exact declared labels",
            },
            "evidence_bindings": (
                f"array of {{slot_id, {reference_field}}}"
            ),
            "transition_record": (
                "{event_id, state_id, from_status, to_status, "
                f"{reference_field}, applied}}"
            ),
            "transition_gate": (
                "{status, permitted_action, satisfied_prerequisite, "
                "next_action, support_slot_ids}"
            ),
            "retention_attestation": "{status, immutable_fields}",
        },
        "required_evidence_bindings": evidence_payload(
            "binding-separated", reference_field
        ),
        "initial_state": {
            "known_state": [],
            "unknown_state": copy.deepcopy(unknown_state),
            "forbidden_inferences": copy.deepcopy(forbidden_inferences),
            "gate_status": "blocked",
        },
        "transition_event": {
            "event_id": "event-api-approval-001",
            "scope": "fixture_only",
            "state_id": target_state,
            "from_status": "unknown",
            "to_status": "approved",
            reference_field: ["ev-09"],
        },
        "required_postconditions": postconditions,
        "required_transition_gate": expected_gate(target_state),
        "required_attestation": attestation(
            "binding-separated", reference_field
        ),
        "editable_fields": [],
        "citation_policy": "none",
        "style_profile": "minimal_json",
        "tool_trace_required": False,
    }
    if arm == "explicit-delta":
        output_contract["required_transition_delta"] = delta

    memory_slice = {
        "slice_id": f"{fixture_name}_memory_001",
        "must_load": [
            "branch and CI state remain unknown",
            "API permission changes only through event-api-approval-001",
            "the event applies only inside this fixture",
        ],
        "must_not_load": [
            "alternative evidence fields or state vocabularies",
            "implicit branch or CI values",
            "production readiness claims",
        ],
        "staleness_policy": "event_driven_snapshot",
    }
    evidence_bundle = {
        "bundle_id": f"{fixture_name}_evidence_001",
        "items": evidence_items(config),
    }
    evaluation_spec = {
        "evaluation_version": "stage_b_v53_explicit_transition_delta_001",
        "primary_metric": "residual_unknown_vocabulary_accuracy",
        "protocol_arm": arm.replace("-", "_"),
        "representation_arm": arm.replace("-", "_"),
        "perturbation_condition": condition.replace("-", "_"),
        "evidence_section": "evidence_bindings",
        "reference_field": reference_field,
        "expected_payload": [
            {"slot_id": slot["slot_id"], "references": slot["references"]}
            for slot in EVIDENCE_SLOTS
        ],
        "expected_known_state": golden["state_inventory"]["known_state"],
        "expected_unknown_state": unknown_state[:-1],
        "expected_forbidden_inferences": forbidden_inferences[:-1],
        "expected_transition_record": golden["transition_record"],
        "expected_gate": golden["transition_gate"],
        "expected_attestation": golden["retention_attestation"],
        "expected_postconditions": postconditions,
        "expected_transition_delta": delta if arm == "explicit-delta" else None,
        "known_bad_expectations": bad_expectations,
        "model_surface_files": [
            "input.md",
            "task_spec.json",
            "memory_slice.json",
            "evidence_bundle.json",
            "output_contract.json",
        ],
        "forbidden_model_surface_values": [
            "postcondition_only",
            "explicit_delta",
            "postcondition-only",
            "explicit-delta",
            (
                "source_references"
                if reference_field == "evidence_ids"
                else "evidence_ids"
            ),
            *(
                PARAPHRASED_UNKNOWN
                if unknown_state == CANONICAL_UNKNOWN
                else CANONICAL_UNKNOWN
            ),
            *(
                PARAPHRASED_FORBIDDEN
                if forbidden_inferences == CANONICAL_FORBIDDEN
                else CANONICAL_FORBIDDEN
            ),
        ],
    }

    control_rule = (
        "- Execute every operation in `required_transition_delta` exactly.\n"
        if arm == "explicit-delta"
        else "- Satisfy `required_postconditions` exactly.\n"
    )
    input_text = f"""# Stage B v5.3 Controlled State Transition

Protocol profile: {profile}
Perturbation condition: {condition}

Apply the supplied fixture event to the declared initial state.

Rules:
- Use `{reference_field}` as the only reference field.
- Copy every `required_evidence_bindings` object exactly and in order.
{control_rule}- Copy `required_transition_gate` exactly, including `next_action`.
- Copy `required_attestation` exactly.
- The event has fixture-only scope and does not authorize a real tool call.
- Return exactly one JSON object with no Markdown fence or extra prose.
"""

    dump_json(fixture_dir / "task_spec.json", task_spec)
    dump_json(fixture_dir / "memory_slice.json", memory_slice)
    dump_json(fixture_dir / "evidence_bundle.json", evidence_bundle)
    dump_json(fixture_dir / "output_contract.json", output_contract)
    dump_json(fixture_dir / "evaluation_spec.json", evaluation_spec)
    dump_json(fixture_dir / "golden_output.json", golden)
    (fixture_dir / "input.md").write_text(input_text, encoding="utf-8")
    for name, payload in bads.items():
        dump_json(bad_dir / f"{name}.json", payload)
    return fixture_name


def build_matrix(fixtures_dir: Path, fixtures: list[str]) -> dict[str, Any]:
    runs = []
    for fixture in fixtures:
        for repetition in range(1, 4):
            runs.append(
                {
                    "run_id": (
                        f"{fixture}__budget_model__G9__r{repetition}"
                    ),
                    "fixture": fixture,
                    "model": "budget_model",
                    "harness_arm": "G9",
                    "repetition": repetition,
                    "status": "planned",
                }
            )
    return {
        "fixtures_dir": str(fixtures_dir),
        "models": ["budget_model"],
        "harness_arms": ["G9"],
        "protocol_profiles": list(PROFILE_BY_ARM.values()),
        "conditions": CONDITIONS,
        "fixtures": fixtures,
        "repetitions": 3,
        "run_count": len(runs),
        "runs": runs,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--matrix-output", required=True)
    args = parser.parse_args()

    output_root = Path(args.output_dir)
    output_root.parent.mkdir(parents=True, exist_ok=True)
    reset_dir(output_root, output_root.parent)
    fixtures = [
        write_fixture(output_root, arm, condition)
        for arm in PROTOCOL_ARMS
        for condition in CONDITIONS
    ]
    dump_json(
        output_root / "suite.json",
        {
            "suite_id": "stage_b_v53_explicit_transition_delta",
            "protocol_arms": PROTOCOL_ARMS,
            "model_visible_profiles": list(PROFILE_BY_ARM.values()),
            "conditions": CONDITIONS,
            "fixture_count": len(fixtures),
            "known_bad_count": len(fixtures) * 10,
            "fixtures": fixtures,
            "provider_calls": 0,
            "pooling_policy": "must_not_pool_with_v51_or_v52",
        },
    )
    dump_json(
        Path(args.matrix_output),
        build_matrix(Path(args.output_dir), fixtures),
    )
    print(f"Built {len(fixtures)} fixtures and 30-run matrix")


if __name__ == "__main__":
    main()
