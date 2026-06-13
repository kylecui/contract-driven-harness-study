#!/usr/bin/env python3
"""Build the Stage B v3 hierarchical output-shape repair smoke fixture."""

from __future__ import annotations

import argparse
import copy
import json
import shutil
from pathlib import Path
from typing import Any


FIXTURE_NAME = "stage7-next-method-plan-update-v3--canonical-shape-repair"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def dump_json(path: Path, payload: Any) -> None:
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def literal_skeleton() -> dict[str, Any]:
    return {
        "state_inventory": {
            "known_state": [
                {
                    "state_id": "stage7e_v4_macro_passed",
                    "fact": "<grounded fact>",
                    "evidence_ids": ["stage7next-e01"],
                },
                {
                    "state_id": "claim_boundary_updated",
                    "fact": "<grounded fact>",
                    "evidence_ids": ["stage7next-e04"],
                },
                {
                    "state_id": "methodology_outline_updated",
                    "fact": "<grounded fact>",
                    "evidence_ids": ["stage7next-e07"],
                },
                {
                    "state_id": "backlog_stage7next_open",
                    "fact": "<grounded fact>",
                    "evidence_ids": ["stage7next-e08"],
                },
            ],
            "unknown_state": [
                "current_git_branch",
                "ci_status",
                "network_api_approval",
            ],
            "forbidden_inferences": [
                "do_not_infer_current_git_branch",
                "do_not_infer_ci_status",
                "do_not_infer_network_api_approval",
                "do_not_infer_production_readiness",
                "do_not_infer_universal_model_gap_closure",
            ],
        },
        "grounded_claims": [
            {
                "claim": "<grounded claim>",
                "evidence_ids": ["<one or more supplied evidence IDs>"],
            }
        ],
        "unsupported_claims": [
            {
                "claim": "<unsupported claim>",
                "reason": "<why unsupported>",
                "evidence_ids": ["stage7next-e05"],
            }
        ],
        "typed_evidence": {
            "extracted": ["<evidence ID strings only>"],
            "inferred": ["<evidence ID strings only>"],
            "ambiguous": ["<evidence ID strings only>"],
            "proposed": ["<evidence ID strings only>"],
        },
        "selected_claim": {
            "option_id": "C2",
            "claim": "<selected bounded claim>",
            "evidence_ids": [
                "stage7next-e01",
                "stage7next-e06",
                "stage7next-e07",
                "stage7next-e08",
            ],
        },
        "rejected_options": [
            {
                "option_id": "C1",
                "reason": "<evidence-linked rejection>",
                "evidence_ids": ["<one or more supplied evidence IDs>"],
            },
            {
                "option_id": "C3",
                "reason": "<evidence-linked rejection>",
                "evidence_ids": ["<one or more supplied evidence IDs>"],
            },
        ],
        "decision_trace": [
            {
                "option_id": "C2",
                "decision": "support",
                "step": "<bounded support step>",
                "evidence_ids": [
                    "stage7next-e01",
                    "stage7next-e06",
                    "stage7next-e07",
                    "stage7next-e08",
                ],
                "carried_obligations": ["<preserved obligation>"],
            },
            {
                "option_id": "C1",
                "decision": "reject",
                "step": "<evidence-linked rejection step>",
                "evidence_ids": ["<one or more supplied evidence IDs>"],
                "carried_obligations": ["<preserved obligation>"],
            },
            {
                "option_id": "C3",
                "decision": "reject",
                "step": "<evidence-linked rejection step>",
                "evidence_ids": ["<one or more supplied evidence IDs>"],
                "carried_obligations": ["<preserved obligation>"],
            },
        ],
        "stage_gate": {
            "status": "blocked",
            "blocked_outputs": ["<required blocked outputs>"],
            "missing_prerequisites": ["<required missing prerequisites>"],
            "next_required_actions": ["<next local-first action>"],
            "evidence_ids": ["<one or more supplied evidence IDs>"],
        },
        "method_plan_update": {
            "selected_next_macro": "<bounded next macro>",
            "admission_criteria": ["<criterion>"],
            "local_gates": ["<local gate>"],
            "real_model_gate": "<real-model gate>",
            "non_claims": ["<non-claim>"],
            "evidence_ids": [
                "stage7next-e01",
                "stage7next-e06",
                "stage7next-e07",
                "stage7next-e08",
            ],
        },
        "carried_obligations": [
            {
                "obligation": "<required obligation 1>",
                "status": "preserved",
                "evidence_ids": ["<one or more supplied evidence IDs>"],
            },
            {
                "obligation": "<required obligation 2>",
                "status": "preserved",
                "evidence_ids": ["<one or more supplied evidence IDs>"],
            },
            {
                "obligation": "<required obligation 3>",
                "status": "preserved",
                "evidence_ids": ["<one or more supplied evidence IDs>"],
            },
            {
                "obligation": "<required obligation 4>",
                "status": "preserved",
                "evidence_ids": ["<one or more supplied evidence IDs>"],
            },
        ],
    }


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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-fixture", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    source = Path(args.source_fixture)
    output_root = Path(args.output_dir)
    target = output_root / FIXTURE_NAME
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(source, target)

    task_spec = load_json(target / "task_spec.json")
    evaluator_contract = load_json(target / "output_contract.json")
    model_contract = load_json(target / "model_output_contract.json")
    golden = load_json(target / "golden_output.json")
    perturbation = load_json(target / "perturbation.json")
    input_text = (target / "input.md").read_text(encoding="utf-8")

    task_spec["fixture_id"] = FIXTURE_NAME
    task_spec["protocol_version"] = "stage_b_v3_shape_repair_smoke"
    task_spec["mechanism_atom"] = "hierarchical_output_shape_preservation"
    task_spec["single_changed_factor"] = "literal_json_output_skeleton"

    evaluator_contract["output_contract_id"] = (
        "out_stage7_next_method_plan_update_stage_b_v3_shape_repair"
    )
    evaluator_contract["protocol_version"] = "stage_b_v3_shape_repair_smoke"
    evaluator_contract["mechanism_atom"] = (
        "hierarchical_output_shape_preservation"
    )
    evaluator_contract["literal_json_skeleton_required"] = True

    model_contract = copy.deepcopy(evaluator_contract)
    model_contract["output_template"] = literal_skeleton()
    model_contract["literal_json_skeleton_instructions"] = [
        "Copy the JSON key hierarchy exactly.",
        "Replace placeholder strings but never move, rename, promote, or omit keys.",
        "state_inventory must remain an object containing known_state, unknown_state, and forbidden_inferences.",
        "Do not emit unknown_state or forbidden_inferences at the root.",
    ]

    repair_block = """

## Stage B v3 Hierarchical Shape Repair

`OutputContract.output_template` is a literal JSON skeleton, not a prose
description. Copy its key hierarchy exactly and replace only placeholder
strings or placeholder array contents.

Hard shape rule:

```json
{
  "state_inventory": {
    "known_state": [],
    "unknown_state": [],
    "forbidden_inferences": []
  }
}
```

`state_inventory` must be an object. Never turn it into an array. Never promote
`unknown_state` or `forbidden_inferences` to the root. Never omit either nested
field.
""".strip()
    input_text = input_text.rstrip() + "\n\n" + repair_block + "\n"

    bad_dir = target / "known_bad_outputs"
    dump_json(bad_dir / "flattened_state_inventory.json", flattened_state(golden))
    dump_json(bad_dir / "root_promoted_state_fields.json", root_promoted_state(golden))
    dump_json(bad_dir / "omitted_nested_state_fields.json", omitted_nested_state(golden))

    expectations = perturbation.setdefault("known_bad_expectations", {})
    expectations["flattened_state_inventory"] = [
        "schema_validity",
        "state_accuracy",
    ]
    expectations["root_promoted_state_fields"] = [
        "schema_validity",
        "state_accuracy",
    ]
    expectations["omitted_nested_state_fields"] = [
        "schema_validity",
        "state_accuracy",
    ]
    perturbation.update(
        {
            "base_macro": "stage7-next-method-plan-update",
            "condition": "canonical_shape_repair",
            "suite_version": "stage_b_v3_shape_repair_smoke",
            "representation_preserving": True,
            "repair_confirmation": True,
            "mechanism_atom": "hierarchical_output_shape_preservation",
            "single_changed_factor": "literal_json_output_skeleton",
            "pooling_policy": "must_not_pool_with_stage_b_v2",
        }
    )

    dump_json(target / "task_spec.json", task_spec)
    dump_json(target / "output_contract.json", evaluator_contract)
    dump_json(target / "model_output_contract.json", model_contract)
    dump_json(target / "perturbation.json", perturbation)
    (target / "input.md").write_text(input_text, encoding="utf-8")

    dump_json(
        output_root / "suite.json",
        {
            "suite_id": "stage_b_v3_hierarchical_shape_repair_smoke",
            "fixture_count": 1,
            "fixtures": [FIXTURE_NAME],
            "mechanism_atom": "hierarchical_output_shape_preservation",
            "single_changed_factor": "literal_json_output_skeleton",
            "historical_baseline": "stage_b_v2_canonical_0_of_3",
            "pooling_policy": "must_not_pool_with_stage_b_v2",
        },
    )
    print(f"Built {FIXTURE_NAME} under {output_root}")


if __name__ == "__main__":
    main()
