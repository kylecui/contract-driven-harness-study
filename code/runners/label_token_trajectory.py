#!/usr/bin/env python3
"""Heuristic trajectory labeling for topic-aware compaction A/B results.

This script works with the existing `ab_test_results.json`, which stores
per-API-call token records but not full message/tool text. Labels are therefore
token-trajectory heuristics, not human-verified semantic labels.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from statistics import mean
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def label_call(call: dict[str, int], prev_ctx: int | None) -> str:
    input_tokens = int(call.get("input", 0))
    output_tokens = int(call.get("output", 0))
    cache_read = int(call.get("cache_read", 0))
    effective_ctx = int(call.get("effective_ctx", 0))

    if cache_read == 0 and prev_ctx is not None:
        return "compaction_or_context_reset"
    if input_tokens >= 8000:
        return "large_tool_or_state_rebuild"
    if output_tokens >= 3500:
        return "large_generation"
    if prev_ctx is not None and effective_ctx - prev_ctx >= 8000:
        return "context_jump"
    if output_tokens <= 80 and input_tokens <= 400:
        return "short_control_step"
    return "normal_progress"


def summarize_variant(name: str, variant: dict[str, Any]) -> dict[str, Any]:
    calls = variant.get("per_message_tokens", [])
    labels: list[dict[str, Any]] = []
    prev_ctx: int | None = None

    for index, call in enumerate(calls, start=1):
        label = label_call(call, prev_ctx)
        row = {
            "call_index": index,
            "label": label,
            "input": call.get("input", 0),
            "output": call.get("output", 0),
            "cache_read": call.get("cache_read", 0),
            "effective_ctx": call.get("effective_ctx", 0),
        }
        labels.append(row)
        prev_ctx = int(call.get("effective_ctx", 0))

    counts: dict[str, int] = {}
    for row in labels:
        counts[row["label"]] = counts.get(row["label"], 0) + 1

    effective_contexts = [int(c.get("effective_ctx", 0)) for c in calls]
    avg_ctx = round(mean(effective_contexts), 2) if effective_contexts else 0

    return {
        "variant": name,
        "session_id": variant.get("session_id", ""),
        "api_calls": variant.get("messages", len(calls)),
        "compactions": variant.get("compactions", 0),
        "wall_time_s": variant.get("wall_time_s", 0),
        "peak_context_window": variant.get("peak_context_window", 0),
        "avg_effective_ctx": avg_ctx,
        "label_counts": counts,
        "labels": labels,
    }


def markdown_report(summary: dict[str, Any]) -> str:
    baseline = summary["baseline"]
    plugin = summary["plugin"]

    lines = [
        "# Token Trajectory Label Report",
        "",
        "## Method Note",
        "",
        "This report uses token-only heuristics because the current result JSON does not include full message or tool-call text. Treat labels as screening signals for later manual session inspection.",
        "",
        "## Variant Summary",
        "",
        "| Variant | API calls | Compactions | Wall time (s) | Peak context | Avg effective ctx |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for item in [baseline, plugin]:
        lines.append(
            f"| {item['variant']} | {item['api_calls']} | {item['compactions']} | "
            f"{item['wall_time_s']} | {item['peak_context_window']} | {item['avg_effective_ctx']} |"
        )

    label_names = sorted(
        set(baseline["label_counts"].keys()) | set(plugin["label_counts"].keys())
    )
    lines.extend(
        [
            "",
            "## Label Counts",
            "",
            "| Label | Baseline | Plugin | Delta |",
            "|---|---:|---:|---:|",
        ]
    )
    for label in label_names:
        b = baseline["label_counts"].get(label, 0)
        p = plugin["label_counts"].get(label, 0)
        lines.append(f"| `{label}` | {b} | {p} | {p - b:+d} |")

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- `large_tool_or_state_rebuild` and `context_jump` are candidate signals for state rebuilding or large tool-result ingestion.",
            "- `compaction_or_context_reset` marks cache-read-zero calls after the first call; these should align with compaction/reset points.",
            "- A real behavioral-change claim still requires message/tool text labels such as `state_rebuild`, `useful_progress`, and `verification`.",
            "",
            "## Next Step",
            "",
            "Preserve full session messages in future harness runs and join this token report with human or scripted tool-call labels.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Path to ab_test_results.json")
    parser.add_argument("--output-json", required=True)
    parser.add_argument("--output-md", required=True)
    args = parser.parse_args()

    result_path = Path(args.input)
    data = load_json(result_path)
    summary = {
        "source": str(result_path),
        "model": data.get("model", ""),
        "timestamp": data.get("timestamp", ""),
        "baseline": summarize_variant("baseline", data["baseline"]),
        "plugin": summarize_variant("plugin", data["plugin"]),
    }

    Path(args.output_json).write_text(
        json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    Path(args.output_md).write_text(markdown_report(summary), encoding="utf-8")


if __name__ == "__main__":
    main()

