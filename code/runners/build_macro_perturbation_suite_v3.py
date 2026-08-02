#!/usr/bin/env python3
"""Build the full Stage B v3 literal-skeleton perturbation suite."""

from __future__ import annotations

import argparse
import copy
import json
import shutil
from pathlib import Path
from typing import Any


MACROS = [
    "stage7e-v4-known-state-provenance-decision",
    "stage7-next-method-plan-update",
]

CONDITIONS = [
    "canonical",
    "evidence-order-shuffled",
    "field-alias",
    "unknown-state-paraphrase",
    "distractor-evidence",
]

GROUNDED_SUPPORT = {
    "stage7e-v4-known-state-provenance-decision": [
        "stage7e-e01",
        "stage7e-e04",
        "stage7e-e08",
        "stage7e-e09",
    ],
    "stage7-next-method-plan-update": [
        "stage7next-e01",
        "stage7next-e06",
        "stage7next-e07",
        "stage7next-e08",
    ],
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def dump_json(path: Path, payload: Any) -> None:
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def evidence_field(golden: dict[str, Any]) -> str:
    selected = golden["selected_claim"]
    return "source_references" if "source_references" in selected else "evidence_ids"


def placeholder_skeleton(golden: dict[str, Any]) -> dict[str, Any]:
    skeleton = copy.deepcopy(golden)

    for item in skeleton["state_inventory"]["known_state"]:
        item["fact"] = f"<grounded fact for {item['state_id']}>"

    for index, item in enumerate(skeleton["grounded_claims"], start=1):
        item["claim"] = f"<grounded claim {index}>"

    for index, item in enumerate(skeleton["unsupported_claims"], start=1):
        item["claim"] = f"<unsupported claim {index}>"
        item["reason"] = f"<evidence-linked reason {index}>"

    skeleton["selected_claim"]["claim"] = "<selected bounded C2 claim>"

    for item in skeleton["rejected_options"]:
        item["reason"] = f"<evidence-linked reason for {item['option_id']}>"

    for item in skeleton["decision_trace"]:
        item["step"] = f"<decision step for {item['option_id']}>"

    return skeleton


def flattened_state(golden: dict[str, Any]) -> dict[str, Any]:
    bad = copy.deepcopy(golden)
    inventory = bad.pop("state_inventory")
    bad["state_inventory"] = inventory["known_state"]
    bad["unknown_state"] = inventory["unknown_state"]
    bad["forbidden_inferences"] = inventory["forbidden_inferences"]
    return bad


def root_promoted_state(golden: dict[str, Any]) -> dict[str, Any]:
    bad = copy.deepcopy(golden)
    inventory = bad["state_inventory"]
    bad["state_inventory"] = {"known_state": inventory["known_state"]}
    bad["unknown_state"] = inventory["unknown_state"]
    bad["forbidden_inferences"] = inventory["forbidden_inferences"]
    return bad


def omitted_nested_state(golden: dict[str, Any]) -> dict[str, Any]:
    bad = copy.deepcopy(golden)
    bad["state_inventory"].pop("unknown_state")
    bad["state_inventory"].pop("forbidden_inferences")
    return bad


def compressed_grounded_claims(
    golden: dict[str, Any], *, field: str, required_support: list[str]
) -> dict[str, Any]:
    bad = copy.deepcopy(golden)
    removable_id = required_support[1]
    bad["grounded_claims"] = [
        claim
        for claim in bad["grounded_claims"]
        if removable_id not in claim.get(field, [])
    ]
    return bad


def patch_contract(
    contract: dict[str, Any],
    *,
    macro: str,
    golden: dict[str, Any],
) -> None:
    contract_id = str(contract["output_contract_id"])
    if contract_id.endswith("_stage_b_v2"):
        contract_id = contract_id.removesuffix("_stage_b_v2")
    contract["output_contract_id"] = f"{contract_id}_stage_b_v3_full"
    contract["protocol_version"] = "stage_b_v3_full"
    contract["mechanism_atoms"] = [
        "hierarchical_output_shape_preservation",
        "explicit_grounded_claim_slot_preservation",
    ]
    contract["literal_json_skeleton_required"] = True
    contract["output_template"] = placeholder_skeleton(golden)

    grounding = contract.setdefault("claim_grounding_rules", {})
    grounding["grounded_claim_support_any"] = [GROUNDED_SUPPORT[macro]]

    shape_rules = contract.setdefault("output_shape_rules", {})
    counts = shape_rules.setdefault("exact_array_counts", {})
    counts["grounded_claims"] = len(golden["grounded_claims"])
    counts["unsupported_claims"] = len(golden["unsupported_claims"])
    counts["rejected_options"] = len(golden["rejected_options"])
    counts["decision_trace"] = len(golden["decision_trace"])
    counts["carried_obligations"] = len(golden["carried_obligations"])

    contract["literal_json_skeleton_instructions"] = [
        "Copy the JSON key hierarchy and array slot count exactly.",
        "Replace placeholder prose strings but never move, rename, promote, omit, merge, or add contract keys.",
        "Preserve every evidence-reference array exactly as shown in the skeleton.",
        "state_inventory must remain an object containing known_state, unknown_state, and forbidden_inferences.",
        "grounded_claims must retain every explicit evidence slot; do not compress multiple slots into fewer claims.",
    ]


def patch_prompt(
    input_text: str,
    *,
    field: str,
    grounded_support: list[str],
    grounded_count: int,
) -> str:
    evidence_text = ", ".join(grounded_support)
    return (
        input_text.rstrip()
        + "\n\n## Stage B v3 Literal Skeleton Protocol\n\n"
        + "`OutputContract.output_template` is a literal JSON skeleton. Copy its key hierarchy, array slot count, state labels, option IDs, and evidence-reference arrays exactly. Replace only placeholder prose strings enclosed in angle brackets.\n\n"
        + "- `state_inventory` must remain an object containing `known_state`, `unknown_state`, and `forbidden_inferences`.\n"
        + "- Never promote nested state fields to the root and never omit them.\n"
        + f"- Emit exactly {grounded_count} `grounded_claims` objects.\n"
        + f"- Across those grounded claims, preserve all required `{field}` values: {evidence_text}.\n"
        + "- Do not merge or compress grounded-claim slots.\n"
        + "- Return exactly one JSON object with no Markdown fence or extra prose.\n"
    )


def build_fixture(
    source_root: Path,
    output_root: Path,
    macro: str,
    condition: str,
) -> str:
    source_name = f"{macro}-v2--{condition}"
    fixture_name = f"{macro}-v3--{condition}"
    source = source_root / source_name
    target = output_root / fixture_name
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(source, target)

    task_spec = load_json(target / "task_spec.json")
    evaluator_contract = load_json(target / "output_contract.json")
    model_contract = load_json(target / "model_output_contract.json")
    golden = load_json(target / "golden_output.json")
    perturbation = load_json(target / "perturbation.json")
    input_text = (target / "input.md").read_text(encoding="utf-8")
    field = evidence_field(golden)

    task_spec["fixture_id"] = fixture_name
    task_spec["protocol_version"] = "stage_b_v3_full"
    task_spec["repair_confirmation"] = True
    task_spec["mechanism_atoms"] = [
        "hierarchical_output_shape_preservation",
        "explicit_grounded_claim_slot_preservation",
    ]

    patch_contract(evaluator_contract, macro=macro, golden=golden)
    patch_contract(model_contract, macro=macro, golden=golden)
    input_text = patch_prompt(
        input_text,
        field=field,
        grounded_support=GROUNDED_SUPPORT[macro],
        grounded_count=len(golden["grounded_claims"]),
    )

    bad_dir = target / "known_bad_outputs"
    dump_json(bad_dir / "flattened_state_inventory.json", flattened_state(golden))
    dump_json(bad_dir / "root_promoted_state_fields.json", root_promoted_state(golden))
    dump_json(bad_dir / "omitted_nested_state_fields.json", omitted_nested_state(golden))
    dump_json(
        bad_dir / "compressed_grounded_claim_slots.json",
        compressed_grounded_claims(
            golden,
            field=field,
            required_support=GROUNDED_SUPPORT[macro],
        ),
    )

    expectations = perturbation.setdefault("known_bad_expectations", {})
    for name in [
        "flattened_state_inventory",
        "root_promoted_state_fields",
        "omitted_nested_state_fields",
    ]:
        expectations[name] = ["schema_validity", "state_accuracy"]
    expectations["compressed_grounded_claim_slots"] = [
        "schema_validity",
        "citation_grounding",
    ]
    perturbation.update(
        {
            "base_macro": macro,
            "condition": condition,
            "suite_version": "stage_b_v3_full",
            "repair_confirmation": True,
            "representation_preserving": True,
            "mechanism_atoms": [
                "hierarchical_output_shape_preservation",
                "explicit_grounded_claim_slot_preservation",
            ],
            "pooling_policy": "must_not_pool_with_stage_b_v1_or_v2",
        }
    )

    dump_json(target / "task_spec.json", task_spec)
    dump_json(target / "output_contract.json", evaluator_contract)
    dump_json(target / "model_output_contract.json", model_contract)
    dump_json(target / "perturbation.json", perturbation)
    (target / "input.md").write_text(input_text, encoding="utf-8")
    return fixture_name


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-dir", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    source_root = Path(args.source_dir)
    output_root = Path(args.output_dir)
    output_root.mkdir(parents=True, exist_ok=True)

    fixtures = [
        build_fixture(source_root, output_root, macro, condition)
        for macro in MACROS
        for condition in CONDITIONS
    ]
    dump_json(
        output_root / "suite.json",
        {
            "suite_id": "stage_b_v3_full_perturbation_suite",
            "purpose": "full_repair_confirmation_after_stage_b_v3_shape_smoke",
            "macros": MACROS,
            "conditions": CONDITIONS,
            "fixture_count": len(fixtures),
            "fixtures": fixtures,
            "mechanism_atoms": [
                "hierarchical_output_shape_preservation",
                "explicit_grounded_claim_slot_preservation",
            ],
            "pooling_policy": "must_not_pool_with_stage_b_v1_or_v2",
        },
    )
    print(f"Built {len(fixtures)} Stage B v3 fixtures under {output_root}")


if __name__ == "__main__":
    main()
