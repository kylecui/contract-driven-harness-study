# Writing Contract Reference

## Purpose

Writing Contract defines the writing task before expansion starts. It prevents the agent from producing content with unclear audience, unclear document type, or unclear success criteria.

## Contract Fields

| Field | Required | Default | Notes |
|---|---|---|---|
| document_type | Yes | structured long-form article | book/chapter/whitepaper/report/course/thesis/article |
| audience | Yes | professional reader with basic background | expert/manager/student/customer/public |
| outcome | Yes | clear explanation and actionable conclusion | explain/persuade/plan/teach/archive |
| length_target | Optional | none | total length and per-section target |
| tone | Optional | formal, clear, restrained | formal/technical/strategic/teaching/oral |
| evidence_policy | Yes | distinguish verified facts, assumptions, and pending checks | whether citation or verification is required |

## Inference Rules

If the user provides enough context (e.g., "写一本给管理者的AI战略白皮书"), infer all fields silently without asking.

If context is ambiguous, ask at most 1-2 questions. Prioritize:
1. document_type (determines structure)
2. audience (determines depth and terminology)

Do not ask all 6 fields — that interrupts the user's flow.

## Default Contract

Use when the user does not provide enough information:

- document_type: structured long-form article
- audience: professional reader with basic background
- outcome: clear explanation and actionable conclusion
- tone: formal, clear, restrained
- evidence_policy: distinguish verified facts, assumptions, and pending checks; do not fabricate sources
