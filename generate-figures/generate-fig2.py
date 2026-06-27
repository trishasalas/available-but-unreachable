#!/usr/bin/env python3
"""
Generate Figure 2: Recognition Precedes Generation — Pythia.

Dual line chart showing averaged perplexity for correct vs. wrong
definitions across five Pythia model sizes. Lines cross between
410M and 1B, marking the recognition-before-generation threshold.

Data: results/pythia/perplexity_data.csv
      Three concept pairs: screen_reader, alt_text, skip_link
      Values averaged across pairs per model.

Run from anywhere:
    python generate-figures/generate-fig2.py

Output: figures/pythia-perplexity.png
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
import pandas as pd
from pathlib import Path

SCRIPT_DIR  = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent  # accessibility-knowledge-emergence/
FIGURES_DIR = PROJECT_DIR / "figures"
RESULTS_DIR = PROJECT_DIR / "results"

# ── Palette (matches fig1) ─────────────────────────────────────────────────────
NAVY       = "#08306b"
LIGHT_BLUE = "#6baed6"

# ── Font (matches fig1) ────────────────────────────────────────────────────────
available_fonts = [f.name for f in fm.fontManager.ttflist]
FONT = "Atkinson Hyperlegible" if "Atkinson Hyperlegible" in available_fonts else "DejaVu Sans"

plt.rcParams.update({
    "font.family":       FONT,
    "axes.spines.top":   False,
    "axes.spines.right": False,
    "figure.facecolor":  "white",
    "axes.facecolor":    "white",
})

# ── Model order ────────────────────────────────────────────────────────────────
MODELS = ["160M", "410M", "2.8B", "6.9B", "12B"]

# ── Flip zone: crossing occurs between 410M (index 1) and 1B (index 2) ────────
FLIP_ZONE = (1, 2)


def load_data():
    """Load and average perplexity across concept pairs per model."""
    df = pd.read_csv(RESULTS_DIR / "pythia/perplexity_data.csv")
    avg = df.groupby("model")[["correct_ppl", "wrong_ppl"]].mean()
    avg = avg.reindex(MODELS)
    return avg["correct_ppl"].tolist(), avg["wrong_ppl"].tolist()


def make_figure():
    correct, wrong = load_data()
    x = np.arange(len(MODELS))

    fig, ax = plt.subplots(figsize=(9, 5.2))

    # Flip zone shading
    ax.axvspan(*FLIP_ZONE, color="#e8eaf0", alpha=0.7, zorder=0)
    ax.text(
        sum(FLIP_ZONE) / 2, max(max(correct), max(wrong)) * 0.87,
        "flip\nzone",
        ha="center", va="top",
        fontsize=9, color="#888888", style="italic", linespacing=1.4,
    )

    # Preference flip annotation — points to where lines cross
    ax.annotate(
        "preference flips\nbetween 410M and 1B",
        xy=(1.97, correct[2] - 0.5),
        xytext=(0.5, correct[2] -10),
        fontsize=9, color="#555555",
        ha="center", linespacing=1.4,
        arrowprops=dict(arrowstyle="->", color="#aaaaaa", lw=1.0),
    )

    # Correct definition line — navy, circle markers
    ax.plot(x, correct, color=NAVY, linewidth=2.5, zorder=4,
            label="Correct definition")
    ax.scatter(x, correct, color=NAVY, s=65, zorder=5)

    # Wrong definition line — light blue, square markers
    ax.plot(x, wrong, color=LIGHT_BLUE, linewidth=2.5, zorder=4,
            label="Wrong definition")
    ax.scatter(x, wrong, color=LIGHT_BLUE, marker="s", s=65, zorder=5)

    ax.set_xticks(x)
    ax.set_xticklabels(MODELS, fontsize=10.5)
    ax.set_xlabel("Model Size (Parameters)", fontsize=10, labelpad=8)
    ax.set_ylabel("Perplexity  (lower = more expected)", fontsize=10, labelpad=8)
    ax.set_ylim(0, max(max(correct), max(wrong)) * 1.18)
    ax.set_xlim(-0.3, len(MODELS) - 0.7)

    ax.legend(fontsize=11, frameon=False, loc="upper right")

    out = FIGURES_DIR / "pythia-perplexity.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {out}")


if __name__ == "__main__":
    make_figure()
