#!/usr/bin/env python3
"""Validate provider mapping config for real benchmark adapters."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any


REQUIRED_MODEL_TIERS = ["strong_model", "budget_model"]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def validate(config: dict[str, Any], *, require_keys: bool) -> list[str]:
    errors: list[str] = []
    providers = config.get("providers")
    model_tiers = config.get("model_tiers")

    if not isinstance(providers, dict) or not providers:
        errors.append("providers must be a non-empty object")
        providers = {}
    if not isinstance(model_tiers, dict) or not model_tiers:
        errors.append("model_tiers must be a non-empty object")
        model_tiers = {}

    for tier in REQUIRED_MODEL_TIERS:
        if tier not in model_tiers:
            errors.append(f"missing model tier mapping: {tier}")

    for tier, mapping in model_tiers.items():
        if not isinstance(mapping, dict):
            errors.append(f"model_tiers.{tier} must be an object")
            continue
        provider_name = mapping.get("provider")
        model_name = mapping.get("model")
        if not provider_name:
            errors.append(f"model_tiers.{tier}.provider missing")
        elif provider_name not in providers:
            errors.append(f"model_tiers.{tier}.provider references unknown provider: {provider_name}")
        if not model_name:
            errors.append(f"model_tiers.{tier}.model missing")

    for provider_name, provider in providers.items():
        if not isinstance(provider, dict):
            errors.append(f"providers.{provider_name} must be an object")
            continue
        key_env = provider.get("api_key_env")
        if not key_env:
            errors.append(f"providers.{provider_name}.api_key_env missing")
        elif require_keys and not os.environ.get(str(key_env)):
            errors.append(f"environment variable not set: {key_env}")
        timeout = provider.get("timeout_seconds", 120)
        if not isinstance(timeout, int) or timeout <= 0:
            errors.append(f"providers.{provider_name}.timeout_seconds must be a positive integer")

    return errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--require-keys", action="store_true")
    args = parser.parse_args()

    config = load_json(Path(args.config))
    errors = validate(config, require_keys=args.require_keys)
    if errors:
        print("FAIL provider config")
        for error in errors:
            print(f"  - {error}")
        raise SystemExit(1)
    print("OK provider config")


if __name__ == "__main__":
    main()

