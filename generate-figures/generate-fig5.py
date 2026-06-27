#!/usr/bin/env python3
"""
Generate Figure 5: Binding Generalizes Across Accessibility Compounds.

Grouped bar chart showing head counts at Pythia 2.8B for three
accessibility compounds: screen reader, alt text, skip link.
Two bars per group: all heads (attention > 0.1) and strong heads (≥ 0.5).

All text (title, caption, alt text) lives in the LaTeX document —
this script outputs a clean chart only.

Data: hardcoded from Pythia 2.8B attention binding analysis.
      screen reader: all=101, strong=25
      alt text:      all=200, strong=40
      skip link:     all=208, strong=40

Run from anywhere:
    python generate-figures/generate-fig5.py

Output: figures/compound-comparison.png
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
from pathlib import Path

SCRIPT_DIR  = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent  # accessibility-knowledge-emergence/
FIGURES_DIR = PROJECT_DIR / "figures"

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

# ── Data: Pythia 2.8B head counts ─────────────────────────────────────────────
CONCEPTS     = ["screen reader", "alt text", "skip link"]
ALL_HEADS    = [101, 200, 182]   # attention weight > 0.1
STRONG_HEADS = [25,  49,  32]    # attention weight ≥ 0.5

BAR_WIDTH = 0.35


def make_figure():
    x = np.arange(len(CONCEPTS))

    fig, ax = plt.subplots(figsize=(9, 5.2))

    bars_all    = ax.bar(x - BAR_WIDTH / 2, ALL_HEADS,    BAR_WIDTH,
                         color=LIGHT_BLUE, label="All heads  (>0.1)",  zorder=2)
    bars_strong = ax.bar(x + BAR_WIDTH / 2, STRONG_HEADS, BAR_WIDTH,
                         color=NAVY,       label="Strong heads  (≥0.5)", zorder=2)

    # Value labels on bars
    for bar, val in zip(bars_all, ALL_HEADS):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 2,
            str(val),
            ha="center", va="bottom", fontsize=9.5, color="#444444",
        )
    for bar, val in zip(bars_strong, STRONG_HEADS):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 2,
            str(val),
            ha="center", va="bottom", fontsize=9.5, color="#444444",
        )

    ax.set_xticks(x)
    ax.set_xticklabels(CONCEPTS, fontsize=10.5)
    ax.set_xlabel("Accessibility Compound", fontsize=10, labelpad=8)
    ax.set_ylabel("Head count  (Pythia 2.8B)", fontsize=10, labelpad=8)
    ax.set_ylim(0, max(ALL_HEADS) * 1.18)
    ax.set_xlim(-0.5, len(CONCEPTS) - 0.5)

    ax.legend(fontsize=11, frameon=False, loc="upper left")

    out = FIGURES_DIR / "compound-comparison.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {out}")


if __name__ == "__main__":
    make_figure()
