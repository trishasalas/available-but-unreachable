#!/usr/bin/env python3
"""
Figure: Per-concept scaling trajectories.

Heatmap of accuracy score (0 incorrect / 1 partial / 2 correct) for every concept
across every scale, faceted by suite. Concepts are grouped by trajectory type so
the three shapes read at a glance: monotonic climb, peak-and-regress (inverse
scaling at the top — watch keyboard navigation and skip link go dark at 12B), and
never-emerges (ARIA flat at zero throughout).

Reads:  results/analysis/per_concept_trajectories.csv
Writes: paper/figures/concept-trajectories.png

Run from anywhere:
    python generate-figures/generate-fig-concept-trajectories.py
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.colors import ListedColormap, BoundaryNorm
from matplotlib.patches import Patch
import numpy as np
import pandas as pd
from pathlib import Path

SCRIPT_DIR   = Path(__file__).resolve().parent
PROJECT_DIR  = SCRIPT_DIR.parent
ANALYSIS_DIR = PROJECT_DIR / "results" / "analysis"
FIGURES_DIR  = PROJECT_DIR / "paper" / "figures"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

# Discrete 3-level palette for ordinal accuracy (incorrect / partial / correct)
INCORRECT = "#e8eaf0"   # pale
PARTIAL   = "#6baed6"   # light blue
CORRECT   = "#08306b"   # navy
CMAP = ListedColormap([INCORRECT, PARTIAL, CORRECT])
NORM = BoundaryNorm([-0.5, 0.5, 1.5, 2.5], CMAP.N)

available_fonts = [f.name for f in fm.fontManager.ttflist]
FONT = "Atkinson Hyperlegible" if "Atkinson Hyperlegible" in available_fonts else "DejaVu Sans"
plt.rcParams.update({
    "font.family":       FONT,
    "figure.facecolor":  "white",
    "axes.facecolor":    "white",
})

PYTHIA_SCALES = ["160M", "410M", "1B", "2.8B", "6.9B", "12B"]
GPT2_SCALES   = ["124M", "355M", "774M", "1.5B"]

# Order trajectory groups so the story flows top -> bottom
TRAJ_ORDER = ["monotonic_climb", "mixed", "peak_regress", "never_emerges"]
TRAJ_LABEL = {
    "monotonic_climb": "climb",
    "mixed":           "mixed",
    "peak_regress":    "peak/regress",
    "never_emerges":   "never",
}


def _panel(ax, df, suite, scales, show_concept_labels):
    sub = df[df.suite == suite].copy()
    # Stable ordering: by trajectory group, then concept name
    sub["traj_rank"] = sub["trajectory"].map({t: i for i, t in enumerate(TRAJ_ORDER)})
    sub = sub.sort_values(["traj_rank", "concept"]).reset_index(drop=True)

    matrix = sub[scales].astype(float).values
    concepts = sub["concept"].tolist()
    trajs = sub["trajectory"].tolist()

    ax.imshow(matrix, cmap=CMAP, norm=NORM, aspect="auto")

    ax.set_xticks(range(len(scales)))
    ax.set_xticklabels(scales, fontsize=9.5, rotation=0)
    ax.set_yticks(range(len(concepts)))
    if show_concept_labels:
        ax.set_yticklabels(
            [f"{c}  ({TRAJ_LABEL[t]})" for c, t in zip(concepts, trajs)],
            fontsize=9.5,
        )
    else:
        ax.set_yticklabels([])

    # Cell value labels, readable on either background
    for r in range(matrix.shape[0]):
        for c in range(matrix.shape[1]):
            v = matrix[r, c]
            txt = "—" if np.isnan(v) else str(int(v))
            color = "white" if (v == 2) else "#333333"
            ax.text(c, r, txt, ha="center", va="center", fontsize=9, color=color)

    # Thin separators between trajectory groups
    boundaries = [i for i in range(1, len(trajs)) if trajs[i] != trajs[i - 1]]
    for b in boundaries:
        ax.axhline(b - 0.5, color="#999999", linewidth=1.0)

    ax.set_xticks(np.arange(-0.5, len(scales), 1), minor=True)
    ax.set_yticks(np.arange(-0.5, len(concepts), 1), minor=True)
    ax.grid(which="minor", color="white", linewidth=1.5)
    ax.tick_params(which="minor", length=0)


def make_figure():
    df = pd.read_csv(ANALYSIS_DIR / "per_concept_trajectories.csv")

    fig, (ax1, ax2) = plt.subplots(
        1, 2, figsize=(12, 6),
        gridspec_kw={"width_ratios": [len(PYTHIA_SCALES), len(GPT2_SCALES)], "wspace": 0.08},
    )

    _panel(ax1, df, "pythia", PYTHIA_SCALES, show_concept_labels=True)
    ax1.set_title("Pythia", fontsize=12, color="#333333", pad=10)

    _panel(ax2, df, "gpt2", GPT2_SCALES, show_concept_labels=False)
    ax2.set_title("GPT-2", fontsize=12, color="#333333", pad=10)

    legend_handles = [
        Patch(facecolor=INCORRECT, edgecolor="#cccccc", label="0  incorrect"),
        Patch(facecolor=PARTIAL,   label="1  partial"),
        Patch(facecolor=CORRECT,   label="2  correct"),
    ]
    fig.legend(handles=legend_handles, fontsize=10, frameon=False,
               loc="lower center", ncol=3, bbox_to_anchor=(0.5, -0.04))

    fig.suptitle("Concepts do not share one emergence curve",
                 fontsize=13, fontweight="bold", y=1.0)

    fig.tight_layout(rect=[0, 0.03, 1, 0.97])
    out = FIGURES_DIR / "concept-trajectories.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {out}")


if __name__ == "__main__":
    make_figure()
