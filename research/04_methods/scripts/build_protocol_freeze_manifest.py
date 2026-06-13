#!/usr/bin/env python3
"""Create a deterministic SHA-256 manifest for a frozen experiment protocol."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import date
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def collect_files(includes: list[str], output: Path) -> list[Path]:
    files: set[Path] = set()
    for raw_path in includes:
        path = Path(raw_path)
        if path.is_dir():
            files.update(item for item in path.rglob("*") if item.is_file())
        elif path.is_file():
            files.add(path)
        else:
            raise FileNotFoundError(raw_path)
    files.discard(output)
    return sorted(files, key=lambda item: item.as_posix())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--protocol-id", required=True)
    parser.add_argument("--base-commit", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--include", action="append", required=True)
    args = parser.parse_args()

    output = Path(args.output)
    files = collect_files(args.include, output)
    payload = {
        "protocol_id": args.protocol_id,
        "prepared_date": date.today().isoformat(),
        "base_commit": args.base_commit,
        "hash_algorithm": "sha256",
        "file_count": len(files),
        "files": [
            {
                "path": path.as_posix(),
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
            for path in files
        ],
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {len(files)} hashes to {output}")


if __name__ == "__main__":
    main()
