"""Generate all paper figures from verified experimental data.

Produces:
    Figure 1: Multi-model pass rates with Wilson 95% CI
    Figure 2: Repair-loop convergence curve (0/40 → 40/40)
    Figure 3: Stage D matched overhead (G0 vs G9)
    Figure 4: Experimental stage progression diagram

Output: research/06_outputs/figures/figure-{1-4}-{name}.{pdf,png}
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker as mticker
import numpy as np

OUTPUT_DIR = Path("research/06_outputs/figures")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ── Style ───────────────────────────────────────────────────────────────────

plt.rcParams.update({
    "font.size": 11,
    "font.family": "serif",
    "axes.labelsize": 12,
    "axes.titlesize": 13,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "legend.fontsize": 9,
    "figure.dpi": 300,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "axes.spines.top": False,
    "axes.spines.right": False,
})

COLOR_ABOVE = "#2196F3"
COLOR_BELOW = "#F44336"
COLOR_G0 = "#FF9800"
COLOR_G9 = "#4CAF50"
COLOR_CONVERGENCE = "#673AB7"
COLOR_ANNOTATION = "#607D8BF0"

# ── Figure 1: Multi-Model Pass Rates ────────────────────────────────────────

def wilson_interval(passes: int, total: int, z: float = 1.96) -> tuple[float, float]:
    if total == 0:
        return 0.0, 0.0
    n, p = total, passes / total
    denom = 1 + z * z / n
    center = (p + z * z / (2 * n)) / denom
    margin = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return max(0, center - margin), min(1, center + margin)


def figure_1_multi_model():
    models = [
        ("Qwen3-8B\n(8B)", 40, 40, "above"),
        ("DeepSeek-V3.2\n(MoE)", 40, 40, "above"),
        ("Qwen3-14B\n(14B)", 40, 40, "above"),
        ("GLM-4-9B\n(9B)", 40, 30, "above"),
        ("Qwen2.5-7B\n(7B)", 40, 0, "below"),
    ]

    fig, ax = plt.subplots(figsize=(7, 3.5))

    y_pos = np.arange(len(models))
    colors = [COLOR_ABOVE if m[3] == "above" else COLOR_BELOW for m in models]

    rates = [m[2] / m[1] for m in models]
    errors = []
    for m in models:
        lo, hi = wilson_interval(m[2], m[1])
        errors.append([m[2] / m[1] - lo, hi - m[2] / m[1]])

    errors = np.array(errors).T

    bars = ax.barh(y_pos, rates, color=colors, edgecolor="white", linewidth=0.5, height=0.6, zorder=2)
    ax.errorbar(rates, y_pos, xerr=errors, fmt="none", color="black", capsize=3, capthick=1, linewidth=1, zorder=3)

    # Labels on bars
    for i, m in enumerate(models):
        rate = m[2] / m[1]
        label = f"{m[2]}/{m[1]}" if m[2] != 0 else "0/40"
        if rate > 0.5:
            ax.text(rate - 0.05, i, label, ha="right", va="center", color="white", fontweight="bold", fontsize=10)
        else:
            ax.text(0.02, i, label, ha="left", va="center", color=COLOR_BELOW if m[3] == "below" else "black", fontweight="bold", fontsize=10)

    # GLM annotation
    glm_idx = 3
    ax.annotate("paraphrase\nvulnerability", xy=(0.75, glm_idx), xytext=(0.45, glm_idx + 0.5),
                fontsize=8, color="#D32F2F", ha="center",
                arrowprops=dict(arrowstyle="->", color="#D32F2F", lw=1.2))

    ax.set_yticks(y_pos)
    ax.set_yticklabels([m[0] for m in models])
    ax.set_xlabel("Strict Pass Rate (40 runs)")
    ax.set_xlim(0, 1.1)
    ax.xaxis.set_major_formatter(mticker.PercentFormatter(xmax=1.0))
    ax.axvline(x=0.912, color="#90A4AE", linestyle="--", linewidth=0.8, zorder=1)
    ax.text(0.912, -0.7, "Wilson lower\nbound 0.912", fontsize=7, color="#78909C", ha="center")

    # Legend
    above_patch = mpatches.Patch(color=COLOR_ABOVE, label="Above-floor models")
    below_patch = mpatches.Patch(color=COLOR_BELOW, label="Below-floor model")
    ax.legend(handles=[above_patch, below_patch], loc="lower right")

    ax.invert_yaxis()
    ax.set_title("Pass Rates Under a Frozen Contract Across 5 Models", pad=12)

    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "figure-1-multi-model-pass-rates.pdf")
    fig.savefig(OUTPUT_DIR / "figure-1-multi-model-pass-rates.png")
    plt.close(fig)
    print("Figure 1: multi-model pass rates ✓")


# ── Figure 2: Repair-Loop Convergence ───────────────────────────────────────

def figure_2_convergence():
    # Data from Kimi's v1→v5 trajectory + author verification
    iterations = ["v1\n(initial)", "v2\n(+evidence\n+enum)", "v3\n(+transition\nrecord)", "v4\n(+canonical\nnames)", "v5\n(+attestation\ncoverage)"]
    pass_rates = [0.0, 0.525, 0.525, 0.825, 1.0]
    passes = [0, 21, 21, 33, 40]
    total = 40

    fig, ax = plt.subplots(figsize=(7, 3.5))

    # Wilson CIs
    lo_vals, hi_vals = [], []
    for p in passes:
        lo, hi = wilson_interval(p, total)
        lo_vals.append(lo)
        hi_vals.append(hi)

    x = np.arange(len(iterations))

    # CI band
    ax.fill_between(x, lo_vals, hi_vals, alpha=0.15, color=COLOR_CONVERGENCE, zorder=1)

    # Main line
    ax.plot(x, pass_rates, "o-", color=COLOR_CONVERGENCE, linewidth=2, markersize=8, zorder=3)

    # Error bars
    errors = [[r - lo for r, lo in zip(pass_rates, lo_vals)],
              [hi - r for r, hi in zip(pass_rates, hi_vals)]]
    ax.errorbar(x, pass_rates, yerr=errors, fmt="none", color=COLOR_CONVERGENCE, capsize=3, linewidth=1, zorder=2)

    # Annotations for each step
    annotations = [
        "0/40\nNo obligations\ndeclared",
        "21/40\nExact evidence\n+ next_action\nenumeration",
        "21/40\nTransition record\nJSON structure",
        "33/40\nField-required\n+ canonical-name\nobligation",
        "40/40\nAttestation field\ncanonical-name\ncoverage",
    ]

    for i, (xi, rate, ann) in enumerate(zip(x, pass_rates, annotations)):
        offset = 0.12 if rate < 0.9 else -0.15
        va = "bottom" if rate < 0.9 else "top"
        ax.text(xi, rate + offset, ann, ha="center", va=va, fontsize=7, color="#37474F",
                bbox=dict(boxstyle="round,pad=0.2", facecolor="#ECEFF1", edgecolor="#CFD8DC", alpha=0.8))

    ax.set_xticks(x)
    ax.set_xticklabels(iterations, fontsize=9)
    ax.set_ylabel("Strict Pass Rate")
    ax.set_ylim(-0.08, 1.18)
    ax.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=1.0))
    ax.set_title("Repair-Loop Convergence: 0/40 → 40/40 Over Four Iterations", pad=12)

    # Arrow showing the trajectory
    ax.annotate("", xy=(4, 1.0), xytext=(0, 0.0),
                arrowprops=dict(arrowstyle="->", color="#BDBDBD", lw=1.5, connectionstyle="arc3,rad=0.1"),
                zorder=0)

    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "figure-2-repair-loop-convergence.pdf")
    fig.savefig(OUTPUT_DIR / "figure-2-repair-loop-convergence.png")
    plt.close(fig)
    print("Figure 2: repair-loop convergence ✓")


# ── Figure 3: Stage D Overhead Matrix ───────────────────────────────────────

def figure_3_stage_d():
    with open("research/05_analysis/stage-d-overhead-matrix.json") as f:
        data = json.load(f)

    models = ["qwen3-8b", "deepseek-v3.2"]
    model_labels = ["Qwen3-8B", "DeepSeek-V3.2"]

    fig, axes = plt.subplots(1, 3, figsize=(9, 3.5))

    # Panel A: Pass rate
    ax = axes[0]
    x = np.arange(len(models))
    width = 0.35
    g0_rates = [data[m]["G0"]["pass_rate"] for m in models]
    g9_rates = [data[m]["G9"]["pass_rate"] for m in models]
    ax.bar(x - width / 2, g0_rates, width, label="G0 (no contract)", color=COLOR_G0, edgecolor="white")
    ax.bar(x + width / 2, g9_rates, width, label="G9 (full contract)", color=COLOR_G9, edgecolor="white")
    ax.set_xticks(x)
    ax.set_xticklabels(model_labels)
    ax.set_ylabel("Pass Rate")
    ax.set_ylim(0, 1.25)
    ax.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=1.0))
    ax.set_title("(a) Pass Rate", fontsize=11)
    ax.legend(fontsize=8)

    for i, (g0, g9) in enumerate(zip(g0_rates, g9_rates)):
        ax.text(i - width / 2, g0 + 0.03, f"{g0:.0%}", ha="center", fontsize=8)
        ax.text(i + width / 2, g9 + 0.03, f"{g9:.0%}", ha="center", fontsize=8)

    # Panel B: Prompt tokens
    ax = axes[1]
    g0_tok = [data[m]["G0"]["avg_prompt_tokens"] for m in models]
    g9_tok = [data[m]["G9"]["avg_prompt_tokens"] for m in models]
    ax.bar(x - width / 2, g0_tok, width, label="G0", color=COLOR_G0, edgecolor="white")
    ax.bar(x + width / 2, g9_tok, width, label="G9", color=COLOR_G9, edgecolor="white")
    ax.set_xticks(x)
    ax.set_xticklabels(model_labels)
    ax.set_ylabel("Avg Prompt Tokens / Run")
    ax.set_title("(b) Prompt Cost", fontsize=11)
    ax.legend(fontsize=8)

    for i, (g0, g9) in enumerate(zip(g0_tok, g9_tok)):
        ax.text(i - width / 2, g0 + 30, str(g0), ha="center", fontsize=8)
        ax.text(i + width / 2, g9 + 30, str(g9), ha="center", fontsize=8)

    # Panel C: Latency
    ax = axes[2]
    g0_lat = [data[m]["G0"]["avg_latency_s"] for m in models]
    g9_lat = [data[m]["G9"]["avg_latency_s"] for m in models]
    ax.bar(x - width / 2, g0_lat, width, label="G0", color=COLOR_G0, edgecolor="white")
    ax.bar(x + width / 2, g9_lat, width, label="G9", color=COLOR_G9, edgecolor="white")
    ax.set_xticks(x)
    ax.set_xticklabels(model_labels)
    ax.set_ylabel("Avg Latency (s)")
    ax.set_title("(c) Latency", fontsize=11)
    ax.legend(fontsize=8)

    for i, (g0, g9) in enumerate(zip(g0_lat, g9_lat)):
        ax.text(i - width / 2, g0 + 1.5, f"{g0:.0f}s", ha="center", fontsize=8)
        ax.text(i + width / 2, g9 + 1.5, f"{g9:.0f}s", ha="center", fontsize=8)

    fig.suptitle("Stage D: Contract Stack Converts 0% → 100% at 8.6× Prompt Cost", fontsize=12, y=1.02)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "figure-3-stage-d-overhead.pdf")
    fig.savefig(OUTPUT_DIR / "figure-3-stage-d-overhead.png")
    plt.close(fig)
    print("Figure 3: Stage D overhead ✓")


# ── Figure 4: Experimental Stage Progression ────────────────────────────────

def figure_4_stage_progression():
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis("off")
    ax.set_title("Experimental Progression: From Atoms to Multi-Model Stability", fontsize=13, pad=20)

    # Define stages as boxes
    stages = [
        # (x, y, width, height, label, runs, color, section)
        (0.5, 7.5, 2.0, 1.2, "Stage 6\nMechanism Atoms", "48 runs\n§4.3", "#BBDEFB", "A1-A10 atoms\nG0/G2/G8/G9"),
        (3.0, 7.5, 2.0, 1.2, "Stage 7p\nComposition", "12 runs\n§4.4", "#BBDEFB", "A10→A9→A6\npartial macro"),
        (5.5, 7.5, 2.0, 1.2, "Stage 7r\nRevised Atoms", "44 runs\n§4.5", "#BBDEFB", "A2R-A8R +\ntargeted smoke"),
        (8.0, 7.5, 1.8, 1.2, "Stage 7e\nRepair Loop", "18 runs\n§4.6", "#C8E6C9", "v1→v4\nevidence-decision"),

        (0.5, 5.0, 2.0, 1.2, "Stage 7-next\nNeighbor Transfer", "4 runs\n§4.7", "#C8E6C9", "method-plan\nmacro"),
        (3.0, 5.0, 2.5, 1.2, "Stage B v5→v5.3\nContract Evolution", "~68 runs\n§4.8", "#FFE0B2", "state-transition\nrepair trajectory"),
        (6.0, 5.0, 2.0, 1.2, "Stage B v5.4\nFrozen Stability", "40×3 runs\n§4.8", "#FFCC80", "40/40 Qwen3-8B\nWilson [0.912,1.0]"),

        (1.0, 2.5, 2.5, 1.2, "Multi-Model\nInterchangeability", "200×2 runs\n§4.10", "#E1BEE7", "5 models\n40/40,40/40,40/40,\n30/40,0/40"),
        (4.0, 2.5, 2.0, 1.2, "Stage D\nCost Matrix", "40×2 runs\n§4.13", "#E1BEE7", "G0 0%→G9 100%\n8.6× token cost"),
        (6.5, 2.5, 2.5, 1.2, "Reproducibility\n4 Rounds × 1458 calls", "§5.2\n", "#B3E5FC", "v5.4 sim=1.0\n(petfishframework)"),

        (3.0, 0.3, 4.0, 1.0, "Stage 6 Task Slices (§4.2)", "~50 runs", "#F5F5F5", "structured extraction | project init | research workflow | gap compression"),
    ]

    # Draw boxes
    for s in stages:
        x, y, w, h = s[0], s[1], s[2], s[3]
        label = s[4]
        runs = s[5]
        color = s[6]
        detail = s[7] if len(s) > 7 else ""

        rect = mpatches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1",
                                        facecolor=color, edgecolor="#78909C", linewidth=1.2)
        ax.add_patch(rect)
        ax.text(x + w / 2, y + h * 0.65, label, ha="center", va="center", fontsize=8, fontweight="bold")
        ax.text(x + w / 2, y + h * 0.30, runs, ha="center", va="center", fontsize=7, color="#546E7A")
        if detail:
            ax.text(x + w / 2, y - 0.25, detail, ha="center", va="top", fontsize=6, color="#90A4AE")

    # Arrows showing flow
    arrow_kw = dict(arrowstyle="->", color="#546E7A", lw=1.5, connectionstyle="arc3,rad=0")

    # Row 1 horizontal flow
    ax.annotate("", xy=(3.0, 8.1), xytext=(2.5, 8.1), arrowprops=arrow_kw)
    ax.annotate("", xy=(5.5, 8.1), xytext=(5.0, 8.1), arrowprops=arrow_kw)
    ax.annotate("", xy=(8.0, 8.1), xytext=(7.5, 8.1), arrowprops=arrow_kw)

    # Row 1 → Row 2
    ax.annotate("", xy=(1.5, 6.2), xytext=(1.5, 7.5), arrowprops=arrow_kw)  # 6 → 7-next
    ax.annotate("", xy=(4.0, 6.2), xytext=(4.0, 7.5), arrowprops=arrow_kw)  # 7p → B
    ax.annotate("", xy=(8.9, 6.2), xytext=(8.9, 7.5), arrowprops=dict(arrowstyle="->", color="#546E7A", lw=1.5, connectionstyle="arc3,rad=-0.3"))

    # Row 2 horizontal
    ax.annotate("", xy=(3.0, 5.6), xytext=(2.5, 5.6), arrowprops=arrow_kw)
    ax.annotate("", xy=(6.0, 5.6), xytext=(5.5, 5.6), arrowprops=arrow_kw)

    # Row 2 → Row 3
    ax.annotate("", xy=(2.0, 3.7), xytext=(2.0, 5.0), arrowprops=arrow_kw)
    ax.annotate("", xy=(5.0, 3.7), xytext=(7.0, 5.0), arrowprops=dict(arrowstyle="->", color="#546E7A", lw=1.5, connectionstyle="arc3,rad=0.2"))

    # Row 3 horizontal
    ax.annotate("", xy=(4.0, 3.1), xytext=(3.5, 3.1), arrowprops=arrow_kw)
    ax.annotate("", xy=(6.5, 3.1), xytext=(6.0, 3.1), arrowprops=arrow_kw)

    # Phase labels
    ax.text(5.0, 9.2, "Phase 1: Mechanism Atoms & Composition", ha="center", fontsize=9, fontweight="bold", color="#1565C0")
    ax.text(5.0, 6.5, "Phase 2: Contract Evolution & Stability", ha="center", fontsize=9, fontweight="bold", color="#E65100")
    ax.text(5.0, 4.0, "Phase 3: Cross-Model & Cost Verification", ha="center", fontsize=9, fontweight="bold", color="#6A1B9A")

    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "figure-4-stage-progression.pdf")
    fig.savefig(OUTPUT_DIR / "figure-4-stage-progression.png")
    plt.close(fig)
    print("Figure 4: stage progression ✓")


# ── Main ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    figure_1_multi_model()
    figure_2_convergence()
    figure_3_stage_d()
    figure_4_stage_progression()
    print(f"\nAll figures saved to {OUTPUT_DIR}/")
