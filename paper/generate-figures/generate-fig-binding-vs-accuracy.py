#!/usr/bin/env python3
"""
Figure: Binding is not knowing.

Scatter of max attention-binding score (x) against behavioral accuracy score (y),
one point per compound per scale, colored by family. The point is the dense
vertical band at x ~ 1.0 spanning every accuracy level: binding saturates
regardless of whether the model understands the concept. Pearson/Spearman
correlations are annotated from binding_accuracy_corr.csv and asserted against
the values reported in the paper (GPT-2 0.087, Pythia -0.003, OLMo 0.115).

Reads:  results/analysis/binding_vs_accuracy.csv, binding_accuracy_corr.csv
Writes: paper/figures/binding-vs-accuracy.png

Run from anywhere:
    python paper/generate-figures/generate-fig-binding-vs-accuracy.py
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
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

# Paper-wide meaning: families are orange / purple / green.
SUITE_COLOR = {
    "pythia": okabe_ito["orange"],
    "gpt2": okabe_ito["purple"],
    "olmo": okabe_ito["green"],
}
SUITE_LABEL = {"pythia": "Pythia", "gpt2": "GPT-2", "olmo": "OLMo 2"}
SUITES = ["pythia", "gpt2", "olmo"]

# Paper-reported Pearson correlations; the script refuses to draw if the
# data on disk disagrees with the prose.
EXPECTED_PEARSON = {"gpt2": 0.087, "pythia": -0.003, "olmo": 0.115}

available_fonts = [f.name for f in fm.fontManager.ttflist]
FONT = "Atkinson Hyperlegible" if "Atkinson Hyperlegible" in available_fonts else "DejaVu Sans"
plt.rcParams.update({
    "font.family":       FONT,
    "axes.spines.top":   False,
    "axes.spines.right": False,
    "figure.facecolor":  "white",
    "axes.facecolor":    "white",
})

# Deterministic vertical jitter so overlapping points at each accuracy level
# spread out (accuracy is the ordinal 0/1/2; jitter is cosmetic only).
RNG = np.random.default_rng(0)


def make_figure():
    bv = pd.read_csv(ANALYSIS_DIR / "binding_vs_accuracy.csv")
    corr = pd.read_csv(ANALYSIS_DIR / "binding_accuracy_corr.csv").set_index("suite")

    for suite in SUITES:
        assert suite in corr.index, f"missing correlations for {suite}"
        assert abs(corr.loc[suite, "pearson_r"] - EXPECTED_PEARSON[suite]) < 1e-6, (
            suite, corr.loc[suite, "pearson_r"], EXPECTED_PEARSON[suite],
        )
        n_scatter = int((bv.suite == suite).sum())
        assert n_scatter == int(corr.loc[suite, "n_pairs"]), (
            suite, n_scatter, int(corr.loc[suite, "n_pairs"]),
        )

    fig, ax = plt.subplots(figsize=(9, 5.5))

    for suite in SUITES:
        sub = bv[bv.suite == suite]
        jitter = RNG.uniform(-0.28, 0.28, size=len(sub))
        ax.scatter(sub["max_binding"], sub["accuracy_score"] + jitter,
                   s=40, alpha=0.6, color=SUITE_COLOR[suite],
                   edgecolor="white", linewidth=0.5,
                   label=SUITE_LABEL[suite], zorder=3)

    ax.set_yticks([0, 1, 2])
    ax.set_yticklabels(["incorrect (0)", "partial (1)", "correct (2)"], fontsize=10)
    ax.set_ylim(-0.45, 2.6)
    x_lo = min(0.65, float(bv["max_binding"].min()) - 0.02)
    ax.set_xlim(x_lo, 1.02)
    ax.set_xlabel("Max attention-binding score", fontsize=10, labelpad=8)
    ax.set_ylabel("Behavioral accuracy", fontsize=10, labelpad=8)

    ax.legend(fontsize=11, frameon=False, loc="upper left",
              bbox_to_anchor=(0.0, 1.0))

    fig.tight_layout()
    out = FIGURES_DIR / "binding-vs-accuracy.png"
    fig.savefig(out, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {out}")


if __name__ == "__main__":
    make_figure()
