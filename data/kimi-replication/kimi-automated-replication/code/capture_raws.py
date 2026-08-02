# -*- coding: utf-8 -*-
"""全程留痕重跑：输入 prompt + 原始输出逐条保存"""
import json, sys
from concurrent.futures import ThreadPoolExecutor
from petfishframework import Agent, ReAct
from petfishframework.models.openai import OpenAIModel
from contract_core import build_prompt, evaluate, CONDITIONS, REPS_PER_CONDITION
import variant_user_fixture as V

def run(agent, prompt):
    return agent.session(prompt).run().answer

def capture(model_id, tag, make_prompt_eval, tasks, workers=10):
    agent = Agent(model=OpenAIModel(model=model_id), reasoning=ReAct(), tools=())
    def one(t):
        name, prompt = t
        raw = run(agent, prompt)
        ok, detail = make_prompt_eval(raw)
        return {"task": name, "prompt": prompt, "raw_output": raw, "pass": ok, "detail": detail}
    with ThreadPoolExecutor(max_workers=workers) as ex:
        recs = list(ex.map(one, tasks))
    passed = sum(r["pass"] for r in recs)
    print(f"{tag} {model_id}: {passed}/{len(recs)}", flush=True)
    return recs

out = {}

# A. 我的原始 fixture：GLM 全协议 5条件×8
model = "THUDM/GLM-4-9B-0414"
tasks = [(f"{c}#{i}", build_prompt(c)) for c in CONDITIONS for i in range(REPS_PER_CONDITION)]
out["A_glm_original_fixture"] = {
    "model": model, "fixture": "contract_core (单残留未知 data_residency)",
    "evaluator": "contract_core.evaluate (7项检查+strict)",
    "records": capture(model, "A", lambda r: (evaluate(r)["strict"][0],
                       {k: v[1] for k, v in evaluate(r).items() if not v[0]}), tasks)}

# B. 用户结构变体：GLM canonical + paraphrase 各8
for cond, prompt in [("canonical", V.PROMPT), ("unknown_state_paraphrase", V.PROMPT_PARAPHRASE)]:
    tasks = [(f"{cond}#{i}", prompt) for i in range(8)]
    out[f"B_glm_variant_{cond}"] = {
        "model": model, "fixture": "variant_user_fixture (双残留未知+诱人第三状态)",
        "evaluator": "residual_unknown_state 精确匹配",
        "records": capture(model, f"B-{cond}", lambda r: V.check(r)[0:1] + (V.check(r)[1],), tasks)}

# C. 变体对照：Qwen3-8B canonical + paraphrase
model2 = "Qwen/Qwen3-8B"
for cond, prompt in [("canonical", V.PROMPT), ("unknown_state_paraphrase", V.PROMPT_PARAPHRASE)]:
    tasks = [(f"{cond}#{i}", prompt) for i in range(8)]
    out[f"C_qwen3_variant_{cond}"] = {
        "model": model2, "fixture": "variant_user_fixture",
        "evaluator": "residual_unknown_state 精确匹配",
        "records": capture(model2, f"C-{cond}", lambda r: V.check(r)[0:1] + (V.check(r)[1],), tasks)}

with open("/tmp/repro/raw_data_full.json", "w") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("saved raw_data_full.json")
