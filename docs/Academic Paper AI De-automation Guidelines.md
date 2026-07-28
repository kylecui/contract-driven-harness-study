学术论文去 AI 化写作与审校规范

版本：v1.0

1. 目的与适用范围

本规范用于减少学术论文中的 AI 式同质化表达，恢复研究者真实的论证轨迹、证据边界和专业判断。

本规范不以“通过 AI 检测器”为目标，也不要求故意加入语病、口语或不规则表达。其目标是：

•

使每项论断可追溯至证据、设计选择或文献；

•

使语言结构服从研究逻辑，而不是服从生成模板；

•

保留负面结果、局部失败、测量困难和适用边界；

•

允许使用 AI 辅助校对，但避免由 AI 代替作者完成研究论证。

2. “AI 化”的三个层次

2.1 内容层 AI 化

主要表现为：

•

论断宽泛，但没有数据、案例或文献支持；

•

只报告正面结果，不报告失败、例外和限制；

•

研究问题、方法、结果和结论之间缺乏可验证的对应关系；

•

根据标题或摘要拼接相关工作，而没有实际阅读来源；

•

生成不存在的因果关系、贡献、实验解释或引用。

内容层问题最严重。即使句子写得自然，只要证据链不存在，仍属于实质性 AI 化。

2.2 修辞层 AI 化

主要表现为：

•

每段都遵循相同的“背景—转折—方案—总结”结构；

•

连续使用完全平行的句型；

•

每个局部设计都被命名为一个新概念；

•

每段末尾都出现提升意义的总结句；

•

过度使用二元对照、三项排比和覆盖性枚举；

•

使用大量  Furthermore 、 Moreover 、 Additionally 、 Finally  推动文本，而非依靠实际逻辑关

系。

2.3 表面层 AI 化

主要表现为：

•

句长、语气和复杂度高度均匀；

•

抽象名词和评价形容词密度过高；

1

•

缺乏研究对象、参数、版本、条件和失败现象；

•

频繁使用“学术化”但信息量低的表达；

•

为避免重复而随意更换术语，导致概念漂移。

审校顺序必须是：

内容证据 → 论证结构 → 修辞表达 → 词句表面

不得只做同义词替换或句式扰动。

3. 核心原则

3.1 先有证据，再有句子

任何关键论断在进入正文前，应能够回答：

1.

该论断来自实验、实现、文献还是作者判断？

2.

对应的数据、日志、代码、图表或来源在哪里？

3.

它在什么条件下成立？

4.

哪些情况尚未得到验证？

5.

它是观察、解释、假设还是结论？

不能回答上述问题的句子，不应通过“润色”进入论文。

3.2 局部真实优先于整体流畅

真实研究通常包含：

•

指标难以解释；

•

实验结果不一致；

•

某次修复暴露了新的缺陷；

•

某个假设只在部分任务上成立；

•

某些运行需要重试；

•

当前证据只能支持局部结论。

不得为了叙事流畅，将研究过程改写为线性成功故事。

3.3 具体事实优先于抽象评价

优先写：

The model passed 4 of 4 targeted smoke runs under G8 and G9.

而不是：

The proposed approach demonstrated strong and robust performance.

优先写：

Contract adherence increased, whereas gap movement remained mixed.

2

而不是：

The harness significantly improved overall reliability.

3.4 语言结构服从逻辑结构

平行句、排比和枚举不是禁用项。仅在下列情况下使用：

•

表达正式分类；

•

对齐可比较的实验条件；

•

定义后文持续使用的维度；

•

列出互不重叠的贡献或组件。

不得只因为句子“听起来完整”而补齐第三项、第五项或最后一项。

4. 主语与  we  的使用规则

4.1 不全面禁止  we

we  是否合适，取决于句子表达的责任主体，而不是取决于其是否“主观”。

适合使用  we  的情形

用于明确作者实施的研究行为：

•

We introduce ...

•

We evaluate ...

•

We selected ...

•

We exclude ...

•

We restrict the claim to ...

•

We changed the evaluation unit because ...

这些句子回答“作者做了什么”，使用主动语态通常比被动语态清楚。

可删除的导航型  we

例如：

We next describe the execution engine.

可以直接改为：

The execution engine consists of an interpreter and an executor.

章节标题已经提供导航时，不必反复使用  We next ... 、 We then ... 。

应避免的主观型  we

•

We believe ...

3

•

We think ...

•

We can clearly see ...

•

We feel that ...

•

We hope that the results prove ...

应改为证据、推断或范围表述：

The results are consistent with ...

The evidence supports ...

The current experiments do not establish ...

4.2 主语选择顺序

在同样准确的情况下，按以下顺序选择主语：

1.

结果或证据

Table 3 reports ...

The four runs produced ...

2.

研究对象或系统组件

The validator rejects ...

The harness preserves ...

3.

实验或研究设计

The evaluation covers ...

The ablation isolates ...

4.

作者

We selected ...

We define ...

5.

被动语态

仅在行为主体不重要或已知时使用：

Accuracy was computed using exact match.

4.3  we  的审校触发条件

以下情况应重新检查，但不是机械禁令：

•

连续三句以  We  开头；

•

一个段落中的每句话都以作者为主语；

•

we  只承担章节导航作用；

•

we  后面接主观判断而非研究行为；

•

被动语态只是为了机械删除  we 。

4

5. 句子级规范

5.1 一个句子只承担一个主要论证任务

避免在一个长句中同时完成：

•

背景说明；

•

相关工作比较；

•

方法介绍；

•

功能枚举；

•

效果判断。

过载句应按逻辑拆分，而不是按固定字数拆分。

5.2 不追求人工制造的句长变化

句长变化应来自内容需要：

•
•

定义和结论可以较短；
条件、过程和限制可以较长；

•

关键结果可单独成句；

•

不得为了“像人写的”而随机切句。

5.3 限制覆盖性枚举

当列表超过四项时，应检查：

•

是否都是核心项；

•

是否属于同一分类层级；

•

是否会在后文逐项讨论；

•

是否可以拆成机制与基础设施两组；

•

是否只是为了显得系统完整。

原式：

The harness provides specifications, bounded memory, evidence bundles, output

contracts, gates, validators, tracing, logging, replay, and auditing.

可改为：

The harness makes task obligations explicit through specifications, bounded memory,

evidence constraints, and validation gates. Execution traces support later inspection and

auditing.

5.4 避免装饰性对称

原式：

Version 2 repaired trace retention but exposed unknown-state omissions. Version 3

repaired unknown-state retention but exposed provenance compression.

5

这种结构可以使用一次，但连续重复会显得机械。

可改为：

Version 2 retained the decision trace and stage gate. Some runs still omitted unknown

state, so Version 3 added an explicit unknown-state requirement. That change removed

the omission but revealed a separate provenance problem for known state.

5.5 区分观察、解释和假设

观察

解释

假设

Contract adherence increased from X to Y.

The increase is consistent with the validator preventing incomplete outputs.

One possible explanation is that explicit state fields reduced the need for implicit context

recovery.

不得把解释直接写成已证实的因果关系。

5.6 删除无证据的程度词

以下词语只有在有定义或证据时才能使用：

•

significant

•

substantial

•

robust

•

comprehensive

•

effective

•

efficient

•

scalable

•

reliable

•
•

flexible
seamless

•

precise

•

strong

•

superior

例如：

a significant improvement

应明确是统计显著、工程上显著，还是仅指数值较大。否则直接报告数值。

6

5.7 避免无信息量的强调语

优先删除或具体化：

•

It is important to note that ...

•

It is worth mentioning that ...

•

Notably, ...

•

Interestingly, ...

•

Clearly, ...

•

Undoubtedly, ...

•

As is well known, ...

如果一句话必须依靠  Notably  才显得重要，通常应补充说明其重要性来自何处。

5.8 不做同义词轮换

同一技术对象应持续使用同一术语。不要为了避免重复，在以下词语之间随意切换：

•

harness

•

framework

•

infrastructure

•

architecture

•
•

platform
environment

除非它们确实指向不同层次。

学术写作中的术语重复通常优于概念漂移。

6. 段落级规范

6.1 每段只处理一个问题簇

一个技术段落通常包含：

1.

局部论点或对象；

2.
3.

必要的机制、证据或过程；
解释或适用边界。

不是每段都必须完整包含三部分，也不是每段都必须以总结句结束。

6.2 避免空泛的段首句

低信息量段首：

Reliability is an important issue in modern agent systems.

更具体的段首：

7

Workflow-level scores cannot identify whether a failure originated in schema compliance,

state retention, evidence grounding, or stage control.

6.3 不要求每段闭环升华

以下模式使用过多时容易产生 AI 感：

事实 → 解释 → “This demonstrates the broader importance of ...”

如果下一段自然继续讨论，无须在当前段末增加宏观意义。

6.4 段落之间依靠论证关系连接

只有在逻辑关系不明显时才使用连接词。

•

递进： Furthermore

•

对比： By contrast

•

因果： Therefore

•

转折： However

如果句子内容本身已表达对比，不必再叠加连接词。

7. 术语与命名治理

7.1 新术语的准入条件

只有同时满足下列条件，才应命名新概念：

•

它代表一个稳定、可复用的研究对象；

•

与现有术语存在明确区别；

•

后文会多次使用；

•

有操作性定义或判定标准；

•

命名有助于测量、实现或比较。

7.2 不为每个实验步骤命名

以下对象通常不必全部获得正式名称：

•

一次局部修复；

•

一个临时测试序列；

•

一个中间版本；

•

一组只出现一次的义务；

•

一次邻近任务验证。

可以保留编号，例如  Stage 7e ，但不必同时增加长名称，除非该名称在全文承担索引功能。

8

7.3 缩略语准入

缩略语应满足：

•

在全文中会反复出现；

•

能显著减少阅读负担；

•

不与领域已有缩略语冲突；

•

首次出现时完整定义。

仅出现两三次的长名称，通常不需要缩写。

7.4 避免营销式命名

慎用以下结构：

•

X-driven

•

X-aware

•

X-oriented

•

next-generation

•

unified intelligent

•

comprehensive adaptive

•

end-to-end robust

名称应描述机制，而不是预先宣布价值。

8. 各章节写作规范

8.1 摘要

摘要应完成五项任务：

1.

明确具体问题；

2.

指出现有方法缺口；

3.

说明本文方法或系统；

4.

给出主要评价证据；

5.

限定结论范围。

摘要规则

•

we introduce / we evaluate / we show  可以使用；

•

系统能力优先以系统为主语；

•

只保留核心功能，不写完整产品清单；

•

至少给出一个具体评价范围、数据或任务类型；

•

不写正文没有验证的价值判断；

•

不连续使用  Furthermore 、 Additionally 、 Finally  罗列贡献；

•
•

不把“支持某功能”自动写成“提高可靠性”；
结尾应陈述证据支持的结论，而非愿景。

9

推荐结构

Existing systems exhibit problem P under condition C.

Current approaches address A but leave B unresolved.

This paper introduces method M, which externalizes or controls X.

Evaluation on tasks T shows result R under conditions K.

The evidence supports bounded claim Q; it does not establish broader claim Z.

8.2 引言

引言应从具体研究问题开始，而不是从宏大趋势开始。

避免：

优先：

Artificial intelligence has revolutionized numerous industries.

Long-running agent workflows often carry control flow and intermediate state implicitly in

the model context.

引言规则

•

每项领域现状判断应有来源；

•

相关工作缺点必须具体到机制或使用条件；

•

不将“尚未解决”写成“完全不能解决”；

•

研究空白应与后文方法直接对应；

•

贡献列表中的各项应互不重复并可被验证；

•

不在引言中提前宣布所有结果都成功；

•

不重复摘要中的整套功能枚举。

8.3 相关工作

相关工作不是论文名单，也不是摘要拼接。

推荐组织方式

按比较维度组织：

•

控制流表示；

•

状态管理；

•

证据管理；

•

执行环境；

•

验证机制；

•

可组合性；

•

评价对象。

10

相关工作规则

•

每个引用支持一个明确命题；

•

不使用未实际阅读的来源；

•

AI 检索结果只能作为候选线索；

•

避免  many studies 、 numerous approaches  等无边界概括；

•

不把自己的系统设置为唯一拥有全部优点的一方；

•

比较表的维度必须可定义、可重复判定；

•

对竞争方法的描述应与其原文一致。

8.4 方法与系统设计

方法章节的目标是可理解、可复现和可审查，而不是显得全面。

主语选择

优先使用：

•

The interpreter ...

•

Each workflow ...

•

The validator ...

•

The state record ...

•

A stage gate ...

内容要求

•

输入、输出和状态；

•

控制流和数据流；

•

前置条件与后置条件；

•

失败处理；

•

默认行为；

•

边界条件；

•

配置项；

•

与其他模块的接口。

避免

•

seamlessly integrates

•

offers unparalleled flexibility

•

provides comprehensive support

•

greatly simplifies

•

ensures reliability

除非后文给出操作定义和证据。

设计目标与已实现性质必须区分：

The design aims to preserve state across stages.

不等同于：

11

The design preserves state across stages.

8.5 实验与结果

推荐顺序：

1.

研究问题或假设；

2.

实验对象；

3.

基线；

4.

输入和条件；

5.

指标；

6.

结果；

7.

解释；

8.

威胁与限制。

结果陈述规则

•

先给事实，再给解释；

•

报告数值、样本量、版本和条件；

•

明确是绝对变化还是相对变化；

•

明确重试、剔除和失败运行；

•

不把 smoke test 写成完整验证；

•

不把局部迁移写成普遍泛化；

•

不隐藏 mixed、undefined 或 negative results；

•

不用“outperforms”替代数值；

•

不根据少量运行声称稳定性。

推荐句式

Under G8 and G9, all four targeted runs satisfied the strict macro metric.

The result supports local transfer to a closely related macro. It does not establish transfer

to open-ended workflows.

8.6 讨论

讨论应解释结果，而不是重复结果。

至少考虑：

•

为什么出现该结果；

•

是否存在替代解释；

•

哪个机制可能产生影响；

•

当前设计能否隔离该机制；

•

结果对什么任务成立；

•

哪些任务不应外推；

•

哪些证据仍然缺失。

12

使用：

•

is consistent with

•

may be explained by

•

suggests

•

does not distinguish between

•

cannot establish

慎用：

•

proves

•

demonstrates that X causes Y

•

confirms

•

ensures

8.7 局限性

局限性不应只是结尾处的礼节性段落。

应具体说明：

•

任务范围；

•

模型范围；

•

样本规模；

•

评价指标限制；

•

基线公平性；

•

重试和随机性；

•

人工判断环节；

•

LLM-as-judge 风险；

•

外部有效性；

•

尚未覆盖的自主性或组合复杂度。

好的限制不是削弱论文，而是确定论断的合法边界。

8.8 结论

结论只做三件事：

1.

重述被验证的问题和方法；

2.

总结证据支持的主要结论；

3.

说明最重要的边界或下一步。

避免：

•

引入新术语；

•

增加正文未证明的贡献；

•

重复全部功能列表；

•

连续列举大量 future work；

13

•

paves the way

•

marks a significant step

•

holds great promise

•

remains an exciting direction

•

We hope this work will ...

未来工作应来自已暴露的问题，而非通用愿望。

例如：

优于：

The current evaluation does not isolate transfer across unrelated workflow classes. A

broader transfer study is therefore the next required step.

Exploring broader applications remains an exciting direction for future work.

9. 图、表与代码的去 AI 化规则

9.1 图表必须承担证据功能

每张图表应回答：

•

它展示什么对象；

•

在什么条件下产生；

•

读者应观察什么；

•

它支持哪个论点。

不得只写：

Figure 3 provides an overview of the system.

应说明：

Figure 3 separates workflow specification from runtime execution and shows where state is

persisted across the boundary.

9.2 表格维度必须可判定

避免为了显示“本方法全优”而选择模糊维度。

每个 ✓、Partial、✗ 应有：

•

明确定义；

•

一致判定标准；

•

可验证来源；

•

必要时给出注释。

14

9.3 代码和配置应来自真实实现

不得让 AI 生成与实现不一致的伪代码。所有代码片段应核对：

•

字段名；

•

参数；

•

默认值；

•

文件路径；

•

返回结构；

•

错误处理；

•

实际版本。

10. AI 辅助写作的使用边界

10.1 适合交给 AI 的任务

•

拼写与语法检查；

•

术语一致性检查；

•

单句或局部段落的清晰度修改；

•

查找重复句式；

•

标记无证据形容词；

•

对照表格检查数字一致性；

•

检查缩略语首次定义；

•

检查图表引用和章节编号；

•

提示可能遗漏的限制项。

10.2 需要严格审查的任务

•

重新组织整个章节；

•

总结多篇文献；

•

改写讨论和结论；

•

从实验日志生成结果叙事；

•

自动补充相关工作；

•

生成贡献列表；

•

解释实验异常；

•

添加引用。

这些任务可能改变论断范围，必须逐句核对。

10.3 不应直接采用的任务方式

避免使用以下宽泛提示：

•

“Rewrite this in an academic style.”

•

“Make this more professional and comprehensive.”

•

“Expand this section.”

•

“Make the argument stronger.”

•

“Write a related-work section with citations.”

•

“Make this less detectable as AI-generated.”

15

这些提示通常会产生抽象化、扩写、术语增殖和无证据强化。

11. 推荐的 AI 校对提示词

11.1 诊断，不重写

Review the passage only for the following issues:

1. unsupported claims;

2. causal claims not justified by the stated evidence;

3. generic academic phrases;

4. unnecessary parallel lists;

5. terminology introduced but not operationally defined;

6. repeated sentence openings;

7. conclusions broader than the reported evidence.

Do not rewrite the passage. Quote each affected sentence and explain the issue.

11.2 受限局部润色

Act as a copy editor.

Preserve all:

- technical claims;

- numerical values;

- citations;

- limitations;

- terminology;

- uncertainty levels;

- paragraph order.

Do not add examples, implications, claims, references, or new terminology.

Return a redline-style revision and explain every substantive change.

11.3 证据追踪检查

For each factual or evaluative claim, identify whether its support is:

- experimental result;

- implementation fact;

- cited literature;

- author interpretation;

- hypothesis;

- unsupported.

Do not supply missing evidence. Mark unsupported or ambiguous claims for author review.

16

11.4 去模板化检查

Identify:

- repeated rhetorical templates;

- consecutive parallel sentence structures;

- decorative transitions;

- generic paragraph-ending summaries;

- unnecessary three-part or five-part lists.

Do not vary sentence structure randomly. Suggest changes only when the structure does not

reflect a real taxonomy or causal sequence.

12. 高风险词语审校表

类型

常见表达

审校问题

夸大价值

groundbreaking, transformative, unprecedented 是否有比较依据

无定义质量 robust, effective, reliable, scalable

如何测量

产品化表达 seamless, flexible, user-friendly

是否经过评价

空泛重要性 crucial, pivotal, significant

对谁、在何条件下

通用升华

paves the way, broad implications

是否超出证据

模板式未来 promising direction, exciting avenue

是否来自具体缺口

强制强调

notably, importantly, clearly

能否由事实本身体现

泛化范围

widely, generally, universally

样本和范围是否支持

不明主体

it is believed, it is recognized

谁认为、来源何在

因果强化

leads to, ensures, results in

是否只是相关或推测

这些词语不是绝对禁用词，但每次出现都应通过证据审查。

13. 完整审校流程

阶段 1：建立证据账本

为每个主要论断记录：

•

claim ID；

•

所属章节；

•

证据类型；

•

数据或来源位置；

•

条件；

•

限制；

17

•

是否允许因果表述。

阶段 2：人工建立论证骨架

先写：

•

研究问题；

•

方法选择；

•

实验设计；

•

结果；

•

异常；

•

解释；

•

边界。

此阶段不追求完整英语句子。

阶段 3：从证据写初稿

不得让 AI 仅根据章节标题生成正文。初稿必须从：

•

表格；

•

日志；

•

代码；

•

图；

•

实验记录；

•

文献笔记

逐项写出。

阶段 4：结构审查

检查：

•

每段是否只有一个问题簇；

•

结果和讨论是否分离；

•

贡献和实验是否对应；

•

结论是否超出证据；

•

是否保留不利结果。

阶段 5：受限 AI 校对

仅进行：

•

语法；

•

清晰度；

•

重复；

•

术语；

•

过度模板化诊断。

18

阶段 6：逐句人工接受

任何 AI 修改必须由作者判断：

•

是否改变事实；

•

是否提高确定性；

•

是否删除限制；

•

是否增加因果；

•

是否引入新术语；

•

是否造成概念漂移。

阶段 7：最终事实核对

逐项核对：

•

数字；

•

表格；

•

图号；

•

版本；

•

模型；

•

数据集；

•

引用；

•

超链接；

•

附录；

•

实验条件。

阶段 8：披露 AI 使用

根据投稿场所要求，说明 AI 用于：

•

编程辅助；

•

文献检索辅助；

•

语言校对；

•

图表或代码辅助；

•

其他具体环节。

不得以“AI 仅用于润色”为由忽略其实际参与的研究步骤。

14. 最终验收清单

提交前，逐项回答“是”或“否”。

内容

•

[ ] 每个主要论断都有可追溯依据。

•

[ ] 观察、解释、假设和结论已经区分。

•

[ ] 负面、混合和未定义结果得到保留。

•

[ ] 所有因果表述都有相应设计支持。

•

[ ] 结论没有超出实验范围。

•

[ ] 所有引用均已实际核验。

19

结构

•

[ ] 摘要中的贡献均在正文得到验证。

•

[ ] 每个贡献都有对应实现或实验。

•

[ ] 结果与讨论没有混写为宣传性叙事。

•

[ ] 局限性具体，而非礼节性声明。

•

[ ] 结论没有引入新事实和新术语。

语言

•

[ ]  we  仅用于真实作者行为或范围决策。

•

[ ] 没有为了删除  we  而滥用被动语态。

•

[ ] 没有连续使用相同句式推进多段内容。

•

[ ] 列表反映真实分类，而非追求完整感。

•

[ ] 评价形容词均有定义、数据或比较依据。

•

[ ] 连接词表达真实逻辑关系。

•

[ ] 术语保持一致，没有同义词轮换。

•

[ ] 段末没有不必要的宏观升华。

AI 使用

•

[ ] AI 没有生成未经核实的事实或引用。

•

[ ] AI 没有擅自扩大论断。

•

[ ] AI 修改已逐句审查。

•

[ ] 原始数据、日志和版本记录仍然保留。

•

[ ] AI 使用范围按要求进行披露。

15. 项目级硬约束简版

## Academic Writing Constraints

1. Evidence precedes prose. Every major claim must map to an experiment,

   implementation fact, source, or explicitly marked interpretation.

2. Do not optimize for AI-detector scores. Do not introduce grammatical

   errors, random sentence variation, or synonym substitution.

3. Use "we" only for genuine author actions, methodological choices, scope

   decisions, and contribution statements. Prefer the result, system component,

   experiment, or table as the subject when it is the actual actor.

4. Do not replace all active constructions with passive voice.

5. Separate observation, interpretation, hypothesis, and conclusion.

   Do not convert correlation or plausible explanation into causation.

6. Preserve negative, mixed, undefined, retried, and scope-limited results.

7. Avoid generic academic expansion, decorative transitions, repeated parallel

20

   templates, exhaustive feature lists, and paragraph-ending significance claims.

8. Introduce a new term only when it has an operational definition, is reused,

   and supports implementation, measurement, or comparison.

9. Prefer exact conditions, versions, metrics, sample sizes, failures, and

   numerical results over adjectives such as robust, effective, comprehensive,

   significant, or scalable.

10. AI may assist with grammar, consistency, and diagnostic review. It must not

    add claims, evidence, citations, terminology, implications, or limitations.

11. Every AI-assisted revision must preserve technical claims, numbers,

    citations, uncertainty, terminology, and evidentiary scope.

12. The final manuscript must be reviewed against the source data, logs, code,

    figures, tables, and cited papers.

21

