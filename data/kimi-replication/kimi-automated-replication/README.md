# 复现实验原始数据包（README）

**披露声明**：本数据包由 LLM agent（Kimi）自动执行实验产生，应标注为 *automated replication by an LLM agent*，而非 independent human replication。fixture 为 agent 自行设计的简化版，**不等同于论文原版 Stage B fixture**。

## 文件清单

### 核心原始数据
| 文件 | 内容 |
|---|---|
| `raw_data_full.json` | **2026-07-27 全程留痕重跑**：每运行含 task 名、完整输入 prompt、模型原始输出（未截断）、判定结果与失败详情。共四组：A=GLM×原始fixture全协议（40次）；B=GLM×对抗变体（canonical 8 + paraphrase 8）；C=Qwen3-8B×对抗变体（同 16 次） |
| `petfish_real_raws.json` | 2026-07-19 Qwen3-8B 修复后 40 次运行的原始输出（当时未含 GLM 的原始输出——这是当时的留痕缺口，已由 raw_data_full.json 弥补） |
| `records_*.json`（5 个） | 2026-07-19 五模型互换性实验的逐运行判定记录（无原始输出，仅有 pass/fail 与失败原因） |

### 可执行代码（fixture/评估器即在其中）
| 文件 | 内容 |
|---|---|
| `contract_core.py` | 原始 fixture（单残留未知 `data_residency`）、5 种扰动、7 项确定性检查、Wilson 区间、40 次协议运行器。`build_prompt(condition)` 可逐字重建全部输入 prompt |
| `variant_user_fixture.py` | 对抗变体（双残留未知 + "诱人第三状态"），含 canonical/paraphrase 两个 prompt 常量与精确匹配评估器 |
| `floor_probe.py` | 修复后的 8 项能力地板探针（P3 已修） |
| `capture_raws.py` | 本次留痕重跑的执行脚本 |

## 两次 GLM 测试的关键参数

| 参数 | 值 |
|---|---|
| 模型 ID | `THUDM/GLM-4-9B-0414`（SiliconFlow，快照版本不受控） |
| temperature | 0（petfishframework ModelRequest 默认值，随请求发送） |
| 执行框架 | petfishframework v1.1.0，`Agent + ReAct()`，无工具 |
| 并发 | ThreadPoolExecutor，10 workers |
| 日期 | 首次 2026-07-19；留痕重跑 2026-07-27 |

## 结果摘要与重要波动

| 实验 | 7/19 首测 | 7/27 留痕重跑 |
|---|---|---|
| GLM × 原始 fixture 全协议 | 40/40 | **40/40**（一致） |
| GLM × 对抗变体 canonical | 8/8（7/27 首测） | 8/8 |
| GLM × 对抗变体 paraphrase | 0/8（7/27 首测） | **1/8**（有波动） |
| Qwen3-8B × 对抗变体 两条件 | 8/8 + 8/8 | 8/8 + 8/8 |

**GLM 在 paraphrase 下的失败模式三次观察均不同**：①规范名漂移（`current_branch`）；②（用户观察）过度生成第三状态（`permission_to_use_external_model_api`）；③本次——输出结构修饰化（evidence_array 变成带 source/content 的对象数组）。失败模式本身不稳定，但失败**集中在 paraphrase 条件**这一点三次一致。这支持"GLM 在 paraphrase 输入下状态清单纪律不稳"的定性，但具体失败形态不可复现，写作时不应锁定单一失败模式。

## 与你 30/40 结果的差异归因

你的 fixture（双残留 + 语义相邻诱惑项）对 GLM 的压力维度在我的原始 fixture（单残留）中不存在。差异由 fixture 难度解释，非快照漂移（7/27 重跑原始 fixture 仍 40/40）。

## 重跑方式

```bash
pip install "petfishframework[openai]"
export OPENAI_API_KEY=... OPENAI_BASE_URL=https://api.siliconflow.cn/v1
python capture_raws.py        # 完整重跑 A/B/C 三组（约 72 次调用）
```
