#!/usr/bin/env python3
"""
Figure: The opening vignette, drawn.

Three prompt/completion cards from Pythia-12B, same structure, three
different failure modes: correct (alt text), fluent-but-wrong (screen
reader), incoherent 404 template (skip link). Corpus counts sit in each
card header so the frequency inversion is visible at a glance: screen
reader is the most frequent of the three and still fails.

Text-only styling on purpose: no color coding, so the figure carries no
palette semantics and survives any rendering. The verdicts are glyphs
and words.

Writes: paper/figures/vignette-three-completions.png
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.patches import FancyBboxPatch
from pathlib import Path

SCRIPT_DIR  = Path(__file__).resolve().parent
FIGURES_DIR = SCRIPT_DIR.parent / "figures"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

available_fonts = [f.name for f in fm.fontManager.ttflist]
FONT = "Atkinson Hyperlegible" if "Atkinson Hyperlegible" in available_fonts else "DejaVu Sans"
plt.rcParams.update({"font.family": FONT, "figure.facecolor": "white"})

CARDS = [
    {
        "header": "alt text \u2014 23,306 occurrences",
        "prompt": "An image without alt text is not accessible because",
        "completion": "\u201cit has no text alternative\u201d",
        "verdict": "\u2713 correct",
    },
    {
        "header": "screen reader \u2014 32,100 occurrences",
        "prompt": "A website without screen reader support is not accessible because",
        "completion": "\u201cit does not have a text alternative\u201d",
        "verdict": "\u2717 fluent, confident, wrong",
    },
    {
        "header": "skip link \u2014 662 occurrences",
        "prompt": "A long navigation menu without a skip link is not accessible because",
        "completion": "\u201cof the following error: The page you are trying to reach\n"
                      "is not available in the current context\u201d",
        "verdict": "\u2717 a fluent 404 template",
    },
]


def make_figure():
    fig, ax = plt.subplots(figsize=(9.5, 5.0))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 3.15)
    ax.axis("off")

    for i, card in enumerate(CARDS):
        top = 3.05 - i * 1.05
        box = FancyBboxPatch(
            (0.01, top - 0.92), 0.98, 0.92,
            boxstyle="round,pad=0.012",
            facecolor="#f5f6fa", edgecolor="#c9cdd6", linewidth=1.0,
        )
        ax.add_patch(box)

        ax.text(0.04, top - 0.14, card["header"],
                fontsize=11, fontweight="bold", color="#222222", va="top")
        ax.text(0.96, top - 0.14, card["verdict"],
                fontsize=11, fontweight="bold", color="#222222",
                va="top", ha="right")
        ax.text(0.04, top - 0.40, card["prompt"] + " \u2026",
                fontsize=10.5, color="#555555", va="top")
        ax.text(0.07, top - 0.62, card["completion"],
                fontsize=10.5, color="#111111", va="top",
                style="italic", linespacing=1.35)

    fig.tight_layout()
    out = FIGURES_DIR / "vignette-three-completions.png"
    fig.savefig(out, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {out}")


if __name__ == "__main__":
    make_figure()
