#!/usr/bin/env python3
"""
Figure: The declarative-evaluative gap, behavioral and internal.

Top row  -- declarative vs evaluative ACCURACY across scale (the behavioral gap).
Bottom row -- declarative vs evaluative ENTROPY across scale (the internal gap).
Columns are the three families: Pythia, GPT-2, and OLMo 2. The pairing shows
the gap is real in behavior AND mirrored by the model's own uncertainty, which
stays high on evaluative prompts even as declarative accuracy improves and
declarative entropy falls.

Reads:  results/analysis/pythia_gap.csv, gpt2_gap.csv, olmo_gap.csv,
        entropy_divergence.csv
Writes: paper/figures/gap-behavioral-internal.png

Run from anywhere:
    python paper/generate-figures/generate-fig-gap-behavioral-internal.py
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import pandas as pd
from pathlib import Path

SCRIPT_DIR   = Path(__file__).resolve().parent
PROJECT_DIR  = SCRIPT_DIR.parent.parent
ANALYSIS_DIR = PROJECT_DIR / "results" / "analysis"
FIGURES_DIR  = PROJECT_DIR / "paper" / "figures"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

# Okabe-Ito colorblind-safe palette (matplotlib)
okabe_ito = {
    "purple":    "#CC79A7",
    "blue":      "#0072B2",
    "skyblue":   "#56B4E9",
    "green":     "#009E73",
    "yellow":    "#F0E442",
    "orange":    "#E69F00",
    "red":       "#D55E00",
}

# Paper-wide meaning: blue/skyblue = the declarative/evaluative pair.
DECL_COLOR = okabe_ito["blue"]      # declarative: solid
EVAL_COLOR = okabe_ito["skyblue"]   # evaluative: dashed

available_fonts = [f.name for f in fm.fontManager.ttflist]
FONT = "Atkinson Hyperlegible" if "Atkinson Hyperlegible" in available_fonts else "DejaVu Sans"
plt.rcParams.update({
    "font.family":       FONT,
    "axes.spines.top":   False,
    "axes.spines.right": False,
    "figure.facecolor":  "white",
    "axes.facecolor":    "white",
})

FAMILIES = [
    (
        "pythia",
        "Pythia", 
        "pythia_gap.csv", [
            "160M", 
            "410M", 
            "1B", 
            "2.8B", 
            "6.9B", 
            "12B"
         ]
     ),
    (
        "gpt2", 
        "GPT-2", 
        "gpt2_gap.csv", [
            "124M", 
            "355M", 
            "774M", 
            "1.5B"
            ]
        ),
    (
        "olmo", 
        "OLMo 2", 
        "olmo_gap.csv", [
            "1B", 
            "7B", 
            "13B"
            ]
        ),
]


def _gap_line(ax, scales, declarative, evaluative, ylabel, fill_color):
    x = range(len(scales))
    ax.fill_between(x, evaluative, declarative,
                    color=fill_color, alpha=0.15, zorder=1, interpolate=True)
    ax.plot(x, declarative, color=DECL_COLOR, linewidth=2.5, zorder=4, label="Declarative")
    ax.scatter(x, declarative, color=DECL_COLOR, s=55, zorder=5)
    ax.plot(x, evaluative, color=EVAL_COLOR, linewidth=2.5, linestyle="--",
            zorder=4, label="Evaluative")
    ax.scatter(x, evaluative, color=EVAL_COLOR, s=55, zorder=5)
    ax.set_xticks(list(x))
    ax.set_xticklabels(scales, fontsize=9.5)
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=10, labelpad=8)


def make_figure():
    ent = pd.read_csv(ANALYSIS_DIR / "entropy_divergence.csv")

    fig, axes = plt.subplots(2, 3, figsize=(14, 8))

    for col, (suite, label, gap_file, scales) in enumerate(FAMILIES):
        gap = pd.read_csv(ANALYSIS_DIR / gap_file)
        e = (ent[ent.suite == suite]
             .set_index("scale").reindex(scales).reset_index())
        assert len(gap) == len(scales), (suite, len(gap))
        assert not e["declarative_entropy"].isna().any(), (suite, "entropy scales")

        _gap_line(axes[0][col], scales, gap["declarative_pct"], gap["evaluative_pct"],
                  "Accuracy (%)" if col == 0 else None, EVAL_COLOR)
        axes[0][col].set_ylim(0, 80)
        axes[0][col].set_title(f"{label} — behavioral gap",
                               fontsize=11, color="#333333", pad=8)

        _gap_line(axes[1][col], scales,
                  e["declarative_entropy"], e["evaluative_entropy"],
                  "Last-token entropy (nats)" if col == 0 else None, DECL_COLOR)
        axes[1][col].set_title(f"{label} — internal uncertainty gap",
                               fontsize=11, color="#333333", pad=8)
        axes[1][col].set_xlabel("Model size (parameters)", fontsize=10, labelpad=8)

    handles, labels = axes[0][0].get_legend_handles_labels()
    fig.legend(handles, labels, fontsize=11, frameon=False,
               loc="lower center", ncol=2, bbox_to_anchor=(0.5, -0.02))

    fig.tight_layout(rect=[0, 0.04, 1, 1])
    out = FIGURES_DIR / "gap-behavioral-internal.png"
    fig.savefig(out, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {out}")


if __name__ == "__main__":
    make_figure()
