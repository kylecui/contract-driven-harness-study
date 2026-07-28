# Contract-Aware Companion落地计划质量审查

Reviewed: 2026-06-15

Artifact:
`research/06_outputs/petfish-companion-contract-aware-landing-plan.md`

Overall grade: **A**

Blocking issues: none

## 九维审查

| Dimension | Rating | Review |
|---|---|---|
| Question alignment | Pass | 计划回答了产品入口、目标架构、MVP、阶段、资源、指标、决策门和生产准入问题。 |
| Evidence completeness | Pass | 关键架构和研究边界引用16个项目证据ID，人工核验缺失引用为0。 |
| Citation coverage | Pass | 当前Companion职责、论文结果边界、repair loop和explicit-delta边界均有证据引用。实现建议明确属于proposed plan。 |
| Logic chain | Pass | 路线从Companion现状和论文结果，推导到hybrid compiler、advisory MVP、bounded execution和controlled beta，没有直接跳到全面生产。 |
| Counter-evidence | Pass | 计划保留了gap compression非普遍、v5.3因果结果mixed、v5.4不代表生产就绪、live tools未验证等反面边界。 |
| Method fit | Pass | 采用Planning为主、Product/Technology为辅的方法，包含TRL、MVP实验、里程碑、依赖、资源和go/pivot/stop门。 |
| Actionability | Pass | 每阶段包含日期、交付、工程任务、量化验收和决策门；另有前30天Backlog。 |
| Expression quality | Pass | 文档主要使用具体对象、阈值和动作。未使用无证据的弱模型替代、全面可靠或生产就绪表述。 |
| Risk disclosure | Pass | 覆盖用户摩擦、schema漂移、模型路由、evaluator过拟合、成本、平台差异、隐私和副作用风险。 |

## 仓库基线检查

- 实施仓库：`kylecui/petfish.ai`
- 分支：`master`
- 核对提交：`348b7b75a5c27067e7e99f5f814a8d28328dd125`
- 研究工作区角色：证据、方法、fixture和计划，不承载正式运行时实现

## 量化检查

- Evidence references: 16 unique
- Missing evidence references: 0
- Phases: 5, from G0 through G4
- Suggested delivery window: 2026-06-22 through 2026-10-09
- MVP workflows: 4
- Primary cross-model runs in Phase 3: 320
- Critical safety tolerance: 0 violations

## 自动工具限制

`report_quality_gate.py`只接受`EV-XXXXXX`格式，而本项目账本使用
`P2-E###`。自动结果因此错误地把整个账本判为无效，不能用于本计划评级。
本次审查改用显式正则提取和账本比对，16个引用全部存在。

`style_check.py`对Markdown表格、代码块和整段标题元数据按长句处理，并将
用户问题中的“落地”和论文术语`harness`计为AI flavor。人工复核未发现对应
表达构成发布阻断。

## 非阻断问题

1. Phase 0中的产品阈值属于预设工程门，不是历史数据结论。G0必须由产品、
   工程和安全共同冻结，后续不得事后调整。
2. 计划假设3名核心成员。若只有2人，应采用文档中的压缩方案，并将beta推迟。
3. 当前官方仓库已经存在online Gateway contract和output-schema相关计划。
   实施前应做一次SSOT对齐，避免重复创建第二套schema。
4. `fish-trail`接入被正确推迟，但Phase 4后必须决定task memory与topic memory
   的主键和所有权。

## 发布决定

该计划适合作为Companion契约化试点的执行基线。建议先批准Phase 0和Phase 1，
不要一次性批准16周全部投入。G1达标后再释放用户侧Contract Card开发资源。
