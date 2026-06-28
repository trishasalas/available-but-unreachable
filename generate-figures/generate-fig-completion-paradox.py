#!/usr/bin/env python3
"""
Figure: The completion paradox.

Few-shot completion accuracy (can the model produce correct `alt="..."` syntax?)
vs declarative accuracy (can it define the concept?) across scale, for alt text
and captions, faceted by suite. The story is the completion line pinned near the
top while the declarative line climbs from below to meet it: procedural competence
precedes conceptual competence.

Reads:  results/analysis/completion_paradox.csv
Writes: paper/figures/completion-paradox.png

Run from anywhere:
    python generate-figures/generate-fig-completion-paradox.py
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
SUITES        = [("pythia", "Pythia", PYTHIA_SCALES), ("gpt2", "GPT-2", GPT2_SCALES)]
CONCEPTS      = ["alt text", "captions"]


def make_figure():
    df = pd.read_csv(ANALYSIS_DIR / "completion_paradox.csv")

    fig, axes = plt.subplots(2, 2, figsize=(11, 8), sharey=True)

    for i, concept in enumerate(CONCEPTS):
        for j, (suite, suite_label, scales) in enumerate(SUITES):
            ax = axes[i][j]
            sub = (df[(df.suite == suite) & (df.concept == concept)]
                   .set_index("scale").reindex(scales).reset_index())
            x = range(len(scales))

            comp = sub["completion_pct"]
            decl = sub["declarative_pct"]

            # Shade the paradox gap (completion above declarative)
            ax.fill_between(x, decl, comp, where=(comp >= decl),
                            color=LIGHT_BLUE, alpha=0.18, zorder=1,
                            interpolate=True)

            ax.plot(x, comp, color=NAVY, linewidth=2.5, zorder=4,
                    label="Completion (syntax)")
            ax.scatter(x, comp, color=NAVY, s=55, zorder=5)

            ax.plot(x, decl, color=LIGHT_BLUE, linewidth=2.5, linestyle="--",
                    zorder=4, label="Declarative (definition)")
            ax.scatter(x, decl, color=LIGHT_BLUE, s=55, zorder=5)

            ax.set_xticks(list(x))
            ax.set_xticklabels(scales, fontsize=9.5)
            ax.set_ylim(-5, 108)
            ax.set_title(f"{concept} — {suite_label}", fontsize=11,
                         color="#333333", pad=8)
            if j == 0:
                ax.set_ylabel("Accuracy (%)", fontsize=10, labelpad=8)
            if i == len(CONCEPTS) - 1:
                ax.set_xlabel("Model size (parameters)", fontsize=10, labelpad=8)

    # Single shared legend
    handles, labels = axes[0][0].get_legend_handles_labels()
    fig.legend(handles, labels, fontsize=11, frameon=False,
               loc="lower center", ncol=2, bbox_to_anchor=(0.5, -0.02))

    fig.suptitle("The Completion Paradox: producing syntax before defining the concept",
                 fontsize=13, fontweight="bold", y=1.0)

    fig.tight_layout(rect=[0, 0.04, 1, 0.98])
    out = FIGURES_DIR / "completion-paradox.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {out}")


if __name__ == "__main__":
    make_figure()
