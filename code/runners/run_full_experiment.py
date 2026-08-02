"""Full-provenance experiment runner for Stage B v5.4 + Stage D G0.

Saves per-run: prompt, raw API response, parsed JSON, metrics, usage, timing.
Designed for round-02 reproducibility verification.

Output structure:
    {output_dir}/
    ├── _index.md                         ← human-readable index
    ├── _summary.csv                      ← cross-model comparison
    ├── prompts/                          ← exact prompts saved once
    │   ├── stage-b-v54__canonical.md
    │   ├── stage-b-v54__field-alias.md
    │   └── ...
    ├── stage-b-v54/
    │   ├── {model}__full.json            ← all runs for this model
    │   └── ...
    └── stage-d-g0/
        ├── {model}__g0__full.json
        └── ...

Usage:
    # Full Stage B v5.4 (5 models × 40 runs = 200 calls, ~2-3 hours)
    python run_full_experiment.py stage-b --all-models --output-dir research/05_analysis/experiment-rounds/round-02-full-reproducibility

    # Stage D G0 (2 models × 20 runs = 40 calls, ~30-60 min)
    python run_full_experiment.py stage-d --models qwen3-8b deepseek-v3.2 --output-dir research/05_analysis/experiment-rounds/round-02-full-reproducibility

    # Single model smoke test
    python run_full_experiment.py stage-b --model qwen3-8b --reps 2 --conditions canonical
"""
from __future__ import annotations

import argparse
import copy
import csv
import json
import math
import os
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# ── Config ──────────────────────────────────────────────────────────────────

MODELS = {
    "qwen3-8b":      {"id": "Qwen/Qwen3-8B",             "family": "Qwen3",    "size": "8B",  "floor": "above"},
    "glm-4-9b":      {"id": "THUDM/GLM-4-9B-0414",       "family": "GLM",      "size": "9B",  "floor": "above"},
    "qwen3-14b":     {"id": "Qwen/Qwen3-14B",            "family": "Qwen3",    "size": "14B", "floor": "above"},
    "deepseek-v3.2": {"id": "deepseek-ai/DeepSeek-V3.2", "family": "DeepSeek", "size": "MoE", "floor": "above"},
    "qwen2.5-7b":    {"id": "Qwen/Qwen2.5-7B-Instruct",  "family": "Qwen2.5",  "size": "7B",  "floor": "below"},
}

CONDITIONS = ("canonical", "field_alias", "evidence_order_shuffled", "distractor_evidence", "unknown_state_paraphrase")
REPS = 8

PROMPT_ROOT = Path("research/05_analysis/real-run-artifacts/stage-b-v54-explicit-delta-stability")

# ── Prompt loading ──────────────────────────────────────────────────────────

def load_prompt(condition: str) -> str:
    dir_condition = condition.replace("_", "-")
    pattern = f"stage-b-v54-delta-stability--{dir_condition}__budget_model__G9__r1"
    prompt_dir = PROMPT_ROOT / pattern
    if not prompt_dir.exists():
        for d in PROMPT_ROOT.iterdir():
            if d.is_dir() and f"--{dir_condition}__" in d.name and d.name.endswith("__r1"):
                prompt_dir = d
                break
    return (prompt_dir / "prompt.md").read_text(encoding="utf-8")

def load_reference(condition: str) -> dict[str, Any]:
    dir_condition = condition.replace("_", "-")
    pattern = f"stage-b-v54-delta-stability--{dir_condition}__budget_model__G9__r1"
    prompt_dir = PROMPT_ROOT / pattern
    if not prompt_dir.exists():
        for d in PROMPT_ROOT.iterdir():
            if d.is_dir() and f"--{dir_condition}__" in d.name and d.name.endswith("__r1"):
                prompt_dir = d
                break
    return json.loads((prompt_dir / "output.md").read_text(encoding="utf-8"))

def build_g0_prompt(condition: str) -> str:
    """Minimal G0 prompt: bare task, output schema, no contract scaffolding."""
    ref = load_reference(condition)
    event_id = ref.get("transition_record", {}).get("event_id", "event-api-approval-001")
    state_id = ref.get("transition_record", {}).get("state_id", "network_api_approval")
    unknown_states = ref.get("state_inventory", {}).get("unknown_state", ["x", "y"])
    evidence_id = ref.get("transition_record", {}).get("evidence_ids", ["e1"])[0]
    return f"""# Task: State Transition

Apply the following state transition and return the result as JSON.

## Context
- Initial unknown states: {', '.join(unknown_states)}
- An event ({event_id}) changes {state_id} from unknown to approved
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

# ── API call ────────────────────────────────────────────────────────────────

def call_api(model_id: str, prompt: str, max_retries: int = 3) -> dict[str, Any]:
    key = os.environ.get("OPENAI_API_KEY")
    base = os.environ.get("OPENAI_BASE_URL", "https://api.siliconflow.cn/v1")
    if not key:
        raise RuntimeError("OPENAI_API_KEY not set")
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
        req = urllib.request.Request(url, data=body, headers={
            "Authorization": "Bearer " + key,
            "Content-Type": "application/json",
        }, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                data = json.loads(resp.read())
            return {
                "content": data["choices"][0]["message"]["content"],
                "usage": data.get("usage", {}),
                "model": data.get("model", model_id),
                "response_id": data.get("id", ""),
                "created": data.get("created", 0),
                "raw_api_response": data,
            }
        except urllib.error.HTTPError as e:
            last_err = f"HTTP {e.code}: {e.read().decode('utf-8', errors='replace')[:300]}"
            if e.code == 429:
                wait = min(30, 2 ** attempt * 2)
                print(f"  rate limited, waiting {wait}s", file=sys.stderr)
                time.sleep(wait)
                continue
            elif e.code >= 500:
                time.sleep(2 ** attempt)
                continue
            else:
                raise
        except Exception as e:
            last_err = str(e)
            time.sleep(2 ** attempt)
    raise RuntimeError(f"API call failed after {max_retries} retries: {last_err}")

# ── Output parsing + evaluation ────────────────────────────────────────────

import re

def extract_json(content: str) -> dict[str, Any] | None:
    text = content.strip()
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

REQUIRED_SECTIONS = ("state_inventory", "evidence_bindings", "transition_record", "transition_gate", "retention_attestation")

def _norm(val: Any) -> Any:
    if isinstance(val, list):
        if val and all(isinstance(x, str) for x in val):
            return sorted(val)
        return [_norm(x) for x in val]
    if isinstance(val, dict):
        return {k: _norm(v) for k, v in val.items()}
    return val

def evaluate(output: dict[str, Any], reference: dict[str, Any]) -> dict[str, float]:
    m = {}
    m["schema_validity"] = 1.0 if all(s in output for s in REQUIRED_SECTIONS) else 0.0
    try:
        out_eb = output.get("evidence_bindings", [])
        ref_eb = reference.get("evidence_bindings", [])
        ok = len(out_eb) == len(ref_eb) and all(
            o.get("slot_id") == r.get("slot_id") and list(o.get("evidence_ids", [])) == list(r.get("evidence_ids", []))
            for o, r in zip(out_eb, ref_eb)
        )
        m["exact_evidence_array_preservation"] = 1.0 if ok else 0.0
    except Exception:
        m["exact_evidence_array_preservation"] = 0.0
    try:
        out_si = output.get("state_inventory", {})
        ref_si = reference.get("state_inventory", {})
        m["residual_unknown_vocabulary_accuracy"] = 1.0 if (
            sorted(out_si.get("unknown_state", [])) == sorted(ref_si.get("unknown_state", [])) and
            sorted(out_si.get("forbidden_inferences", [])) == sorted(ref_si.get("forbidden_inferences", []))
        ) else 0.0
    except Exception:
        m["residual_unknown_vocabulary_accuracy"] = 0.0
    try:
        out_tr = output.get("transition_record", {})
        ref_tr = reference.get("transition_record", {})
        fields = ("event_id", "state_id", "from_status", "to_status", "evidence_ids", "applied")
        m["state_transition_accuracy"] = 1.0 if all(out_tr.get(f) == ref_tr.get(f) for f in fields) else 0.0
    except Exception:
        m["state_transition_accuracy"] = 0.0
    try:
        m["transition_gate_accuracy"] = 1.0 if _norm(output.get("transition_gate", {})) == _norm(reference.get("transition_gate", {})) else 0.0
    except Exception:
        m["transition_gate_accuracy"] = 0.0
    try:
        m["retention_attestation_accuracy"] = 1.0 if _norm(output.get("retention_attestation", {})) == _norm(reference.get("retention_attestation", {})) else 0.0
    except Exception:
        m["retention_attestation_accuracy"] = 0.0
    m["controlled_state_mutation_success"] = 1.0 if all(v == 1.0 for k, v in m.items()) else 0.0
    return m

# ── Wilson CI ───────────────────────────────────────────────────────────────

def wilson(passes: int, total: int, z: float = 1.96) -> tuple[float, float]:
    if total == 0:
        return 0.0, 0.0
    n = total
    p = passes / n
    denom = 1 + z*z/n
    center = (p + z*z/(2*n)) / denom
    margin = z * math.sqrt(p*(1-p)/n + z*z/(4*n*n)) / denom
    return max(0.0, center - margin), min(1.0, center + margin)

# ── Main runner ─────────────────────────────────────────────────────────────

def run_model(model_key: str, conditions: tuple[str, ...], reps: int, arm: str = "G9") -> dict[str, Any]:
    model_info = MODELS[model_key]
    model_id = model_info["id"]
    total = len(conditions) * reps
    print(f"\n{'='*60}")
    print(f"  {arm} | {model_key} ({model_id})")
    print(f"  {len(conditions)} conditions × {reps} reps = {total} calls")
    print(f"{'='*60}")

    runs = []
    strict_passes = 0

    for ci, cond in enumerate(conditions, 1):
        if arm == "G9":
            prompt = load_prompt(cond)
            reference = load_reference(cond)
        else:
            prompt = build_g0_prompt(cond)
            reference = load_reference(cond)

        cond_passes = 0
        for rep in range(1, reps + 1):
            run_id = f"{model_key}__{arm}__{cond}__r{rep:02d}"
            ts = datetime.now(timezone.utc).isoformat()
            print(f"  [{ci}/{len(conditions)}] {cond} r{rep}/{reps} ...", end="", flush=True)

            t0 = time.time()
            try:
                result = call_api(model_id, prompt)
                elapsed = time.time() - t0
                content = result["content"]
                parsed = extract_json(content)

                run_record = {
                    "run_id": run_id,
                    "model_key": model_key,
                    "model_id": model_id,
                    "arm": arm,
                    "condition": cond,
                    "rep": rep,
                    "timestamp": ts,
                    "elapsed_s": round(elapsed, 2),
                    "response_id": result.get("response_id", ""),
                    "usage": result.get("usage", {}),
                    # Full provenance
                    "prompt_sent": prompt,           # exact prompt text
                    "raw_content": content,           # exact model response text
                    "parsed_output": parsed,          # extracted JSON or null
                }

                if parsed is None:
                    run_record["parse_error"] = True
                    run_record["metrics"] = {k: 0.0 for k in (
                        "schema_validity", "exact_evidence_array_preservation",
                        "residual_unknown_vocabulary_accuracy", "state_transition_accuracy",
                        "transition_gate_accuracy", "retention_attestation_accuracy",
                        "controlled_state_mutation_success"
                    )}
                    run_record["strict_pass"] = False
                    print(f" FAIL (json parse) [{elapsed:.1f}s]")
                else:
                    metrics = evaluate(parsed, reference)
                    strict = all(v == 1.0 for v in metrics.values())
                    run_record["metrics"] = metrics
                    run_record["strict_pass"] = strict
                    run_record["failed_checks"] = [k for k, v in metrics.items() if v == 0.0] if not strict else []
                    if strict:
                        cond_passes += 1
                        strict_passes += 1
                        print(f" PASS [{elapsed:.1f}s]")
                    else:
                        print(f" FAIL ({', '.join(run_record['failed_checks'])}) [{elapsed:.1f}s]")

                runs.append(run_record)

            except Exception as e:
                elapsed = time.time() - t0
                print(f" ERROR: {e} [{elapsed:.1f}s]")
                runs.append({
                    "run_id": run_id,
                    "model_key": model_key,
                    "model_id": model_id,
                    "arm": arm,
                    "condition": cond,
                    "rep": rep,
                    "timestamp": ts,
                    "elapsed_s": round(elapsed, 2),
                    "error": str(e)[:500],
                    "prompt_sent": prompt,
                    "strict_pass": False,
                })
                time.sleep(2)

            time.sleep(0.3)

        print(f"  → {cond}: {cond_passes}/{reps}")

    lo, hi = wilson(strict_passes, total)
    summary = {
        "model_key": model_key,
        "model_id": model_id,
        "family": model_info["family"],
        "arm": arm,
        "total_runs": total,
        "strict_passes": strict_passes,
        "pass_rate": round(strict_passes / total, 4),
        "wilson_95": [round(lo, 4), round(hi, 4)],
        "conditions": {},
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "runs": runs,
    }
    for cond in conditions:
        cr = [r for r in runs if r["condition"] == cond]
        cp = sum(1 for r in cr if r.get("strict_pass"))
        summary["conditions"][cond] = {"passes": cp, "total": len(cr)}

    print(f"\n  SUMMARY: {strict_passes}/{total} = {strict_passes/total:.1%}  Wilson [{lo:.4f}, {hi:.4f}]")
    return summary

def save_prompts(output_dir: Path, arm: str, conditions: tuple[str, ...]):
    """Save exact prompt text per condition (saved once, referenced by runs)."""
    prompt_dir = output_dir / "prompts"
    prompt_dir.mkdir(parents=True, exist_ok=True)
    for cond in conditions:
        if arm == "G9":
            prompt = load_prompt(cond)
        else:
            prompt = build_g0_prompt(cond)
        (prompt_dir / f"{arm}__{cond}.md").write_text(prompt, encoding="utf-8")

def write_index(output_dir: Path, results: dict[str, dict], arm: str):
    """Write human-readable index and summary CSV."""
    index_lines = [
        f"# {arm} Full-Provenance Experiment Index",
        "",
        f"**Date**: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
        f"**Arm**: {arm}",
        f"**Protocol**: Stage B v5.4 frozen explicit-transition-delta",
        f"**Temperature**: 0",
        f"**Provider**: SiliconFlow",
        "",
        "## Per-Model Results",
        "",
        "| Model | Passes | Total | Rate | Wilson 95% CI |",
        "|---|---:|---:|---:|---|",
    ]
    csv_rows = []
    for mk, data in results.items():
        index_lines.append(
            f"| {mk} ({data['model_id']}) | {data['strict_passes']} | {data['total_runs']} | "
            f"{data['pass_rate']:.1%} | [{data['wilson_95'][0]}, {data['wilson_95'][1]}] |"
        )
        csv_rows.append({
            "model_key": mk,
            "model_id": data["model_id"],
            "arm": arm,
            "total_runs": data["total_runs"],
            "strict_passes": data["strict_passes"],
            "pass_rate": data["pass_rate"],
            "wilson_95_low": data["wilson_95"][0],
            "wilson_95_high": data["wilson_95"][1],
        })

    (output_dir / "_index.md").write_text("\n".join(index_lines) + "\n", encoding="utf-8")

    with open(output_dir / "_summary.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["model_key", "model_id", "arm", "total_runs",
                                                "strict_passes", "pass_rate", "wilson_95_low", "wilson_95_high"])
        writer.writeheader()
        writer.writerows(csv_rows)

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="command", required=True)

    sb = sub.add_parser("stage-b", help="Stage B v5.4 full protocol (G9)")
    sb.add_argument("--model", choices=list(MODELS.keys()))
    sb.add_argument("--all-models", action="store_true")
    sb.add_argument("--reps", type=int, default=REPS)
    sb.add_argument("--conditions", nargs="+", default=list(CONDITIONS))
    sb.add_argument("--output-dir", type=Path, required=True)

    sd = sub.add_parser("stage-d", help="Stage D G0 (no-contract arm)")
    sd.add_argument("--models", nargs="+", required=True, choices=list(MODELS.keys()))
    sd.add_argument("--reps", type=int, default=4)
    sd.add_argument("--conditions", nargs="+", default=list(CONDITIONS))
    sd.add_argument("--output-dir", type=Path, required=True)

    args = ap.parse_args()
    conditions = tuple(args.conditions)

    if args.command == "stage-b":
        arm = "G9"
        subdir_name = "stage-b-v54"
        models_to_run = list(MODELS.keys()) if args.all_models else [args.model]
        reps = args.reps
    elif args.command == "stage-d":
        arm = "G0"
        subdir_name = "stage-d-g0"
        models_to_run = args.models
        reps = args.reps

    output_dir = args.output_dir / subdir_name
    output_dir.mkdir(parents=True, exist_ok=True)

    # Save prompts once
    save_prompts(output_dir, arm, conditions)

    all_results = {}
    for mk in models_to_run:
        data = run_model(mk, conditions, reps, arm=arm)
        out_path = output_dir / f"{mk}__full.json"
        out_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"\n  Wrote: {out_path}")
        all_results[mk] = data
        if mk != models_to_run[-1]:
            print("\n  (cool-down 5s between models)")
            time.sleep(5)

    write_index(output_dir, all_results, arm)
    print(f"\n{'='*60}")
    print(f"  {arm} COMPLETE: {len(all_results)} models")
    for mk, data in all_results.items():
        print(f"    {mk:18s} {data['strict_passes']:3d}/{data['total_runs']:<3d} "
              f"Wilson [{data['wilson_95'][0]}, {data['wilson_95'][1]}]")
    print(f"  Index: {output_dir / '_index.md'}")
    print(f"{'='*60}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
