#!/usr/bin/env python3
"""Freeze the exact FEC-v2 source, input, test, and result closure."""

from __future__ import annotations

import json

from verify_manifest import MANIFEST_PATH, build_manifest_payload


def main() -> None:
    payload = build_manifest_payload()
    MANIFEST_PATH.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "manifest": str(MANIFEST_PATH.relative_to(MANIFEST_PATH.parents[4])),
                "entry_count": payload["entry_count"],
                "entries_root_sha256": payload["entries_root_sha256"],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
