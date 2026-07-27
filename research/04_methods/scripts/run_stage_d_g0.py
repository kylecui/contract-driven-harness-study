"""Stage D: G0 (no-contract) arm runner for matched overhead matrix.

Compares G0 (bare task description, no contract scaffolding) against G9
(full contract stack) on the same task family. Measures:
- Strict pass rate (same 7 evaluators)
- Prompt token cost (G0 is much shorter)
- Completion token cost
- Latency per call

Usage:
    python run_stage_d_g0.py --model qwen3-8b --output research/05_analysis/stage-d-g0-qwen3-8b.json
    python run_stage_d_g0.py --model qwen3-8b --reps 4  # reduced for speed
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.request
from pathlib import Path
from typing import Any

# Reuse infrastructure from the main verifier
sys.path.insert(0, str(Path(__file__).parent))
from verify_stage_b_v54_live import (
    MODELS, CONDITIONS, call_api, extract_json, evaluate_output,
    load_reference_output, run_model,
)

# ── G0 Prompt Builder ───────────────────────────────────────────────────────

def build_g0_prompt(condition: str) -> str:
    """Build a minimal G0 prompt: bare task, output schema, no contract scaffolding.

    G0 gives the model:
    - A one-paragraph task description
    - The required output fields (names only, no detailed schema)
    - The basic context (initial state, event)

    G0 does NOT give:
    - TaskSpec with constraints and success conditions
    - EvidenceBundle with structured evidence
    - MemorySlice with memory boundaries
    - OutputContract with detailed schema, postconditions, deltas
    """
    # Load the reference output to extract the essential context
    ref = load_reference_output(condition)

    # Extract key facts from reference
    event_id = ref.get("transition_record", {}).get("event_id", "event-api-approval-001")
    state_id = ref.get("transition_record", {}).get("state_id", "network_api_approval")
    from_status = ref.get("transition_record", {}).get("from_status", "unknown")
    to_status = ref.get("transition_record", {}).get("to_status", "approved")
    evidence_id = ref.get("transition_record", {}).get("evidence_ids", ["ev-09"])[0]

    unknown_states = ref.get("state_inventory", {}).get("unknown_state", ["current_git_branch", "ci_status"])
    forbidden = ref.get("state_inventory", {}).get("forbidden_inferences", [])

    prompt = f"""# Task: State Transition

Apply the following state transition and return the result as JSON.

## Context
- Initial unknown states: {', '.join(unknown_states)}
- An event ({event_id}) changes {state_id} from {from_status} to {to_status}
- Evidence supporting this: {evidence_id}

## Output Format
Return a JSON object with these fields:
- state_inventory: {{known_state: [...], unknown_state: [...], forbidden_inferences: [...]}}
- evidence_bindings: [{{slot_id: "...", evidence_ids: [...]}}]
- transition_record: {{event_id, state_id, from_status, to_status, evidence_ids, applied}}
- transition_gate: {{status, permitted_action, satisfied_prerequisite, next_action, support_slot_ids}}
- retention_attestation: {{status, immutable_fields: [...]}}

Condition: {condition}
Return only the JSON object. No markdown, no prose."""

    return prompt

# ── G0 Runner ───────────────────────────────────────────────────────────────

def run_g0_model(model_key: str, reps: int = 4) -> dict[str, Any]:
    """Run G0 arm for one model."""
    model_info = MODELS[model_key]
    model_id = model_info["id"]

    print(f"\n{'='*60}")
    print(f"Stage D G0 Arm: {model_key} ({model_id})")
    print(f"Conditions: {len(CONDITIONS)} × Reps: {reps} = {len(CONDITIONS)*reps} calls")
    print(f"{'='*60}")

    runs = []
    strict_pass_count = 0
    total = len(CONDITIONS) * reps

    for cond_idx, cond in enumerate(CONDITIONS, 1):
        prompt = build_g0_prompt(cond)
        prompt_tokens = len(prompt) // 4  # rough estimate
        reference = load_reference_output(cond)

        cond_passes = 0
        for rep in range(1, reps + 1):
            run_id = f"g0_{model_key}__{cond}__r{rep}"
            print(f"  [{cond_idx}/{len(CONDITIONS)}] {cond} r{rep}/{reps} ...", end="", flush=True)

            t0 = time.time()
            try:
                result = call_api(model_id, prompt)
                elapsed = time.time() - t0
                output = extract_json(result["content"])

                usage = result.get("usage", {})
                prompt_tokens_actual = usage.get("prompt_tokens", prompt_tokens)
                completion_tokens = usage.get("completion_tokens", 0)

                if output is None:
                    print(f" FAIL (json parse) [{elapsed:.1f}s]")
                    runs.append({
                        "run_id": run_id, "arm": "G0", "model": model_id,
                        "condition": cond, "rep": rep, "strict_pass": False,
                        "parse_error": True, "elapsed_s": round(elapsed, 2),
                        "prompt_tokens": prompt_tokens_actual,
                        "completion_tokens": completion_tokens,
                    })
                    continue

                metrics = evaluate_output(output, reference)
                strict_pass = all(v == 1.0 for v in metrics.values())

                if strict_pass:
                    cond_passes += 1
                    strict_pass_count += 1
                    print(f" PASS [{elapsed:.1f}s]")
                else:
                    failed = [k for k, v in metrics.items() if v == 0.0]
                    print(f" FAIL ({len(failed)} checks) [{elapsed:.1f}s]")

                runs.append({
                    "run_id": run_id, "arm": "G0", "model": model_id,
                    "condition": cond, "rep": rep, "strict_pass": strict_pass,
                    "metrics": metrics, "elapsed_s": round(elapsed, 2),
                    "prompt_tokens": prompt_tokens_actual,
                    "completion_tokens": completion_tokens,
                    "response_id": result.get("response_id", ""),
                })
                time.sleep(0.5)
            except Exception as e:
                elapsed = time.time() - t0
                print(f" ERROR: {e} [{elapsed:.1f}s]")
                runs.append({
                    "run_id": run_id, "arm": "G0", "model": model_id,
                    "condition": cond, "rep": rep, "strict_pass": False,
                    "error": str(e), "elapsed_s": round(elapsed, 2),
                })
                time.sleep(2)

        print(f"  → G0 {cond}: {cond_passes}/{reps}")

    # Summary
    pass_rate = strict_pass_count / total
    # Cost analysis
    total_prompt_tokens = sum(r.get("prompt_tokens", 0) for r in runs if "prompt_tokens" in r)
    total_completion_tokens = sum(r.get("completion_tokens", 0) for r in runs if "completion_tokens" in r)
    avg_latency = sum(r.get("elapsed_s", 0) for r in runs) / len(runs) if runs else 0

    summary = {
        "arm": "G0",
        "model_key": model_key,
        "model_id": model_id,
        "total_runs": total,
        "strict_passes": strict_pass_count,
        "pass_rate": round(pass_rate, 4),
        "total_prompt_tokens": total_prompt_tokens,
        "total_completion_tokens": total_completion_tokens,
        "avg_prompt_tokens_per_run": total_prompt_tokens // max(len(runs), 1),
        "avg_completion_tokens_per_run": total_completion_tokens // max(len(runs), 1),
        "avg_latency_s": round(avg_latency, 2),
        "runs": runs,
    }

    print(f"\n{'─'*40}")
    print(f"G0 SUMMARY {model_key}: {strict_pass_count}/{total} = {pass_rate:.1%}")
    print(f"  Prompt tokens: {total_prompt_tokens} ({summary['avg_prompt_tokens_per_run']}/run)")
    print(f"  Completion tokens: {total_completion_tokens} ({summary['avg_completion_tokens_per_run']}/run)")
    print(f"  Avg latency: {avg_latency:.1f}s")
    print(f"{'─'*40}")

    return summary

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--model", choices=list(MODELS.keys()), required=True)
    ap.add_argument("--reps", type=int, default=4)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()

    summary = run_g0_model(args.model, reps=args.reps)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nWrote: {args.output}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
