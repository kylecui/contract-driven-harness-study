#!/usr/bin/env python3
"""Narrow subprocess worker for the pinned external Invariant evaluator."""

from __future__ import annotations

import copy
import hashlib
import json
import os
import socket
import sys
from pathlib import Path
from typing import Any


def _blocked_connect(*_args: Any, **_kwargs: Any) -> None:
    raise RuntimeError("network access is forbidden in the isolated evaluator")


socket.socket.connect = _blocked_connect

SOURCE_ROOT = Path(
    os.environ.get("INVARIANT_SOURCE_ROOT", "/tmp/invariant-2340fe2d")
).resolve()
DEPS_ROOT = Path(
    os.environ.get("INVARIANT_DEPS_ROOT", "/tmp/invariant-deps-035")
).resolve()
for path in (DEPS_ROOT, SOURCE_ROOT):
    sys.path.insert(0, str(path))

from invariant.analyzer import LocalPolicy  # noqa: E402


def _canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _sha256_json(value: Any) -> str:
    return hashlib.sha256(_canonical_json(value).encode("utf-8")).hexdigest()


def evaluate_request(request: dict[str, Any]) -> dict[str, Any]:
    if set(request) != {"policy_source", "public_trace"}:
        raise ValueError("isolated evaluator accepts only policy_source and public_trace")
    if not isinstance(request["policy_source"], str):
        raise TypeError("policy_source must be a string")
    if not isinstance(request["public_trace"], list):
        raise TypeError("public_trace must be a list")
    trace_copy = copy.deepcopy(request["public_trace"])
    before_sha256 = _sha256_json(trace_copy)
    policy = LocalPolicy.from_string(request["policy_source"])
    analysis = policy.analyze(trace_copy)
    after_sha256 = _sha256_json(trace_copy)
    errors = [str(error) for error in analysis.errors]
    return {
        "worker_protocol": "IEBV1-isolated-evaluator-1",
        "request_keys": sorted(request),
        "network_connect_guard": True,
        "decision": "violation_detected" if errors else "no_violation_detected",
        "error_count": len(errors),
        "errors": errors,
        "public_trace_sha256_before": before_sha256,
        "public_trace_sha256_after": after_sha256,
        "public_trace_unmodified": before_sha256 == after_sha256,
    }


def main() -> None:
    request = json.load(sys.stdin)
    result = evaluate_request(request)
    sys.stdout.write(json.dumps(result, ensure_ascii=False, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
