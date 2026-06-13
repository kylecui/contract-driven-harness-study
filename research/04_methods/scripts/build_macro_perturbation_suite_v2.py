#!/usr/bin/env python3
"""Build the Stage B v2 repair-confirmation perturbation fixtures."""

from __future__ import annotations

import argparse
import copy
import shutil
from pathlib import Path
from typing import Any

import build_macro_perturbation_suite as v1


SELECTED_SUPPORT = {
    "stage7e-v4-known-state-provenance-decision": [
        "stage7e-e01",
        "stage7e-e04",
        "stage7e-e07",
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


def evidence_field(output_contract: dict[str, Any]) -> str:
    aliases = output_contract.get("required_surface_aliases", {})
    return str(aliases.get("evidence_ids", "evidence_ids"))


def output_template(field: str, include_method_plan: bool) -> dict[str, Any]:
    template: dict[str, Any] = {
        "state_inventory": {
            "known_state": f"array of {{state_id, fact, {field}}}",
            "unknown_state": "array of exact declared labels",
            "forbidden_inferences": "array of exact declared labels",
        },
        "grounded_claims": f"array of {{claim, {field}}}",
        "unsupported_claims": f"array of {{claim, reason, {field}}}",
        "typed_evidence": {
            "extracted": "array of evidence ID strings",
            "inferred": "array of evidence ID strings",
            "ambiguous": "array of evidence ID strings",
            "proposed": "array of evidence ID strings",
        },
        "selected_claim": f"object {{option_id, claim, {field}}}",
        "rejected_options": f"exactly 2 objects {{option_id, reason, {field}}}",
        "decision_trace": (
            f"exactly 3 objects {{option_id, decision, step, {field}, "
            "carried_obligations}"
        ),
        "stage_gate": (
            f"object {{status, blocked_outputs, missing_prerequisites, "
            f"next_required_actions, {field}}}"
        ),
        "carried_obligations": (
            f"exactly 4 objects {{obligation, status='preserved', {field}}}"
        ),
    }
    if include_method_plan:
        template["method_plan_update"] = (
            f"object {{selected_next_macro, admission_criteria, local_gates, "
            f"real_model_gate, non_claims, {field}}}"
        )
    return template


def replace_selected_support(
    output_contract: dict[str, Any], required_support: list[str]
) -> None:
    rules = output_contract.setdefault("claim_grounding_rules", {})
    rules["grounded_claim_support_any"] = copy.deepcopy(
        rules.get("selected_claim_support_any", [])
    )
    rules["selected_claim_support_any"] = [required_support]


def add_v2_contract(
    output_contract: dict[str, Any],
    *,
    macro: str,
    condition: str,
) -> None:
    field = evidence_field(output_contract)
    include_method_plan = macro == "stage7-next-method-plan-update"
    output_contract["output_contract_id"] = (
        f"{output_contract['output_contract_id']}_stage_b_v2"
    )
    output_contract["protocol_version"] = "stage_b_v2"
    output_contract["output_template"] = output_template(field, include_method_plan)
    output_contract["output_shape_rules"] = {
        "typed_evidence_id_lists_only": True,
        "enforce_required_nested_fields": True,
        "required_nested_fields": v1.replace_exact_values(
            copy.deepcopy(output_contract.get("required_nested_fields", {})),
            output_contract.get("field_aliases", {}),
        ),
        "exact_array_counts": {
            "rejected_options": 2,
            "decision_trace": 3,
            "carried_obligations": 4,
        },
        "carried_obligation_status_values": ["preserved"],
    }
    output_contract["closed_vocabularies"] = {
        "carried_obligations.status": ["preserved"]
    }
    output_contract["compact_output_rules"] = [
        "Return exactly one JSON object with no Markdown fence or prose.",
        "Use evidence ID strings only inside typed_evidence buckets.",
        "Use exactly the arrays and object shapes declared in output_template.",
        "Use preserved as the only carried-obligation status.",
        "Do not repeat EvidenceBundle claim text inside typed_evidence.",
    ]
    replace_selected_support(output_contract, SELECTED_SUPPORT[macro])
    if condition == "unknown-state-paraphrase":
        output_contract["forbidden_surface_values"] = list(v1.PARAPHRASES)


def model_visible_contract(
    output_contract: dict[str, Any], *, condition: str
) -> dict[str, Any]:
    visible = copy.deepcopy(output_contract)
    surface_requirements: list[str] = []

    if condition == "field-alias":
        visible.pop("field_aliases", None)
        visible.pop("required_surface_aliases", None)
        visible["output_shape_rules"]["required_nested_fields"] = (
            v1.replace_exact_values(
                visible["output_shape_rules"]["required_nested_fields"],
                {"evidence_ids": "source_references"},
            )
        )
        surface_requirements.append(
            "Use source_references everywhere an evidence-reference array is required; do not emit evidence_ids."
        )

    if condition == "unknown-state-paraphrase":
        visible.pop("value_aliases", None)
        visible.pop("forbidden_surface_values", None)
        visible["state_retention_rules"] = v1.replace_exact_values(
            visible.get("state_retention_rules", {}), v1.PARAPHRASES
        )
        surface_requirements.append(
            "Use only the six required_surface_values for unknown-state and forbidden-inference labels."
        )

    if surface_requirements:
        visible["surface_requirements"] = surface_requirements
    return visible


def add_v2_prompt(
    input_text: str,
    *,
    output_contract: dict[str, Any],
    required_support: list[str],
) -> str:
    field = evidence_field(output_contract)
    required = ", ".join(required_support)
    return (
        input_text.rstrip()
        + "\n\n## Stage B v2 Output Protocol\n\n"
        + "- Return exactly one JSON object. Do not use a Markdown fence or add prose.\n"
        + "- Follow `OutputContract.output_template` exactly.\n"
        + "- Keep `typed_evidence` compact: each bucket is an array of evidence ID strings only.\n"
        + f"- The selected C2 claim must include all of these `{field}` values: {required}.\n"
        + "- Emit exactly 2 rejected options, 3 decision-trace entries, and 4 carried obligations.\n"
        + "- Every carried-obligation `status` must be exactly `preserved`.\n"
        + "- Use the exact field names and state labels declared by this fixture.\n"
    )


def remove_selected_evidence(
    payload: dict[str, Any], *, field: str, evidence_id: str
) -> None:
    selected = payload["selected_claim"]
    selected[field] = [
        item for item in selected.get(field, []) if item != evidence_id
    ]


def add_v2_known_bads(
    target: Path,
    *,
    output_contract: dict[str, Any],
    golden: dict[str, Any],
    condition: str,
    required_support: list[str],
) -> None:
    perturbation = v1.load_json(target / "perturbation.json")
    expectations = perturbation["known_bad_expectations"]
    bad_dir = target / "known_bad_outputs"
    field = evidence_field(output_contract)

    incomplete = copy.deepcopy(golden)
    remove_selected_evidence(
        incomplete, field=field, evidence_id=required_support[-1]
    )
    v1.dump_json(bad_dir / "incomplete_selected_claim_support.json", incomplete)
    expectations["incomplete_selected_claim_support"] = ["trace_completeness"]

    expanded = copy.deepcopy(golden)
    expanded["typed_evidence"]["extracted"] = [
        {"evidence_id": evidence_id, "claim": "repeated evidence text"}
        for evidence_id in expanded["typed_evidence"]["extracted"]
    ]
    v1.dump_json(bad_dir / "expanded_typed_evidence_objects.json", expanded)
    expectations["expanded_typed_evidence_objects"] = ["schema_validity"]

    open_status = copy.deepcopy(golden)
    open_status["carried_obligations"][0]["status"] = "satisfied"
    v1.dump_json(bad_dir / "open_vocabulary_status.json", open_status)
    expectations["open_vocabulary_status"] = ["schema_validity"]

    missing_nested = copy.deepcopy(golden)
    missing_nested["carried_obligations"][0].pop(field, None)
    v1.dump_json(bad_dir / "missing_required_nested_field.json", missing_nested)
    expectations["missing_required_nested_field"] = ["schema_validity"]

    if condition == "unknown-state-paraphrase":
        hybrid = copy.deepcopy(golden)
        hybrid["state_inventory"]["forbidden_inferences"][0] = (
            "do_not_infer_branch_currently_checked_out"
        )
        v1.dump_json(bad_dir / "hybrid_unknown_state_surface.json", hybrid)
        expectations["hybrid_unknown_state_surface"] = ["schema_validity"]

    perturbation["suite_version"] = "stage_b_v2"
    perturbation["repair_confirmation"] = True
    perturbation["known_bad_expectations"] = expectations
    v1.dump_json(target / "perturbation.json", perturbation)


def build_fixture(
    base_dir: Path, output_dir: Path, macro: str, condition: str
) -> str:
    old_name = v1.build_fixture(base_dir, output_dir, macro, condition)
    source = output_dir / old_name
    fixture_name = f"{macro}-v2--{condition}"
    target = output_dir / fixture_name
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(source, target)
    shutil.rmtree(source)

    task_spec = v1.load_json(target / "task_spec.json")
    output_contract = v1.load_json(target / "output_contract.json")
    golden = v1.load_json(target / "golden_output.json")
    input_text = (target / "input.md").read_text(encoding="utf-8")

    task_spec["protocol_version"] = "stage_b_v2"
    task_spec["repair_confirmation"] = True
    task_spec["fixture_id"] = fixture_name
    add_v2_contract(output_contract, macro=macro, condition=condition)
    input_text = add_v2_prompt(
        input_text,
        output_contract=output_contract,
        required_support=SELECTED_SUPPORT[macro],
    )

    v1.dump_json(target / "task_spec.json", task_spec)
    v1.dump_json(target / "output_contract.json", output_contract)
    v1.dump_json(
        target / "model_output_contract.json",
        model_visible_contract(output_contract, condition=condition),
    )
    (target / "input.md").write_text(input_text, encoding="utf-8")
    add_v2_known_bads(
        target,
        output_contract=output_contract,
        golden=golden,
        condition=condition,
        required_support=SELECTED_SUPPORT[macro],
    )
    return fixture_name


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-dir", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    base_dir = Path(args.base_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    fixtures = [
        build_fixture(base_dir, output_dir, macro, condition)
        for macro in v1.MACROS
        for condition in v1.CONDITIONS
    ]
    v1.dump_json(
        output_dir / "suite.json",
        {
            "suite_id": "stage7_post_freeze_perturbation_suite_v2",
            "purpose": "repair_confirmation_after_stage_b_v1_failure",
            "pooling_policy": "must_not_pool_with_stage_b_v1",
            "macros": v1.MACROS,
            "conditions": v1.CONDITIONS,
            "fixture_count": len(fixtures),
            "fixtures": fixtures,
        },
    )
    print(f"Built {len(fixtures)} Stage B v2 fixtures under {output_dir}")


if __name__ == "__main__":
    main()
