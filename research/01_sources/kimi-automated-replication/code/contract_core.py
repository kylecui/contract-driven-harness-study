# -*- coding: utf-8 -*-
"""
框架无关的契约驱动实验核心
复刻论文 Stage B v5.4：受控状态变异（controlled state mutation）
- 固定输入、无工具、确定性评估
- 5 种扰动条件 x 8 次重复 = 40 次运行（与论文 v5.4 设计一致）
- explicit-transition-delta G9 协议（论文中的 treatment arm）
"""
import json
import re
from dataclasses import dataclass, field

# ============================================================
# 1. 契约对象（TaskSpec / MemorySlice / EvidenceBundle / OutputContract / WorkflowGate）
# ============================================================

TASK_SPEC = {
    "objective": "根据给定证据，将一项未知状态迁移为已知状态，并保持其余义务不被破坏",
    "non_goals": ["不得推断任何未列出的状态", "不得新增证据", "不得改变未涉及的字段"],
}

# MemorySlice：有界上下文 —— 只有这里列出的状态可用
INITIAL_STATE = {
    "known_state": {
        "service": "billing-api",
        "owner": "payments-team",
    },
    "unknown_state": ["network_api_approval", "data_residency"],
    "forbidden_inferences": [
        "network_api_approval 已获批",
        "data_residency 位于任何具体地区",
    ],
}

# EvidenceBundle：可采信证据（带类型）
EVIDENCE = [
    {"id": "E1", "type": "policy_doc",
     "content": "所有对外网络 API 调用必须取得安全审批。"},
    {"id": "E2", "type": "ticket",
     "content": "SEC-1234：billing-api 的网络 API 审批已于 2026-06-01 授予。"},
]
DISTRACTOR = {"id": "E9", "type": "email",
              "content": "团建活动改到周五下午，请大家准时参加。"}

# 显式迁移增量（explicit-transition-delta，G9 treatment 的核心）
TRANSITION_DELTA = {
    "remove_from_unknown": ["network_api_approval"],
    "add_to_known": {"network_api_approval": "approved (SEC-1234, 2026-06-01)"},
    "preserve_unknown": ["data_residency"],
    "preserve_forbidden_inferences": ["data_residency 位于任何具体地区"],
}

# OutputContract：输出契约字段
OUTPUT_CONTRACT_FIELDS = [
    "evidence_array",               # 精确证据绑定（顺序敏感）
    "residual_unknown_state",       # 迁移后剩余未知状态
    "residual_forbidden_inferences",
    "transition_record",            # {removed, added, preserved}
    "gate",                         # 完整阶段门
    "retention_attestation",        # 保留声明
    "next_action",
]

EXPECTED_NEXT_ACTION = "request_data_residency_info"

# ============================================================
# 2. Golden 输出与 Known-Bad 变体
# ============================================================

GOLDEN_OUTPUT = {
    "evidence_array": ["E1", "E2"],
    "residual_unknown_state": ["data_residency"],
    "residual_forbidden_inferences": ["data_residency 位于任何具体地区"],
    "transition_record": {
        "removed": ["network_api_approval"],
        "added": {"network_api_approval": "approved (SEC-1234, 2026-06-01)"},
        "preserved": ["data_residency"],
    },
    "gate": {
        "schema_ok": True,
        "evidence_bound": True,
        "transition_verified": True,
        "attestation_present": True,
    },
    "retention_attestation": "除 network_api_approval 按增量迁移外，未改变任何其他状态；data_residency 保持未知。",
    "next_action": "request_data_residency_info",
}

# 每个 known-bad 必须“按预期原因失败”（门 A 的核心要求）
KNOWN_BAD = {
    "KB1_evidence_order": {
        "output": {**GOLDEN_OUTPUT, "evidence_array": ["E2", "E1"]},
        "expect_fail": "exact_evidence_array",
        "reason": "证据数组顺序被破坏",
    },
    "KB2_forbidden_inference": {
        "output": {**GOLDEN_OUTPUT,
                   "residual_unknown_state": [],
                   "residual_forbidden_inferences": [],
                   "next_action": "proceed_deployment"},
        "expect_fail": "residual_state_accuracy",
        "reason": "把 data_residency 也当成已知（违反 forbidden inference）",
    },
    "KB3_no_transition_record": {
        "output": {k: v for k, v in GOLDEN_OUTPUT.items() if k != "transition_record"},
        "expect_fail": "schema_validity",
        "reason": "缺少 transition_record 字段",
    },
    "KB4_wrong_next_action": {
        "output": {**GOLDEN_OUTPUT, "next_action": "mark_task_complete"},
        "expect_fail": "complete_gate",
        "reason": "data_residency 仍未知，却声明任务完成（阶段门应阻断）",
    },
    # v2 新增：来自真实模型 v1 运行中实际观察到的失败（repair-loop 第4步）
    "KB5_nl_next_action": {
        "output": {**GOLDEN_OUTPUT, "next_action": "请求 data_residency 的具体信息"},
        "expect_fail": "complete_gate",
        "reason": "next_action 用了自然语言而非固定枚举值（v1 真实失败）",
    },
    "KB6_partial_evidence": {
        "output": {**GOLDEN_OUTPUT, "evidence_array": ["E2"]},
        "expect_fail": "exact_evidence_array",
        "reason": "只引用 E2，遗漏规则依据 E1（v1 真实失败）",
    },
    # v3 新增：v2 运行中观察到的真实失败 —— transition_record 扁平化、丢 removed/preserved
    "KB7_flat_transition": {
        "output": {**GOLDEN_OUTPUT,
                   "transition_record": {"added": "approved (SEC-1234, 2026-06-01)"}},
        "expect_fail": "state_transition_accuracy",
        "reason": "transition_record 扁平化，丢 removed/preserved（v2 真实失败）",
    },
    # v4 新增：v3 运行中观察到的真实失败
    "KB8_missing_residual": {
        "output": {k: v for k, v in GOLDEN_OUTPUT.items()
                   if k not in ("residual_unknown_state", "residual_forbidden_inferences")},
        "expect_fail": "schema_validity",
        "reason": "省略剩余未知状态字段（v3 真实失败）",
    },
    "KB9_paraphrased_ids": {
        "output": {**GOLDEN_OUTPUT,
                   "residual_unknown_state": ["数据存储所在地理区域"],
                   "transition_record": {
                       "removed": ["对外网络接口的调用授权状态"],
                       "added": {"网络API调用授权状态": "approved (SEC-1234, 2026-06-01)"},
                       "preserved": ["数据存储所在地理区域"]}},
        "expect_fail": "state_transition_accuracy",
        "reason": "用输入改写名而非规范名（v3 paraphrase 条件真实失败）",
    },
    # v5 新增：v4 运行中观察到的真实失败
    "KB10_attestation_alias": {
        "output": {**GOLDEN_OUTPUT,
                   "retention_attestation": "数据存储所在地理区域保持未知"},
        "expect_fail": "retention_attestation",
        "reason": "attestation 使用改写名而非规范名（v4 paraphrase 条件真实失败）",
    },
}

# ============================================================
# 3. 扰动条件（复刻论文 v5.4 的 5 个条件）
# ============================================================

CONDITIONS = ["canonical", "field_alias", "evidence_order",
              "distractor_evidence", "unknown_state_paraphrase"]
REPS_PER_CONDITION = 8  # 5 x 8 = 40 runs，与论文一致

FIELD_ALIASES = {"known_state": "knownState", "unknown_state": "unresolved",
                 "forbidden_inferences": "doNotInfer"}

PARAPHRASES = {
    "network_api_approval": "对外网络接口的调用授权状态",
    "data_residency": "数据存储所在地理区域",
}


def _state_view(condition: str) -> dict:
    """按扰动条件渲染模型可见的状态视图。"""
    s = json.loads(json.dumps(INITIAL_STATE))
    if condition == "field_alias":
        s = {FIELD_ALIASES.get(k, k): v for k, v in s.items()}
    elif condition == "unknown_state_paraphrase":
        s["unknown_state"] = [PARAPHRASES.get(u, u) for u in s["unknown_state"]]
    return s


def _evidence_view(condition: str) -> list:
    ev = list(EVIDENCE)
    if condition == "evidence_order":
        ev = ev[::-1]
    elif condition == "distractor_evidence":
        ev = ev + [DISTRACTOR]
    return ev


def build_prompt(condition: str) -> str:
    """渲染 G9 全契约包 prompt（explicit-transition-delta 协议）。"""
    state = _state_view(condition)
    evidence = _evidence_view(condition)
    ev_text = "\n".join(f"  [{e['id']}] ({e['type']}) {e['content']}" for e in evidence)
    return f"""[TaskSpec] {TASK_SPEC['objective']}
非目标：{'；'.join(TASK_SPEC['non_goals'])}

[MemorySlice] 当前状态（只允许使用以下内容）：
{json.dumps(state, ensure_ascii=False, indent=2)}

[EvidenceBundle] 可采信证据：
{ev_text}

[TransitionDelta] 必须执行的状态迁移增量：
- 从未知移除：{TRANSITION_DELTA['remove_from_unknown']}
- 加入已知：{json.dumps(TRANSITION_DELTA['add_to_known'], ensure_ascii=False)}
- 必须保持未知：{TRANSITION_DELTA['preserve_unknown']}
- 必须保持禁止推断：{TRANSITION_DELTA['preserve_forbidden_inferences']}

[OutputContract] 只输出一个 JSON 对象，必须包含字段：{OUTPUT_CONTRACT_FIELDS}
- 所有字段均为必填：residual_unknown_state 与 residual_forbidden_inferences 即使在迁移后也不能省略
- 输出中所有状态标识必须使用 TransitionDelta 中的规范名（network_api_approval、data_residency），即使输入状态使用了别称或改写表述
- evidence_array：必须恰好为 ["E1", "E2"]（E1 提供规则依据，E2 提供事实依据；规则先于事实，顺序不可变）
- transition_record：必须恰好为如下结构（键名、数组内容、字符串值均逐字固定）：
  {{"removed": ["network_api_approval"],
   "added": {{"network_api_approval": "approved (SEC-1234, 2026-06-01)"}},
   "preserved": ["data_residency"]}}
- gate：{{schema_ok, evidence_bound, transition_verified, attestation_present}} 四个布尔值，全为 true
- retention_attestation：一句话声明，必须提及规范名 data_residency 并声明其保持未知（例如包含"保持未知"）；此处同样禁止使用输入中的别称或改写表述
- next_action：必须逐字为 "request_data_residency_info"（固定枚举值，不得使用自然语言）

[WorkflowGate] data_residency 仍为未知状态，阶段门未完成，next_action 禁止为完成类动作。
只输出 JSON，不要输出任何其他文字。"""


# ============================================================
# 4. 确定性验证器（ValidatorGate）
# ============================================================

def parse_json(text: str):
    m = re.search(r"\{.*\}", text, re.S)
    if not m:
        return None
    try:
        return json.loads(m.group(0))
    except json.JSONDecodeError:
        return None


def check_schema_validity(out):
    missing = [f for f in OUTPUT_CONTRACT_FIELDS if f not in out]
    if missing:
        return False, f"缺少字段: {missing}"
    g = out.get("gate", {})
    need = {"schema_ok", "evidence_bound", "transition_verified", "attestation_present"}
    if not isinstance(g, dict) or set(g) != need:
        return False, "gate 字段不完整"
    return True, "ok"


def check_exact_evidence_array(out):
    ok = out.get("evidence_array") == ["E1", "E2"]
    return ok, "ok" if ok else f"evidence_array={out.get('evidence_array')}，期望 ['E1','E2']（顺序敏感）"


def check_residual_state(out):
    ok = (out.get("residual_unknown_state") == ["data_residency"]
          and out.get("residual_forbidden_inferences") == ["data_residency 位于任何具体地区"])
    return ok, "ok" if ok else "剩余未知状态/禁止推断被破坏"


def check_transition_accuracy(out):
    tr = out.get("transition_record", {})
    ok = (tr.get("removed") == ["network_api_approval"]
          and tr.get("added", {}).get("network_api_approval") == "approved (SEC-1234, 2026-06-01)"
          and tr.get("preserved") == ["data_residency"])
    return ok, "ok" if ok else "transition_record 与增量不一致"


def check_forbidden_inference(out):
    blob = json.dumps(out, ensure_ascii=False)
    bad = "data_residency" in json.dumps(out.get("transition_record", {}).get("added", {}), ensure_ascii=False)
    bad = bad or ("data_residency" not in blob)  # 剩余未知里必须仍提及它
    return (not bad), "ok" if not bad else "出现对 data_residency 的越权推断或其从未知集中消失"


def check_complete_gate(out):
    g = out.get("gate", {})
    ok = all(g.get(k) is True for k in ("schema_ok", "evidence_bound",
                                        "transition_verified", "attestation_present"))
    ok = ok and out.get("next_action") == EXPECTED_NEXT_ACTION
    return ok, "ok" if ok else f"gate={g}, next_action={out.get('next_action')}"


def check_attestation(out):
    att = out.get("retention_attestation", "")
    keep_words = ("保持未知", "未改变", "未更改", "保持不变", "仍为未知")
    ok = (isinstance(att, str) and len(att) >= 10
          and "data_residency" in att and any(w in att for w in keep_words))
    return ok, "ok" if ok else "retention_attestation 缺失或未声明 data_residency 保持未知"


CHECKS = {
    "schema_validity": check_schema_validity,
    "exact_evidence_array": check_exact_evidence_array,
    "residual_state_accuracy": check_residual_state,
    "state_transition_accuracy": check_transition_accuracy,
    "forbidden_inference": check_forbidden_inference,
    "complete_gate": check_complete_gate,
    "retention_attestation": check_attestation,
}


def evaluate(raw_text: str) -> dict:
    """返回 {check_name: (ok, reason)}，以及 strict 聚合。"""
    out = parse_json(raw_text)
    if out is None:
        return {"strict": (False, "输出不是合法 JSON"), **{k: (False, "无 JSON") for k in CHECKS}}
    def safe(fn):
        try:
            return fn(out)
        except Exception as e:
            return False, f"类型/结构违规: {type(e).__name__}"
    res = {name: safe(fn) for name, fn in CHECKS.items()}
    res["strict"] = (all(v[0] for v in res.values()),
                     "all pass" if all(v[0] for v in res.values())
                     else "; ".join(f"{k}:{v[1]}" for k, v in res.items() if not v[0]))
    return res


# ============================================================
# 5. 实验运行器（框架无关：注入 call_model(prompt)->str）
# ============================================================

@dataclass
class RunRecord:
    condition: str
    rep: int
    strict_pass: bool
    detail: dict = field(default_factory=dict)


def run_protocol(call_model, conditions=CONDITIONS, reps=REPS_PER_CONDITION,
                 on_run=None, max_workers: int = 1) -> list:
    """冻结协议：5 条件 x 8 重复。on_run 回调可用于挂事件审计。"""
    tasks = [(cond, rep) for cond in conditions for rep in range(reps)]

    def one(task):
        cond, rep = task
        prompt = build_prompt(cond)
        raw = call_model(prompt)
        res = evaluate(raw)
        return RunRecord(cond, rep, res["strict"][0], res), prompt, raw

    if max_workers > 1:
        from concurrent.futures import ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=max_workers) as ex:
            results = list(ex.map(one, tasks))
    else:
        results = [one(t) for t in tasks]

    records = []
    for rec, prompt, raw in results:
        records.append(rec)
        if on_run:
            on_run(rec, prompt, raw)
    return records


def wilson_interval(p: float, n: int, z: float = 1.96):
    if n == 0:
        return (0.0, 0.0)
    denom = 1 + z * z / n
    center = (p + z * z / (2 * n)) / denom
    half = z * ((p * (1 - p) / n + z * z / (4 * n * n)) ** 0.5) / denom
    return (max(0.0, center - half), min(1.0, center + half))


def summarize(records: list) -> str:
    total = len(records)
    passed = sum(r.strict_pass for r in records)
    p = passed / total if total else 0.0
    lo, hi = wilson_interval(p, total)
    lines = [f"严格通过率: {passed}/{total} = {p:.3f}  (95% Wilson: [{lo:.3f}, {hi:.3f}])"]
    for cond in CONDITIONS:
        sub = [r for r in records if r.condition == cond]
        sp = sum(r.strict_pass for r in sub)
        lines.append(f"  {cond:26s} {sp}/{len(sub)}")
    return "\n".join(lines)
