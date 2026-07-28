# Contract-Aware Companion Landing Synthesis

## Research Task Plan

- **research_type**: Mixed
- **primary_type**: Planning
- **secondary_types**: Product, Technology
- **complexity_level**: Full
- **recommended_skill_chain**: research-router -> planning-technology-assessor -> planning-roadmap-developer -> product-validation-planner -> research-synthesis -> research-report-writer -> research-quality-reviewer
- **expected_artifacts**:
  - Companion landing synthesis
  - 16-week implementation roadmap
  - milestone and dependency plan
  - MVP validation plan
  - independent quality review
- **key_risks**:
  - treating bounded paper evidence as production-readiness evidence;
  - exposing contract complexity to users;
  - retaining model-dependent routing inside an apparently deterministic control plane;
  - adding token and latency overhead without measurable task benefit;
  - creating schema drift across local packs, online Gateway, and platform adapters.

## Decision

The product entry should be Companion, not Quality Gate.

Companion already owns intent sensing, capability discovery, skill creation,
installation guidance, and governance communication. The online Gateway also
already has deterministic envelopes and an explicit execution-truth boundary.
This makes Companion the natural place to compile a user request into a
machine-readable work contract. Quality Gate, validators, and known-bad
regression remain downstream enforcement mechanisms. (Evidence: P2-E179,
P2-E180, P2-E181, P2-E182)

## Evidence-Bounded Findings

| Finding | Confidence | Evidence | Product implication |
|---|---|---|---|
| Contract-rich harnessing improves absolute adherence across tested task classes. | High for tested slices | P2-E27, P2-E29, P2-E31, P2-E33 | A Companion-generated contract can be tested as a reliability intervention. |
| Gap compression is conditional rather than universal. | High | P2-E28, P2-E30, P2-E32, P2-E33 | Do not market the feature as weak-model equivalence. Measure per-task contract success. |
| Missing obligations can be repaired through explicit contracts and known-bad regression. | High for bounded mechanisms | P2-E58, P2-E60, P2-E62, P2-E64, P2-E66, P2-E68 | Build failure classification and regression capture into the product workflow. |
| Repaired obligations transfer to a neighboring bounded macro. | Medium | P2-E72, P2-E74, P2-E75 | Start with adjacent Companion workflows rather than unrelated task families. |
| One frozen explicit-delta protocol was stable across 40 fresh runs. | High for the frozen protocol | P2-E169, P2-E170, P2-E171, P2-E172 | State transitions should be represented explicitly, but the result does not validate arbitrary workflow state. |
| Companion already contains part of a control plane. | High | P2-E179, P2-E180, P2-E181 | Extend existing Companion and Gateway surfaces instead of creating a separate product. |

## Target Product Model

```text
User request
  -> Companion sensing
  -> hybrid Contract Compiler
  -> ContractEnvelope
       - TaskSpec
       - CapabilityPlan
       - MemorySlice
       - EvidenceBundle
       - OutputContract
       - Risk/Approval policy
       - StageGate
  -> model/skill/MCP adapter
  -> deterministic validators
  -> user-facing Companion explanation
  -> failure classification and repair regression
```

The compiler should be hybrid:

1. Deterministic inputs provide commands, installed packs, registry metadata,
   project mode, runtime type, permissions, and known policy.
2. A model-assisted step may draft intent and ambiguous fields.
3. Deterministic normalization validates names, allowed tools, schemas, and
   blocked actions.
4. User confirmation is required only for uncertain or high-impact fields.

This structure avoids pretending that natural-language intent parsing is fully
deterministic while keeping execution obligations outside free-form generation.

## Implementation Repository Baseline

Implementation must target `kylecui/petfish.ai`, using its `master` branch and
current repository structure as the source of truth. The inspected baseline is
commit `348b7b75a5c27067e7e99f5f814a8d28328dd125`.

This research workspace supplies method artifacts, evidence, fixtures, and the
landing plan. It must not become a second implementation source for Companion,
Gateway, catalog, schemas, or Quality Gate behavior.

## MVP Boundary

The first MVP should cover four bounded Companion workflows:

1. capability and skill discovery;
2. skill creation planning;
3. skill validation and publication decision;
4. installation command preview.

Actual remote installation, arbitrary filesystem mutation, deployment,
concurrent tool execution, and rollback are excluded from the first release.

## Maturity Assessment

| Component | Current maturity | Basis | Next gate |
|---|---:|---|---|
| Research schemas and fixtures | TRL 4 | Local schemas, compiled packets, 52 current method tests | Extract stable v0.1 product schemas |
| Deterministic validators and known-bad gates | TRL 5 | Repeated local gates and model-backed repair loops | Generalize from research fixtures to Companion workflows |
| Companion sensing and capability discovery | TRL 5-6 | Existing fish-brain, catalog query, registries, profiles | Return structured CapabilityPlan |
| Online execution-truth boundary | TRL 5 | Existing deterministic envelope and preview-only contract | Integrate ContractEnvelope references |
| User-facing Contract Card | TRL 2 | Product concept only | Test usability in advisory mode |
| Live side-effecting contract execution | TRL 2 | Current paper excludes live tools and rollback | Defer until post-beta reliability work |

## Recommended Verdict

**Pilot Only**, with Companion as the user-facing control plane and Contract
Mode initially operating in shadow and advisory modes.

Promotion to enforced execution requires evidence from real Companion tasks,
cross-model runs, user correction rates, latency and token overhead, and
execution-truth audits. The paper's 40/40 result is a method input, not the
production acceptance test.
