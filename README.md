# Contract-Driven Harness — Publication Support

This branch contains the paper, supporting experiments, code, prompts, and reproduction verification data for:

> **Contracts as Task Skeleton: Externalizing Implicit Obligations for Bounded LLM-Agent Determinism**

## Quick Navigation

| What you need | Where |
|---|---|
| **Read the paper** | `paper/contract-driven-harness-arxiv-v5.1-draft.md` (v5 draft preserved) |
| **View figures** | `paper/figures/` |
| **Bibliography** | `paper/contract-driven-harness-references.bib` |
| **Reproduce experiments** | See [Reproduction Guide](#reproduction-guide) below |
| **Verify our claims** | `data/reproduction/` (4 rounds, 1458 API calls) |
| **Inspect frozen prompts** | `data/frozen-artifacts/real-run-artifacts/` (529 runs × prompt/output/metrics) |
| **Framework-agnostic core** | `code/reference-core/contract_core.py` |
| **Audit oracle coupling** | `code/runners/oracle-coupling/` |
| **Inspect audit evidence** | `data/reproduction/oracle-coupling/` |

## Repository Structure

```
├── paper/                                  # Paper, figures, and supporting documents
│   ├── contract-driven-harness-arxiv-v5.1-draft.md   # Latest draft (adds §4.14 oracle-coupling audit)
│   ├── contract-driven-harness-arxiv-v5-draft.md     # V5 draft (preserved)
│   ├── contract-driven-harness-arxiv-v4-frozen.md    # V4 frozen body (preserved)
│   ├── contract-driven-harness-references.bib        # Bibliography (20+ entries)
│   ├── ai-use-disclosure.md                          # AI assistance disclosure
│   ├── glossary.md                                   # 15+ term definitions
│   ├── v5-decisions-log.md                           # Decision record D1-D7
│   ├── v5-reframe-and-scope-limit.md                 # Essence reframe text
│   ├── methodology-sections-draft.md                 # §3.4-3.5 drafts
│   └── figures/                                      # Rendered publication figures
│       ├── figure-1-multi-model-pass-rates.{pdf,png}
│       ├── figure-2-repair-loop-convergence.{pdf,png}
│       ├── figure-3-stage-d-overhead.{pdf,png}
│       ├── figure-4-stage-progression.{drawio,pdf,png}
│       └── figure-oracle-coupling-audit.{pdf,png,svg}
│
├── code/                                   # All executable code
│   ├── reference-core/                               # Framework-agnostic core (MIT)
│   │   ├── contract_core.py                          # 260-line reference implementation
│   │   ├── README.md
│   │   └── LICENSE
│   └── runners/                                      # Experiment runner scripts
│       ├── oracle-coupling/                          # Causal policy-source and commit-boundary audits
│       ├── verify_stage_b_v54_live.py               # Live API verification runner
│       ├── run_full_experiment.py                   # Full-provenance runner (Stage B + D)
│       ├── rerun_all_frozen.py                      # Round 03: bare API re-run of all prompts
│       ├── rerun_via_petfishframework.py            # Round 04: petfishframework pipeline
│       ├── equivalence_pf_vs_lc.py                  # TOST equivalence test
│       ├── verify_zero_petfish_dep.py               # Framework independence checker
│       ├── generate_paper_figures.py                # Figure generation from data
│       ├── diagnose_glm_paraphrase.py              # GLM failure mode diagnostic
│       └── [60+ build/evaluate/postprocess scripts]
│
├── data/                                   # All experiment data
│   ├── frozen-artifacts/                             # Original V4 experiment data
│   │   └── real-run-artifacts/                       # 529 runs, each with prompt.md + output.md + metrics.json
│   ├── reproduction/                                 # 4-round reproduction campaign (1458 API calls)
│   │   ├── oracle-coupling/                           # Deterministic causal-audit evidence
│   │   └── experiment-rounds/
│   │       ├── round-01-author-verification-20260727/  # 240 runs (bare API)
│   │       ├── round-02-full-reproducibility/          # 240 runs (full provenance)
│   │       ├── round-03-full-history/                  # 469 runs (all frozen prompts)
│   │       ├── round-04-precise-petfishframework/      # 509 runs (Agent+ReAct, sim=1.0)
│   │       ├── _comparison-round-01-vs-02.md
│   │       └── README.md
│   ├── author-verification/                          # Multi-model verified results
│   │   └── records/                                  # 5 models × 40 runs + summary.csv
│   ├── kimi-replication/                             # Kimi Agent raw data
│   │   └── kimi-automated-replication/               # Full-trace automated replication
│   └── analysis/                                    # Key analysis documents
│       ├── multi-model-verification-analysis.md      # §4.10 analysis
│       ├── stage-d-overhead-analysis.md              # §4.13 analysis
│       ├── contract-evolution-ledger.md              # Appendix E
│       ├── stage-d-overhead-matrix.json             # Cost matrix data
│       ├── table-2-experiment-overview.csv           # Table 4 data
│       └── figure-2-convergence-data.csv            # Figure 2 data
│
├── fixtures/                               # Task definitions and contract specifications
│   ├── oracle-coupling/                              # Fixed inputs for the causal audits
│   ├── frozen-protocol-spec-v1.md                    # Frozen protocol specification
│   ├── [mechanism atoms, macros, perturbations]     # Task fixtures for all stages
│   └── [provider configs, benchmark matrices]
│
├── literature/                             # Related work and source materials
│   ├── closely-related-work-differentiation.md      # vs AgentSpec/ABC
│   ├── source-index.md                               # Source registry
│   └── scholar/                                      # 18 literature search CSVs
│
├── assets/
│   └── repair-loop-architecture.png                 # Repair-loop flow diagram
│
├── .gitignore
└── README.md                               # This file
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

python code/runners/verify_stage_b_v54_live.py \
    --model qwen3-8b \
    --output results.json
```

Expected: 40/40 strict passes, Wilson [0.912, 1.000].

### Full Multi-Model Verification (3 hours, ~¥30)

```bash
python code/runners/verify_stage_b_v54_live.py \
    --all-models \
    --output-dir results/
```

Expected: Qwen3-8B 40/40, GLM-4-9B ~30/40, Qwen3-14B ~40/40, DeepSeek-V3.2 40/40, Qwen2.5-7B 0/40.

### Stage D Cost Comparison (1 hour)

```bash
python code/runners/run_full_experiment.py stage-d \
    --models qwen3-8b deepseek-v3.2 \
    --output-dir results/stage-d
```

Expected: G0 0/20, G9 40/40 on both models.

### Complete History Reproduction (4-8 hours)

Re-run ALL 529 frozen prompts through the original petfishframework pipeline:

```bash
python code/runners/rerun_via_petfishframework.py \
    --output-dir results/round-pf
```

Expected: Stage B v5.4 sim=1.0 (bit-exact reproduction).

### Evaluating Your Own Output

```python
import sys
sys.path.insert(0, "code/reference-core")

from contract_core import ContractHarness, parse_json_output
import json

reference = json.load(open(
    "data/frozen-artifacts/real-run-artifacts/"
    "stage-b-v54-explicit-delta-stability/"
    "stage-b-v54-delta-stability--canonical__budget_model__G9__r1/output.md"
))

harness = ContractHarness(reference)
result = harness.evaluate_raw(your_model_output)
print(f"Strict pass: {result.strict_pass}, Failed: {result.failed_checks}")
```

## Oracle-Coupling Audit

The added audit asks a different question from the model-performance campaign:
does an executable policy come from public task facts, or from the answer later
used to score the run?

The authored-oracle FEC-v2 compiler matched all 28 task labels and all 392 frozen
candidate classifications, but deleting its expected answer prevented 28/28
compilations and poisoning answer-derived authorization fields changed 28/28
contracts. A separate public-input compiler reproduced the same finite corpus
without runtime access to `expected_output` or the preselected evidence fields
excluded by its allowlist. It remained invariant in 112/112 grounded
metamorphic conditions and failed closed in 55/55 authority perturbations
nested within 13 initially allowed tasks.

Two additional controls bound the interpretation. A pinned Invariant evaluator
kept six of six fixed-input label groups unchanged while responding to two of
two public-trace edits and two of two policy-source edits across 18 isolated,
zero-model calls. File and SQLite adapters then tested post-acceptance state
binding and recorded their residual pathname and same-user trust assumptions.

These are exact deterministic counts, not independent population samples. The
public-input compiler was developed after seeing three task grammars; the
external evaluator exercise is a boundary control, not an independent
replication of the audited FEC-v2 coupling pattern. Task and split identifiers
and grammar-family metadata remain fixed, and authority sensitivity is tested
only from apply to block, not through block-to-apply repair. Unseen-grammar
transfer, independent policy authorship, and complete mediation remain
unestablished.

Rebuild the deterministic artifacts and rerun their tests in dependency order:

```bash
python -m unittest discover \
  -s code/runners/oracle-coupling/failure_to_executable_contract_v2/tests -v
python code/runners/oracle-coupling/failure_to_executable_contract_v2/run_offline_verification.py \
  --fixtures fixtures/oracle-coupling/failure_to_executable_contract_v2.json \
  --output-dir data/reproduction/oracle-coupling/failure_to_executable_contract_v2
python code/runners/oracle-coupling/failure_to_executable_contract_v2/build_artifact_manifest.py
python -m unittest discover \
  -s code/runners/oracle-coupling/oracle_independent_compiler_v1/tests -v
python code/runners/oracle-coupling/oracle_independent_compiler_v1/run_experiment.py
python code/runners/oracle-coupling/metamorphic_public_input_v1/run_experiment.py
python code/runners/oracle-coupling/hardened_state_adapter_v1/run_experiment.py
python -m unittest discover \
  -s code/runners/oracle-coupling/second_harness_audit_v1/tests -v
python code/runners/oracle-coupling/second_harness_audit_v1/run_audit.py
python code/runners/oracle-coupling/invariant_external_boundary_v1/run_experiment.py
python code/runners/oracle-coupling/verify_all.py
```

The external Invariant control additionally requires the pinned source and
dependency paths described in its README.

### Platform Requirements

- **Artifact verification** (`verify_all.py` and all six `SHA256_MANIFEST.json`
  closures) runs on any OS with Python 3.12+ and git. The manifests hash raw
  file bytes, so the audited trees must stay LF in the working tree; this is
  enforced by `eol=lf` rules in `.gitattributes`. Clones made before those
  rules existed should re-normalize: `git rm -r --cached . && git checkout -- .`
  (or re-clone) before verifying.
- **Test suites by platform:**
  - `failure_to_executable_contract_v2`, `second_harness_audit_v1`,
    `oracle_independent_compiler_v1`, `metamorphic_public_input_v1`: run on
    Windows, macOS, and Linux. Manifest path classification uses POSIX path
    semantics by convention, so failure labels are identical on every OS.
  - `hardened_state_adapter_v1`: POSIX only. The audited check-to-commit
    mechanism depends on `fcntl` advisory locks, mode-bit permission gates,
    and directory `fsync`. On non-POSIX hosts the 21 adapter tests skip
    gracefully at class level (the 2 manifest-closure tests still run); a
    POSIX environment (Linux, macOS, or WSL) is required to execute the full
    suite, and to re-freeze its manifest after any change to its covered
    files.
  - `invariant_external_boundary_v1`: any OS, but requires the pinned external
    source and dependency roots (see its README; configurable via
    `INVARIANT_SOURCE_ROOT` / `INVARIANT_DEPS_ROOT`).
- The frozen artifacts embed the original authoring environment (timestamps,
  Python/SQLite versions, platform strings). Byte-identical regeneration is
  neither expected nor required; the supported reproduction model is
  freeze-and-verify — the manifest hashes must match the committed files.
  The OIC-v1 and MPIV1 manifests were re-ledgered after a cross-platform
  classification fix in their verifiers; the frozen result artifacts are
  unchanged.

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

- Code: MIT (see `code/reference-core/LICENSE`)
- Paper: Author retains copyright
- Experiment data: Provided for reproducibility verification only
