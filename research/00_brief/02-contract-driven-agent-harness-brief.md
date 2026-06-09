# Brief: Contract-Driven Agent Harness Engineering

## Research Type

Mixed scientific / software engineering research.

## One-Line Goal

Study whether stable agent harnesses can compress cross-model capability gaps in productivity tasks by externalizing workflows, tools, memory, contracts, and evaluation.

## Core Research Question

Under what task types and harness strengths can the output gap between stronger and weaker models be reduced to a smaller, observable, governable engineering gap?

## Working Thesis

The strongest thesis is:

> Harnesses do not erase model capability differences, but for tasks that are structured, toolable, and verifiable, contract-driven harness engineering can reduce model sensitivity and improve portability, auditability, and reliability.

## Existing Local Evidence

- `proposal/02-Contract-Driven_Agent_Harness_Engineering/early-study/constraint_harness_research_plan_V2.md` gives the current best formulation: stable harnesses compress model capability gaps in bounded productivity tasks.
- `proposal/02-Contract-Driven_Agent_Harness_Engineering/early-study/harness_engineering_survey.md` already surveys related systems and warns against overclaiming model-independence.
- `proposal/02-Contract-Driven_Agent_Harness_Engineering/early-study/petfish-ai-research.md` reframes PEtFiSh as a layered control system and recommends TaskSpec / EvidenceBundle / MemorySlice / OutputContract.

## Scope

Included:

- Coding, research, initialization, documentation, deployment, skill lifecycle, structured extraction, and other productivity tasks.
- Contracts, registries, workflows, MCP/tools, memory policy, validators, guardrails, trace/replay, and regression evals.
- Cross-model behavior and output consistency under fixed harness conditions.

Excluded:

- General claims that weak models equal strong models.
- Fully autonomous open-ended agents without task contracts.
- High-creativity or low-verifiability tasks as primary evidence.

## Recommended Research Framing

Use "Model Capability Gap Compression" as the measurable concept:

```text
Gap_baseline = PerformanceGap(models, prompt_only)
Gap_harness = PerformanceGap(models, full_harness)
CompressionRatio = 1 - Gap_harness / Gap_baseline
```

Report this by task class and harness layer, not as a single universal number.

## Key Risks

- Harness benefits may be model-specific, especially around memory and compaction.
- Over-strong workflows can reduce flexibility on open tasks.
- Contract drift across registry, installer, docs, prompts, and tests may become the real system failure mode.
- Structured outputs can enforce form without guaranteeing truth unless grounded evidence and validators are included.

