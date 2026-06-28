#!/usr/bin/env python3
"""
Figure: The declarative-evaluative gap, behavioral and internal.

Top row  — declarative vs evaluative ACCURACY across scale (the behavioral gap).
Bottom row — declarative vs evaluative ENTROPY across scale (the internal gap).
Columns are the two suites. The pairing shows the gap is real in behavior AND
mirrored by the model's own uncertainty, which stays high on evaluative prompts
even as declarative accuracy improves and declarative entropy falls.

Reads:  results/analysis/pythia_gap.csv, gpt2_gap.csv, entropy_divergence.csv
Writes: paper/figures/gap-behavioral-internal.png

Run from anywhere:
    python generate-figures/generate-fig-gap-behavioral-internal.py
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import pandas as pd
from pathlib import Path

SCRIPT_DIR   = Path(__file__).resolve().parent
PROJECT_DIR  = SCRIPT_DIR.parent
ANALYSIS_DIR = PROJECT_DIR / "results" / "analysis"
FIGURES_DIR  = PROJECT_DIR / "paper" / "figures"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

NAVY       = "#08306b"
LIGHT_BLUE = "#6baed6"

available_fonts = [f.name for f in fm.fontManager.ttflist]
FONT = "Atkinson Hyperlegible" if "Atkinson Hyperlegible" in available_fonts else "DejaVu Sans"
plt.rcParams.update({
    "font.family":       FONT,
    "axes.spines.top":   False,
    "axes.spines.right": False,
    "figure.facecolor":  "white",
    "axes.facecolor":    "white",
})

PYTHIA_SCALES = ["160M", "410M", "1B", "2.8B", "6.9B", "12B"]
GPT2_SCALES   = ["124M", "355M", "774M", "1.5B"]


def _gap_line(ax, scales, declarative, evaluative, ylabel, fill_color):
    x = range(len(scales))
    ax.fill_between(x, evaluative, declarative,
                    color=fill_color, alpha=0.15, zorder=1, interpolate=True)
    ax.plot(x, declarative, color=NAVY, linewidth=2.5, zorder=4, label="Declarative")
    ax.scatter(x, declarative, color=NAVY, s=55, zorder=5)
    ax.plot(x, evaluative, color=LIGHT_BLUE, linewidth=2.5, linestyle="--",
            zorder=4, label="Evaluative")
    ax.scatter(x, evaluative, color=LIGHT_BLUE, s=55, zorder=5)
    ax.set_xticks(list(x))
    ax.set_xticklabels(scales, fontsize=9.5)
    ax.set_ylabel(ylabel, fontsize=10, labelpad=8)


def make_figure():
    pg = pd.read_csv(ANALYSIS_DIR / "pythia_gap.csv")
    gg = pd.read_csv(ANALYSIS_DIR / "gpt2_gap.csv")
    ent = pd.read_csv(ANALYSIS_DIR / "entropy_divergence.csv")

    pe = ent[ent.suite == "pythia"].set_index("scale").reindex(PYTHIA_SCALES).reset_index()
    ge = ent[ent.suite == "gpt2"].set_index("scale").reindex(GPT2_SCALES).reset_index()

    fig, axes = plt.subplots(2, 2, figsize=(11, 8))

    # Row 0: accuracy
    _gap_line(axes[0][0], PYTHIA_SCALES, pg["declarative_pct"], pg["evaluative_pct"],
              "Accuracy (%)", LIGHT_BLUE)
    axes[0][0].set_ylim(0, 80)
    axes[0][0].set_title("Pythia — behavioral gap", fontsize=11, color="#333333", pad=8)

    _gap_line(axes[0][1], GPT2_SCALES, gg["declarative_pct"], gg["evaluative_pct"],
              "Accuracy (%)", LIGHT_BLUE)
    axes[0][1].set_ylim(0, 80)
    axes[0][1].set_title("GPT-2 — behavioral gap", fontsize=11, color="#333333", pad=8)

    # Row 1: entropy
    _gap_line(axes[1][0], PYTHIA_SCALES, pe["declarative_entropy"], pe["evaluative_entropy"],
              "Last-token entropy (nats)", NAVY)
    axes[1][0].set_title("Pythia — internal uncertainty gap", fontsize=11, color="#333333", pad=8)
    axes[1][0].set_xlabel("Model size (parameters)", fontsize=10, labelpad=8)

    _gap_line(axes[1][1], GPT2_SCALES, ge["declarative_entropy"], ge["evaluative_entropy"],
              "Last-token entropy (nats)", NAVY)
    axes[1][1].set_title("GPT-2 — internal uncertainty gap", fontsize=11, color="#333333", pad=8)
    axes[1][1].set_xlabel("Model size (parameters)", fontsize=10, labelpad=8)

    handles, labels = axes[0][0].get_legend_handles_labels()
    fig.legend(handles, labels, fontsize=11, frameon=False,
               loc="lower center", ncol=2, bbox_to_anchor=(0.5, -0.02))

    fig.suptitle("The model behaves as if it knows the gap it cannot close",
                 fontsize=13, fontweight="bold", y=1.0)

    fig.tight_layout(rect=[0, 0.04, 1, 0.98])
    out = FIGURES_DIR / "gap-behavioral-internal.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {out}")


if __name__ == "__main__":
    make_figure()
