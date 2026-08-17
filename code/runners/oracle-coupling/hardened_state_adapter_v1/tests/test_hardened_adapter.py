#!/usr/bin/env python3
"""Adversarial tests for the hardened local JSON state adapter."""

from __future__ import annotations

import copy
import hashlib
import json
import multiprocessing
import os
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any
from unittest.mock import patch

try:
    import fcntl
except ImportError:  # Windows lacks POSIX advisory locks; see class skip below.
    fcntl = None


ROOT = Path(__file__).resolve().parents[1]
AUDIT_CODE_ROOT = ROOT.parent
REPO_ROOT = AUDIT_CODE_ROOT.parents[2]
FEC_ROOT = AUDIT_CODE_ROOT / "failure_to_executable_contract_v2"
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(FEC_ROOT))
sys.path.insert(0, str(AUDIT_CODE_ROOT))

from contract_gate import ExecutableContract, executable_gate  # noqa: E402
from run_offline_verification import build_candidates  # noqa: E402
from hardened_state_adapter_v1.verify_manifest import (  # noqa: E402
    build_manifest_payload,
    canonical_json,
    verify_manifest_payload,
)
import hardened_adapter  # noqa: E402
from hardened_adapter import (  # noqa: E402
    AdapterError,
    CommitOutcomeUnknownError,
    ConcurrentModificationError,
    StateTargetError,
    execute_hardened,
    initialize_state_file,
    normalize_and_freeze_candidate,
    read_state_snapshot,
)


FIXTURES_PATH = REPO_ROOT / "fixtures" / "oracle-coupling" / "failure_to_executable_contract_v2.json"


def load_apply_fixture() -> dict[str, Any]:
    fixtures = json.loads(FIXTURES_PATH.read_text(encoding="utf-8"))["fixtures"]
    return next(item for item in fixtures if item["expected_output"]["decision"] == "apply")


def load_block_fixture() -> dict[str, Any]:
    fixtures = json.loads(FIXTURES_PATH.read_text(encoding="utf-8"))["fixtures"]
    return next(item for item in fixtures if item["expected_output"]["decision"] == "block")


class PhasedPatchList(list[dict[str, Any]]):
    """Expose a benign iterator first, then an unauthorized patch."""

    def __init__(
        self,
        safe: list[dict[str, Any]],
        malicious: list[dict[str, Any]],
    ) -> None:
        super().__init__(safe)
        self.safe = safe
        self.malicious = malicious
        self.iteration_count = 0

    def __iter__(self):  # type: ignore[override]
        self.iteration_count += 1
        values = self.safe if self.iteration_count <= 2 else self.malicious
        return iter(values)


def contention_worker(
    state_path_text: str,
    expected_snapshot_hash: str,
    nonce: str,
    start_event: Any,
    output_queue: Any,
) -> None:
    """Execute the same version-zero transition in a cooperating process."""

    fixture = load_apply_fixture()
    contract = ExecutableContract.compile(fixture)
    start_event.wait(10)
    try:
        trace = execute_hardened(
            contract,
            copy.deepcopy(fixture["expected_output"]),
            Path(state_path_text),
            expected_version=0,
            expected_snapshot_hash=expected_snapshot_hash,
            nonce=nonce,
        )
        output_queue.put({"ok": True, "trace": trace})
    except Exception as exc:  # pragma: no cover - diagnostic transport
        output_queue.put(
            {"ok": False, "error": f"{type(exc).__name__}:{exc}"}
        )


@unittest.skipUnless(
    fcntl is not None,
    "hardened adapter semantics (flock, mode-bit gates, directory fsync) require POSIX",
)
class HardenedAdapterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fixture = load_apply_fixture()
        cls.contract = ExecutableContract.compile(cls.fixture)
        cls.golden = cls.fixture["expected_output"]
        cls.editable_path = cls.golden["state_patch"][0]["path"]

    def make_state(
        self,
        directory: str,
        state: dict[str, Any] | None = None,
        *,
        version: int = 0,
    ) -> Path:
        state_path = Path(directory) / "state.json"
        initialize_state_file(
            state_path,
            state if state is not None else self.contract.initial_state,
            version=version,
        )
        return state_path

    def test_valid_transition_updates_state_version_and_nonce_ledger(self) -> None:
        with tempfile.TemporaryDirectory(prefix="hsa-valid-") as directory:
            state_path = self.make_state(directory)
            before = read_state_snapshot(state_path)
            trace = execute_hardened(
                self.contract,
                copy.deepcopy(self.golden),
                state_path,
                expected_version=0,
                expected_snapshot_hash=before.envelope_hash,
                nonce="nonce-valid-0001",
            )
            snapshot = read_state_snapshot(state_path)
        self.assertTrue(trace["accepted"])
        self.assertTrue(trace["wrote"])
        self.assertEqual((trace["version_before"], trace["version_after"]), (0, 1))
        self.assertEqual(snapshot.version, 1)
        self.assertEqual(snapshot.used_nonce_count, 1)
        self.assertEqual(
            snapshot.state[self.editable_path],
            self.golden["state_patch"][0]["to"],
        )

    def test_version_cas_rejects_stale_overwrite(self) -> None:
        drifted = copy.deepcopy(self.contract.initial_state)
        drifted[self.editable_path] = "__concurrent_update__"
        with tempfile.TemporaryDirectory(prefix="hsa-stale-version-") as directory:
            state_path = self.make_state(directory, drifted, version=1)
            before = read_state_snapshot(state_path)
            trace = execute_hardened(
                self.contract,
                copy.deepcopy(self.golden),
                state_path,
                expected_version=0,
                expected_snapshot_hash="0" * 64,
                nonce="nonce-stale-0001",
            )
            after = read_state_snapshot(state_path)
        self.assertFalse(trace["accepted"])
        self.assertEqual(trace["reason_codes"], ["stale_version"])
        self.assertEqual(before.envelope_hash, after.envelope_hash)
        self.assertEqual(after.state[self.editable_path], "__concurrent_update__")

    def test_live_from_check_rejects_stale_candidate_at_current_version(self) -> None:
        drifted = copy.deepcopy(self.contract.initial_state)
        drifted[self.editable_path] = "__concurrent_update__"
        with tempfile.TemporaryDirectory(prefix="hsa-stale-from-") as directory:
            state_path = self.make_state(directory, drifted, version=1)
            before = read_state_snapshot(state_path)
            trace = execute_hardened(
                self.contract,
                copy.deepcopy(self.golden),
                state_path,
                expected_version=1,
                expected_snapshot_hash=before.envelope_hash,
                nonce="nonce-live-from-0001",
            )
            after = read_state_snapshot(state_path)
        self.assertFalse(trace["accepted"])
        self.assertIn("stale_or_fabricated_from_state", trace["reason_codes"])
        self.assertEqual(before.envelope_hash, after.envelope_hash)

    def test_snapshot_hash_cas_rejects_same_version_uncovered_state_change(self) -> None:
        with tempfile.TemporaryDirectory(prefix="hsa-snapshot-cas-") as directory:
            state_path = self.make_state(directory)
            observed = read_state_snapshot(state_path)
            envelope = json.loads(state_path.read_text(encoding="utf-8"))
            envelope["state"]["project.authorization_revoked"] = True
            state_path.write_text(
                json.dumps(envelope, ensure_ascii=False, sort_keys=True) + "\n",
                encoding="utf-8",
            )
            changed = read_state_snapshot(state_path)
            self.assertEqual(changed.version, observed.version)
            trace = execute_hardened(
                self.contract,
                copy.deepcopy(self.golden),
                state_path,
                expected_version=observed.version,
                expected_snapshot_hash=observed.envelope_hash,
                nonce="nonce-snapshot-cas-0001",
            )
            after = read_state_snapshot(state_path)
        self.assertFalse(trace["accepted"])
        self.assertEqual(trace["reason_codes"], ["stale_snapshot_hash"])
        self.assertEqual(after.envelope_hash, changed.envelope_hash)
        self.assertTrue(after.state["project.authorization_revoked"])

    def test_candidate_is_json_normalized_and_deep_frozen(self) -> None:
        candidate = copy.deepcopy(self.golden)
        frozen = normalize_and_freeze_candidate(candidate)
        candidate["decision"] = "block"
        candidate["state_patch"][0]["path"] = "system.unscoped"
        self.assertEqual(frozen["decision"], self.golden["decision"])
        self.assertEqual(frozen["state_patch"][0]["path"], self.editable_path)
        with self.assertRaises(TypeError):
            frozen["state_patch"][0]["path"] = "system.unscoped"
        with self.assertRaises(TypeError):
            dict.__setitem__(frozen, "decision", "block")
        with self.assertRaises(TypeError):
            list.__setitem__(frozen["state_patch"], 0, {})

    def test_frozen_gate_matches_reference_on_full_authored_corpus(self) -> None:
        fixtures = json.loads(FIXTURES_PATH.read_text(encoding="utf-8"))["fixtures"]
        comparisons = 0
        for fixture in fixtures:
            contract, candidates = build_candidates(fixture)
            for item in candidates:
                with self.subTest(candidate_id=item["candidate_id"]):
                    reference = executable_gate(contract, item["value"])
                    frozen = normalize_and_freeze_candidate(item["value"])
                    hardened = hardened_adapter._executable_gate_frozen(contract, frozen)
                    self.assertEqual(hardened, reference)
                    comparisons += 1
        self.assertEqual(comparisons, 392)

    def test_phased_candidate_cannot_switch_patch_after_validation(self) -> None:
        malicious_path = "system.unscoped"
        malicious_patch = [
            {
                "path": malicious_path,
                "from": None,
                "to": "__written_after_validation__",
                "evidence_ids": [],
            }
        ]
        candidate = copy.deepcopy(self.golden)
        phased = PhasedPatchList(copy.deepcopy(self.golden["state_patch"]), malicious_patch)
        candidate["state_patch"] = phased
        with tempfile.TemporaryDirectory(prefix="hsa-phased-") as directory:
            state_path = self.make_state(directory)
            before = read_state_snapshot(state_path)
            trace = execute_hardened(
                self.contract,
                candidate,
                state_path,
                expected_version=0,
                expected_snapshot_hash=before.envelope_hash,
                nonce="nonce-phased-0001",
            )
            snapshot = read_state_snapshot(state_path)
        self.assertTrue(trace["accepted"])
        self.assertNotIn(malicious_path, snapshot.state)
        self.assertEqual(snapshot.state[self.editable_path], self.golden["state_patch"][0]["to"])

    def test_mutating_original_candidate_before_replace_has_no_effect(self) -> None:
        candidate = copy.deepcopy(self.golden)

        def mutate_original() -> None:
            candidate["state_patch"][0]["path"] = "system.unscoped"
            candidate["state_patch"][0]["to"] = "__written_after_validation__"

        with tempfile.TemporaryDirectory(prefix="hsa-mutation-hook-") as directory:
            state_path = self.make_state(directory)
            before = read_state_snapshot(state_path)
            trace = execute_hardened(
                self.contract,
                candidate,
                state_path,
                expected_version=0,
                expected_snapshot_hash=before.envelope_hash,
                nonce="nonce-mutation-hook-0001",
                before_replace_hook=mutate_original,
            )
            snapshot = read_state_snapshot(state_path)
        self.assertTrue(trace["accepted"])
        self.assertNotIn("system.unscoped", snapshot.state)
        self.assertEqual(snapshot.state[self.editable_path], self.golden["state_patch"][0]["to"])

    def test_final_hash_cas_detects_noncooperating_pre_replace_change(self) -> None:
        concurrent_value = "__noncooperating_update__"
        with tempfile.TemporaryDirectory(prefix="hsa-final-cas-") as directory:
            state_path = self.make_state(directory)
            before = read_state_snapshot(state_path)

            def noncooperating_write() -> None:
                envelope = json.loads(state_path.read_text(encoding="utf-8"))
                envelope["__adapter__"]["version"] = 1
                envelope["state"][self.editable_path] = concurrent_value
                state_path.write_text(
                    json.dumps(envelope, ensure_ascii=False, sort_keys=True) + "\n",
                    encoding="utf-8",
                )

            with self.assertRaisesRegex(
                ConcurrentModificationError,
                "state_changed_before_atomic_replace",
            ):
                execute_hardened(
                    self.contract,
                    copy.deepcopy(self.golden),
                    state_path,
                    expected_version=0,
                    expected_snapshot_hash=before.envelope_hash,
                    nonce="nonce-final-cas-0001",
                    before_replace_hook=noncooperating_write,
                )
            snapshot = read_state_snapshot(state_path)
            temporary_files = list(Path(directory).glob(".state.json.*.tmp"))
        self.assertEqual(snapshot.version, 1)
        self.assertEqual(snapshot.state[self.editable_path], concurrent_value)
        self.assertEqual(snapshot.used_nonce_count, 0)
        self.assertEqual(temporary_files, [])

    def test_accepted_action_nonce_cannot_be_replayed(self) -> None:
        with tempfile.TemporaryDirectory(prefix="hsa-replay-") as directory:
            state_path = self.make_state(directory)
            before_first = read_state_snapshot(state_path)
            first = execute_hardened(
                self.contract,
                copy.deepcopy(self.golden),
                state_path,
                expected_version=0,
                expected_snapshot_hash=before_first.envelope_hash,
                nonce="nonce-replay-0001",
            )
            before_replay = read_state_snapshot(state_path)
            second = execute_hardened(
                self.contract,
                copy.deepcopy(self.golden),
                state_path,
                expected_version=1,
                expected_snapshot_hash=before_replay.envelope_hash,
                nonce="nonce-replay-0001",
            )
            after_replay = read_state_snapshot(state_path)
        self.assertTrue(first["accepted"])
        self.assertFalse(second["accepted"])
        self.assertEqual(second["reason_codes"], ["replay_nonce"])
        self.assertEqual(before_replay.envelope_hash, after_replay.envelope_hash)

    def test_accepted_block_consumes_nonce_and_replay_is_rejected(self) -> None:
        fixture = load_block_fixture()
        contract = ExecutableContract.compile(fixture)
        with tempfile.TemporaryDirectory(prefix="hsa-block-replay-") as directory:
            state_path = Path(directory) / "state.json"
            initialize_state_file(state_path, contract.initial_state)
            before = read_state_snapshot(state_path)
            first = execute_hardened(
                contract,
                copy.deepcopy(fixture["expected_output"]),
                state_path,
                expected_version=before.version,
                expected_snapshot_hash=before.envelope_hash,
                nonce="nonce-block-replay-0001",
            )
            after_first = read_state_snapshot(state_path)
            second = execute_hardened(
                contract,
                copy.deepcopy(fixture["expected_output"]),
                state_path,
                expected_version=after_first.version,
                expected_snapshot_hash=after_first.envelope_hash,
                nonce="nonce-block-replay-0001",
            )
            after_second = read_state_snapshot(state_path)
        self.assertTrue(first["accepted"])
        self.assertFalse(first["wrote"])
        self.assertEqual(after_first.version, 1)
        self.assertEqual(after_first.used_nonce_count, 1)
        self.assertFalse(second["accepted"])
        self.assertEqual(second["reason_codes"], ["replay_nonce"])
        self.assertEqual(after_first.envelope_hash, after_second.envelope_hash)

    def test_symlink_state_target_is_rejected_without_following(self) -> None:
        with tempfile.TemporaryDirectory(prefix="hsa-symlink-") as directory:
            target_path = self.make_state(directory)
            before = target_path.read_bytes()
            link_path = Path(directory) / "linked-state.json"
            link_path.symlink_to(target_path)
            target_snapshot = read_state_snapshot(target_path)
            with self.assertRaisesRegex(StateTargetError, "symlink"):
                execute_hardened(
                    self.contract,
                    copy.deepcopy(self.golden),
                    link_path,
                    expected_version=0,
                    expected_snapshot_hash=target_snapshot.envelope_hash,
                    nonce="nonce-symlink-0001",
                )
            after = target_path.read_bytes()
        self.assertEqual(before, after)

    def test_symlink_parent_component_is_rejected_without_following(self) -> None:
        with tempfile.TemporaryDirectory(prefix="hsa-parent-symlink-") as directory:
            real_parent = Path(directory) / "real"
            real_parent.mkdir()
            state_path = real_parent / "state.json"
            initialize_state_file(state_path, self.contract.initial_state)
            before = state_path.read_bytes()
            linked_parent = Path(directory) / "linked"
            linked_parent.symlink_to(real_parent, target_is_directory=True)
            linked_state = linked_parent / "state.json"
            snapshot = read_state_snapshot(state_path)
            with self.assertRaisesRegex(StateTargetError, "symlink_path_component"):
                execute_hardened(
                    self.contract,
                    copy.deepcopy(self.golden),
                    linked_state,
                    expected_version=snapshot.version,
                    expected_snapshot_hash=snapshot.envelope_hash,
                    nonce="nonce-parent-symlink-0001",
                )
            after = state_path.read_bytes()
        self.assertEqual(before, after)

    def test_group_or_world_writable_parent_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory(prefix="hsa-parent-mode-") as directory:
            state_path = self.make_state(directory)
            snapshot = read_state_snapshot(state_path)
            os.chmod(directory, 0o777)
            try:
                with self.assertRaisesRegex(StateTargetError, "untrusted_parent_permissions"):
                    execute_hardened(
                        self.contract,
                        copy.deepcopy(self.golden),
                        state_path,
                        expected_version=snapshot.version,
                        expected_snapshot_hash=snapshot.envelope_hash,
                        nonce="nonce-parent-mode-0001",
                    )
            finally:
                os.chmod(directory, 0o700)

    def test_pre_replace_exception_leaves_valid_old_state(self) -> None:
        def interrupt() -> None:
            raise OSError("simulated pre-replace interruption")

        with tempfile.TemporaryDirectory(prefix="hsa-interrupt-") as directory:
            state_path = self.make_state(directory)
            snapshot_before = read_state_snapshot(state_path)
            before = state_path.read_bytes()
            with self.assertRaisesRegex(OSError, "simulated pre-replace interruption"):
                execute_hardened(
                    self.contract,
                    copy.deepcopy(self.golden),
                    state_path,
                    expected_version=0,
                    expected_snapshot_hash=snapshot_before.envelope_hash,
                    nonce="nonce-interrupt-0001",
                    before_replace_hook=interrupt,
                )
            after = state_path.read_bytes()
            parsed = json.loads(after.decode("utf-8"))
            temporary_files = list(Path(directory).glob(".state.json.*.tmp"))
        self.assertEqual(before, after)
        self.assertEqual(parsed["__adapter__"]["version"], 0)
        self.assertEqual(temporary_files, [])

    def test_post_replace_directory_fsync_failure_is_explicit_commit_unknown(self) -> None:
        with tempfile.TemporaryDirectory(prefix="hsa-commit-unknown-") as directory:
            state_path = self.make_state(directory)
            before = read_state_snapshot(state_path)
            captured: CommitOutcomeUnknownError | None = None
            with patch.object(
                hardened_adapter,
                "_fsync_directory",
                side_effect=OSError("simulated directory fsync failure"),
            ):
                with self.assertRaisesRegex(
                    CommitOutcomeUnknownError,
                    "replace_completed_but_directory_fsync_failed",
                ) as raised:
                    execute_hardened(
                        self.contract,
                        copy.deepcopy(self.golden),
                        state_path,
                        expected_version=before.version,
                        expected_snapshot_hash=before.envelope_hash,
                        nonce="nonce-commit-unknown-0001",
                    )
                captured = raised.exception
            observed = read_state_snapshot(state_path)
        self.assertIsNotNone(captured)
        self.assertTrue(captured.replacement_completed)
        self.assertFalse(captured.durable_directory_entry_confirmed)
        self.assertFalse(captured.retry_safe_without_reconciliation)
        self.assertEqual(observed.version, 1)
        self.assertEqual(observed.used_nonce_count, 1)
        self.assertEqual(
            observed.state[self.editable_path],
            self.golden["state_patch"][0]["to"],
        )

    def test_hostile_same_user_replace_window_remains_a_known_boundary(self) -> None:
        """Characterize the residual final-hash-check to replace race."""

        concurrent_path = "project.concurrent_marker"
        original_replace = os.replace
        with tempfile.TemporaryDirectory(prefix="hsa-replace-window-") as directory:
            state_path = self.make_state(directory)
            before = read_state_snapshot(state_path)

            def race_at_replace(source: Any, destination: Any) -> None:
                envelope = json.loads(state_path.read_text(encoding="utf-8"))
                envelope["state"][concurrent_path] = "lost"
                state_path.write_text(
                    json.dumps(envelope, ensure_ascii=False, sort_keys=True) + "\n",
                    encoding="utf-8",
                )
                original_replace(source, destination)

            with patch.object(hardened_adapter.os, "replace", side_effect=race_at_replace):
                trace = execute_hardened(
                    self.contract,
                    copy.deepcopy(self.golden),
                    state_path,
                    expected_version=before.version,
                    expected_snapshot_hash=before.envelope_hash,
                    nonce="nonce-replace-window-0001",
                )
            after = read_state_snapshot(state_path)
        self.assertTrue(trace["accepted"])
        self.assertNotIn(concurrent_path, after.state)

    def test_same_user_can_split_advisory_lock_inode_in_trusted_parent(self) -> None:
        """Characterize why stable parent namespace is a required boundary."""

        with tempfile.TemporaryDirectory(prefix="hsa-lock-inode-") as directory:
            state_path = self.make_state(directory)
            lock_path = state_path.with_name(state_path.name + ".lock")
            first_fd = os.open(lock_path, os.O_CREAT | os.O_RDWR, 0o600)
            second_fd = -1
            try:
                fcntl.flock(first_fd, fcntl.LOCK_EX)
                first_inode = os.fstat(first_fd).st_ino
                lock_path.unlink()
                second_fd = os.open(lock_path, os.O_CREAT | os.O_RDWR, 0o600)
                fcntl.flock(second_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                second_inode = os.fstat(second_fd).st_ino
                self.assertNotEqual(first_inode, second_inode)
            finally:
                if second_fd >= 0:
                    fcntl.flock(second_fd, fcntl.LOCK_UN)
                    os.close(second_fd)
                fcntl.flock(first_fd, fcntl.LOCK_UN)
                os.close(first_fd)

    def test_unauthorized_alias_traversal_and_reserved_paths_are_rejected(self) -> None:
        candidates: list[tuple[str, dict[str, Any], str]] = []
        for label, path, expected_reason in (
            ("unauthorized", "system.unscoped", "unauthorized_write_path"),
            ("slash_alias", self.editable_path.replace(".", "/"), "noncanonical_or_traversal_path"),
            (
                "traversal",
                f"{self.editable_path}/../system.owner",
                "noncanonical_or_traversal_path",
            ),
            ("metadata", "__adapter__.version", "reserved_path"),
            ("envelope", "state.value", "reserved_path"),
        ):
            candidate = copy.deepcopy(self.golden)
            candidate["state_patch"][0]["path"] = path
            candidates.append((label, candidate, expected_reason))
        extra_metadata = copy.deepcopy(self.golden)
        extra_metadata["__adapter__"] = {"version": 999}
        candidates.append(("top_level_metadata", extra_metadata, "reserved_top_level_metadata"))

        for index, (label, candidate, expected_reason) in enumerate(candidates):
            with self.subTest(label=label):
                with tempfile.TemporaryDirectory(prefix=f"hsa-path-{label}-") as directory:
                    state_path = self.make_state(directory)
                    before = read_state_snapshot(state_path)
                    trace = execute_hardened(
                        self.contract,
                        candidate,
                        state_path,
                        expected_version=0,
                        expected_snapshot_hash=before.envelope_hash,
                        nonce=f"nonce-path-{index:04d}",
                    )
                    after = read_state_snapshot(state_path)
                self.assertFalse(trace["accepted"])
                self.assertTrue(any(expected_reason in reason for reason in trace["reason_codes"]))
                self.assertEqual(before.envelope_hash, after.envelope_hash)

    @unittest.skipUnless(os.name == "posix", "fcntl advisory locks require POSIX")
    def test_cooperating_processes_serialize_and_only_one_cas_wins(self) -> None:
        context = multiprocessing.get_context("fork")
        with tempfile.TemporaryDirectory(prefix="hsa-process-") as directory:
            state_path = self.make_state(directory)
            initial_snapshot = read_state_snapshot(state_path)
            start_event = context.Event()
            output_queue = context.Queue()
            processes = [
                context.Process(
                    target=contention_worker,
                    args=(
                        str(state_path),
                        initial_snapshot.envelope_hash,
                        f"nonce-process-{index:04d}",
                        start_event,
                        output_queue,
                    ),
                )
                for index in range(2)
            ]
            for process in processes:
                process.start()
            start_event.set()
            results = [output_queue.get(timeout=15) for _ in processes]
            for process in processes:
                process.join(timeout=15)
                self.assertEqual(process.exitcode, 0)
            snapshot = read_state_snapshot(state_path)
        self.assertTrue(all(result["ok"] for result in results), results)
        traces = [result["trace"] for result in results]
        self.assertEqual(sum(trace["accepted"] for trace in traces), 1)
        self.assertEqual(
            sum(trace["reason_codes"] == ["stale_version"] for trace in traces),
            1,
        )
        self.assertEqual(snapshot.version, 1)
        self.assertEqual(snapshot.used_nonce_count, 1)

    def test_invalid_nonce_fails_closed_before_state_write(self) -> None:
        with tempfile.TemporaryDirectory(prefix="hsa-nonce-shape-") as directory:
            state_path = self.make_state(directory)
            before = read_state_snapshot(state_path)
            with self.assertRaisesRegex(AdapterError, "invalid_nonce"):
                execute_hardened(
                    self.contract,
                    copy.deepcopy(self.golden),
                    state_path,
                    expected_version=0,
                    expected_snapshot_hash=before.envelope_hash,
                    nonce="short",
                )
            after = read_state_snapshot(state_path)
        self.assertEqual(before.envelope_hash, after.envelope_hash)


class ManifestClosureTests(unittest.TestCase):
    @staticmethod
    def rehash(payload: dict[str, Any], key: str, root_key: str) -> None:
        payload[root_key] = hashlib.sha256(
            canonical_json(payload[key]).encode("utf-8")
        ).hexdigest()

    def test_manifest_omission_and_duplicate_mutants_are_rejected(self) -> None:
        omitted = build_manifest_payload()
        omitted["entries"].pop()
        omitted["entry_count"] = len(omitted["entries"])
        self.rehash(omitted, "entries", "entries_root_sha256")
        omitted_result = verify_manifest_payload(omitted)
        self.assertFalse(omitted_result["passed"])
        self.assertIn("schema:entries:exact_path_set", omitted_result["failures"])

        duplicate = build_manifest_payload()
        duplicate["external_inputs"].append(
            copy.deepcopy(duplicate["external_inputs"][0])
        )
        duplicate["external_input_count"] = len(duplicate["external_inputs"])
        self.rehash(
            duplicate, "external_inputs", "external_inputs_root_sha256"
        )
        duplicate_result = verify_manifest_payload(duplicate)
        self.assertFalse(duplicate_result["passed"])
        self.assertIn(
            "schema:external_inputs:duplicate_path", duplicate_result["failures"]
        )

    def test_manifest_schema_injection_is_rejected(self) -> None:
        injected = build_manifest_payload()
        injected["forged"] = True
        observed = verify_manifest_payload(injected)
        self.assertFalse(observed["passed"])
        self.assertIn("schema:exact_top_level_keys", observed["failures"])


if __name__ == "__main__":
    unittest.main()
