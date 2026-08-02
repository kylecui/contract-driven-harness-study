"""Full-history reproduction: re-run ALL frozen artifact prompts.

Scans every run directory under real-run-artifacts/, loads the frozen prompt,
sends it to the API, and saves the new response with full provenance. Compares
new result against frozen metrics.

Output: experiment-rounds/round-03-full-history/{stage_name}/__full.json

Usage:
    python rerun_all_frozen.py                    # all stages
    python rerun_all_frozen.py --stage stage7e-*  # specific stages by glob
    python rerun_all_frozen.py --dry-run          # scan only, no API calls
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

FROZEN_ROOT = Path("research/05_analysis/real-run-artifacts")
OUTPUT_ROOT = Path("research/05_analysis/experiment-rounds/round-03-full-history")
DEFAULT_MODEL = "Qwen/Qwen3-8B"  # primary model for all V4 experiments

def call_api(model_id: str, prompt: str, max_retries: int = 2) -> dict[str, Any]:
    key = os.environ.get("OPENAI_API_KEY")
    base = os.environ.get("OPENAI_BASE_URL", "https://api.siliconflow.cn/v1")
    if not key:
        raise RuntimeError("OPENAI_API_KEY not set")
    payload = {
        "model": model_id,
        "messages": [
            {"role": "system", "content": "You are a precise JSON-producing agent. Return ONLY the JSON object specified by the task. No markdown fences, no prose."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0,
        "max_tokens": 4096,
        "stream": False,
    }
    body = json.dumps(payload).encode("utf-8")
    url = base.rstrip("/") + "/chat/completions"
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
            }
        except Exception as e:
            if attempt < max_retries:
                time.sleep(2 ** attempt)
            else:
                raise

def extract_json(content: str) -> dict[str, Any] | None:
    text = content.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*\n?", "", text)
        text = re.sub(r"\n?```\s*$", "", text)
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1:
        return None
    try:
        return json.loads(text[start:end + 1])
    except json.JSONDecodeError:
        return None

def load_frozen_metrics(run_dir: Path) -> dict[str, Any] | None:
    metrics_path = run_dir / "metrics.json"
    if metrics_path.exists():
        try:
            return json.loads(metrics_path.read_text(encoding="utf-8"))
        except Exception:
            return None
    return None

def load_frozen_output(run_dir: Path) -> str | None:
    output_path = run_dir / "output.md"
    if output_path.exists():
        return output_path.read_text(encoding="utf-8")
    return None

def load_adapter_model(run_dir: Path) -> str:
    """Try to extract model ID from frozen adapter_request.json."""
    adapter_path = run_dir / "adapter_request.json"
    if adapter_path.exists():
        try:
            data = json.loads(adapter_path.read_text(encoding="utf-8"))
            # Look for model field in various locations
            if "model" in data:
                return data["model"]
            if "model_request" in data and "model" in data["model_request"]:
                return data["model_request"]["model"]
        except Exception:
            pass
    return DEFAULT_MODEL

def text_similarity(a: str, b: str) -> float:
    """Simple character-level Jaccard similarity for rough comparison."""
    if not a or not b:
        return 0.0
    set_a = set(a.split())
    set_b = set(b.split())
    if not set_a or not set_b:
        return 0.0
    return len(set_a & set_b) / len(set_a | set_b)

def rerun_stage(stage_dir: Path, output_dir: Path, dry_run: bool = False) -> dict[str, Any]:
    """Re-run all prompts in a frozen stage directory."""
    stage_name = stage_dir.name
    run_dirs = sorted([d for d in stage_dir.iterdir() if d.is_dir() and (d / "prompt.md").exists()])

    if not run_dirs:
        print(f"\n  {stage_name}: no run directories with prompt.md, skipping")
        return {"stage": stage_name, "total_runs": 0, "runs": []}

    print(f"\n{'='*60}")
    print(f"  STAGE: {stage_name}")
    print(f"  Runs: {len(run_dirs)}")
    print(f"{'='*60}")

    if dry_run:
        for rd in run_dirs:
            model = load_adapter_model(rd)
            frozen_metrics = load_frozen_metrics(rd)
            ts = frozen_metrics.get("task_success", "?") if frozen_metrics else "?"
            print(f"    {rd.name} | model={model} | frozen task_success={ts}")
        return {"stage": stage_name, "total_runs": len(run_dirs), "dry_run": True}

    runs = []
    passed = 0
    json_parsed = 0
    matched_frozen = 0

    for i, rd in enumerate(run_dirs, 1):
        run_name = rd.name
        prompt_path = rd / "prompt.md"
        prompt = prompt_path.read_text(encoding="utf-8")

        model_id = load_adapter_model(rd)
        frozen_metrics = load_frozen_metrics(rd)
        frozen_output = load_frozen_output(rd)
        frozen_ts = frozen_metrics.get("task_success") if frozen_metrics else None

        print(f"  [{i}/{len(run_dirs)}] {run_name[:50]} ...", end="", flush=True)

        t0 = time.time()
        try:
            result = call_api(model_id, prompt)
            elapsed = time.time() - t0
            content = result["content"]
            parsed = extract_json(content)

            run_record = {
                "run_id": f"{stage_name}__{run_name}",
                "stage": stage_name,
                "frozen_run_name": run_name,
                "model": model_id,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "elapsed_s": round(elapsed, 2),
                "usage": result.get("usage", {}),
                "response_id": result.get("response_id", ""),
                "raw_content": content,
                "parsed_output": parsed,
                "frozen_task_success": frozen_ts,
            }

            if parsed is not None:
                json_parsed += 1
                run_record["json_valid"] = True
            else:
                run_record["json_valid"] = False

            # Compare with frozen output if available
            if frozen_output:
                sim = text_similarity(content, frozen_output)
                run_record["text_similarity_to_frozen"] = round(sim, 4)
                if sim > 0.8:
                    matched_frozen += 1

            # Check if frozen task_success was 1.0
            if frozen_ts == 1.0 and parsed is not None:
                passed += 1
                print(f" OK [{elapsed:.1f}s]")
            elif frozen_ts == 1.0 and parsed is None:
                print(f" FAIL(json) [{elapsed:.1f}s]")
            elif frozen_ts is not None and frozen_ts < 1.0:
                print(f" (frozen was fail) [{elapsed:.1f}s]")
            else:
                print(f" done [{elapsed:.1f}s]")

            runs.append(run_record)

        except Exception as e:
            elapsed = time.time() - t0
            print(f" ERROR: {e} [{elapsed:.1f}s]")
            runs.append({
                "run_id": f"{stage_name}__{run_name}",
                "stage": stage_name,
                "frozen_run_name": run_name,
                "model": model_id,
                "error": str(e)[:500],
                "elapsed_s": round(elapsed, 2),
            })

        time.sleep(0.3)

    summary = {
        "stage": stage_name,
        "total_runs": len(run_dirs),
        "json_parsed": json_parsed,
        "matched_frozen_high_similarity": matched_frozen,
        "frozen_task_success_1_count": passed,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "runs": runs,
    }

    # Save
    output_dir.mkdir(parents=True, exist_ok=True)
    out_path = output_dir / f"{stage_name}__full.json"
    out_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n  → {stage_name}: {len(runs)} runs re-executed, {json_parsed} JSON valid, {matched_frozen} high-similarity to frozen")
    print(f"  Wrote: {out_path}")

    return summary

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--stage", default="*", help="Glob pattern for stage directories (default: *)")
    ap.add_argument("--dry-run", action="store_true", help="Scan only, no API calls")
    ap.add_argument("--output-dir", type=Path, default=OUTPUT_ROOT)
    args = ap.parse_args()

    # Load env
    for line in open(".env"):
        parts = line.strip().split("=", 1)
        if len(parts) == 2:
            os.environ[parts[0]] = parts[1]

    # Find all stage directories
    import fnmatch
    all_stages = sorted([d for d in FROZEN_ROOT.iterdir() if d.is_dir()])
    matching = [d for d in all_stages if fnmatch.fnmatch(d.name, args.stage)]

    # Skip stage-b-v54 (already re-run in Round 02)
    if args.stage == "*":
        matching = [d for d in matching if d.name != "stage-b-v54-explicit-delta-stability"]
        print(f"NOTE: Skipping stage-b-v54-explicit-delta-stability (already re-run in Round 02)")

    print(f"\nStages to process: {len(matching)}")
    total_runs = 0
    for s in matching:
        run_count = len([d for d in s.iterdir() if d.is_dir() and (d / "prompt.md").exists()])
        total_runs += run_count
        print(f"  {s.name}: {run_count} runs")
    print(f"Total runs to execute: {total_runs}")
    print(f"Estimated time: {total_runs * 0.5 / 60:.0f}-{total_runs * 1.0 / 60:.0f} minutes")

    if args.dry_run:
        print("\n=== DRY RUN ===")
        for s in matching:
            rerun_stage(s, args.output_dir, dry_run=True)
        return 0

    all_summaries = []
    for i, s in enumerate(matching, 1):
        print(f"\n{'#'*60}")
        print(f"# STAGE {i}/{len(matching)}: {s.name}")
        print(f"{'#'*60}")
        summary = rerun_stage(s, args.output_dir)
        all_summaries.append({k: v for k, v in summary.items() if k != "runs"})
        # Cool-down between stages
        if i < len(matching):
            time.sleep(3)

    # Master summary
    master_path = args.output_dir / "_master-summary.json"
    master_path.parent.mkdir(parents=True, exist_ok=True)
    master_path.write_text(json.dumps(all_summaries, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"\n{'='*60}")
    print(f"ALL STAGES COMPLETE")
    print(f"  Stages: {len(all_summaries)}")
    print(f"  Total runs: {sum(s['total_runs'] for s in all_summaries)}")
    print(f"  JSON valid: {sum(s.get('json_parsed', 0) for s in all_summaries)}")
    print(f"  High similarity to frozen: {sum(s.get('matched_frozen_high_similarity', 0) for s in all_summaries)}")
    print(f"  Master summary: {master_path}")
    print(f"{'='*60}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
