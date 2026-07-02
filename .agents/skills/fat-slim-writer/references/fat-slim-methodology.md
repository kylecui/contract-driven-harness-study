# Fat-Slim Writing Methodology Reference

## Phase Details

### Fat Phase Anti-Patterns to Avoid

1. **Premature slimming** — 在Fat阶段就开始删减，导致素材不够
2. **Self-censorship during dumping** — 堆砌时自我审查，限制素材广度
3. **Unstructured dumping** — 漫无目的地写，偏离提纲结构
4. **Skipping uncertain markers** — 不标记 `[待查]`、`[素材]`，导致Slim阶段无法区分

### Slim Phase Decision Framework

```
这段话删掉后论点是否成立？
  ├─ Yes → 删
  └─ No → 保留

这个案例是否是最好的？
  ├─ No → 换成最好的或删
  └─ Yes → 保留

读者会跳过这段吗？
  ├─ Yes → 删或重写
  └─ No → 保留

这段是否在其他地方说过？
  ├─ Yes → 只保留更合适的那处
  └─ No → 保留
```

### Slim Phase Anti-Patterns to Avoid

1. **Attachment to words** — 舍不得删自己写的东西
2. **Skipping cross-chapter audit** — 只做章内减法，不做跨章减法
3. **Residual placeholders** — 最终版还留着 `[待查]` 等标记
4. **Deleting core arguments** — 删过头，核心论点被削弱

## Applicable Scenarios

| Scenario | Typical Length | Notes |
|---|---|---|
| 技术书 | 5万字+ | 每章独立Fat→Slim |
| 白皮书 | 1-3万字 | 全文一起Fat→Slim |
| 长篇报告 | 5000-2万字 | 按section执行 |
| 学位论文 | 3万-10万字 | 按chapter执行，注意文献引用 |
| 深度调研文章 | 3000-1万字 | 全文一起执行 |

## Fat Phase Output Template

```markdown
# 第X章 章节标题

## 核心论点
[必须] 一句话概括本章论点

## 证据与案例
### 案例1: ...
[素材] 案例来源和摘要

### 案例2: ...
[待查] 数据来源待确认

## 反面观点
[至少1个] 与核心论点相对的观点

## 读者疑问预判
[预判] 读者读到此处可能产生的疑问

## 关联章节
→ 第Y章: 关联说明
```
