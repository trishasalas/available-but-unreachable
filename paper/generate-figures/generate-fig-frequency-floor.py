"""Corpus frequency against declarative accuracy, three families.

One panel per family: log-scaled bigram count against mean declarative
accuracy for all 49 compounds. The upward trend is the frequency floor;
the vertical spread at similar counts is what frequency leaves
unexplained. Panel annotations carry the Spearman correlations read
from the frozen summary table.

The script asserts the paper's claims before drawing: 49 compounds per
family, and all-rows Spearman correlations matching the reported
0.5875 / 0.5194 / 0.5823 with p < 0.001.

Data: results/frequency/{pythia,gpt2,olmo}_frequency_accuracy.csv
      results/frequency/spearman_summary.csv
Output: paper/figures/frequency-floor.png
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
FREQ = ROOT / "results" / "frequency"
OUT = Path(__file__).resolve().parents[1] / "figures" / "frequency-floor.png"

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

# Paper-wide meaning: families are orange / purple / green.
PANELS = [
    ("pythia", "Pythia (Pile counts)", okabe_ito["orange"], 0.5875),
    ("gpt2", "GPT-2 (Pile counts, proxy)", okabe_ito["purple"], 0.5194),
    ("olmo", "OLMo 2 (OLMo-Mix counts)", okabe_ito["green"], 0.5823),
]


def main() -> None:
    summary = pd.read_csv(FREQ / "spearman_summary.csv")
    summary = summary[summary["sense_split"] == "all_rows"].set_index("suite")

    fig, axes = plt.subplots(1, 3, figsize=(10.5, 3.6), sharey=True)

    for ax, (suite, title, color, expected_rho) in zip(axes, PANELS):
        df = pd.read_csv(FREQ / f"{suite}_frequency_accuracy.csv")
        assert len(df) == 49, f"{suite}: expected 49 compounds, got {len(df)}"

        row = summary.loc[suite]
        assert abs(row["spearman_rho"] - expected_rho) < 1e-4, (
            suite,
            row["spearman_rho"],
        )
        assert row["spearman_p"] < 0.001, (suite, row["spearman_p"])

        ax.scatter(
            df["bigram_count"],
            df["mean_accuracy"],
            s=26,
            color=color,
            alpha=0.75,
            edgecolors="none",
        )
        ax.set_xscale("log")
        ax.set_title(title, fontsize=10)
        ax.annotate(
            f"Spearman $\\rho$ = {row['spearman_rho']:.2f}",
            xy=(0.04, 0.92),
            xycoords="axes fraction",
            fontsize=9,
        )
        ax.set_xlabel("Bigram count (log scale)")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    axes[0].set_ylabel("Mean declarative accuracy")
    axes[0].set_ylim(-0.05, 1.05)

    fig.tight_layout()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=300, bbox_inches="tight")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
