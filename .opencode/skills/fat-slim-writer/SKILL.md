---
name: fat-slim-writer
description: >
  Long-form writing via two-stage "expand then reduce" workflow: build a material-rich fat draft from outline, then slim into final draft.
  Trigger for 写书, 写长文, 长篇写作, book writing, long-form writing, white paper, long report, thesis section, deep research article, 先加后减, fat-slim.
  Do not use for short copywriting, simple polishing, one-paragraph rewrites, or style normalization across an existing series.
compatibility: opencode
metadata:
  version: "0.2.0"
  author: "petfish-community"
  owner: "petfish-community"
  license: "Apache-2.0"
---

# Fat-Slim Writer

## Role

Long-form content production engine. Executes a two-phase "expand then reduce" writing method: build a material-rich fat draft, then slim it into a final draft through professional editing actions.

## Activation

Activate when the user needs to produce structured long-form content (books, chapters, white papers, long reports, course materials, thesis sections, deep research articles) from outline to final draft.

Do NOT activate for: short copywriting, single-paragraph rewrites, polishing existing text, or style normalization across a series.

## Execution Modes

Choose mode before starting based on user intent.

| User Intent | Mode | Behavior |
|---|---|---|
| "我们一起写" "先帮我堆素材" | `interactive` | Pause after Fat for user confirmation before Slim |
| "直接给完整稿" "不要中途问我" "一次完成" | `auto` | Fat→Slim automatically, include Fat summary and Slim action log |
| "这篇太长，帮我删减" "做减法" "精简" | `review-only` | Only execute Slim on existing draft, no Fat regeneration |

Default: `interactive` if ambiguous.

## Writing Contract

Before Fat phase, confirm or infer from context:

| Field | Required | Default |
|---|---|---|
| document_type | Yes | structured long-form article |
| audience | Yes | professional reader with basic background |
| outcome | Yes | clear explanation and actionable conclusion |
| length_target | Optional | none (no hard limit) |
| tone | Optional | formal, clear, restrained |
| evidence_policy | Yes | distinguish verified facts, assumptions, and pending checks |

If the user provides enough context, infer silently. If not, ask briefly (1-2 questions max).

## Core Method: Fat → Slim

### Phase 1: Fat (Expand)

Goal: pile up materials into a fat draft. Do not judge quality.

1. **Lock outline**: if user has no outline, generate one first; if outline exists, confirm and lock structure
2. **Per-chapter expansion**: for each chapter, cover these dimensions:
   - Core argument (required)
   - Evidence / data / cases (at least 2)
   - Counter-arguments or boundary conditions (at least 1)
   - Cross-chapter references
   - Anticipated reader questions
3. **Material tagging**: tag every piece of material (see Fat Material Tags below)
4. **Source ledger**: maintain `outputs/fat/source-ledger.md` (see references for template)
5. **Rules**:
   - Do not judge quality, just pile
   - Allow repetition, allow roughness
   - Tag everything; never leave untagged material
   - One file per chapter

#### Fat Material Tags

| Tag | Meaning |
|---|---|
| `[用户提供]` | From user input, attachments, or project files |
| `[已知事实]` | Verifiable background fact, use with care |
| `[待查]` | Needs search, citation, or human confirmation |
| `[推测]` | Inferred from context, not a fact |
| `[例子]` | Hypothetical example for illustration |
| `[风险]` | May be off-topic, redundant, inaccurate, or conflicting |
| `[金句]` | Key expression worth preserving into final draft |
| `[争议]` | Multiple viewpoints exist, Slim phase must handle |

**Prohibition**: Do not fabricate statistics, citations, laws, cases, publication names, or external references. If evidence is unverified, tag as `[待查]`.

### Phase 2: Slim (Reduce)

Goal: professional editing — not just deletion.

1. **Transition**: in `interactive` mode, pause and ask "Fat draft ready. Start slimming?" — in `auto` mode, proceed automatically
2. **Per-chapter review**: for each chapter, apply Slim actions (see taxonomy below)
3. **Cross-chapter audit**: check for redundancy, order, and argument completeness across chapters
4. **Close**: verify no `[素材]`, `[待查]`, `[待定]` markers remain in final draft

#### Slim Action Taxonomy

| Action | When to Use |
|---|---|
| `DELETE` | Content does not support argument, repeats, or weakens structure |
| `COMPRESS` | Content is useful but too verbose |
| `MERGE` | Two or more sections express similar points; combine into one stronger section |
| `MOVE` | Content is valuable but in wrong place; relocate to chapter, appendix, footnote, or source ledger |
| `REWRITE` | Idea is valuable but expression is unclear, generic, or inconsistent with writing contract |

For each action, record in `outputs/slim/slim-review.md`: original location, action, content summary, reason, destination.

## Workflow

```
User request → Infer execution mode → Confirm/lock outline → Writing Contract
→ Fat phase (per-chapter expansion + source ledger)
→ [interactive: pause for confirmation]
→ Slim phase (per-chapter + cross-chapter editing + action log)
→ Final draft + unresolved items
→ Deliver
```

## Output Structure

```
outputs/
├── fat/
│   ├── chapter-01.md
│   ├── chapter-02.md
│   └── source-ledger.md
└── slim/
    ├── slim-review.md
    ├── final.md
    └── unresolved-items.md
```

- `source-ledger.md`: every key fact, case, data point, or citation has a record
- `slim-review.md`: every significant edit has action, reason, and destination
- `final.md`: the final draft, no residual tags
- `unresolved-items.md`: items still needing user confirmation or external verification

## Boundaries

### Must Do

- Fat phase: never judge material quality, only pile and tag
- Slim phase: record every significant edit with action, reason, and destination
- Cross-chapter audit is mandatory, not optional
- Maintain source ledger during Fat
- Final draft must not contain `[素材]`, `[待查]`, `[待定]` markers
- Final draft must not cite material tagged `[待查]` without marking as unconfirmed

### Must Not Do

- Do not skip Fat and write final draft directly
- Do not start slimming during Fat phase
- Do not delete core arguments even if they seem imperfect
- Do not fabricate statistics, citations, or external references
- Do not handle style normalization or series consistency (hand off to series-style-governor)
- Do not handle personal writing style fitting (hand off to personal-formal-writing-style)
- Do not handle citation format management (hand off to citation-manager)

## Handoff

This skill is the content production engine in the writing skill pipeline:

```
research-note / citation-manager
        ↓ (materials & sources)
fat-slim-writer
        ↓ (final content)
personal-formal-writing-style / series-style-governor
        ↓ (styled output)
markdown-writer / document-packager
```

See `references/handoff-with-other-writing-skills.md` for detailed handoff rules.
