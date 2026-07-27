"""Contract-Driven Harness Reference Core (framework-agnostic).

A ~320-line reference implementation of the contract stack and deterministic
evaluators for the controlled-state-mutation task family. Contains zero
imports from any agent framework (PEtFiSh, LangChain, LangGraph, etc.).

License: MIT
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from typing import Any, Sequence

__version__ = "1.0.0"

# ── Type Definitions ────────────────────────────────────────────────────────

@dataclass
class EvidenceItem:
    evidence_id: str
    type: str  # EXTRACTED | INFERRED | AMBIGUOUS | PROPOSED
    claim: str
    source: str

@dataclass
class EvidenceBundle:
    bundle_id: str
    items: list[EvidenceItem]

@dataclass
class MemorySlice:
    slice_id: str
    must_load: list[str]
    must_not_load: list[str]
    staleness_policy: str

@dataclass
class StateEntry:
    state_id: str
    value: str
    evidence_ids: list[str]

@dataclass
class TransitionEvent:
    event_id: str
    scope: str
    state_id: str
    from_status: str
    to_status: str
    evidence_ids: list[str]

@dataclass
class TransitionDelta:
    remove_from_unknown_state: list[str]
    remove_from_forbidden_inferences: list[str]
    add_to_known_state: list[StateEntry]
    preserve_unknown_state: list[str]
    preserve_forbidden_inferences: list[str]

@dataclass
class TransitionGate:
    status: str
    permitted_action: str
    satisfied_prerequisite: str
    next_action: str
    support_slot_ids: list[str]

@dataclass
class RetentionAttestation:
    status: str
    immutable_fields: list[str]

@dataclass
class EvidenceBinding:
    slot_id: str
    evidence_ids: list[str]

@dataclass
class OutputContract:
    output_contract_id: str
    format: str
    required_sections: list[str]
    reference_field: str
    required_evidence_bindings: list[EvidenceBinding]
    initial_state: dict[str, Any]
    transition_event: TransitionEvent
    required_postconditions: dict[str, Any]
    required_transition_gate: TransitionGate
    required_attestation: RetentionAttestation
    required_transition_delta: TransitionDelta
    editable_fields: list[str] = field(default_factory=list)

@dataclass
class TaskSpec:
    task_id: str
    task_type: str
    objective: str
    constraints: list[str]
    success_conditions: list[str]

# ── Output Parsing ──────────────────────────────────────────────────────────

def parse_json_output(raw: str) -> dict[str, Any] | None:
    """Parse JSON from model output, tolerating markdown fences and preamble."""
    text = raw.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*\n?", "", text)
        text = re.sub(r"\n?```\s*$", "", text)
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        return None
    try:
        return json.loads(text[start:end + 1])
    except json.JSONDecodeError:
        return None

# ── The 7 Deterministic Evaluators ─────────────────────────────────────────

REQUIRED_SECTIONS = (
    "state_inventory",
    "evidence_bindings",
    "transition_record",
    "transition_gate",
    "retention_attestation",
)

def _norm(val: Any) -> Any:
    """Deep-normalize for structural comparison (sorts lists of strings)."""
    if isinstance(val, list):
        if val and all(isinstance(x, str) for x in val):
            return sorted(val)
        return [_norm(x) for x in val]
    if isinstance(val, dict):
        return {k: _norm(v) for k, v in val.items()}
    return val

def check_schema_validity(output: dict[str, Any]) -> float:
    """Evaluator 1: all required top-level sections present."""
    return 1.0 if all(s in output for s in REQUIRED_SECTIONS) else 0.0

def check_evidence_array_preservation(output: dict[str, Any], reference: dict[str, Any]) -> float:
    """Evaluator 2: evidence_bindings match reference exactly (order-sensitive)."""
    out_eb = output.get("evidence_bindings", [])
    ref_eb = reference.get("evidence_bindings", [])
    if len(out_eb) != len(ref_eb):
        return 0.0
    for o, r in zip(out_eb, ref_eb):
        if o.get("slot_id") != r.get("slot_id"):
            return 0.0
        if list(o.get("evidence_ids", [])) != list(r.get("evidence_ids", [])):
            return 0.0
    return 1.0

def check_residual_unknown_vocabulary(output: dict[str, Any], reference: dict[str, Any]) -> float:
    """Evaluator 3: unknown_state and forbidden_inferences match exactly."""
    out_si = output.get("state_inventory", {})
    ref_si = reference.get("state_inventory", {})
    out_unknown = out_si.get("unknown_state", [])
    ref_unknown = ref_si.get("unknown_state", [])
    out_forbid = out_si.get("forbidden_inferences", [])
    ref_forbid = ref_si.get("forbidden_inferences", [])
    ok_unknown = sorted(out_unknown) == sorted(ref_unknown) if isinstance(out_unknown, list) and isinstance(ref_unknown, list) else False
    ok_forbid = sorted(out_forbid) == sorted(ref_forbid) if isinstance(out_forbid, list) and isinstance(ref_forbid, list) else False
    return 1.0 if (ok_unknown and ok_forbid) else 0.0

def check_state_transition_accuracy(output: dict[str, Any], reference: dict[str, Any]) -> float:
    """Evaluator 4: transition_record matches reference."""
    out_tr = output.get("transition_record", {})
    ref_tr = reference.get("transition_record", {})
    fields = ("event_id", "state_id", "from_status", "to_status", "evidence_ids", "applied")
    return 1.0 if all(out_tr.get(f) == ref_tr.get(f) for f in fields) else 0.0

def check_transition_gate_accuracy(output: dict[str, Any], reference: dict[str, Any]) -> float:
    """Evaluator 5: transition_gate matches reference exactly."""
    out_tg = output.get("transition_gate", {})
    ref_tg = reference.get("transition_gate", {})
    return 1.0 if _norm(out_tg) == _norm(ref_tg) else 0.0

def check_retention_attestation_accuracy(output: dict[str, Any], reference: dict[str, Any]) -> float:
    """Evaluator 6: retention_attestation matches reference."""
    out_ra = output.get("retention_attestation", {})
    ref_ra = reference.get("retention_attestation", {})
    return 1.0 if _norm(out_ra) == _norm(ref_ra) else 0.0

def check_controlled_state_mutation_success(metrics: dict[str, float]) -> float:
    """Evaluator 7: all other evaluators passed."""
    others = {k: v for k, v in metrics.items() if k != "controlled_state_mutation_success"}
    return 1.0 if all(v == 1.0 for v in others.values()) else 0.0

# ── Harness: Ties Evaluators Together ───────────────────────────────────────

CRITICAL_METRICS = (
    "schema_validity",
    "exact_evidence_array_preservation",
    "residual_unknown_vocabulary_accuracy",
    "state_transition_accuracy",
    "transition_gate_accuracy",
    "retention_attestation_accuracy",
    "controlled_state_mutation_success",
)

@dataclass
class EvaluationResult:
    """Result of evaluating one model output against the contract."""
    strict_pass: bool
    metrics: dict[str, float]
    failed_checks: list[str]

    @property
    def pass_rate(self) -> float:
        return sum(self.metrics.values()) / len(self.metrics) if self.metrics else 0.0

class ContractHarness:
    """Framework-agnostic contract-driven harness evaluator.

    Given a golden reference output, evaluates model outputs against the
    7 deterministic criteria for the controlled-state-mutation task family.
    """

    def __init__(self, reference_output: dict[str, Any]) -> None:
        self.reference = reference_output

    def evaluate(self, model_output: dict[str, Any]) -> EvaluationResult:
        """Run all 7 evaluators and return aggregated result."""
        metrics: dict[str, float] = {}
        metrics["schema_validity"] = check_schema_validity(model_output)
        metrics["exact_evidence_array_preservation"] = check_evidence_array_preservation(model_output, self.reference)
        metrics["residual_unknown_vocabulary_accuracy"] = check_residual_unknown_vocabulary(model_output, self.reference)
        metrics["state_transition_accuracy"] = check_state_transition_accuracy(model_output, self.reference)
        metrics["transition_gate_accuracy"] = check_transition_gate_accuracy(model_output, self.reference)
        metrics["retention_attestation_accuracy"] = check_retention_attestation_accuracy(model_output, self.reference)
        metrics["controlled_state_mutation_success"] = check_controlled_state_mutation_success(metrics)
        strict_pass = metrics["controlled_state_mutation_success"] == 1.0
        failed = [k for k, v in metrics.items() if v == 0.0]
        return EvaluationResult(strict_pass=strict_pass, metrics=metrics, failed_checks=failed)

    def evaluate_raw(self, raw_output: str) -> EvaluationResult:
        """Parse and evaluate raw model output string."""
        parsed = parse_json_output(raw_output)
        if parsed is None:
            zero = {k: 0.0 for k in CRITICAL_METRICS}
            return EvaluationResult(strict_pass=False, metrics=zero, failed_checks=list(CRITICAL_METRICS) + ["json_parse"])
        return self.evaluate(parsed)

def evaluate_output(output: dict[str, Any], reference: dict[str, Any]) -> dict[str, float]:
    """Convenience function: evaluate and return metrics dict (backward compat)."""
    harness = ContractHarness(reference)
    return harness.evaluate(output).metrics

# ── Adapter Interface ──────────────────────────────────────────────────────

class FrameworkAdapter:
    """Minimal adapter interface for connecting the contract core to a framework.

    Subclass this to integrate with PEtFiSh, LangChain, or any other framework.
    The adapter is responsible for:
    1. Building the prompt from a TaskSpec + OutputContract
    2. Calling the model via the framework's API
    3. Returning the raw output string for evaluation
    """

    def build_prompt(self, task_spec: TaskSpec, output_contract: OutputContract,
                     evidence: EvidenceBundle, memory: MemorySlice) -> str:
        raise NotImplementedError

    def call_model(self, prompt: str, model_id: str, **kwargs: Any) -> str:
        raise NotImplementedError

# ── Self-Test ──────────────────────────────────────────────────────────────

def _self_test() -> bool:
    """Verify the core evaluates a known-good output as strict-pass."""
    golden = {
        "state_inventory": {"known_state": [{"state_id": "x", "value": "y", "evidence_ids": ["e1"]}],
                            "unknown_state": ["a"], "forbidden_inferences": ["b"]},
        "evidence_bindings": [{"slot_id": "s1", "evidence_ids": ["e1"]}],
        "transition_record": {"event_id": "ev1", "state_id": "x", "from_status": "unknown",
                               "to_status": "y", "evidence_ids": ["e1"], "applied": True},
        "transition_gate": {"status": "open", "permitted_action": "exec",
                            "satisfied_prerequisite": "x", "next_action": "done",
                            "support_slot_ids": ["s1"]},
        "retention_attestation": {"status": "preserved", "immutable_fields": ["a", "b"]},
    }
    harness = ContractHarness(golden)
    result = harness.evaluate(golden)
    assert result.strict_pass, f"Self-test failed: {result.failed_checks}"
    # Negative test: break one field
    broken = json.loads(json.dumps(golden))
    broken["evidence_bindings"][0]["evidence_ids"] = ["e2"]
    result2 = harness.evaluate(broken)
    assert not result2.strict_pass, "Self-test failed: broken output should not pass"
    assert "exact_evidence_array_preservation" in result2.failed_checks
    return True

if __name__ == "__main__":
    import sys
    ok = _self_test()
    print(f"Self-test: {'PASS' if ok else 'FAIL'}")
    print(f"Framework-agnostic core v{__version__}")
    print(f"Critical metrics: {len(CRITICAL_METRICS)}")
    print(f"Required sections: {len(REQUIRED_SECTIONS)}")
    sys.exit(0 if ok else 1)
