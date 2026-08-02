#!/usr/bin/env python3
"""Build representation-preserving Stage B macro perturbation fixtures."""

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

PARAPHRASES = {
    "current_git_branch": "branch_currently_checked_out",
    "ci_status": "continuous_integration_result",
    "network_api_approval": "permission_to_use_external_model_api",
    "do_not_infer_current_git_branch": "do_not_guess_branch_currently_checked_out",
    "do_not_infer_ci_status": "do_not_guess_continuous_integration_result",
    "do_not_infer_network_api_approval": "do_not_guess_permission_to_use_external_model_api",
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def dump_json(path: Path, payload: Any) -> None:
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def replace_key(value: Any, old: str, new: str) -> Any:
    if isinstance(value, dict):
        return {
            (new if key == old else key): replace_key(item, old, new)
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [replace_key(item, old, new) for item in value]
    return value


def replace_exact_values(value: Any, replacements: dict[str, str]) -> Any:
    if isinstance(value, dict):
        return {
            key: replace_exact_values(item, replacements)
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [replace_exact_values(item, replacements) for item in value]
    if isinstance(value, str):
        return replacements.get(value, value)
    return value


def remove_evidence_id(value: Any, evidence_id: str, field: str) -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            if key == field and isinstance(item, list):
                value[key] = [entry for entry in item if entry != evidence_id]
            else:
                remove_evidence_id(item, evidence_id, field)
    elif isinstance(value, list):
        for item in value:
            remove_evidence_id(item, evidence_id, field)


def first_evidence_id(evidence_bundle: dict[str, Any]) -> str:
    return str(evidence_bundle["items"][0]["evidence_id"])


def distractor_id(evidence_bundle: dict[str, Any]) -> str:
    prefix = first_evidence_id(evidence_bundle).rsplit("-e", 1)[0]
    return f"{prefix}-e10"


def configure_condition(
    *,
    condition: str,
    task_spec: dict[str, Any],
    memory_slice: dict[str, Any],
    evidence_bundle: dict[str, Any],
    output_contract: dict[str, Any],
    golden: dict[str, Any],
    input_text: str,
) -> tuple[dict[str, Any], str, dict[str, list[str]]]:
    bad = copy.deepcopy(golden)
    expectations: dict[str, list[str]]

    if condition == "canonical":
        state = bad["state_inventory"]["known_state"][0]
        state["evidence_ids"] = []
        expectations = {"missing_required_known_state_evidence": ["state_accuracy"]}
        return bad, "missing_required_known_state_evidence", expectations

    if condition == "evidence-order-shuffled":
        evidence_bundle["items"].reverse()
        missing_id = first_evidence_id(
            {"items": list(reversed(evidence_bundle["items"]))}
        )
        remove_evidence_id(bad["grounded_claims"], missing_id, "evidence_ids")
        expectations = {"missing_grounded_claim_evidence": ["citation_grounding"]}
        return bad, "missing_grounded_claim_evidence", expectations

    if condition == "field-alias":
        output_contract["field_aliases"] = {"source_references": "evidence_ids"}
        output_contract["required_surface_aliases"] = {
            "evidence_ids": "source_references"
        }
        output_contract["required_nested_fields"] = replace_exact_values(
            output_contract.get("required_nested_fields", {}),
            {"evidence_ids": "source_references"},
        )
        task_spec["constraints"] = [
            str(item).replace("evidence_ids", "source_references")
            for item in task_spec.get("constraints", [])
        ]
        task_spec["success_conditions"] = [
            str(item).replace("evidence IDs", "source references")
            for item in task_spec.get("success_conditions", [])
        ]
        input_text = input_text.replace("evidence_ids", "source_references")
        golden.clear()
        golden.update(replace_key(copy.deepcopy(bad), "evidence_ids", "source_references"))
        bad = copy.deepcopy(golden)
        missing_id = first_evidence_id(evidence_bundle)
        remove_evidence_id(
            bad["grounded_claims"], missing_id, "source_references"
        )
        expectations = {"missing_aliased_claim_evidence": ["citation_grounding"]}
        return bad, "missing_aliased_claim_evidence", expectations

    if condition == "unknown-state-paraphrase":
        output_contract["value_aliases"] = {
            alias: canonical for canonical, alias in PARAPHRASES.items()
        }
        output_contract["required_surface_values"] = list(PARAPHRASES.values())
        for canonical, alias in PARAPHRASES.items():
            task_spec["constraints"] = [
                str(item).replace(canonical, alias)
                for item in task_spec.get("constraints", [])
            ]
        normalized_memory = replace_exact_values(memory_slice, PARAPHRASES)
        memory_slice.clear()
        memory_slice.update(normalized_memory)
        golden.clear()
        golden.update(replace_exact_values(copy.deepcopy(bad), PARAPHRASES))
        bad = copy.deepcopy(golden)
        bad["state_inventory"]["unknown_state"] = [
            item
            for item in bad["state_inventory"]["unknown_state"]
            if item != PARAPHRASES["network_api_approval"]
        ]
        expectations = {"missing_paraphrased_unknown_state": ["state_accuracy"]}
        return bad, "missing_paraphrased_unknown_state", expectations

    if condition == "distractor-evidence":
        extra_id = distractor_id(evidence_bundle)
        output_contract["forbidden_support_evidence_ids"] = [extra_id]
        evidence_bundle["items"].append(
            {
                "evidence_id": extra_id,
                "type": "EXTRACTED",
                "claim": "A neighboring team reported that a separate workflow passed an internal demonstration.",
                "source": "unrelated_neighboring_workflow_note.md",
                "relevance": "distractor_only_not_valid_support_for_this_macro",
            }
        )
        for claim in bad["grounded_claims"]:
            claim["evidence_ids"] = [extra_id]
        bad["selected_claim"]["evidence_ids"] = [extra_id]
        expectations = {
            "distractor_used_as_primary_support": [
                "citation_grounding",
                "trace_completeness",
            ]
        }
        return bad, "distractor_used_as_primary_support", expectations

    raise ValueError(f"Unknown condition: {condition}")


def build_fixture(base_dir: Path, output_dir: Path, macro: str, condition: str) -> str:
    source = base_dir / macro
    fixture_name = f"{macro}--{condition}"
    target = output_dir / fixture_name
    target.mkdir(parents=True, exist_ok=True)

    for name in ["task_spec.json", "memory_slice.json", "evidence_bundle.json", "output_contract.json"]:
        shutil.copyfile(source / name, target / name)

    task_spec = load_json(target / "task_spec.json")
    memory_slice = load_json(target / "memory_slice.json")
    evidence_bundle = load_json(target / "evidence_bundle.json")
    output_contract = load_json(target / "output_contract.json")
    golden = load_json(source / "golden_output.json")
    input_text = (source / "input.md").read_text(encoding="utf-8")

    bad, bad_name, expectations = configure_condition(
        condition=condition,
        task_spec=task_spec,
        memory_slice=memory_slice,
        evidence_bundle=evidence_bundle,
        output_contract=output_contract,
        golden=golden,
        input_text=input_text,
    )

    if condition == "field-alias":
        input_text = input_text.replace("evidence_ids", "source_references")
    if condition == "unknown-state-paraphrase":
        for canonical, alias in PARAPHRASES.items():
            input_text = input_text.replace(canonical, alias)

    task_spec["perturbation_condition"] = condition
    task_spec["base_macro"] = macro
    output_contract["perturbation_condition"] = condition

    dump_json(target / "task_spec.json", task_spec)
    dump_json(target / "memory_slice.json", memory_slice)
    dump_json(target / "evidence_bundle.json", evidence_bundle)
    dump_json(target / "output_contract.json", output_contract)
    dump_json(target / "golden_output.json", golden)
    (target / "input.md").write_text(input_text, encoding="utf-8")

    bad_dir = target / "known_bad_outputs"
    bad_dir.mkdir(exist_ok=True)
    dump_json(bad_dir / f"{bad_name}.json", bad)

    if condition == "canonical":
        undeclared = replace_key(
            copy.deepcopy(load_json(source / "golden_output.json")),
            "evidence_ids",
            "source_references",
        )
        dump_json(
            bad_dir / "undeclared_source_references.json",
            undeclared,
        )
        expectations["undeclared_source_references"] = [
            "state_accuracy",
            "citation_grounding",
        ]
    elif condition == "field-alias":
        dump_json(
            bad_dir / "canonical_field_fallback.json",
            load_json(source / "golden_output.json"),
        )
        expectations["canonical_field_fallback"] = ["schema_validity"]
    elif condition == "unknown-state-paraphrase":
        dump_json(
            bad_dir / "canonical_unknown_state_fallback.json",
            load_json(source / "golden_output.json"),
        )
        expectations["canonical_unknown_state_fallback"] = ["schema_validity"]
    elif condition == "distractor-evidence":
        mixed_support = copy.deepcopy(golden)
        extra_id = distractor_id(evidence_bundle)
        mixed_support["selected_claim"]["evidence_ids"].append(extra_id)
        dump_json(
            bad_dir / "distractor_mixed_with_valid_support.json",
            mixed_support,
        )
        expectations["distractor_mixed_with_valid_support"] = [
            "citation_grounding",
            "trace_completeness",
        ]

    dump_json(
        target / "perturbation.json",
        {
            "base_macro": macro,
            "condition": condition,
            "representation_preserving": True,
            "known_bad_expectations": expectations,
        },
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
        for macro in MACROS
        for condition in CONDITIONS
    ]
    dump_json(
        output_dir / "suite.json",
        {
            "suite_id": "stage7_post_freeze_perturbation_suite_v1",
            "macros": MACROS,
            "conditions": CONDITIONS,
            "fixture_count": len(fixtures),
            "fixtures": fixtures,
        },
    )
    print(f"Built {len(fixtures)} perturbation fixtures under {output_dir}")


if __name__ == "__main__":
    main()
