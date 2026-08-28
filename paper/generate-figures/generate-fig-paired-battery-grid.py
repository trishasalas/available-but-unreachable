"""Paired-battery outcome grid.

One cell per model-by-concept pair in the frozen paired battery.
Cell color encodes the evaluative outcome (neither item correct,
conformant only, violation only, or both). A black dot marks cells
where the same model gave a correct declarative response for the
same concept. The twelve confirmatory models are separated from the
development-exposed Pythia-2.8B pilot by a vertical rule.

The script asserts the paper's reported counts before drawing:
85 neither / 7 conformant-only / 4 violation-only / 0 both, and
35 declarative passes, across the 96 confirmatory cells.

Data: results/analysis/paired_gap_cells.csv
Output: paper/figures/paired-battery-grid.png
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "results" / "analysis" / "paired_gap_cells.csv"
OUT = Path(__file__).resolve().parents[1] / "figures" / "paired-battery-grid.png"

# Column order: family blocks, ascending scale; pilot last, after a rule.
MODEL_ORDER = [
    ("pythia-160m", "Pythia 160M"),
    ("pythia-410m", "Pythia 410M"),
    ("pythia-1b", "Pythia 1B"),
    ("pythia-6.9b", "Pythia 6.9B"),
    ("pythia-12b", "Pythia 12B"),
    ("gpt2", "GPT-2 124M"),
    ("gpt2-medium", "GPT-2 355M"),
    ("gpt2-large", "GPT-2 774M"),
    ("gpt2-xl", "GPT-2 1.5B"),
    ("OLMo-2-0425-1B", "OLMo 2 1B"),
    ("OLMo-2-1124-7B", "OLMo 2 7B"),
    ("OLMo-2-1124-13B", "OLMo 2 13B"),
    ("pythia-2.8b", "Pythia 2.8B\n(pilot)"),
]

CONCEPT_ORDER = [
    "alt text",
    "closed captions",
    "color contrast",
    "focus indicator",
    "keyboard navigation",
    "screen reader",
    "semantic HTML",
    "skip link",
]

# Okabe-Ito colorblind-safe palette (matplotlib)
okabe_ito = {
    "purple":    "#CC79A7",
    "blue":      "#0072B2",
    "skyblue":   "#56B4E9",
    "green":     "#009E73",
    "yellow":    "#F0E442",
    "orange":    "#E69F00",
    "red":       "#D55E00",
}

# Outcome colors are scoped to this figure. The blues echo the paper's
# measurement-pair convention (dark member / light member); "both" is black
# so the single passing cell is maximally salient and survives grayscale.
# Family colors (orange/purple/green) are deliberately not used here.
CATEGORY_COLORS = {
    "neither": "#e8e8e8",
    "conformant only": okabe_ito["skyblue"],
    "violation only": okabe_ito["blue"],
    "both": "black",
}
CATEGORY_INDEX = {name: i for i, name in enumerate(CATEGORY_COLORS)}


def outcome(row: pd.Series) -> str:
    if row["violation_correct"] and row["conformant_correct"]:
        return "both"
    if row["violation_correct"]:
        return "violation only"
    if row["conformant_correct"]:
        return "conformant only"
    return "neither"


def main() -> None:
    df = pd.read_csv(DATA)
    df["outcome"] = df.apply(outcome, axis=1)

    # Self-check against the paper's reported counts (confirmatory set).
    conf = df[df["confirmatory"]]
    counts = conf["outcome"].value_counts()
    assert len(conf) == 96, f"expected 96 confirmatory cells, got {len(conf)}"
    assert counts.get("neither", 0) == 85, counts.to_dict()
    assert counts.get("conformant only", 0) == 7, counts.to_dict()
    assert counts.get("violation only", 0) == 4, counts.to_dict()
    assert counts.get("both", 0) == 0, counts.to_dict()
    assert int(conf["declarative_pass"].sum()) == 35, int(
        conf["declarative_pass"].sum()
    )

    n_rows = len(CONCEPT_ORDER)
    n_cols = len(MODEL_ORDER)
    grid = np.zeros((n_rows, n_cols), dtype=int)
    dots_light_bg = []
    dots_dark_bg = []

    lookup = df.set_index(["model", "concept"])
    for c, (model_key, _) in enumerate(MODEL_ORDER):
        for r, concept in enumerate(CONCEPT_ORDER):
            row = lookup.loc[(model_key, concept)]
            grid[r, c] = CATEGORY_INDEX[row["outcome"]]
            if bool(row["declarative_pass"]):
                target = dots_dark_bg if row["outcome"] == "both" else dots_light_bg
                target.append((c, r))

    fig, ax = plt.subplots(figsize=(10.5, 4.2))
    cmap = plt.matplotlib.colors.ListedColormap(list(CATEGORY_COLORS.values()))
    ax.imshow(grid, cmap=cmap, vmin=0, vmax=len(CATEGORY_COLORS) - 1, aspect="auto")

    if dots_light_bg:
        xs, ys = zip(*dots_light_bg)
        ax.scatter(xs, ys, s=28, c="black", zorder=3)
    if dots_dark_bg:
        xs, ys = zip(*dots_dark_bg)
        ax.scatter(xs, ys, s=28, c="white", zorder=3)

    # White gridlines between cells.
    ax.set_xticks(np.arange(-0.5, n_cols, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, n_rows, 1), minor=True)
    ax.grid(which="minor", color="white", linewidth=1.4)
    ax.tick_params(which="minor", length=0)

    # Rule separating the confirmatory set from the pilot column.
    ax.axvline(n_cols - 1.5, color="black", linewidth=1.6)

    ax.set_xticks(range(n_cols))
    ax.set_xticklabels([label for _, label in MODEL_ORDER], rotation=45, ha="right")
    ax.set_yticks(range(n_rows))
    ax.set_yticklabels(CONCEPT_ORDER)
    ax.tick_params(length=0)
    for spine in ax.spines.values():
        spine.set_visible(False)

    legend_handles = [
        Patch(facecolor=color, label=name)
        for name, color in CATEGORY_COLORS.items()
    ] + [
        Line2D(
            [0],
            [0],
            marker="o",
            color="none",
            markerfacecolor="black",
            markersize=6,
            label="declarative pass",
        )
    ]
    ax.legend(
        handles=legend_handles,
        loc="upper center",
        bbox_to_anchor=(0.5, -0.32),
        ncol=5,
        frameon=False,
        fontsize=8,
    )

    fig.tight_layout()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=300, bbox_inches="tight")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
