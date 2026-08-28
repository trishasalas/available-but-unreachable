#!/usr/bin/env python3
"""Introduction figure: definition success does not transfer to application.

One line per confirmatory model connects two rates over the same eight concepts:

1. the share with a correct declarative definition;
2. the share passing the strict paired application criterion (both the
   violation and conformant item correct).

The script reads the cell-level analysis artifact and asserts the paper's
reported aggregate result before drawing: 35 correct declarative cells and
zero strict paired-application passes across 96 confirmatory model-concept
cells. Colors use the Okabe-Ito colorblind-safe palette.

Data:   results/analysis/paired_gap_cells.csv
Writes: paper/figures/introduction-knowledge-use-gap.png
"""

from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "results" / "analysis" / "paired_gap_cells.csv"
OUTPUT = ROOT / "paper" / "figures" / "introduction-knowledge-use-gap.png"

# Okabe-Ito colorblind-safe palette, matching the paper's other figures.
OI = {
    "orange": "#E69F00",
    "sky_blue": "#56B4E9",
    "bluish_green": "#009E73",
    "yellow": "#F0E442",
    "blue": "#0072B2",
    "vermillion": "#D55E00",
    "reddish_purple": "#CC79A7",
    "black": "#000000",
}

FAMILY_ORDER = ["pythia", "gpt2", "olmo"]
FAMILY_LABEL = {
    "pythia": "Pythia",
    "gpt2": "GPT-2",
    "olmo": "OLMo 2",
}
FAMILY_COLOR = {
    "pythia": OI["orange"],
    "gpt2": OI["reddish_purple"],
    "olmo": OI["bluish_green"],
}

MODEL_ORDER = {
    "pythia-160m": 0,
    "pythia-410m": 1,
    "pythia-1b": 2,
    "pythia-6.9b": 3,
    "pythia-12b": 4,
    "gpt2": 5,
    "gpt2-medium": 6,
    "gpt2-large": 7,
    "gpt2-xl": 8,
    "OLMo-2-0425-1B": 9,
    "OLMo-2-1124-7B": 10,
    "OLMo-2-1124-13B": 11,
}

INK = "#202124"
FAMILY_X_OFFSET = {
    "pythia": -0.025,
    "gpt2": 0.0,
    "olmo": 0.025,
}

available_fonts = {font.name for font in fm.fontManager.ttflist}
FONT = (
    "Atkinson Hyperlegible"
    if "Atkinson Hyperlegible" in available_fonts
    else "DejaVu Sans"
)

plt.rcParams.update(
    {
        "font.family": FONT,
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "axes.edgecolor": INK,
        "axes.labelcolor": INK,
        "xtick.color": INK,
        "ytick.color": INK,
        "text.color": INK,
        "font.size": 11,
    }
)


def as_bool(value: str) -> bool:
    return value.strip().lower() == "true"


def load_model_rates() -> list[dict[str, object]]:
    with DATA.open(newline="", encoding="utf-8") as handle:
        rows = [
            row
            for row in csv.DictReader(handle)
            if as_bool(row["confirmatory"])
        ]

    assert len(rows) == 96, f"expected 96 confirmatory cells, found {len(rows)}"
    assert sum(as_bool(row["declarative_pass"]) for row in rows) == 35
    assert sum(as_bool(row["evaluative_pass"]) for row in rows) == 0

    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[row["model"]].append(row)

    rates = []
    for model, model_rows in grouped.items():
        assert len(model_rows) == 8, f"expected 8 concepts for {model}"
        suite = model_rows[0]["suite"]
        rates.append(
            {
                "model": model,
                "suite": suite,
                "definition": 100
                * sum(as_bool(row["declarative_pass"]) for row in model_rows)
                / len(model_rows),
                "application": 100
                * sum(as_bool(row["evaluative_pass"]) for row in model_rows)
                / len(model_rows),
            }
        )

    rates.sort(key=lambda row: MODEL_ORDER[str(row["model"])])
    assert len(rates) == 12, f"expected 12 confirmatory models, found {len(rates)}"
    return rates


def make_figure() -> None:
    rates = load_model_rates()
    fig, ax = plt.subplots(figsize=(8.2, 5.3))

    # Draw low-definition models first so denser, higher trajectories stay legible.
    for row in sorted(rates, key=lambda item: float(item["definition"])):
        suite = str(row["suite"])
        color = FAMILY_COLOR[suite]
        offset = FAMILY_X_OFFSET[suite]
        x = [0 + offset, 1 + offset]
        y = [float(row["definition"]), float(row["application"])]
        ax.plot(
            x,
            y,
            color=color,
            linewidth=2.0,
            alpha=0.72,
            zorder=2,
        )
        ax.scatter(
            x,
            y,
            s=70,
            color=color,
            edgecolor="white",
            linewidth=0.8,
            alpha=0.90,
            zorder=3,
        )

    # Aggregate markers summarize the cell counts without replacing the raw models.
    aggregate_definition = 100 * 35 / 96
    aggregate_application = 0.0
    aggregate_x = [0, 1]
    ax.scatter(
        aggregate_x,
        [aggregate_definition, aggregate_application],
        s=145,
        marker="D",
        facecolor="white",
        edgecolor=OI["black"],
        linewidth=2.0,
        zorder=5,
    )
    ax.text(
        -0.045,
        aggregate_definition + 4.0,
        "35 / 96",
        ha="center",
        va="bottom",
        fontsize=10.5,
        fontweight="bold",
    )
    ax.text(
        1.0,
        aggregate_application + 4.0,
        "0 / 96",
        ha="center",
        va="bottom",
        fontsize=10.5,
        fontweight="bold",
    )

    ax.set_xlim(-0.22, 1.22)
    ax.set_ylim(-5, 105)
    ax.set_xticks([0, 1])
    ax.set_xticklabels(["Correct definition", "Passed both\napplication items"])
    ax.tick_params(axis="x", length=0, pad=10)
    ax.set_yticks([0, 25, 50, 75, 100])
    ax.set_yticklabels(["0", "25", "50", "75", "100"])
    ax.set_ylabel("Model–concept cells passing criterion (%)")

    ax.grid(False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_linewidth(1.1)
    ax.spines["bottom"].set_linewidth(1.1)

    family_handles = [
        Line2D(
            [0],
            [0],
            marker="o",
            linestyle="-",
            color=FAMILY_COLOR[family],
            markerfacecolor=FAMILY_COLOR[family],
            markeredgecolor="white",
            linewidth=2.0,
            markersize=7,
            label=FAMILY_LABEL[family],
        )
        for family in FAMILY_ORDER
    ]
    family_handles.append(
        Line2D(
            [0],
            [0],
            marker="D",
            linestyle="none",
            color=OI["black"],
            markerfacecolor="white",
            markeredgecolor=OI["black"],
            markeredgewidth=1.5,
            markersize=7,
            label="All cells",
        )
    )
    ax.legend(
        handles=family_handles,
        loc="upper right",
        frameon=False,
        fontsize=10.5,
        handlelength=2.0,
    )

    fig.tight_layout()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Saved: {OUTPUT}")


if __name__ == "__main__":
    make_figure()
