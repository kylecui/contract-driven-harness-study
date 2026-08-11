"""Hardened JSON-file adapter for the FEC-v2 executable gate.

The adapter narrows the trusted-state assumptions exposed by stale-state,
mutable-proposal, replay, path-confusion, and interrupted-write probes. It is
deliberately limited to local JSON files and uses only the Python standard
library. The authored contract and its semantic oracle remain unchanged and
outside this adapter's claim.
"""

from __future__ import annotations

import contextlib
import copy
import dataclasses
import errno
import fcntl
import hashlib
import json
import os
import re
import stat
import tempfile
import unicodedata
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Any, Callable, Iterator


EXPERIMENT_ROOT = Path(__file__).resolve().parent
AUDIT_CODE_ROOT = EXPERIMENT_ROOT.parent
FEC_ROOT = AUDIT_CODE_ROOT / "failure_to_executable_contract_v2"

import sys

if str(FEC_ROOT) not in sys.path:
    sys.path.insert(0, str(FEC_ROOT))

from contract_gate import (  # noqa: E402
    REQUIRED_FIELDS,
    ExecutableContract,
    GateDecision,
    apply_patch_to_state,
)


FORMAT_ID = "hardened-json-state-v1"
METADATA_KEY = "__adapter__"
STATE_KEY = "state"
MAX_JSON_BYTES = 1_048_576
PATH_PATTERN = re.compile(r"[A-Za-z0-9_]+(?:\.[A-Za-z0-9_]+)*\Z")
NONCE_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:-]{7,127}\Z")
RESERVED_ROOTS = frozenset(
    {
        METADATA_KEY,
        STATE_KEY,
        "adapter_metadata",
        "metadata",
        "nonce",
        "used_nonce_sha256",
        "version",
    }
)
RESERVED_TOP_LEVEL_CANDIDATE_KEYS = frozenset(
    {METADATA_KEY, STATE_KEY, "adapter_metadata", "nonce", "version"}
)


class AdapterError(RuntimeError):
    """Base class for fail-closed adapter errors."""


class StateTargetError(AdapterError):
    """The requested state or lock target is unsafe or malformed."""


class ConcurrentModificationError(AdapterError):
    """The state changed outside the cooperative lock before replacement."""


class CommitOutcomeUnknownError(AdapterError):
    """Replacement completed but durable directory sync was not confirmed."""

    replacement_completed = True
    durable_directory_entry_confirmed = False
    retry_safe_without_reconciliation = False


@dataclass(frozen=True)
class StateSnapshot:
    """Read-only snapshot returned to a proposal-producing caller."""

    version: int
    state: MappingProxyType
    used_nonce_count: int
    envelope_hash: str


def _reject_nonfinite(_value: str) -> None:
    raise ValueError("non-finite JSON number is not permitted")


def _canonical_json_bytes(value: Any) -> bytes:
    return (
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode("utf-8")
        + b"\n"
    )


def _deep_freeze(value: Any) -> Any:
    if isinstance(value, dict):
        return MappingProxyType(
            {key: _deep_freeze(item) for key, item in value.items()}
        )
    if isinstance(value, list):
        return tuple(_deep_freeze(item) for item in value)
    return value


def normalize_and_freeze_candidate(candidate: Any) -> Mapping[str, Any]:
    """Take one JSON snapshot and reject non-JSON or oversized candidates.

    JSON round-tripping removes user-defined container behavior.  The recursive
    frozen containers then ensure that validation and application see the same
    candidate snapshot.
    """

    try:
        encoded = json.dumps(
            candidate,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode("utf-8")
    except (TypeError, ValueError, OverflowError, RecursionError) as exc:
        raise AdapterError(f"candidate_not_strict_json:{type(exc).__name__}") from exc
    if len(encoded) > MAX_JSON_BYTES:
        raise AdapterError("candidate_json_too_large")
    try:
        normalized = json.loads(encoded.decode("utf-8"), parse_constant=_reject_nonfinite)
    except (json.JSONDecodeError, ValueError, RecursionError) as exc:
        raise AdapterError(f"candidate_json_roundtrip_failed:{type(exc).__name__}") from exc
    if not isinstance(normalized, dict):
        raise AdapterError("candidate_not_an_object")
    frozen = _deep_freeze(normalized)
    if not isinstance(frozen, MappingProxyType):
        raise AssertionError("deep-freeze invariant failed")
    return frozen


def _path_reason(path: Any) -> str | None:
    if not isinstance(path, str):
        return "path_not_string"
    if not path or len(path.encode("utf-8")) > 256:
        return "path_length_invalid"
    if unicodedata.normalize("NFKC", path) != path:
        return "noncanonical_unicode_path"
    root = path.split(".", 1)[0]
    if root in RESERVED_ROOTS or root.startswith("__"):
        return "reserved_path"
    if not PATH_PATTERN.fullmatch(path):
        return "noncanonical_or_traversal_path"
    return None


def _validate_logical_state(state_value: Any) -> dict[str, Any]:
    if not isinstance(state_value, dict):
        raise StateTargetError("state_payload_not_object")
    for path in state_value:
        reason = _path_reason(path)
        if reason:
            raise StateTargetError(f"unsafe_state_key:{reason}:{path!r}")
    return state_value


def _validate_contract_paths(contract: ExecutableContract) -> None:
    collections = (
        contract.initial_state.keys(),
        contract.editable_paths,
        contract.immutable_paths,
        (item.get("path") for item in contract.desired_patch),
        (item.get("path") for item in contract.required_preserved_state),
    )
    for paths in collections:
        for path in paths:
            reason = _path_reason(path)
            if reason:
                raise AdapterError(f"unsafe_contract_path:{reason}:{path!r}")


def _is_tuple_of_mappings(value: Any) -> bool:
    return isinstance(value, tuple) and all(isinstance(item, Mapping) for item in value)


def _schema_gate_frozen(candidate: Mapping[str, Any]) -> GateDecision:
    reasons: list[str] = []
    missing = sorted(REQUIRED_FIELDS - set(candidate))
    extra = sorted(set(candidate) - REQUIRED_FIELDS)
    if missing:
        reasons.append("missing_fields:" + ",".join(missing))
    if extra:
        reasons.append("unexpected_fields:" + ",".join(extra))
    if candidate.get("decision") not in {"apply", "block"}:
        reasons.append("invalid_decision_enum")
    for field in ("state_patch", "preserved_state", "evidence_bindings"):
        if not _is_tuple_of_mappings(candidate.get(field)):
            reasons.append(f"invalid_{field}_shape")
    for field in ("unknown_state", "forbidden_inferences"):
        value = candidate.get(field)
        if not isinstance(value, tuple) or not all(isinstance(item, str) for item in value):
            reasons.append(f"invalid_{field}_shape")
    if not isinstance(candidate.get("gate"), Mapping):
        reasons.append("invalid_gate_shape")
    return GateDecision(not reasons, tuple(reasons))


def _executable_gate_frozen(
    contract: ExecutableContract,
    candidate: Mapping[str, Any],
) -> GateDecision:
    """Evaluate the reference gate semantics without thawing the JSON snapshot."""

    shape = _schema_gate_frozen(candidate)
    if not shape.accepted:
        return shape
    reasons: list[str] = []
    if candidate["task_id"] != contract.task_id:
        reasons.append("task_identity_mismatch")
    if candidate["decision"] != contract.expected_decision:
        reasons.append("decision_mismatch")

    patches = candidate["state_patch"]
    desired_by_path = {item["path"]: item for item in contract.desired_patch}
    seen_paths: set[str] = set()
    for patch in patches:
        path = patch.get("path")
        seen_paths.add(path)
        if path not in contract.editable_paths:
            reasons.append("unauthorized_write_path")
            continue
        if path not in desired_by_path:
            reasons.append("unrequested_write")
            continue
        desired = desired_by_path[path]
        if patch.get("from") != _deep_freeze(contract.initial_state.get(path)):
            reasons.append("stale_or_fabricated_from_state")
        if patch.get("to") != _deep_freeze(desired.get("to")):
            reasons.append("wrong_target_state")
        if set(patch.get("evidence_ids", ())) != set(desired.get("evidence_ids", ())):
            reasons.append("patch_evidence_mismatch")

    if contract.expected_decision == "apply":
        if seen_paths != set(desired_by_path):
            reasons.append("incomplete_requested_patch")
    elif patches:
        reasons.append("write_attempt_under_block_decision")

    preserved = {item.get("path"): item.get("value") for item in candidate["preserved_state"]}
    expected_preserved = {
        item["path"]: _deep_freeze(item["value"])
        for item in contract.required_preserved_state
    }
    if preserved != expected_preserved:
        reasons.append("preserved_state_mismatch")
    if set(preserved) & contract.editable_paths and contract.expected_decision == "apply":
        reasons.append("edited_path_reported_as_preserved")

    decision_bindings = [
        item for item in candidate["evidence_bindings"] if item.get("slot_id") == "decision"
    ]
    if len(decision_bindings) != 1:
        reasons.append("decision_binding_cardinality")
    elif set(decision_bindings[0].get("evidence_ids", ())) != contract.required_evidence_ids:
        reasons.append("decision_evidence_mismatch")

    if set(candidate["unknown_state"]) != contract.required_unknown_state:
        reasons.append("unknown_state_not_preserved")
    if set(candidate["forbidden_inferences"]) != contract.forbidden_inferences:
        reasons.append("forbidden_inference_boundary_changed")
    if candidate["gate"] != _deep_freeze(contract.expected_gate):
        reasons.append("gate_attestation_mismatch")
    if candidate["next_action"] != contract.expected_next_action:
        reasons.append("next_action_mismatch")
    return GateDecision(not reasons, tuple(dict.fromkeys(reasons)))


def _candidate_path_reasons(candidate: Mapping[str, Any]) -> list[str]:
    reasons: list[str] = []
    reserved_keys = sorted(set(candidate) & RESERVED_TOP_LEVEL_CANDIDATE_KEYS)
    if reserved_keys:
        reasons.append("reserved_top_level_metadata:" + ",".join(reserved_keys))
    for field in ("state_patch", "preserved_state"):
        entries = candidate.get(field, [])
        if not isinstance(entries, tuple):
            continue
        for item in entries:
            if not isinstance(item, Mapping):
                continue
            path = item.get("path")
            reason = _path_reason(path)
            if reason:
                reasons.append(f"{reason}:{field}:{path!r}")
    return list(dict.fromkeys(reasons))


def _nonce_digest(nonce: str) -> str:
    return hashlib.sha256(nonce.encode("utf-8")).hexdigest()


def _validate_nonce(nonce: Any) -> str | None:
    if not isinstance(nonce, str) or not NONCE_PATTERN.fullmatch(nonce):
        return "invalid_nonce"
    return None


def _reject_symlink_components(path: Path, *, allow_missing_final: bool) -> None:
    """Reject symlinks in every existing component without resolving them."""

    absolute = Path(os.path.abspath(os.fspath(path)))
    components = absolute.parts
    current = Path(components[0])
    for index, component in enumerate(components[1:], start=1):
        current = current / component
        try:
            info = os.lstat(current)
        except FileNotFoundError:
            if allow_missing_final and index == len(components) - 1:
                return
            raise StateTargetError(f"path_component_missing:{current}")
        if stat.S_ISLNK(info.st_mode):
            parent_info = os.lstat(current.parent)
            trusted_system_link = (
                info.st_uid == 0
                and parent_info.st_uid == 0
                and not (stat.S_IMODE(parent_info.st_mode) & 0o022)
            )
            if not trusted_system_link:
                raise StateTargetError(f"symlink_path_component:{current}")


def _validate_trusted_parent(path: Path) -> None:
    """Require a same-user parent that is not group- or world-writable."""

    parent = Path(os.path.abspath(os.fspath(path))).parent
    info = os.lstat(parent)
    if not stat.S_ISDIR(info.st_mode):
        raise StateTargetError("state_parent_not_directory")
    if info.st_uid != os.geteuid():
        raise StateTargetError("state_parent_not_owned_by_effective_user")
    if stat.S_IMODE(info.st_mode) & 0o022:
        raise StateTargetError("untrusted_parent_permissions")


def _safe_open_regular_file(path: Path) -> int:
    _reject_symlink_components(path, allow_missing_final=False)
    _validate_trusted_parent(path)
    try:
        info = os.lstat(path)
    except FileNotFoundError as exc:
        raise StateTargetError("state_target_missing") from exc
    if stat.S_ISLNK(info.st_mode):
        raise StateTargetError("state_target_symlink")
    if not stat.S_ISREG(info.st_mode):
        raise StateTargetError("state_target_not_regular_file")
    if info.st_uid != os.geteuid() or stat.S_IMODE(info.st_mode) & 0o022:
        raise StateTargetError("state_target_permissions_or_owner_untrusted")
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(path, flags)
    except OSError as exc:
        if exc.errno in {errno.ELOOP, errno.EMLINK}:
            raise StateTargetError("state_target_symlink") from exc
        raise
    opened_info = os.fstat(descriptor)
    if not stat.S_ISREG(opened_info.st_mode):
        os.close(descriptor)
        raise StateTargetError("state_target_not_regular_file")
    if (info.st_dev, info.st_ino) != (opened_info.st_dev, opened_info.st_ino):
        os.close(descriptor)
        raise StateTargetError("state_target_changed_during_open")
    return descriptor


def _read_envelope(path: Path) -> tuple[dict[str, Any], str]:
    descriptor = _safe_open_regular_file(path)
    try:
        chunks: list[bytes] = []
        total = 0
        while True:
            block = os.read(descriptor, 65_536)
            if not block:
                break
            total += len(block)
            if total > MAX_JSON_BYTES:
                raise StateTargetError("state_file_too_large")
            chunks.append(block)
    finally:
        os.close(descriptor)
    raw = b"".join(chunks)
    try:
        envelope = json.loads(raw.decode("utf-8"), parse_constant=_reject_nonfinite)
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
        raise StateTargetError(f"invalid_state_json:{type(exc).__name__}") from exc
    if not isinstance(envelope, dict) or set(envelope) != {METADATA_KEY, STATE_KEY}:
        raise StateTargetError("invalid_state_envelope_keys")
    metadata = envelope[METADATA_KEY]
    if not isinstance(metadata, dict) or set(metadata) != {
        "format",
        "used_nonce_sha256",
        "version",
    }:
        raise StateTargetError("invalid_adapter_metadata")
    if metadata["format"] != FORMAT_ID:
        raise StateTargetError("unsupported_state_format")
    version = metadata["version"]
    if isinstance(version, bool) or not isinstance(version, int) or version < 0:
        raise StateTargetError("invalid_state_version")
    nonce_hashes = metadata["used_nonce_sha256"]
    if (
        not isinstance(nonce_hashes, list)
        or len(nonce_hashes) != len(set(nonce_hashes))
        or any(
            not isinstance(item, str)
            or len(item) != 64
            or any(char not in "0123456789abcdef" for char in item)
            for item in nonce_hashes
        )
    ):
        raise StateTargetError("invalid_nonce_ledger")
    _validate_logical_state(envelope[STATE_KEY])
    envelope_hash = hashlib.sha256(_canonical_json_bytes(envelope)).hexdigest()
    return envelope, envelope_hash


@contextlib.contextmanager
def _advisory_lock(state_path: Path) -> Iterator[None]:
    """Serialize cooperating processes through a no-follow sidecar lock."""

    lock_path = state_path.with_name(state_path.name + ".lock")
    _reject_symlink_components(lock_path, allow_missing_final=True)
    _validate_trusted_parent(lock_path)
    flags = os.O_CREAT | os.O_RDWR | getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(lock_path, flags, 0o600)
    except OSError as exc:
        if exc.errno in {errno.ELOOP, errno.EMLINK}:
            raise StateTargetError("lock_target_symlink") from exc
        raise
    try:
        lock_info = os.fstat(descriptor)
        if not stat.S_ISREG(lock_info.st_mode):
            raise StateTargetError("lock_target_not_regular_file")
        if lock_info.st_uid != os.geteuid() or stat.S_IMODE(lock_info.st_mode) & 0o022:
            raise StateTargetError("lock_target_permissions_or_owner_untrusted")
        fcntl.flock(descriptor, fcntl.LOCK_EX)
        yield
    finally:
        try:
            fcntl.flock(descriptor, fcntl.LOCK_UN)
        finally:
            os.close(descriptor)


def _fsync_directory(directory: Path) -> None:
    flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
    descriptor = os.open(directory, flags)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def _atomic_replace_envelope(
    state_path: Path,
    envelope: dict[str, Any],
    expected_before_hash: str,
    before_replace_hook: Callable[[], None] | None,
) -> None:
    """Durably stage a new envelope and atomically replace the old file."""

    parent = state_path.parent
    descriptor, temp_name = tempfile.mkstemp(
        prefix=f".{state_path.name}.", suffix=".tmp", dir=parent
    )
    temp_path = Path(temp_name)
    try:
        os.fchmod(descriptor, 0o600)
        encoded = _canonical_json_bytes(envelope)
        stream = os.fdopen(descriptor, "wb", closefd=True)
        descriptor = -1
        with stream:
            stream.write(encoded)
            stream.flush()
            os.fsync(stream.fileno())
        if before_replace_hook is not None:
            before_replace_hook()
        _, current_hash = _read_envelope(state_path)
        if current_hash != expected_before_hash:
            raise ConcurrentModificationError("state_changed_before_atomic_replace")
        os.replace(temp_path, state_path)
        try:
            _fsync_directory(parent)
        except OSError as exc:
            raise CommitOutcomeUnknownError(
                "replace_completed_but_directory_fsync_failed"
            ) from exc
    finally:
        if descriptor >= 0:
            os.close(descriptor)
        try:
            temp_path.unlink()
        except FileNotFoundError:
            pass


def initialize_state_file(
    state_path: Path,
    state_value: dict[str, Any],
    *,
    version: int = 0,
) -> None:
    """Create a new state envelope without following an existing path."""

    if isinstance(version, bool) or not isinstance(version, int) or version < 0:
        raise ValueError("version must be a non-negative integer")
    normalized_state = json.loads(
        json.dumps(state_value, ensure_ascii=False, allow_nan=False),
        parse_constant=_reject_nonfinite,
    )
    _validate_logical_state(normalized_state)
    envelope = {
        METADATA_KEY: {
            "format": FORMAT_ID,
            "used_nonce_sha256": [],
            "version": version,
        },
        STATE_KEY: normalized_state,
    }
    state_path.parent.mkdir(parents=True, exist_ok=True)
    _reject_symlink_components(state_path, allow_missing_final=True)
    _validate_trusted_parent(state_path)
    flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY | getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(state_path, flags, 0o600)
    try:
        encoded = _canonical_json_bytes(envelope)
        stream = os.fdopen(descriptor, "wb", closefd=True)
        descriptor = -1
        with stream:
            stream.write(encoded)
            stream.flush()
            os.fsync(stream.fileno())
        _fsync_directory(state_path.parent)
    finally:
        if descriptor >= 0:
            os.close(descriptor)


def read_state_snapshot(state_path: Path) -> StateSnapshot:
    """Read and validate an envelope without following a symlink target."""

    envelope, envelope_hash = _read_envelope(state_path)
    state_copy = copy.deepcopy(envelope[STATE_KEY])
    metadata = envelope[METADATA_KEY]
    return StateSnapshot(
        version=metadata["version"],
        state=MappingProxyType(state_copy),
        used_nonce_count=len(metadata["used_nonce_sha256"]),
        envelope_hash=envelope_hash,
    )


def _trace(
    contract: ExecutableContract,
    *,
    accepted: bool,
    reason_codes: list[str],
    wrote: bool,
    before_hash: str,
    after_hash: str,
    version_before: int,
    version_after: int,
) -> dict[str, Any]:
    return {
        "adapter_format": FORMAT_ID,
        "contract_id": contract.contract_id,
        "accepted": accepted,
        "reason_codes": reason_codes,
        "wrote": wrote,
        "before_hash": before_hash,
        "after_hash": after_hash,
        "version_before": version_before,
        "version_after": version_after,
        "rejected_state_unchanged": accepted or before_hash == after_hash,
    }


def execute_hardened(
    contract: ExecutableContract,
    candidate: Any,
    state_path: Path,
    *,
    expected_version: int,
    expected_snapshot_hash: str,
    nonce: str,
    before_replace_hook: Callable[[], None] | None = None,
) -> dict[str, Any]:
    """Validate one frozen proposal and conditionally commit one state change.

    The caller binds its proposal to both the version and exact envelope hash
    returned by :func:`read_state_snapshot`. The sidecar lock serializes
    cooperating adapter processes. A final hash check detects modifications
    visible before that check; the trusted-parent-directory boundary remains
    necessary because path-based replacement cannot exclude a hostile rename
    between the check and ``os.replace``. Durability ultimately depends on the
    filesystem honoring ``fsync`` and same-directory replace semantics.
    """

    _validate_contract_paths(contract)
    frozen_candidate = normalize_and_freeze_candidate(candidate)
    if isinstance(expected_version, bool) or not isinstance(expected_version, int):
        raise AdapterError("expected_version_not_integer")
    if (
        not isinstance(expected_snapshot_hash, str)
        or len(expected_snapshot_hash) != 64
        or any(char not in "0123456789abcdef" for char in expected_snapshot_hash)
    ):
        raise AdapterError("expected_snapshot_hash_invalid")
    nonce_reason = _validate_nonce(nonce)
    if nonce_reason:
        raise AdapterError(nonce_reason)

    with _advisory_lock(state_path):
        envelope, before_hash = _read_envelope(state_path)
        metadata = envelope[METADATA_KEY]
        version_before = metadata["version"]
        if expected_version != version_before:
            return _trace(
                contract,
                accepted=False,
                reason_codes=["stale_version"],
                wrote=False,
                before_hash=before_hash,
                after_hash=before_hash,
                version_before=version_before,
                version_after=version_before,
            )
        if expected_snapshot_hash != before_hash:
            return _trace(
                contract,
                accepted=False,
                reason_codes=["stale_snapshot_hash"],
                wrote=False,
                before_hash=before_hash,
                after_hash=before_hash,
                version_before=version_before,
                version_after=version_before,
            )

        nonce_hash = _nonce_digest(nonce)
        if nonce_hash in metadata["used_nonce_sha256"]:
            return _trace(
                contract,
                accepted=False,
                reason_codes=["replay_nonce"],
                wrote=False,
                before_hash=before_hash,
                after_hash=before_hash,
                version_before=version_before,
                version_after=version_before,
            )

        path_reasons = _candidate_path_reasons(frozen_candidate)
        if path_reasons:
            return _trace(
                contract,
                accepted=False,
                reason_codes=path_reasons,
                wrote=False,
                before_hash=before_hash,
                after_hash=before_hash,
                version_before=version_before,
                version_after=version_before,
            )

        live_state = envelope[STATE_KEY]
        live_contract = dataclasses.replace(
            contract, initial_state=copy.deepcopy(live_state)
        )
        decision = _executable_gate_frozen(live_contract, frozen_candidate)
        if not decision.accepted:
            return _trace(
                contract,
                accepted=False,
                reason_codes=list(decision.reason_codes),
                wrote=False,
                before_hash=before_hash,
                after_hash=before_hash,
                version_before=version_before,
                version_after=version_before,
            )

        logical_write = frozen_candidate["decision"] == "apply"
        next_state = (
            apply_patch_to_state(live_state, frozen_candidate["state_patch"])
            if logical_write
            else copy.deepcopy(live_state)
        )
        _validate_logical_state(next_state)
        next_envelope = {
            METADATA_KEY: {
                "format": FORMAT_ID,
                "used_nonce_sha256": [
                    *metadata["used_nonce_sha256"],
                    nonce_hash,
                ],
                "version": version_before + 1,
            },
            STATE_KEY: next_state,
        }
        _atomic_replace_envelope(
            state_path,
            next_envelope,
            before_hash,
            before_replace_hook,
        )
        after_envelope, after_hash = _read_envelope(state_path)
        return _trace(
            contract,
            accepted=True,
            reason_codes=[],
            wrote=logical_write,
            before_hash=before_hash,
            after_hash=after_hash,
            version_before=version_before,
            version_after=after_envelope[METADATA_KEY]["version"],
        )
