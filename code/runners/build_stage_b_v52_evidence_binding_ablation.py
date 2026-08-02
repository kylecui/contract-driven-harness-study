#!/usr/bin/env python3
"""Build Stage B v5.2 evidence-binding ablation fixtures and matrix."""

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


REPRESENTATIONS = ["claim-coupled", "binding-separated"]
CONDITIONS = [
    "canonical",
    "field-alias",
    "evidence-order-shuffled",
    "distractor-evidence",
    "unknown-state-paraphrase",
]


def condition_config(condition: str) -> dict[str, Any]:
    config = {
        "reference_field": "evidence_ids",
        "unknown_state": copy.deepcopy(CANONICAL_UNKNOWN),
        "forbidden_inferences": copy.deepcopy(CANONICAL_FORBIDDEN),
        "evidence_order": ["ev-01", "ev-04", "ev-06", "ev-08", "ev-09", "ev-10", "ev-11"],
        "distractors": False,
    }
    if condition == "field-alias":
        config["reference_field"] = "source_references"
    elif condition == "evidence-order-shuffled":
        config["evidence_order"] = [
            "ev-11",
            "ev-04",
            "ev-09",
            "ev-01",
            "ev-10",
            "ev-06",
            "ev-08",
        ]
    elif condition == "distractor-evidence":
        config["distractors"] = True
    elif condition == "unknown-state-paraphrase":
        config["unknown_state"] = copy.deepcopy(PARAPHRASED_UNKNOWN)
        config["forbidden_inferences"] = copy.deepcopy(PARAPHRASED_FORBIDDEN)
    return config


def expected_gate(target_state: str) -> dict[str, Any]:
    return {
        "status": "open",
        "permitted_action": "provider_execution",
        "satisfied_prerequisite": target_state,
        "next_action": "complete_stage_b_v52_evidence_binding_ablation",
        "support_slot_ids": [
            "claim_alpha",
            "claim_beta",
            "claim_gamma",
            "claim_delta",
        ],
    }


def evidence_payload(
    representation: str, reference_field: str
) -> list[dict[str, Any]]:
    payload = []
    for slot in EVIDENCE_SLOTS:
        item = {
            "slot_id": slot["slot_id"],
            reference_field: copy.deepcopy(slot["references"]),
        }
        if representation == "claim-coupled":
            item["claim"] = slot["claim"]
            item = {
                "slot_id": item["slot_id"],
                "claim": item["claim"],
                reference_field: item[reference_field],
            }
        payload.append(item)
    return payload


def attestation(
    representation: str, reference_field: str
) -> dict[str, Any]:
    section = (
        "grounded_claims"
        if representation == "claim-coupled"
        else "evidence_bindings"
    )
    return {
        "status": "preserved_after_transition",
        "immutable_fields": [
            f"{section}[].slot_id",
            f"{section}[].{reference_field}",
            "state_inventory.unknown_state",
            "state_inventory.forbidden_inferences",
            "state_inventory.known_state[].state_id",
            f"state_inventory.known_state[].{reference_field}",
            "transition_record.event_id",
            f"transition_record.{reference_field}",
        ],
    }


def golden_output(
    representation: str,
    reference_field: str,
    unknown_state: list[str],
    forbidden_inferences: list[str],
) -> dict[str, Any]:
    target_state = unknown_state[-1]
    evidence_section = (
        "grounded_claims"
        if representation == "claim-coupled"
        else "evidence_bindings"
    )
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
        evidence_section: evidence_payload(representation, reference_field),
        "transition_record": {
            "event_id": "event-api-approval-001",
            "state_id": target_state,
            "from_status": "unknown",
            "to_status": "approved",
            reference_field: ["ev-09"],
            "applied": True,
        },
        "transition_gate": expected_gate(target_state),
        "retention_attestation": attestation(representation, reference_field),
    }


def expectation(
    *,
    schema: float = 1.0,
    evidence: float = 1.0,
    vocabulary: float = 1.0,
    transition: float = 1.0,
    gate: float = 1.0,
    attestation_score: float = 1.0,
) -> dict[str, float]:
    aggregate = min(
        schema, evidence, vocabulary, transition, gate, attestation_score
    )
    return {
        "schema_validity": schema,
        "exact_evidence_array_preservation": evidence,
        "residual_unknown_vocabulary_accuracy": vocabulary,
        "state_transition_accuracy": transition,
        "transition_gate_accuracy": gate,
        "retention_attestation_accuracy": attestation_score,
        "controlled_state_mutation_success": aggregate,
    }


def known_bads(
    golden: dict[str, Any],
    representation: str,
    reference_field: str,
    unknown_state: list[str],
    forbidden_inferences: list[str],
) -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, float]]]:
    section = (
        "grounded_claims"
        if representation == "claim-coupled"
        else "evidence_bindings"
    )
    alternate_field = (
        "source_references"
        if reference_field == "evidence_ids"
        else "evidence_ids"
    )
    bads: dict[str, dict[str, Any]] = {}
    expectations: dict[str, dict[str, float]] = {}

    bad = copy.deepcopy(golden)
    bad[section][2][reference_field] = ["ev-10"]
    bads["v5_observed_evidence_omission"] = bad
    expectations["v5_observed_evidence_omission"] = expectation(evidence=0.0)

    bad = copy.deepcopy(golden)
    bad[section][2][reference_field] = ["ev-10"]
    bad[section][3][reference_field] = ["ev-09", "ev-11"]
    bads["semantic_evidence_remap"] = bad
    expectations["semantic_evidence_remap"] = expectation(evidence=0.0)

    bad = copy.deepcopy(golden)
    bad[section][2][reference_field] = ["ev-11", "ev-10"]
    bads["evidence_array_reordered"] = bad
    expectations["evidence_array_reordered"] = expectation(evidence=0.0)

    bad = copy.deepcopy(golden)
    for item in bad[section]:
        item[alternate_field] = item.pop(reference_field)
    bads["undeclared_reference_field"] = bad
    expectations["undeclared_reference_field"] = expectation(
        schema=0.0, evidence=0.0
    )

    bad = copy.deepcopy(golden)
    bad["transition_gate"]["next_action"] = "await_api_approval"
    bads["wrong_gate_next_action"] = bad
    expectations["wrong_gate_next_action"] = expectation(gate=0.0)

    bad = copy.deepcopy(golden)
    bad["state_inventory"]["unknown_state"].reverse()
    bads["residual_unknown_reordered"] = bad
    expectations["residual_unknown_reordered"] = expectation(vocabulary=0.0)

    bad = copy.deepcopy(golden)
    bad["state_inventory"]["known_state"][0][reference_field] = ["ev-08"]
    bad["transition_record"][reference_field] = ["ev-08"]
    bads["wrong_transition_evidence"] = bad
    expectations["wrong_transition_evidence"] = expectation(transition=0.0)

    bad = copy.deepcopy(golden)
    target_state = unknown_state[-1]
    bad["state_inventory"]["known_state"] = []
    bad["state_inventory"]["unknown_state"] = copy.deepcopy(unknown_state)
    bad["state_inventory"]["forbidden_inferences"] = copy.deepcopy(
        forbidden_inferences
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
    expectations["static_pretransition_copy"] = expectation(
        vocabulary=0.0, transition=0.0, gate=0.0
    )

    bad = copy.deepcopy(golden)
    bad["retention_attestation"]["immutable_fields"].pop()
    bads["incomplete_retention_attestation"] = bad
    expectations["incomplete_retention_attestation"] = expectation(
        attestation_score=0.0
    )

    return bads, expectations


def evidence_items(config: dict[str, Any]) -> list[dict[str, Any]]:
    items_by_id = {
        "ev-01": {
            "evidence_id": "ev-01",
            "type": "EXTRACTED",
            "claim": "Stage B v4-local passed all local gates.",
            "source": "P2-E136",
        },
        "ev-04": {
            "evidence_id": "ev-04",
            "type": "AMBIGUOUS",
            "claim": "Stage B v3 macros retained mixed failed cells.",
            "source": "P2-E133",
        },
        "ev-06": {
            "evidence_id": "ev-06",
            "type": "EXTRACTED",
            "claim": "Stage B v4 isolated smoke passed all eight runs.",
            "source": "P2-E140",
        },
        "ev-08": {
            "evidence_id": "ev-08",
            "type": "PROPOSED",
            "claim": "A state transition should follow a clean local gate.",
            "source": "Stage B v5 plan",
        },
        "ev-09": {
            "evidence_id": "ev-09",
            "type": "EXTRACTED",
            "claim": "The fixture event approves provider execution.",
            "source": "event-api-approval-001",
        },
        "ev-10": {
            "evidence_id": "ev-10",
            "type": "EXTRACTED",
            "claim": "Stage B v4 recomposition smoke completed four calls.",
            "source": "P2-E145",
        },
        "ev-11": {
            "evidence_id": "ev-11",
            "type": "EXTRACTED",
            "claim": "All four bounded recomposition outputs passed.",
            "source": "P2-E146",
        },
    }
    items = [copy.deepcopy(items_by_id[item]) for item in config["evidence_order"]]
    if config["distractors"]:
        items.extend(
            [
                {
                    "evidence_id": "ev-90",
                    "type": "EXTRACTED",
                    "claim": "A documentation draft mentions a future dashboard.",
                    "source": "unrelated-note-90",
                },
                {
                    "evidence_id": "ev-91",
                    "type": "AMBIGUOUS",
                    "claim": "An unrelated branch may contain formatting work.",
                    "source": "unrelated-note-91",
                },
            ]
        )
    return items


def write_fixture(
    root: Path,
    representation: str,
    condition: str,
) -> str:
    config = condition_config(condition)
    reference_field = config["reference_field"]
    unknown_state = config["unknown_state"]
    forbidden_inferences = config["forbidden_inferences"]
    target_state = unknown_state[-1]
    representation_profile = (
        "R1" if representation == "claim-coupled" else "R2"
    )
    fixture_name = f"stage-b-v52-{representation_profile.lower()}--{condition}"
    fixture_dir = root / fixture_name
    reset_dir(fixture_dir, root)
    bad_dir = fixture_dir / "known_bad_outputs"
    bad_dir.mkdir()

    evidence_section = (
        "grounded_claims"
        if representation == "claim-coupled"
        else "evidence_bindings"
    )
    golden = golden_output(
        representation,
        reference_field,
        unknown_state,
        forbidden_inferences,
    )
    bads, bad_expectations = known_bads(
        golden,
        representation,
        reference_field,
        unknown_state,
        forbidden_inferences,
    )

    task_spec = {
        "task_id": fixture_name.replace("-", "_"),
        "task_type": "stage_b_v52_evidence_binding_ablation",
        "objective": (
            "Apply one supplied state transition while preserving exact "
            "evidence bindings, residual state, the complete gate, and the "
            "retention attestation."
        ),
        "representation_profile": representation_profile,
        "perturbation_condition": condition.replace("-", "_"),
        "constraints": [
            "Use only the supplied fixture event.",
            f"Use `{reference_field}` as the only reference field.",
            f"Preserve every `{evidence_section}` slot and array exactly.",
            "Move only the declared API-permission state to approved.",
            "Copy the complete required transition gate exactly.",
            "Return exactly one JSON object with no extra prose.",
        ],
        "success_conditions": [
            "Schema validity passes.",
            "All four evidence arrays remain exact.",
            "Residual state and transition checks pass.",
            "The complete gate and attestation remain exact.",
        ],
    }

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

    shape_item = (
        f"array of {{slot_id, claim, {reference_field}}}"
        if representation == "claim-coupled"
        else f"array of {{slot_id, {reference_field}}}"
    )
    output_contract = {
        "output_contract_id": f"out_{fixture_name.replace('-', '_')}_001",
        "format": "json",
        "required_sections": [
            "state_inventory",
            evidence_section,
            "transition_record",
            "transition_gate",
            "retention_attestation",
        ],
        "reference_field": reference_field,
        "representation_profile": representation_profile,
        "output_shape": {
            "state_inventory": {
                "known_state": f"array of {{state_id, value, {reference_field}}}",
                "unknown_state": "array of exact declared labels",
                "forbidden_inferences": "array of exact declared labels",
            },
            evidence_section: shape_item,
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
        "required_evidence_payload": evidence_payload(
            representation, reference_field
        ),
        "initial_state": {
            "known_state": [],
            "unknown_state": unknown_state,
            "forbidden_inferences": forbidden_inferences,
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
            "residual_unknown_state": unknown_state[:-1],
            "residual_forbidden_inferences": forbidden_inferences[:-1],
        },
        "required_transition_gate": expected_gate(target_state),
        "required_attestation": attestation(representation, reference_field),
        "editable_fields": (
            ["grounded_claims[].claim"]
            if representation == "claim-coupled"
            else []
        ),
        "citation_policy": "none",
        "style_profile": "minimal_json",
        "tool_trace_required": False,
    }

    evaluation_spec = {
        "evaluation_version": "stage_b_v52_evidence_binding_ablation_001",
        "primary_metric": "controlled_state_mutation_success",
        "representation_arm": representation.replace("-", "_"),
        "perturbation_condition": condition.replace("-", "_"),
        "evidence_section": evidence_section,
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
        "known_bad_expectations": bad_expectations,
        "model_surface_files": [
            "input.md",
            "task_spec.json",
            "memory_slice.json",
            "evidence_bundle.json",
            "output_contract.json",
        ],
        "forbidden_model_surface_values": [
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

    representation_rule = (
        "Write non-empty claim prose in each grounded claim, but copy every "
        "slot ID and reference array exactly."
        if representation == "claim-coupled"
        else "Copy the evidence-binding objects exactly; do not add claim prose."
    )
    input_text = f"""# Stage B v5.2 Evidence-Binding Ablation

Representation profile: {representation_profile}
Perturbation condition: {condition}

Apply the supplied fixture event to the declared initial state.

Rules:
- Use `{reference_field}` as the only reference field.
- {representation_rule}
- Move only `{target_state}` from unknown to approved.
- Preserve the other unknown-state and forbidden-inference values exactly.
- Copy `required_transition_gate` exactly, including `next_action`.
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
        "representations": REPRESENTATIONS,
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
        write_fixture(output_root, representation, condition)
        for representation in REPRESENTATIONS
        for condition in CONDITIONS
    ]
    dump_json(
        output_root / "suite.json",
        {
            "suite_id": "stage_b_v52_evidence_binding_ablation",
            "representations": REPRESENTATIONS,
            "conditions": CONDITIONS,
            "fixture_count": len(fixtures),
            "known_bad_count": len(fixtures) * 9,
            "fixtures": fixtures,
            "provider_calls": 0,
            "pooling_policy": "must_not_pool_with_stage_b_v5_or_v51",
        },
    )
    dump_json(
        Path(args.matrix_output),
        build_matrix(Path(args.output_dir), fixtures),
    )
    print(f"Built {len(fixtures)} fixtures and 30-run matrix")


if __name__ == "__main__":
    main()
