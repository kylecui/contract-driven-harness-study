#!/usr/bin/env python3
"""Render the discriminating policy-source audit figure from frozen artifacts."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path

import matplotlib as mpl

mpl.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle


plt.rcParams.update(
    {
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"],
        "svg.fonttype": "none",
        "pdf.fonttype": 42,
        "font.size": 5.7,
        "axes.titlesize": 7.1,
        "axes.labelsize": 5.7,
        "xtick.labelsize": 5.3,
        "ytick.labelsize": 5.3,
        "axes.linewidth": 0.7,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "legend.frameon": False,
    }
)


ROOT = Path(__file__).resolve().parents[3]
FEC_OFFLINE_SUMMARY = (
    ROOT
    / "data"
    / "reproduction"
    / "oracle-coupling"
    / "failure_to_executable_contract_v2"
    / "offline_verification_summary.json"
)
OIC_RESULTS = (
    ROOT
    / "data"
    / "reproduction"
    / "oracle-coupling"
    / "oracle_independent_compiler_v1"
    / "artifacts"
    / "results.json"
)
METAMORPHIC_PROTOCOL = (
    ROOT
    / "data"
    / "reproduction"
    / "oracle-coupling"
    / "metamorphic_public_input_v1"
    / "artifacts"
    / "protocol.json"
)
METAMORPHIC_CASES = (
    ROOT
    / "data"
    / "reproduction"
    / "oracle-coupling"
    / "metamorphic_public_input_v1"
    / "artifacts"
    / "cases.json"
)
METAMORPHIC_RESULTS = (
    ROOT
    / "data"
    / "reproduction"
    / "oracle-coupling"
    / "metamorphic_public_input_v1"
    / "artifacts"
    / "results.json"
)
EXTERNAL_PROTOCOL = (
    ROOT
    / "data"
    / "reproduction"
    / "oracle-coupling"
    / "invariant_external_boundary_v1"
    / "artifacts"
    / "protocol.json"
)
EXTERNAL_RESULTS = (
    ROOT
    / "data"
    / "reproduction"
    / "oracle-coupling"
    / "invariant_external_boundary_v1"
    / "artifacts"
    / "results.json"
)
EXTERNAL_SOURCE_SNAPSHOT = (
    ROOT
    / "data"
    / "reproduction"
    / "oracle-coupling"
    / "invariant_external_boundary_v1"
    / "artifacts"
    / "source_snapshot.json"
)

DEFAULT_OUT = ROOT / "paper" / "figures"
DEFAULT_SOURCE_DATA = ROOT / "data" / "analysis" / "oracle-coupling" / "figure-source-data.json"
DEFAULT_PREFIX = "figure-oracle-coupling-audit"

FIG_WIDTH_MM = 178
FIG_HEIGHT_MM = 112
MM_PER_INCH = 25.4

INK = "#17212B"
MUTED = "#65717D"
HAIRLINE = "#D7DDE3"
PANEL_BG = "#F6F8FA"
WHITE = "#FFFFFF"

COUPLED = "#A84642"
COUPLED_FILL = "#F8E9E7"
PUBLIC = "#245A8D"
PUBLIC_FILL = "#E7EFF6"
EXTERNAL = "#4D7474"
EXTERNAL_FILL = "#E9F1F0"

PASS = "#2F7D57"
PASS_FILL = "#E6F2EB"
BOUNDARY = "#6D737A"
BOUNDARY_FILL = "#EEF0F2"
ACCENT = "#C28B2C"
ACCENT_FILL = "#F7F0E1"


TRANSFORMATION_LABELS = {
    "rename_domain_identifiers": "Rename domain identifiers",
    "rename_evidence_identifiers": "Rename evidence identifiers",
    "insert_irrelevant_evidence": "Insert irrelevant evidence",
    "compose_invariant_transforms": "Compose all three",
    "remove_authority": "Remove authority",
    "mismatch_authority_target": "Mismatch authority target",
    "mismatch_authorized_destination": "Mismatch destination",
    "mismatch_authority_scope": "Mismatch authority scope",
    "expire_authority": "Expire authority",
}

# Coarse three-action granularity used by the paper prose (§4.14: "removing,
# retargeting, or expiring authority"). Every sensitivity family maps to
# exactly one action; the mapping is asserted in extract_source_data().
SENSITIVITY_ACTION_GROUPS: list[tuple[str, list[str]]] = [
    ("remove", ["remove_authority"]),
    (
        "retarget",
        [
            "mismatch_authority_target",
            "mismatch_authorized_destination",
            "mismatch_authority_scope",
        ],
    ),
    ("expire", ["expire_authority"]),
]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relative_path(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def passed_count(rows: list[dict]) -> int:
    return sum(bool(row.get("passed")) for row in rows)


def extract_source_data() -> dict:
    """Build a compact, checked figure ledger from frozen artifacts."""

    oic = load_json(OIC_RESULTS)
    fec_summary = load_json(FEC_OFFLINE_SUMMARY)
    metamorphic_protocol = load_json(METAMORPHIC_PROTOCOL)
    metamorphic_cases_artifact = load_json(METAMORPHIC_CASES)
    metamorphic = load_json(METAMORPHIC_RESULTS)
    external_protocol = load_json(EXTERNAL_PROTOCOL)
    external = load_json(EXTERNAL_RESULTS)
    external_snapshot = load_json(EXTERNAL_SOURCE_SNAPSHOT)

    assert oic["overall_passed"] is True
    assert metamorphic["overall_passed"] is True
    assert external["overall_passed"] is True
    assert all(external["coverage_gate"].values())
    assert external["source_commit"] == external_snapshot["source_commit"]
    assert external["source_license_sha256"] == external_snapshot["license_sha256"]

    # Panel a: matched interventions at three distinct policy/evaluator boundaries.
    reference = oic["coupled_reference_negative_control"]
    public = oic["dynamic_leakage_audit"]
    public_facts = oic["public_input_counterfactuals"]
    task_units = reference["fixture_count"]
    assert reference["passed"] is True and public["passed"] is True
    assert public_facts["passed"] is True
    assert task_units == public["fixture_count"]
    assert reference["compile_failures_after_answer_deletion"] == task_units
    assert reference["contracts_changed_after_answer_field_poisoning"] == task_units
    assert public["compile_after_label_deletion_identical"] == task_units
    assert (
        public["compile_after_label_and_label_bearing_field_poisoning_identical"]
        == task_units
    )
    assert passed_count(public_facts["cases"]) == public_facts["case_count"]
    public_fact_base_fixture_count = len(
        {row["fixture_id"] for row in public_facts["cases"]}
    )
    assert public_fact_base_fixture_count == 4

    excluded_keys = set(oic["input_boundary"]["explicitly_excluded_keys"])
    assert {"answer_key", "expected_output", "gold"}.issubset(excluded_keys)
    assert (
        external_protocol["external_evaluator_boundary"]["excluded_argument"]
        == "answer_label_payload"
    )

    # FEC-v2 authored-oracle reference: the frozen offline corpus it must
    # reproduce (task labels via fixture parity; candidate classifications
    # via the executable-contract arm accepting every valid candidate and
    # blocking every invalid one).
    assert fec_summary["protocol_id"] == "FEC-v2-offline-mechanism-verification"
    assert fec_summary["fixture_count"] == task_units
    fec_arm = fec_summary["summary"]["executable_contract"]
    assert fec_summary["valid_candidate_count"] + fec_summary[
        "invalid_candidate_count"
    ] == fec_summary["candidate_count"]
    assert fec_arm["valid_accepted"] == fec_summary["valid_candidate_count"]
    assert fec_arm["invalid_blocked"] == fec_summary["invalid_candidate_count"]
    reference_reproduction = {
        "task_fixture_count": fec_summary["fixture_count"],
        "candidate_classifications": fec_summary["candidate_count"],
        "valid_accepted": fec_arm["valid_accepted"],
        "invalid_blocked": fec_arm["invalid_blocked"],
    }

    label_groups = external["label_invariance_groups"]
    public_relations = external["public_fact_relations"]
    policy_relations = external.get("policy_source_relations", [])
    assert passed_count(label_groups) == len(label_groups)
    assert passed_count(public_relations) == len(public_relations)
    if policy_relations:
        assert passed_count(policy_relations) == len(policy_relations)

    # Panel b: recompute relation counts directly from case-level outcomes.
    assert metamorphic_cases_artifact["protocol_id"] == metamorphic["protocol_id"]
    metamorphic_cases = metamorphic_cases_artifact["cases"]
    assert all(row["passed"] for row in metamorphic_cases)
    totals_by_transform = Counter(row["transformation"] for row in metamorphic_cases)
    passed_by_transform = Counter(
        row["transformation"] for row in metamorphic_cases if row["passed"]
    )
    assert dict(totals_by_transform) == metamorphic["by_transformation"]

    invariant_relations = metamorphic_protocol["invariant_relations"]
    sensitivity_sets = metamorphic_protocol["sensitivity_relations"]
    sensitivity_relations = []
    for relation_group in sensitivity_sets.values():
        for relation in relation_group:
            if relation not in sensitivity_relations:
                sensitivity_relations.append(relation)

    invariant_rows = [
        {
            "transformation": relation,
            "display_label": TRANSFORMATION_LABELS[relation],
            "passed": passed_by_transform[relation],
            "total": totals_by_transform[relation],
            "kind": "composed" if relation.startswith("compose_") else "primitive",
        }
        for relation in invariant_relations
    ]
    sensitivity_rows = [
        {
            "transformation": relation,
            "display_label": TRANSFORMATION_LABELS[relation],
            "passed": passed_by_transform[relation],
            "total": totals_by_transform[relation],
        }
        for relation in sensitivity_relations
    ]
    invariant_total = sum(row["total"] for row in invariant_rows)
    sensitivity_total = sum(row["total"] for row in sensitivity_rows)
    assert invariant_total == metamorphic["invariant_case_count"]
    assert sensitivity_total == metamorphic["sensitivity_case_count"]
    assert sum(row["passed"] for row in invariant_rows) == metamorphic[
        "invariant_cases_passed"
    ]
    assert sum(row["passed"] for row in sensitivity_rows) == metamorphic[
        "sensitivity_cases_passed"
    ]

    # Group the sensitivity families into the paper's three coarse actions
    # (remove / retarget / expire); every family maps to exactly one action.
    grouped_relations: list[str] = []
    for _, relations in SENSITIVITY_ACTION_GROUPS:
        grouped_relations.extend(relations)
    assert sorted(grouped_relations) == sorted(sensitivity_relations)
    rows_by_relation = {row["transformation"]: row for row in sensitivity_rows}
    action_groups = []
    for action, relations in SENSITIVITY_ACTION_GROUPS:
        group_rows = [rows_by_relation[relation] for relation in relations]
        action_groups.append(
            {
                "action": action,
                "relations": list(relations),
                "passed": sum(row["passed"] for row in group_rows),
                "total": sum(row["total"] for row in group_rows),
            }
        )
    assert sum(group["total"] for group in action_groups) == sensitivity_total
    assert sum(group["passed"] for group in action_groups) == metamorphic[
        "sensitivity_cases_passed"
    ]

    # Panel c: preserve policy-level grouping so calls remain visibly nested.
    label_groups_by_policy: dict[str, list[dict]] = defaultdict(list)
    for group in label_groups:
        label_groups_by_policy[group["base_case_id"]].append(group)
    public_relations_by_policy = {
        row["base_case_id"]: row for row in public_relations
    }
    policy_relations_by_policy = {
        row["base_case_id"]: row for row in policy_relations
    }
    policy_ids = sorted(label_groups_by_policy)
    assert len(policy_ids) == external["base_case_count"]

    external_policy_rows = []
    for policy_id in policy_ids:
        groups = label_groups_by_policy[policy_id]
        external_policy_rows.append(
            {
                "policy_id": policy_id,
                "label_groups_passed": passed_count(groups),
                "label_group_total": len(groups),
                "public_fact_relation_passed": bool(
                    public_relations_by_policy[policy_id]["passed"]
                ),
                "public_fact_baseline_decision": next(
                    group["decision"]
                    for group in groups
                    if group["public_condition"] == "baseline_public_trace"
                ),
                "public_fact_edited_decision": next(
                    group["decision"]
                    for group in groups
                    if group["public_condition"] == "paired_public_fact_edit"
                ),
                "policy_source_relation_passed": (
                    bool(policy_relations_by_policy[policy_id]["passed"])
                    if policy_id in policy_relations_by_policy
                    else None
                ),
            }
        )

    source_files = {
        "fec_offline_summary": FEC_OFFLINE_SUMMARY,
        "same_team_boundary_results": OIC_RESULTS,
        "metamorphic_protocol": METAMORPHIC_PROTOCOL,
        "metamorphic_cases": METAMORPHIC_CASES,
        "metamorphic_results": METAMORPHIC_RESULTS,
        "external_boundary_protocol": EXTERNAL_PROTOCOL,
        "external_boundary_results": EXTERNAL_RESULTS,
        "external_source_snapshot": EXTERNAL_SOURCE_SNAPSHOT,
    }

    return {
        "figure_contract": {
            "core_conclusion": (
                "The same label and public-fact interventions return contrasting "
                "prespecified results for an answer-coupled compiler and two "
                "label-separated evaluator boundaries; nested metamorphic checks "
                "test non-vacuity."
            ),
            "archetype": "schematic-led composite",
            "final_size_mm": [FIG_WIDTH_MM, FIG_HEIGHT_MM],
            "statistics": (
                "Exact deterministic counts only. Primary reporting units are "
                "fixed task fixtures and upstream policy examples; transformed "
                "conditions and evaluator calls are nested checks."
            ),
        },
        "panel_a_policy_source_intervention": {
            "same_team_task_units": task_units,
            "reference_answer_coupled": {
                "label_reaches_policy": True,
                "deletion_compile_failures": reference[
                    "compile_failures_after_answer_deletion"
                ],
                "poisoning_contract_changes": reference[
                    "contracts_changed_after_answer_field_poisoning"
                ],
                "reference_reproduction": reference_reproduction,
            },
            "same_team_public_input": {
                "label_reaches_policy": False,
                "deletion_invariant": public[
                    "compile_after_label_deletion_identical"
                ],
                "poisoning_invariant": public[
                    "compile_after_label_and_label_bearing_field_poisoning_identical"
                ],
                "public_fact_relations_passed": passed_count(public_facts["cases"]),
                "public_fact_relation_total": public_facts["case_count"],
                "public_fact_base_fixture_count": public_fact_base_fixture_count,
            },
            "external_evaluator_boundary": {
                "label_reaches_evaluator": False,
                "label_groups_passed": passed_count(label_groups),
                "label_group_total": len(label_groups),
                "public_fact_relations_passed": passed_count(public_relations),
                "public_fact_relation_total": len(public_relations),
                "boundary_label": "External boundary control; not replication",
            },
        },
        "panel_b_metamorphic_relations": {
            "primary_task_units": metamorphic["statistical_design"][
                "primary_task_level_reporting_unit_n"
            ],
            "baseline_apply_task_units": metamorphic["statistical_design"][
                "sensitivity_subset_n"
            ],
            "invariant_rows": invariant_rows,
            "invariant_passed": metamorphic["invariant_cases_passed"],
            "invariant_total": metamorphic["invariant_case_count"],
            "sensitivity_rows": sensitivity_rows,
            "sensitivity_action_groups": action_groups,
            "sensitivity_passed": metamorphic["sensitivity_cases_passed"],
            "sensitivity_total": metamorphic["sensitivity_case_count"],
            "nested_conditions_notice": metamorphic["statistical_design"][
                "repeated_measures"
            ],
        },
        "panel_c_external_boundary_control": {
            "source_commit": external["source_commit"],
            "policy_examples": external_policy_rows,
            "policy_example_count": external["base_case_count"],
            "label_groups_passed": passed_count(label_groups),
            "label_group_total": len(label_groups),
            "public_fact_relations_passed": passed_count(public_relations),
            "public_fact_relation_total": len(public_relations),
            "policy_source_relations_passed": passed_count(policy_relations),
            "policy_source_relation_total": len(policy_relations),
            "external_evaluator_calls": external["external_evaluator_call_count"],
            "model_calls": external["model_call_count"],
            "claim_boundary": external["claim_boundary"],
            "external_final_schema_complete": bool(policy_relations),
        },
        "provenance_sources": [
            {
                "role": role,
                "path": relative_path(path),
                "sha256": sha256(path),
            }
            for role, path in source_files.items()
        ],
        "provenance_sha256": {
            role: sha256(path) for role, path in source_files.items()
        },
    }


def add_card(
    ax: mpl.axes.Axes,
    x: float,
    y: float,
    width: float,
    height: float,
    *,
    facecolor: str,
    edgecolor: str = HAIRLINE,
    linewidth: float = 0.65,
    radius: float = 0.012,
    zorder: float = 1,
) -> FancyBboxPatch:
    card = FancyBboxPatch(
        (x, y),
        width,
        height,
        boxstyle=f"round,pad=0.006,rounding_size={radius}",
        facecolor=facecolor,
        edgecolor=edgecolor,
        linewidth=linewidth,
        transform=ax.transAxes,
        clip_on=False,
        zorder=zorder,
    )
    ax.add_patch(card)
    return card


def add_status_strip(
    ax: mpl.axes.Axes,
    x: float,
    y: float,
    height: float,
    color: str,
) -> None:
    ax.add_patch(
        Rectangle(
            (x, y),
            0.006,
            height,
            transform=ax.transAxes,
            facecolor=color,
            edgecolor="none",
            zorder=3,
        )
    )


def draw_panel_a(ax: mpl.axes.Axes, source: dict) -> None:
    ax.set_axis_off()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    panel = source["panel_a_policy_source_intervention"]
    task_units = panel["same_team_task_units"]

    ax.text(0.0, 1.035, "a", fontsize=8.2, weight="bold", ha="left", va="bottom")
    ax.text(
        0.025,
        1.035,
        "The paired test traces the declared policy-source boundary",
        fontsize=7.2,
        weight="bold",
        color=INK,
        ha="left",
        va="bottom",
    )

    x_system, x_access, x_labels, x_facts = 0.012, 0.275, 0.485, 0.756
    w_system, w_access, w_labels, w_facts = 0.245, 0.192, 0.253, 0.232
    header_y = 0.873
    ax.text(x_system + 0.012, header_y, "Evaluator boundary", weight="bold", color=MUTED)
    ax.text(x_access + w_access / 2, header_y, "Tested score-label\npath to policy", ha="center", weight="bold", color=MUTED)
    ax.text(x_labels + w_labels / 2, header_y, "Delete / poison\nscore label", ha="center", weight="bold", color=MUTED)
    ax.text(x_facts + w_facts / 2, header_y, "Edit policy-relevant\npublic facts", ha="center", weight="bold", color=MUTED)

    rows = [
        {
            "y": 0.605,
            "fill": COUPLED_FILL,
            "color": COUPLED,
            "title": "Answer-coupled FEC-v2",
            "subtitle": "authored-oracle compiler",
            "footnote": (
                "reference reproduces {cand}/{cand} frozen candidate classifications "
                "· {valid} valid accepted · {invalid} invalid blocked".format(
                    cand=panel["reference_answer_coupled"]["reference_reproduction"][
                        "candidate_classifications"
                    ],
                    valid=panel["reference_answer_coupled"]["reference_reproduction"][
                        "valid_accepted"
                    ],
                    invalid=panel["reference_answer_coupled"]["reference_reproduction"][
                        "invalid_blocked"
                    ],
                )
            ),
            "access_big": "OBSERVED",
            "access_small": "direct label -> policy channel",
            "label_big": f"delete: {panel['reference_answer_coupled']['deletion_compile_failures']}/{task_units}",
            "label_small": (
                "compile failures\n"
                f"poison: {panel['reference_answer_coupled']['poisoning_contract_changes']}/{task_units} contracts changed"
            ),
            "fact_big": "not queried",
            "fact_small": "known-coupled control\nscoped to label dependence",
        },
        {
            "y": 0.346,
            "fill": PUBLIC_FILL,
            "color": PUBLIC,
            "title": "Public-input compiler",
            "subtitle": "public-input control",
            "access_big": "NOT ADMITTED",
            "access_small": "keys excluded; closure checks passed",
            "label_big": f"{panel['same_team_public_input']['deletion_invariant']}/{task_units} each",
            "label_small": "contracts invariant under\ndeletion and poisoning",
            "fact_big": (
                f"{panel['same_team_public_input']['public_fact_relations_passed']}/"
                f"{panel['same_team_public_input']['public_fact_relation_total']}"
            ),
            "fact_small": (
                f"conditions over {panel['same_team_public_input']['public_fact_base_fixture_count']} fixtures\n"
                "across all three grammars"
            ),
        },
        {
            "y": 0.087,
            "fill": EXTERNAL_FILL,
            "color": EXTERNAL,
            "title": "External policy evaluator",
            "subtitle": "boundary control · not replication",
            "access_big": "NOT ADMITTED",
            "access_small": "label absent from evaluator request",
            "label_big": (
                f"{panel['external_evaluator_boundary']['label_groups_passed']}/"
                f"{panel['external_evaluator_boundary']['label_group_total']} groups"
            ),
            "label_small": "decision invariant across\noriginal / deleted / poisoned",
            "fact_big": (
                f"{panel['external_evaluator_boundary']['public_fact_relations_passed']}/"
                f"{panel['external_evaluator_boundary']['public_fact_relation_total']}"
            ),
            "fact_small": "paired public-trace\nrelations changed decision",
        },
    ]

    row_height = 0.205
    for row in rows:
        add_card(
            ax,
            x_system,
            row["y"],
            0.976,
            row_height,
            facecolor=row["fill"],
            edgecolor=HAIRLINE,
        )
        add_status_strip(ax, x_system + 0.003, row["y"] + 0.014, row_height - 0.028, row["color"])
        for xpos in (x_access - 0.009, x_labels - 0.009, x_facts - 0.009):
            ax.plot(
                [xpos, xpos],
                [row["y"] + 0.023, row["y"] + row_height - 0.023],
                color=WHITE,
                lw=1.05,
                transform=ax.transAxes,
                clip_on=False,
                zorder=2,
            )

        ax.text(
            x_system + 0.020,
            row["y"] + 0.126,
            row["title"],
            fontsize=6.25,
            weight="bold",
            color=INK,
            ha="left",
            va="center",
        )
        ax.text(
            x_system + 0.020,
            row["y"] + 0.070,
            row["subtitle"],
            fontsize=5.25,
            color=row["color"],
            ha="left",
            va="center",
        )
        if row.get("footnote"):
            ax.text(
                x_system + 0.020,
                row["y"] + 0.026,
                row["footnote"],
                fontsize=5.0,
                color=MUTED,
                ha="left",
                va="center",
            )
        ax.text(
            x_access + w_access / 2,
            row["y"] + 0.128,
            row["access_big"],
            fontsize=6.6,
            weight="bold",
            color=row["color"],
            ha="center",
            va="center",
        )
        ax.text(
            x_access + w_access / 2,
            row["y"] + 0.068,
            row["access_small"],
            fontsize=5.15,
            color=MUTED,
            ha="center",
            va="center",
        )
        ax.text(
            x_labels + w_labels / 2,
            row["y"] + 0.137,
            row["label_big"],
            fontsize=6.35,
            weight="bold",
            color=row["color"],
            ha="center",
            va="center",
        )
        ax.text(
            x_labels + w_labels / 2,
            row["y"] + 0.069,
            row["label_small"],
            fontsize=5.15,
            color=MUTED,
            ha="center",
            va="center",
            linespacing=1.18,
        )
        ax.text(
            x_facts + w_facts / 2,
            row["y"] + 0.137,
            row["fact_big"],
            fontsize=6.35,
            weight="bold",
            color=(MUTED if row["fact_big"] == "not queried" else row["color"]),
            ha="center",
            va="center",
        )
        ax.text(
            x_facts + w_facts / 2,
            row["y"] + 0.069,
            row["fact_small"],
            fontsize=5.15,
            color=MUTED,
            ha="center",
            va="center",
            linespacing=1.18,
        )


def draw_relation_list(
    ax: mpl.axes.Axes,
    rows: list[dict],
    *,
    x: float,
    y_top: float,
    width: float,
    row_gap: float,
    color: str,
    composed_fill: str | None = None,
) -> None:
    for index, row in enumerate(rows):
        y = y_top - index * row_gap
        fill = composed_fill if row.get("kind") == "composed" else WHITE
        add_card(
            ax,
            x,
            y,
            width,
            row_gap * 0.77,
            facecolor=fill or WHITE,
            edgecolor=HAIRLINE,
            radius=0.009,
        )
        ax.add_patch(
            Rectangle(
                (x + 0.010, y + row_gap * 0.215),
                0.018,
                0.018,
                transform=ax.transAxes,
                facecolor=color,
                edgecolor="none",
                zorder=4,
            )
        )
        ax.text(
            x + 0.039,
            y + row_gap * 0.39,
            row["display_label"],
            fontsize=5.25,
            color=INK,
            ha="left",
            va="center",
        )
        ax.text(
            x + width - 0.014,
            y + row_gap * 0.39,
            f"{row['passed']}/{row['total']}",
            fontsize=5.55,
            weight="bold",
            color=color,
            ha="right",
            va="center",
        )


def draw_grouped_sensitivity_list(
    ax: mpl.axes.Axes,
    panel: dict,
    *,
    x: float,
    width: float,
    color: str,
) -> None:
    """Draw the five sensitivity families inside dashed three-action groups.

    The dashed containers map the fine-grained families onto the paper's
    coarse action granularity (remove / retarget / expire) and carry the
    per-group subtotals; the family rows keep their exact per-family counts.
    """
    rows_by_relation = {
        row["transformation"]: row for row in panel["sensitivity_rows"]
    }
    row_gap = 0.092
    row_height = row_gap * 0.72
    box_pad = 0.030
    box_gap = 0.032
    top = 0.858
    for group in panel["sensitivity_action_groups"]:
        group_rows = [rows_by_relation[r] for r in group["relations"]]
        box_height = len(group_rows) * row_gap + box_pad
        box_bottom = top - box_height
        ax.add_patch(
            FancyBboxPatch(
                (x, box_bottom),
                width,
                box_height,
                boxstyle="round,pad=0.004,rounding_size=0.010",
                facecolor="none",
                edgecolor=MUTED,
                linewidth=0.55,
                linestyle=(0, (2.4, 1.9)),
                transform=ax.transAxes,
                clip_on=False,
                zorder=1,
            )
        )
        ax.text(
            x + 0.014,
            top,
            f"{group['action']} · {group['passed']}/{group['total']}",
            fontsize=5.35,
            weight="bold",
            color=color,
            ha="left",
            va="center",
            transform=ax.transAxes,
            bbox={
                "boxstyle": "square,pad=0.22",
                "facecolor": WHITE,
                "edgecolor": "none",
            },
            zorder=4,
        )
        for index, row in enumerate(group_rows):
            y = top - box_pad - index * row_gap - row_height
            add_card(
                ax,
                x + 0.020,
                y,
                width - 0.040,
                row_height,
                facecolor=WHITE,
                edgecolor=HAIRLINE,
                radius=0.009,
            )
            ax.add_patch(
                Rectangle(
                    (x + 0.032, y + row_height * 0.30),
                    0.016,
                    0.016,
                    transform=ax.transAxes,
                    facecolor=color,
                    edgecolor="none",
                    zorder=4,
                )
            )
            ax.text(
                x + 0.058,
                y + row_height * 0.5,
                row["display_label"],
                fontsize=5.25,
                color=INK,
                ha="left",
                va="center",
            )
            ax.text(
                x + width - 0.026,
                y + row_height * 0.5,
                f"{row['passed']}/{row['total']}",
                fontsize=5.55,
                weight="bold",
                color=color,
                ha="right",
                va="center",
            )
        top = box_bottom - box_gap


def draw_panel_b(ax: mpl.axes.Axes, source: dict) -> None:
    ax.set_axis_off()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    panel = source["panel_b_metamorphic_relations"]

    ax.text(0.0, 1.035, "b", fontsize=8.2, weight="bold", ha="left", va="bottom")
    ax.text(
        0.045,
        1.035,
        "Public-input metamorphic stress test",
        fontsize=7.0,
        weight="bold",
        color=INK,
        ha="left",
        va="bottom",
    )

    left_x, right_x = 0.012, 0.505
    left_w, right_w = 0.462, 0.483
    ax.text(
        left_x,
        0.905,
        f"Invariance · {panel['primary_task_units']} fixed tasks",
        fontsize=5.8,
        weight="bold",
        color=PUBLIC,
        ha="left",
        va="center",
    )
    ax.text(
        right_x,
        0.905,
        f"Fail closed · {panel['baseline_apply_task_units']} baseline-apply tasks",
        fontsize=5.8,
        weight="bold",
        color=PASS,
        ha="left",
        va="center",
    )

    draw_relation_list(
        ax,
        panel["invariant_rows"],
        x=left_x,
        y_top=0.724,
        width=left_w,
        row_gap=0.143,
        color=PUBLIC,
        composed_fill=PUBLIC_FILL,
    )
    draw_grouped_sensitivity_list(
        ax,
        panel,
        x=right_x,
        width=right_w,
        color=PASS,
    )

    add_card(
        ax,
        left_x,
        0.055,
        left_w,
        0.118,
        facecolor=PUBLIC_FILL,
        edgecolor=PUBLIC,
        radius=0.012,
    )
    ax.text(
        left_x + 0.020,
        0.118,
        f"{panel['invariant_passed']}/{panel['invariant_total']}",
        fontsize=7.1,
        weight="bold",
        color=PUBLIC,
        ha="left",
        va="center",
    )
    ax.text(
        left_x + 0.150,
        0.118,
        "nested deterministic conditions\n(3 primitive + 1 composed / task)",
        fontsize=5.15,
        color=MUTED,
        ha="left",
        va="center",
        linespacing=1.18,
    )

    add_card(
        ax,
        right_x,
        0.055,
        right_w,
        0.118,
        facecolor=PASS_FILL,
        edgecolor=PASS,
        radius=0.012,
    )
    ax.text(
        right_x + 0.020,
        0.118,
        f"{panel['sensitivity_passed']}/{panel['sensitivity_total']}",
        fontsize=7.1,
        weight="bold",
        color=PASS,
        ha="left",
        va="center",
    )
    ax.text(
        right_x + 0.155,
        0.118,
        "nested authority conditions\n(3 or 5 / task, by family)",
        fontsize=5.15,
        color=MUTED,
        ha="left",
        va="center",
        linespacing=1.18,
    )


def draw_metric_tile(
    ax: mpl.axes.Axes,
    *,
    x: float,
    y: float,
    width: float,
    height: float,
    numerator: int,
    denominator: int,
    title: str,
    subtitle: str,
    color: str,
    fill: str,
) -> None:
    add_card(
        ax,
        x,
        y,
        width,
        height,
        facecolor=fill,
        edgecolor=color,
        radius=0.012,
    )
    ax.text(
        x + 0.025,
        y + height * 0.64,
        f"{numerator}/{denominator}",
        fontsize=7.1,
        weight="bold",
        color=color,
        ha="left",
        va="center",
    )
    ax.text(
        x + 0.205,
        y + height * 0.69,
        title,
        fontsize=5.5,
        weight="bold",
        color=INK,
        ha="left",
        va="center",
    )
    ax.text(
        x + 0.205,
        y + height * 0.34,
        subtitle,
        fontsize=5.1,
        color=MUTED,
        ha="left",
        va="center",
    )


def draw_panel_c(ax: mpl.axes.Axes, source: dict) -> None:
    ax.set_axis_off()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    panel = source["panel_c_external_boundary_control"]

    ax.text(0.0, 1.035, "c", fontsize=8.2, weight="bold", ha="left", va="bottom")
    ax.text(
        0.065,
        1.035,
        "External evaluator boundary control",
        fontsize=7.0,
        weight="bold",
        color=INK,
        ha="left",
        va="bottom",
    )
    add_card(
        ax,
        0.012,
        0.852,
        0.976,
        0.095,
        facecolor=BOUNDARY_FILL,
        edgecolor=BOUNDARY,
        radius=0.012,
    )
    ax.text(
        0.035,
        0.900,
        "BOUNDARY CONTROL · NOT REPLICATION",
        fontsize=5.7,
        weight="bold",
        color=BOUNDARY,
        ha="left",
        va="center",
    )
    ax.text(
        0.965,
        0.900,
        f"pinned {panel['source_commit'][:8]}",
        fontsize=5.1,
        color=MUTED,
        ha="right",
        va="center",
    )

    draw_metric_tile(
        ax,
        x=0.012,
        y=0.662,
        width=0.976,
        height=0.145,
        numerator=panel["label_groups_passed"],
        denominator=panel["label_group_total"],
        title="label-invariance groups",
        subtitle="original / deleted / poisoned labels",
        color=EXTERNAL,
        fill=EXTERNAL_FILL,
    )
    draw_metric_tile(
        ax,
        x=0.012,
        y=0.478,
        width=0.976,
        height=0.145,
        numerator=panel["public_fact_relations_passed"],
        denominator=panel["public_fact_relation_total"],
        title="public-fact relations",
        subtitle="paired trace edit changes the decision",
        color=PASS,
        fill=PASS_FILL,
    )
    draw_metric_tile(
        ax,
        x=0.012,
        y=0.294,
        width=0.976,
        height=0.145,
        numerator=panel["policy_source_relations_passed"],
        denominator=panel["policy_source_relation_total"],
        title="policy-source relations",
        subtitle="paired policy edit changes the decision",
        color=ACCENT,
        fill=ACCENT_FILL,
    )

    add_card(
        ax,
        0.012,
        0.085,
        0.976,
        0.157,
        facecolor=PANEL_BG,
        edgecolor=HAIRLINE,
        radius=0.012,
    )
    ax.text(
        0.045,
        0.174,
        f"{panel['policy_example_count']} upstream policy examples",
        fontsize=5.7,
        weight="bold",
        color=INK,
        ha="left",
        va="center",
    )
    ax.text(
        0.045,
        0.119,
        "calls and intervention conditions are nested",
        fontsize=5.1,
        color=MUTED,
        ha="left",
        va="center",
    )
    ax.text(
        0.955,
        0.174,
        f"{panel['external_evaluator_calls']} evaluator calls",
        fontsize=5.7,
        weight="bold",
        color=EXTERNAL,
        ha="right",
        va="center",
    )
    ax.text(
        0.955,
        0.119,
        f"{panel['model_calls']} model calls",
        fontsize=5.1,
        color=MUTED,
        ha="right",
        va="center",
    )


def draw_figure(source: dict) -> mpl.figure.Figure:
    fig = plt.figure(
        figsize=(FIG_WIDTH_MM / MM_PER_INCH, FIG_HEIGHT_MM / MM_PER_INCH),
        facecolor=WHITE,
    )
    grid = fig.add_gridspec(
        2,
        2,
        height_ratios=[1.38, 1.0],
        width_ratios=[1.64, 1.0],
        left=0.025,
        right=0.988,
        bottom=0.055,
        top=0.958,
        hspace=0.19,
        wspace=0.105,
    )
    draw_panel_a(fig.add_subplot(grid[0, :]), source)
    draw_panel_b(fig.add_subplot(grid[1, 0]), source)
    draw_panel_c(fig.add_subplot(grid[1, 1]), source)
    return fig


def write_outputs(
    source: dict,
    output_dir: Path,
    prefix: str,
    source_data_path: Path,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    source_data_path.parent.mkdir(parents=True, exist_ok=True)
    source_data_path.write_text(
        json.dumps(source, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    fig = draw_figure(source)
    svg_path = output_dir / f"{prefix}.svg"
    fig.savefig(svg_path, facecolor=WHITE)
    svg_text = svg_path.read_text(encoding="utf-8")
    svg_path.write_text(
        "\n".join(line.rstrip() for line in svg_text.splitlines()) + "\n",
        encoding="utf-8",
    )
    fig.savefig(output_dir / f"{prefix}.pdf", facecolor=WHITE)
    fig.savefig(output_dir / f"{prefix}.png", dpi=600, facecolor=WHITE)
    plt.close(fig)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--prefix", default=DEFAULT_PREFIX)
    parser.add_argument("--source-data", type=Path, default=DEFAULT_SOURCE_DATA)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    source = extract_source_data()
    external_complete = source["panel_c_external_boundary_control"][
        "external_final_schema_complete"
    ]
    if not external_complete:
        raise SystemExit(
            "External boundary artifact is not final: policy_source_relations "
            "are absent. Refusing to render the figure."
        )
    write_outputs(source, args.output_dir, args.prefix, args.source_data)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
