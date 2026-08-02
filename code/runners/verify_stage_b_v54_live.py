"""Stage B v5.4 Live Verification Runner

Re-runs the frozen Stage B v5.4 controlled-state-mutation protocol against
live SiliconFlow API for author verification of Kimi's automated replication.

Usage:
    python verify_stage_b_v54_live.py --model Qwen/Qwen3-8B --output research/05_analysis/author-confirmation-records/qwen3-8b.json
    python verify_stage_b_v54_live.py --all-models --output-dir research/05_analysis/author-confirmation-records/
    python verify_stage_b_v54_live.py --model Qwen/Qwen3-8B --reps 2 --smoke  # quick test

Environment:
    OPENAI_API_KEY, OPENAI_BASE_URL (SiliconFlow OpenAI-compatible endpoint)

Cost estimate per model:
    5 conditions × 8 reps = 40 calls
    ~8KB prompt in, ~2KB output out per call
    Qwen3-8B ~ ¥0.0007/M cached → < ¥1 per model
"""
from __future__ import annotations

import argparse
import copy
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# ── Model registry ──────────────────────────────────────────────────────────

MODELS = {
    "qwen3-8b":       {"id": "Qwen/Qwen3-8B",              "family": "Qwen3",   "size": "8B",  "floor": "above"},
    "glm-4-9b":       {"id": "THUDM/GLM-4-9B-0414",        "family": "GLM",     "size": "9B",  "floor": "above"},
    "qwen3-14b":      {"id": "Qwen/Qwen3-14B",             "family": "Qwen3",   "size": "14B", "floor": "above"},
    "deepseek-v3.2":  {"id": "deepseek-ai/DeepSeek-V3.2",  "family": "DeepSeek","size": "MoE", "floor": "above"},
    "qwen2.5-7b":     {"id": "Qwen/Qwen2.5-7B-Instruct",   "family": "Qwen2.5", "size": "7B",  "floor": "below_candidate"},
}

CONDITIONS = ("canonical", "field_alias", "evidence_order_shuffled", "distractor_evidence", "unknown_state_paraphrase")
REPS = 8

# ── Prompt loading ──────────────────────────────────────────────────────────

PROMPT_ROOT = Path("research/05_analysis/real-run-artifacts/stage-b-v54-explicit-delta-stability")

def load_prompt(condition: str) -> str:
    """Load the r1 prompt for a condition (task content identical across reps)."""
    # Directory names use hyphens; condition keys use underscores
    dir_condition = condition.replace("_", "-")
    pattern = f"stage-b-v54-delta-stability--{dir_condition}__budget_model__G9__r1"
    prompt_dir = PROMPT_ROOT / pattern
    if not prompt_dir.exists():
        # try other model tier names
        for d in PROMPT_ROOT.iterdir():
            if d.is_dir() and f"--{dir_condition}__" in d.name and d.name.endswith("__r1"):
                prompt_dir = d
                break
    prompt_path = prompt_dir / "prompt.md"
    return prompt_path.read_text(encoding="utf-8")

def load_reference_output(condition: str) -> dict[str, Any]:
    """Load the r1 output (golden reference) for a condition."""
    dir_condition = condition.replace("_", "-")
    pattern = f"stage-b-v54-delta-stability--{dir_condition}__budget_model__G9__r1"
    prompt_dir = PROMPT_ROOT / pattern
    if not prompt_dir.exists():
        for d in PROMPT_ROOT.iterdir():
            if d.is_dir() and f"--{dir_condition}__" in d.name and d.name.endswith("__r1"):
                prompt_dir = d
                break
    output_text = (prompt_dir / "output.md").read_text(encoding="utf-8")
    return json.loads(output_text)

# ── API call ────────────────────────────────────────────────────────────────

def call_api(model_id: str, prompt: str, max_retries: int = 3) -> dict[str, Any]:
    """Call SiliconFlow OpenAI-compatible chat completions endpoint."""
    key = os.environ.get("OPENAI_API_KEY")
    base = os.environ.get("OPENAI_BASE_URL", "https://api.siliconflow.cn/v1")
    if not key:
        raise RuntimeError("OPENAI_API_KEY not set")

    # Strip code fences from the system message to discourage markdown wrapping
    system_msg = (
        "You are a precise JSON-producing agent. Return ONLY the JSON object "
        "specified by the task. No markdown fences, no prose, no explanations. "
        "The first character of your response must be '{' and the last must be '}'."
    )

    payload = {
        "model": model_id,
        "messages": [
            {"role": "system", "content": system_msg},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0,
        "max_tokens": 2048,
        "stream": False,
    }

    body = json.dumps(payload).encode("utf-8")
    url = base.rstrip("/") + "/chat/completions"
    last_err = None
    for attempt in range(1, max_retries + 1):
        req = urllib.request.Request(
            url,
            data=body,
            headers={
                "Authorization": "Bearer " + key,
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=90) as resp:
                data = json.loads(resp.read())
            return {
                "content": data["choices"][0]["message"]["content"],
                "usage": data.get("usage", {}),
                "model": data.get("model", model_id),
                "response_id": data.get("id", ""),
                "created": data.get("created", 0),
            }
        except urllib.error.HTTPError as e:
            last_err = f"HTTP {e.code}: {e.read().decode('utf-8', errors='replace')[:300]}"
            if e.code == 429:
                wait = min(30, 2 ** attempt * 2)
                print(f"  rate limited, waiting {wait}s (attempt {attempt}/{max_retries})", file=sys.stderr)
                time.sleep(wait)
                continue
            elif e.code >= 500:
                wait = 2 ** attempt
                print(f"  server error {e.code}, retry in {wait}s", file=sys.stderr)
                time.sleep(wait)
                continue
            else:
                raise
        except Exception as e:
            last_err = str(e)
            wait = 2 ** attempt
            print(f"  error: {e}, retry in {wait}s", file=sys.stderr)
            time.sleep(wait)
    raise RuntimeError(f"API call failed after {max_retries} retries: {last_err}")

# ── Output parsing ──────────────────────────────────────────────────────────

def extract_json(content: str) -> dict[str, Any] | None:
    """Parse JSON from model output, tolerating markdown fences and preamble."""
    text = content.strip()
    # strip markdown fences
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*\n?", "", text)
        text = re.sub(r"\n?```\s*$", "", text)
    # find the outermost JSON object
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        return None
    try:
        return json.loads(text[start:end + 1])
    except json.JSONDecodeError:
        return None

# ── Evaluators (7 critical metrics) ────────────────────────────────────────

def _norm(val: Any) -> Any:
    """Normalize for comparison (deep sort lists of strings)."""
    if isinstance(val, list):
        if all(isinstance(x, str) for x in val):
            return sorted(val)
        return [_norm(x) for x in val]
    if isinstance(val, dict):
        return {k: _norm(v) for k, v in val.items()}
    return val

def _exact_list(a: list, b: list) -> bool:
    """Exact list equality including order."""
    return list(a) == list(b)

def evaluate_output(output: dict[str, Any], reference: dict[str, Any]) -> dict[str, float]:
    """Run the 7 critical deterministic evaluators.

    Returns a dict of metric_name -> 1.0 or 0.0.
    """
    metrics: dict[str, float] = {}

    # 1. schema_validity: all 5 required sections present
    required = ("state_inventory", "evidence_bindings", "transition_record", "transition_gate", "retention_attestation")
    metrics["schema_validity"] = 1.0 if all(s in output for s in required) else 0.0

    # 2. exact_evidence_array_preservation: evidence_bindings match reference exactly (order matters)
    try:
        out_eb = output.get("evidence_bindings", [])
        ref_eb = reference.get("evidence_bindings", [])
        # Compare slot_id + evidence_ids for each slot, in order
        if len(out_eb) != len(ref_eb):
            metrics["exact_evidence_array_preservation"] = 0.0
        else:
            ok = True
            for o, r in zip(out_eb, ref_eb):
                if o.get("slot_id") != r.get("slot_id"):
                    ok = False
                    break
                if _exact_list(o.get("evidence_ids", []), r.get("evidence_ids", [])):
                    continue
                else:
                    ok = False
                    break
            metrics["exact_evidence_array_preservation"] = 1.0 if ok else 0.0
    except Exception:
        metrics["exact_evidence_array_preservation"] = 0.0

    # 3. residual_unknown_vocabulary_accuracy: unknown_state and forbidden_inferences match exactly
    try:
        out_si = output.get("state_inventory", {})
        ref_si = reference.get("state_inventory", {})
        out_unknown = out_si.get("unknown_state", [])
        ref_unknown = ref_si.get("unknown_state", [])
        out_forbid = out_si.get("forbidden_inferences", [])
        ref_forbid = ref_si.get("forbidden_inferences", [])
        # Compare as sets (order shouldn't matter for these)
        ok_unknown = sorted(out_unknown) == sorted(ref_unknown) if isinstance(out_unknown, list) and isinstance(ref_unknown, list) else False
        ok_forbid = sorted(out_forbid) == sorted(ref_forbid) if isinstance(out_forbid, list) and isinstance(ref_forbid, list) else False
        metrics["residual_unknown_vocabulary_accuracy"] = 1.0 if (ok_unknown and ok_forbid) else 0.0
    except Exception:
        metrics["residual_unknown_vocabulary_accuracy"] = 0.0

    # 4. state_transition_accuracy: transition_record matches reference
    try:
        out_tr = output.get("transition_record", {})
        ref_tr = reference.get("transition_record", {})
        fields = ("event_id", "state_id", "from_status", "to_status", "evidence_ids", "applied")
        ok = all(out_tr.get(f) == ref_tr.get(f) for f in fields)
        metrics["state_transition_accuracy"] = 1.0 if ok else 0.0
    except Exception:
        metrics["state_transition_accuracy"] = 0.0

    # 5. transition_gate_accuracy: transition_gate matches reference exactly
    try:
        out_tg = output.get("transition_gate", {})
        ref_tg = reference.get("transition_gate", {})
        metrics["transition_gate_accuracy"] = 1.0 if _norm(out_tg) == _norm(ref_tg) else 0.0
    except Exception:
        metrics["transition_gate_accuracy"] = 0.0

    # 6. retention_attestation_accuracy: retention_attestation matches reference
    try:
        out_ra = output.get("retention_attestation", {})
        ref_ra = reference.get("retention_attestation", {})
        metrics["retention_attestation_accuracy"] = 1.0 if _norm(out_ra) == _norm(ref_ra) else 0.0
    except Exception:
        metrics["retention_attestation_accuracy"] = 0.0

    # 7. controlled_state_mutation_success: all above pass
    metrics["controlled_state_mutation_success"] = 1.0 if all(
        v == 1.0 for k, v in metrics.items() if k != "controlled_state_mutation_success"
    ) else 0.0

    # task_success (aggregate, same as 7 for this protocol)
    metrics["task_success"] = metrics["controlled_state_mutation_success"]

    # atom_primary_metric
    metrics["atom_primary_metric"] = metrics["controlled_state_mutation_success"]

    return metrics

# ── Main runner ─────────────────────────────────────────────────────────────

def run_model(model_key: str, reps: int = REPS, conditions: tuple[str, ...] = CONDITIONS) -> dict[str, Any]:
    """Run full protocol for one model."""
    model_info = MODELS[model_key]
    model_id = model_info["id"]
    print(f"\n{'='*60}")
    print(f"Model: {model_key} ({model_id})")
    print(f"Family: {model_info['family']} | Size: {model_info['size']} | Floor: {model_info['floor']}")
    print(f"Conditions: {len(conditions)} × Reps: {reps} = {len(conditions)*reps} calls")
    print(f"{'='*60}")

    # Load prompts and references for each condition
    prompts = {}
    references = {}
    for cond in conditions:
        prompts[cond] = load_prompt(cond)
        references[cond] = load_reference_output(cond)

    runs = []
    strict_pass_count = 0
    total = len(conditions) * reps

    for cond_idx, cond in enumerate(conditions, 1):
        cond_passes = 0
        for rep in range(1, reps + 1):
            run_id = f"{model_key}__{cond}__r{rep}"
            print(f"  [{cond_idx}/{len(conditions)}] {cond} r{rep}/{reps} ...", end="", flush=True)

            t0 = time.time()
            try:
                result = call_api(model_id, prompts[cond])
                elapsed = time.time() - t0
                output = extract_json(result["content"])

                if output is None:
                    print(f" FAIL (json parse) [{elapsed:.1f}s]")
                    runs.append({
                        "run_id": run_id,
                        "model": model_id,
                        "condition": cond,
                        "rep": rep,
                        "strict_pass": False,
                        "parse_error": True,
                        "raw_output": result["content"][:500],
                        "elapsed_s": round(elapsed, 2),
                        "usage": result.get("usage", {}),
                    })
                    continue

                metrics = evaluate_output(output, references[cond])
                strict_pass = all(v == 1.0 for v in metrics.values())

                if strict_pass:
                    cond_passes += 1
                    strict_pass_count += 1
                    print(f" PASS [{elapsed:.1f}s]")
                else:
                    failed = [k for k, v in metrics.items() if v == 0.0]
                    print(f" FAIL ({', '.join(failed)}) [{elapsed:.1f}s]")

                runs.append({
                    "run_id": run_id,
                    "model": model_id,
                    "condition": cond,
                    "rep": rep,
                    "strict_pass": strict_pass,
                    "metrics": metrics,
                    "elapsed_s": round(elapsed, 2),
                    "usage": result.get("usage", {}),
                    "response_id": result.get("response_id", ""),
                })

                # rate limit protection
                time.sleep(0.5)

            except Exception as e:
                elapsed = time.time() - t0
                print(f" ERROR: {e} [{elapsed:.1f}s]")
                runs.append({
                    "run_id": run_id,
                    "model": model_id,
                    "condition": cond,
                    "rep": rep,
                    "strict_pass": False,
                    "error": str(e),
                    "elapsed_s": round(elapsed, 2),
                })
                time.sleep(2)

        print(f"  → {cond}: {cond_passes}/{reps}")

    # Summary
    from math import sqrt
    pass_rate = strict_pass_count / total
    # Wilson 95% CI
    if total > 0:
        z = 1.96
        n = total
        p = pass_rate
        denom = 1 + z*z/n
        center = (p + z*z/(2*n)) / denom
        margin = z * sqrt(p*(1-p)/n + z*z/(4*n*n)) / denom
        wilson_low = max(0.0, center - margin)
        wilson_high = min(1.0, center + margin)
    else:
        wilson_low = wilson_high = 0.0

    summary = {
        "model_key": model_key,
        "model_id": model_id,
        "family": model_info["family"],
        "size": model_info["size"],
        "floor_expectation": model_info["floor"],
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "total_runs": total,
        "strict_passes": strict_pass_count,
        "pass_rate": round(pass_rate, 4),
        "wilson_95_low": round(wilson_low, 4),
        "wilson_95_high": round(wilson_high, 4),
        "conditions": {},
        "runs": runs,
    }
    for cond in conditions:
        cond_runs = [r for r in runs if r["condition"] == cond]
        cond_passes = sum(1 for r in cond_runs if r.get("strict_pass"))
        summary["conditions"][cond] = {
            "passes": cond_passes,
            "total": len(cond_runs),
            "pass_rate": round(cond_passes / len(cond_runs), 4) if cond_runs else 0,
        }

    print(f"\n{'─'*40}")
    print(f"SUMMARY {model_key}: {strict_pass_count}/{total} = {pass_rate:.1%}")
    print(f"  Wilson 95%: [{wilson_low:.4f}, {wilson_high:.4f}]")
    for cond, s in summary["conditions"].items():
        print(f"  {cond}: {s['passes']}/{s['total']}")
    print(f"{'─'*40}")

    return summary

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--model", choices=list(MODELS.keys()), help="Single model to verify")
    ap.add_argument("--all-models", action="store_true", help="Run all 5 models")
    ap.add_argument("--reps", type=int, default=REPS, help=f"Reps per condition (default {REPS})")
    ap.add_argument("--smoke", action="store_true", help="Smoke test: 2 reps, canonical only")
    ap.add_argument("--output", type=Path, help="Output JSON path (single model)")
    ap.add_argument("--output-dir", type=Path, help="Output directory (all models)")
    args = ap.parse_args()

    if args.smoke:
        args.reps = 2
        conditions = ("canonical",)
    else:
        conditions = CONDITIONS

    if args.all_models:
        out_dir = args.output_dir or Path("research/05_analysis/author-confirmation-records")
        out_dir.mkdir(parents=True, exist_ok=True)
        all_summaries = []
        for key in MODELS:
            summary = run_model(key, reps=args.reps, conditions=conditions)
            out_path = out_dir / f"{key}.json"
            out_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
            print(f"\nWrote: {out_path}")
            all_summaries.append({
                "model_key": summary["model_key"],
                "model_id": summary["model_id"],
                "total_runs": summary["total_runs"],
                "strict_passes": summary["strict_passes"],
                "pass_rate": summary["pass_rate"],
                "wilson_95": [summary["wilson_95_low"], summary["wilson_95_high"]],
            })
            # cool-down between models
            if key != list(MODELS.keys())[-1]:
                print("\n  (cool-down 5s between models)")
                time.sleep(5)
        # combined summary
        combined_path = out_dir / "_all-models-summary.json"
        combined_path.write_text(json.dumps(all_summaries, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"\nWrote combined: {combined_path}")
        print(f"\n{'='*60}")
        print("ALL MODELS SUMMARY")
        print(f"{'='*60}")
        for s in all_summaries:
            ci = f"[{s['wilson_95'][0]:.4f}, {s['wilson_95'][1]:.4f}]"
            print(f"  {s['model_key']:18s} {s['strict_passes']:3d}/{s['total_runs']:<3d} = {s['pass_rate']:.1%}  Wilson {ci}")
    elif args.model:
        summary = run_model(args.model, reps=args.reps, conditions=conditions)
        out_path = args.output or Path(f"research/05_analysis/author-confirmation-records/{args.model}.json")
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"\nWrote: {out_path}")
    else:
        ap.error("must specify --model or --all-models")

    return 0

if __name__ == "__main__":
    sys.exit(main())
