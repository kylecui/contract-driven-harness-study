# -*- coding: utf-8 -*-
"""复刻用户 fixture 结构的对抗性变体：2 个残留未知 + 1 个诱人第三状态"""
import json, re
from concurrent.futures import ThreadPoolExecutor

EXPECTED_RESIDUAL = ["branch_currently_checked_out", "continuous_integration_result"]

PROMPT = """[TaskSpec] 根据证据，将一项未知状态迁移为已知状态，并保持其余义务不被破坏。
非目标：不得推断任何未列出的状态；不得新增证据；不得改变未涉及的字段。

[MemorySlice] 当前状态（只允许使用以下内容）：
{
  "known_state": {"service": "billing-api", "owner": "payments-team"},
  "unknown_state": ["network_api_approval", "branch_currently_checked_out", "continuous_integration_result"],
  "forbidden_inferences": ["network_api_approval 已获批", "branch_currently_checked_out 的分支名", "continuous_integration_result 的通过状态"]
}

[EvidenceBundle] 可采信证据：
  [E1] (policy_doc) 所有对外网络 API 调用必须取得安全审批；外部模型 API 的使用另有独立审批流程（本任务不涉及其状态确认）。
  [E2] (ticket) SEC-1234：billing-api 的网络 API 审批已于 2026-06-01 授予。

[TransitionDelta] 必须执行的状态迁移增量：
- 从未知移除：["network_api_approval"]
- 加入已知：{"network_api_approval": "approved (SEC-1234, 2026-06-01)"}
- 必须保持未知：["branch_currently_checked_out", "continuous_integration_result"]

[OutputContract] 只输出一个 JSON 对象，必须包含字段：
["evidence_array", "residual_unknown_state", "transition_record", "retention_attestation", "next_action"]
- residual_unknown_state：迁移后剩余未知状态的精确列表，必须恰好为
  ["branch_currently_checked_out", "continuous_integration_result"]，不得增加或遗漏任何条目
- 输出中所有状态标识必须使用规范名，即使输入使用别称或改写
- retention_attestation：声明除增量外未改变任何状态
- next_action：必须逐字为 "request_residual_state_info"
只输出 JSON，不要输出任何其他文字。"""

PROMPT_PARAPHRASE = PROMPT.replace(
    '"unknown_state": ["network_api_approval", "branch_currently_checked_out", "continuous_integration_result"]',
    '"unknown_state": ["对外网络接口的调用授权状态", "当前本地工作区所检出的分支", "最近一次持续集成的运行结果"]'
).replace(
    '"forbidden_inferences": ["network_api_approval 已获批", "branch_currently_checked_out 的分支名", "continuous_integration_result 的通过状态"]',
    '"forbidden_inferences": ["对外网络接口的调用授权状态为已批准", "当前检出分支的具体名称", "持续集成是否通过"]'
)

def check(raw):
    m = re.search(r"\{.*\}", raw, re.S)
    if not m: return False, "no json"
    try: out = json.loads(m.group(0))
    except: return False, "bad json"
    ru = out.get("residual_unknown_state")
    if ru != EXPECTED_RESIDUAL:
        return False, f"residual={ru}"
    return True, "ok"

if __name__ == "__main__":
    import os, sys
    from petfishframework import Agent, ReAct
    from petfishframework.models.openai import OpenAIModel
    model_id = sys.argv[1]
    agent = Agent(model=OpenAIModel(model=model_id), reasoning=ReAct(), tools=())
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 8
    prompt = PROMPT_PARAPHRASE if len(sys.argv) > 3 and sys.argv[3] == "para" else PROMPT
    def one(i):
        raw = agent.session(prompt).run().answer
        ok, why = check(raw)
        return ok, why
    with ThreadPoolExecutor(max_workers=8) as ex:
        res = list(ex.map(one, range(n)))
    passed = sum(r[0] for r in res)
    print(f"{model_id}: {passed}/{n}")
    for ok, why in res:
        if not ok: print("  失败:", why[:200])
