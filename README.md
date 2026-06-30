# petfish4codex-test4fun

Academic research workspace initialized for Codex with PEtFiSh.

## Purpose

This project is prepared for academic research workflows: framing research questions, discovering sources, capturing notes, building evidence ledgers, synthesizing findings, and writing reviewable outputs.

## Workspace Map

- `research/` - Research brief, sources, notes, evidence, methods, analysis, outputs, reviews, and ADRs.
- `docs/` - Project overview and supporting documentation.
- `tasks/` - Backlog and roadmap.
- `qa/` - Research quality and evidence review checklists.
- `.agents/` - Installed PEtFiSh skill registry and local skills.

## Installed PEtFiSh Packs

- `companion` - PEtFiSh routing, status, and marketplace companion.
- `petfish` - Engineering writing style support.
- `doc-reader` - Document-to-Markdown conversion.
- `research` - Research workbench skills.

## Getting Started

1. Define the research goal in `research/CONTEXT.md`.
2. Add the first research tasks in `tasks/backlog.md`.
3. Start source discovery from `research/01_sources/`.
4. Record claims in `research/03_evidence/` before writing conclusions.

## Latest Stage B Reproduction

Run the local method tests:

```powershell
# Tests live under research/04_methods/scripts and only import siblings,
# so they run from the scripts directory.
cd research/04_methods/scripts
python -m unittest discover -p "test_*.py"
```

Regenerate the frozen v5.4 analysis from retained outputs:

```powershell
# Run from the repository root, not from scripts/.
# Scripts import siblings by bare module name, so PYTHONPATH must include the scripts dir.
$env:PYTHONPATH = "research/04_methods/scripts"

python research/04_methods/scripts/evaluate_stage_b_v53_explicit_transition_delta.py `
  --fixtures-dir research/04_methods/macro-explicit-transition-delta-stage-b-v53 `
  --manifest research/05_analysis/real-run-artifacts/stage-b-v54-explicit-delta-stability-manifest-with-prompts.json `
  --output-runs research/05_analysis/stage-b-v54-explicit-delta-stability-results.json `
  --output-md research/05_analysis/stage-b-v54-explicit-delta-stability-results.md

python research/04_methods/scripts/analyze_stage_b_v54_delta_stability.py `
  --evaluated-runs research/05_analysis/stage-b-v54-explicit-delta-stability-results.json `
  --execution research/05_analysis/stage-b-v54-explicit-delta-stability-execution.json `
  --output-json research/05_analysis/stage-b-v54-explicit-delta-stability-analysis.json `
  --output-md research/05_analysis/stage-b-v54-explicit-delta-stability-analysis.md
```

## Paper Drafts

- Frozen v3.1.1 PDF:
  `research/06_outputs/contract-driven-harness-paper-v3.1.1-frozen.pdf`
- Frozen V4 evidence-extension source:
  `research/06_outputs/contract-driven-harness-arxiv-v4-frozen.md`
- Frozen V4 reader PDF:
  `research/06_outputs/contract-driven-harness-paper-v4-frozen.pdf`
- Reader-facing V4 presentation PDF:
  `research/06_outputs/contract-driven-harness-paper-v4-presentation-draft.pdf`
- Reader-facing V4 presentation source:
  `research/06_outputs/contract-driven-harness-arxiv-v4-presentation-draft.md`
- V4 LaTeX source package:
  `research/06_outputs/arxiv-source-v4/`
- V4 presentation LaTeX source package:
  `research/06_outputs/arxiv-source-v4-presentation/`

V4 adds the Stage B v5.2-v5.4 evidence. It reports the v5.3 causal
comparison as mixed and the separate v5.4 result as bounded absolute
stability: 40/40 fresh strict passes across five tested perturbations. The
body and empirical narrative were frozen on 2026-06-15. The presentation
derivative adds descriptive stage names without changing that frozen
empirical record.
