#!/usr/bin/env python3
"""
Figure 2 (Section 4): the per-model paired-battery collapse.

One dumbbell per model: declarative pair-concepts passed (filled, family color)
vs evaluative PAIR passes (hollow). Every confirmatory model collapses to zero
evaluative pair-passes regardless of how much it knows declaratively; only the
development-exposed Pythia-2.8B pilot clears one. Companion to Figure 3 (the full
cell grid).

Reads:  results/analysis/paired_gap_summary.csv
Writes: paper/figures/paired-collapse.png

Run:  python paper/generate-figures/generate-fig-paired-collapse.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from _figstyle import ANALYSIS_DIR, FIGURES_DIR, FAMILY_COLOR, OKABE, apply_style
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import pandas as pd

apply_style()
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

PARAMS = {"124M": 0.124, "160M": 0.16, "355M": 0.355, "410M": 0.41, "774M": 0.774,
          "1B": 1.0, "1.5B": 1.5, "2.8B": 2.8, "6.9B": 6.9, "7B": 7.0, "12B": 12.0, "13B": 13.0}
FAM_ORDER = [("pythia", "Pythia"), ("gpt2", "GPT-2"), ("olmo", "OLMo 2")]


def make_figure():
    s = pd.read_csv(ANALYSIS_DIR / "paired_gap_summary.csv")
    s["p"] = s["scale"].map(PARAMS)

    # Build row order: family blocks (Pythia, GPT-2, OLMo), ascending scale within.
    rows, ylabels, y = [], [], 0.0
    ypos = []
    block_tops = {}
    for suite, _ in FAM_ORDER:
        block = s[s.suite == suite].sort_values("p")
        block_tops[suite] = y + len(block) - 1
        for _, r in block.iterrows():
            rows.append(r); ypos.append(y); ylabels.append(r["scale"]); y += 1
        y += 1.0  # gap between families

    n = len(rows)
    fig, ax = plt.subplots(figsize=(8.2, 6.2))
    total = int(rows[0]["n_concepts"])

    for r, yy in zip(rows, ypos):
        color = FAMILY_COLOR[r["suite"]]
        decl = int(r["declarative_passes"])
        evl = int(r["evaluative_pair_passes"])
        # connecting line = declarative knowledge that fails to apply
        ax.plot([evl, decl], [yy, yy], color="#cfcfcf", lw=2.2, zorder=1, solid_capstyle="round")
        ax.scatter(evl, yy, facecolor="white", edgecolor=color, s=55, lw=1.6, zorder=3)
        ax.scatter(decl, yy, color=color, s=80, zorder=4, edgecolor="white", lw=0.6)
        if r["is_pilot"]:
            ax.annotate("pilot (2.8B): the only\nevaluative pair-pass",
                        xy=(evl, yy), xytext=(3.4, yy + -1.19), fontsize=8, color="#333",
                        ha="left", va="center",
                        arrowprops=dict(arrowstyle="->", color="#888", lw=1.0))

    # zero wall
    ax.axvline(0, color="#999", lw=1.0, ls=":", zorder=0)

    ax.set_yticks(ypos)
    ax.set_yticklabels(ylabels, fontsize=9)
    ax.set_ylim(-1, n + (len(FAM_ORDER) - 1) + 0.5)
    ax.invert_yaxis()
    ax.set_xlim(-0.4, total + 0.3)
    ax.set_xticks(range(0, total + 1))
    ax.set_xlabel(f"Concepts passed (of {total} paired concepts)", fontsize=10.5, labelpad=8)

    # family group labels
    for suite, label in FAM_ORDER:
        yy = min(p for p, r in zip(ypos, rows) if r["suite"] == suite)
        ax.text(-0.36, yy - 0.7, label, fontsize=10, fontweight="bold",
                color=FAMILY_COLOR[suite], va="center")

    ax.set_title("Per-model collapse: declarative knowledge present, evaluative application at zero",
                 fontsize=11.8, pad=12, color="#222")

    leg = [Line2D([0], [0], marker="o", color="w", markerfacecolor="#666", markersize=9,
                  label="Declarative pair-concepts passed"),
           Line2D([0], [0], marker="o", color="w", markerfacecolor="white",
                  markeredgecolor="#666", markersize=9, markeredgewidth=1.6,
                  label="Evaluative PAIR passes")]
    ax.legend(handles=leg, frameon=False, fontsize=9, loc="lower right")

    fig.tight_layout()
    out = FIGURES_DIR / "paired-collapse.png"
    fig.savefig(out, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {out} | models: {n}")


if __name__ == "__main__":
    make_figure()
