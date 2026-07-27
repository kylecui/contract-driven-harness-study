"""Build Stage D matched overhead matrix from G0 and G9 data."""
import json
from pathlib import Path

RECORDS_DIR = Path("research/05_analysis/author-confirmation-records")

def extract_g9_usage(model_key: str) -> dict:
    """Extract G9 cost data from verified records."""
    path = RECORDS_DIR / f"{model_key}-confirmed.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    runs = data.get("runs", [])
    valid = [r for r in runs if "usage" in r and r.get("usage")]
    if not valid:
        return {}
    prompt_tokens = sum(r["usage"].get("prompt_tokens", 0) for r in valid)
    completion_tokens = sum(r["usage"].get("completion_tokens", 0) for r in valid)
    latencies = [r.get("elapsed_s", 0) for r in valid if r.get("elapsed_s")]
    passes = sum(1 for r in valid if r.get("strict_pass"))
    return {
        "arm": "G9",
        "total_runs": len(valid),
        "strict_passes": passes,
        "pass_rate": round(passes / len(valid), 4),
        "total_prompt_tokens": prompt_tokens,
        "total_completion_tokens": completion_tokens,
        "avg_prompt_tokens": prompt_tokens // len(valid),
        "avg_completion_tokens": completion_tokens // len(valid),
        "avg_latency_s": round(sum(latencies) / len(latencies), 2) if latencies else 0,
    }

def load_g0(model_key: str) -> dict:
    path = Path(f"research/05_analysis/stage-d-g0-{model_key}.json")
    return json.loads(path.read_text(encoding="utf-8"))

# Build matrix
models = ["qwen3-8b", "deepseek-v3.2"]
matrix = {}

for mk in models:
    g0 = load_g0(mk)
    g9 = extract_g9_usage(mk)
    
    # Compute overhead
    g0_prompt = g0.get("avg_prompt_tokens_per_run", 0)
    g9_prompt = g9.get("avg_prompt_tokens", 0)
    g0_completion = g0.get("avg_completion_tokens_per_run", 0)
    g9_completion = g9.get("avg_completion_tokens", 0)
    g0_latency = g0.get("avg_latency_s", 0)
    g9_latency = g9.get("avg_latency_s", 0)
    
    matrix[mk] = {
        "model": mk,
        "G0": {
            "pass_rate": g0.get("pass_rate", 0),
            "strict_passes": g0.get("strict_passes", 0),
            "total_runs": g0.get("total_runs", 0),
            "avg_prompt_tokens": g0_prompt,
            "avg_completion_tokens": g0_completion,
            "avg_latency_s": g0_latency,
        },
        "G9": {
            "pass_rate": g9.get("pass_rate", 0),
            "strict_passes": g9.get("strict_passes", 0),
            "total_runs": g9.get("total_runs", 0),
            "avg_prompt_tokens": g9_prompt,
            "avg_completion_tokens": g9_completion,
            "avg_latency_s": g9_latency,
        },
        "overhead": {
            "prompt_token_ratio": round(g9_prompt / max(g0_prompt, 1), 2),
            "completion_token_ratio": round(g9_completion / max(g0_completion, 1), 2),
            "latency_ratio": round(g9_latency / max(g0_latency, 1), 2),
            "pass_rate_gain": round(g9.get("pass_rate", 0) - g0.get("pass_rate", 0), 4),
        }
    }

# Output
out = Path("research/05_analysis/stage-d-overhead-matrix.json")
out.write_text(json.dumps(matrix, indent=2, ensure_ascii=False), encoding="utf-8")

# Print summary
print("=" * 70)
print("Stage D Matched Overhead Matrix")
print("=" * 70)
for mk, m in matrix.items():
    print(f"\n{mk}:")
    print(f"  {'':15s} {'G0 (no contract)':>20s}  {'G9 (full contract)':>20s}  {'Ratio':>8s}")
    print(f"  {'Pass rate':15s} {m['G0']['pass_rate']:>19.1%}  {m['G9']['pass_rate']:>19.1%}  {'—':>8s}")
    print(f"  {'Prompt tok/run':15s} {m['G0']['avg_prompt_tokens']:>20d}  {m['G9']['avg_prompt_tokens']:>20d}  {m['overhead']['prompt_token_ratio']:>7.1f}x")
    print(f"  {'Compl tok/run':15s} {m['G0']['avg_completion_tokens']:>20d}  {m['G9']['avg_completion_tokens']:>20d}  {m['overhead']['completion_token_ratio']:>7.1f}x")
    print(f"  {'Latency (s)':15s} {m['G0']['avg_latency_s']:>20.1f}  {m['G9']['avg_latency_s']:>20.1f}  {m['overhead']['latency_ratio']:>7.1f}x")

print(f"\nWrote: {out}")
