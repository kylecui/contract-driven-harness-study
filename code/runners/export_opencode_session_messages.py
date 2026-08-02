#!/usr/bin/env python3
"""Export raw OpenCode session messages for later trajectory labeling."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import httpx


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, required=True)
    parser.add_argument("--session-id", required=True)
    parser.add_argument("--password", default="test")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    headers = {"Authorization": f"Bearer {args.password}"}
    with httpx.Client(
        base_url=f"http://127.0.0.1:{args.port}",
        headers=headers,
        timeout=60,
    ) as client:
        response = client.get(f"/api/session/{args.session_id}/message")
        response.raise_for_status()
        messages = response.json()

    Path(args.output).write_text(
        json.dumps(messages, indent=2, ensure_ascii=False), encoding="utf-8"
    )


if __name__ == "__main__":
    main()

