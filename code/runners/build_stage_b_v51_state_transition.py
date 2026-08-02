#!/usr/bin/env python3
"""Build Stage B v5.1 repaired controlled-transition fixtures."""

from __future__ import annotations

import argparse
import copy
import json
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


def expected_attestation(reference_field: str) -> dict[str, Any]:
    return {
        "status": "preserved_after_transition",
        "immutable_fields": [
            "evidence_bindings[].slot_id",
            f"evidence_bindings[].{reference_field}",
            "state_inventory.unknown_state",
            "state_inventory.forbidden_inferences",
            "state_inventory.known_state[].state_id",
            f"state_inventory.known_state[].{reference_field}",
            "transition_record.event_id",
            f"transition_record.{reference_field}",
        ],
    }


def expected_gate(target_state: str) -> dict[str, Any]:
    return {
        "status": "open",
        "permitted_action": "provider_execution",
        "satisfied_prerequisite": target_state,
        "next_action": "run_targeted_state_transition_repair_smoke",
        "support_slot_ids": [
            "claim_alpha",
            "claim_beta",
            "claim_gamma",
            "claim_delta",
        ],
    }


def evidence_bindings(reference_field: str) -> list[dict[str, Any]]:
    return [
        {
            "slot_id": slot["slot_id"],
            reference_field: copy.deepcopy(slot["references"]),
        }
        for slot in EVIDENCE_SLOTS
    ]


def golden_output(
    *,
    reference_field: str,
    initial_unknown: list[str],
    initial_forbidden: list[str],
) -> dict[str, Any]:
    target_state = initial_unknown[-1]
    return {
        "state_inventory": {
            "known_state": [
                {
                    "state_id": target_state,
                    "value": "approved",
                    reference_field: ["ev-09"],
                }
            ],
            "unknown_state": copy.deepcopy(initial_unknown[:-1]),
            "forbidden_inferences": copy.deepcopy(initial_forbidden[:-1]),
        },
        "evidence_bindings": evidence_bindings(reference_field),
        "transition_record": {
            "event_id": "event-api-approval-001",
            "state_id": target_state,
            "from_status": "unknown",
            "to_status": "approved",
            reference_field: ["ev-09"],
            "applied": True,
        },
        "transition_gate": expected_gate(target_state),
        "retention_attestation": expected_attestation(reference_field),
    }


def known_bads(
    *,
    golden: dict[str, Any],
    reference_field: str,
    alternate_field: str,
    initial_unknown: list[str],
    initial_forbidden: list[str],
    prefix_substitution: list[str],
) -> dict[str, dict[str, Any]]:
    bads: dict[str, dict[str, Any]] = {}

    bad = copy.deepcopy(golden)
    bad["evidence_bindings"][1][reference_field] = ["ev-04"]
    bads["evidence_substitution"] = bad

    bad = copy.deepcopy(golden)
    bad["evidence_bindings"][2][reference_field] = ["ev-11", "ev-10"]
    bads["evidence_array_reordered"] = bad

    bad = copy.deepcopy(golden)
    bad["evidence_bindings"].reverse()
    bads["evidence_slot_reordered"] = bad

    bad = copy.deepcopy(golden)
    bad["evidence_bindings"][3]["slot_id"] = "claim_epsilon"
    bads["evidence_slot_renamed"] = bad

    bad = copy.deepcopy(golden)
    for binding in bad["evidence_bindings"]:
        binding[alternate_field] = binding.pop(reference_field)
    bads["undeclared_reference_field"] = bad

    bad = copy.deepcopy(golden)
    bad["evidence_bindings"][2][reference_field] = ["ev-10"]
    bad["evidence_bindings"][3][reference_field] = ["ev-09", "ev-11"]
    bads["v5_observed_semantic_remap"] = bad

    bad = copy.deepcopy(golden)
    bad["state_inventory"]["unknown_state"].reverse()
    bads["residual_unknown_reordered"] = bad

    bad = copy.deepcopy(golden)
    bad["state_inventory"]["forbidden_inferences"] = prefix_substitution
    bads["residual_forbidden_prefix_substitution"] = bad

    bad = copy.deepcopy(golden)
    bad["state_inventory"]["unknown_state"].append(initial_unknown[-1])
    bad["state_inventory"]["forbidden_inferences"].append(initial_forbidden[-1])
    bads["transitioned_target_duplicated_as_unknown"] = bad

    bad = copy.deepcopy(golden)
    bad["state_inventory"]["known_state"][0]["value"] = "denied"
    bad["transition_record"]["to_status"] = "denied"
    bads["wrong_transition_value"] = bad

    bad = copy.deepcopy(golden)
    bad["state_inventory"]["known_state"][0][reference_field] = ["ev-08"]
    bad["transition_record"][reference_field] = ["ev-08"]
    bads["wrong_transition_evidence"] = bad

    bad = copy.deepcopy(golden)
    bad.pop("transition_record")
    bads["transition_record_omitted"] = bad

    bad = copy.deepcopy(golden)
    bad["transition_gate"]["next_action"] = "await_api_approval"
    bads["wrong_gate_next_action"] = bad

    bad = copy.deepcopy(golden)
    bad["transition_gate"]["status"] = "blocked"
    bad["transition_gate"]["permitted_action"] = "none"
    bads["stale_blocked_gate"] = bad

    bad = copy.deepcopy(golden)
    bad["transition_gate"]["support_slot_ids"].remove("claim_delta")
    bads["incomplete_gate_support"] = bad

    bad = copy.deepcopy(golden)
    target_state = initial_unknown[-1]
    bad["state_inventory"]["known_state"] = []
    bad["state_inventory"]["unknown_state"] = copy.deepcopy(initial_unknown)
    bad["state_inventory"]["forbidden_inferences"] = copy.deepcopy(
        initial_forbidden
    )
    bad["transition_record"] = {
        "event_id": "event-api-approval-001",
        "state_id": target_state,
        "from_status": "unknown",
        "to_status": "unknown",
        reference_field: ["ev-09"],
        "applied": False,
    }
    bad["transition_gate"] = {
        "status": "blocked",
        "permitted_action": "none",
        "satisfied_prerequisite": "none",
        "next_action": "await_api_approval",
        "support_slot_ids": [
            "claim_alpha",
            "claim_beta",
            "claim_gamma",
            "claim_delta",
        ],
    }
    bads["static_pretransition_copy"] = bad

    bad = copy.deepcopy(golden)
    bad["evidence_bindings"][1][reference_field] = ["ev-04"]
    bad["state_inventory"]["known_state"][0]["value"] = "denied"
    bad["transition_record"]["to_status"] = "denied"
    bads["evidence_and_transition_corruption"] = bad

    bad = copy.deepcopy(golden)
    bad["retention_attestation"]["immutable_fields"].remove(
        f"transition_record.{reference_field}"
    )
    bads["incomplete_retention_attestation"] = bad

    return bads


def expectation(
    *,
    evidence: float = 1.0,
    vocabulary: float = 1.0,
    transition: float = 1.0,
    gate: float = 1.0,
    attestation: float = 1.0,
    schema: float = 1.0,
) -> dict[str, float]:
    return {
        "schema_validity": schema,
        "exact_evidence_array_preservation": evidence,
        "residual_unknown_vocabulary_accuracy": vocabulary,
        "state_transition_accuracy": transition,
        "transition_gate_accuracy": gate,
        "retention_attestation_accuracy": attestation,
        "controlled_state_mutation_success": min(
            schema, evidence, vocabulary, transition, gate, attestation
        ),
    }


def write_fixture(
    *,
    root: Path,
    variant: str,
    reference_field: str,
    initial_unknown: list[str],
    initial_forbidden: list[str],
    alternate_unknown: list[str],
    alternate_forbidden: list[str],
    prefix_substitution: list[str],
) -> str:
    fixture_name = f"stage-b-v51-state-transition--{variant}"
    fixture_dir = root / fixture_name
    reset_dir(fixture_dir, root)
    bad_dir = fixture_dir / "known_bad_outputs"
    bad_dir.mkdir()

    alternate_field = (
        "source_references"
        if reference_field == "evidence_ids"
        else "evidence_ids"
    )
    target_state = initial_unknown[-1]
    residual_unknown = initial_unknown[:-1]
    residual_forbidden = initial_forbidden[:-1]
    golden = golden_output(
        reference_field=reference_field,
        initial_unknown=initial_unknown,
        initial_forbidden=initial_forbidden,
    )
    bads = known_bads(
        golden=golden,
        reference_field=reference_field,
        alternate_field=alternate_field,
        initial_unknown=initial_unknown,
        initial_forbidden=initial_forbidden,
        prefix_substitution=prefix_substitution,
    )

    task_spec = {
        "task_id": fixture_name.replace("-", "_"),
        "task_type": "stage_b_v51_controlled_state_transition_macro",
        "objective": (
            "Apply one evidence-backed unknown-to-known transition while "
            "copying immutable evidence bindings and the complete gate exactly."
        ),
        "composition_chain": [
            "B4B",
            "B4A",
            "state_transition",
            "transition_gate",
        ],
        "constraints": [
            "Use only the supplied transition event.",
            "Treat the event as fixture state, not runner authorization.",
            f"Use `{reference_field}` as the only reference field.",
            "Copy every evidence-binding object exactly and in order.",
            "Move only the declared API-permission state from unknown to known.",
            "Keep branch and CI state unknown in their declared order.",
            "Remove only the matching API-permission forbidden inference.",
            "Copy the complete required transition gate exactly.",
            "Return exactly one JSON object with no extra prose.",
        ],
        "success_conditions": [
            "Exact evidence-array preservation passes.",
            "Residual unknown-state vocabulary passes.",
            "The transition record and known-state item match the event.",
            "The complete gate matches the declared postcondition.",
            "The retention attestation remains complete.",
        ],
    }

    memory_slice = {
        "slice_id": f"{fixture_name}_memory_001",
        "must_load": [
            "Stage B v5 smoke preserved residual state and transition semantics",
            "branch and CI state remain unknown",
            "API permission changes only through event-api-approval-001",
            "the event applies only inside this fixture",
        ],
        "must_not_load": [
            "alternative evidence fields or state vocabularies",
            "implicit branch or CI values",
            "production or full-workflow readiness claims",
        ],
        "staleness_policy": "event_driven_snapshot",
    }

    evidence_bundle = {
        "bundle_id": f"{fixture_name}_evidence_001",
        "items": [
            {
                "evidence_id": "ev-01",
                "type": "EXTRACTED",
                "claim": "Stage B v4-local passed all local gates.",
                "source": "P2-E136",
            },
            {
                "evidence_id": "ev-04",
                "type": "AMBIGUOUS",
                "claim": "Stage B v3 macros retained mixed failed cells.",
                "source": "P2-E133",
            },
            {
                "evidence_id": "ev-06",
                "type": "EXTRACTED",
                "claim": "Stage B v4 isolated smoke passed all eight runs.",
                "source": "P2-E140",
            },
            {
                "evidence_id": "ev-08",
                "type": "PROPOSED",
                "claim": "A state transition should follow a clean local gate.",
                "source": "Stage B v5 plan",
            },
            {
                "evidence_id": "ev-09",
                "type": "EXTRACTED",
                "claim": (
                    "Within this fixture, provider execution is explicitly "
                    "approved for the state transition."
                ),
                "source": "event-api-approval-001",
            },
            {
                "evidence_id": "ev-10",
                "type": "EXTRACTED",
                "claim": "Stage B v4 recomposition smoke completed four calls.",
                "source": "P2-E145",
            },
            {
                "evidence_id": "ev-11",
                "type": "EXTRACTED",
                "claim": "All four bounded recomposition outputs passed.",
                "source": "P2-E146",
            },
        ],
    }

    required_gate = expected_gate(target_state)
    binding_contract = evidence_bindings(reference_field)
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
        "output_shape": {
            "state_inventory": {
                "known_state": (
                    f"array of {{state_id, value, {reference_field}}}"
                ),
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
        "required_evidence_bindings": binding_contract,
        "initial_state": {
            "known_state": [],
            "unknown_state": initial_unknown,
            "forbidden_inferences": initial_forbidden,
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
        "required_postconditions": {
            "known_state_id": target_state,
            "known_state_value": "approved",
            "residual_unknown_state": residual_unknown,
            "residual_forbidden_inferences": residual_forbidden,
        },
        "required_transition_gate": required_gate,
        "required_attestation": expected_attestation(reference_field),
        "editable_fields": [],
        "citation_policy": "none",
        "style_profile": "minimal_json",
        "tool_trace_required": False,
    }

    known_bad_expectations = {
        "evidence_substitution": expectation(evidence=0.0),
        "evidence_array_reordered": expectation(evidence=0.0),
        "evidence_slot_reordered": expectation(evidence=0.0),
        "evidence_slot_renamed": expectation(evidence=0.0),
        "undeclared_reference_field": expectation(evidence=0.0, schema=0.0),
        "v5_observed_semantic_remap": expectation(evidence=0.0),
        "residual_unknown_reordered": expectation(vocabulary=0.0),
        "residual_forbidden_prefix_substitution": expectation(vocabulary=0.0),
        "transitioned_target_duplicated_as_unknown": expectation(vocabulary=0.0),
        "wrong_transition_value": expectation(transition=0.0),
        "wrong_transition_evidence": expectation(transition=0.0),
        "transition_record_omitted": expectation(transition=0.0, schema=0.0),
        "wrong_gate_next_action": expectation(gate=0.0),
        "stale_blocked_gate": expectation(gate=0.0),
        "incomplete_gate_support": expectation(gate=0.0),
        "static_pretransition_copy": expectation(
            vocabulary=0.0, transition=0.0, gate=0.0
        ),
        "evidence_and_transition_corruption": expectation(
            evidence=0.0, transition=0.0
        ),
        "incomplete_retention_attestation": expectation(attestation=0.0),
    }

    evaluation_spec = {
        "evaluation_version": "stage_b_v51_state_transition_local_001",
        "primary_metric": "controlled_state_mutation_success",
        "reference_field": reference_field,
        "expected_bindings": [
            {"slot_id": slot["slot_id"], "references": slot["references"]}
            for slot in EVIDENCE_SLOTS
        ],
        "expected_known_state": golden["state_inventory"]["known_state"],
        "expected_unknown_state": residual_unknown,
        "expected_forbidden_inferences": residual_forbidden,
        "expected_transition_record": golden["transition_record"],
        "expected_gate": golden["transition_gate"],
        "expected_attestation": golden["retention_attestation"],
        "known_bad_expectations": known_bad_expectations,
        "model_surface_files": [
            "input.md",
            "task_spec.json",
            "memory_slice.json",
            "evidence_bundle.json",
            "output_contract.json",
        ],
        "forbidden_model_surface_values": [
            alternate_field,
            *alternate_unknown,
            *alternate_forbidden,
        ],
    }

    input_text = f"""# Stage B v5.1 Controlled State Transition

Apply one supplied event to the fixed initial state.

Initial unknown state:
{json.dumps(initial_unknown)}

Initial forbidden inferences:
{json.dumps(initial_forbidden)}

Transition event:
- event_id: event-api-approval-001
- scope: fixture_only
- state_id: {target_state}
- from_status: unknown
- to_status: approved
- {reference_field}: ["ev-09"]

Rules:
- Use `{reference_field}` as the only reference field.
- Follow `OutputContract.output_shape` exactly.
- Copy `required_evidence_bindings` exactly, including order.
- Move only `{target_state}` from unknown to known.
- Keep the other two unknown-state and forbidden-inference values exact.
- Emit one transition record for `unknown` to `approved`.
- Copy `required_transition_gate` exactly, including `next_action`.
- Treat the event as fixture state; it does not authorize a provider call.
- Copy `required_attestation` exactly.
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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    output_root = Path(args.output_dir)
    output_root.mkdir(parents=True, exist_ok=True)
    fixtures = [
        write_fixture(
            root=output_root,
            variant="canonical",
            reference_field="evidence_ids",
            initial_unknown=CANONICAL_UNKNOWN,
            initial_forbidden=CANONICAL_FORBIDDEN,
            alternate_unknown=PARAPHRASED_UNKNOWN,
            alternate_forbidden=PARAPHRASED_FORBIDDEN,
            prefix_substitution=[
                "do_not_guess_current_git_branch",
                "do_not_guess_ci_status",
            ],
        ),
        write_fixture(
            root=output_root,
            variant="dual-surface-stress",
            reference_field="source_references",
            initial_unknown=PARAPHRASED_UNKNOWN,
            initial_forbidden=PARAPHRASED_FORBIDDEN,
            alternate_unknown=CANONICAL_UNKNOWN,
            alternate_forbidden=CANONICAL_FORBIDDEN,
            prefix_substitution=[
                "do_not_infer_branch_currently_checked_out",
                "do_not_infer_continuous_integration_result",
            ],
        ),
    ]
    dump_json(
        output_root / "suite.json",
        {
            "suite_id": "stage_b_v51_controlled_state_transition_local",
            "protocol_relation": (
                "new repaired protocol; does not replace or rescore Stage B v5"
            ),
            "composition_chain": [
                "B4B",
                "B4A",
                "state_transition",
                "transition_gate",
            ],
            "fixtures": fixtures,
            "fixture_count": len(fixtures),
            "known_bad_count": 36,
            "provider_calls": 0,
            "pooling_policy": "must_not_pool_with_stage_b_v5_or_prior_protocols",
            "next_gate": (
                "a four-run repair smoke is admissible only after all local "
                "expectations, surface checks, unit tests, and historical "
                "regressions pass"
            ),
        },
    )
    print(f"Built {len(fixtures)} v5.1 fixtures under {output_root}")


if __name__ == "__main__":
    main()
