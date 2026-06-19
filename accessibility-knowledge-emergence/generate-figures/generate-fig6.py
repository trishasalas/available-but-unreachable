#!/usr/bin/env python3
"""
Generate Figure 6: Per-Concept Perplexity — Small Multiples.

Three side-by-side panels showing correct vs. wrong definition perplexity
for screen_reader, alt_text, and skip_link individually across the full
Pythia suite (160M–12B). Shared y-axis so flip points are comparable.

Data: results/pythia/perplexity_data.csv

Run from anywhere:
    python generate-figures/generate-fig6.py

Output: figures/pythia-perplexity-panels.png
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
import pandas as pd
from pathlib import Path

SCRIPT_DIR  = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent
FIGURES_DIR = PROJECT_DIR / "figures"
RESULTS_DIR = PROJECT_DIR / "results"

# ── Palette (matches other figures) ──────────────────────────────────────────
NAVY       = "#08306b"
LIGHT_BLUE = "#6baed6"

# ── Font (matches other figures) ─────────────────────────────────────────────
available_fonts = [f.name for f in fm.fontManager.ttflist]
FONT = "Atkinson Hyperlegible" if "Atkinson Hyperlegible" in available_fonts else "DejaVu Sans"

plt.rcParams.update({
    "font.family":       FONT,
    "axes.spines.top":   False,
    "axes.spines.right": False,
    "figure.facecolor":  "white",
    "axes.facecolor":    "white",
})

# ── Model order (full Pythia suite) ──────────────────────────────────────────
MODELS = ["160M", "410M", "1B", "2.8B", "6.9B", "12B"]

# ── Concepts and display names ───────────────────────────────────────────────
CONCEPTS = ["screen_reader", "alt_text", "skip_link"]
DISPLAY  = {
    "screen_reader": "Screen Reader",
    "alt_text":      "Alt Text",
    "skip_link":     "Skip Link",
}


def load_data():
    """Load perplexity CSV and return dict of concept → (correct, wrong) lists."""
    df = pd.read_csv(RESULTS_DIR / "pythia/perplexity_data.csv")
    df["model"] = pd.Categorical(df["model"], categories=MODELS, ordered=True)
    df = df.sort_values("model")

    data = {}
    for concept in CONCEPTS:
        cdf = df[df["concept"] == concept]
        data[concept] = (
            cdf["correct_ppl"].tolist(),
            cdf["wrong_ppl"].tolist(),
        )
    return data


def find_flip(correct, wrong):
    """Return index of first model where correct < wrong, or None."""
    for i in range(len(correct)):
        if correct[i] < wrong[i]:
            return i
    return None


def make_figure():
    data = load_data()
    x = np.arange(len(MODELS))

    # Shared y-axis limits across panels
    all_vals = []
    for correct, wrong in data.values():
        all_vals.extend(correct)
        all_vals.extend(wrong)
    y_max = max(all_vals) * 1.15

    fig, axes = plt.subplots(1, 3, figsize=(14, 4.8), sharey=True)
    fig.subplots_adjust(wspace=0.08)

    for ax, concept in zip(axes, CONCEPTS):
        correct, wrong = data[concept]
        flip_idx = find_flip(correct, wrong)

        # Correct definition line — navy, circle markers
        ax.plot(x, correct, color=NAVY, linewidth=2.2, zorder=4,
                label="Correct definition")
        ax.scatter(x, correct, color=NAVY, s=50, zorder=5)

        # Wrong definition line — light blue, square markers
        ax.plot(x, wrong, color=LIGHT_BLUE, linewidth=2.2, zorder=4,
                label="Wrong definition")
        ax.scatter(x, wrong, color=LIGHT_BLUE, marker="s", s=50, zorder=5)

        # Flip annotation
        if concept == "screen_reader":
            # Flip between 410M (idx 1) and 1B (idx 2)
            ax.axvspan(1, 2, color="#e8eaf0", alpha=0.6, zorder=0)
            ax.text(
                1.5, y_max * 0.88,
                "preference\nflips",
                ha="center", va="top",
                fontsize=8.5, color="#555555", style="italic",
                linespacing=1.3,
            )
        elif concept == "alt_text":
            # Already flipped at 160M
            ax.annotate(
                "already prefers\ncorrect at 160M",
                xy=(0, correct[0] + 3),
                xytext=(2.2, y_max * 0.55),
                fontsize=8.5, color="#555555",
                ha="center", linespacing=1.3,
                arrowprops=dict(arrowstyle="->", color="#aaaaaa", lw=1.0),
            )
        elif concept == "skip_link":
            # Never flips
            ax.text(
                x[-1] - 0.1, y_max * 0.88,
                "no flip",
                ha="right", va="top",
                fontsize=8.5, color="#555555", style="italic",
            )

        ax.set_title(DISPLAY[concept], fontsize=11, pad=10)
        ax.set_xticks(x)
        ax.set_xticklabels(MODELS, fontsize=9, rotation=30, ha="right")
        ax.set_xlim(-0.3, len(MODELS) - 0.7)
        ax.set_ylim(0, y_max)

    # Shared axis labels
    axes[0].set_ylabel("Perplexity  (lower = more expected)", fontsize=10, labelpad=8)
    fig.text(0.5, -0.02, "Model Size (Parameters)", ha="center", fontsize=10)

    # Single legend for all panels — placed at top right of first panel
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(
        handles, labels,
        loc="upper right",
        bbox_to_anchor=(0.98, 0.98),
        fontsize=10,
        frameon=False,
    )

    out = FIGURES_DIR / "pythia-perplexity-panels.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {out}")


if __name__ == "__main__":
    make_figure()
