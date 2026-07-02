<!-- BEGIN pack: doc-reader-skill -->
# Doc Reader Skill Pack Rules

This pack provides unified document-to-Markdown conversion for reading, review, and extraction.

## Skill Routing (强制)

### Rules

1. When the user wants to **read, extract text from, or convert** a non-Markdown document (PDF, DOCX, XLSX, HTML, EPUB) to Markdown, **MUST** route to `doc-reader`.
2. When the user needs **structured text content** from a document (tables, paragraphs, lists), **MUST** use `doc-reader` to convert first, then read the Markdown output.
3. For **PPTX files**: use `ppt-reader` for structural inventory (slide order, media, comments, layout), use `doc-reader` for full text extraction including tables and charts. Use both for complete PPTX understanding.
4. When the user provides a document and asks to **review, summarize, or extract key points**, use `doc-reader` for conversion, then apply `reference-document-review` for analysis. Do NOT treat conversion as analysis.

### Conflict Resolution

- "Read this PDF and summarize": route `doc-reader` (convert) → agent reads output → summarize. Conversion and analysis are separate steps.
- "Extract the tables from this DOCX": route `doc-reader` with `--json` for metadata, then read the Markdown output.
- "Read this PPTX": route `ppt-reader` first for structure, then `doc-reader` for full text if structural inventory is insufficient.
- "Convert this document to Markdown": route `doc-reader` only. No analysis needed.
- When `reference-document-review` is also installed: `doc-reader` handles conversion, `reference-document-review` handles analysis and extraction into course inputs. Do not merge these responsibilities.

## doc-reader Workflow

1. Identify input file and format (PDF, DOCX, XLSX, HTML, EPUB, etc.)
2. Run conversion:
   ```bash
   uv run scripts/doc_to_markdown.py input.pdf --output output.md
   ```
3. Read the converted Markdown output
4. Optionally extract structured metadata:
   ```bash
   uv run scripts/doc_to_markdown.py input.pdf --output output.md --json metadata.json
   ```

## Behavioral Rules

- Always convert before reading. Do NOT attempt to interpret binary file contents directly.
- Preserve the conversion output as a file when the user needs to review or cite it later. Use `--output` flag.
- For scanned PDFs, warn the user that markitdown does NOT perform OCR by default; text extraction will be minimal.
- For PPTX, always recommend `ppt-reader` for structural analysis first if structure matters (slide order, media inventory, layout issues).
- Do NOT attempt LLM-based image description through this skill. The agent can view images natively.

## Output Format

**doc-reader** outputs:
1. Markdown file — converted text content from the source document
2. (Optional) JSON metadata — `{source_file, source_ext, text_length, title_guess}`
<!-- END pack: doc-reader-skill -->

<!-- BEGIN pack: opencode-ppt-skills -->
# PPT Skills Pack Rules

This pack provides PPTX reading and writing capabilities for course slides, proposals, reports, and technical decks.

## Skill Routing (强制)

### Rules

1. When the user wants to **read, inspect, summarize, audit, or compare** a PPT/PPTX file, **MUST** route to `ppt-reader`. Do NOT route to `ppt-writer`.
2. When the user wants to **create, rewrite, restructure, update, or export** a PPT/PPTX deck, **MUST** route to `ppt-writer`. Do NOT route to `ppt-reader`.
3. When the user provides a Markdown outline, document, meeting notes, or old PPT and asks to generate a new deck, **MUST** route to `ppt-writer`.
4. When the user asks for a "rewrite brief" or "per-slide action plan" as input for a future writing task, **MUST** route to `ppt-reader` (produces the brief), then `ppt-writer` (executes it).
5. When the user asks for visual QA of a generated deck, **MUST** use `ppt-writer`'s `qa_deck.py` step — do NOT treat this as a `ppt-reader` task.

### Conflict Resolution

- "Read and then rewrite" requests: route `ppt-reader` first to produce inventory + rewrite brief, then `ppt-writer` to execute. Do not merge into a single step.
- "Summarize the slides" = `ppt-reader`. "Update the slides" = `ppt-writer`.
- When ambiguous, ask: is the primary output a **report about** the deck (`ppt-reader`) or **a new deck** (`ppt-writer`)?

## ppt-reader Workflow

1. Extract slide inventory → `pptx_inventory.json` (titles, layout, notes, comments, media, links)
2. Produce Markdown summary of structure and content
3. Flag: missing placeholders, sensitive info, broken links, layout inconsistencies
4. Optionally produce a rewrite brief / per-slide action plan for `ppt-writer`

## ppt-writer Workflow

1. Receive input: Markdown / doc / outline / old PPTX / rewrite brief
2. Build narrative structure and page plan
3. Run `build_deck.py` to generate PPTX
4. Run `qa_deck.py` to verify output
5. Fix issues found in QA
6. Re-verify until QA passes
7. Deliver final PPTX

## Behavioral Rules

- Never skip the `qa_deck.py` step after `build_deck.py`. Generate → QA → fix → re-verify is mandatory.
- `ppt-reader` output (inventory JSON + Markdown summary) must be saved before passing to `ppt-writer`.
- Template and style unification must be applied consistently across all slides in a deck.
- Do not mix reading and writing in a single tool invocation.
- LibreOffice and Poppler are optional dependencies for visual QA; if unavailable, note the limitation and proceed with structural QA only.

## Output Format

**ppt-reader** outputs:
1. `pptx_inventory.json` — structured slide inventory
2. Markdown summary — human-readable structure and content overview
3. (Optional) Rewrite brief — per-slide action plan

**ppt-writer** outputs:
1. Generated `.pptx` file
2. QA report — issues found and fixed
3. Delivery summary — slide count, template used, known limitations
<!-- END pack: opencode-ppt-skills -->

<!-- BEGIN pack: opencode-skill-pack-testcases-usage-docs -->
# Test Cases & Usage Docs Skill Pack Rules

This pack provides two complementary skills: generating test cases from real project code, and generating usage documentation from real project capabilities.

## Skill Routing (强制)

### Rules

1. When the user asks to generate **test cases, test strategy, test matrix, or test plan** from a project, **MUST** route to `generate-test-cases`. Do NOT route to `generate-usage-docs`.
2. When the user asks to generate **README, Quick Start, API docs, CLI docs, FAQ, or troubleshooting guides** from a project, **MUST** route to `generate-usage-docs`. Do NOT route to `generate-test-cases`.
3. Both skills require a **project inventory step first**: run `uv run scripts/project_inventory.py .` before generating artifacts. Do not skip this step.
4. When the user asks for both tests and docs in the same request, run `generate-test-cases` and `generate-usage-docs` sequentially (inventory once, then both generation steps). Do not merge them into a single pass.
5. Both skills operate on **real project code and design docs** — do not generate generic/template artifacts without first reading the actual project.

### Conflict Resolution

- "Write tests for this project" = `generate-test-cases`.
- "Document this project" = `generate-usage-docs`.
- "Help me ship this project" (ambiguous) → ask whether the priority is test coverage or user-facing documentation, then route accordingly.
- If the user provides a design doc or spec as input, both skills can use it — but route based on the desired output type (tests vs docs).

## generate-test-cases Workflow

1. Run project inventory: `uv run scripts/project_inventory.py .`
2. Build traceability map: capabilities → test targets
3. Generate layered test artifacts:
   - Test strategy (scope, risk areas, coverage goals)
   - Test matrix (feature × scenario × priority)
   - Test cases (input, expected output, pass/fail criteria)
4. Output to `tests/` or designated output directory

## generate-usage-docs Workflow

1. Run project inventory: `uv run scripts/project_inventory.py .`
2. Identify target audience (end user / developer / operator)
3. Identify project capabilities (CLI, API, config, integrations)
4. Build doc set:
   - README (overview, install, quick start)
   - API / CLI reference
   - FAQ and troubleshooting
5. Output to `docs/` or designated output directory

## Behavioral Rules

- Always run project inventory before generating any artifact. Do not generate from assumptions.
- Test cases must be traceable to specific project capabilities identified in the inventory.
- Usage docs must reflect actual project behavior, not generic boilerplate.
- If the project inventory reveals missing or ambiguous capabilities, flag them before generating — do not silently fill gaps with invented behavior.
- Generated test cases must include: input, expected output, and pass/fail criteria. Vague test descriptions are not acceptable.
- Generated docs must include: at least one working example per capability documented.

## Output Format

**generate-test-cases** outputs:
1. Test strategy document — scope, risk areas, coverage goals
2. Test matrix — feature × scenario × priority table
3. Test case files — structured cases with input/output/criteria

**generate-usage-docs** outputs:
1. README — overview, install, quick start
2. Reference docs — API / CLI / config
3. FAQ / Troubleshooting — common issues and resolutions
<!-- END pack: opencode-skill-pack-testcases-usage-docs -->

<!-- BEGIN pack: trustskills-governance-pack -->
# Trust Skills Governance Pack Rules

This pack provides skill trust scanning, governance level assignment, and manifest generation/verification for PEtFiSh skill packs.

## Skill Routing (强制)

### Rules

1. When the user asks to **scan skills for trust, safety, or governance issues**, **MUST** route to `skill-trust-governance`.
2. When the user asks to **generate or verify a trust manifest** for a skill or pack, **MUST** route to `skill-trust-governance`.
3. When the user asks to **assign or review governance levels** (allow / allow_with_ask / sandbox_required / manual_review_required / deny) for skills, **MUST** route to `skill-trust-governance`.
4. When the user asks to **redline** a skill (flag it as requiring manual review or denial), **MUST** route to `skill-trust-governance`.
5. The entrypoint for all trust operations is: `uv run .opencode/skills/skill-trust-governance/scripts/trust_scan.py`. Do not invoke `trustskills` CLI directly without going through this entrypoint.

### Conflict Resolution

- Trust governance vs security audit: `skill-trust-governance` handles **governance classification and manifest management** (what level of trust to grant a skill). `skill-security-auditor` handles **vulnerability and risk scanning** (what security risks a skill poses). They are complementary — run security audit first, then use findings to inform governance level assignment.
- When the user asks to "check if a skill is safe to install", route to `skill-security-auditor` for risk findings, then `skill-trust-governance` for governance decision.
- When the user asks to "publish a skill", the governance manifest must be generated by `skill-trust-governance` before the `quality-gate` publish flow.

## Governance Levels

| Level | Meaning | Agent Behavior |
|---|---|---|
| `allow` | Trusted, no restrictions | Execute without prompting |
| `allow_with_ask` | Trusted but requires confirmation for sensitive actions | Prompt user before sensitive operations |
| `sandbox_required` | Must run in isolated environment | Do not execute outside sandbox |
| `manual_review_required` | Flagged for human review before use | Block execution, notify user |
| `deny` | Rejected, must not be used | Refuse to load or execute |

## trust_scan.py Modes

- **scan**: Analyze a skill directory and produce a trust report
- **manifest**: Generate a signed trust manifest for a skill
- **verify**: Verify an existing trust manifest against current skill content
- **redline**: Flag a skill at `manual_review_required` or `deny` level

## Behavioral Rules

- Never assign `allow` governance level without completing a full scan. Partial scans must result in `manual_review_required` at minimum.
- Trust manifests must be regenerated whenever skill content changes. Stale manifests are treated as `manual_review_required`.
- `deny`-level skills must not be loaded, executed, or referenced in routing rules.
- When a scan finds issues, report them with the specific governance level recommendation and the reason. Do not silently downgrade to `allow`.
- Governance decisions must be logged with: skill path, scan timestamp, findings summary, assigned level, and agent ID.

## Output Format

**scan** output:
1. Trust report — findings per skill file, risk signals detected
2. Recommended governance level with justification

**manifest** output:
1. Signed trust manifest file (saved alongside skill)
2. Manifest summary — skill path, level, timestamp, hash

**verify** output:
1. Verification result: PASS / FAIL / STALE
2. If FAIL or STALE: diff of what changed and recommended action

**redline** output:
1. Updated governance level in manifest
2. Redline reason and required remediation steps before level can be upgraded
<!-- END pack: trustskills-governance-pack -->

<!-- BEGIN pack: fish-trail -->
# Fish Trail — 话题治理器

本pack为项目提供上下文治理能力，降低跨话题污染风险。

## Skill路由（强制）

### 必须遵守的路由规则

1. 涉及话题管理、上下文治理、污染检测、话题切换类任务时，**必须**路由到 `fish-trail` skill
2. 用户说"整理话题"、"切换到X"、"合并话题"、"topic管理"时，**必须**加载fish-trail执行深度治理
3. 当system prompt中注入的topic context显示high-risk话题切换时，**必须**暂停正常处理，向用户说明风险并建议fork/switch/reset
4. 对merge、archive、bridge三种关系类型，检测置信度低时**必须**提示用户确认，**不得**自动执行

### 冲突解决

- 当话题治理与正常任务并行时，话题治理优先级更高——先处理上下文风险，再执行任务
- 当MCP不可用时，不阻塞正常工作，静默降级

## Topic Context: Plugin Injection（非MCP工具调用）

### 机制

Topic context由 `system-prompt-context-inject` 插件自动注入到system prompt的cached prefix中。**你无需也不应在每轮交互中调用 `topic_detect` 或 `get_memory_context`**——插件已处理。

### 3-Block注入结构（#164+#166+#167）

插件输出3个独立block，每个block有不同的变更频率：

| Block | 内容 | 变更频率 | 用途 |
|-------|------|---------|------|
| `## Topics` | 话题ID、标题、状态列表 | 每100轮 | 稳定注册表 |
| `## Related` | 相关话题一行摘要 + 关系 | 每20轮 | 温话题提醒 |
| `## Focus` | 当前话题 + 反射摘要 + 模式标记 | 每轮 | 活跃焦点 |

### 模式标记（Mode Indicator）

Focus block末尾的方括号标记控制MCP调用行为：

```
[disk|rMCP:off|detail:topic_show]
```

| 标记 | 含义 | 行为 |
|------|------|------|
| `disk` | 当前运行在disk模式 | 话题感知由插件注入，非MCP实时检测 |
| `rMCP:off` | 例行MCP调用已抑制 | **禁止**自动调用topic_detect、get_memory_context、topic_list等 |
| `detail:topic_show` | 冷数据按需获取工具 | 需要完整话题详情（scope、summary、tags、edges）时使用topic_show |

### #165: MCP调用条件化规则

根据模式标记决定MCP调用策略：

**禁止的例行调用（rMCP:off时）：**
- ❌ `topic_detect` — 插件已处理，每轮无需调用
- ❌ `get_memory_context` — 插件已注入，每轮无需调用
- ❌ `topic_list` — 插件已注入 `## Topics` block
- ❌ `topic_graph` — 插件已注入 `## Related` block

**允许的按需调用：**
- ✅ `topic_show` — 需要完整话题详情时（冷数据）
- ✅ `topic_create` — 用户发起新话题
- ✅ `topic_update` — 交互后更新话题摘要/状态
- ✅ `topic_link`/`topic_unlink` — 用户发起话题关系操作
- ✅ `topic_archive` — 用户发起归档
- ✅ `session_bind`/`session_list`/`session_resume` — 会话管理

**禁止 → 允许的升级条件：**
- 用户明确发起话题管理操作
- Focus block显示high-risk切换信号
- Agent需要理解另一个话题的完整上下文（使用topic_show）

### 根据注入的context采取行动

| 话题状态 | 行为 |
|---------|------|
| 当前话题继续（无切换信号） | 静默继续 |
| 检测到话题切换 | 回复开头一行说明上下文变更 |
| 检测到high-risk切换（跨领域大幅切换） | 向用户说明话题变更风险，建议fork/switch/reset |
| Focus block包含RESET | 上下文已清除，开始新话题 |

### 何时使用MCP工具

MCP工具**仅限**用户主动发起的话题管理操作和冷数据按需获取：

| 场景 | 使用MCP工具 | 原因 |
|------|-----------|------|
| 例行话题感知 | ❌ 不使用 | 插件已注入3个block |
| 例行记忆上下文 | ❌ 不使用 | 插件已注入Focus+Related |
| 查看话题列表 | ❌ 不使用 | 插件已注入Topics block |
| 需要完整话题详情 | ✅ 调用topic_show | 冷数据，按需获取 |
| 用户问"有哪些话题" | ✅ 调用topic_list | 用户触发，需返回完整列表 |
| 用户要求切换/分叉/合并话题 | ✅ 调用对应MCP工具 | 状态变更，需事务保证 |
| 用户要求创建新话题 | ✅ 调用topic_create | 状态变更 |

### One-turn延迟

插件从磁盘读取上一轮的状态。首次对话（冷启动）时无注入，第二轮起才有完整的topic context。质量评估（N=18）显示此延迟不影响使用。

### 交互后更新

当本次交互产生实质性成果（代码变更、文档输出、决策结论等）时，调用`topic_update`更新当前topic的summary和status。

### 交互后Reflective Brief

当本次交互产生实质性成果时，调用topic_update并附带reflective_brief：
- brief ≤200字符（≈40-80 tokens），必须包含：当前阶段 + 核心动作/决策
- 示例："v1.2 design complete, 2 proposals drafted"
- 示例："#169 console.log→stderr fix committed, pre-release updated"
- 不要写："继续开发中"（无信息量，会被MCP server拒绝）
- 不要写：完整长句（太浪费tokens）
- MCP server会校验brief质量（10-200字符，无低质量模式），无效brief会被拒绝并用启发式替代
- 连续3次提交无效brief会触发自动降级，后续不再接受agent brief

### 会话管理

fish-trail支持会话级追踪。会话（session）绑定外部平台的session ID或自动推断创建。

- **会话绑定**：在会话开始时调用`session_bind`绑定外部session_id和当前topic
- **事件追踪**：用户发起话题管理操作时，自动记录到session timeline
- **会话查询**：通过`session_list`按topic、时间、状态过滤，回答"昨天我们做了什么？"
- **会话恢复**：通过`session_resume`查找与特定topic关联的最近session，支持跨会话上下文继承

会话数据存储在`.petfish/fish-trail/sessions/`，与topic数据独立管理。

### 话题关系类型

检测到的关系类型决定上下文处理策略：

- **continue**：完全继承当前上下文
- **fork**：从当前topic分叉，继承部分上下文，创建子topic
- **switch**：切换到已有topic，加载该topic的Context Package
- **merge**：合并两个topic（需用户确认）
- **archive**：归档当前topic，冻结上下文
- **reset**：清空上下文，建立干净包
- **bridge**：两个topic间建立桥接，只继承交叉部分（需用户确认）

对merge、archive、bridge三种类型，检测置信度较低时必须提示用户确认，不得自动执行。

### 会话边界自动管理

fish-trail自动管理会话边界：

- 用户发起archive或reset操作时，自动关闭关联session
- `session_bind`时自动清理不活跃超过24小时的session
- 使用`session_close`显式关闭session并附带summary
- `session_resume`返回resume context（session summary + timeline digest），支持跨会话上下文继承
- 新增`session_timeline`查看session时间线摘要
- 使用`session_query`按时间范围、topic、agent查询活动（回答"昨天我们做了什么？"）
- 使用`session_agents`查看agent-topic归属关系（哪个agent处理了哪个topic）
- 使用`topic_recommend`从topic图谱推荐关联topic

### MCP不可用时的降级行为

当context-state MCP server未启动、连接失败或调用超时时：

- 不报错，不阻塞正常工作
- 插件注入的topic context仍然可用（来自磁盘缓存）
- 仅MCP工具调用不可用（用户主动的话题管理操作受影响）
- 每次会话最多提示一次"⚠ fish-trail MCP未连接"

## 深度治理触发条件

以下情况自动加载`.opencode/skills/fish-trail/SKILL.md`执行完整5步工作流：

- 插件注入的topic context显示high-risk话题切换
- 用户主动要求话题管理（"整理一下话题"、"切换到X"、"把这两个话题合并"等）
- 用户使用fish-trail相关关键词（topic、话题、上下文、污染、继承、隔离等）
<!-- END pack: fish-trail -->

<!-- BEGIN pack: petfish-companion-skill -->
# PEtFiSh Companion Rules

本项目已安装胖鱼PEtFiSh伙伴skill。

## Skill路由（强制）

### 必须遵守的路由规则

1. 用户说"/petfish"或任何petfish子命令时，**必须**路由到 `fish-brain` skill处理
2. 用户需要创建新skill时，**必须**使用 `skill-author`；需要验证skill质量时，**必须**使用 `skill-lint`
3. 用户需要搜索外部skill或MCP server时，**必须**使用 `fish-market`
4. 用户需要发布skill时，**必须**使用 `quality-gate` 运行完整发布门禁（lint+security→决策）
5. 用户需要从仓库挖掘skill候选时，**必须**使用 `repo-skill-miner`
6. 用户需要安全审计skill时，**必须**使用 `skill-security-auditor`
7. 用户需要发布pack到市场时，**必须**使用 `skill-publish`（在 `quality-gate` PASS 之后）

### Pack分类（v1.4）

- **Core packs** (4): companion, toolchain, init, context — 直接从 petfish.ai 安装，不可发布到市场
- **Optional packs** (9): research, course, deploy, ppt, testdocs, petfish, calibrate, trust, reflect — 通过 petfish-market 发布和分发

Optional pack 的安装路由经过 petfish-market index.json；用户无需关心内部路由差异。

### 冲突解决

- 当用户同时涉及skill创建和质量检查时，先创建（`skill-author`），后检查（`skill-lint` → `quality-gate`）
- 当用户请求"搜索skill"时，区分：搜索外部市场用 `fish-market`，搜索已安装skill用 `fish-brain`

## 感知规则

在对话过程中，如果用户的需求涉及以下领域，但对应skill pack尚未安装，应主动提示：

| 领域 | 对应Pack | 安装命令 |
|------|---------|---------|
| 部署/运维/Docker | deploy | `/petfish install deploy` |
| 课程/教学/大纲 | course | `/petfish install course` |
| PPT/幻灯片 | ppt | `/petfish install ppt` |
| 测试用例/文档 | testdocs | `/petfish install testdocs` |
| 写作风格/润色 | petfish | `/petfish install petfish` |
| 评审/评价/批判/校准/反迎合 | calibrate | `/petfish install calibrate` |
| 话题治理/上下文污染/topic管理 | context | `/petfish install context` |
| 研究/调研/文献/证据/综述 | research | `/petfish install research` |

当用户需要创建新skill、搜索外部skill、或验证skill质量时，使用companion内置的skill-author、fish-market、skill-lint。

每次会话对同一pack最多主动推荐1次。

### 能力缺口自动检测（Tier 2：未知领域）

当上面的Tier 1白名单未命中时，判断用户消息是否暗示了一个**当前环境无法满足的能力需求**。

**触发条件 — 必须同时满足全部：**

1. 用户的请求涉及一个具体的活动、场景或任务（而非泛泛闲聊）
2. 该任务超出了agent内置能力（代码、文件、git、搜索、通用推理）
3. 当前已安装的skill也无法覆盖（检查已安装skill列表）

**排除条件（不触发）：**
- 普通编码、项目管理、git操作、文件整理
- 通用问答（解释概念、分析代码、给建议）
- 对话管理（"继续"、"停"、"换个方向"）
- 已安装skill明确覆盖的领域

**触发时行为：**
1. 推断用户需求最相关的英文关键词
2. 主动运行 fish-market（即 /petfish search <关键词>）搜索跨市场skill和MCP server
3. 根据搜索结果：
   - **找到匹配skill** → 推荐安装并提供命令
   - **找到相似但不完全匹配** → 展示结果，建议参考这些skill用 skill-author 手动创建
   - **完全找不到** → 建议用 repo-skill-miner 从相关GitHub仓库挖掘，或用 skill-author 从零创建

**示例：**
- "我想参加吐槽大会" → 触发 → 搜索 "roast comedy event planning"
- "帮我发个邮件通知团队" → 触发 → 搜索 "email notification"
- "帮我画一个甘特图" → 触发 → 搜索 "gantt chart"
- "帮我查一下这个API的rate limit" → 不触发（agent原生能力）

**行为约束：**
- 每次会话对同一类缺口最多提示1次
- 不自动安装，只推荐和展示搜索结果
- 用户拒绝后不再重复

## 可用命令

- `/petfish` — 查看当前skill状态
- `/petfish catalog` — 浏览全量技能目录
- `/petfish search <keyword>` — 跨市场搜索skill和MCP server
- `/petfish suggest` — 基于项目特征推荐skill
- `/petfish install <alias>` — 获取安装命令
- `/petfish detect` — 检测当前平台
- `/petfish create <name>` — 创建新skill
- `/petfish lint [path]` — 验证skill质量
- `/petfish mine <repo>` — 从仓库挖掘候选skill
- `/petfish audit <path>` — skill安全审计
- `/petfish gate <path>` — 运行发布门禁（lint+security→决策）
- `/petfish optimize <path>` — 分析并优化skill描述
- `/petfish eval <path>` — 测试skill触发准确率
- `/petfish stats` — 查看skill使用统计
- `/petfish upgrade` — 显示升级命令
- `/petfish uninstall <alias>` — 显示卸载命令（需本地安装器）

## 行为边界

- 不自动安装skill，只推荐并提供命令
- 不修改用户项目文件
- 用户拒绝后本次会话不再重复推荐

## 实施纪律（最小代码原则）

以下两条原则在实施任何任务时强制执行，适用于所有agent工作，不限于PEtFiSh开发。

### 原则一：先读后写

阅读、查找、改写内容或代码时，优先通过**阅读**发现关键点并直接修改，而非写脚本/代码/shell命令来查找或替换。

### 原则二：代码最小化六问

必须使用shell命令、脚本或代码时（已有定稿的设计方案除外），先依次回答以下问题，从上到下满足即停：

0. **既有skills能做到么？** 能→按skills做。
1. **一定需要这个脚本么？** 没有能不能做？能→不写脚本/代码/命令。
2. **标准库能实现么？** 能→用标准库。
3. **平台原生能做到么？** 能→原生。
4. **现成依赖能做到么？** 能→复用。
5. **一行能做到么？** 能→一行命令。
6. **写最少量的代码完成任务。**

## 契约驱动行为（Contract-Driven Behavior）

胖鱼Gateway的每一步都是机制原子（Mechanism Atom），有显式契约、测试用例和验证器。当Gateway行为异常时：

1. 读对应atom的 `contracts/step*.contract.json`，定位 `output_contract.blocked_outputs`
2. 运行 `validators/test_*.py` 验证当前行为
3. 如验证失败，按 `repair_strategy.on_violation` 执行修复循环（max 1 iteration）
4. 修复后添加known-bad fixture，确保回归覆盖

契约文件位于skill目录下的 `contracts/`、`fixtures/`、`validators/`。详见 `references/contract-methodology.md`。

### 阅读笔记（Reading-Notes）

遵循"先读后写"纪律，agent阅读文件时记录理解到 `.petfish/notes/reading-notes.jsonl`。后续session先检索笔记，避免重复阅读。格式：`note_id`/`file_path`/`file_type`/`summary`/`dependencies`/`confidence`。验证：`uv run reading_notes_lint.py --input .petfish/notes/reading-notes.jsonl`。

### Gateway Trace（可观测性，始终输出）

每轮回复最开头输出一行结构化trace，让用户确认Gateway各步确实执行：

```
🐟 [trace] step0=balanced/false | step1=continue/low | step1.5=- | step2=- | step2.5=non-eval | step2.6=notes:0/3 | violations=0
```

`step2.6=notes:hit/total` 显示阅读笔记命中情况。同时追加JSON到 `.petfish/gateway-trace.jsonl`。验证命令：
```bash
uv run <skills_dir>/fish-brain/validators/verify_trace.py --last 10
```

### 阅读笔记staleness检测

读文件前先grep笔记 + stat文件比对mtime/size。文件变更则重读更新，未变更则用summary跳过。详见SKILL.md Section 10.3。
<!-- END pack: petfish-companion-skill -->

<!-- BEGIN pack: petfish-toolchain-skill -->
# PEtFiSh Toolchain Rules

本pack提供Skill生命周期管理工具链。

## Skill路由
- 用户说"create a skill"、"new skill"、"write a skill" → skill-author
- 用户说"lint skill"、"check skill"、"validate skill" → skill-lint
- 用户说"audit skill security"、"security review" → skill-security-auditor
- 用户说"publish skill"、"quality gate"、"run gate" → quality-gate
- 用户说"publish skill"、"发布到市场"、"release to market"、"publish pack" → skill-publish
- 用户说"optimize description"、"improve trigger" → skill-description-optimizer
- 用户说"evaluate triggers"、"test trigger" → skill-trigger-evaluator
- 用户说"mine skills from repo"、"analyze repo" → repo-skill-miner
- 用户说"usage stats"、"track usage" → skill-usage-tracker
<!-- END pack: petfish-toolchain-skill -->

<!-- BEGIN pack: anti-sycophancy-calibration-pack -->
# Anti-Sycophancy Calibration Pack

本pack提供一个用于反迎合决策校准的prompt skill，帮助Agent在评审、方案设计、代码审查、写作反馈等判断型任务中减少顺着用户说的倾向。

## Skill路由（强制）

### 必须遵守的路由规则

1. 涉及评审、评价、批判、review、critique、feedback、judgment类任务时，**必须**加载 `anti-sycophancy-calibration` skill
2. 用户在问确认性问题（"对吗？/right?/是不是?/你同意吗?"）时，**必须**先中性化问题再给结论，不得直接顺着用户预设表态
3. 涉及方案评估、可行性分析、code review、架构判断时，**必须**先给评分维度再做判断
4. 简单事实查询、翻译、排版、机械编辑**不得**启用本skill，除非用户明确要求judgment或critique

### 冲突解决

- 当评审意图与写作润色意图并存时（如"帮我润色并评审这段话"），同时加载 `petfish-style-rewriter` 和 `anti-sycophancy-calibration`
- 当用户请求"帮我review"但上下文是简单校对时，按校对处理，不启用本skill

## 何时启用

- 用户要求评审、评价、批判、review、critique、feedback、judgment、decision、evaluation、calibration
- 用户在问"对吗？/right?/是不是?/你同意吗?/is this correct?"这类确认性问题
- 用户需要方案评估、可行性分析、code review、架构判断、论文或提案反馈

## 行为规则

- 先中性化问题，再给结论；不要直接顺着用户预设表态
- 先给评分维度，再做判断；至少补一个反方或替代方案
- 结论与置信度必须分开表达；证据不足时要明确降级
- 不把skill用成“杠精模式”；该同意时同意，该保留时保留，该反对时反对
- 简单事实查询、翻译、排版、机械编辑默认不启用，除非用户明确要求 judgment或critique

## 组合示例

- `course-outline-design + anti-sycophancy-calibration`：避免课程大纲只顺着最初设想扩写
- `code-review + anti-sycophancy-calibration`：避免审查只给礼貌性正反馈
- `petfish-style-rewriter + anti-sycophancy-calibration`：在润色同时指出论证漏洞和边界条件
- `strategy-writer + anti-sycophancy-calibration`：把支持理由、反对理由、替代路线拆开表达
<!-- END pack: anti-sycophancy-calibration-pack -->

<!-- BEGIN pack: fish-reflection-pack -->
# Fish Reflection Pack

本pack提供结构化反思与经验沉淀能力，帮助Agent将一次性修正转化为可复用的预防规则和项目知识资产。

## Skill路由（强制）

### 必须遵守的路由规则

1. 用户说"反思"、"reflect"、"what went wrong"、"lessons learned"、"复盘"时，**必须**路由到 `fish-reflection` skill
2. 检测到用户纠正/返工信号（用户指出错误并要求修正）时，**必须**在修正后触发L1即时反思
3. 检测到连续失败（同一操作2+次失败）时，**必须**暂停并触发L1即时反思，分析失败模式再继续
4. 任务完成后用户要求复盘时，**必须**触发L2任务复盘
5. 反思产出的prevention_rule具有普遍性时，**应当**建议沉淀到AGENTS.md `开发经验沉淀` section

### 冲突解决

- 反思不阻塞任务执行：L1在修正后内联输出，不打断工作流
- 反思不替代调试：反思关注"为什么会犯这个错"，调试关注"怎么修这个bug"
- 简单任务不触发：单文件typo修复、格式调整、直接回答问题等不启用反思

## 何时启用

- 用户指出Agent的输出有误并要求修正（用户纠正信号）
- 同一操作连续失败2次以上（重复失败信号）
- 用户显式请求反思或复盘（"reflect"、"反思"、"what went wrong"、"复盘"、"lessons learned"）
- 用户要求将经验写成规则或指导文件（L3触发）

## 何时不启用

- 正常的首次尝试和调试过程
- 简单事实查询、翻译、排版、格式修正
- 用户自己改变需求（不是纠正错误，是需求变更）
- 外部因素导致的失败（网络超时、服务不可用）

## 行为规则

- 反思必须产出具体的prevention_rule，不允许"下次更仔细"这类空洞建议
- 反思卡片限4个字段（trigger, root_cause, prevention_rule, scope），不允许膨胀
- L1内联在修正后3-5行内完成，不允许写长篇分析
- L2在任务结束后输出，包含完整的失败-修正-教训链
- L3仅在发现跨任务通用模式时触发，输出为独立guidance文件
- 反思不暴露内部推理链给用户，只输出结构化结论
<!-- END pack: fish-reflection-pack -->

<!-- BEGIN pack: opencode-course-skills-pack -->
# 课程开发项目AGENTS.md

本项目使用OpenCode进行课程开发、课程治理与课程交付。

本文件定义的是**项目级全局规则**。它不替代 `.opencode/skills/*/SKILL.md`，而是为所有技能和后续代理会话提供统一边界、默认流程、目录规范、质量门禁与交付要求。

---

## 1. 项目目标

本项目面向课程产品的全生命周期工作，包括但不限于：

-课程规划与项目治理
-课程提纲设计与模块拆分
-课程正文编写与重构
-实验、演示与作业设计
-学员资料与教师资料制作
-参考文档阅读与提炼
-质量保证、质量控制与发布决策
-课程方法论与复用技能沉淀

本项目的核心目标不是“尽快写出很多文档”，而是形成：

1. 结构清晰、可追踪的课程项目资产
2. 面向交付的课程内容，而非零散草稿
3. 可复用的方法论、模板、审阅标准与skills
4. 清晰区分学员版、教师版、QA/QC版和正式发布版

---

## 2. 优先级与判断原则

处理任何任务时，默认遵循以下优先级：

1. **项目边界优先**：先判断任务属于项目治理、提纲、正文、实验、资料、QA、QC还是发布。
2. **结构一致性优先**：先保持目录、命名、版本与资料边界清晰，再追求局部文字优化。
3. **提纲先于正文**：涉及大范围内容调整时，先更新或确认提纲，再批量改正文。
4. **QA先于QC**：先做问题发现与审阅，再做闭环判定与发布建议。
5. **正式交付与参考资料分离**：`references/` 不是交付物，`release/` 才是稳定对外交付物。
6. **学员资料与教师资料严格分离**：避免答案、讲师提示、内部批注泄露到学员材料。
7. **保留可追踪性**：重大调整必须留下计划、变更记录、审阅记录或QC结论。

---

## 3. 项目资料分层

本项目默认采用以下目录语义。若实际目录存在偏差，应优先向此规范收敛。

### 3.1核心目录

- `docs/00-project/`：项目治理材料
- `docs/01-outline/`：课程顶层提纲、模块图、课时分配
- `docs/02-content/`：课程正文
- `docs/03-labs/`：实验、演示、作业与环境说明
- `docs/04-learner-pack/`：学员资料
- `docs/05-instructor-pack/`：教师资料
- `docs/06-qa/`：质量保证过程材料
- `docs/07-qc/`：质量控制结论与发布建议
- `assets/`：图片、drawio、表格、静态资源
- `references/`：外部与内部参考资料
- `release/`：阶段性交付与正式发布版本
- `archive/`：归档与废弃内容

### 3.2目录语义要求

- `docs/00-project/` 不放课程正文。
- `docs/01-outline/` 不放完整讲稿。
- `docs/02-content/` 不混入QA批注或发布决策。
- `docs/03-labs/` 中的学员手册与教师答案必须分离。
- `docs/04-learner-pack/` 中不能出现内部审阅痕迹、答案、讲师提示。
- `docs/05-instructor-pack/` 可以包含讲解提示、答案索引、课堂风险提示。
- `docs/06-qa/` 强调“发现问题、记录问题、分类问题”。
- `docs/07-qc/` 强调“问题是否关闭、是否允许发布、是否降级发布”。
- `references/` 中的材料不得直接视为正式课程内容；必须经过提炼、重写或适配后再进入 `docs/`。
- `release/` 中只放稳定版本，不放临时草稿。

详细目录规范见：`COURSE-PROJECT-STRUCTURE-STANDARD.md`

---

## 4. 命名与文件规则

### 4.1命名规则

默认使用以下规则：

-目录与文件名优先使用小写 `kebab-case`
-有顺序的内容使用两位数字前缀
-一个文件只承载一个主主题
-尽量避免 `final`、`new`、`new2`、`最新版` 这类无信息量命名
- QA/QC文件建议显式带轮次或日期

推荐示例：

- `docs/01-outline/course-overview.md`
- `docs/02-content/01-module-01/01-lesson-01.md`
- `docs/03-labs/01-lab-01/learner-guide.md`
- `docs/05-instructor-pack/instructor-guide.md`
- `docs/06-qa/qa-review-round-01.md`
- `docs/07-qc/qc-report-2026-04-16.md`

### 4.2文件内容规则

- Markdown优先作为中间工作格式与审阅格式。
-对PDF、DOCX、图片、网页等参考材料的提炼结果，应沉淀为Markdown审阅记录或课程正文，而不是长期停留在“看过了”的状态。
-课程正文中不要残留“待补充”“后面再写”“这里可能有问题”这类内部工作痕迹；这类内容应留在QA/QC文件中。
-表格、图示、课程图、实验拓扑尽量把原始编辑文件保存在 `assets/` 下可维护的位置，而不是只保留导出图片。

---

## 5. 技能使用原则

本项目优先通过skills组织工作，而不是每次从零开始描述流程。

### 5.1默认技能路由

-涉及项目统筹、任务分流、跨多个环节的复杂任务：`course-development-orchestrator`
-涉及目录初始化、结构审计、文件归位、命名规范：`course-directory-structure`
-涉及Markdown风格、模板、课程正文排版：`markdown-course-writing`
-涉及drawio、结构图、流程图、课程架构图：`drawio-course-diagrams`
-涉及PDF、Markdown、DOC/DOCX、图片等参考资料研读：`reference-document-review`
-涉及里程碑、计划、变更、风险、实施路线：`development-plan-governance`
-涉及课程总纲、模块划分、课时分配：`course-outline-design`
-涉及课程内容展开、章节重写、案例补强：`course-content-authoring`
-涉及实验目标、实验步骤、环境说明、验收标准：`course-lab-design`
-涉及学员讲义、手册、复习资料：`learner-materials`
-涉及教师讲义、答题参考、讲解节奏与授课提醒：`instructor-reference-materials`
-涉及问题发现、审阅清单、严重性分类：`course-quality-assurance`
-涉及整改闭环、发布建议、质量控制报告：`course-quality-control-reporting`
-涉及可沉淀的方法、模板、技能化路线：`course-methodology-playbook`
-涉及从公共仓库或参考资料中发现skill范式：`skill-reference-discovery`

### 5.2使用顺序

默认顺序如下：

1. 先由 `course-development-orchestrator` 判断任务所在阶段
2. 再由专项skill执行具体工作
3. 涉及发布前检查时，必须经过QA与QC两步
4. 涉及目录或大规模整理时，优先用 `course-directory-structure` 做初始化或审计

### 5.3 Commands与Agents

本项目除了skills以外，还可以通过 `.opencode/commands/` 与 `.opencode/agents/` 提高执行效率。

- `commands` 用于高频工作流入口，例如项目初始化、结构审计、提纲生成、QA/QC审阅
- `agents` 用于角色化分工，例如目录治理、提纲设计、正文编写、实验设计、QA、QC

推荐做法：

-直接执行高频工作流时，优先使用 `/course-init`、`/course-audit`、`/course-outline`、`/course-qa`、`/course-qc` 等命令
-需要明确角色分工时，优先使用 `curriculum-build`、`outline-architect`、`content-crafter`、`lab-designer`、`qa-auditor`、`qc-gatekeeper` 等代理
- commands与agents都不替代skills；它们应建立在skills和本 `AGENTS.md` 的规则之上
---

## 6. 默认工作流

### 6.1新项目初始化

新课程项目默认按以下顺序推进：

1. 明确项目目标、对象、范围、交付物
2. 建立标准目录结构
3. 写 `docs/00-project/project-brief.md`
4. 写 `docs/00-project/milestone-plan.md`
5. 写 `docs/01-outline/` 下的总纲、模块图、课时分配
6. 再开始课程正文、实验、学员资料与教师资料
7. 完成后进入QA
8. QA闭环后生成QC报告
9. 满足发布条件后形成 `release/` 版本

### 6.2现有项目接管

若接手的是已有项目，默认按以下顺序：

1. 先做结构审计，而不是直接新建文件覆盖原有资产
2. 判断当前材料分别属于project/outline/content/labs/learner/instructor/qa/qc/release/archive哪一层
3. 形成整理建议
4. 再做目录归位、拆分、重命名
5. 补齐缺失层级
6. 再启动内容增补或重写

### 6.3大范围修改

以下情况视为大范围修改，必须先有计划或提纲更新：

-调整课程总体目标、对象、定位
-大规模改变模块划分或课时分配
-重构多个章节
-增加或删除整块实验内容
-学员版和教师版重新分层
-发布目标、交付边界、验收口径发生变化

遇到上述情况，应先更新：

- `docs/00-project/change-log.md`
-必要时更新 `milestone-plan.md`
-必要时更新 `docs/01-outline/` 中的相关文件

---

## 7. 审阅与修改规则

### 7.1可以直接修改的情况

以下情况可以直接处理：

-纯排版与格式统一
-明显错字、病句、标题层级问题
-明确归属且不会引起歧义的文件归位
-不改变对外语义的轻量补充说明

### 7.2先出建议再修改的情况

以下情况应先给出方案、影响面或整理建议：

-大规模重命名
-跨目录搬迁文件
-合并或拆分多个章节
-学员版与教师版的内容边界调整
-把参考资料改写为正式课程内容
-删除疑似仍在使用的文件
-调整实验验收口径或评分标准

### 7.3保守处理原则

-不确定归属时，先产出整理建议，不贸然移动。
-不确定是否已发布时，不直接覆盖 `release/`。
-不确定是否仍被引用时，不直接删除旧文件。
-不确定是草稿还是准正式版时，先保留并标记，再整理。

---

## 8. 质量门禁

本项目采用分阶段质量门禁。没有通过前一门禁，不建议跳过直接发布。

### 8.1项目门禁

至少应具备：

-明确的项目目标
-明确的交付物边界
-基本里程碑或阶段计划
-变更记录入口

### 8.2提纲门禁

至少应具备：

-课程对象与先修要求
-模块划分
-课时分配
-课程目标与实验目标映射
-学员收益表述

### 8.3内容门禁

至少应具备：

-正文章节结构稳定
-概念定义一致
-章节之间不明显重复或冲突
-图表、案例、示例与正文对应
-没有明显内部批注残留

### 8.4实验门禁

至少应具备：

-实验目标
-环境说明
-操作步骤
-验收标准
-常见失败点或教师提示
-学员版与答案版分离

### 8.5资料包门禁

-学员包不得泄露教师提示、答案、内部审阅内容
-教师包应包含讲解提示、答案索引、时间控制建议与风险提示
-资料包中的链接、图片、引用文件应可解析

### 8.6 QA门禁

QA至少要回答：

-发现了哪些问题
-问题属于哪一类
-严重性如何
-哪些问题必须在发布前关闭

### 8.7 QC门禁

QC至少要回答：

-哪些问题已关闭
-哪些问题接受风险并延期处理
-当前版本是否允许发布
-若允许发布，是正式发布、受限发布还是内部试运行

---

## 9. 发布规则

### 9.1何时进入 `release/`

只有在下列条件满足后，才应形成或更新 `release/` 内容：

-已完成至少一轮QA
-已形成QC结论
-交付边界明确
-学员版与教师版材料边界明确
-对外材料不含明显内部痕迹

### 9.2发布目录要求

发布版本建议带版本号或日期，例如：

- `release/v0.1/`
- `release/v1.0/`
- `release/2026-04-internal-preview/`

### 9.3不应发布的内容

以下内容不应直接进入发布版本：

-仅供内部审阅的QA记录
-未脱敏的教师答案
-未整理的参考资料原件
-仍处于争议中的章节草稿
-仅为占位而存在的空文件

---

## 10. 参考资料处理规则

### 10.1参考资料不是最终交付

参考资料可来自：

- PDF
- Markdown
- DOC/DOCX
-图片
-网页
-历史对话整理稿
-外部高星skill仓库

但这些材料只能作为输入，不直接等于课程交付物。

### 10.2提炼要求

对参考资料的处理，默认要求至少输出以下一种成果：

-审阅摘要
-差距分析
-课程提纲修订建议
-内容重写建议
-实验设计输入
- QA问题单
-可沉淀为skill的流程、模板或gotchas

### 10.3外部skill参考规则

可以参考外部高质量skill仓库，但不得机械复制；应结合本项目的课程开发目标、命名规范、目录结构与质量门禁进行改造。

---

## 11. 目录初始化、审计与整理

本项目默认使用 `course-directory-structure` skill处理目录问题。

### 11.1初始化

新项目可优先运行：

```bash
uv run .opencode/skills/course-directory-structure/scripts/bootstrap_course_tree.py --root . --mode full --with-placeholders
```

### 11.2结构审计

对现有项目，优先运行：

```bash
uv run .opencode/skills/course-directory-structure/scripts/check_course_tree.py --root .
```

### 11.3整理原则

-先审计、后整理
-先出建议、后批量移动
-先拆分混合内容，再进行发布分层
-尽量减少破坏性重命名
-对可能被引用的路径保持谨慎

---

## 12. QA与QC的角色边界

### 12.1 QA的角色

QA负责：

-找问题
-记问题
-分类问题
-评估严重性
-提醒风险

QA不负责直接替代所有整改动作，也不负责单方面宣布可以发布。

### 12.2 QC的角色

QC负责：

-判断问题处理状态
-判断风险接受与否
-判断是否允许发布
-形成对项目管理和交付负责的结论性报告

### 12.3 QA/QC文档输出

- QA输出进入 `docs/06-qa/`
- QC输出进入 `docs/07-qc/`
-若生成汇总报告，默认采用Markdown，必要时再导出其他格式

---

## 13. 常见错误与禁止事项

### 13.1常见错误

-直接开始写正文，却没有项目brief和提纲
-学员版、教师版和QA批注混在一个文件里
-参考资料收集很多，但没有完成提炼
- QA做了很多意见，却没有对应QC结论
-反复生成“最终版”，但没有真正的版本管理与发布目录
-目录命名以日期或作者为主，而不是以课程结构为主

### 13.2禁止事项

-禁止把教师答案或内部提示直接混入学员资料
-禁止把 `references/` 直接当成 `release/`
-禁止在没有审计与建议的情况下大规模乱移文件
-禁止把QA记录伪装成正式课程正文
-禁止用含糊命名覆盖已有正式版本
-禁止在没有QC结论时把草稿宣称为正式发布版

---

## 14. 任务完成的最小交付标准

任何较完整的课程开发任务，至少应交付以下之一：

-已更新的目标文件
-审阅意见与问题列表
-结构整理建议
-计划与变更记录
- QA记录
- QC结论
-可复用模板或方法说明

不能只停留在“我已阅读”“建议如下”而没有可落地成果文件，除非任务本身明确只要求口头分析。

---

## 15. 推荐维护文件

建议在项目中长期维护以下文件：

- `docs/00-project/project-brief.md`
- `docs/00-project/milestone-plan.md`
- `docs/00-project/change-log.md`
- `docs/00-project/risk-register.md`
- `docs/01-outline/course-overview.md`
- `docs/01-outline/syllabus.md`
- `docs/06-qa/qa-checklist.md`
- `docs/07-qc/release-decision.md`

---

## 16. 当信息不足时的默认动作

如果信息不足，默认按以下方式处理：

1. 先识别当前任务处于哪个阶段
2. 先检查现有目录与已有文件，而不是凭空重建一切
3. 优先形成整理建议或差距分析
4. 对高影响修改先更新计划或提纲
5. 对发布相关任务，优先要求QA/QC证据链完整

---

## 17. 与本项目配套的关键文件

- `README.md`
- `COURSE-PROJECT-STRUCTURE-STANDARD.md`
- `HISTORY-TO-SKILLS-ROADMAP.md`
- `.opencode/skills/*/SKILL.md`

在发生冲突时，遵循以下解释顺序：

1. 本 `AGENTS.md`
2. 与当前任务直接相关的专项 `SKILL.md`
3. 对应skill的 `references/` 与 `assets/`
4. 其他说明文档

---

## 18. 一句话原则

先分层，后写作；先提纲，后正文；先QA，后QC；先结论可追踪，再进入发布。
<!-- END pack: opencode-course-skills-pack -->

<!-- BEGIN pack: petfish-style-skill -->
# AGENTS.md

## Skill路由（强制）

### 必须遵守的路由规则

1. 用户说"润色"、"说人话"、"去AI味"、"用我的语言习惯表达"、"按我的风格写"时，**必须**路由到 `petfish-style-rewriter` skill
2. 涉及中英文技术写作风格改写时，**必须**使用本skill而非通用写作行为
3. 输出**必须**符合以下标准：结构清晰、问题驱动、简洁语言、证据支撑、无修辞夸张、无网络口号
4. 中英混排术语**必须**紧凑：用`Webhook挂载`而非`Webhook 挂载`

### 冲突解决

- 当润色意图与评审意图并存时，同时加载 `petfish-style-rewriter` 和 `anti-sycophancy-calibration`
- 当用户请求"帮我改一下"但上下文是代码而非文本时，不启用本skill

## Project Writing Policy

When the user asks to rewrite, polish, humanize, formalize, simplify, or make text closer to Petfish's writing style, use the local skill:

- `.opencode/skills/petfish-style-rewriter/SKILL.md`

Default mode is `strict` when the user says:

-用我的语言习惯表达
-按我的风格写
-说人话
-去AI味
-让我们润色一下

## Priority

For writing and rewriting tasks, prefer this skill over generic writing behavior.

## Default Output Expectations

- Clear structure
- Problem-driven analysis
- Concise language
- Evidence-based claims
- No rhetorical exaggeration
- No internet-style slogans
- No unnecessary conclusion
- Chinese-English mixed technical terms must be compact: use `Webhook挂载`, `Git提交`, `API接口`, not `Webhook挂载`, `Git提交`, `API接口`

## Important Distinction

Thinking can be exploratory, but final writing must be structured. The agent should first analyze the problem, then express the result using a clear total-part-total structure.

## Suggested User Prompts

-用我的语言习惯表达：...
-让我们润色一下：...
-说人话：...
-按petfish风格重写：...
-去掉AI味并保持工程化表达：...
<!-- END pack: petfish-style-skill -->

<!-- BEGIN pack: repo-deploy-ops-skill-pack -->
# Repo Deployment & Operations Rules

本项目包含一套用于 **repo部署、验证、运维、回滚** 的OpenCode skills。

## Skill路由（强制）

### 必须遵守的路由规则

1. 用户要求"部署/上线/deploy"时，**必须**先用 `repo-runtime-discovery` 识别技术栈，再用 `target-host-readiness` 检查主机，最后用 `deployment-executor` 执行
2. 用户给出宽泛部署任务（"帮我把这个repo部署起来"）时，**必须**启用 `repo-service-lifecycle` 作为总控
3. 部署完成后，**必须**用 `deployment-verifier` 给出至少一份验证结果（健康检查/smoke test/日志核验）
4. 遇到部署异常或线上故障时，**必须**使用 `incident-rollback` 处理，优先止血
5. 持续运维场景**必须**使用 `service-operations`，记录版本、路径、端口、变更时间

### 冲突解决

- 当用户同时要求"部署并运维"时，先走部署链路（discovery→readiness→executor→verifier），完成后再切入 `service-operations`
- 当不确定是新部署还是升级时，先用 `repo-runtime-discovery` 判断现有部署状态

## 工作原则

-当用户要求“读取repo/GitHub项目并部署到指定主机”时，优先走完整链路：
  1. `repo-runtime-discovery`
  2. `target-host-readiness`
  3. `deployment-executor`
  4. `deployment-verifier`
  5. 如需持续管理，再使用 `service-operations`
  6. 如遇异常，再使用 `incident-rollback`

-如果用户给的是宽泛任务，例如：
  - “帮我把这个仓库部署到10.0.0.5”
  - “把这个GitHub repo跑起来并验收”
  - “把这个服务上线后帮我持续运维”

  优先启用 `repo-service-lifecycle` 作为总控技能。

## 必须遵守

-先分析repo与目标主机，再选择部署方式。
-不得在未形成最小部署计划前直接执行高风险变更。
-不操作其它仓库的内容（即使有权限），只能通过issues反馈问题和建议。
-网络出现问题或可能是网络问题导致的中断（SSH无法连接、apt install失败、docker pull超时），不要急于改变当前方案，至少重试两次再行调整。
-涉及覆盖、替换、重启、删除、迁移时，必须先说明：
  -本次动作影响范围
  -回滚入口
  -验证办法
-部署完成后必须给出至少一份验证结果：
  -健康检查
  -功能smoke test
  -日志核验
  -端口/进程/页面/API结果
-任何长期运维动作都要记录版本、时间、路径、端口、依赖、观察点。

## 输出偏好

当任务涉及部署或运维时，默认输出以下结构：

1. **识别结果**
2. **部署计划**
3. **执行结果**
4. **验证结果**
5. **回滚点**
6. **后续运维建议**

## 懒加载参考文件

只在需要时读取skill中的 `references/*.md` 与 `assets/*` 文件，不要一次性全部加载。
<!-- END pack: repo-deploy-ops-skill-pack -->

<!-- BEGIN pack: research-skill-pack -->
# Research Skill Pack Rules

本项目已安装研究工作台技能包（research-skill-pack）。

## 工作原则

- 先定义问题，再搜集资料
- 先合法获取全文，再摘录原文与出处
- 先记录阅读笔记和灵光闪现，再提升为正式证据
- 先建立证据账本，再形成判断
- 先区分事实、推断、灵感、假设与建议，再写报告
- 生成与审查分离
- skill本体短小精确，复杂知识放入references与scripts

## 默认研究流程

```
research-router → research-brief-framer → research-source-discovery → research-literature-access → research-note-capture → research-insight-log → research-evidence-ledger → research-synthesis → research-report-writer → research-quality-reviewer
```

## 证据类型系统

| Type | Meaning | Can enter report? |
|---|---|---|
| EXTRACTED | Directly from source | Yes, with citation |
| INFERRED | Derived from multiple facts | Yes, with reasoning |
| AMBIGUOUS | Conflicting sources | Yes, as uncertainty |
| PROPOSED | Our suggestion/hypothesis | Yes, labeled as recommendation |

## 必须遵守

- 每条重要claim必须有source_id和evidence_id
- 不得把模型常识当作研究事实
- 不得把摘要伪装成原文
- 不得存储明文凭据
- 不得使用非法来源获取文献
- 质量审查必须独立于报告生成
- 灵感不能直接当作事实进入报告

## 研究工作区结构

```
research/
  CONTEXT.md
  00_brief/
  01_sources/
  02_notes/
  03_evidence/
  04_methods/
  05_analysis/
  06_outputs/
  07_reviews/
  adr/
```

## Skill路由（强制）

### 必须遵守的路由规则

1. **研究意图必须首先路由到 research-router**：当用户表达研究、调研、文献、综述、竞品分析、市场分析、论文方向等研究意图时，**必须**首先路由到 `research-router`，由router判断研究类型后再分发到具体skill。不得跳过router直接调用下游skill。
2. **证据链路必须完整**：涉及证据收集和报告生成的任务，**必须**按照默认研究流程（router → brief → sources → ... → report → review）执行，不得跳过中间环节直接写报告。
3. **质量审查必须独立于生成**：`research-quality-reviewer` **必须**在 `research-report-writer` 之后独立运行，不得将生成与审查合并在同一步骤。
4. **研究意图 vs 普通搜索的冲突解决**：当用户请求可能同时匹配"搜索信息"和"做研究"时，以下信号判定为研究意图并路由到research-router：
   - 包含"研究"、"调研"、"综述"、"literature"、"survey"等明确研究词汇
   - 要求系统性分析、证据收集、对比评估
   - 涉及多来源交叉验证、方法设计、实验规划
   - 要求产出结构化报告或决策建议
5. **Agent自发研究同样必须路由**：当agent在执行复合任务时自行判断需要研究（如可行性分析、架构调研、技术选型、方案对比等），即使没有用户消息显式触发，**也必须**路由到 `research-router`。判断标准：agent的子任务目标包含"调研"、"分析可行性"、"对比方案"、"评估技术"、"了解现状"等研究性动作时，视为研究意图。不得因为是agent自发行为而跳过路由。

### 意图分类 → Skill路由映射

| 用户意图 | 必须路由到 |
|---|---|
| 模糊研究请求 | research-router |
| 需要定义研究问题 | research-brief-framer |
| 需要找资料 | research-source-discovery |
| 需要获取文献全文 | research-literature-access |
| 需要摘录和阅读笔记 | research-note-capture |
| 有想法要记录 | research-insight-log |
| 需要建立证据 | research-evidence-ledger |
| 需要综合分析 | research-synthesis |
| 需要写报告 | research-report-writer |
| 需要审查报告质量 | research-quality-reviewer |
| 需要引用审计或检查无证据断言 | research-citation-auditor |
| 需要文献综述或系统回顾 | scientific-literature-review |
| 需要找研究空白或贡献点 | scientific-gap-finder |
| 需要方法设计或验证路径 | scientific-methodology-designer |
| 需要实验设计或评价指标 | scientific-experiment-planner |
| 需要写论文或论文骨架 | scientific-paper-writer |
| 需要审稿自查或回复审稿人 | scientific-review-rebuttal |
| 需要用户研究、访谈、问卷或画像 | product-user-research |
| 需要竞品分析、市场分析或SWOT | product-competitor-analysis |
| 需要机会分析、JTBD或需求挖掘 | product-opportunity-mapper |
| 需要验证计划、MVP设计或假设验证 | product-validation-planner |
| 需要产品决策简报或go/no-go建议 | product-decision-brief |
| 需要环境扫描、PESTLE或趋势分析 | planning-environment-scanner |
| 需要利益相关方分析或参与策略 | planning-stakeholder-analyst |
| 需要情景规划或不确定性分析 | planning-scenario-planner |
| 需要政策研究或法规分析 | planning-policy-researcher |
| 需要技术评估或成熟度分析 | planning-technology-assessor |
| 需要战略路线图或里程碑规划 | planning-roadmap-developer |
| 需要定义学习目标或学习计划 | learning-goal-framer |
| 需要梳理前置知识或学习依赖 | learning-prerequisite-mapper |
| 需要发现和筛选学习资源 | learning-resource-discovery |
| 需要设计分阶段学习路径 | learning-path-designer |
| 需要设计练习任务或动手实操 | learning-practice-planner |
| 需要检查学习进度或阶段复盘 | learning-progress-reviewer |
| 需要定义决策问题和约束 | decision-brief-framer |
| 需要构建决策标准和权重 | decision-criteria-builder |
| 需要方案对比打分矩阵 | option-comparison-matrix |
| 需要生成最终决策建议 | decision-recommendation |
| 需要定义风险评估对象和边界 | risk-research-brief |
| 需要供应商或开源项目尽调 | vendor-source-diligence |
| 需要安全风险审查 | security-risk-review |
| 需要合规风险检查 | compliance-check |
| 需要总拥有成本和运营风险评估 | tco-operational-risk |
| 需要最终采用建议 | adoption-recommendation |
| 需要定义活动或体验目标 | experience-brief-framer |
| 需要场地或目的地研究 | venue-destination-research |
| 需要日程或行程规划 | schedule-itinerary-planner |
| 需要参与者体验设计或旅程优化 | participant-experience-designer |
| 需要后勤和风险预案 | logistics-risk-planner |
| 需要活动执行手册 | event-runbook-writer |
| 需要旅行规划领域增强 | travel-adapter |
| 需要会议筹备领域增强 | conference-adapter |
| 需要培训活动领域增强 | training-event-adapter |
| 需要内容选择领域增强 | content-selection-adapter |

## 数据格式约定

- 面向机器消费的数据技能（source-discovery、note-capture、evidence-ledger）默认使用 JSONL。
- JSONL 便于结构化校验、lint 检查、脚本处理与流水线拼接。
- 面向人类阅读的输出技能（brief-framer、synthesis、report-writer）默认使用 Markdown。
- Markdown 更适合叙述、审阅与协作编辑。
- 这是有意设计：JSONL 负责保存可追踪证据链，Markdown 负责呈现结论与洞见。
- 两种格式都有效，不存在“谁替代谁”。
- 选择原则：下游消费者是脚本就优先 JSONL；是读者/评审就优先 Markdown。
<!-- END pack: research-skill-pack -->

<!-- BEGIN pack: series-style-governor-pack -->
# Series Style Governor Pack

本pack提供跨文档风格一致性治理能力，帮助Agent在系列Markdown文档（书籍、课程、白皮书、研究笔记等）中维持术语、命名、排版和叙事结构的一致性。

## Skill路由（强制）

### 必须遵守的路由规则

1. 用户要求跨多个文档统一风格、术语、命名或排版时，**必须**路由到 `series-style-governor` skill
2. 用户提供参考文档并要求其他文档对齐其风格时，**必须**路由到 `series-style-governor` skill
3. 用户要求检查系列文档的术语漂移、命名不一致或排版漂移时，**必须**路由到 `series-style-governor` skill
4. 用户要求保守改写文档以匹配系列基线风格时，**必须**先产出审计报告和改写计划，再执行改写

### 冲突解决

- 单文档润色不触发本skill → 路由到 `petfish-style-rewriter`
- 长文写作流程（fat/slim）不触发本skill → 路由到对应写作skill
- 纯Markdown格式修复且无系列上下文 → 路由到 `markdown-course-writing`
- 研究笔记摘录 → 路由到 `research-note-capture`
- 本skill可与 `petfish-style-rewriter` 组合：先归一化再润色

## 何时启用

- 用户明确提到"系列风格"、"跨文档一致性"、"风格画像"、"术语漂移"、"排版漂移"
- 用户要求以某个文档为基准统一其他文档风格
- 用户要求审计或改写一批Markdown文档以保持风格一致
- 用户要求构建或更新系列风格规范

## 何时不启用

- 单文档编辑或润色
- 纯排版格式修复（无系列上下文）
- 研究或调研任务
- 代码编写或调试

## 行为规则

- 不引入新事实、不删除引用、不改变技术论断
- 不把作者语言变成通用AI腔
- 改写可能改变语义时标记为 `review-needed`，不静默应用
- 基线文件不覆盖，除非用户显式要求
- 后续文档结构优于基线时，报告建议基线升级，不降级
- 中文技术写作默认中文英文之间无空格（如 `Webhook挂载`），除非基线另有惯例
<!-- END pack: series-style-governor-pack -->
