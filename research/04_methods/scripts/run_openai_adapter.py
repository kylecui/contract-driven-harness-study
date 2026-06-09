#!/usr/bin/env python3
"""OpenAI-compatible adapter for the first real benchmark slice.

By default this script runs in `--dry-run` mode and only checks the queue,
provider config, prompts, and output paths. Use `--execute` to make network API
calls after setting the configured API key environment variable.

The HTTP call uses OpenAI-compatible Chat Completions shape. If a target
provider requires a different API, keep the run artifact contract and replace
only `call_provider`.
"""

from __future__ import annotations

import argparse
import json
import os
import time
from pathlib import Path
from typing import Any
from urllib import request


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def dump_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def append_jsonl(path: Path | None, payload: dict[str, Any]) -> None:
    if path is None:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False) + "\n")


def monotonic_ms() -> int:
    return int(time.monotonic() * 1000)


def call_provider(
    *,
    provider: dict[str, Any],
    model: str,
    prompt: str,
    temperature: float,
    max_output_tokens: int,
) -> str:
    key_env = str(provider["api_key_env"])
    api_key = os.environ.get(key_env)
    if not api_key:
        raise RuntimeError(f"Missing API key environment variable: {key_env}")

    base_url = str(provider.get("base_url", "https://api.openai.com/v1")).rstrip("/")
    timeout = int(provider.get("timeout_seconds", 120))
    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": prompt,
            }
        ],
        "temperature": temperature,
        "max_tokens": max_output_tokens,
    }
    data = json.dumps(payload).encode("utf-8")
    req = request.Request(
        f"{base_url}/chat/completions",
        data=data,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with request.urlopen(req, timeout=timeout) as response:  # noqa: S310 - user-configured endpoint
        result = json.loads(response.read().decode("utf-8"))
    return result["choices"][0]["message"]["content"]


def run_adapter(
    *,
    manifest: dict[str, Any],
    config: dict[str, Any],
    execute: bool,
    limit: int | None,
    report_path: Path | None = None,
    event_log_path: Path | None = None,
) -> dict[str, Any]:
    defaults = config.get("defaults", {})
    temperature = float(defaults.get("temperature", 0))
    max_output_tokens = int(defaults.get("max_output_tokens", 2000))

    results = []
    run_total = len(manifest.get("runs", []))
    for index, run in enumerate(manifest["runs"], start=1):
        if limit is not None and index > limit:
            break
        prompt_path = Path(run["paths"]["prompt"])
        output_path = Path(run["paths"]["output"])
        trace_path = Path(run["paths"]["tool_trace"])
        request_path = Path(run["paths"]["adapter_request"])
        adapter_request = load_json(request_path)
        model_tier = str(adapter_request["model_tier"])
        mapping = config["model_tiers"][model_tier]
        provider = config["providers"][mapping["provider"]]
        model = mapping["model"]
        run_started_ms = monotonic_ms()

        status = "dry_run"
        error = None
        append_jsonl(
            event_log_path,
            {
                "event": "run_start",
                "run_id": run["run_id"],
                "index": index,
                "run_total": run_total,
                "execute": execute,
                "model_tier": model_tier,
                "provider": mapping["provider"],
                "model": model,
                "harness_arm": run.get("harness_arm"),
                "prompt": str(prompt_path),
                "output": str(output_path),
                "monotonic_ms": run_started_ms,
            },
        )
        if execute:
            try:
                prompt = prompt_path.read_text(encoding="utf-8")
                append_jsonl(
                    event_log_path,
                    {
                        "event": "provider_request_start",
                        "run_id": run["run_id"],
                        "provider": mapping["provider"],
                        "model": model,
                        "timeout_seconds": provider.get("timeout_seconds", 120),
                        "temperature": temperature,
                        "max_output_tokens": max_output_tokens,
                        "prompt_bytes": len(prompt.encode("utf-8")),
                        "monotonic_ms": monotonic_ms(),
                    },
                )
                output = call_provider(
                    provider=provider,
                    model=model,
                    prompt=prompt,
                    temperature=temperature,
                    max_output_tokens=max_output_tokens,
                )
                output_path.write_text(output, encoding="utf-8")
                elapsed_ms = monotonic_ms() - run_started_ms
                trace_path.write_text(
                    json.dumps(
                        {
                            "event": "model_call",
                            "provider": mapping["provider"],
                            "model": model,
                            "temperature": temperature,
                            "max_output_tokens": max_output_tokens,
                            "tools_used": [],
                            "elapsed_ms": elapsed_ms,
                        },
                        ensure_ascii=False,
                    )
                    + "\n",
                    encoding="utf-8",
                )
                status = "executed"
                append_jsonl(
                    event_log_path,
                    {
                        "event": "provider_response_end",
                        "run_id": run["run_id"],
                        "status": status,
                        "output_bytes": len(output.encode("utf-8")),
                        "elapsed_ms": elapsed_ms,
                        "monotonic_ms": monotonic_ms(),
                    },
                )
            except Exception as exc:  # noqa: BLE001 - preserve adapter failures
                status = "failed"
                error = str(exc)
                append_jsonl(
                    event_log_path,
                    {
                        "event": "provider_error",
                        "run_id": run["run_id"],
                        "status": status,
                        "error": error,
                        "elapsed_ms": monotonic_ms() - run_started_ms,
                        "monotonic_ms": monotonic_ms(),
                    },
                )

        results.append(
            {
                "run_id": run["run_id"],
                "model_tier": model_tier,
                "provider": mapping["provider"],
                "model": model,
                "status": status,
                "error": error,
                "prompt": str(prompt_path),
                "output": str(output_path),
                "elapsed_ms": monotonic_ms() - run_started_ms,
            }
        )
        append_jsonl(
            event_log_path,
            {
                "event": "run_end",
                "run_id": run["run_id"],
                "status": status,
                "error": error,
                "elapsed_ms": monotonic_ms() - run_started_ms,
                "monotonic_ms": monotonic_ms(),
            },
        )
        if report_path is not None:
            dump_json(
                report_path,
                {
                    "execute": execute,
                    "processed": len(results),
                    "partial": index < run_total and (limit is None or index < limit),
                    "results": results,
                },
            )

    return {
        "execute": execute,
        "processed": len(results),
        "results": results,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--config", required=True)
    parser.add_argument("--report", required=True)
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument(
        "--event-log",
        default=None,
        help="Optional JSONL path for incremental per-run adapter events.",
    )
    args = parser.parse_args()

    manifest = load_json(Path(args.manifest))
    config = load_json(Path(args.config))
    report_path = Path(args.report)
    report = run_adapter(
        manifest=manifest,
        config=config,
        execute=args.execute,
        limit=args.limit,
        report_path=report_path,
        event_log_path=Path(args.event_log) if args.event_log else None,
    )
    dump_json(report_path, report)
    print(f"Processed {report['processed']} runs; execute={report['execute']}")
    if any(item["status"] == "failed" for item in report["results"]):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
