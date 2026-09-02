#!/usr/bin/env python3
"""Figure 1: identical prompt structure, divergent Pythia-12B behavior.

This is a reproducible Matplotlib rendering of the Introduction infographic.
It reads and validates the three frozen model completions and their Pile
bigram counts.  All marks are explanatory; the count track is explicitly a
log-scaled position rather than a decorative distribution.

Reads:
  results/logits/pythia/pythia-12b_because_generations.csv
  results/frequency/frequency_table.csv

Writes:
  paper/figures/introduction-frequency-gap.png
"""

from __future__ import annotations

import csv
import math
import re
import textwrap
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch


ROOT = Path(__file__).resolve().parents[2]
GENERATIONS = ROOT / "results" / "logits" / "pythia" / "pythia-12b_because_generations.csv"
FREQUENCY = ROOT / "results" / "frequency" / "frequency_table.csv"
OUTPUT = ROOT / "paper" / "figures" / "introduction-frequency-gap.png"

MODEL = "pythia-12b"
EXPECTED_COUNTS = {"alt_text": 23_306, "screen_reader": 32_100, "skip_link": 662}
EXPECTED_STARTS = {
    "alt_text": "it has no text alternative",
    "screen_reader": "it does not have a text alternative",
    "skip_link": "of the following error:",
}

# Okabe-Ito colors; labels and symbols make meaning redundant with color.
GREEN = "#007D53"
BLUE = "#0057A6"
ORANGE = "#D55E00"
RED = "#A40000"
INK = "#171717"
MID = "#606060"
LIGHT = "#F5F6F7"
RULE = "#D7D9DC"

FONT = (
    "Atkinson Hyperlegible"
    if "Atkinson Hyperlegible" in {f.name for f in fm.fontManager.ttflist}
    else "DejaVu Sans"
)

ROWS = [
    {
        "compound": "alt_text",
        "label": "alt text",
        "short": "ALT",
        "color": GREEN,
        "completion": "“it has no text alternative”",
        "emphasis": "text alternative",
        "symbol": "✓",
        "outcome": "CORRECT",
        "outcome_note": "Matches the accessibility definition",
    },
    {
        "compound": "screen_reader",
        "label": "screen reader",
        "short": "SR",
        "color": BLUE,
        "completion": "“it does not have a\ntext alternative”",
        "emphasis": "text alternative",
        "symbol": "×",
        "outcome": "INCORRECT",
        "outcome_note": "Plausible, fluent, and wrong",
    },
    {
        "compound": "skip_link",
        "label": "skip link",
        "short": "SKIP",
        "color": ORANGE,
        "completion": (
            "“of the following error:\n"
            "The page you are trying to reach is not\n"
            "available in the current context”"
        ),
        "emphasis": "",
        "symbol": "×",
        "outcome": "404 TEMPLATE",
        "outcome_note": "Unrelated error message",
    },
]


def _flat(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().lower()


def load_and_validate() -> dict[str, int]:
    with FREQUENCY.open(newline="", encoding="utf-8") as handle:
        freq = {
            row["compound"]: int(row["bigram_count"])
            for row in csv.DictReader(handle)
            if row["compound"] in EXPECTED_COUNTS
        }
    assert freq == EXPECTED_COUNTS, (freq, EXPECTED_COUNTS)

    with GENERATIONS.open(newline="", encoding="utf-8") as handle:
        generations = {
            row["compound"]: row["generation_text"]
            for row in csv.DictReader(handle)
            if row["model"] == MODEL
        }
    assert set(generations) == set(EXPECTED_COUNTS), sorted(generations)
    for compound, expected_start in EXPECTED_STARTS.items():
        assert _flat(generations[compound]).startswith(expected_start), (
            compound,
            generations[compound],
        )
    return freq


def rounded_box(ax, xy, width, height, *, edge=RULE, face="white", radius=0.012, lw=1.0):
    box = FancyBboxPatch(
        xy,
        width,
        height,
        boxstyle=f"round,pad=0.010,rounding_size={radius}",
        linewidth=lw,
        edgecolor=edge,
        facecolor=face,
        transform=ax.transAxes,
        clip_on=False,
    )
    ax.add_patch(box)
    return box


def draw_count_track(ax, x0: float, x1: float, y: float, count: int, color: str) -> None:
    """Place a count on a shared 10^2--10^5 log track."""
    ax.plot([x0, x1], [y, y], color=RULE, lw=1.1, transform=ax.transAxes, clip_on=False)
    for exponent in (2, 3, 4, 5):
        x = x0 + (exponent - 2) / 3 * (x1 - x0)
        ax.plot([x, x], [y - 0.006, y + 0.006], color="#AEB2B7", lw=0.8,
                transform=ax.transAxes, clip_on=False)
    pos = (math.log10(count) - 2) / 3
    x = x0 + pos * (x1 - x0)
    ax.scatter([x], [y], s=52, color=color, edgecolor="white", linewidth=0.8,
               transform=ax.transAxes, zorder=4, clip_on=False)


def draw() -> None:
    counts = load_and_validate()
    plt.rcParams.update({"font.family": FONT, "font.size": 10, "text.color": INK})

    fig, ax = plt.subplots(figsize=(12, 7.6))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    fig.patch.set_facecolor("white")

    # Prompt banner.
    rounded_box(ax, (0.035, 0.913), 0.93, 0.052, edge="#E8EAED", face=LIGHT, radius=0.014, lw=0.7)
    ax.text(0.055, 0.939, "IDENTICAL PROMPT STRUCTURE", transform=ax.transAxes,
            ha="left", va="center", fontsize=10, fontweight="bold")
    ax.text(0.300, 0.939, r"$X$ is not accessible because", transform=ax.transAxes,
            ha="left", va="center", fontsize=17)
    ax.plot([0.575, 0.895], [0.928, 0.928], color=INK, lw=1.0, transform=ax.transAxes)

    # Column labels.
    headers = [
        (0.100, "COMPOUND"),
        (0.320, "PILE BIGRAM COUNT\n(log position)"),
        (0.625, "PYTHIA-12B COMPLETION"),
        (0.875, "OUTCOME"),
    ]
    for x, label in headers:
        ax.text(x, 0.875, label, transform=ax.transAxes, ha="center", va="center",
                fontsize=9.5, fontweight="bold", linespacing=1.0)

    y_rows = [0.752, 0.573, 0.394]
    for y in (0.662, 0.483):
        ax.plot([0.035, 0.965], [y, y], color=RULE, lw=0.8, transform=ax.transAxes)

    for row, y in zip(ROWS, y_rows):
        color = row["color"]
        compound = row["compound"]

        # Compact, reproducible concept badge instead of platform-dependent icons.
        ax.add_patch(Circle((0.066, y), 0.028, transform=ax.transAxes,
                            facecolor="white", edgecolor=color, linewidth=1.4))
        ax.text(0.066, y, row["short"], transform=ax.transAxes, ha="center", va="center",
                color=color, fontsize=8.5, fontweight="bold")
        ax.text(0.112, y, row["label"], transform=ax.transAxes, ha="left", va="center",
                color=color, fontsize=15, fontweight="bold")

        ax.text(0.320, y + 0.026, f"{counts[compound]:,}", transform=ax.transAxes,
                ha="center", va="center", color=color, fontsize=14, fontweight="bold")
        draw_count_track(ax, 0.258, 0.382, y - 0.025, counts[compound], color)

        # Completion card.
        rounded_box(ax, (0.458, y - 0.052), 0.300, 0.104,
                    edge=color, face=color + "0D", radius=0.012, lw=0.9)
        ax.text(0.608, y, row["completion"], transform=ax.transAxes,
                ha="center", va="center", fontsize=11.5, linespacing=1.22)

        # Outcome symbol and label.
        outcome_color = GREEN if row["outcome"] == "CORRECT" else RED
        ax.add_patch(Circle((0.803, y), 0.023, transform=ax.transAxes,
                            facecolor="white", edgecolor=outcome_color, linewidth=1.5))
        if row["symbol"] == "✓":
            ax.plot([0.792, 0.800, 0.815], [y - 0.001, y - 0.011, y + 0.012],
                    color=outcome_color, lw=2.4, solid_capstyle="round",
                    transform=ax.transAxes)
        else:
            ax.plot([0.795, 0.811], [y - 0.010, y + 0.010], color=outcome_color,
                    lw=2.4, solid_capstyle="round", transform=ax.transAxes)
            ax.plot([0.795, 0.811], [y + 0.010, y - 0.010], color=outcome_color,
                    lw=2.4, solid_capstyle="round", transform=ax.transAxes)
        ax.text(0.837, y + 0.020, row["outcome"], transform=ax.transAxes,
                ha="left", va="center", color=outcome_color, fontsize=11, fontweight="bold")
        ax.text(0.837, y - 0.016, "\n".join(textwrap.wrap(row["outcome_note"], 27)),
                transform=ax.transAxes, ha="left", va="center", fontsize=9.5, linespacing=1.15)

    # What the three examples establish.
    ax.text(0.318, 0.294, "FREQUENCY HELPS EXPLAIN", transform=ax.transAxes,
            ha="center", color=GREEN, fontsize=10.5, fontweight="bold")
    ax.text(0.318, 0.265, "the rare failure", transform=ax.transAxes,
            ha="center", fontsize=10.5)
    ax.text(0.646, 0.294, "FREQUENCY DOES NOT EXPLAIN", transform=ax.transAxes,
            ha="center", color=BLUE, fontsize=10.5, fontweight="bold")
    ax.text(0.646, 0.265, "the higher-frequency failure", transform=ax.transAxes,
            ha="center", fontsize=10.5)

    ax.add_patch(FancyArrowPatch((0.318, 0.360), (0.318, 0.315), arrowstyle="-|>",
                                 mutation_scale=11, lw=1.2, linestyle=":", color=GREEN,
                                 transform=ax.transAxes))
    ax.add_patch(FancyArrowPatch((0.395, 0.355), (0.535, 0.315),
                                 connectionstyle="arc3,rad=.25", arrowstyle="-|>",
                                 mutation_scale=11, lw=1.2, linestyle=":", color=BLUE,
                                 transform=ax.transAxes))

    ax.plot([0.070, 0.930], [0.220, 0.220], color=RULE, lw=0.8, transform=ax.transAxes)

    # Conceptual takeaway. This is explicitly framing, not a third estimate.
    rounded_box(ax, (0.075, 0.075), 0.210, 0.096, edge=RULE, face=LIGHT, radius=0.012, lw=0.8)
    ax.text(0.180, 0.137, "CORPUS FREQUENCY", transform=ax.transAxes,
            ha="center", va="center", color=GREEN, fontsize=10, fontweight="bold")
    ax.text(0.180, 0.105, "predicts which concepts are\nlikely to be available",
            transform=ax.transAxes, ha="center", va="center", fontsize=9.5)

    rounded_box(ax, (0.715, 0.075), 0.210, 0.096, edge=RULE, face=LIGHT, radius=0.012, lw=0.8)
    ax.text(0.820, 0.137, "PROMPT DEMANDS", transform=ax.transAxes,
            ha="center", va="center", color=BLUE, fontsize=10, fontweight="bold")
    ax.text(0.820, 0.105, "constrain whether available\nknowledge can be used",
            transform=ax.transAxes, ha="center", va="center", fontsize=9.5)

    ax.text(0.500, 0.145, "AVAILABLE  ≠  REACHABLE", transform=ax.transAxes,
            ha="center", va="center", fontsize=14, fontweight="bold")
    ax.text(0.500, 0.105, "Knowledge stated in one prompt\ndoes not always transfer to use",
            transform=ax.transAxes, ha="center", va="center", fontsize=9.5)
    ax.add_patch(FancyArrowPatch((0.300, 0.122), (0.390, 0.122), arrowstyle="-|>",
                                 mutation_scale=11, lw=1.2, linestyle=":", color=GREEN,
                                 transform=ax.transAxes))
    ax.add_patch(FancyArrowPatch((0.700, 0.122), (0.610, 0.122), arrowstyle="-|>",
                                 mutation_scale=11, lw=1.2, linestyle=":", color=BLUE,
                                 transform=ax.transAxes))

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"wrote {OUTPUT}")


if __name__ == "__main__":
    draw()
