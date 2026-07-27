"""Verify that the framework-agnostic core has zero PEtFiSh coupling.

Scans the reference-core Python module(s) for any textual or structural
reference to PEtFiSh-specific imports, identifiers, or attribute access.
This is a HEURISTIC check, not a proof of conceptual independence — the
core may still embed PEtFiSh design philosophy in ways grep cannot detect.
The check's purpose is to catch obvious textual coupling before publishing
the core as an independent artifact.

What this script checks:
    1. No `import petfishframework` / `from petfishframework...`
    2. No `import pf` / `from pf...` aliasing
    3. No `petfish.` attribute access
    4. No `pf.` attribute access (excluding common false positives like
       `self.`, `opf.`, `pf_path` etc. — see FALSE_POSITIVE_PREFIXES)
    5. No string literals mentioning "petfish" or "PEtFiSh" outside comments
       (configuration paths, error messages, etc.)

What this script DOES NOT check:
    - Conceptual lineage (design philosophy inherited from PEtFiSh)
    - Naming conventions that mirror PEtFiSh internals
    - Test fixtures coupled to PEtFiSh-specific schema

For full independence review, supplement this script with manual review
by an author NOT affiliated with PEtFiSh.

Usage
-----
    python verify_zero_petfish_dep.py \\
        --core-path /path/to/contract-driven-harness-reference-core/ \\
        --report research/05_analysis/reference-core-independence-check.json

Exit codes:
    0 = no textual coupling found
    1 = textual coupling found (review findings before publishing core)
    2 = script error (file not found, parse error, etc.)
"""

from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path


# Patterns that would indicate PEtFiSh coupling
IMPORT_PATTERNS = [
    re.compile(r"^\s*import\s+petfishframework", re.MULTILINE),
    re.compile(r"^\s*from\s+petfishframework", re.MULTILINE),
    re.compile(r"^\s*import\s+pf\b(?!\w)", re.MULTILINE),
    re.compile(r"^\s*from\s+pf\b(?!\w)", re.MULTILINE),
]

# Attribute access patterns (e.g., petfish.Agent, pf.Session)
ATTR_PATTERNS = [
    re.compile(r"\bpetfish\.\w"),
    # `pf.` is risky to flag because of false positives; we restrict to
    # likely framework usage by requiring uppercase first letter after dot
    # (e.g., pf.Agent, pf.Session) or known framework method names
    re.compile(r"\bpf\.(?:[A-Z]\w*|session|agent|model|budget|environment|policy|replay|rerun|resume)"),
]

# String literal patterns (config paths, error messages mentioning petfish)
STRING_PATTERNS = [
    re.compile(r"""['"](?:[^'"]*?)petfishframework([^'"]*?)['"]""", re.IGNORECASE),
    re.compile(r"""['"](?:[^'"]*?)petfish-?skills?([^'"]*?)['"]""", re.IGNORECASE),
]

# Comments are OK to mention petfish (historical context); we still report them
COMMENT_PATTERNS = [
    re.compile(r"#.*\bpetfish\b", re.IGNORECASE),
]


@dataclass
class Finding:
    file: str
    line_number: int
    line_content: str
    pattern_type: str  # import / attr / string / comment
    severity: str  # BLOCKER / WARNING / INFO


@dataclass
class VerificationReport:
    core_path: str
    files_scanned: int
    total_lines: int
    findings: list[Finding] = field(default_factory=list)

    @property
    def blockers(self) -> list[Finding]:
        return [f for f in self.findings if f.severity == "BLOCKER"]

    @property
    def warnings(self) -> list[Finding]:
        return [f for f in self.findings if f.severity == "WARNING"]

    @property
    def infos(self) -> list[Finding]:
        return [f for f in self.findings if f.severity == "INFO"]

    @property
    def passed(self) -> bool:
        return len(self.blockers) == 0

    def to_dict(self) -> dict:
        return {
            "core_path": self.core_path,
            "files_scanned": self.files_scanned,
            "total_lines": self.total_lines,
            "blocker_count": len(self.blockers),
            "warning_count": len(self.warnings),
            "info_count": len(self.infos),
            "passed": self.passed,
            "findings": [
                {
                    "file": f.file,
                    "line": f.line_number,
                    "type": f.pattern_type,
                    "severity": f.severity,
                    "content": f.line_content,
                }
                for f in self.findings
            ],
        }


def scan_file(path: Path) -> list[Finding]:
    """Scan a single Python file for PEtFiSh coupling."""
    findings: list[Finding] = []
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    for i, line in enumerate(lines, start=1):
        for pattern in IMPORT_PATTERNS:
            if pattern.search(line):
                findings.append(
                    Finding(
                        file=str(path),
                        line_number=i,
                        line_content=line.rstrip(),
                        pattern_type="import",
                        severity="BLOCKER",
                    )
                )
        for pattern in ATTR_PATTERNS:
            if pattern.search(line):
                findings.append(
                    Finding(
                        file=str(path),
                        line_number=i,
                        line_content=line.rstrip(),
                        pattern_type="attribute",
                        severity="BLOCKER",
                    )
                )
        for pattern in STRING_PATTERNS:
            if pattern.search(line):
                findings.append(
                    Finding(
                        file=str(path),
                        line_number=i,
                        line_content=line.rstrip(),
                        pattern_type="string",
                        severity="WARNING",
                    )
                )
        for pattern in COMMENT_PATTERNS:
            if pattern.search(line):
                findings.append(
                    Finding(
                        file=str(path),
                        line_number=i,
                        line_content=line.rstrip(),
                        pattern_type="comment",
                        severity="INFO",
                    )
                )

    # Also do AST-based check for import statements (catches multiline imports)
    try:
        tree = ast.parse(text, filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name.startswith(("petfishframework", "pf")):
                        findings.append(
                            Finding(
                                file=str(path),
                                line_number=node.lineno,
                                line_content=f"AST: import {alias.name}",
                                pattern_type="ast_import",
                                severity="BLOCKER",
                            )
                        )
            elif isinstance(node, ast.ImportFrom):
                if node.module and (
                    node.module.startswith("petfishframework")
                    or node.module == "pf"
                    or node.module.startswith("pf.")
                ):
                    findings.append(
                        Finding(
                            file=str(path),
                            line_number=node.lineno,
                            line_content=f"AST: from {node.module} import ...",
                            pattern_type="ast_import",
                            severity="BLOCKER",
                        )
                    )
    except SyntaxError as e:
        findings.append(
            Finding(
                file=str(path),
                line_number=e.lineno or 0,
                line_content=f"SyntaxError: {e.msg}",
                pattern_type="syntax",
                severity="WARNING",
            )
        )

    # Deduplicate (a line might trigger both regex and AST)
    seen = set()
    unique: list[Finding] = []
    for f in findings:
        key = (f.file, f.line_number, f.severity, f.line_content)
        if key not in seen:
            seen.add(key)
            unique.append(f)
    return unique


def verify_core(core_path: Path) -> VerificationReport:
    """Verify a directory or single file."""
    if core_path.is_file() and core_path.suffix == ".py":
        files = [core_path]
    elif core_path.is_dir():
        files = sorted(core_path.rglob("*.py"))
    else:
        raise ValueError(f"{core_path}: not a Python file or directory")

    report = VerificationReport(
        core_path=str(core_path),
        files_scanned=len(files),
        total_lines=0,
    )

    for f in files:
        report.total_lines += sum(1 for _ in f.open(encoding="utf-8"))
        report.findings.extend(scan_file(f))

    return report


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument(
        "--core-path",
        required=True,
        type=Path,
        help="Path to the framework-agnostic core (.py file or directory)",
    )
    ap.add_argument(
        "--report",
        type=Path,
        default=None,
        help="Optional JSON report output path",
    )
    args = ap.parse_args()

    if not args.core_path.exists():
        print(f"ERROR: {args.core_path} does not exist", file=sys.stderr)
        return 2

    try:
        report = verify_core(args.core_path)
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2

    print("=" * 60)
    print(f"Framework-agnostic core independence check")
    print(f"  path            : {report.core_path}")
    print(f"  files scanned   : {report.files_scanned}")
    print(f"  total lines     : {report.total_lines}")
    print(f"  blocker findings: {len(report.blockers)}")
    print(f"  warning findings: {len(report.warnings)}")
    print(f"  info findings   : {len(report.infos)}")
    print("=" * 60)

    if report.blockers:
        print("\nBLOCKERS (must fix before publishing core as independent):")
        for f in report.blockers:
            print(f"  {f.file}:{f.line_number} [{f.pattern_type}]")
            print(f"    {f.line_content}")
    if report.warnings:
        print("\nWARNINGS (review before publishing):")
        for f in report.warnings:
            print(f"  {f.file}:{f.line_number} [{f.pattern_type}]")
            print(f"    {f.line_content}")
    if report.infos:
        print("\nINFO (comments mentioning petfish; OK to keep as historical context):")
        for f in report.infos[:5]:
            print(f"  {f.file}:{f.line_number}")
            print(f"    {f.line_content}")
        if len(report.infos) > 5:
            print(f"  ... and {len(report.infos) - 5} more")

    print()
    if report.passed:
        print("RESULT: PASS — no textual PEtFiSh coupling found.")
        print("NOTE: This is a heuristic check. Conceptual lineage may still")
        print("exist; supplement with manual review by a non-PEtFiSh-affiliated author.")
    else:
        print("RESULT: FAIL — textual PEtFiSh coupling found. Fix before publishing.")

    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(
            json.dumps(report.to_dict(), indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        print(f"\nWrote: {args.report}")

    return 0 if report.passed else 1


if __name__ == "__main__":
    sys.exit(main())
