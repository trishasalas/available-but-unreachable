"""Frequency-binding correlations across all thirteen model-scale points.

One dot per model: the Spearman correlation between log bigram
frequency and the 95th-percentile late-layer value-weighted binding
measure, with bootstrap confidence intervals. Every dot sits left of
zero. Per-model intervals vary in width; the aggregate significance
claim (p = 0.0003) comes from the preregistered shared-label
permutation test described in Methods, not from any single interval.

The script asserts the paper's claim before drawing: exactly thirteen
model-scale points, all with negative correlations, matching Table 5.

Data: results/analysis/effective_binding_correlations_natural.csv
Output: paper/figures/binding-frequency-forest.png
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "results" / "analysis" / "effective_binding_correlations_natural.csv"
OUT = Path(__file__).resolve().parents[1] / "figures" / "binding-frequency-forest.png"

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

# Display order matches Table 5: GPT-2, OLMo 2, Pythia, ascending scale.
MODEL_ORDER = [
    ("gpt2", "GPT-2 124M"),
    ("gpt2-medium", "GPT-2 355M"),
    ("gpt2-large", "GPT-2 774M"),
    ("gpt2-xl", "GPT-2 1.5B"),
    ("OLMo-2-0425-1B", "OLMo 2 1B"),
    ("OLMo-2-1124-7B", "OLMo 2 7B"),
    ("OLMo-2-1124-13B", "OLMo 2 13B"),
    ("pythia-160m", "Pythia 160M"),
    ("pythia-410m", "Pythia 410M"),
    ("pythia-1b", "Pythia 1B"),
    ("pythia-2.8b", "Pythia 2.8B"),
    ("pythia-6.9b", "Pythia 6.9B"),
    ("pythia-12b", "Pythia 12B"),
]

# Paper-wide meaning: families are orange / purple / green.
FAMILY_COLORS = {
    "gpt2": okabe_ito["purple"],
    "olmo": okabe_ito["green"],
    "pythia": okabe_ito["orange"],
}

def main() -> None:
    df = pd.read_csv(DATA)
    df = df[df["measure"] == "p95_relative"].set_index("model")

    # Self-check against the paper's claim.
    assert len(df) == 13, f"expected 13 model-scale points, got {len(df)}"
    assert (df["rho"] < 0).all(), "expected all thirteen correlations negative"

    fig, ax = plt.subplots(figsize=(6.5, 4.6))

    # Leave a blank slot between family blocks.
    y = 0
    positions, labels = [], []
    prev_family = None
    for model_key, label in MODEL_ORDER:
        row = df.loc[model_key]
        if prev_family is not None and row["family"] != prev_family:
            y += 1
        prev_family = row["family"]
        color = FAMILY_COLORS[row["family"]]
        ax.errorbar(
            row["rho"],
            y,
            xerr=[[row["rho"] - row["ci_low"]], [row["ci_high"] - row["rho"]]],
            fmt="o",
            color=color,
            ecolor=color,
            elinewidth=1.4,
            capsize=3,
            markersize=6,
        )
        positions.append(y)
        labels.append(label)
        y += 1

    ax.axvline(0, color="black", linewidth=1, linestyle="--")
    ax.set_yticks(positions)
    ax.set_yticklabels(labels)
    ax.invert_yaxis()
    ax.set_xlabel(
        "Spearman $\\rho$: log bigram frequency vs.\n"
        "late-layer value-weighted binding (95th percentile)"
    )
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_xlim(-0.75, 0.25)

    fig.tight_layout()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=300, bbox_inches="tight")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
