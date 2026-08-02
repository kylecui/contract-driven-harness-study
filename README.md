# Contract-Driven Harness — Publication Support

This branch contains the paper, supporting experiments, code, prompts, and reproduction verification data for:

> **Contracts as Task Skeleton: Externalizing Implicit Obligations for Bounded LLM-Agent Determinism**

## Quick Navigation

| What you need | Where |
|---|---|
| **Read the paper** | `research/06_outputs/contract-driven-harness-arxiv-v5-draft.md` |
| **View figures** | `research/06_outputs/figures/` |
| **Bibliography** | `research/06_outputs/contract-driven-harness-references.bib` |
| **Reproduce experiments** | See [Reproduction Guide](#reproduction-guide) below |
| **Verify our claims** | `research/05_analysis/experiment-rounds/` (4 rounds, 1458 API calls) |
| **Inspect frozen prompts** | `research/05_analysis/real-run-artifacts/` (529 runs × prompt/output/metrics) |
| **Framework-agnostic core** | `reference-core/contract_core.py` |

## Repository Structure

```
├── research/
│   ├── 06_outputs/                         # Paper and figures
│   │   ├── contract-driven-harness-arxiv-v5-draft.md    # Latest paper
│   │   ├── contract-driven-harness-arxiv-v4-frozen.md   # V4 frozen body (preserved)
│   │   ├── contract-driven-harness-references.bib       # Bibliography
│   │   ├── figures/                                     # 4 rendered figures
│   │   ├── glossary.md                                  # 15+ term definitions
│   │   ├── v5-decisions-log.md                          # Decision record D1-D7
│   │   ├── v5-reframe-and-scope-limit.md                # Essence reframe text
│   │   └── methodology-sections-draft.md                # §3.4-3.5 drafts
│   │
│   ├── 04_methods/                         # Experiment code and fixtures
│   │   ├── scripts/                                     # All runner scripts
│   │   │   ├── verify_stage_b_v54_live.py               # Live API verification runner
│   │   │   ├── run_full_experiment.py                   # Full-provenance runner (Stage B + D)
│   │   │   ├── rerun_all_frozen.py                      # Round 03: bare API re-run
│   │   │   ├── rerun_via_petfishframework.py            # Round 04: petfishframework pipeline
│   │   │   ├── equivalence_pf_vs_lc.py                  # TOST equivalence test
│   │   │   ├── verify_zero_petfish_dep.py               # Framework independence checker
│   │   │   ├── generate_paper_figures.py                # Figure generation from data
│   │   │   └── diagnose_glm_paraphrase.py              # GLM failure mode diagnostic
│   │   ├── frozen-protocol-spec-v1.md                   # Frozen protocol specification
│   │   └── [mechanism atoms, macros, perturbations]    # Task fixtures
│   │
│   ├── 05_analysis/                        # Experiment data and results
│   │   ├── real-run-artifacts/                          # Frozen V4 experiment data
│   │   │                                                # 529 runs, each with prompt.md + output.md + metrics.json
│   │   ├── experiment-rounds/                           # 4-round reproduction campaign
│   │   │   ├── round-01-author-verification-20260727/   # 240 runs (bare API)
│   │   │   ├── round-02-full-reproducibility/           # 240 runs (full provenance)
│   │   │   ├── round-03-full-history/                   # 469 runs (all frozen prompts)
│   │   │   ├── round-04-precise-petfishframework/       # 509 runs (Agent+ReAct, sim=1.0)
│   │   │   ├── _comparison-round-01-vs-02.md            # Inter-round comparison
│   │   │   └── README.md                                # Rounds index
│   │   ├── author-confirmation-records/                 # Verified multi-model data
│   │   ├── multi-model-verification-analysis.md         # §4.10 analysis
│   │   ├── stage-d-overhead-analysis.md                 # §4.13 analysis
│   │   ├── contract-evolution-ledger.md                 # Appendix E
│   │   ├── table-2-experiment-overview.csv              # Table 4 data
│   │   └── figure-2-convergence-data.csv                # Figure 2 data
│   │
│   ├── 01_sources/                         # External sources and Kimi data
│   │   ├── kimi-automated-replication/                  # Kimi Agent raw data
│   │   ├── closely-related-work-differentiation.md      # vs AgentSpec/ABC
│   │   └── literature-search/scholar/                   # 18 literature CSVs
│   │
│   ├── 07_reviews/
│   │   └── ai-use-disclosure.md                         # AI assistance disclosure
│   │
│   └── CONTEXT.md
│
├── reference-core/                         # Framework-agnostic implementation
│   ├── contract_core.py                                # 260-line reference core
│   ├── README.md
│   └── LICENSE                                         # MIT
│
└── assets/
    └── repair-loop-architecture.png
```

## Reproduction Guide

### Prerequisites

- Python 3.10+
- SiliconFlow API key (or any OpenAI-compatible endpoint)
- `petfishframework` v1.1.0 (`pip install petfishframework[openai]`)

### Quick Verification (30 minutes, ~¥3)

Reproduce the paper's headline result (Stage B v5.4 on Qwen3-8B):

```bash
export OPENAI_API_KEY=your_siliconflow_key
export OPENAI_BASE_URL=https://api.siliconflow.cn/v1

python research/04_methods/scripts/verify_stage_b_v54_live.py \
    --model qwen3-8b \
    --output results.json
```

Expected: 40/40 strict passes, Wilson [0.912, 1.000].

### Full Multi-Model Verification (3 hours, ~¥30)

```bash
python research/04_methods/scripts/verify_stage_b_v54_live.py \
    --all-models \
    --output-dir results/
```

Expected: Qwen3-8B 40/40, GLM-4-9B ~30/40, Qwen3-14B ~40/40, DeepSeek-V3.2 40/40, Qwen2.5-7B 0/40.

### Stage D Cost Comparison (1 hour)

```bash
python research/04_methods/scripts/run_full_experiment.py stage-d \
    --models qwen3-8b deepseek-v3.2 \
    --output-dir results/stage-d
```

Expected: G0 0/20, G9 40/40 on both models.

### Complete History Reproduction (4-8 hours)

Re-run ALL 529 frozen prompts through the original petfishframework pipeline:

```bash
python research/04_methods/scripts/rerun_via_petfishframework.py \
    --output-dir results/round-pf
```

Expected: Stage B v5.4 sim=1.0 (bit-exact reproduction).

### Evaluating Your Own Output

```python
from reference_core.contract_core import ContractHarness, parse_json_output
import json

reference = json.load(open(
    "research/05_analysis/real-run-artifacts/"
    "stage-b-v54-explicit-delta-stability/"
    "stage-b-v54-delta-stability--canonical__budget_model__G9__r1/output.md"
))

harness = ContractHarness(reference)
result = harness.evaluate_raw(your_model_output)
print(f"Strict pass: {result.strict_pass}, Failed: {result.failed_checks}")
```

## Claim Verification Matrix

| Paper Claim | Section | Data Source | Reproduced |
|---|---|---|---|
| Qwen3-8B 40/40 [0.912, 1.000] | §4.8 | R01+R02+R04 | ✅ 3 rounds |
| GLM-4-9B 30/40 paraphrase vulnerability | §4.10 | R01+R02 | ✅ 2 rounds |
| Qwen3-14B 40/40 | §4.10 | R01+R02 | ✅ 2 rounds |
| DeepSeek-V3.2 40/40 | §4.10 | R01+R02 | ✅ 2 rounds |
| Qwen2.5-7B 0/40 structural floor | §4.12 | R01+R02 | ✅ 2 rounds |
| G0 0% → G9 100% | §4.13 | R01+R02 | ✅ 2 rounds |
| Repair-loop 0→40/40 trajectory | §4.8 | R04 | ✅ sim=0.82→1.0 |
| v5.4 bit-exact reproducible | App. F | R04 | ✅ sim=1.0 |

## License

- Code: MIT (see `reference-core/LICENSE`)
- Paper: Author retains copyright
- Experiment data: Provided for reproducibility verification only
