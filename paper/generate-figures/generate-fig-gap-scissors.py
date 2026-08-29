#!/usr/bin/env python3
"""
Figure (Introduction): the declarative-evaluative gap, behavioral, by family.

Declarative vs evaluative accuracy across scale, one small-multiple panel per
family, the gap shaded between the two lines and labeled in points. The Pythia
12B crossover -- where the gap closes because declarative accuracy *regresses*
to meet evaluative -- is annotated. Behavior only; the uncertainty side of the
gap lives in the fluent-wrongness raincloud (Section 4).

Reads:  results/analysis/{pythia,gpt2,olmo}_gap.csv
Writes: paper/figures/gap-scissors.png

Run:  python paper/generate-figures/generate-fig-gap-scissors.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from _figstyle import ANALYSIS_DIR, FIGURES_DIR, DECL_COLOR, EVAL_COLOR, OKABE, apply_style
import matplotlib.pyplot as plt
import pandas as pd

apply_style()
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

FAMILIES = [
    ("pythia", "Pythia", ["160M", "410M", "1B", "2.8B", "6.9B", "12B"]),
    ("gpt2",   "GPT-2",  ["124M", "355M", "774M", "1.5B"]),
    ("olmo",   "OLMo 2", ["1B", "7B", "13B"]),
]


def make_figure():
    fig, axes = plt.subplots(1, 3, figsize=(13, 4.6),
                             gridspec_kw={"width_ratios": [6, 4, 3]})

    for ax, (suite, label, scales) in zip(axes, FAMILIES):
        g = pd.read_csv(ANALYSIS_DIR / f"{suite}_gap.csv")
        assert len(g) == len(scales), (suite, len(g))
        x = range(len(scales))
        decl = g["declarative_pct"].values
        evl = g["evaluative_pct"].values

        ax.fill_between(x, evl, decl, color=OKABE["grey"], alpha=0.13,
                        zorder=1, interpolate=True)
        ax.plot(x, decl, color=DECL_COLOR, lw=2.6, zorder=4, label="Declarative")
        ax.scatter(x, decl, color=DECL_COLOR, s=58, zorder=5)
        ax.plot(x, evl, color=EVAL_COLOR, lw=2.6, ls="--", zorder=4, label="Evaluative")
        ax.scatter(x, evl, color=EVAL_COLOR, s=58, zorder=5, marker="s")

        for xi, d, e in zip(x, decl, evl):
            ax.annotate(f"{d - e:+.0f}", (xi, (d + e) / 2), fontsize=8, color="#555",
                        ha="center", va="center",
                        bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none", alpha=0.7))

        ax.set_xticks(list(x))
        ax.set_xticklabels(scales, fontsize=9.5)
        ax.set_ylim(0, 82)
        ax.set_title(label, fontsize=12, pad=10, fontweight="bold")
        ax.set_xlabel("Model size", fontsize=10, labelpad=6)
        if suite == "pythia":
            ax.set_ylabel("Accuracy (%)", fontsize=11, labelpad=8)
            ax.annotate("declarative regresses,\ngap closes at 12B",
                        xy=(5, 47), xytext=(3.15, 71), fontsize=8.5, color="#333",
                        ha="left", va="center",
                        arrowprops=dict(arrowstyle="->", color="#888", lw=1.1))

    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, fontsize=11, frameon=False, loc="lower center",
               ncol=2, bbox_to_anchor=(0.5, -0.03))
    fig.tight_layout(rect=[0, 0.03, 1, 1])
    out = FIGURES_DIR / "gap-scissors.png"
    fig.savefig(out, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {out}")


if __name__ == "__main__":
    make_figure()
