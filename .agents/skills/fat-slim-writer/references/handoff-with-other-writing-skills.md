# Handoff with Other Writing Skills

## Responsibility Boundary

`fat-slim-writer` is responsible for content production: taking an outline and materials through expansion and reduction to produce a final draft.

It should NOT replace the following skills:

| Skill | Responsibility |
|---|---|
| series-style-governor | Unify style, naming, layout, and terminology across a series of documents |
| personal-formal-writing-style | Adapt output to a specific person's formal writing style |
| markdown-writer | Ensure Markdown structure, formatting, and rendering quality |
| research-note | Extract notes, quotations, sources, and research evidence |
| citation-manager | Validate citations and reference format |

## Handoff Rules

### Upstream (into fat-slim-writer)

- If the user asks to write new long-form content, start with `fat-slim-writer`.
- If the user provides raw research materials, suggest running `research-note` first to organize sources before entering Fat phase.
- If the user has citation-heavy requirements, ensure `citation-manager` is available for the final delivery stage.

### Downstream (out of fat-slim-writer)

- If the user asks to unify multiple existing articles, hand off to `series-style-governor` after Fat-Slim completes individual pieces.
- If the user asks to match a specific personal writing style, hand off to `personal-formal-writing-style` after Slim phase produces the final draft.
- If the user asks for final formatting, hand off to `markdown-writer` for structure and rendering quality.

### Parallel (not to be combined)

- Do not run `fat-slim-writer` and `series-style-governor` simultaneously — content production must complete before style unification.
- Do not use `fat-slim-writer` for short-form tasks that other skills handle better.

## Pipeline Position

```
research-note / citation-manager
        ↓ (organized materials & sources)
fat-slim-writer
        ↓ (final content draft)
personal-formal-writing-style / series-style-governor
        ↓ (styled, consistent output)
markdown-writer / document-packager
        ↓ (formatted deliverable)
```
