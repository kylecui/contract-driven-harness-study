#!/usr/bin/env python3
"""Build the bounded Stage B v4 B4A+B4B recomposition fixtures."""

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
        "claim": "Stage B v4-local passed before provider execution.",
        "references": ["ev-01"],
    },
    {
        "slot_id": "claim_beta",
        "claim": "The isolated Stage B v4 smoke passed all eight runs.",
        "references": ["ev-06"],
    },
    {
        "slot_id": "claim_gamma",
        "claim": "Provider execution remains blocked until the recomposition local gate passes.",
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

GATE = {
    "status": "blocked",
    "blocked_action": "provider_execution",
    "missing_prerequisite": "stage_b_v4_recomposition_local_gate",
    "next_action": "prepare_targeted_recomposition_smoke",
    "support_slot_ids": ["claim_alpha", "claim_beta", "claim_gamma"],
}


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


def golden_output(
    *,
    reference_field: str,
    unknown_state: list[str],
    forbidden_inferences: list[str],
) -> dict[str, Any]:
    grounded_claims = [
        {
            "slot_id": slot["slot_id"],
            "claim": slot["claim"],
            reference_field: copy.deepcopy(slot["references"]),
        }
        for slot in EVIDENCE_SLOTS
    ]
    return {
        "state_inventory": {
            "unknown_state": copy.deepcopy(unknown_state),
            "forbidden_inferences": copy.deepcopy(forbidden_inferences),
        },
        "grounded_claims": grounded_claims,
        "composition_gate": copy.deepcopy(GATE),
        "retention_attestation": {
            "status": "preserved",
            "immutable_fields": [
                "state_inventory.unknown_state",
                "state_inventory.forbidden_inferences",
                "grounded_claims[].slot_id",
                f"grounded_claims[].{reference_field}",
            ],
        },
    }


def known_bads(
    *,
    golden: dict[str, Any],
    reference_field: str,
    alternate_field: str,
    alternate_unknown: list[str],
    alternate_forbidden: list[str],
    prefix_substitution: list[str],
) -> dict[str, dict[str, Any]]:
    bads: dict[str, dict[str, Any]] = {}

    substituted = copy.deepcopy(golden)
    substituted["grounded_claims"][1][reference_field] = ["ev-04"]
    bads["evidence_substitution"] = substituted

    reordered_evidence = copy.deepcopy(golden)
    reordered_evidence["grounded_claims"][2][reference_field] = ["ev-08", "ev-07"]
    bads["evidence_array_reordered"] = reordered_evidence

    field_fallback = copy.deepcopy(golden)
    for claim in field_fallback["grounded_claims"]:
        claim[alternate_field] = claim.pop(reference_field)
    field_fallback["retention_attestation"]["immutable_fields"][-1] = (
        f"grounded_claims[].{alternate_field}"
    )
    bads["undeclared_reference_field"] = field_fallback

    vocab_prefix = copy.deepcopy(golden)
    vocab_prefix["state_inventory"]["forbidden_inferences"] = prefix_substitution
    bads["forbidden_prefix_substitution"] = vocab_prefix

    vocab_fallback = copy.deepcopy(golden)
    vocab_fallback["state_inventory"]["unknown_state"] = copy.deepcopy(
        alternate_unknown
    )
    vocab_fallback["state_inventory"]["forbidden_inferences"] = copy.deepcopy(
        alternate_forbidden
    )
    bads["alternate_vocabulary_fallback"] = vocab_fallback

    vocab_reordered = copy.deepcopy(golden)
    vocab_reordered["state_inventory"]["unknown_state"] = list(
        reversed(vocab_reordered["state_inventory"]["unknown_state"])
    )
    bads["unknown_state_reordered"] = vocab_reordered

    gate_open = copy.deepcopy(golden)
    gate_open["composition_gate"]["status"] = "open"
    gate_open["composition_gate"]["blocked_action"] = "none"
    bads["premature_gate_open"] = gate_open

    gate_support = copy.deepcopy(golden)
    gate_support["composition_gate"]["support_slot_ids"].remove("claim_beta")
    bads["incomplete_gate_support"] = gate_support

    dual_corruption = copy.deepcopy(golden)
    dual_corruption["grounded_claims"][1][reference_field] = ["ev-04"]
    dual_corruption["state_inventory"]["forbidden_inferences"] = prefix_substitution
    bads["dual_component_corruption"] = dual_corruption

    flattened_state = copy.deepcopy(golden)
    inventory = flattened_state.pop("state_inventory")
    flattened_state["unknown_state"] = inventory["unknown_state"]
    flattened_state["forbidden_inferences"] = inventory["forbidden_inferences"]
    bads["flattened_state_inventory"] = flattened_state

    return bads


def expectation(
    *,
    evidence: float,
    vocabulary: float,
    gate: float,
    schema: float = 1.0,
) -> dict[str, float]:
    return {
        "schema_validity": schema,
        "exact_evidence_array_preservation": evidence,
        "exact_closed_vocabulary_retention": vocabulary,
        "composition_gate_accuracy": gate,
        "composition_retention": min(evidence, vocabulary, gate, schema),
    }


def write_fixture(
    *,
    root: Path,
    variant: str,
    reference_field: str,
    unknown_state: list[str],
    forbidden_inferences: list[str],
    alternate_unknown: list[str],
    alternate_forbidden: list[str],
    prefix_substitution: list[str],
) -> str:
    fixture_name = f"stage-b-v4-recomposition--{variant}"
    fixture_dir = root / fixture_name
    reset_dir(fixture_dir, root)
    bad_dir = fixture_dir / "known_bad_outputs"
    bad_dir.mkdir()

    alternate_field = (
        "source_references"
        if reference_field == "evidence_ids"
        else "evidence_ids"
    )
    golden = golden_output(
        reference_field=reference_field,
        unknown_state=unknown_state,
        forbidden_inferences=forbidden_inferences,
    )
    bads = known_bads(
        golden=golden,
        reference_field=reference_field,
        alternate_field=alternate_field,
        alternate_unknown=alternate_unknown,
        alternate_forbidden=alternate_forbidden,
        prefix_substitution=prefix_substitution,
    )

    task_spec = {
        "task_id": fixture_name.replace("-", "_"),
        "task_type": "stage_b_v4_bounded_recomposition_macro",
        "objective": (
            "Compose exact state-vocabulary retention and exact per-slot "
            "evidence-array retention into one bounded local-first gate packet."
        ),
        "composition_chain": ["B4B", "B4A", "composition_gate"],
        "constraints": [
            "Preserve both state arrays exactly, including order and multiplicity.",
            f"Use `{reference_field}` as the only evidence-reference field.",
            "Preserve every claim slot and reference array exactly.",
            "Keep provider execution blocked pending the recomposition local gate.",
            "Use all three claim slots as composition-gate support.",
            "Only claim prose may be edited.",
            "Return exactly one JSON object with no extra prose.",
        ],
        "success_conditions": [
            "B4A exact evidence-array preservation passes.",
            "B4B exact closed-vocabulary retention passes.",
            "The composition gate remains blocked and complete.",
            "The retention attestation names all immutable fields.",
        ],
    }

    memory_slice = {
        "slice_id": f"{fixture_name}_memory_001",
        "must_load": [
            "B4A and B4B passed their isolated local and smoke gates",
            "recomposition provider execution remains blocked",
            "only claim prose is editable",
        ],
        "must_not_load": [
            "Stage B v3 broad macro obligations",
            "alternative evidence fields or state vocabularies",
            "production or workflow readiness claims",
        ],
        "staleness_policy": "fixed_snapshot",
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
                "claim": "Stage B v3 full macros had mixed and failed cells.",
                "source": "P2-E133",
            },
            {
                "evidence_id": "ev-06",
                "type": "EXTRACTED",
                "claim": "Stage B v4-smoke passed all eight isolated runs.",
                "source": "P2-E140",
            },
            {
                "evidence_id": "ev-07",
                "type": "INFERRED",
                "claim": "The next unresolved question is bounded composition transfer.",
                "source": "P2-E141",
            },
            {
                "evidence_id": "ev-08",
                "type": "PROPOSED",
                "claim": "Provider execution follows only after the recomposition local gate.",
                "source": "Stage B v4 recomposition plan",
            },
        ],
    }

    output_contract = {
        "output_contract_id": f"out_{fixture_name.replace('-', '_')}_001",
        "format": "json",
        "required_sections": [
            "state_inventory",
            "grounded_claims",
            "composition_gate",
            "retention_attestation",
        ],
        "reference_field": reference_field,
        "editable_fields": ["grounded_claims[].claim"],
        "immutable_fields": golden["retention_attestation"]["immutable_fields"],
        "exact_output_template": golden,
        "citation_policy": "none",
        "style_profile": "minimal_json",
        "tool_trace_required": False,
    }

    known_bad_expectations = {
        "evidence_substitution": expectation(
            evidence=0.0, vocabulary=1.0, gate=1.0
        ),
        "evidence_array_reordered": expectation(
            evidence=0.0, vocabulary=1.0, gate=1.0
        ),
        "undeclared_reference_field": expectation(
            evidence=0.0, vocabulary=1.0, gate=1.0, schema=0.0
        ),
        "forbidden_prefix_substitution": expectation(
            evidence=1.0, vocabulary=0.0, gate=1.0
        ),
        "alternate_vocabulary_fallback": expectation(
            evidence=1.0, vocabulary=0.0, gate=1.0
        ),
        "unknown_state_reordered": expectation(
            evidence=1.0, vocabulary=0.0, gate=1.0
        ),
        "premature_gate_open": expectation(
            evidence=1.0, vocabulary=1.0, gate=0.0
        ),
        "incomplete_gate_support": expectation(
            evidence=1.0, vocabulary=1.0, gate=0.0
        ),
        "dual_component_corruption": expectation(
            evidence=0.0, vocabulary=0.0, gate=1.0
        ),
        "flattened_state_inventory": expectation(
            evidence=1.0, vocabulary=0.0, gate=1.0, schema=0.0
        ),
    }

    evaluation_spec = {
        "evaluation_version": "stage_b_v4_recomposition_local_001",
        "primary_metric": "composition_retention",
        "reference_field": reference_field,
        "expected_slots": [
            {"slot_id": slot["slot_id"], "references": slot["references"]}
            for slot in EVIDENCE_SLOTS
        ],
        "expected_unknown_state": unknown_state,
        "expected_forbidden_inferences": forbidden_inferences,
        "expected_gate": GATE,
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

    input_text = f"""# Stage B v4 Bounded Recomposition

Build one local-first composition packet from the supplied fixed snapshot.

Rules:
- Copy `OutputContract.exact_output_template`.
- Preserve both `state_inventory` arrays exactly.
- Preserve all `grounded_claims` slot IDs and `{reference_field}` arrays exactly.
- Only `claim` prose may be edited.
- Keep `composition_gate.status` equal to `blocked`.
- Keep `provider_execution` blocked until `stage_b_v4_recomposition_local_gate` passes.
- Keep all three support slot IDs in their declared order.
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
            unknown_state=CANONICAL_UNKNOWN,
            forbidden_inferences=CANONICAL_FORBIDDEN,
            alternate_unknown=PARAPHRASED_UNKNOWN,
            alternate_forbidden=PARAPHRASED_FORBIDDEN,
            prefix_substitution=[
                "do_not_guess_current_git_branch",
                "do_not_guess_ci_status",
                "do_not_guess_network_api_approval",
            ],
        ),
        write_fixture(
            root=output_root,
            variant="dual-surface-stress",
            reference_field="source_references",
            unknown_state=PARAPHRASED_UNKNOWN,
            forbidden_inferences=PARAPHRASED_FORBIDDEN,
            alternate_unknown=CANONICAL_UNKNOWN,
            alternate_forbidden=CANONICAL_FORBIDDEN,
            prefix_substitution=[
                "do_not_infer_branch_currently_checked_out",
                "do_not_infer_continuous_integration_result",
                "do_not_infer_permission_to_use_external_model_api",
            ],
        ),
    ]
    dump_json(
        output_root / "suite.json",
        {
            "suite_id": "stage_b_v4_bounded_recomposition_local",
            "composition_chain": ["B4B", "B4A", "composition_gate"],
            "fixtures": fixtures,
            "fixture_count": len(fixtures),
            "provider_calls": 0,
            "pooling_policy": "must_not_pool_with_stage_b_v1_v2_v3_or_v4_atoms",
            "next_gate": (
                "targeted recomposition smoke is admissible only after all local "
                "expectations, surface-isolation checks, unit tests, and v3 "
                "regression checks pass"
            ),
        },
    )
    print(f"Built {len(fixtures)} bounded recomposition fixtures under {output_root}")


if __name__ == "__main__":
    main()
