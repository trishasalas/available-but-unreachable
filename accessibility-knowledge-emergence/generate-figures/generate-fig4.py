#!/usr/bin/env python3
"""
Generate Figure 4: Binding Persistence by Model Scale — Pythia.

Bar chart showing the last layer containing a strong binding head
(attention weight ≥ 0.5) for each Pythia model size. Pre-emergence
models (160M–1B) shown in light blue; post-emergence (2.8B–6.9B)
in navy. Dashed vertical marker at emergence threshold.

All text (title, caption, alt text) lives in the LaTeX document —
this script outputs a clean chart only.

Data: results/pythia/*_attention_binding.csv

Run from anywhere:
    python generate-figures/generate-fig4.py

Output: figures/binding-persistence.png
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

# ── Model metadata ─────────────────────────────────────────────────────────────
MODELS       = ["160M", "410M", "1B", "2.8B", "6.9B", "12B"]
TOTAL_LAYERS = [12, 24, 16, 32, 32, 36]

# Colors: light blue = pre-emergence, navy = post-emergence
COLORS = [LIGHT_BLUE, LIGHT_BLUE, LIGHT_BLUE, NAVY, NAVY, NAVY]

# ── Threshold marker: between 1B (index 2) and 2.8B (index 3) ─────────────────
THRESHOLD_X = 2.5


def last_strong_layer(csv_path, threshold=0.5):
    """Return the highest layer index containing at least one head above threshold."""
    df = pd.read_csv(csv_path)
    strong = df[df["reader_to_screen"] >= threshold]
    return int(strong["layer"].max()) if not strong.empty else 0


def make_figure():
    csv_files = [
        RESULTS_DIR / "pythia/160m_attention_binding.csv",
        RESULTS_DIR / "pythia/410m_attention_binding.csv",
        RESULTS_DIR / "pythia/1b_attention_binding.csv",
        RESULTS_DIR / "pythia/2.8b_attention_binding.csv",
        RESULTS_DIR / "pythia/6.9b_attention_binding.csv",
        RESULTS_DIR / "pythia/12b_attention_binding.csv",
    ]
    last_layers = [last_strong_layer(p) for p in csv_files]

    x = np.arange(len(MODELS))

    fig, ax = plt.subplots(figsize=(9, 5.2))

    bars = ax.bar(x, last_layers, color=COLORS, width=0.55, zorder=2)

    # Value labels on bars
    for bar, val, total in zip(bars, last_layers, TOTAL_LAYERS):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.4,
            f"Layer {val}\n({val}/{total})",
            ha="center", va="bottom",
            fontsize=8.5, color="#444444", linespacing=1.3,
        )

    # Emergence threshold marker
    ax.axvline(THRESHOLD_X, color="#555555", linewidth=1.6,
               linestyle="--", alpha=0.6, zorder=3)
    ax.text(
        THRESHOLD_X - 0.08, max(last_layers) * 1.02,
        "emergence\nthreshold",
        ha="right", va="bottom",
        fontsize=8, color="#555555", linespacing=1.3,
    )

    ax.set_xticks(x)
    ax.set_xticklabels(MODELS, fontsize=10.5)
    ax.set_xlabel("Model Size (Parameters)", fontsize=10, labelpad=8)
    ax.set_ylabel("Last layer with strong binding head (≥0.5)", fontsize=9.5, labelpad=8)
    ax.set_ylim(0, max(last_layers) * 1.22)
    ax.set_xlim(-0.5, len(MODELS) - 0.5)

    out = FIGURES_DIR / "binding-persistence.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {out}")


if __name__ == "__main__":
    make_figure()
