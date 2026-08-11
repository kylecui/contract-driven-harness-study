#!/usr/bin/env python3
"""Repository layout and provenance helpers for the oracle-coupling audits."""

from __future__ import annotations

import subprocess
from pathlib import Path


AUDIT_CODE_ROOT = Path(__file__).resolve().parent
REPO_ROOT = AUDIT_CODE_ROOT.parents[2]
FIXTURE_ROOT = REPO_ROOT / "fixtures" / "oracle-coupling"
DATA_ROOT = REPO_ROOT / "data" / "reproduction" / "oracle-coupling"
ANALYSIS_ROOT = REPO_ROOT / "data" / "analysis" / "oracle-coupling"
BASE_SOURCE_COMMIT = "33de73a00c21ef8562bf9a7a6831c5ac3dafa245"

# The audit is additive. These are the only paths it may modify relative to the
# frozen publication-support base while it regenerates artifacts.
CONTRIBUTION_PATHS = (
    "README.md",
    "code/runners/oracle-coupling/",
    "data/analysis/oracle-coupling/",
    "data/reproduction/oracle-coupling/",
    "fixtures/oracle-coupling/",
    "paper/figures/figure-oracle-coupling-audit.pdf",
    "paper/figures/figure-oracle-coupling-audit.png",
    "paper/figures/figure-oracle-coupling-audit.svg",
)


def repo_relative(path: Path) -> str:
    return path.resolve().relative_to(REPO_ROOT.resolve()).as_posix()


def git_output(*args: str) -> str:
    return subprocess.check_output(
        ["git", "-C", str(REPO_ROOT), *args], text=True
    ).strip()


def base_snapshot_available() -> bool:
    completed = subprocess.run(
        [
            "git",
            "-C",
            str(REPO_ROOT),
            "merge-base",
            "--is-ancestor",
            BASE_SOURCE_COMMIT,
            "HEAD",
        ],
        capture_output=True,
        check=False,
    )
    return completed.returncode == 0


def unexpected_worktree_paths() -> list[str]:
    """Return modified paths outside the additive contribution boundary."""

    output = subprocess.check_output(
        [
            "git",
            "-C",
            str(REPO_ROOT),
            "status",
            "--porcelain=v1",
            "--untracked-files=all",
        ],
        text=True,
    )
    unexpected: list[str] = []
    for line in output.splitlines():
        if len(line) < 4:
            continue
        path = line[3:]
        if " -> " in path:
            path = path.rsplit(" -> ", 1)[-1]
        if not any(
            path.startswith(allowed) if allowed.endswith("/") else path == allowed
            for allowed in CONTRIBUTION_PATHS
        ):
            unexpected.append(path)
    return sorted(set(unexpected))
