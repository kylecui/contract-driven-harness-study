# -*- coding: utf-8 -*-
"""
能力地板探针（floor probe）
从受控状态变异任务的 7 项义务中提取 8 个最小能力检查，
每个一次调用、确定性判定，目标是：用 ~8 次廉价调用预测模型是否"在地板以上"，
避免对地板以下模型浪费完整 40 次冻结协议。
"""
import json, re, sys
from concurrent.futures import ThreadPoolExecutor

PROBES = [
    ("P1_json_formation",
     '只输出JSON对象 {"a": 1, "b": [2, 3], "c": {"d": "x"}}，不要其他文字。',
     lambda t: (lambda o: isinstance(o, dict) and o.get("a")==1 and o.get("b")==[2,3] and isinstance(o.get("c"),dict))(parse(t))),
    ("P2_verbatim_token",
     '只输出JSON {"code": "approved (SEC-1234, 2026-06-01)"}，code值逐字复制引号内内容，不要其他文字。',
     lambda t: (lambda o: isinstance(o, dict) and o.get("code")=="approved (SEC-1234, 2026-06-01)")(parse(t))),
    ("P3_enum_compliance",
     '从固定枚举 request_info / hold / escalate 中选择 request_info。只输出JSON对象 {"next_action": "request_info"}，不要输出任何其他文字。',
     lambda t: (lambda o: isinstance(o, dict) and o.get("next_action")=="request_info")(parse(t))),
    ("P4_field_retention",
     '输入 {"x": 1, "y": 2, "z": 3}。输出同样的三个字段，只把 y 改成 20，不得省略任何字段。只输出JSON。',
     lambda t: (lambda o: isinstance(o, dict) and o.get("x")==1 and o.get("y")==20 and o.get("z")==3)(parse(t))),
    ("P5_unknown_preservation",
     '已知 service=billing-api；未知 data_residency（禁止推断其取值）。输出JSON {"known": {"service": "billing-api"}, "unknown": ["data_residency"]}，保持未知项原样列出。只输出JSON。',
     lambda t: (lambda o: isinstance(o, dict) and o.get("unknown")==["data_residency"] and "data_residency" not in json.dumps(o.get("known",{}),ensure_ascii=False))(parse(t))),
    ("P6_canonical_mapping",
     '输入中提到"数据存储所在地理区域"（规范名 data_residency）。输出JSON {"state_id": "data_residency"}，必须使用规范名。只输出JSON。',
     lambda t: (lambda o: isinstance(o, dict) and o.get("state_id")=="data_residency")(parse(t))),
    ("P7_order_sensitivity",
     '输出JSON {"evidence": ["E1", "E2"]}，顺序必须是 E1 在前 E2 在后。只输出JSON。',
     lambda t: (lambda o: isinstance(o, dict) and o.get("evidence")==["E1","E2"])(parse(t))),
    ("P8_no_extras",
     '输出JSON {"a": 1, "b": 2}，只能有 a 和 b 两个字段，不得添加任何其他字段。只输出JSON。',
     lambda t: (lambda o: isinstance(o, dict) and set(o.keys())=={"a","b"})(parse(t))),
]

def parse(text):
    m = re.search(r"\{.*\}", text, re.S)
    if not m: return None
    try: return json.loads(m.group(0))
    except json.JSONDecodeError: return None

def run_probe(model_id, make_call):
    results = {}
    with ThreadPoolExecutor(max_workers=8) as ex:
        futs = {name: ex.submit(make_call, prompt) for name, prompt, _ in PROBES}
        for name, prompt, check in PROBES:
            try:
                ok = bool(check(futs[name].result()))
            except Exception:
                ok = False
            results[name] = ok
    passed = sum(results.values())
    return passed, results

if __name__ == "__main__":
    import os
    from petfishframework import Agent, ReAct
    from petfishframework.models.openai import OpenAIModel
    model_id = sys.argv[1]
    agent = Agent(model=OpenAIModel(model=model_id), reasoning=ReAct(), tools=())
    passed, results = run_probe(model_id, lambda p: agent.session(p).run().answer)
    print(f"{model_id}: 探针 {passed}/8  {'' if passed==8 else '<-- 地板以下'}")
    for k, v in results.items():
        if not v: print(f"   失败: {k}")
