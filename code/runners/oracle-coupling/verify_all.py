#!/usr/bin/env python3
"""Verify every frozen manifest in the oracle-coupling evidence bundle."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from layout import REPO_ROOT


def run_verifier(relative: str) -> dict[str, Any]:
    completed = subprocess.run(
        [sys.executable, str(REPO_ROOT / relative)],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    return {
        "name": Path(relative).parent.name,
        "returncode": completed.returncode,
        "stdout": completed.stdout.strip(),
        "stderr": completed.stderr.strip(),
        "failures": [] if completed.returncode == 0 else [f"verifier:{relative}"],
    }


def main() -> int:
    results = [
        run_verifier(
            "code/runners/oracle-coupling/failure_to_executable_contract_v2/verify_manifest.py"
        ),
        run_verifier(
            "code/runners/oracle-coupling/oracle_independent_compiler_v1/verify_manifest.py"
        ),
        run_verifier(
            "code/runners/oracle-coupling/metamorphic_public_input_v1/verify_manifest.py"
        ),
        run_verifier(
            "code/runners/oracle-coupling/hardened_state_adapter_v1/verify_manifest.py"
        ),
        run_verifier(
            "code/runners/oracle-coupling/second_harness_audit_v1/verify_manifest.py"
        ),
        run_verifier(
            "code/runners/oracle-coupling/invariant_external_boundary_v1/verify_manifest.py"
        ),
        run_verifier(
            "code/runners/oracle-coupling/executed_counterfactual_v1/verify_manifest.py"
        ),
        run_verifier(
            "code/runners/oracle-coupling/external_tau_bench_v1/verify_manifest.py"
        ),
    ]
    failures = [failure for result in results for failure in result["failures"]]
    print(
        json.dumps(
            {
                "bundle": "oracle-coupling",
                "verified_components": sum(not result["failures"] for result in results),
                "component_count": len(results),
                "failures": failures,
                "passed": not failures,
                "components": results,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
