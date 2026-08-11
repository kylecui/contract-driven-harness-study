"""SQLite-backed transactional implementation of the bounded policy gate."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
SCHEMA_SQL = (ROOT / "policy.sql").read_text(encoding="utf-8")


def _json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


class SQLitePolicyBackend:
    """Evaluate and commit one compiled policy inside SQLite transactions."""

    def __init__(
        self,
        policy: dict[str, Any],
        database: str | Path = ":memory:",
        *,
        initialise: bool = True,
    ) -> None:
        self.policy = policy
        self.database = str(database)
        self.connection = sqlite3.connect(self.database, isolation_level=None, timeout=0.0)
        self.connection.execute("PRAGMA foreign_keys = ON")
        if self.database != ":memory:":
            self.connection.execute("PRAGMA journal_mode = WAL")
            self.connection.execute("PRAGMA synchronous = FULL")
        if initialise:
            self.connection.executescript(SCHEMA_SQL)
            self._load_policy()
            self.reset_state()

    def close(self) -> None:
        self.connection.close()

    def _load_policy(self) -> None:
        p = self.policy
        self.connection.execute(
            "INSERT INTO policy VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                p["fixture_id"],
                p["family"],
                p["decision"],
                p["gate"]["status"],
                p["gate"]["reason_code"],
                p["gate"]["permitted_action"],
                p["next_action"],
            ),
        )
        for patch in p["patches"]:
            self.connection.execute(
                "INSERT INTO policy_patch(path, from_json, to_json) VALUES (?, ?, ?)",
                (patch["path"], _json(patch["from"]), _json(patch["to"])),
            )
            self.connection.executemany(
                "INSERT INTO policy_patch_evidence(path, evidence_id) VALUES (?, ?)",
                [(patch["path"], evidence_id) for evidence_id in patch["evidence_ids"]],
            )
        self.connection.executemany(
            "INSERT INTO policy_preserved(path, value_json) VALUES (?, ?)",
            [(item["path"], _json(item["value"])) for item in p["preserved_state"]],
        )
        self.connection.executemany(
            "INSERT INTO policy_decision_evidence(evidence_id) VALUES (?)",
            [(value,) for value in p["decision_evidence_ids"]],
        )
        self.connection.executemany(
            "INSERT INTO policy_unknown(value) VALUES (?)",
            [(value,) for value in p["unknown_state"]],
        )
        self.connection.executemany(
            "INSERT INTO policy_forbidden(value) VALUES (?)",
            [(value,) for value in p["forbidden_inferences"]],
        )

    def reset_state(self, state: dict[str, Any] | None = None) -> None:
        active = state if state is not None else self.policy["initial_state"]
        self.connection.execute("BEGIN IMMEDIATE")
        try:
            self.connection.execute("DELETE FROM candidate")
            self.connection.execute("DELETE FROM state_kv")
            self.connection.executemany(
                "INSERT INTO state_kv(path, value_json, version) VALUES (?, ?, 0)",
                [(path, _json(value)) for path, value in active.items()],
            )
            self.connection.execute("COMMIT")
        except Exception:
            self.connection.execute("ROLLBACK")
            raise

    def state(self) -> dict[str, Any]:
        return {
            row[0]: json.loads(row[1])
            for row in self.connection.execute(
                "SELECT path, value_json FROM state_kv ORDER BY path"
            )
        }

    def versions(self) -> dict[str, int]:
        return dict(
            self.connection.execute("SELECT path, version FROM state_kv ORDER BY path")
        )

    def evaluate_and_commit(self, candidate: Any) -> dict[str, Any]:
        before = self.state()
        self.connection.execute("BEGIN IMMEDIATE")
        try:
            self.connection.execute("DELETE FROM candidate")
            self.connection.execute(
                "INSERT INTO candidate(singleton, raw_json) VALUES (1, ?)",
                (_json(candidate),),
            )
            reasons = [row[0] for row in self.connection.execute(
                "SELECT reason FROM candidate_violations"
            )]
            accepted = not reasons
            wrote = False
            if accepted and candidate.get("decision") == "apply":
                for patch in candidate["state_patch"]:
                    cursor = self.connection.execute(
                        """
                        UPDATE state_kv
                           SET value_json = ?, version = version + 1
                         WHERE path = ?
                           AND json_extract(value_json, '$') IS json_extract(?, '$')
                        """,
                        (_json(patch["to"]), patch["path"], _json(patch["from"])),
                    )
                    if cursor.rowcount != 1:
                        raise RuntimeError("live state changed after policy evaluation")
                wrote = bool(candidate["state_patch"])
            self.connection.execute("COMMIT")
        except Exception:
            self.connection.execute("ROLLBACK")
            raise
        after = self.state()
        return {
            "accepted": accepted,
            "reason_codes": reasons,
            "wrote": wrote,
            "before": before,
            "after": after,
            "state_changed": before != after,
            "versions": self.versions(),
        }

    def set_live_value(self, path: str, value: Any) -> None:
        self.connection.execute("BEGIN IMMEDIATE")
        try:
            cursor = self.connection.execute(
                "UPDATE state_kv SET value_json = ?, version = version + 1 WHERE path = ?",
                (_json(value), path),
            )
            if cursor.rowcount != 1:
                raise KeyError(path)
            self.connection.execute("COMMIT")
        except Exception:
            self.connection.execute("ROLLBACK")
            raise
