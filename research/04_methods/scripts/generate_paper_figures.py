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

    fig, ax = plt.subplots(figsize=(7, 4.2))
    fig.subplots_adjust(top=0.74, bottom=0.12)

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

    ax.set_yticks(y_pos)
    ax.set_yticklabels([m[0] for m in models])
    ax.set_xlabel("Strict Pass Rate (40 runs)")
    ax.set_xlim(0, 1.15)
    ax.set_ylim(-0.6, 4.6)
    ax.xaxis.set_major_formatter(mticker.PercentFormatter(xmax=1.0))
    ax.axvline(x=0.912, color="#90A4AE", linestyle="--", linewidth=0.8, zorder=1)

    ax.invert_yaxis()

    # Title — explicitly centered
    fig.suptitle("Pass Rates Under a Frozen Contract Across 5 Models",
                 x=0.5, ha="center", fontsize=13, y=0.96)

    # Legend — centered below title, with generous gap
    above_patch = mpatches.Patch(color=COLOR_ABOVE, label="Above-floor models")
    below_patch = mpatches.Patch(color=COLOR_BELOW, label="Below-floor model")
    fig.legend(handles=[above_patch, below_patch], loc="upper center",
               bbox_to_anchor=(0.5, 0.90), ncol=2, fontsize=9, frameon=True, edgecolor="#cccccc")

    # Dashed line note — centered below legend, with clear gap
    fig.text(0.5, 0.82, "Dashed line: Wilson 95% lower bound at 0.912",
             ha="center", va="top", fontsize=8, color="#78909C")

    fig.savefig(OUTPUT_DIR / "figure-1-multi-model-pass-rates.pdf", bbox_inches="tight")
    fig.savefig(OUTPUT_DIR / "figure-1-multi-model-pass-rates.png", bbox_inches="tight")
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

    fig, axes = plt.subplots(1, 3, figsize=(10, 3.8))

    # Shared legend handles — placed ONCE below suptitle, above subplots
    g0_patch = mpatches.Patch(color=COLOR_G0, label="G0 (no contract)")
    g9_patch = mpatches.Patch(color=COLOR_G9, label="G9 (full contract)")
    fig.legend(handles=[g0_patch, g9_patch], loc="upper center",
               bbox_to_anchor=(0.5, 0.93), ncol=2, fontsize=9, frameon=True, edgecolor="#cccccc")

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
    # No per-subplot legend — shared legend is above subplots

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
    # No per-subplot legend

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
    # No per-subplot legend

    for i, (g0, g9) in enumerate(zip(g0_lat, g9_lat)):
        ax.text(i - width / 2, g0 + 1.5, f"{g0:.0f}s", ha="center", fontsize=8)
        ax.text(i + width / 2, g9 + 1.5, f"{g9:.0f}s", ha="center", fontsize=8)

    fig.suptitle("Stage D: Contract Stack Converts 0% → 100% at 8.6× Prompt Cost", fontsize=12, y=0.99)
    fig.tight_layout(rect=(0, 0, 1, 0.88))
    fig.savefig(OUTPUT_DIR / "figure-3-stage-d-overhead.pdf")
    fig.savefig(OUTPUT_DIR / "figure-3-stage-d-overhead.png")
    plt.close(fig)
    print("Figure 3: Stage D overhead ✓")


# ── Figure 4: Experimental Stage Progression ────────────────────────────────

def figure_4_stage_progression():
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(-1.5, 11)
    ax.set_ylim(-0.5, 11)
    ax.axis("off")
    ax.set_title("Experimental Progression: From Atoms to Multi-Model Stability", fontsize=13, pad=25)

    # Phase labels — moved to LEFT margin to avoid crossing arrows
    phase_labels = [
        (0, 8.0, "Phase 1:\nMechanism Atoms\n& Composition", "#1565C0"),
        (0, 4.8, "Phase 2:\nContract Evolution\n& Stability", "#E65100"),
        (0, 1.5, "Phase 3:\nCross-Model\n& Cost Verification", "#6A1B9A"),
    ]
    for x, y, text, color in phase_labels:
        ax.text(x, y, text, ha="left", va="center", fontsize=8, fontweight="bold",
                color=color, rotation=0,
                bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor=color, alpha=0.9))

    # Stage boxes — wider spacing, no detail text below (moved inside boxes)
    stages = [
        # (x, y, w, h, label, runs+detail_combined, color)
        (1.8, 8.5, 1.8, 1.3, "Stage 6\nMechanism Atoms", "48 runs | §4.3\nA1-A10, G0/G2/G8/G9", "#BBDEFB"),
        (4.0, 8.5, 1.8, 1.3, "Stage 7p\nComposition", "12 runs | §4.4\nA10→A9→A6 macro", "#BBDEFB"),
        (6.2, 8.5, 1.8, 1.3, "Stage 7r\nRevised Atoms", "44 runs | §4.5\nA2R-A8R + smoke", "#BBDEFB"),
        (8.4, 8.5, 1.8, 1.3, "Stage 7e\nRepair Loop", "18 runs | §4.6\nv1→v4 iterations", "#C8E6C9"),

        (1.8, 5.3, 1.8, 1.3, "Stage 7-next\nNeighbor Transfer", "4 runs | §4.7\nmethod-plan macro", "#C8E6C9"),
        (4.0, 5.3, 2.2, 1.3, "Stage B v5→v5.3\nContract Evolution", "~68 runs | §4.8\nstate-transition repair", "#FFE0B2"),
        (6.6, 5.3, 2.0, 1.3, "Stage B v5.4\nFrozen Stability", "40×3 runs | §4.8\n40/40, Wilson [.912,1.0]", "#FFCC80"),

        (2.0, 2.0, 2.2, 1.3, "Multi-Model\nInterchangeability", "200×2 runs | §4.10\n40/40,40/40,40/40,30/40,0/40", "#E1BEE7"),
        (4.6, 2.0, 1.8, 1.3, "Stage D\nCost Matrix", "40×2 runs | §4.13\nG0 0%→G9 100%", "#E1BEE7"),
        (6.8, 2.0, 2.2, 1.3, "Reproducibility\n4 Rounds × 1458 calls", "§Appendix F\nv5.4 sim=1.0 (pf)", "#B3E5FC"),

        (4.0, 0.0, 3.5, 0.8, "Task Slices (§4.2)", "~50 runs: extraction, init, workflow | gap compression", "#F5F5F5"),
    ]

    for s in stages:
        x, y, w, h = s[0], s[1], s[2], s[3]
        label = s[4]
        detail = s[5]
        color = s[6]

        rect = mpatches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.12",
                                        facecolor=color, edgecolor="#78909C", linewidth=1.0)
        ax.add_patch(rect)
        ax.text(x + w / 2, y + h * 0.72, label, ha="center", va="center", fontsize=8, fontweight="bold")
        ax.text(x + w / 2, y + h * 0.28, detail, ha="center", va="center", fontsize=6.5, color="#546E7A")

    # Arrows — simplified routing, only horizontal + vertical (no curved arrows)
    arrow_kw = dict(arrowstyle="->", color="#78909C", lw=1.3)

    # Row 1 horizontal (Phase 1)
    ax.annotate("", xy=(4.0, 9.15), xytext=(3.6, 9.15), arrowprops=arrow_kw)
    ax.annotate("", xy=(6.2, 9.15), xytext=(5.8, 9.15), arrowprops=arrow_kw)
    ax.annotate("", xy=(8.4, 9.15), xytext=(8.0, 9.15), arrowprops=arrow_kw)

    # Row 1 → Row 2 (vertical drops, spread out)
    ax.annotate("", xy=(2.7, 6.6), xytext=(2.7, 8.5), arrowprops=arrow_kw)   # Stage 6 → 7-next
    ax.annotate("", xy=(5.1, 6.6), xytext=(5.1, 8.5), arrowprops=arrow_kw)   # 7p → B v5
    ax.annotate("", xy=(7.6, 6.6), xytext=(9.3, 8.5), arrowprops=arrow_kw)   # 7e → B v5.4 (diagonal)

    # Row 2 horizontal
    ax.annotate("", xy=(4.0, 5.95), xytext=(3.6, 5.95), arrowprops=arrow_kw)
    ax.annotate("", xy=(6.6, 5.95), xytext=(6.2, 5.95), arrowprops=arrow_kw)

    # Row 2 → Row 3 (vertical drops)
    ax.annotate("", xy=(3.1, 3.3), xytext=(3.1, 5.3), arrowprops=arrow_kw)   # Multi-model
    ax.annotate("", xy=(5.5, 3.3), xytext=(7.6, 5.3), arrowprops=arrow_kw)   # v5.4 → Stage D (diagonal)
    ax.annotate("", xy=(7.9, 3.3), xytext=(5.5, 5.3), arrowprops=arrow_kw)   # B → Reproducibility (diagonal)

    # Row 3 horizontal
    ax.annotate("", xy=(4.6, 2.65), xytext=(4.2, 2.65), arrowprops=arrow_kw)
    ax.annotate("", xy=(6.8, 2.65), xytext=(6.4, 2.65), arrowprops=arrow_kw)

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
