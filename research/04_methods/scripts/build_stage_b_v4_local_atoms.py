#!/usr/bin/env python3
"""Build Stage B v4 local mechanism atoms and known-bad outputs."""

from __future__ import annotations

import argparse
import copy
import json
import shutil
from pathlib import Path
from typing import Any


EVIDENCE_SLOTS = [
    {
        "slot_id": "claim_alpha",
        "claim": "The local gate passed before provider execution.",
        "references": ["ev-01"],
    },
    {
        "slot_id": "claim_beta",
        "claim": "The proposed stressor remains blocked pending a targeted smoke.",
        "references": ["ev-06"],
    },
    {
        "slot_id": "claim_gamma",
        "claim": "The next decision must preserve both the method rule and the backlog state.",
        "references": ["ev-07", "ev-08"],
    },
]

CANONICAL_UNKNOWN = [
    "current_git_branch",
    "ci_status",
    "network_api_approval",
]

CANONICAL_FORBIDDEN = [
    "do_not_infer_current_git_branch",
    "do_not_infer_ci_status",
    "do_not_infer_network_api_approval",
]

PARAPHRASED_UNKNOWN = [
    "branch_currently_checked_out",
    "continuous_integration_result",
    "permission_to_use_external_model_api",
]

PARAPHRASED_FORBIDDEN = [
    "do_not_guess_branch_currently_checked_out",
    "do_not_guess_continuous_integration_result",
    "do_not_guess_permission_to_use_external_model_api",
]


def dump_json(path: Path, payload: Any) -> None:
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def reset_dir(path: Path, root: Path) -> None:
    resolved = path.resolve()
    resolved_root = root.resolve()
    if not resolved.is_relative_to(resolved_root):
        raise ValueError(f"Refusing to reset path outside output root: {resolved}")
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True)


def common_memory_slice(slice_id: str, must_load: list[str]) -> dict[str, Any]:
    return {
        "slice_id": slice_id,
        "must_load": must_load,
        "must_not_load": [
            "alternative field names or value aliases",
            "undeclared evidence IDs or state labels",
        ],
        "staleness_policy": "fixed_snapshot",
    }


def write_fixture(
    *,
    root: Path,
    fixture_name: str,
    mechanism_atom: dict[str, Any],
    task_spec: dict[str, Any],
    memory_slice: dict[str, Any],
    evidence_bundle: dict[str, Any],
    output_contract: dict[str, Any],
    evaluation_spec: dict[str, Any],
    input_text: str,
    golden: dict[str, Any],
    known_bads: dict[str, dict[str, Any]],
) -> None:
    fixture_dir = root / fixture_name
    reset_dir(fixture_dir, root)
    bad_dir = fixture_dir / "known_bad_outputs"
    bad_dir.mkdir()

    dump_json(fixture_dir / "mechanism_atom.json", mechanism_atom)
    dump_json(fixture_dir / "task_spec.json", task_spec)
    dump_json(fixture_dir / "memory_slice.json", memory_slice)
    dump_json(fixture_dir / "evidence_bundle.json", evidence_bundle)
    dump_json(fixture_dir / "output_contract.json", output_contract)
    dump_json(fixture_dir / "evaluation_spec.json", evaluation_spec)
    dump_json(fixture_dir / "golden_output.json", golden)
    (fixture_dir / "input.md").write_text(input_text.rstrip() + "\n", encoding="utf-8")
    for name, payload in known_bads.items():
        dump_json(bad_dir / f"{name}.json", payload)


def evidence_output(field: str) -> dict[str, Any]:
    claims = []
    for slot in EVIDENCE_SLOTS:
        claims.append(
            {
                "slot_id": slot["slot_id"],
                "claim": slot["claim"],
                field: copy.deepcopy(slot["references"]),
            }
        )
    return {
        "grounded_claims": claims,
        "immutability_check": {
            "status": "preserved",
            "immutable_fields": ["slot_id", field],
        },
    }


def evidence_known_bads(field: str) -> dict[str, dict[str, Any]]:
    golden = evidence_output(field)

    substituted = copy.deepcopy(golden)
    substituted["grounded_claims"][1][field] = ["ev-04"]

    reordered = copy.deepcopy(golden)
    reordered["grounded_claims"][2][field] = ["ev-08", "ev-07"]

    duplicated = copy.deepcopy(golden)
    duplicated["grounded_claims"][0][field] = ["ev-01", "ev-01"]

    added = copy.deepcopy(golden)
    added["grounded_claims"][1][field] = ["ev-06", "ev-09"]

    edited_slot = copy.deepcopy(golden)
    edited_slot["grounded_claims"][1]["slot_id"] = "claim_delta"

    merged = copy.deepcopy(golden)
    merged["grounded_claims"][0][field] = ["ev-01", "ev-06"]
    merged["grounded_claims"].pop(1)

    bads = {
        "substituted_reference": substituted,
        "reordered_multi_reference_array": reordered,
        "duplicated_reference": duplicated,
        "added_undeclared_reference": added,
        "edited_slot_id": edited_slot,
        "merged_claim_slots": merged,
    }

    alternate_field = "source_references" if field == "evidence_ids" else "evidence_ids"
    fallback = copy.deepcopy(golden)
    for claim in fallback["grounded_claims"]:
        claim[alternate_field] = claim.pop(field)
    fallback["immutability_check"]["immutable_fields"] = ["slot_id", alternate_field]
    bads["undeclared_field_fallback"] = fallback
    return bads


def build_evidence_atom(root: Path, *, field: str, variant: str) -> str:
    fixture_name = f"b4a-evidence-array-immutability--{variant}"
    atom_id = "B4A"
    contract_id = f"out_stage_b_v4_b4a_{variant.replace('-', '_')}_001"
    golden = evidence_output(field)
    expected_slots = [
        {"slot_id": slot["slot_id"], "references": slot["references"]}
        for slot in EVIDENCE_SLOTS
    ]
    alternate_field = "source_references" if field == "evidence_ids" else "evidence_ids"

    mechanism_atom = {
        "atom_version": "0.4.0-stage-b-v4-local",
        "atom_id": atom_id,
        "atom_name": f"Exact Evidence-Array Immutability ({variant})",
        "primary_mechanism": "OutputContract",
        "supporting_mechanisms": ["EvidenceBundle"],
        "capability_under_test": (
            "Preserve each declared claim slot and its evidence-reference array "
            "with exact value, multiplicity, and order equality."
        ),
        "non_goals": [
            "Do not evaluate prose quality.",
            "Do not evaluate evidence relevance beyond the frozen slot mapping.",
            "Do not evaluate broad workflow composition.",
        ],
        "input_contract": {
            "required_inputs": [
                "input.md",
                "task_spec.json",
                "memory_slice.json",
                "evidence_bundle.json",
                "output_contract.json",
            ],
            "fixed_snapshot": True,
            "forbidden_assumptions": [
                "Do not substitute a semantically related evidence ID.",
                "Do not rename the declared reference field.",
            ],
        },
        "output_contract_id": contract_id,
        "pass_criteria": [
            {
                "metric": "schema_validity",
                "threshold": 1.0,
                "required": True,
            },
            {
                "metric": "exact_evidence_array_preservation",
                "threshold": 1.0,
                "required": True,
            },
        ],
        "known_failure_modes": [
            "Evidence ID substitution",
            "Evidence-array reordering",
            "Evidence-array duplication or extension",
            "Claim-slot merge or rename",
            "Undeclared field-name fallback",
        ],
        "composition_interface": {
            "input_from_previous": ["fixed_claim_slots", "fixed_evidence_bundle"],
            "output_to_next": ["immutable_grounded_claim_slots"],
            "state_dependencies": [],
            "evidence_dependencies": ["evidence_bundle"],
            "failure_signal": "exact-evidence-array-preservation_failed",
            "repair_policy": "validator_repair",
        },
    }

    task_spec = {
        "task_id": f"stage_b_v4_{fixture_name}",
        "task_type": "mechanism_atom",
        "objective": (
            f"Return the three declared claim slots using `{field}` and preserve "
            "every immutable value exactly."
        ),
        "constraints": [
            "Only the claim prose may be edited.",
            "Keep claim slots in the declared order.",
            f"Use `{field}` as the only evidence-reference field.",
            "Preserve every reference array exactly, including order and duplicates.",
            "Return exactly one JSON object with no extra prose.",
        ],
        "success_conditions": [
            "All three slot IDs match exactly.",
            "All three reference arrays match exactly.",
            "The immutability check reports preserved.",
        ],
    }

    output_contract = {
        "output_contract_id": contract_id,
        "format": "json",
        "required_sections": ["grounded_claims", "immutability_check"],
        "reference_field": field,
        "editable_fields": ["grounded_claims[].claim"],
        "immutable_fields": [
            "grounded_claims[].slot_id",
            f"grounded_claims[].{field}",
        ],
        "exact_output_template": golden,
        "style_profile": "minimal_json",
        "tool_trace_required": False,
    }

    evaluation_spec = {
        "evaluation_version": "stage_b_v4_local_001",
        "atom_kind": "exact_evidence_array_immutability",
        "primary_metric": "exact_evidence_array_preservation",
        "reference_field": field,
        "expected_slots": expected_slots,
        "model_surface_files": [
            "input.md",
            "task_spec.json",
            "memory_slice.json",
            "evidence_bundle.json",
            "output_contract.json",
        ],
        "forbidden_model_surface_values": [alternate_field],
        "known_bad_primary_metric_must_equal": 0.0,
    }

    evidence_bundle = {
        "bundle_id": f"stage_b_v4_b4a_{variant}_evidence_001",
        "items": [
            {
                "evidence_id": f"ev-0{index}",
                "type": "EXTRACTED" if index != 6 else "PROPOSED",
                "claim": f"Frozen evidence record ev-0{index}.",
                "source": "Stage B v4 synthetic fixed snapshot",
            }
            for index in [1, 4, 6, 7, 8, 9]
        ],
    }

    input_text = f"""# Stage B v4 B4A Input: Exact Evidence-Array Immutability

Copy the three slots from `OutputContract.exact_output_template`.

Rules:
- Only `claim` prose is editable.
- `slot_id` and `{field}` are immutable.
- Array order and multiplicity are part of the contract.
- Do not merge slots, add support, remove support, or rename fields.
- Return exactly one JSON object.
"""

    write_fixture(
        root=root,
        fixture_name=fixture_name,
        mechanism_atom=mechanism_atom,
        task_spec=task_spec,
        memory_slice=common_memory_slice(
            f"stage_b_v4_b4a_{variant}_memory_001",
            [
                f"the declared evidence-reference field is {field}",
                "only claim prose is editable",
                "array order and multiplicity are immutable",
            ],
        ),
        evidence_bundle=evidence_bundle,
        output_contract=output_contract,
        evaluation_spec=evaluation_spec,
        input_text=input_text,
        golden=golden,
        known_bads=evidence_known_bads(field),
    )
    return fixture_name


def closed_vocab_output(
    unknown_state: list[str],
    forbidden_inferences: list[str],
) -> dict[str, Any]:
    return {
        "state_inventory": {
            "unknown_state": copy.deepcopy(unknown_state),
            "forbidden_inferences": copy.deepcopy(forbidden_inferences),
        },
        "retention_status": "preserved",
    }


def closed_vocab_known_bads(
    *,
    unknown_state: list[str],
    forbidden_inferences: list[str],
    alternate_unknown: list[str],
    alternate_forbidden: list[str],
    prefix_substitution: list[str],
) -> dict[str, dict[str, Any]]:
    golden = closed_vocab_output(unknown_state, forbidden_inferences)

    prefix_changed = copy.deepcopy(golden)
    prefix_changed["state_inventory"]["forbidden_inferences"] = prefix_substitution

    alternate_fallback = closed_vocab_output(alternate_unknown, alternate_forbidden)

    reordered = copy.deepcopy(golden)
    reordered["state_inventory"]["unknown_state"] = list(reversed(unknown_state))

    omitted = copy.deepcopy(golden)
    omitted["state_inventory"]["forbidden_inferences"].pop()

    added = copy.deepcopy(golden)
    added["state_inventory"]["unknown_state"].append("provider_region")

    mixed = copy.deepcopy(golden)
    mixed["state_inventory"]["unknown_state"][1] = alternate_unknown[1]

    renamed_section = copy.deepcopy(golden)
    inventory = renamed_section["state_inventory"]
    inventory["unknowns"] = inventory.pop("unknown_state")

    return {
        "prefix_substitution": prefix_changed,
        "alternate_vocabulary_fallback": alternate_fallback,
        "reordered_unknown_state": reordered,
        "omitted_forbidden_value": omitted,
        "added_undeclared_value": added,
        "mixed_surface_vocabulary": mixed,
        "renamed_inventory_section": renamed_section,
    }


def build_closed_vocab_atom(root: Path, *, variant: str) -> str:
    fixture_name = f"b4b-closed-vocabulary-retention--{variant}"
    atom_id = "B4B"
    contract_id = f"out_stage_b_v4_b4b_{variant.replace('-', '_')}_001"
    if variant == "canonical":
        unknown = CANONICAL_UNKNOWN
        forbidden = CANONICAL_FORBIDDEN
        alternate_unknown = PARAPHRASED_UNKNOWN
        alternate_forbidden = PARAPHRASED_FORBIDDEN
        prefix_substitution = [
            "do_not_guess_current_git_branch",
            "do_not_guess_ci_status",
            "do_not_guess_network_api_approval",
        ]
    else:
        unknown = PARAPHRASED_UNKNOWN
        forbidden = PARAPHRASED_FORBIDDEN
        alternate_unknown = CANONICAL_UNKNOWN
        alternate_forbidden = CANONICAL_FORBIDDEN
        prefix_substitution = [
            "do_not_infer_branch_currently_checked_out",
            "do_not_infer_continuous_integration_result",
            "do_not_infer_permission_to_use_external_model_api",
        ]

    golden = closed_vocab_output(unknown, forbidden)
    mechanism_atom = {
        "atom_version": "0.4.0-stage-b-v4-local",
        "atom_id": atom_id,
        "atom_name": f"Exact Closed-Vocabulary Retention ({variant})",
        "primary_mechanism": "OutputContract",
        "supporting_mechanisms": ["MemorySlice"],
        "capability_under_test": (
            "Retain declared unknown-state and forbidden-inference labels with "
            "exact value, multiplicity, and order equality."
        ),
        "non_goals": [
            "Do not evaluate whether alternative labels are semantically similar.",
            "Do not evaluate broad state reasoning.",
            "Do not evaluate workflow composition.",
        ],
        "input_contract": {
            "required_inputs": [
                "input.md",
                "task_spec.json",
                "memory_slice.json",
                "evidence_bundle.json",
                "output_contract.json",
            ],
            "fixed_snapshot": True,
            "forbidden_assumptions": [
                "Do not normalize labels to familiar synonyms.",
                "Do not infer undeclared state.",
            ],
        },
        "output_contract_id": contract_id,
        "pass_criteria": [
            {
                "metric": "schema_validity",
                "threshold": 1.0,
                "required": True,
            },
            {
                "metric": "exact_closed_vocabulary_retention",
                "threshold": 1.0,
                "required": True,
            },
        ],
        "known_failure_modes": [
            "Guess-to-infer prefix substitution",
            "Canonical or paraphrased vocabulary fallback",
            "Value omission, addition, or reordering",
            "Mixed vocabulary surfaces",
            "Inventory section rename",
        ],
        "composition_interface": {
            "input_from_previous": ["declared_unknown_state_vocabulary"],
            "output_to_next": ["immutable_state_inventory_labels"],
            "state_dependencies": ["memory_slice"],
            "evidence_dependencies": [],
            "failure_signal": "exact-closed-vocabulary-retention_failed",
            "repair_policy": "validator_repair",
        },
    }

    task_spec = {
        "task_id": f"stage_b_v4_{fixture_name}",
        "task_type": "mechanism_atom",
        "objective": "Copy the two declared closed-vocabulary arrays without normalization.",
        "constraints": [
            "Use only the labels declared in the output template.",
            "Preserve value order and multiplicity.",
            "Do not replace guess with infer or infer with guess.",
            "Do not mix canonical and paraphrased labels.",
            "Return exactly one JSON object with no extra prose.",
        ],
        "success_conditions": [
            "unknown_state exactly matches the declared array.",
            "forbidden_inferences exactly matches the declared array.",
            "retention_status is preserved.",
        ],
    }

    output_contract = {
        "output_contract_id": contract_id,
        "format": "json",
        "required_sections": ["state_inventory", "retention_status"],
        "required_nested_fields": {
            "state_inventory": ["unknown_state", "forbidden_inferences"],
        },
        "closed_vocabularies": {
            "state_inventory.unknown_state": unknown,
            "state_inventory.forbidden_inferences": forbidden,
            "retention_status": ["preserved"],
        },
        "exact_output_template": golden,
        "style_profile": "minimal_json",
        "tool_trace_required": False,
    }

    evaluation_spec = {
        "evaluation_version": "stage_b_v4_local_001",
        "atom_kind": "exact_closed_vocabulary_retention",
        "primary_metric": "exact_closed_vocabulary_retention",
        "expected_unknown_state": unknown,
        "expected_forbidden_inferences": forbidden,
        "model_surface_files": [
            "input.md",
            "task_spec.json",
            "memory_slice.json",
            "evidence_bundle.json",
            "output_contract.json",
        ],
        "forbidden_model_surface_values": alternate_unknown + alternate_forbidden,
        "known_bad_primary_metric_must_equal": 0.0,
    }

    input_text = """# Stage B v4 B4B Input: Exact Closed-Vocabulary Retention

Copy both arrays from `OutputContract.exact_output_template`.

Rules:
- The labels are protocol tokens, not prose.
- Preserve exact spelling, order, and multiplicity.
- Do not normalize a token to a familiar synonym.
- Do not add or omit a token.
- Return exactly one JSON object.
"""

    write_fixture(
        root=root,
        fixture_name=fixture_name,
        mechanism_atom=mechanism_atom,
        task_spec=task_spec,
        memory_slice=common_memory_slice(
            f"stage_b_v4_b4b_{variant}_memory_001",
            [
                "state labels are closed-vocabulary protocol tokens",
                "semantic similarity does not authorize substitution",
                "value order and multiplicity are immutable",
            ],
        ),
        evidence_bundle={
            "bundle_id": f"stage_b_v4_b4b_{variant}_evidence_001",
            "items": [],
        },
        output_contract=output_contract,
        evaluation_spec=evaluation_spec,
        input_text=input_text,
        golden=golden,
        known_bads=closed_vocab_known_bads(
            unknown_state=unknown,
            forbidden_inferences=forbidden,
            alternate_unknown=alternate_unknown,
            alternate_forbidden=alternate_forbidden,
            prefix_substitution=prefix_substitution,
        ),
    )
    return fixture_name


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    output_root = Path(args.output_dir)
    output_root.mkdir(parents=True, exist_ok=True)

    fixtures = [
        build_evidence_atom(output_root, field="evidence_ids", variant="canonical"),
        build_evidence_atom(
            output_root,
            field="source_references",
            variant="declared-field-alias",
        ),
        build_closed_vocab_atom(output_root, variant="canonical"),
        build_closed_vocab_atom(output_root, variant="paraphrased"),
    ]
    dump_json(
        output_root / "suite.json",
        {
            "suite_id": "stage_b_v4_local_mechanism_atoms",
            "purpose": (
                "isolate exact evidence-array immutability and exact "
                "closed-vocabulary retention after Stage B v3"
            ),
            "fixture_count": len(fixtures),
            "fixtures": fixtures,
            "provider_calls": 0,
            "pooling_policy": "must_not_pool_with_stage_b_v1_v2_or_v3",
            "next_gate": (
                "targeted real-model smoke is admissible only if all golden, "
                "known-bad, model-surface, and regression checks pass"
            ),
        },
    )
    print(f"Built {len(fixtures)} Stage B v4 local atoms under {output_root}")


if __name__ == "__main__":
    main()
