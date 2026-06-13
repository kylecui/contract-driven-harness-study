#!/usr/bin/env python3
"""Local tests for provider-response audit metadata."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_openai_adapter import parse_provider_response, retry_lineage


class ProviderResponseTests(unittest.TestCase):
    def test_openai_usage_is_preserved_and_normalized(self) -> None:
        parsed = parse_provider_response(
            {
                "id": "chatcmpl-test",
                "model": "example/model",
                "created": 123,
                "system_fingerprint": "fp-test",
                "choices": [{"message": {"content": "ok"}}],
                "usage": {
                    "prompt_tokens": 10,
                    "completion_tokens": 4,
                    "total_tokens": 14,
                    "prompt_tokens_details": {"cached_tokens": 2},
                },
            },
            header_request_id="request-test",
        )

        self.assertEqual(parsed["content"], "ok")
        self.assertEqual(parsed["response_id"], "chatcmpl-test")
        self.assertEqual(parsed["request_id"], "request-test")
        self.assertEqual(parsed["usage"]["prompt_tokens"], 10)
        self.assertEqual(parsed["usage"]["completion_tokens"], 4)
        self.assertEqual(parsed["usage"]["total_tokens"], 14)
        self.assertEqual(
            parsed["usage"]["raw"]["prompt_tokens_details"]["cached_tokens"], 2
        )

    def test_missing_usage_remains_explicitly_unavailable(self) -> None:
        parsed = parse_provider_response(
            {"choices": [{"message": {"content": "ok"}}]}
        )

        self.assertIsNone(parsed["usage"])
        self.assertIsNone(parsed["response_id"])
        self.assertIsNone(parsed["request_id"])

    def test_retry_lineage_defaults_and_declared_retry(self) -> None:
        self.assertEqual(
            retry_lineage({}, run_id="run-1"),
            {"lineage_id": "run-1", "attempt": 1, "retry_of_run_id": None},
        )
        self.assertEqual(
            retry_lineage(
                {
                    "lineage_id": "macro-cell-1",
                    "attempt": 2,
                    "retry_of_run_id": "run-1",
                },
                run_id="run-2",
            ),
            {
                "lineage_id": "macro-cell-1",
                "attempt": 2,
                "retry_of_run_id": "run-1",
            },
        )


if __name__ == "__main__":
    unittest.main()
