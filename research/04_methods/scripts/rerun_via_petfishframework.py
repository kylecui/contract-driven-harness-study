"""Round 04: Precise reproduction using petfishframework Agent + ReAct() pipeline.

Replicates the exact execution path of the original V4 experiments by using
the same framework (petfishframework v1.1.0) with Agent + ReAct() reasoning
and OpenAIModel for API calls. This closes the text-similarity gap from
Round 03 (which used bare API calls).

Usage:
    python rerun_via_petfishframework.py                    # all stages
    python rerun_via_petfishframework.py --stage stage7e-*  # specific stages
    python rerun_via_petfishframework.py --dry-run          # scan only
"""
from __future__ import annotations

import argparse
import fnmatch
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# Load framework
from petfishframework import Agent, ReAct
from petfishframework.models.openai import OpenAIModel

FROZEN_ROOT = Path("research/05_analysis/real-run-artifacts")
OUTPUT_ROOT = Path("research/05_analysis/experiment-rounds/round-04-precise-petfishframework")
DEFAULT_MODEL = "Qwen/Qwen3-8B"

def load_env():
    for line in open(".env"):
        parts = line.strip().split("=", 1)
        if len(parts) == 2:
            os.environ[parts[0]] = parts[1]

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
    p = run_dir / "metrics.json"
    if p.exists():
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            return None
    return None

def load_frozen_output(run_dir: Path) -> str | None:
    p = run_dir / "output.md"
    return p.read_text(encoding="utf-8") if p.exists() else None

def load_adapter_model(run_dir: Path) -> str:
    p = run_dir / "adapter_request.json"
    if p.exists():
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
            if "model" in data:
                return data["model"]
            if "model_request" in data and "model" in data["model_request"]:
                return data["model_request"]["model"]
        except Exception:
            pass
    return DEFAULT_MODEL

def text_similarity(a: str, b: str) -> float:
    if not a or not b:
        return 0.0
    sa, sb = set(a.split()), set(b.split())
    return len(sa & sb) / len(sa | sb) if sa and sb else 0.0

def run_via_petfishframework(prompt: str, model_id: str, max_retries: int = 2) -> dict[str, Any]:
    """Send prompt through petfishframework Agent + ReAct() pipeline."""
    model = OpenAIModel(model=model_id)
    agent = Agent(model=model, reasoning=ReAct(), tools=())

    for attempt in range(1, max_retries + 1):
        try:
            t0 = time.time()
            session = agent.session(prompt)
            result = session.run()
            elapsed = time.time() - t0
            return {
                "answer": result.answer,
                "session_id": getattr(result, "session_id", ""),
                "elapsed_s": round(elapsed, 2),
            }
        except Exception as e:
            if attempt < max_retries:
                time.sleep(2 ** attempt)
            else:
                raise

def rerun_stage(stage_dir: Path, output_dir: Path, dry_run: bool = False) -> dict[str, Any]:
    stage_name = stage_dir.name
    run_dirs = sorted([d for d in stage_dir.iterdir() if d.is_dir() and (d / "prompt.md").exists()])

    if not run_dirs:
        print(f"\n  {stage_name}: no runs, skipping")
        return {"stage": stage_name, "total_runs": 0}

    print(f"\n{'='*60}")
    print(f"  STAGE: {stage_name} ({len(run_dirs)} runs)")
    print(f"{'='*60}")

    if dry_run:
        for rd in run_dirs:
            model = load_adapter_model(rd)
            print(f"    {rd.name} | model={model}")
        return {"stage": stage_name, "total_runs": len(run_dirs), "dry_run": True}

    runs = []
    json_valid = 0
    high_sim = 0
    errors = 0

    for i, rd in enumerate(run_dirs, 1):
        run_name = rd.name
        prompt = (rd / "prompt.md").read_text(encoding="utf-8")
        model_id = load_adapter_model(rd)
        frozen_output = load_frozen_output(rd)
        frozen_metrics = load_frozen_metrics(rd)

        print(f"  [{i}/{len(run_dirs)}] {run_name[:50]} ...", end="", flush=True)

        t0 = time.time()
        try:
            result = run_via_petfishframework(prompt, model_id)
            elapsed = result["elapsed_s"]
            answer = result["answer"]
            parsed = extract_json(answer)

            record = {
                "run_id": f"{stage_name}__{run_name}",
                "stage": stage_name,
                "frozen_run_name": run_name,
                "model": model_id,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "elapsed_s": elapsed,
                "raw_answer": answer,
                "parsed_output": parsed,
                "json_valid": parsed is not None,
            }

            if frozen_output:
                sim = text_similarity(answer, frozen_output)
                record["text_similarity_to_frozen"] = round(sim, 4)
                if sim > 0.8:
                    high_sim += 1

            if parsed is not None:
                json_valid += 1
                print(f" OK [{elapsed:.1f}s]{' sim=' + str(round(sim, 2)) if frozen_output else ''}")
            else:
                print(f" FAIL(json) [{elapsed:.1f}s]")

            runs.append(record)

        except Exception as e:
            elapsed = round(time.time() - t0, 2)
            errors += 1
            print(f" ERROR: {str(e)[:80]} [{elapsed}s]")
            runs.append({
                "run_id": f"{stage_name}__{run_name}",
                "stage": stage_name,
                "frozen_run_name": run_name,
                "model": model_id,
                "error": str(e)[:500],
                "elapsed_s": elapsed,
            })

        time.sleep(0.5)

    summary = {
        "stage": stage_name,
        "total_runs": len(run_dirs),
        "json_valid": json_valid,
        "high_similarity": high_sim,
        "errors": errors,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "runs": runs,
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    out_path = output_dir / f"{stage_name}__pf.json"
    out_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n  → {stage_name}: {len(runs)} runs, {json_valid} JSON valid, {high_sim} high-sim, {errors} errors")
    print(f"  Wrote: {out_path}")
    return summary

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--stage", default="*", help="Glob pattern (default: *)")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--output-dir", type=Path, default=OUTPUT_ROOT)
    args = ap.parse_args()

    load_env()

    all_stages = sorted([d for d in FROZEN_ROOT.iterdir() if d.is_dir()])
    matching = [d for d in all_stages if fnmatch.fnmatch(d.name, args.stage)]
    if args.stage == "*":
        matching = [d for d in matching if d.name != "stage-b-v54-explicit-delta-stability"]
        print("NOTE: Skipping stage-b-v54 (already re-run in Round 02)")

    print(f"\nStages: {len(matching)}, Total runs: {sum(len([r for r in s.iterdir() if r.is_dir() and (r / 'prompt.md').exists()]) for s in matching)}")

    if args.dry_run:
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
        if i < len(matching):
            time.sleep(3)

    master = args.output_dir / "_master-summary.json"
    master.parent.mkdir(parents=True, exist_ok=True)
    master.write_text(json.dumps(all_summaries, indent=2, ensure_ascii=False), encoding="utf-8")

    total = sum(s["total_runs"] for s in all_summaries)
    jv = sum(s.get("json_valid", 0) for s in all_summaries)
    hs = sum(s.get("high_similarity", 0) for s in all_summaries)
    err = sum(s.get("errors", 0) for s in all_summaries)
    print(f"\n{'='*60}")
    print(f"ROUND 04 COMPLETE (petfishframework Agent + ReAct)")
    print(f"  Stages: {len(all_summaries)}")
    print(f"  Total runs: {total}")
    print(f"  JSON valid: {jv}")
    print(f"  High similarity: {hs}")
    print(f"  Errors: {err}")
    print(f"  Master: {master}")
    print(f"{'='*60}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
