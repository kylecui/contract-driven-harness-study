#!/usr/bin/env python3
"""Run the public-input compiler positive-control experiment."""

from __future__ import annotations

import ast
import copy
import hashlib
import json
import re
import sys
from collections import Counter
from collections.abc import Iterator, Mapping
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


EXPERIMENT_ROOT = Path(__file__).resolve().parent
AUDIT_CODE_ROOT = EXPERIMENT_ROOT.parent
sys.path.insert(0, str(AUDIT_CODE_ROOT))

from layout import (  # noqa: E402
    BASE_SOURCE_COMMIT,
    DATA_ROOT,
    FIXTURE_ROOT,
    REPO_ROOT,
    base_snapshot_available,
    repo_relative,
    unexpected_worktree_paths,
)

FEC_ROOT = AUDIT_CODE_ROOT / "failure_to_executable_contract_v2"
ARTIFACT_ROOT = DATA_ROOT / "oracle_independent_compiler_v1" / "artifacts"
FIXTURES_PATH = FIXTURE_ROOT / "failure_to_executable_contract_v2.json"
CORPUS_PATH = DATA_ROOT / "failure_to_executable_contract_v2" / "candidate_corpus.json"

sys.path.insert(0, str(FEC_ROOT))
sys.path.insert(0, str(EXPERIMENT_ROOT))

from contract_gate import ExecutableContract, executable_gate  # noqa: E402
from public_input import (  # noqa: E402
    FORBIDDEN_INPUT_KEYS,
    PUBLIC_OBLIGATION_FIELDS,
    PUBLIC_TOP_LEVEL_FIELDS,
    contract_to_dict,
    forbidden_paths,
    project_public_fixture,
    public_fixture_to_dict,
)
from public_policy_compiler import (  # noqa: E402
    canonical_candidate,
    compile_contract,
)
from verify_manifest import (  # noqa: E402
    EXPECTED_MANIFEST_PATHS,
    MANIFEST_VERSION,
)


CORE_PATHS = (
    EXPERIMENT_ROOT / "public_policy_compiler.py",
    EXPERIMENT_ROOT / "policy_rules.py",
)

FORBIDDEN_CORE_FRAGMENTS = (
    "expected_output",
    "gold",
    "answer_key",
    "oracle",
    "objective",
    "gate_rule",
    "required_decision_evidence_ids",
    "distractor_evidence_ids",
)

FORBIDDEN_IMPORT_ROOTS = {
    "asyncio",
    "builtins",
    "http",
    "importlib",
    "json",
    "multiprocessing",
    "os",
    "pathlib",
    "pickle",
    "shutil",
    "socket",
    "subprocess",
    "urllib",
}

FORBIDDEN_CALLS = {
    "__import__",
    "compile",
    "eval",
    "exec",
    "open",
}

FORBIDDEN_ATTRIBUTES = {
    "getenv",
    "popen",
    "read_bytes",
    "read_text",
    "system",
    "write_bytes",
    "write_text",
}


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest_value(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


class AccessTraceMapping(Mapping[str, Any]):
    """Record every key lookup made by the projection boundary."""

    def __init__(self, values: Mapping[str, Any], prefix: str, trace: list[str]) -> None:
        self._values = values
        self._prefix = prefix
        self._trace = trace

    def __getitem__(self, key: str) -> Any:
        self._trace.append(f"{self._prefix}.{key}")
        value = self._values[key]
        if key == "obligations" and isinstance(value, Mapping):
            return AccessTraceMapping(value, f"{self._prefix}.obligations", self._trace)
        return value

    def __iter__(self) -> Iterator[str]:
        return iter(self._values)

    def __len__(self) -> int:
        return len(self._values)


def static_source_audit() -> dict[str, Any]:
    token_violations: list[str] = []
    fixture_branches: list[str] = []
    import_violations: list[str] = []
    call_violations: list[str] = []
    for path in CORE_PATHS:
        source = path.read_text(encoding="utf-8")
        lower = source.lower()
        for fragment in FORBIDDEN_CORE_FRAGMENTS:
            if fragment in lower:
                token_violations.append(f"{path.name}:{fragment}")
        for match in re.finditer(r"\b[DH]-(?:ST|CFG|COMM)-\d+\b", source):
            fixture_branches.append(f"{path.name}:{match.group(0)}")
        tree = ast.parse(source, filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    root = alias.name.split(".", 1)[0]
                    if root in FORBIDDEN_IMPORT_ROOTS:
                        import_violations.append(f"{path.name}:{alias.name}")
            elif isinstance(node, ast.ImportFrom) and node.module:
                root = node.module.split(".", 1)[0]
                if root in FORBIDDEN_IMPORT_ROOTS:
                    import_violations.append(f"{path.name}:{node.module}")
            elif isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name) and node.func.id in FORBIDDEN_CALLS:
                    call_violations.append(f"{path.name}:{node.func.id}")
                elif (
                    isinstance(node.func, ast.Attribute)
                    and node.func.attr in FORBIDDEN_ATTRIBUTES
                ):
                    call_violations.append(f"{path.name}:{node.func.attr}")
    passed = not any(
        (token_violations, fixture_branches, import_violations, call_violations)
    )
    return {
        "passed": passed,
        "files": [path.name for path in CORE_PATHS],
        "forbidden_fragments": list(FORBIDDEN_CORE_FRAGMENTS),
        "token_violations": token_violations,
        "fixture_specific_literals": fixture_branches,
        "forbidden_imports": import_violations,
        "forbidden_calls": call_violations,
        "interpretation": (
            "The audited core contains no answer-label tokens, fixture identifiers, "
            "or direct file, environment, network, process, or dynamic-code access."
        ),
    }


def dynamic_independence_audit(fixtures: list[dict[str, Any]]) -> dict[str, Any]:
    deleted_identical = 0
    poisoned_identical = 0
    access_violations: list[dict[str, Any]] = []
    public_key_violations: list[dict[str, Any]] = []
    per_fixture: list[dict[str, Any]] = []
    for raw in fixtures:
        baseline = contract_to_dict(compile_contract(project_public_fixture(raw)))
        baseline_hash = digest_value(baseline)

        deleted = copy.deepcopy(raw)
        deleted.pop("expected_output", None)
        deleted_contract = contract_to_dict(
            compile_contract(project_public_fixture(deleted))
        )
        deleted_same = digest_value(deleted_contract) == baseline_hash
        deleted_identical += int(deleted_same)

        poisoned = copy.deepcopy(raw)
        poisoned["expected_output"] = {
            "decision": "__POISON__",
            "state_patch": [{"path": "__POISON__", "to": "__POISON__"}],
        }
        poisoned["gold"] = "__POISON__"
        poisoned["answer_key"] = "__POISON__"
        poisoned["objective"] = "__POISON_BLOCK_OR_APPLY__"
        poisoned["obligations"]["gate_rule"] = "__POISON__"
        poisoned["obligations"]["required_decision_evidence_ids"] = ["__POISON__"]
        poisoned["obligations"]["distractor_evidence_ids"] = ["__POISON__"]
        poison_contract = contract_to_dict(
            compile_contract(project_public_fixture(poisoned))
        )
        poisoned_same = digest_value(poison_contract) == baseline_hash
        poisoned_identical += int(poisoned_same)

        trace: list[str] = []
        traced = AccessTraceMapping(poisoned, "$", trace)
        traced_contract = contract_to_dict(
            compile_contract(project_public_fixture(traced))
        )
        traced_same = digest_value(traced_contract) == baseline_hash
        touched_forbidden = [
            path
            for path in trace
            if path.rsplit(".", 1)[-1].lower() in FORBIDDEN_INPUT_KEYS
        ]
        if touched_forbidden or not traced_same:
            access_violations.append({
                "fixture_id": raw["fixture_id"],
                "touched_forbidden": touched_forbidden,
                "traced_contract_identical": traced_same,
            })

        public_payload = public_fixture_to_dict(project_public_fixture(poisoned))
        payload_violations = forbidden_paths(public_payload)
        if payload_violations:
            public_key_violations.append({
                "fixture_id": raw["fixture_id"],
                "paths": payload_violations,
            })
        per_fixture.append({
            "fixture_id": raw["fixture_id"],
            "contract_sha256": baseline_hash,
            "deletion_identical": deleted_same,
            "poisoning_identical": poisoned_same,
            "traced_projection_identical": traced_same,
            "accessed_keys": sorted(set(trace)),
        })

    count = len(fixtures)
    return {
        "passed": (
            deleted_identical == count
            and poisoned_identical == count
            and not access_violations
            and not public_key_violations
        ),
        "fixture_count": count,
        "compile_after_label_deletion_identical": deleted_identical,
        "compile_after_label_and_label_bearing_field_poisoning_identical": poisoned_identical,
        "projection_access_violations": access_violations,
        "public_payload_forbidden_key_violations": public_key_violations,
        "per_fixture": per_fixture,
    }


def reference_negative_control(fixtures: list[dict[str, Any]]) -> dict[str, Any]:
    """Confirm that the deliberately coupled reference fails the same probes."""
    compile_failures = 0
    error_types = Counter()
    poison_changed = 0
    for raw in fixtures:
        baseline = contract_to_dict(ExecutableContract.compile(raw))
        deleted = copy.deepcopy(raw)
        deleted.pop("expected_output", None)
        try:
            ExecutableContract.compile(deleted)
        except Exception as exc:  # exception class is recorded as negative-control evidence
            compile_failures += 1
            error_types[type(exc).__name__] += 1

        poisoned = copy.deepcopy(raw)
        poisoned["expected_output"]["gate"]["reason_code"] = "__LABEL_POISON__"
        poisoned["expected_output"]["next_action"] = "__LABEL_POISON__"
        changed = contract_to_dict(ExecutableContract.compile(poisoned))
        poison_changed += int(digest_value(changed) != digest_value(baseline))

    source = (FEC_ROOT / "contract_gate.py").read_text(encoding="utf-8").lower()
    token_hits = [item for item in FORBIDDEN_CORE_FRAGMENTS if item in source]
    count = len(fixtures)
    observed = (
        compile_failures == count
        and poison_changed == count
        and "expected_output" in token_hits
    )
    return {
        "passed": observed,
        "control_role": "deliberately_answer_coupled_reference_compiler",
        "compiler_path": repo_relative(FEC_ROOT / "contract_gate.py"),
        "fixture_count": count,
        "compile_failures_after_answer_deletion": compile_failures,
        "deletion_error_types": dict(sorted(error_types.items())),
        "contracts_changed_after_answer_field_poisoning": poison_changed,
        "static_forbidden_fragment_hits": token_hits,
        "interpretation": (
            "The reference compiler fails both deletion and poisoning probes, so the "
            "positive-control invariance checks distinguish the intended dependency."
        ),
    }


def label_agreement_audit(fixtures: list[dict[str, Any]]) -> dict[str, Any]:
    mismatches: list[dict[str, Any]] = []
    counts = Counter()
    family_counts = Counter()
    split_counts = Counter()
    for raw in fixtures:
        contract = compile_contract(project_public_fixture(raw))
        derived = canonical_candidate(contract)
        reference = raw["expected_output"]
        exact = derived == reference
        counts[(reference["decision"], exact)] += 1
        family_counts[(raw["family"], reference["decision"], exact)] += 1
        split_counts[(raw["split"], exact)] += 1
        if not exact:
            mismatches.append({
                "fixture_id": raw["fixture_id"],
                "derived": derived,
                "reference": reference,
            })
    return {
        "passed": not mismatches,
        "statistical_unit": "one authored task fixture",
        "fixture_count": len(fixtures),
        "exact_contract_candidate_matches": len(fixtures) - len(mismatches),
        "apply_matches": counts[("apply", True)],
        "block_matches": counts[("block", True)],
        "by_family": [
            {
                "family": family,
                "decision": decision,
                "matched": family_counts[(family, decision, True)],
                "mismatched": family_counts[(family, decision, False)],
            }
            for family, decision in sorted({(key[0], key[1]) for key in family_counts})
        ],
        "by_split": [
            {
                "split": split,
                "matched": split_counts[(split, True)],
                "mismatched": split_counts[(split, False)],
            }
            for split in sorted({key[0] for key in split_counts})
        ],
        "mismatches": mismatches,
        "interpretation": (
            "Reference labels are used only by this evaluator after compilation; "
            "agreement is a post-hoc finite-fixture mechanism check."
        ),
    }


def mutation_corpus_audit(
    fixtures: list[dict[str, Any]], corpus: list[dict[str, Any]]
) -> dict[str, Any]:
    contracts = {
        raw["fixture_id"]: compile_contract(project_public_fixture(raw)) for raw in fixtures
    }
    valid_total = valid_accepted = invalid_total = invalid_rejected = 0
    failures: list[dict[str, Any]] = []
    for row in corpus:
        decision = executable_gate(contracts[row["fixture_id"]], row["value"])
        if row["label"] == "valid":
            valid_total += 1
            valid_accepted += int(decision.accepted)
            passed = decision.accepted
        else:
            invalid_total += 1
            invalid_rejected += int(not decision.accepted)
            passed = not decision.accepted
        if not passed:
            failures.append({
                "fixture_id": row["fixture_id"],
                "candidate_id": row["candidate_id"],
                "label": row["label"],
                "accepted": decision.accepted,
                "reason_codes": list(decision.reason_codes),
            })
    return {
        "passed": not failures,
        "task_clusters": len(fixtures),
        "candidate_artifacts": len(corpus),
        "valid_candidates_accepted": valid_accepted,
        "valid_candidates_total": valid_total,
        "invalid_mutations_rejected": invalid_rejected,
        "invalid_mutations_total": invalid_total,
        "failures": failures,
        "statistical_boundary": (
            "Candidate artifacts are deterministic within 28 task clusters and are "
            "not treated as independent population samples."
        ),
    }


def _fixture(fixtures: Mapping[str, dict[str, Any]], fixture_id: str) -> dict[str, Any]:
    return copy.deepcopy(fixtures[fixture_id])


def counterfactual_audit(fixtures: list[dict[str, Any]]) -> dict[str, Any]:
    by_id = {raw["fixture_id"]: raw for raw in fixtures}
    cases: list[tuple[str, dict[str, Any], str]] = []

    value = _fixture(by_id, "D-ST-01")
    value["evidence"] = [item for item in value["evidence"] if item["type"] != "authoritative_transition"]
    cases.append(("remove_transition_authority", value, "missing_authoritative_evidence"))

    value = _fixture(by_id, "D-ST-01")
    next(item for item in value["evidence"] if item["type"] == "authoritative_transition")[
        "claim"
    ] = "status pending -> rejected"
    cases.append(("change_transition_destination", value, "to_state_mismatch"))

    value = _fixture(by_id, "D-ST-01")
    value["request"] = "Mark project omega as approved."
    cases.append(("change_requested_target", value, "target_mismatch"))

    value = _fixture(by_id, "D-CFG-01")
    value["evidence"][0]["status"] = "expired"
    cases.append(("expire_configuration_approval", value, "approval_expired"))

    value = _fixture(by_id, "H-CFG-01")
    value["evidence"][0]["scope"] = "service.retries"
    cases.append(("change_configuration_scope", value, "approval_scope_mismatch"))

    value = _fixture(by_id, "H-COMM-01")
    value["evidence"][0]["recipient"] = "other@example.org"
    cases.append(("change_communication_recipient", value, "communication_recipient_mismatch"))

    value = _fixture(by_id, "H-COMM-01")
    value["evidence"][0]["scope"] = "restricted"
    cases.append(("change_communication_scope", value, "communication_scope_mismatch"))

    results: list[dict[str, Any]] = []
    for name, raw, expected_reason in cases:
        contract = compile_contract(project_public_fixture(raw))
        observed_reason = contract.expected_gate["reason_code"]
        passed = contract.expected_decision == "block" and observed_reason == expected_reason
        results.append({
            "case_id": name,
            "fixture_id": raw["fixture_id"],
            "changed_input_class": "public_request_or_evidence",
            "expected_decision": "block",
            "observed_decision": contract.expected_decision,
            "expected_reason": expected_reason,
            "observed_reason": observed_reason,
            "passed": passed,
        })
    return {
        "passed": all(item["passed"] for item in results),
        "case_count": len(results),
        "cases": results,
        "interpretation": (
            "Unlike label poisoning, policy-relevant public-input changes alter the "
            "derived decision in the expected direction across all three families."
        ),
    }


def build_manifest(source_commit: str) -> dict[str, Any]:
    entries = []
    for relative_path in sorted(EXPECTED_MANIFEST_PATHS):
        path = REPO_ROOT / relative_path
        if not path.is_file():
            raise FileNotFoundError(f"manifest input is missing: {relative_path}")
        entries.append({
            "path": relative_path,
            "sha256": sha256_path(path),
            "bytes": path.stat().st_size,
        })
    return {
        "manifest_version": MANIFEST_VERSION,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_snapshot_commit": source_commit,
        "entry_count": len(entries),
        "entries": entries,
    }


def main() -> None:
    fixture_payload = load_json(FIXTURES_PATH)
    fixtures = fixture_payload["fixtures"]
    corpus = load_json(CORPUS_PATH)
    source_commit = BASE_SOURCE_COMMIT
    base_available = base_snapshot_available()
    unexpected_before = unexpected_worktree_paths()

    public_payload = {
        "protocol_id": "OIC-v1-public-inputs",
        "source_fixture_sha256": sha256_path(FIXTURES_PATH),
        "input_boundary": {
            "top_level_allowlist": sorted(PUBLIC_TOP_LEVEL_FIELDS - {"obligations"}),
            "policy_constraint_allowlist": sorted(PUBLIC_OBLIGATION_FIELDS),
            "explicitly_excluded_keys": sorted(FORBIDDEN_INPUT_KEYS),
        },
        "fixtures": [public_fixture_to_dict(project_public_fixture(raw)) for raw in fixtures],
    }
    public_violations = forbidden_paths(public_payload)
    if public_violations:
        raise RuntimeError(f"public-input artifact retained forbidden keys: {public_violations}")

    contracts = [
        contract_to_dict(compile_contract(project_public_fixture(raw))) for raw in fixtures
    ]
    compiled_payload = {
        "protocol_id": "OIC-v1-compiled-contracts",
        "public_input_sha256": digest_value(public_payload),
        "contracts": contracts,
    }

    static = static_source_audit()
    dynamic = dynamic_independence_audit(fixtures)
    negative_control = reference_negative_control(fixtures)
    agreement = label_agreement_audit(fixtures)
    mutation = mutation_corpus_audit(fixtures, corpus)
    counterfactual = counterfactual_audit(fixtures)

    unexpected_after = unexpected_worktree_paths()
    overall = all(
        item["passed"]
        for item in (
            static,
            dynamic,
            negative_control,
            agreement,
            mutation,
            counterfactual,
        )
    ) and base_available and not unexpected_before and not unexpected_after

    result = {
        "protocol_id": "oracle-independent-compiler-positive-control-v1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "overall_passed": overall,
        "development_design": "post_hoc_mechanism_positive_control",
        "source_snapshot": {
            "base_commit": source_commit,
            "base_commit_is_ancestor": base_available,
            "unexpected_paths_before": unexpected_before,
            "unexpected_paths_after": unexpected_after,
            "boundary": "Only the additive oracle-coupling contribution paths may change.",
        },
        "input_boundary": public_payload["input_boundary"],
        "static_leakage_audit": static,
        "dynamic_leakage_audit": dynamic,
        "coupled_reference_negative_control": negative_control,
        "frozen_fixture_agreement": agreement,
        "candidate_mutation_check": mutation,
        "public_input_counterfactuals": counterfactual,
        "statistical_unit": {
            "primary": "one task fixture",
            "n": len(fixtures),
            "families": dict(sorted(Counter(raw["family"] for raw in fixtures).items())),
            "secondary": "392 deterministic candidate artifacts nested within 28 tasks",
            "inference": "exact descriptive counts only; no prevalence or independence claim",
        },
        "bounded_claim": (
            "For the 28 frozen single-transition fixtures in three supported grammars, "
            "a pure compiler using only allowlisted request, current-state, evidence, "
            "and path/boundary policy inputs reproduced all 28 authored decisions and "
            "all 392 candidate classifications; deleting or poisoning answer labels "
            "and preselected evidence-ID fields changed none of the 28 compiled contracts."
        ),
        "non_claims": [
            "The compiler was developed post hoc after inspecting the frozen fixture schema.",
            "The policy catalogue and fixtures were not independently authored.",
            "The result does not establish transfer to a new harness, policy family, or natural-language grammar.",
            "Static and dynamic checks reduce direct runtime leakage; they do not prove historical cognitive independence of the implementer.",
            "Agreement with authored labels does not prove that the public policy constraints are normatively correct or complete.",
            "Candidate artifacts are clustered mechanism checks, not 392 independent statistical samples.",
        ],
        "non_completion_states": [
            "independent_author_set_missing",
            "cross_harness_external_validation_missing",
            "prospective_heldout_policy_family_missing",
            "independent_human_output_review_missing",
        ],
    }

    public_path = ARTIFACT_ROOT / "public_fixtures.json"
    compiled_path = ARTIFACT_ROOT / "compiled_contracts.json"
    counterfactual_path = ARTIFACT_ROOT / "counterfactual_results.json"
    results_path = ARTIFACT_ROOT / "results.json"
    write_json(public_path, public_payload)
    write_json(compiled_path, compiled_payload)
    write_json(counterfactual_path, counterfactual)
    write_json(results_path, result)

    manifest = build_manifest(source_commit)
    write_json(ARTIFACT_ROOT / "SHA256_MANIFEST.json", manifest)

    print(json.dumps({
        "overall_passed": overall,
        "fixture_exact_matches": agreement["exact_contract_candidate_matches"],
        "fixture_count": agreement["fixture_count"],
        "valid_candidates_accepted": mutation["valid_candidates_accepted"],
        "valid_candidates_total": mutation["valid_candidates_total"],
        "invalid_mutations_rejected": mutation["invalid_mutations_rejected"],
        "invalid_mutations_total": mutation["invalid_mutations_total"],
        "label_deletion_invariant": dynamic["compile_after_label_deletion_identical"],
        "label_poisoning_invariant": dynamic[
            "compile_after_label_and_label_bearing_field_poisoning_identical"
        ],
        "negative_control_deletion_failures": negative_control[
            "compile_failures_after_answer_deletion"
        ],
        "negative_control_poison_changes": negative_control[
            "contracts_changed_after_answer_field_poisoning"
        ],
        "public_counterfactuals_passed": sum(
            item["passed"] for item in counterfactual["cases"]
        ),
        "public_counterfactual_count": counterfactual["case_count"],
        "manifest_entries": manifest["entry_count"],
    }, indent=2))
    if not overall:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
