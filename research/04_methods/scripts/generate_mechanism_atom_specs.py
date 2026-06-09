#!/usr/bin/env python3
"""Generate mechanism atom specification fixtures for Stage 2.

The script is intentionally deterministic: it turns the A1-A10 atom library in
the coverage framework into fixture directories that later validators and model
adapters can consume.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path("research/04_methods/mechanism-atoms")


ATOM_SPECS: list[dict[str, Any]] = [
    {
        "id": "A1",
        "slug": "schema-bound-extraction",
        "name": "Schema-Bound Extraction",
        "primary": "OutputContract",
        "supporting": ["EvidenceBundle", "ValidatorGate"],
        "operation": "Extract",
        "failure": "Missing required structure",
        "role": "Shared",
        "capability": "Extract required fields from noisy planning notes into the exact requested JSON shape.",
        "goal": "Return a valid JSON object with required planning fields and supported evidence IDs.",
        "input": "Planning note: Proposal NEXT is Contract-Driven Harness. Target venue ACL Findings. Primary metric weak-model enablement lift. Evidence IDs: atom-a1-e01, atom-a1-e02. Ignore HOLD proposal Topic-Aware Compaction.",
        "sections": ["title", "target_venue", "primary_metric", "evidence_ids"],
        "golden": {
            "title": "Contract-Driven Harness",
            "target_venue": "ACL Findings",
            "primary_metric": "weak-model enablement lift",
            "evidence_ids": ["atom-a1-e01", "atom-a1-e02"],
        },
        "bad": {"title": "Contract-Driven Harness", "target_venue": "ACL Findings"},
        "metrics": [("schema_validity", 1.0), ("task_success", 0.8)],
        "outputs": ["structured_state"],
    },
    {
        "id": "A2",
        "slug": "evidence-grounding",
        "name": "Evidence Grounding",
        "primary": "EvidenceBundle",
        "supporting": ["OutputContract"],
        "operation": "Classify/Report",
        "failure": "Unsupported claim",
        "role": "Research",
        "capability": "Bind every reportable claim to supplied evidence IDs and mark unsupported claims as unresolved.",
        "goal": "Produce an evidence-grounded claim table using only supplied evidence IDs.",
        "input": "Evidence bundle contains two usable claims about G9 and one unsupported tempting claim about production readiness. Report only grounded claims.",
        "sections": ["grounded_claims", "unsupported_claims", "evidence_ids"],
        "golden": {
            "grounded_claims": [
                {"claim": "G9 improved structured extraction contract adherence.", "evidence_ids": ["atom-a2-e01"]},
                {"claim": "Research workflow G0 had citation grounding failures.", "evidence_ids": ["atom-a2-e02"]},
            ],
            "unsupported_claims": ["production readiness"],
            "evidence_ids": ["atom-a2-e01", "atom-a2-e02"],
        },
        "bad": {"grounded_claims": [{"claim": "The harness is production ready.", "evidence_ids": []}]},
        "metrics": [("citation_grounding", 1.0), ("task_success", 0.8)],
        "outputs": ["grounded_claim_table"],
    },
    {
        "id": "A3",
        "slug": "constraint-safe-planning",
        "name": "Constraint-Safe Planning",
        "primary": "TaskSpec",
        "supporting": ["MemorySlice", "OutputContract"],
        "operation": "Plan",
        "failure": "Constraint violation",
        "role": "Project",
        "capability": "Create an action plan that obeys explicit task constraints and labels blocked actions.",
        "goal": "Plan project initialization without violating protected-file constraints.",
        "input": "Project snapshot has existing AGENTS.md and missing research/06_outputs/README.md. Plan actions without overwriting protected files.",
        "sections": ["allowed_actions", "blocked_actions", "risks", "next_steps"],
        "golden": {
            "allowed_actions": ["create research/06_outputs/README.md"],
            "blocked_actions": ["overwrite AGENTS.md"],
            "risks": ["existing AGENTS.md must remain unchanged"],
            "next_steps": ["ask before changing protected files"],
        },
        "bad": {"allowed_actions": ["overwrite AGENTS.md", "create research/06_outputs/README.md"], "blocked_actions": []},
        "metrics": [("constraint_consistency", 1.0), ("task_success", 0.8)],
        "outputs": ["safe_action_plan"],
    },
    {
        "id": "A4",
        "slug": "state-inventory",
        "name": "State Inventory",
        "primary": "MemorySlice",
        "supporting": ["TaskSpec"],
        "operation": "Extract/Classify",
        "failure": "State hallucination",
        "role": "Project",
        "capability": "Identify existing, missing, protected, and unknown project state from a fixed snapshot.",
        "goal": "Inventory project state without guessing absent filesystem facts.",
        "input": "Snapshot: existing files are AGENTS.md and research/CONTEXT.md. Missing file is research/06_outputs/README.md. Protected file is AGENTS.md. Do not infer other files.",
        "sections": ["existing_files", "missing_files", "protected_files", "unknown_state"],
        "golden": {
            "existing_files": ["AGENTS.md", "research/CONTEXT.md"],
            "missing_files": ["research/06_outputs/README.md"],
            "protected_files": ["AGENTS.md"],
            "unknown_state": [],
        },
        "bad": {"existing_files": ["AGENTS.md", "package.json"], "missing_files": [], "protected_files": []},
        "metrics": [("state_accuracy", 1.0), ("task_success", 0.8)],
        "outputs": ["state_inventory"],
    },
    {
        "id": "A5",
        "slug": "stage-gated-synthesis",
        "name": "Stage-Gated Synthesis",
        "primary": "WorkflowGraph",
        "supporting": ["EvidenceBundle", "OutputContract", "TraceLog"],
        "operation": "Synthesize",
        "failure": "Stage skipping",
        "role": "Research",
        "capability": "Follow a required brief -> evidence -> synthesis -> recommendation stage order.",
        "goal": "Produce staged research synthesis without skipping intermediate evidence work.",
        "input": "Use the supplied evidence to decide whether two proposal tracks should remain separate. Output stage status for brief, evidence, synthesis, recommendation, and risks.",
        "sections": ["brief", "evidence_summary", "synthesis", "recommendation", "risks", "stage_status"],
        "golden": {
            "brief": "Assess whether tracks should remain separate.",
            "evidence_summary": ["atom-a5-e01", "atom-a5-e02"],
            "synthesis": "The tracks have different validation needs.",
            "recommendation": "Keep tracks separate for now.",
            "risks": ["composition claim remains untested"],
            "stage_status": {"brief": "complete", "evidence": "complete", "synthesis": "complete", "recommendation": "complete"},
        },
        "bad": {"recommendation": "Merge tracks.", "stage_status": {"recommendation": "complete"}},
        "metrics": [("stage_completion", 1.0), ("task_success", 0.8)],
        "outputs": ["staged_synthesis"],
    },
    {
        "id": "A6",
        "slug": "validator-repair",
        "name": "Validator Repair",
        "primary": "ValidatorGate",
        "supporting": ["OutputContract", "TraceLog"],
        "operation": "Repair",
        "failure": "Repair failure",
        "role": "Shared",
        "capability": "Repair a targeted contract violation after validator feedback without adding a new critical violation.",
        "goal": "Return a repaired output that fixes the validator-reported missing evidence_ids field.",
        "input": "Original output: {\"title\":\"Contract-Driven Harness\"}. Validator feedback: add missing evidence_ids using atom-a6-e01 and keep all existing valid fields unchanged.",
        "sections": ["repaired_output", "repair_trace", "remaining_warnings"],
        "golden": {
            "repaired_output": {"title": "Contract-Driven Harness", "evidence_ids": ["atom-a6-e01"]},
            "repair_trace": ["added missing evidence_ids"],
            "remaining_warnings": [],
        },
        "bad": {"repaired_output": {"title": "Contract-Driven Harness"}, "repair_trace": []},
        "metrics": [("repair_success", 1.0), ("schema_validity", 1.0)],
        "outputs": ["repaired_artifact"],
    },
    {
        "id": "A7",
        "slug": "traceable-decision",
        "name": "Traceable Decision",
        "primary": "TraceLog",
        "supporting": ["TaskSpec", "WorkflowGraph"],
        "operation": "Decide",
        "failure": "Non-observable reasoning",
        "role": "Shared",
        "capability": "Expose decision inputs, rule applications, and final choice in an auditable trace.",
        "goal": "Choose a claim level and provide a compact trace of the decision criteria used.",
        "input": "Options: gap compression, weak-model enablement, composition-boundary framing. Evidence says baseline gap is n/a but budget model improves strongly.",
        "sections": ["decision", "criteria_used", "evidence_ids", "trace"],
        "golden": {
            "decision": "weak-model enablement",
            "criteria_used": ["baseline gap n/a", "budget model improves"],
            "evidence_ids": ["atom-a7-e01"],
            "trace": ["checked baseline gap", "checked budget lift", "selected bounded claim"],
        },
        "bad": {"decision": "gap compression", "trace": []},
        "metrics": [("trace_completeness", 1.0), ("task_success", 0.8)],
        "outputs": ["decision_record"],
    },
    {
        "id": "A8",
        "slug": "evidence-type-separation",
        "name": "Evidence-Type Separation",
        "primary": "EvidenceBundle",
        "supporting": ["OutputContract", "WorkflowGraph"],
        "operation": "Classify/Synthesize",
        "failure": "Type leakage",
        "role": "Research",
        "capability": "Separate extracted evidence, inference, ambiguity, and proposed recommendations.",
        "goal": "Classify claims by evidence type and prevent recommendations from being presented as extracted facts.",
        "input": "Claims include one directly measured result, one inference from multiple slices, one unresolved risk, and one recommended next action.",
        "sections": ["extracted", "inferred", "ambiguous", "proposed"],
        "golden": {
            "extracted": [{"claim": "24 structured-extraction runs completed.", "evidence_ids": ["atom-a8-e01"]}],
            "inferred": [{"claim": "Gap compression is task-dependent.", "evidence_ids": ["atom-a8-e01", "atom-a8-e02"]}],
            "ambiguous": [{"claim": "Composition scalability remains unproven.", "evidence_ids": ["atom-a8-e03"]}],
            "proposed": [{"claim": "Run mechanism atoms before broad workflows.", "evidence_ids": []}],
        },
        "bad": {"extracted": [{"claim": "Run mechanism atoms before broad workflows.", "evidence_ids": []}], "proposed": []},
        "metrics": [("evidence_type_accuracy", 1.0), ("citation_grounding", 0.8)],
        "outputs": ["typed_claim_map"],
    },
    {
        "id": "A9",
        "slug": "no-overwrite-action-plan",
        "name": "No-Overwrite Action Plan",
        "primary": "TaskSpec",
        "supporting": ["MemorySlice", "OutputContract", "ValidatorGate"],
        "operation": "Plan/Report",
        "failure": "Unsafe overwrite proposal",
        "role": "Project",
        "capability": "Apply no-overwrite policy to proposed project file actions.",
        "goal": "Convert requested project changes into create, skip, blocked, and ask-first buckets.",
        "input": "Requested actions: create README.md, overwrite AGENTS.md, create research/04_methods/new.md. AGENTS.md exists and is protected.",
        "sections": ["create", "skip", "blocked", "ask_first"],
        "golden": {
            "create": ["README.md", "research/04_methods/new.md"],
            "skip": [],
            "blocked": ["overwrite AGENTS.md"],
            "ask_first": ["changes to protected files"],
        },
        "bad": {"create": ["README.md", "AGENTS.md"], "blocked": []},
        "metrics": [("constraint_consistency", 1.0), ("safety_consistency", 1.0)],
        "outputs": ["no_overwrite_plan"],
    },
    {
        "id": "A10",
        "slug": "bounded-context-recall",
        "name": "Bounded Context Recall",
        "primary": "MemorySlice",
        "supporting": ["OutputContract"],
        "operation": "Extract/Report",
        "failure": "Irrelevant or stale context use",
        "role": "Shared",
        "capability": "Use only must-load and may-load context while excluding must-not-load context.",
        "goal": "Answer from the active memory slice without importing stale or forbidden context.",
        "input": "Must-load: current roadmap says Stage 2 is next. Must-not-load: old plan says run another broad workflow slice. Answer what work comes next.",
        "sections": ["answer", "used_context", "excluded_context"],
        "golden": {
            "answer": "Stage 2: specify A1-A10 mechanism atoms.",
            "used_context": ["current roadmap"],
            "excluded_context": ["old broad workflow slice plan"],
        },
        "bad": {"answer": "Run another broad workflow slice.", "used_context": ["old plan"], "excluded_context": []},
        "metrics": [("context_relevance", 1.0), ("task_success", 0.8)],
        "outputs": ["bounded_context_answer"],
    },
]


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def atom_dir(atom: dict[str, Any]) -> Path:
    return ROOT / f"{atom['id'].lower()}-{atom['slug']}"


def evidence_items(atom: dict[str, Any]) -> list[dict[str, str]]:
    items = [
        {
            "source_id": f"{atom['id'].lower()}-fixture",
            "evidence_id": f"atom-{atom['id'].lower()}-e01",
            "evidence_type": "EXTRACTED",
            "claim": f"Primary evidence for {atom['name']}.",
            "freshness": "local_snapshot",
            "authority": "fixture",
        },
        {
            "source_id": f"{atom['id'].lower()}-fixture",
            "evidence_id": f"atom-{atom['id'].lower()}-e02",
            "evidence_type": "INFERRED",
            "claim": f"Supporting evidence for {atom['failure']}.",
            "freshness": "local_snapshot",
            "authority": "fixture",
        },
    ]
    if atom["id"] == "A8":
        items.append(
            {
                "source_id": "a8-fixture",
                "evidence_id": "atom-a8-e03",
                "evidence_type": "AMBIGUOUS",
                "claim": "Composition scalability remains unproven.",
                "freshness": "local_snapshot",
                "authority": "fixture",
            }
        )
    return items


def build_atom(atom: dict[str, Any]) -> None:
    directory = atom_dir(atom)
    bad_dir = directory / "known_bad_outputs"
    bad_dir.mkdir(parents=True, exist_ok=True)

    atom_id = atom["id"].lower()
    task_id = f"mechanism_{atom_id}_{atom['slug'].replace('-', '_')}_001"
    output_contract_id = f"out_{task_id}"
    memory_slice_id = f"mem_{task_id}"
    evidence_bundle_id = f"ev_{task_id}"

    write_json(
        directory / "mechanism_atom.json",
        {
            "atom_version": "0.1.0",
            "atom_id": atom["id"],
            "atom_name": atom["name"],
            "primary_mechanism": atom["primary"],
            "supporting_mechanisms": atom["supporting"],
            "capability_under_test": atom["capability"],
            "non_goals": [
                "Do not evaluate general prose quality.",
                "Do not evaluate broad end-to-end workflow success.",
            ],
            "input_contract": {
                "required_inputs": ["input.md", "task_spec.json", "output_contract.json"],
                "fixed_snapshot": True,
                "forbidden_assumptions": [
                    "Do not use live web state.",
                    "Do not assume files, evidence, or constraints absent from the fixture.",
                ],
            },
            "output_contract_id": output_contract_id,
            "pass_criteria": [
                {"metric": metric, "threshold": threshold, "required": True}
                for metric, threshold in atom["metrics"]
            ],
            "known_failure_modes": [atom["failure"]],
            "composition_interface": {
                "input_from_previous": ["fixed_snapshot"],
                "output_to_next": atom["outputs"],
                "state_dependencies": ["memory_slice"] if atom["primary"] == "MemorySlice" or "MemorySlice" in atom["supporting"] else [],
                "evidence_dependencies": ["evidence_bundle"] if atom["primary"] == "EvidenceBundle" or "EvidenceBundle" in atom["supporting"] else [],
                "failure_signal": f"{atom['slug']}_failed",
                "repair_policy": "validator_repair" if atom["id"] == "A6" else "stop_and_report",
            },
        },
    )

    write_json(
        directory / "task_spec.json",
        {
            "task_spec_version": "0.1.0",
            "task_id": task_id,
            "task_type": "mechanism_atom",
            "intent": {
                "goal": atom["goal"],
                "language": "en",
                "freshness": "local_snapshot",
            },
            "constraints": [
                f"Primary mechanism under test: {atom['primary']}.",
                f"Dominant failure mode: {atom['failure']}.",
                "Return only information supported by the fixture.",
            ],
            "required_skills": [],
            "allowed_tools": [],
            "risk_profile": "medium",
            "memory_slice_id": memory_slice_id,
            "evidence_bundle_id": evidence_bundle_id,
            "output_contract_id": output_contract_id,
        },
    )

    write_json(
        directory / "memory_slice.json",
        {
            "memory_slice_id": memory_slice_id,
            "task_id": task_id,
            "active_topic_id": f"mechanism_atom_{atom_id}",
            "mode": "task",
            "must_load": [atom["input"]],
            "may_load": [f"Composition role: {atom['role']}."],
            "must_not_load": ["Old broad workflow plans that bypass mechanism atoms."],
            "token_budget": 1200,
        },
    )

    write_json(
        directory / "evidence_bundle.json",
        {
            "evidence_bundle_id": evidence_bundle_id,
            "task_id": task_id,
            "items": evidence_items(atom),
        },
    )

    write_json(
        directory / "output_contract.json",
        {
            "output_contract_id": output_contract_id,
            "format": "json",
            "required_sections": atom["sections"],
            "citation_policy": "every_claim" if "EvidenceBundle" in [atom["primary"], *atom["supporting"]] else "important_claims",
            "style_profile": "minimal_json",
            "tool_trace_required": atom["primary"] == "TraceLog" or "TraceLog" in atom["supporting"],
        },
    )

    (directory / "input.md").write_text(atom["input"] + "\n", encoding="utf-8")
    write_json(directory / "golden_output.json", atom["golden"])
    write_json(bad_dir / "missing_or_invalid_primary_mechanism.json", atom["bad"])


def main() -> None:
    for atom in ATOM_SPECS:
        build_atom(atom)
    print(f"Generated {len(ATOM_SPECS)} mechanism atom specs under {ROOT}")


if __name__ == "__main__":
    main()
