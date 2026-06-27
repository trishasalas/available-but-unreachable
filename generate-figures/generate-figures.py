#!/usr/bin/env python3
"""
DEPRECATED — use individual figure scripts (generate-fig1.py through generate-fig5.py) instead.

This was the original combined figure generator before each figure was split
into its own script. Kept for provenance only; outputs may not match current
paper figures.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path

# ── Paths (resolved from script location, run from anywhere) ──────────────────
SCRIPT_DIR  = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent  # accessibility-knowledge-emergence/
FIGURES_DIR = PROJECT_DIR / "figures"
RESULTS_DIR = PROJECT_DIR / "results"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

# ── Palette ────────────────────────────────────────────────────────────────────
NAVY       = "#08306b"
BLUE       = "#2171b5"
LIGHT_BLUE = "#6baed6"

plt.rcParams.update({
    "font.family":       "Atkinson Hyperlegible",
    "axes.spines.top":   False,
    "axes.spines.right": False,
    "figure.facecolor":  "white",
    "axes.facecolor":    "white",
})


# ── Figure: Perplexity preference ─────────────────────────────────────────────
#
# Preference ratio = wrong_ppl / correct_ppl
#   > 1.0  → model finds correct definition more natural (flip has happened)
#   < 1.0  → model finds wrong definition more natural (not yet flipped)
#
# Pythia values derived from raw perplexity recorded during Experiment 3:
#   correct = [106.7, 40.1, 18.8, 13.6, 15.6]
#   wrong   = [ 41.4, 32.8, 42.2, 54.9, 46.1]
#
# GPT-2 values from preference ratios reported in paper (no raw CSVs retained):
#   Wrong 1.1x  → 1/1.1 ≈ 0.91
#   Correct N.Nx → N.N

def make_perplexity_figure(models, ratios, flip_zone, title, subtitle, caption, fig_path):
    """
    Line chart of preference ratio (wrong_ppl / correct_ppl) by model size.
    Dashed line at 1.0 marks the preference flip.
    """
    x = range(len(models))

    fig, ax = plt.subplots(figsize=(7.5, 4.8))

    # Shade flip zone
    ax.axvspan(*flip_zone, color="#e8eaf0", alpha=0.7, zorder=0)
    ax.text(
        sum(flip_zone) / 2, max(ratios) * 0.88,
        "flip\nzone",
        ha="center", va="top",
        fontsize=9, color="#888888", style="italic", linespacing=1.4,
    )

    # Flip threshold line
    ax.axhline(1.0, color="#aaaaaa", linewidth=1.0, linestyle="--", zorder=1)
    ax.text(
        len(models) - 0.1, 1.04,
        "preference\nflip",
        ha="right", va="bottom",
        fontsize=7.5, color="#888888", linespacing=1.3,
    )

    # Color points by side of threshold
    colors = [NAVY if r >= 1.0 else LIGHT_BLUE for r in ratios]

    ax.plot(x, ratios, color=BLUE, linewidth=2, zorder=3)
    for xi, yi, ci in zip(x, ratios, colors):
        ax.scatter(xi, yi, color=ci, s=55, zorder=4)

    ax.set_xticks(list(x))
    ax.set_xticklabels(models, fontsize=10)
    ax.set_xlabel("Model Size (Parameters)", fontsize=10, labelpad=8)
    ax.set_ylabel("Preference ratio  (wrong ppl / correct ppl)", fontsize=9.5, labelpad=8)
    ax.set_ylim(0, max(ratios) * 1.15)

    ax.set_title(subtitle, fontsize=9.5, color="#555555", pad=10)
    fig.suptitle(title, fontsize=11, fontweight="bold", y=1.01, ha="center")

    fig.tight_layout()
    fig.text(
        0.5, -0.03, caption,
        ha="center", fontsize=8, color="#666666", style="italic",
    )

    fig.savefig(fig_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {fig_path}")


# ── Figure: Binding persistence ────────────────────────────────────────────────

def last_strong_layer(csv_path, threshold=0.5):
    """Return the highest layer index containing at least one head above threshold."""
    df = pd.read_csv(csv_path)
    strong = df[df["reader_to_screen"] >= threshold]
    return int(strong["layer"].max()) if not strong.empty else 0


def make_binding_persistence_figure():
    """
    Bar chart: last strong binding layer (≥0.5) for each Pythia model.
    Emergence threshold marker between 1B and 2.8B.
    """
    models = ["160M", "410M", "1B", "2.8B", "6.9B"]
    csv_files = [
        RESULTS_DIR / "pythia/160m_attention_binding.csv",
        RESULTS_DIR / "pythia/410m_attention_binding.csv",
        RESULTS_DIR / "pythia/1b_attention_binding.csv",
        RESULTS_DIR / "pythia/2.8b_attention_binding.csv",
        RESULTS_DIR / "pythia/6.9b_attention_binding.csv",
    ]
    total_layers = [12, 24, 16, 32, 32]

    last_layers = [last_strong_layer(p) for p in csv_files]

    x = np.arange(len(models))

    # Colors: pre-emergence (index 0-2) vs post-emergence (index 3-4)
    colors = [LIGHT_BLUE, LIGHT_BLUE, LIGHT_BLUE, NAVY, NAVY]

    fig, ax = plt.subplots(figsize=(7.5, 5))

    bars = ax.bar(x, last_layers, color=colors, width=0.55, zorder=2)

    # Value labels on bars
    for bar, val, total in zip(bars, last_layers, total_layers):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.4,
            f"Layer {val}\n({val}/{total})",
            ha="center", va="bottom",
            fontsize=8.5, color="#444444", linespacing=1.3,
        )

    # Emergence threshold marker: dashed vertical between 1B (x=2) and 2.8B (x=3)
    ax.axvline(2.5, color="#555555", linewidth=1.6, linestyle="--", alpha=0.6, zorder=3)
    ax.text(
        2.5, max(last_layers) * 1.02,
        "emergence\nthreshold",
        ha="center", va="bottom",
        fontsize=8, color="#555555", linespacing=1.3,
    )

    ax.set_xticks(x)
    ax.set_xticklabels(models, fontsize=10.5)
    ax.set_xlabel("Model Size (Parameters)", fontsize=10, labelpad=8)
    ax.set_ylabel("Last layer with strong binding head (≥0.5)", fontsize=9.5, labelpad=8)
    ax.set_ylim(0, max(last_layers) * 1.2)

    fig.suptitle(
        "Binding Persistence by Model Scale",
        fontsize=12, fontweight="bold", y=1.01, ha="center",
    )
    ax.set_title(
        "Last layer containing a head with attention weight ≥ 0.5  |  Pythia, screen reader",
        fontsize=9.5, color="#555555", pad=10,
    )

    fig.tight_layout()
    fig.text(
        0.5, -0.04,
        "Below the 2.8B emergence threshold, strong binding drops off by layer 6–11. "
        "At 2.8B and 6.9B, it persists to layers 29–30. "
        "Late-layer sustained binding coincides with the onset of correct behavioral generation.",
        ha="center", fontsize=8, color="#666666", style="italic", wrap=True,
    )

    out = FIGURES_DIR / "fig-binding-persistence.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {out}")


# ── Main ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":

    # Pythia: preference ratios derived from raw perplexity values
    #   correct = [106.7, 40.1, 18.8, 13.6, 15.6]
    #   wrong   = [ 41.4, 32.8, 42.2, 54.9, 46.1]
    pythia_ratios = [w / c for w, c in zip(
        [41.4, 32.8, 42.2, 54.9, 46.1],
        [106.7, 40.1, 18.8, 13.6, 15.6],
    )]

    make_perplexity_figure(
        models    = ["160M", "410M", "1B", "2.8B", "6.9B"],
        ratios    = pythia_ratios,
        flip_zone = (1, 2),   # between index 1 (410M) and index 2 (1B)
        title     = "",
        subtitle  = "",
        caption   = (
            ""
            ""
        ),
        fig_path  = FIGURES_DIR / "fig-pythia-perplexity.png",
    )

    # GPT-2: preference ratios from paper (no raw perplexity CSVs retained)
    #   Small/Medium: Wrong 1.1x  → 1/1.1
    #   Large:        Correct 2.0x → 2.0
    #   XL:           Correct 2.6x → 2.6
    gpt2_ratios = [1 / 1.1, 1 / 1.1, 2.0, 2.6]

    make_perplexity_figure(
        models    = ["Small\n(117M)", "Medium\n(406M)", "Large\n(838M)", "XL\n(1.5B)"],
        ratios    = gpt2_ratios,
        flip_zone = (1, 2),   # between index 1 (406M) and index 2 (838M)
        title     = "Recognition Precedes Generation — GPT-2",
        subtitle  = "Perplexity preference ratio for screen reader: correct vs wrong definition",
        caption   = (
            "Preference ratio derived from paper-reported multiples (raw perplexity values not retained). "
            "GPT-2 flip occurs between 406M and 838M -- consistent with Pythia's 410M to 1B transition."
        ),
        fig_path  = FIGURES_DIR / "fig-gpt2-perplexity.png",
    )

    make_binding_persistence_figure()
