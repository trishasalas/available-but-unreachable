#!/usr/bin/env python3
"""
Figure: Binding is not knowing.

Scatter of max attention-binding score (x) against behavioral accuracy score (y),
one point per compound per scale, colored by suite. The point is the dense vertical
band at x ~ 1.0 spanning every accuracy level: binding saturates regardless of
whether the model understands the concept. Pearson/Spearman correlations annotated
from binding_accuracy_corr.csv confirm binding does not predict accuracy.

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

NAVY       = "#08306b"
LIGHT_BLUE = "#6baed6"
SUITE_COLOR = {"pythia": NAVY, "gpt2": LIGHT_BLUE}
SUITE_LABEL = {"pythia": "Pythia", "gpt2": "GPT-2"}

available_fonts = [f.name for f in fm.fontManager.ttflist]
FONT = "Atkinson Hyperlegible" if "Atkinson Hyperlegible" in available_fonts else "DejaVu Sans"
plt.rcParams.update({
    "font.family":       FONT,
    "axes.spines.top":   False,
    "axes.spines.right": False,
    "figure.facecolor":  "white",
    "axes.facecolor":    "white",
})

# Deterministic vertical jitter so overlapping points at each accuracy level spread
# out (accuracy is the ordinal 0/1/2; jitter is cosmetic only).
RNG = np.random.default_rng(0)


def make_figure():
    bv = pd.read_csv(ANALYSIS_DIR / "binding_vs_accuracy.csv")
    corr = pd.read_csv(ANALYSIS_DIR / "binding_accuracy_corr.csv").set_index("suite")

    fig, ax = plt.subplots(figsize=(9, 5.5))

    for suite in ["pythia", "gpt2"]:
        sub = bv[bv.suite == suite]
        jitter = RNG.uniform(-0.12, 0.12, size=len(sub))
        ax.scatter(sub["max_binding"], sub["accuracy_score"] + jitter,
                   s=60, alpha=0.7, color=SUITE_COLOR[suite],
                   edgecolor="white", linewidth=0.5,
                   label=SUITE_LABEL[suite], zorder=3)

    ax.set_yticks([0, 1, 2])
    ax.set_yticklabels(["incorrect (0)", "partial (1)", "correct (2)"], fontsize=10)
    ax.set_ylim(-0.4, 2.4)
    ax.set_xlim(0.65, 1.02)
    ax.set_xlabel("Max attention-binding score", fontsize=10, labelpad=8)
    ax.set_ylabel("Behavioral accuracy", fontsize=10, labelpad=8)

    # Correlation annotation box
    lines = ["Binding does not predict accuracy:"]
    for suite in ["pythia", "gpt2"]:
        r = corr.loc[suite]
        lines.append(
            f"  {SUITE_LABEL[suite]}: r = {r['pearson_r']:.2f}  "
            f"(ρ = {r['spearman_r']:.2f}, n = {int(r['n_pairs'])})"
        )
    ax.text(0.66, 2.3, "\n".join(lines), fontsize=9.5, color="#444444",
            va="top", ha="left", linespacing=1.5,
            bbox=dict(boxstyle="round,pad=0.5", facecolor="#f5f6fa",
                      edgecolor="#cccccc", linewidth=0.8))

    ax.legend(fontsize=11, frameon=False, loc="lower left",
              bbox_to_anchor=(0.0, 0.02))

    fig.suptitle("Strong binding is present even when the concept is absent",
                 fontsize=13, fontweight="bold", y=0.99)

    fig.tight_layout(rect=[0, 0, 1, 0.97])
    out = FIGURES_DIR / "binding-vs-accuracy.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {out}")


if __name__ == "__main__":
    make_figure()
