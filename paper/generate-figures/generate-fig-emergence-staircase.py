#!/usr/bin/env python3
"""
Figure (Section 4): emergence staircase (replaces the paired-battery heatmap).

One row per accessibility concept that emerges (declarative 'correct') in at
least one family; a filled marker at the scale of first emergence, per family.
A family in which a registering concept never emerges shows an open ring in the
'Never emerges' lane (offset per family so the three do not stack). Concepts
that register in NO family are omitted for legibility; their count is preserved
in the subtitle.

Reads:  results/analysis/emergence_thresholds.csv
Writes: paper/figures/emergence-staircase.png

Run:  python paper/generate-figures/generate-fig-emergence-staircase.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from _figstyle import ANALYSIS_DIR, FIGURES_DIR, FAMILY_COLOR, apply_style
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import pandas as pd, numpy as np

apply_style()
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

PARAMS = {"124M": 0.124, "160M": 0.16, "355M": 0.355, "410M": 0.41, "774M": 0.774,
          "1B": 1.0, "1.5B": 1.5, "2.8B": 2.8, "6.9B": 6.9, "7B": 7.0, "12B": 12.0, "13B": 13.0}
FAMS = [("pythia_emergence", "pythia"), ("gpt2_emergence", "gpt2"), ("olmo_emergence", "olmo")]
NEVER_X = {"pythia": 26.0, "gpt2": 37.0, "olmo": 52.0}


def make_figure():
    df = pd.read_csv(ANALYSIS_DIR / "emergence_thresholds.csv")
    n_total = len(df)
    df["nemerge"] = df.apply(lambda r: sum(r[c] in PARAMS for c, _ in FAMS), axis=1)
    n_null = int((df.nemerge == 0).sum())
    df = df[df.nemerge > 0].copy()

    def emin(row):
        vals = [PARAMS[row[c]] for c, _ in FAMS if row[c] in PARAMS]
        return min(vals) if vals else np.inf
    df["_sort"] = df.apply(emin, axis=1)
    df = df.sort_values(["_sort", "nemerge"], ascending=[True, False]).reset_index(drop=True)

    n = len(df)
    fig, ax = plt.subplots(figsize=(9, max(6, n * 0.30)))
    xmin, xmax, divider = 0.10, 15.0, 18.0

    for yi, (_, row) in enumerate(df.iterrows()):
        y = n - 1 - yi
        ax.plot([xmin, xmax], [y, y], color="#eee", lw=0.8, zorder=0)
        for col, fam in FAMS:
            v, color = row[col], FAMILY_COLOR[fam]
            if v in PARAMS:
                ax.scatter(PARAMS[v], y, color=color, s=46, zorder=4,
                           edgecolor="white", linewidth=0.6)
            else:
                ax.scatter(NEVER_X[fam], y, facecolor="none", edgecolor=color, s=34,
                           linewidth=1.2, zorder=4)

    ax.set_yticks(range(n))
    ax.set_yticklabels([c.replace("_", " ") for c in df["concept"][::-1]], fontsize=8.4)
    ax.set_xscale("log")
    ax.set_xlim(xmin, 62)
    ax.set_xticks([0.124, 0.41, 1, 2.8, 6.9, 13])
    ax.set_xticklabels(["124M", "410M", "1B", "2.8B", "6.9B", "13B"], fontsize=9)
    ax.tick_params(axis="x", which="minor", bottom=False)

    ax.axvline(divider, color="#ccc", lw=1, ls=":")
    ax.text(np.sqrt(NEVER_X["pythia"] * NEVER_X["olmo"]), n - 0.3, "Never emerges",
            ha="center", fontsize=9.5, color="#666", style="italic")
    ax.set_xlabel("Scale at which the concept first emerges", fontsize=10.5, labelpad=8)
    ax.set_title("When accessibility concepts first emerge, by family",
                 fontsize=12.5, pad=26, color="#222")
    ax.text(0.5, 1.012,
            f"{n} of {n_total} concepts register in ≥1 family; the other {n_null} "
            f"emerge in no family at any scale (omitted).",
            transform=ax.transAxes, ha="center", va="bottom", fontsize=9, color="#777")

    leg = [Line2D([0], [0], marker="o", color="w", markerfacecolor=FAMILY_COLOR[f],
                  markersize=8, label=lab)
           for f, lab in [("pythia", "Pythia"), ("gpt2", "GPT-2"), ("olmo", "OLMo 2")]]
    leg.append(Line2D([0], [0], marker="o", color="w", markerfacecolor="none",
                      markeredgecolor="#666", markersize=8, label="never (in that family)"))
    ax.set_ylim(-1, n)
    fig.legend(handles=leg, frameon=False, fontsize=9.5, loc="lower center",
               ncol=4, columnspacing=1.4, handletextpad=0.3, bbox_to_anchor=(0.5, -0.015))
    fig.tight_layout(rect=[0, 0.02, 1, 1])
    out = FIGURES_DIR / "emergence-staircase.png"
    fig.savefig(out, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {out} | rows shown: {n} | omitted (null): {n_null}")


if __name__ == "__main__":
    make_figure()
