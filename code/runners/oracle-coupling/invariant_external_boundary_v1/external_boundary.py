#!/usr/bin/env python3
"""Deterministic external-evaluator boundary control using pinned Invariant code."""

from __future__ import annotations

import ast
import copy
import hashlib
import importlib.metadata
import inspect
import json
import os
import platform
import subprocess
import sys
import textwrap
from pathlib import Path
from typing import Any, Callable


EXPERIMENT_ROOT = Path(__file__).resolve().parent
AUDIT_CODE_ROOT = EXPERIMENT_ROOT.parent
sys.path.insert(0, str(AUDIT_CODE_ROOT))

from layout import FIXTURE_ROOT, repo_relative  # noqa: E402

CASE_DEFINITIONS_PATH = FIXTURE_ROOT / "invariant_external_boundary_v1.json"
ISOLATED_WORKER_PATH = EXPERIMENT_ROOT / "isolated_evaluator.py"
UPSTREAM_SOURCE_ROOT = Path(
    os.environ.get("INVARIANT_SOURCE_ROOT", "/tmp/invariant-2340fe2d")
).resolve()
UPSTREAM_DEPS_ROOT = Path(
    os.environ.get("INVARIANT_DEPS_ROOT", "/tmp/invariant-deps-035")
).resolve()

EXPECTED_SOURCE_COMMIT = "2340fe2d9cd619f73d5b67fa05bf8a08c7cad515"
EXPECTED_PACKAGE_VERSION = "0.3.5"
EXPECTED_LICENSE_SHA256 = "90154031b70befefac025106f493124530e13c608b876cc1418b5f65ba945f14"
EXPECTED_DISPATCHER_SOURCE_SHA256 = (
    "5823c491c877a13844661724f561808fa62c8b93e4469314b1ea7e1beb2b4ac9"
)
UPSTREAM_REPOSITORY_URL = "https://github.com/invariantlabs-ai/invariant"
UPSTREAM_LICENSE_URL = (
    "https://github.com/invariantlabs-ai/invariant/blob/"
    f"{EXPECTED_SOURCE_COMMIT}/LICENSE"
)
LABEL_CONDITIONS = ("original", "deleted", "poisoned")
DECISIONS = ("no_violation_detected", "violation_detected")


def _configure_import_path() -> None:
    """Resolve implementation from the pinned source and dependencies from the temp target."""

    if not UPSTREAM_SOURCE_ROOT.is_dir():
        raise RuntimeError(f"missing pinned source: {UPSTREAM_SOURCE_ROOT}")
    if not UPSTREAM_DEPS_ROOT.is_dir():
        raise RuntimeError(f"missing dependency target: {UPSTREAM_DEPS_ROOT}")
    for path in (UPSTREAM_DEPS_ROOT, UPSTREAM_SOURCE_ROOT):
        value = str(path)
        if value in sys.path:
            sys.path.remove(value)
        sys.path.insert(0, value)
    # The second insertion above must leave the source ahead of the installed wheel.
    if sys.path[0] != str(UPSTREAM_SOURCE_ROOT):
        raise RuntimeError("pinned source is not first on sys.path")


_configure_import_path()

from invariant.analyzer import LocalPolicy  # noqa: E402


README_MESSAGE_POLICY = (
    'raise "The one who must not be named" if:\u0020\n'
    '    (msg: Message)\n'
    '    "voldemort" in msg.content.lower() or "tom riddle" in msg.content.lower()\n'
)

README_TOOL_POLICY = '''raise "External email to unknown address" if:
    # detect flows between tools
    (call: ToolCall) -> (call2: ToolCall)

    # check if the first call obtains the user's inbox
    call is tool:get_inbox

    # second call sends an email to an unknown address
    call2 is tool:send_email({
      to: ".*@[^ourcompany.com$].*"
    })
'''

POLICIES = {
    "upstream-readme-voldemort-message": {
        "policy_source": README_MESSAGE_POLICY,
        "upstream_file": "README.md",
        "upstream_example": "The one who must not be named Message policy",
    },
    "upstream-readme-external-email": {
        "policy_source": README_TOOL_POLICY,
        "upstream_file": "README.md",
        "upstream_example": "External email to unknown address ToolCall policy",
    },
}


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_text(value: str) -> str:
    return sha256_bytes(value.encode("utf-8"))


def sha256_json(value: Any) -> str:
    return sha256_text(canonical_json(value))


def sha256_path(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def git_output(*args: str) -> str:
    return subprocess.check_output(
        ["git", "-C", str(UPSTREAM_SOURCE_ROOT), *args], text=True
    ).strip()


def line_span(haystack: str, needle: str) -> dict[str, int]:
    offset = haystack.find(needle)
    if offset < 0:
        raise AssertionError("upstream policy snippet not found verbatim")
    start = haystack[:offset].count("\n") + 1
    # Policy constants retain upstream's trailing newline, but that newline does not
    # occupy an additional source line in the evidentiary span.
    end = start + needle.rstrip("\n").count("\n")
    return {"start": start, "end": end}


def load_case_definitions() -> dict[str, Any]:
    payload = json.loads(CASE_DEFINITIONS_PATH.read_text(encoding="utf-8"))
    validate_case_definitions(payload)
    return payload


def _value_at_path(value: Any, path: list[Any]) -> Any:
    current = value
    for component in path:
        current = current[component]
    return current


def _leaf_differences(left: Any, right: Any, path: tuple[Any, ...] = ()) -> list[tuple[Any, ...]]:
    if type(left) is not type(right):
        return [path]
    if isinstance(left, dict):
        if set(left) != set(right):
            return [path]
        differences: list[tuple[Any, ...]] = []
        for key in sorted(left):
            differences.extend(_leaf_differences(left[key], right[key], path + (key,)))
        return differences
    if isinstance(left, list):
        if len(left) != len(right):
            return [path]
        differences = []
        for index, (left_item, right_item) in enumerate(zip(left, right)):
            differences.extend(
                _leaf_differences(left_item, right_item, path + (index,))
            )
        return differences
    return [] if left == right else [path]


def validate_case_definitions(payload: dict[str, Any]) -> None:
    if set(payload) != {"schema_version", "protocol_id", "base_cases"}:
        raise ValueError("unexpected case-definition top-level keys")
    if payload["schema_version"] != "IEBV1-cases-1":
        raise ValueError("unexpected case-definition schema")
    if payload["protocol_id"] != "invariant-external-boundary-v1":
        raise ValueError("unexpected protocol id")
    cases = payload["base_cases"]
    if not isinstance(cases, list) or len(cases) != 2:
        raise ValueError("exactly two base cases are required")
    if len({case["base_case_id"] for case in cases}) != len(cases):
        raise ValueError("base_case_id values must be unique")
    for case in cases:
        expected_keys = {
            "base_case_id",
            "policy_id",
            "public_trace",
            "score_only_expected_label",
            "paired_policy_source_mutation",
            "paired_public_fact_edit",
        }
        if set(case) != expected_keys:
            raise ValueError(f"unexpected keys for {case.get('base_case_id')}")
        if case["policy_id"] not in POLICIES:
            raise ValueError(f"unknown policy id: {case['policy_id']}")
        if case["score_only_expected_label"] not in DECISIONS:
            raise ValueError("invalid score-only expected label")
        if not isinstance(case["public_trace"], list):
            raise ValueError("public_trace must be a list")
        mutation = case["paired_policy_source_mutation"]
        if set(mutation) != {
            "mutation_id",
            "source_origin",
            "fixed_public_trace_ref",
            "policy_source",
            "score_only_expected_label",
        }:
            raise ValueError("unexpected paired policy-source mutation keys")
        if (
            mutation["source_origin"]
            != "local_adversarial_control_using_upstream_policy_syntax"
        ):
            raise ValueError("policy mutation must be identified as a local control")
        if mutation["fixed_public_trace_ref"] != "public_trace":
            raise ValueError("policy mutation must fix the baseline public trace")
        if not isinstance(mutation["policy_source"], str) or not mutation["policy_source"]:
            raise ValueError("policy mutation source must be a non-empty string")
        if mutation["policy_source"] == POLICIES[case["policy_id"]]["policy_source"]:
            raise ValueError("policy mutation source must differ from official source")
        if mutation["score_only_expected_label"] not in DECISIONS:
            raise ValueError("invalid mutated-policy score-only expected label")
        if mutation["score_only_expected_label"] == case["score_only_expected_label"]:
            raise ValueError("policy mutation must change the expected decision")
        edit = case["paired_public_fact_edit"]
        if set(edit) != {
            "edit_id",
            "changed_public_fact",
            "public_trace",
            "score_only_expected_label",
        }:
            raise ValueError("unexpected paired public-fact edit keys")
        if edit["score_only_expected_label"] not in DECISIONS:
            raise ValueError("invalid edited score-only expected label")
        changed = edit["changed_public_fact"]
        if set(changed) != {"path", "before", "after"}:
            raise ValueError("invalid changed_public_fact record")
        if _value_at_path(case["public_trace"], changed["path"]) != changed["before"]:
            raise ValueError("changed_public_fact.before does not match baseline trace")
        if _value_at_path(edit["public_trace"], changed["path"]) != changed["after"]:
            raise ValueError("changed_public_fact.after does not match edited trace")
        differences = _leaf_differences(case["public_trace"], edit["public_trace"])
        if differences != [tuple(changed["path"])]:
            raise ValueError(
                f"public edit must change exactly the declared leaf, got {differences}"
            )


def poison_label(label: str) -> str:
    if label == "no_violation_detected":
        return "violation_detected"
    if label == "violation_detected":
        return "no_violation_detected"
    raise ValueError(f"cannot poison unknown label: {label}")


def build_answer_label_payload(label: str, condition: str) -> dict[str, str]:
    """Construct the deliberately out-of-band answer-label payload."""

    if condition == "original":
        return {"expected_label": label}
    if condition == "deleted":
        return {}
    if condition == "poisoned":
        return {"expected_label": poison_label(label)}
    raise ValueError(f"unknown label condition: {condition}")


def validate_isolated_worker_source(source: str | None = None) -> dict[str, Any]:
    """Reject worker code that can introspect caller state or accept answer labels."""

    worker_source = source or ISOLATED_WORKER_PATH.read_text(encoding="utf-8")
    tree = ast.parse(worker_source)
    forbidden_imports = {"inspect"}
    forbidden_names = {
        "eval",
        "exec",
        "globals",
        "locals",
        "vars",
        "__import__",
        "score_oracle",
        "expected_label",
    }
    forbidden_attributes = {
        "currentframe",
        "stack",
        "_getframe",
        "f_back",
        "f_locals",
        "f_globals",
    }
    violations: list[str] = []
    request_functions = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.split(".")[0] in forbidden_imports:
                    violations.append(f"forbidden_import:{alias.name}")
        elif isinstance(node, ast.ImportFrom):
            if (node.module or "").split(".")[0] in forbidden_imports:
                violations.append(f"forbidden_import:{node.module}")
        elif isinstance(node, ast.Name) and node.id in forbidden_names:
            violations.append(f"forbidden_name:{node.id}")
        elif isinstance(node, ast.Attribute) and node.attr in forbidden_attributes:
            violations.append(f"forbidden_attribute:{node.attr}")
        elif isinstance(node, ast.Constant) and isinstance(node.value, str):
            lowered = node.value.lower()
            if "score_oracle" in lowered or "expected_label" in lowered:
                violations.append("forbidden_label_literal")
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.name == "evaluate_request":
                request_functions.append(node)
    signature_ok = False
    if len(request_functions) == 1:
        function = request_functions[0]
        signature_ok = (
            [argument.arg for argument in function.args.args] == ["request"]
            and function.args.vararg is None
            and function.args.kwarg is None
            and not function.args.defaults
            and not function.args.kwonlyargs
        )
    if not signature_ok:
        violations.append("evaluate_request_signature")
    exact_request_guard = (
        'if set(request) != {"policy_source", "public_trace"}:' in worker_source
    )
    if not exact_request_guard:
        violations.append("exact_request_key_guard")
    checks = {
        "ast_parsed": True,
        "no_forbidden_introspection": not violations,
        "single_narrow_evaluate_request_signature": signature_ok,
        "exact_policy_trace_request_guard": exact_request_guard,
    }
    if violations:
        raise RuntimeError(f"isolated worker closure gate failed: {sorted(set(violations))}")
    return {
        "worker_path": repo_relative(ISOLATED_WORKER_PATH),
        "worker_sha256": sha256_text(worker_source),
        "checks": checks,
    }


def evaluate_external(policy_source: str, public_trace: list[dict[str, Any]]) -> dict[str, Any]:
    """Evaluate in a child process receiving only policy source and public trace."""

    worker_validation = validate_isolated_worker_source()
    request = {
        "policy_source": policy_source,
        "public_trace": copy.deepcopy(public_trace),
    }
    child_environment = {
        "INVARIANT_SOURCE_ROOT": str(UPSTREAM_SOURCE_ROOT),
        "INVARIANT_DEPS_ROOT": str(UPSTREAM_DEPS_ROOT),
        "PYTHONDONTWRITEBYTECODE": "1",
        "PYTHONHASHSEED": "0",
        "PYTHONUTF8": "1",
    }
    completed = subprocess.run(
        [sys.executable, "-I", str(ISOLATED_WORKER_PATH)],
        input=canonical_json(request) + "\n",
        text=True,
        capture_output=True,
        timeout=30,
        check=False,
        env=child_environment,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            "isolated evaluator failed: "
            f"returncode={completed.returncode}, stderr={completed.stderr.strip()}"
        )
    try:
        result = json.loads(completed.stdout)
    except json.JSONDecodeError as error:
        raise RuntimeError(
            f"isolated evaluator returned invalid JSON: {completed.stdout!r}"
        ) from error
    expected_result_keys = {
        "worker_protocol",
        "request_keys",
        "network_connect_guard",
        "decision",
        "error_count",
        "errors",
        "public_trace_sha256_before",
        "public_trace_sha256_after",
        "public_trace_unmodified",
    }
    if set(result) != expected_result_keys:
        raise RuntimeError(f"unexpected isolated evaluator output keys: {sorted(result)}")
    if result["worker_protocol"] != "IEBV1-isolated-evaluator-1":
        raise RuntimeError("unexpected isolated evaluator protocol")
    if result["request_keys"] != ["policy_source", "public_trace"]:
        raise RuntimeError("isolated evaluator observed unexpected request keys")
    if result["decision"] not in DECISIONS:
        raise RuntimeError("isolated evaluator returned an unknown decision")
    return {
        **result,
        "isolation_mode": "python_-I_subprocess_with_minimal_environment",
        "child_environment_keys": sorted(child_environment),
        "isolated_worker_sha256": worker_validation["worker_sha256"],
        "evaluator_request_sha256": sha256_json(request),
    }


def validate_dispatcher_callable(
    dispatcher: Callable[[str, list[dict[str, Any]]], dict[str, Any]] = evaluate_external,
    *,
    raise_on_failure: bool = True,
) -> dict[str, Any]:
    """Bind the parent dispatcher, not its self-reported child provenance."""

    violations: list[str] = []
    try:
        source = textwrap.dedent(inspect.getsource(dispatcher))
    except (OSError, TypeError) as error:
        source = ""
        violations.append(f"source_unavailable:{type(error).__name__}")
    source_sha256 = sha256_text(source) if source else None
    if source_sha256 != EXPECTED_DISPATCHER_SOURCE_SHA256:
        violations.append("source_sha256_mismatch")

    try:
        signature = inspect.signature(dispatcher)
    except (TypeError, ValueError) as error:
        signature = None
        violations.append(f"signature_unavailable:{type(error).__name__}")
    exact_signature = False
    if signature is not None:
        parameters = list(signature.parameters.values())
        exact_signature = (
            [parameter.name for parameter in parameters]
            == ["policy_source", "public_trace"]
            and all(
                parameter.kind
                is inspect.Parameter.POSITIONAL_OR_KEYWORD
                and parameter.default is inspect.Parameter.empty
                for parameter in parameters
            )
        )
    if not exact_signature:
        violations.append("exact_signature")

    tree = None
    if source:
        try:
            tree = ast.parse(source)
        except SyntaxError:
            violations.append("ast_parse")
    else:
        violations.append("ast_parse")

    exact_request_dict = False
    exact_child_environment = False
    subprocess_calls: list[ast.Call] = []
    if tree is not None:
        forbidden_names = {
            "eval",
            "exec",
            "globals",
            "locals",
            "vars",
            "__import__",
            "score_oracle",
            "expected_label",
        }
        forbidden_attributes = {
            "currentframe",
            "stack",
            "_getframe",
            "f_back",
            "f_locals",
            "f_globals",
        }
        for node in ast.walk(tree):
            if isinstance(node, ast.Name) and node.id in forbidden_names:
                violations.append(f"forbidden_name:{node.id}")
            elif isinstance(node, ast.Attribute) and node.attr in forbidden_attributes:
                violations.append(f"forbidden_attribute:{node.attr}")
            elif isinstance(node, ast.Constant) and isinstance(node.value, str):
                lowered = node.value.lower()
                if "score_oracle" in lowered or "expected_label" in lowered:
                    violations.append("forbidden_label_literal")
            elif isinstance(node, ast.Assign) and len(node.targets) == 1:
                target = node.targets[0]
                if isinstance(target, ast.Name) and isinstance(node.value, ast.Dict):
                    keys = {
                        key.value
                        for key in node.value.keys
                        if isinstance(key, ast.Constant) and isinstance(key.value, str)
                    }
                    if target.id == "request":
                        exact_request_dict = keys == {"policy_source", "public_trace"}
                    elif target.id == "child_environment":
                        exact_child_environment = keys == {
                            "INVARIANT_SOURCE_ROOT",
                            "INVARIANT_DEPS_ROOT",
                            "PYTHONDONTWRITEBYTECODE",
                            "PYTHONHASHSEED",
                            "PYTHONUTF8",
                        }
            elif (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Attribute)
                and isinstance(node.func.value, ast.Name)
                and node.func.value.id == "subprocess"
                and node.func.attr == "run"
            ):
                subprocess_calls.append(node)
    if not exact_request_dict:
        violations.append("exact_request_dict")
    if not exact_child_environment:
        violations.append("exact_child_environment")

    python_isolated_subprocess = (
        len(subprocess_calls) == 1
        and '[sys.executable, "-I", str(ISOLATED_WORKER_PATH)]' in source
        and 'input=canonical_json(request) + "\\n"' in source
        and "env=child_environment" in source
        and "shell=True" not in source
    )
    if not python_isolated_subprocess:
        violations.append("python_isolated_subprocess")

    checks = {
        "source_sha256_matches": source_sha256
        == EXPECTED_DISPATCHER_SOURCE_SHA256,
        "exact_policy_trace_signature": exact_signature,
        "ast_parsed": tree is not None,
        "no_parent_stack_or_label_introspection": not any(
            item.startswith("forbidden_") for item in violations
        ),
        "exact_policy_trace_request_dict": exact_request_dict,
        "exact_minimal_child_environment": exact_child_environment,
        "python_dash_I_subprocess_with_canonical_json_stdin": (
            python_isolated_subprocess
        ),
    }
    passed = all(checks.values()) and not violations
    if raise_on_failure and not passed:
        raise RuntimeError(
            f"production dispatcher closure gate failed: {sorted(set(violations))}"
        )
    return {
        "dispatcher_name": getattr(dispatcher, "__name__", type(dispatcher).__name__),
        "dispatcher_source_sha256": source_sha256,
        "expected_dispatcher_source_sha256": EXPECTED_DISPATCHER_SOURCE_SHA256,
        "checks": checks,
        "violations": sorted(set(violations)),
        "passed": passed,
    }


def validate_upstream_environment() -> dict[str, Any]:
    readme_path = UPSTREAM_SOURCE_ROOT / "README.md"
    license_path = UPSTREAM_SOURCE_ROOT / "LICENSE"
    pyproject_path = UPSTREAM_SOURCE_ROOT / "pyproject.toml"
    policy_path = Path(inspect.getfile(LocalPolicy)).resolve()
    commit = git_output("rev-parse", "HEAD")
    status = git_output("status", "--porcelain")
    observed_origin_url = git_output("remote", "get-url", "origin")
    readme = readme_path.read_text(encoding="utf-8")
    package_version = importlib.metadata.version("invariant-ai")
    worker_validation = validate_isolated_worker_source()
    dispatcher_validation = validate_dispatcher_callable()
    policy_evidence = []
    for policy_id, policy in POLICIES.items():
        source = policy["policy_source"]
        span = line_span(readme, source)
        policy_evidence.append(
            {
                "policy_id": policy_id,
                "upstream_file": policy["upstream_file"],
                "upstream_line_span": span,
                "policy_source_sha256": sha256_text(source),
                "verbatim_in_upstream_readme": True,
            }
        )
    checks = {
        "commit_matches": commit == EXPECTED_SOURCE_COMMIT,
        "source_clean": status == "",
        "origin_matches_official_repository": observed_origin_url
        in {UPSTREAM_REPOSITORY_URL, f"{UPSTREAM_REPOSITORY_URL}.git"},
        "license_hash_matches": sha256_path(license_path) == EXPECTED_LICENSE_SHA256,
        "package_version_matches": package_version == EXPECTED_PACKAGE_VERSION,
        "implementation_imported_from_pinned_source": policy_path.is_relative_to(
            UPSTREAM_SOURCE_ROOT
        ),
        "both_policy_sources_verbatim_in_readme": len(policy_evidence) == 2,
        "isolated_worker_closure_gate_passed": all(
            worker_validation["checks"].values()
        ),
        "production_dispatcher_closure_gate_passed": dispatcher_validation["passed"],
    }
    if not all(checks.values()):
        raise RuntimeError(f"upstream environment validation failed: {checks}")
    return {
        "repository_url": UPSTREAM_REPOSITORY_URL,
        "observed_origin_url": observed_origin_url,
        "source_root_at_run": str(UPSTREAM_SOURCE_ROOT),
        "source_commit": commit,
        "source_status_porcelain": status,
        "license_url": UPSTREAM_LICENSE_URL,
        "license_spdx": "Apache-2.0",
        "license_sha256": sha256_path(license_path),
        "license_bytes": license_path.stat().st_size,
        "readme_sha256": sha256_path(readme_path),
        "pyproject_sha256": sha256_path(pyproject_path),
        "local_policy_implementation_path_at_run": str(policy_path),
        "isolated_worker": worker_validation,
        "production_dispatcher": dispatcher_validation,
        "upstream_policy_evidence": policy_evidence,
        "checks": checks,
    }


def runtime_package_versions() -> dict[str, Any]:
    package_names = (
        "invariant-ai",
        "invariant-sdk",
        "lark",
        "pydantic",
        "openai",
        "pytest",
    )
    return {
        "python": sys.version,
        "python_executable": Path(sys.executable).name,
        "platform": platform.platform(),
        "machine": platform.machine(),
        "source_root": str(UPSTREAM_SOURCE_ROOT),
        "dependency_root": str(UPSTREAM_DEPS_ROOT),
        "packages": {
            name: importlib.metadata.version(name) for name in package_names
        },
    }


def _run_suite_with_evaluator(
    definitions: dict[str, Any],
    evaluator: Callable[[str, list[dict[str, Any]]], dict[str, Any]],
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Run the frozen matrix with an injected evaluator for mutation testing."""

    validate_case_definitions(definitions)
    dispatcher_validation = validate_dispatcher_callable(
        evaluator, raise_on_failure=False
    )
    runs: list[dict[str, Any]] = []
    for case in definitions["base_cases"]:
        official_policy = POLICIES[case["policy_id"]]
        policy_mutation = case["paired_policy_source_mutation"]
        conditions = (
            (
                "official_upstream_policy",
                "baseline_public_trace",
                official_policy["policy_source"],
                case["public_trace"],
                case["score_only_expected_label"],
                None,
                None,
            ),
            (
                "official_upstream_policy",
                "paired_public_fact_edit",
                official_policy["policy_source"],
                case["paired_public_fact_edit"]["public_trace"],
                case["paired_public_fact_edit"]["score_only_expected_label"],
                case["paired_public_fact_edit"]["edit_id"],
                None,
            ),
            (
                "local_policy_source_mutation",
                "baseline_public_trace",
                policy_mutation["policy_source"],
                case["public_trace"],
                policy_mutation["score_only_expected_label"],
                None,
                policy_mutation["mutation_id"],
            ),
        )
        for (
            policy_condition,
            public_condition,
            policy_source,
            trace,
            score_oracle,
            edit_id,
            policy_mutation_id,
        ) in conditions:
            for label_condition in LABEL_CONDITIONS:
                label_payload = build_answer_label_payload(score_oracle, label_condition)
                evaluator_input = {
                    "policy_source": policy_source,
                    "public_trace": copy.deepcopy(trace),
                }
                evaluated = evaluator(**evaluator_input)
                run_id = (
                    f"{case['base_case_id']}::{policy_condition}::"
                    f"{public_condition}::{label_condition}"
                )
                runs.append(
                    {
                        "run_id": run_id,
                        "base_case_id": case["base_case_id"],
                        "policy_id": case["policy_id"],
                        "policy_condition": policy_condition,
                        "policy_mutation_id": policy_mutation_id,
                        "public_condition": public_condition,
                        "public_fact_edit_id": edit_id,
                        "label_condition": label_condition,
                        "answer_label_payload": label_payload,
                        "answer_label_payload_sha256": sha256_json(label_payload),
                        "score_only_expected_label": score_oracle,
                        "evaluator_input_keys": sorted(evaluator_input),
                        "answer_label_excluded_from_evaluator_input": (
                            sorted(evaluator_input) == ["policy_source", "public_trace"]
                        ),
                        "evaluator_input_sha256": sha256_json(evaluator_input),
                        "policy_source": policy_source,
                        "policy_source_sha256": sha256_text(policy_source),
                        "public_trace": trace,
                        "public_trace_sha256": sha256_json(trace),
                        **evaluated,
                        "score_match": evaluated["decision"] == score_oracle,
                    }
                )

    label_groups = []
    group_conditions = (
        ("official_upstream_policy", "baseline_public_trace"),
        ("official_upstream_policy", "paired_public_fact_edit"),
        ("local_policy_source_mutation", "baseline_public_trace"),
    )
    for case in definitions["base_cases"]:
        for policy_condition, public_condition in group_conditions:
            group = [
                run
                for run in runs
                if run["base_case_id"] == case["base_case_id"]
                and run["policy_condition"] == policy_condition
                and run["public_condition"] == public_condition
            ]
            observed_conditions = {run["label_condition"] for run in group}
            checks = {
                "all_three_label_conditions_present": observed_conditions
                == set(LABEL_CONDITIONS),
                "intervention_payloads_are_distinct": len(
                    {run["answer_label_payload_sha256"] for run in group}
                )
                == 3,
                "policy_source_identical": len({run["policy_source"] for run in group})
                == 1,
                "policy_hash_identical": len(
                    {run["policy_source_sha256"] for run in group}
                )
                == 1,
                "public_trace_identical": len(
                    {run["public_trace_sha256"] for run in group}
                )
                == 1,
                "evaluator_input_identical": len(
                    {run["evaluator_input_sha256"] for run in group}
                )
                == 1,
                "decision_identical": len({run["decision"] for run in group}) == 1,
                "all_score_matches": all(run["score_match"] for run in group),
                "all_traces_unmodified": all(
                    run["public_trace_unmodified"] for run in group
                ),
                "all_labels_excluded": all(
                    run["answer_label_excluded_from_evaluator_input"] for run in group
                ),
            }
            label_groups.append(
                {
                    "base_case_id": case["base_case_id"],
                    "policy_condition": policy_condition,
                    "public_condition": public_condition,
                    "decision": group[0]["decision"],
                    "policy_source_sha256": group[0]["policy_source_sha256"],
                    "checks": checks,
                    "passed": all(checks.values()),
                }
            )

    public_fact_relations = []
    for case in definitions["base_cases"]:
        pair_checks = []
        for label_condition in LABEL_CONDITIONS:
            baseline = next(
                run
                for run in runs
                if run["base_case_id"] == case["base_case_id"]
                and run["policy_condition"] == "official_upstream_policy"
                and run["public_condition"] == "baseline_public_trace"
                and run["label_condition"] == label_condition
            )
            edited = next(
                run
                for run in runs
                if run["base_case_id"] == case["base_case_id"]
                and run["policy_condition"] == "official_upstream_policy"
                and run["public_condition"] == "paired_public_fact_edit"
                and run["label_condition"] == label_condition
            )
            checks = {
                "policy_source_unchanged": baseline["policy_source"]
                == edited["policy_source"],
                "policy_hash_unchanged": baseline["policy_source_sha256"]
                == edited["policy_source_sha256"],
                "public_trace_changed": baseline["public_trace_sha256"]
                != edited["public_trace_sha256"],
                "decision_changed": baseline["decision"] != edited["decision"],
                "baseline_matches_score_oracle": baseline["score_match"],
                "edited_matches_score_oracle": edited["score_match"],
            }
            pair_checks.append(
                {
                    "label_condition": label_condition,
                    "baseline_decision": baseline["decision"],
                    "edited_decision": edited["decision"],
                    "checks": checks,
                    "passed": all(checks.values()),
                }
            )
        public_fact_relations.append(
            {
                "base_case_id": case["base_case_id"],
                "edit_id": case["paired_public_fact_edit"]["edit_id"],
                "pair_checks": pair_checks,
                "passed": all(item["passed"] for item in pair_checks),
            }
        )

    policy_source_relations = []
    for case in definitions["base_cases"]:
        pair_checks = []
        for label_condition in LABEL_CONDITIONS:
            official = next(
                run
                for run in runs
                if run["base_case_id"] == case["base_case_id"]
                and run["policy_condition"] == "official_upstream_policy"
                and run["public_condition"] == "baseline_public_trace"
                and run["label_condition"] == label_condition
            )
            mutated = next(
                run
                for run in runs
                if run["base_case_id"] == case["base_case_id"]
                and run["policy_condition"] == "local_policy_source_mutation"
                and run["public_condition"] == "baseline_public_trace"
                and run["label_condition"] == label_condition
            )
            checks = {
                "public_trace_identical": official["public_trace"]
                == mutated["public_trace"],
                "public_trace_hash_identical": official["public_trace_sha256"]
                == mutated["public_trace_sha256"],
                "policy_source_changed": official["policy_source"]
                != mutated["policy_source"],
                "policy_hash_changed": official["policy_source_sha256"]
                != mutated["policy_source_sha256"],
                "decision_changed": official["decision"] != mutated["decision"],
                "official_matches_score_oracle": official["score_match"],
                "mutated_matches_score_oracle": mutated["score_match"],
            }
            pair_checks.append(
                {
                    "label_condition": label_condition,
                    "official_decision": official["decision"],
                    "mutated_decision": mutated["decision"],
                    "checks": checks,
                    "passed": all(checks.values()),
                }
            )
        policy_source_relations.append(
            {
                "base_case_id": case["base_case_id"],
                "mutation_id": case["paired_policy_source_mutation"]["mutation_id"],
                "fixed_public_trace_sha256": sha256_json(case["public_trace"]),
                "pair_checks": pair_checks,
                "passed": all(item["passed"] for item in pair_checks),
            }
        )

    baseline_directions = {
        (
            next(
                run
                for run in runs
                if run["base_case_id"] == case["base_case_id"]
                and run["policy_condition"] == "official_upstream_policy"
                and run["public_condition"] == "baseline_public_trace"
                and run["label_condition"] == "original"
            )["decision"],
            next(
                run
                for run in runs
                if run["base_case_id"] == case["base_case_id"]
                and run["policy_condition"] == "official_upstream_policy"
                and run["public_condition"] == "paired_public_fact_edit"
                and run["label_condition"] == "original"
            )["decision"],
        )
        for case in definitions["base_cases"]
    }
    expected_directions = {
        ("no_violation_detected", "violation_detected"),
        ("violation_detected", "no_violation_detected"),
    }
    policy_directions = {
        (
            relation["pair_checks"][0]["official_decision"],
            relation["pair_checks"][0]["mutated_decision"],
        )
        for relation in policy_source_relations
    }
    expected_worker_sha256 = validate_isolated_worker_source()["worker_sha256"]
    coverage_gate = {
        "exact_run_count": len(runs) == 18,
        "exact_label_invariance_group_count": len(label_groups) == 6,
        "exact_public_fact_relation_count": len(public_fact_relations) == 2,
        "exact_policy_source_relation_count": len(policy_source_relations) == 2,
        "all_label_invariance_groups_pass": all(
            group["passed"] for group in label_groups
        ),
        "all_public_fact_relations_pass": all(
            relation["passed"] for relation in public_fact_relations
        ),
        "all_policy_source_relations_pass": all(
            relation["passed"] for relation in policy_source_relations
        ),
        "both_public_fact_decision_directions_present": baseline_directions
        == expected_directions,
        "both_policy_source_decision_directions_present": policy_directions
        == expected_directions,
        "all_external_evaluator_calls_match_frozen_score_oracles": all(
            run["score_match"] for run in runs
        ),
        "all_calls_used_narrow_isolated_worker": all(
            run.get("isolation_mode")
            == "python_-I_subprocess_with_minimal_environment"
            and run.get("request_keys") == ["policy_source", "public_trace"]
            and run.get("isolated_worker_sha256") == expected_worker_sha256
            for run in runs
        ),
        "production_dispatcher_closure_passed": dispatcher_validation["passed"],
    }
    results = {
        "schema_version": "IEBV1-results-2",
        "protocol_id": definitions["protocol_id"],
        "base_case_count": len(definitions["base_cases"]),
        "external_evaluator_call_count": len(runs),
        "model_call_count": 0,
        "label_invariance_groups": label_groups,
        "public_fact_relations": public_fact_relations,
        "policy_source_relations": policy_source_relations,
        "production_dispatcher": dispatcher_validation,
        "coverage_gate": coverage_gate,
        "overall_passed": all(coverage_gate.values()),
        "claim_boundary": (
            "External evaluator boundary control only; not an external replication of "
            "the audited FEC-v2 coupling pattern, not independent task authorship, and not "
            "a check-to-commit or atomic-enforcement result."
        ),
    }
    return results, runs


def run_suite(
    payload: dict[str, Any] | None = None,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Run the production protocol through the exact isolated evaluator only."""

    definitions = payload or load_case_definitions()
    return _run_suite_with_evaluator(definitions, evaluate_external)
