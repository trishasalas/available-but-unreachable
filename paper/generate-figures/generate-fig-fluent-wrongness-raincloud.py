#!/usr/bin/env python3
"""
Figure (Section 4): fluent-wrongness raincloud.

Distributions of last-token entropy for correct vs incorrect accessibility
answers, across Pythia scale. With scale the incorrect-answer distribution
slides toward the correct one -- the confidence penalty for being wrong shrinks.
Shows the distribution behind the single means in fluent_wrongness.csv.

Split half-violins (incorrect left, correct right) + jittered strip + mean
diamond. Correct=grey (baseline), Incorrect=vermillion (signal).

Reads:  results/entropy/pythia/<model>/<model>-accessibility.csv  (last_token_entropy)
        results/analysis/elicitation_coded.csv                    (accuracy, joined on prompt_id)
Writes: paper/figures/fluent-wrongness-raincloud.png

Run:  python paper/generate-figures/generate-fig-fluent-wrongness-raincloud.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from _figstyle import RESULTS_DIR, ANALYSIS_DIR, FIGURES_DIR, CORRECT_COLOR, INCORRECT_COLOR, apply_style
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
import pandas as pd, numpy as np

apply_style()
np.random.seed(0)  # reproducible strip jitter
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

SCALES = [("pythia-160m", "160M"), ("pythia-410m", "410M"), ("pythia-1b", "1B"),
          ("pythia-2.8b", "2.8B"), ("pythia-6.9b", "6.9B"), ("pythia-12b", "12B")]


def load():
    coded = pd.read_csv(ANALYSIS_DIR / "elicitation_coded.csv")
    coded = coded[(coded.suite == "pythia") & (coded.domain == "accessibility")]
    rows = []
    for model, lab in SCALES:
        raw = pd.read_csv(RESULTS_DIR / f"entropy/pythia/{model}/{model}-accessibility.csv")
        c = coded[coded.model == model][["prompt_id", "accuracy"]]
        m = raw.merge(c, on="prompt_id", how="inner")
        m = m[m.accuracy.isin(["correct", "incorrect"])]
        m["scale"] = lab
        rows.append(m[["scale", "accuracy", "last_token_entropy"]])
    return pd.concat(rows, ignore_index=True)


def make_figure():
    d = load()
    labels = [l for _, l in SCALES]
    fig, ax = plt.subplots(figsize=(11, 5))
    off = 0.18

    def half_violin(vals, center, side, color):
        if len(vals) < 2:
            if len(vals) == 1:
                ax.scatter([center], vals, color=color, s=25, zorder=5)
            return
        v = ax.violinplot(vals, positions=[center], widths=0.7,
                          showmeans=False, showextrema=False)
        for b in v["bodies"]:
            pth = b.get_paths()[0].vertices
            if side == "left":
                pth[:, 0] = np.clip(pth[:, 0], -np.inf, center)
            else:
                pth[:, 0] = np.clip(pth[:, 0], center, np.inf)
            b.set_facecolor(color); b.set_edgecolor(color)
            b.set_alpha(0.35); b.set_zorder(2)

    for i, lab in enumerate(labels):
        for acc, side, color, jit in [("incorrect", "left", INCORRECT_COLOR, -off),
                                       ("correct", "right", CORRECT_COLOR, off)]:
            vals = d[(d.scale == lab) & (d.accuracy == acc)]["last_token_entropy"].values
            half_violin(vals, i, side, color)
            jx = i + jit + np.random.uniform(-0.05, 0.05, size=len(vals))
            ax.scatter(jx, vals, color=color, s=14, alpha=0.7, zorder=4,
                       edgecolor="white", linewidth=0.3)
            if len(vals):
                ax.scatter([i + jit], [vals.mean()], color=color, s=70, zorder=6,
                           marker="D", edgecolor="white", linewidth=1.0)

    ax.set_xticks(np.arange(len(labels)))
    ax.set_xticklabels(labels, fontsize=10)
    ax.set_xlabel("Pythia scale", fontsize=11, labelpad=8)
    ax.set_ylabel("Last-token entropy (nats)", fontsize=11, labelpad=8)
    ax.set_title("Fluent wrongness: the confidence penalty for being wrong shrinks with scale",
                 fontsize=12.5, pad=12, color="#222")
    leg = [Patch(facecolor=INCORRECT_COLOR, alpha=0.5, label="Incorrect (accessibility)"),
           Patch(facecolor=CORRECT_COLOR, alpha=0.5, label="Correct (accessibility)"),
           Line2D([0], [0], marker="D", color="w", markerfacecolor="#555",
                  markersize=8, label="mean")]
    ax.legend(handles=leg, frameon=False, fontsize=10, loc="upper right")
    fig.tight_layout()
    out = FIGURES_DIR / "fluent-wrongness-raincloud.png"
    fig.savefig(out, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {out}")
    print(d.groupby(["scale", "accuracy"]).size().unstack(fill_value=0).reindex(labels))


if __name__ == "__main__":
    make_figure()
