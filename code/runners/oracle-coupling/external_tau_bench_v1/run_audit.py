#!/usr/bin/env python3
"""External oracle-coupling audit: tau-bench (sierra-research/tau-bench).

Applies the paired-intervention protocol from the oracle-coupling working
paper to an external, widely used public agent benchmark. tau-bench's
reward function (tau_bench/envs/base.py::calculate_reward) derives its
validation target by REPLAYING the golden ``task.actions`` field against a
fresh database and hashing the result (``gt_data_hash``); the agent's final
database state is compared against that golden-derived target. This is the
C = G(P, Y) signature: the answer-bearing field constructs the checking
policy.

Interventions (fixture: retail dev task 14 — modify_pending_order_address
writes the golden literal ``city="San Antonio"`` into state; all 20 dev
tasks have ``outputs == []`` so reward is purely the DB-hash component):

1. baseline_matching_state    — replay(golden) as agent state → reward 1
2. baseline_perturbed_state   — replay(golden) + wrong city → reward 0
3. golden_deletion            — task.actions == [] → target becomes the
   initial-state hash; the previously-correct agent state now scores 0
   (necessity: the policy is fully determined by the golden field)
4. golden_poisoning_city      — change ONLY the golden action's city kwarg
   (public facts fixed) → gt_data_hash shifts → the same agent state flips
   1→0, while a state matching the poisoned golden scores 1 (value flow:
   the policy moves with the answer field)
5. public_fact_counterfactual — change a public fact the golden never
   touches (another user's city) in the initial database → a matching run
   still scores 1 (symmetric response to public facts; rules out a
   constant target)

Zero LLM calls: the reward path is deterministic tool execution + hashing.
The agent "state" is a synthetic replay; this audit measures the reward
function's dependence structure, not agent behavior.
"""

from __future__ import annotations

import copy
import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

AUDIT_CODE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(AUDIT_CODE_ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from layout import REPO_ROOT  # noqa: E402

TAU_BENCH_PINNED_COMMIT = "59a200c6d575d595120f1cb70fea53cef0632f6b"
TAU_BENCH_URL = "https://github.com/sierra-research/tau-bench"
TASK_SPLIT = "dev"
TASK_INDEX = 14
TARGET_ORDER_ID = "#W3289292"
GOLDEN_CITY = "San Antonio"
POISON_CITY = "Houston"
AGENT_WRONG_CITY = "Chicago"
OUTPUT_DIR = (
    REPO_ROOT
    / "data/reproduction/oracle-coupling/external_tau_bench_v1/artifacts"
)
MANIFEST_VERSION = "ETB-v1-exact-1"


def tau_bench_root() -> Path:
    root = Path(os.environ.get("TAU_BENCH_ROOT", REPO_ROOT / "tmp" / "tau-bench"))
    if not root.is_dir():
        raise SystemExit(
            f"tau-bench source not found at {root}. Clone it:\n"
            f"  git clone {TAU_BENCH_URL} {root}\n"
            f"  git -C {root} checkout {TAU_BENCH_PINNED_COMMIT}"
        )
    head = subprocess.run(
        ["git", "-C", str(root), "rev-parse", "HEAD"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()
    if head != TAU_BENCH_PINNED_COMMIT:
        raise SystemExit(
            f"tau-bench HEAD {head} != pinned {TAU_BENCH_PINNED_COMMIT} (fail-closed)"
        )
    return root


def make_env():
    sys.path.insert(0, str(tau_bench_root()))
    from tau_bench.envs.retail.env import MockRetailDomainEnv

    env = MockRetailDomainEnv(user_strategy="human", task_split=TASK_SPLIT, task_index=TASK_INDEX)
    assert env.task.actions[0].kwargs["city"] == GOLDEN_CITY
    assert env.task.actions[0].kwargs["order_id"] == TARGET_ORDER_ID
    assert env.task.outputs == []
    return env


def replay(env, actions, data):
    """Apply golden-style actions to ``data`` exactly as calculate_reward does."""
    for action in actions:
        if action.name not in env.terminate_tools:
            env.tools_map[action.name].invoke(data=data, **action.kwargs)
    return data


def get_order(data, order_id):
    return data["orders"][order_id]


def set_task(env, actions):
    from tau_bench.types import Task

    env.task = Task(
        user_id=env.task.user_id,
        actions=actions,
        instruction=env.task.instruction,
        outputs=env.task.outputs,
    )


def score(env, agent_state):
    """Set the agent's final DB state and return the reward result."""
    env.data = copy.deepcopy(agent_state)
    result = env.calculate_reward()
    return {
        "reward": result.reward,
        "r_actions": result.info.r_actions,
        "gt_data_hash": result.info.gt_data_hash,
    }


def build_cases() -> dict:
    env = make_env()
    golden_actions = copy.deepcopy(env.task.actions)

    # --- agent states -------------------------------------------------
    correct_state = replay(env, copy.deepcopy(golden_actions), env.data_load_func())
    assert get_order(correct_state, TARGET_ORDER_ID)["address"]["city"] == GOLDEN_CITY

    wrong_city_state = copy.deepcopy(correct_state)
    get_order(wrong_city_state, TARGET_ORDER_ID)["address"]["city"] = AGENT_WRONG_CITY

    poisoned_actions = copy.deepcopy(golden_actions)
    poisoned_actions[0].kwargs["city"] = POISON_CITY
    poisoned_match_state = replay(env, copy.deepcopy(poisoned_actions), env.data_load_func())
    assert get_order(poisoned_match_state, TARGET_ORDER_ID)["address"]["city"] == POISON_CITY

    # --- interventions --------------------------------------------------
    set_task(env, copy.deepcopy(golden_actions))
    baseline_matching = score(env, correct_state)
    set_task(env, copy.deepcopy(golden_actions))
    baseline_perturbed = score(env, wrong_city_state)

    set_task(env, [])  # golden deletion
    golden_deletion = score(env, correct_state)

    set_task(env, copy.deepcopy(poisoned_actions))
    poisoning_original = score(env, correct_state)
    set_task(env, copy.deepcopy(poisoned_actions))
    poisoning_matched = score(env, poisoned_match_state)

    # public-fact counterfactual: mutate a user the golden never touches
    initial = env.data_load_func()
    other_user_id = next(uid for uid in initial["users"] if uid != env.task.user_id)
    initial["users"][other_user_id]["address"]["city"] = "Portland"
    original_load = env.data_load_func
    env.data_load_func = lambda: copy.deepcopy(initial)
    try:
        set_task(env, copy.deepcopy(golden_actions))
        pf_matched_state = replay(env, copy.deepcopy(golden_actions), copy.deepcopy(initial))
        public_fact = score(env, pf_matched_state)
    finally:
        env.data_load_func = original_load

    cases = {
        "baseline_matching_state": baseline_matching,
        "baseline_perturbed_state": baseline_perturbed,
        "golden_deletion": golden_deletion,
        "golden_poisoning_city_original_agent": poisoning_original,
        "golden_poisoning_city_matched_agent": poisoning_matched,
        "public_fact_counterfactual": public_fact,
    }
    checks = {
        "baseline_matching_scores_1": baseline_matching["reward"] == 1.0,
        "baseline_perturbed_scores_0": baseline_perturbed["reward"] == 0.0,
        "deletion_flips_correct_state_to_0": golden_deletion["reward"] == 0.0,
        "poisoning_flips_original_state_to_0": poisoning_original["reward"] == 0.0,
        "poisoning_matched_state_scores_1": poisoning_matched["reward"] == 1.0,
        "policy_moved_with_golden_field": poisoning_original["gt_data_hash"]
        != baseline_matching["gt_data_hash"],
        "public_fact_change_still_scores_1": public_fact["reward"] == 1.0,
    }
    return {
        "protocol_id": "ETB-v1",
        "external_source": {
            "url": TAU_BENCH_URL,
            "pinned_commit": TAU_BENCH_PINNED_COMMIT,
            "reward_path": "tau_bench/envs/base.py::Env.calculate_reward",
            "task_split": TASK_SPLIT,
            "task_index": TASK_INDEX,
            "task_user": "james_kim_7213",
            "target_order_id": TARGET_ORDER_ID,
            "golden_city": GOLDEN_CITY,
            "poison_city": POISON_CITY,
            "agent_wrong_city": AGENT_WRONG_CITY,
        },
        "cases": cases,
        "checks": checks,
        "overall_passed": all(checks.values()),
        "claim_boundary": (
            "Paired-intervention audit of one external benchmark's reward "
            "dependence structure on one retail task, executed offline with "
            "synthetic agent states (zero LLM calls). Demonstrates the "
            "golden-actions replay signature; no claim about tau-bench task "
            "quality, other splits, or agent behavior."
        ),
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
    }


def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_manifest(results_path: Path) -> dict:
    files = [
        "code/runners/oracle-coupling/external_tau_bench_v1/README.md",
        "code/runners/oracle-coupling/external_tau_bench_v1/run_audit.py",
        "code/runners/oracle-coupling/external_tau_bench_v1/verify_manifest.py",
        "code/runners/oracle-coupling/external_tau_bench_v1/tests/test_external_tau_bench.py",
        "code/runners/oracle-coupling/layout.py",
        "data/reproduction/oracle-coupling/external_tau_bench_v1/artifacts/results.json",
    ]
    entries = [
        {
            "path": relative,
            "sha256": sha256_of(REPO_ROOT / relative),
            "bytes": (REPO_ROOT / relative).stat().st_size,
        }
        for relative in files
    ]
    return {
        "manifest_version": MANIFEST_VERSION,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "entry_count": len(entries),
        "entries_root_sha256": hashlib.sha256(
            json.dumps(entries, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest(),
        "entries": entries,
        "external_pin_note": (
            "The tau-bench source tree is external and pinned by commit in "
            "results.json; this manifest closes over the audit code and the "
            "frozen results only."
        ),
    }


def main() -> int:
    results = build_cases()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    results_path = OUTPUT_DIR / "results.json"
    results_path.write_text(
        json.dumps(results, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    manifest = build_manifest(results_path)
    manifest_path = OUTPUT_DIR.parent / "SHA256_MANIFEST.json"
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(
        json.dumps(
            {
                "overall_passed": results["overall_passed"],
                "checks": results["checks"],
                "results": results_path.relative_to(REPO_ROOT).as_posix(),
                "manifest": manifest_path.relative_to(REPO_ROOT).as_posix(),
            },
            indent=2,
        )
    )
    return 0 if results["overall_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
