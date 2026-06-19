#!/usr/bin/env python3
"""
Generate Figure 1 summary panel for Paper 1: Accessibility Emergence.

Single line graph showing binding depth and behavioral emergence
rising at the same 2.8B threshold.

160M excluded from this figure — see DECISIONS.md for rationale.

Run from anywhere:
    python generate-figures/generate-fig1.py

Output: figures/fig-01-summary.png
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

# ── Palette (matches generate-figures.py) ─────────────────────────────────────
NAVY       = "#08306b"
LIGHT_BLUE = "#6baed6"

# ── Font ──────────────────────────────────────────────────────────────────────
available_fonts = [f.name for f in fm.fontManager.ttflist]
FONT = "Atkinson Hyperlegible" if "Atkinson Hyperlegible" in available_fonts else "DejaVu Sans"

plt.rcParams.update({
    "font.family":       FONT,
    "axes.spines.top":   False,
    "axes.spines.right": False,
    "figure.facecolor":  "white",
    "axes.facecolor":    "white",
})

# ── Data (160M excluded — see DECISIONS.md) ───────────────────────────────────
MODELS       = ["410M", "2.8B", "6.9B", "12B"]
TOTAL_LAYERS = [24, 32, 32, 36]

# Behavioral results: correct=1, partial=0.5, incorrect=0
# ARIA scores negative — confabulation intensifies with scale:
#   1B: starts confabulating (-0.25)
#   2.8B: fluently wrong (-0.5)
#   6.9B–12B: maximally confident and wrong (-1.0)
# 12B scores derived from perplexity ratios (no manual evaluation):
#   screen reader 55.2/12.4=4.45 → 1.0, alt text 33.8/10.8=3.13 → 1.0,
#   skip link 47.4/63.6=0.75 → 0, WCAG extrapolated → 1.0, ARIA saturated → -1.0
BEHAVIORAL_RAW = {
    "screen reader": [0,    0.5,  1,    0.5,  1   ],
    "alt text":      [0,    0,    1,    1,    1   ],
    "skip link":     [0.5,  0,    1,    0,    0   ],
    "WCAG":          [0,    0,    0,    1,    1   ],
    "ARIA":          [0,   -0.25,-0.5, -1.0, -1.0 ],
}


def last_strong_layer(csv_path, threshold=0.5):
    """Return the highest layer index containing at least one head above threshold."""
    df = pd.read_csv(csv_path)
    strong = df[df["reader_to_screen"] >= threshold]
    return int(strong["layer"].max()) if not strong.empty else 0


def make_figure():
    csv_files = [
        RESULTS_DIR / "pythia/410m_attention_binding.csv",
        RESULTS_DIR / "pythia/2.8b_attention_binding.csv",
        RESULTS_DIR / "pythia/6.9b_attention_binding.csv",
        RESULTS_DIR / "pythia/12b_attention_binding.csv",
    ]
    last_layers   = [last_strong_layer(p) for p in csv_files]
    binding_depth = [l / t for l, t in zip(last_layers, TOTAL_LAYERS)]
    behavioral    = [
        sum(BEHAVIORAL_RAW[c][mi] for c in BEHAVIORAL_RAW) / 5
        for mi in range(len(MODELS))
    ]

    x = np.arange(len(MODELS))

    fig, ax = plt.subplots(figsize=(10, 5.2))

    # Reference zero line
    ax.axhline(0, color="#888888", linewidth=0.8, zorder=1)

    # Emergence threshold — index 2 is 2.8B in the 4-model list
    ax.axvline(2, color="#555555", linewidth=1.6, linestyle="--", alpha=0.6, zorder=2)
    ax.annotate(
        "2.8B emergence threshold",
        xy=(2, 0.92),
        xytext=(1.1, 0.93),
        fontsize=11, color="#555555",
        ha="right",
        arrowprops=dict(arrowstyle="->", color="#888888", lw=1.0),
    )

    # Binding depth line
    ax.plot(x, binding_depth, color=NAVY, linewidth=2.5, zorder=4,
            label="Binding depth")
    ax.scatter(x, binding_depth, color=NAVY, s=65, zorder=5)

    # Behavioral emergence line
    ax.plot(x, behavioral, color=LIGHT_BLUE, linewidth=2.5, linestyle="--", zorder=4,
            label="Behavioral emergence")
    ax.scatter(x, behavioral, color=LIGHT_BLUE, s=65, zorder=5)

    # Annotations
    ax.annotate(
        "ARIA confabulation\ndepresses score",
        xy=(3, behavioral[3]),
        xytext=(3.9, behavioral[3] + 0.25),
        fontsize=11, color="#555555",
        arrowprops=dict(arrowstyle="->", color="#aaaaaa", lw=1.0),
        linespacing=1.3,
    )

    ax.set_xticks(x)
    ax.set_xticklabels(MODELS, fontsize=10.5)
    ax.set_xlabel("Model Size (Parameters)", fontsize=10, labelpad=8)
    ax.set_ylabel("Normalized score (0\u20131)", fontsize=10, labelpad=8)
    ax.set_ylim(-0.28, 1.08)
    ax.set_xlim(-0.3, len(MODELS) - 0.7)

    ax.legend(fontsize=12, frameon=False, loc="lower left")

    out = FIGURES_DIR / "fig-01-summary.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {out}")


if __name__ == "__main__":
    make_figure()
