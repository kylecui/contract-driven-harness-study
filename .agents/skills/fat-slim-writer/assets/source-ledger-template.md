# Source Ledger

## Purpose

Track every key fact, case, data point, and citation used in the Fat draft. The Slim phase must update this ledger when material is deleted, merged, or relocated.

## Ledger

| ID | Type | Source | Supporting Chapter | Supporting Argument | Credibility | Status |
|---|---|---|---|---|---|---|
| S001 | user material | references/xxx.md | Chapter 2 | ... | high | used |
| S002 | pending check | search needed | Chapter 3 | ... | unknown | pending |
| S003 | inference | model reasoning | Chapter 4 | ... | medium | needs confirmation |

## Rules

- Every key fact, case, data point, or citation must have a source ledger record.
- Final draft must not cite material with status `pending` unless explicitly marked as unconfirmed.
- Slim phase must update status when material is deleted, merged, moved, or rewritten.

## Status Values

| Status | Meaning |
|---|---|
| used | Incorporated into Fat draft |
| pending | Needs verification before use in final draft |
| needs confirmation | Inferred, requires human review |
| deleted | Removed during Slim phase |
| relocated | Moved to appendix, footnote, or other chapter |
| merged | Combined with other material |
