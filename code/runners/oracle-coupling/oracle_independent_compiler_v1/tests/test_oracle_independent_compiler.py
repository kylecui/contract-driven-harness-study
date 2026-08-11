from __future__ import annotations

import copy
import json
import sys
import unittest
from collections import Counter
from dataclasses import replace
from pathlib import Path


EXPERIMENT_ROOT = Path(__file__).resolve().parents[1]
AUDIT_CODE_ROOT = EXPERIMENT_ROOT.parent
REPO_ROOT = AUDIT_CODE_ROOT.parents[2]
FEC_ROOT = AUDIT_CODE_ROOT / "failure_to_executable_contract_v2"
FIXTURE_PATH = REPO_ROOT / "fixtures" / "oracle-coupling" / "failure_to_executable_contract_v2.json"
CORPUS_PATH = REPO_ROOT / "data" / "reproduction" / "oracle-coupling" / "failure_to_executable_contract_v2" / "candidate_corpus.json"
sys.path.insert(0, str(FEC_ROOT))
sys.path.insert(0, str(EXPERIMENT_ROOT))

from contract_gate import executable_gate  # noqa: E402
from public_input import (  # noqa: E402
    forbidden_paths,
    project_public_fixture,
    public_fixture_to_dict,
)
from public_policy_compiler import (  # noqa: E402
    CompilationError,
    canonical_candidate,
    compile_contract,
)
from run_experiment import (  # noqa: E402
    BASE_SOURCE_COMMIT,
    build_manifest,
    counterfactual_audit,
    dynamic_independence_audit,
    reference_negative_control,
    static_source_audit,
)
from verify_manifest import (  # noqa: E402
    EXPECTED_MANIFEST_PATHS,
    verify_manifest_payload,
)


class PublicPolicyCompilerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fixtures = json.loads(
            FIXTURE_PATH.read_text(encoding="utf-8")
        )["fixtures"]
        cls.corpus = json.loads(
            CORPUS_PATH.read_text(
                encoding="utf-8"
            )
        )

    def test_core_static_leakage_audit(self) -> None:
        result = static_source_audit()
        self.assertTrue(result["passed"], result)

    def test_projection_removes_answer_and_label_bearing_fields(self) -> None:
        for raw in self.fixtures:
            poisoned = copy.deepcopy(raw)
            poisoned["gold"] = {"decision": "poison"}
            poisoned["answer_key"] = {"decision": "poison"}
            poisoned["obligations"]["required_decision_evidence_ids"] = ["poison"]
            poisoned["obligations"]["distractor_evidence_ids"] = ["poison"]
            projected = public_fixture_to_dict(project_public_fixture(poisoned))
            self.assertEqual([], forbidden_paths(projected), raw["fixture_id"])

    def test_all_fixtures_compile_after_answer_deletion(self) -> None:
        for raw in self.fixtures:
            scrubbed = copy.deepcopy(raw)
            scrubbed.pop("expected_output")
            contract = compile_contract(project_public_fixture(scrubbed))
            self.assertEqual(raw["fixture_id"], contract.task_id)

    def test_dynamic_deletion_and_poisoning_invariance(self) -> None:
        result = dynamic_independence_audit(self.fixtures)
        self.assertTrue(result["passed"], result)
        self.assertEqual(28, result["compile_after_label_deletion_identical"])
        self.assertEqual(
            28,
            result[
                "compile_after_label_and_label_bearing_field_poisoning_identical"
            ],
        )

    def test_deliberately_coupled_reference_is_a_negative_control(self) -> None:
        result = reference_negative_control(self.fixtures)
        self.assertTrue(result["passed"], result)
        self.assertEqual(28, result["compile_failures_after_answer_deletion"])
        self.assertEqual(28, result["contracts_changed_after_answer_field_poisoning"])

    def test_canonical_contract_matches_all_frozen_task_labels(self) -> None:
        decisions = Counter()
        for raw in self.fixtures:
            contract = compile_contract(project_public_fixture(raw))
            self.assertEqual(
                raw["expected_output"],
                canonical_candidate(contract),
                raw["fixture_id"],
            )
            decisions[contract.expected_decision] += 1
        self.assertEqual({"apply": 13, "block": 15}, dict(decisions))

    def test_all_valid_and_invalid_candidate_artifacts(self) -> None:
        contracts = {
            raw["fixture_id"]: compile_contract(project_public_fixture(raw))
            for raw in self.fixtures
        }
        counts = Counter()
        for row in self.corpus:
            accepted = executable_gate(contracts[row["fixture_id"]], row["value"]).accepted
            counts[(row["label"], accepted)] += 1
        self.assertEqual(56, counts[("valid", True)])
        self.assertEqual(0, counts[("valid", False)])
        self.assertEqual(336, counts[("invalid", False)])
        self.assertEqual(0, counts[("invalid", True)])

    def test_public_input_counterfactuals_change_decisions(self) -> None:
        result = counterfactual_audit(self.fixtures)
        self.assertTrue(result["passed"], result)
        self.assertEqual(7, result["case_count"])

    def test_unsupported_family_fails_closed(self) -> None:
        public = project_public_fixture(self.fixtures[0])
        with self.assertRaisesRegex(CompilationError, "unsupported family"):
            compile_contract(replace(public, family="unregistered_family"))

    def test_ambiguous_editable_paths_fail_closed(self) -> None:
        public = project_public_fixture(self.fixtures[0])
        extra = public.immutable_paths[0]
        with self.assertRaisesRegex(CompilationError, "exactly one editable path"):
            compile_contract(
                replace(
                    public,
                    editable_paths=public.editable_paths + (extra,),
                    immutable_paths=public.immutable_paths[1:],
                )
            )

    def test_duplicate_evidence_identifiers_and_manifest_mutants_fail_closed(self) -> None:
        public = project_public_fixture(self.fixtures[0])
        duplicated = public.evidence + (copy.deepcopy(public.evidence[0]),)
        with self.assertRaisesRegex(CompilationError, "unique"):
            compile_contract(replace(public, evidence=duplicated))

        baseline = build_manifest(BASE_SOURCE_COMMIT)
        self.assertEqual(15, len(EXPECTED_MANIFEST_PATHS))
        self.assertEqual([], verify_manifest_payload(baseline))

        omitted = copy.deepcopy(baseline)
        omitted_path = omitted["entries"].pop()["path"]
        omitted["entry_count"] = len(omitted["entries"])
        with self.subTest(mutant="omission"):
            failures = verify_manifest_payload(omitted)
            self.assertIn(f"paths:missing:{omitted_path}", failures)

        duplicate = copy.deepcopy(baseline)
        duplicate["entries"][-1] = copy.deepcopy(duplicate["entries"][0])
        with self.subTest(mutant="duplicate"):
            self.assertIn("schema:duplicate_path", verify_manifest_payload(duplicate))

        parent_escape = copy.deepcopy(baseline)
        parent_escape["entries"][0]["path"] = "../manifest-escape"
        with self.subTest(mutant="parent_escape"):
            self.assertIn(
                "path:parent:../manifest-escape",
                verify_manifest_payload(parent_escape),
            )

        absolute = copy.deepcopy(baseline)
        absolute["entries"][0]["path"] = "/tmp/oic-manifest-escape"
        with self.subTest(mutant="absolute_path"):
            self.assertIn(
                "path:absolute:/tmp/oic-manifest-escape",
                verify_manifest_payload(absolute),
            )

        changed_hash = copy.deepcopy(baseline)
        changed_hash["entries"][0]["sha256"] = "0" * 64
        with self.subTest(mutant="hash"):
            self.assertTrue(any(
                failure.startswith("sha256:")
                for failure in verify_manifest_payload(changed_hash)
            ))

        changed_bytes = copy.deepcopy(baseline)
        changed_bytes["entries"][0]["bytes"] += 1
        with self.subTest(mutant="bytes"):
            self.assertTrue(any(
                failure.startswith("bytes:")
                for failure in verify_manifest_payload(changed_bytes)
            ))

        wrong_version = copy.deepcopy(baseline)
        wrong_version["manifest_version"] = "OIC-v1"
        with self.subTest(mutant="version"):
            self.assertIn(
                "schema:manifest_version",
                verify_manifest_payload(wrong_version),
            )


if __name__ == "__main__":
    unittest.main()
