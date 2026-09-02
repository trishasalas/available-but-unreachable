"""Introduction figure: corpus frequency does not order the three 12B outcomes.

A dot plot. One row per compound on a log-scaled Pile bigram-count axis,
each marked by what Pythia-12B did with "<X> is not accessible because":
correct, fluent but wrong, or a 404 template. The point is that correctness
is not monotone in frequency: the rarest compound fails, and so does the
most frequent one. Completions are kept out of the panel;
the companion markdown table carries them.

The script asserts the paper's stated counts before drawing (skip link 662,
alt text 23,306, screen reader 32,100) and that the generations file holds
exactly these three 12B completions. Outcome labels are the author's
judgment, not data, and live in OUTCOME below.

Data:   results/logits/pythia/pythia-12b_because_generations.csv
        results/frequency/frequency_table.csv
Output: paper/figures/intro-frequency-outcome.png
        paper/figures/intro-frequency-outcome-table.md  (Pandoc pipe table with width ratios)
"""

from __future__ import annotations

import re

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.lines import Line2D

from _figstyle import CORRECT_COLOR, INCORRECT_COLOR, FIGURES_DIR, RESULTS_DIR, apply_style

GENERATIONS = RESULTS_DIR / "logits" / "pythia" / "pythia-12b_because_generations.csv"
FREQUENCY = RESULTS_DIR / "frequency" / "frequency_table.csv"
OUT_PNG = FIGURES_DIR / "intro-frequency-outcome.png"
OUT_TABLE = FIGURES_DIR / "intro-frequency-outcome-table.md"

MODEL = "pythia-12b"

# Paper-stated counts; the assert below guards the prose against the CSV drifting.
EXPECTED_COUNTS = {"skip_link": 662, "alt_text": 23306, "screen_reader": 32100}

DISPLAY = {"skip_link": "skip link", "alt_text": "alt text", "screen_reader": "screen reader"}

# Author's coding of each 12B completion. Judgment, not data.
OUTCOME = {
    "alt_text": "correct",
    "screen_reader": "fluent_wrong",
    "skip_link": "template",
}

OUTCOME_LABEL = {
    "correct": "correct",
    "fluent_wrong": "fluent, wrong",
    "template": "404 template, wrong",
}

# Quality axis per _figstyle: correct = grey baseline, incorrect = vermillion.
# Shape carries the correct/wrong split without color; fill separates the two wrong kinds.
MARKER = {
    "correct":      dict(marker="o", facecolor=CORRECT_COLOR,   edgecolor=CORRECT_COLOR),
    "fluent_wrong": dict(marker="D", facecolor=INCORRECT_COLOR, edgecolor=INCORRECT_COLOR),
    "template":     dict(marker="D", facecolor="white",         edgecolor=INCORRECT_COLOR),
}

# The pair whose near-identical frequency is the figure's point; bracketed between rows.
PAIR = ("alt_text", "screen_reader")

GRID = dict(color="#BBBBBB", linestyle="--", linewidth=0.7, alpha=0.6)
INK = "#333333"

# Relative column widths for the companion table. Pandoc reads the dash counts in a
# pipe table's separator row as width ratios whenever any row exceeds --columns (72),
# which the skip-link quote guarantees. Ratios matter, not absolute counts.
TABLE_COLUMNS = (
    ("Compound", 6, "left"),
    ("Pile count", 5, "right"),
    ("Pythia-12B completion", 32, "left"),
    ("Outcome", 8, "left"),
)


def load_rows() -> pd.DataFrame:
    gens = pd.read_csv(GENERATIONS)
    gens = gens[gens["model"] == MODEL]
    assert set(gens["compound"]) == set(EXPECTED_COUNTS), sorted(gens["compound"])
    assert len(gens) == 3, len(gens)

    freq = pd.read_csv(FREQUENCY)[["compound", "bigram_count"]]
    rows = gens.merge(freq, on="compound", how="left", validate="one_to_one")
    assert rows["bigram_count"].notna().all(), rows

    for compound, expected in EXPECTED_COUNTS.items():
        actual = int(rows.loc[rows["compound"] == compound, "bigram_count"].iloc[0])
        assert actual == expected, (compound, actual, expected)

    rows["outcome"] = rows["compound"].map(OUTCOME)
    rows["display"] = rows["compound"].map(DISPLAY)
    return rows.sort_values("bigram_count").reset_index(drop=True)


def first_sentence(text: str) -> str:
    """Collapse whitespace and keep the completion up to its first period."""
    flat = re.sub(r"\s+", " ", text).strip()
    end = flat.find(".")
    return flat if end == -1 else flat[: end + 1]


def row_y(i: int, n: int) -> int:
    """Rows run rarest at top so the upper-right corner stays free for the legend."""
    return n - 1 - i


def draw_pair_bracket(ax: plt.Axes, rows: pd.DataFrame) -> None:
    """Dimension line between the near-tied pair's rows, stating the ratio."""
    idx = {c: row_y(i, len(rows)) for i, c in enumerate(rows["compound"])}
    counts = rows.set_index("compound")["bigram_count"]
    (lo_c, lo), (hi_c, hi) = sorted(((c, int(counts[c])) for c in PAIR), key=lambda t: t[1])
    y = (idx[lo_c] + idx[hi_c]) / 2
    grey = "#8C8C8C"
    ax.plot([lo, hi], [y, y], color=grey, linewidth=0.9, zorder=2)
    for x in (lo, hi):
        ax.plot([x, x], [y - 0.12, y + 0.12], color=grey, linewidth=0.9, zorder=2)
    ax.annotate(f"{hi / lo:.1f}\u00d7 apart", xy=(lo, y), xytext=(-8, 0),
                textcoords="offset points", ha="right", va="center",
                fontsize=8.5, color=grey)





def make_figure(rows: pd.DataFrame) -> None:
    apply_style()
    fig, ax = plt.subplots(figsize=(7.0, 2.6))

    for i, row in rows.iterrows():
        style = MARKER[row["outcome"]]
        ax.scatter(
            row["bigram_count"], row_y(i, len(rows)),
            s=110, marker=style["marker"],
            facecolor=style["facecolor"], edgecolor=style["edgecolor"],
            linewidth=1.6, zorder=3,
        )

    draw_pair_bracket(ax, rows)

    ax.set_xscale("log")
    ax.set_xlim(1e2, 1e5)
    ax.set_xticks([1e2, 1e3, 1e4, 1e5])
    ax.set_xticklabels(["100", "1k", "10k", "100k"])
    ax.minorticks_off()
    ax.set_xlabel("Bigram count in The Pile (log scale)", fontsize=9.5, color=INK)

    ax.set_ylim(-0.6, len(rows) - 0.05)
    ax.set_yticks([row_y(i, len(rows)) for i in range(len(rows))])
    ax.set_yticklabels(rows["display"])
    ax.tick_params(axis="both", labelsize=9, colors=INK)
    ax.grid(True, axis="both", **GRID)
    ax.set_axisbelow(True)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(INK)

    handles = [
        Line2D(
            [0], [0], linestyle="none",
            marker=MARKER[key]["marker"],
            markerfacecolor=MARKER[key]["facecolor"],
            markeredgecolor=MARKER[key]["edgecolor"],
            markeredgewidth=1.4, markersize=5,
            label=OUTCOME_LABEL[key],
        )
        for key in ("correct", "fluent_wrong", "template")
    ]
    legend = ax.legend(
        handles=handles, title="",
        loc="upper right", frameon=True, fancybox=False, framealpha=1.0,
        edgecolor="#CCCCCC", fontsize=8, title_fontsize=7,
        handletextpad=0.5, borderpad=0.7, labelspacing=0.5,
    )
    legend.get_title().set_ha("left")

    fig.tight_layout()
    OUT_PNG.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT_PNG, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"wrote {OUT_PNG}")


def table_separator() -> str:
    """Build the separator row; a trailing colon right-aligns a column in Pandoc."""
    cells = []
    for _, width, align in TABLE_COLUMNS:
        dashes = "-" * width
        cells.append(dashes + ":" if align == "right" else dashes)
    return "| " + " | ".join(cells) + " |"


def write_table(rows: pd.DataFrame) -> None:
    header = "| " + " | ".join(name for name, _, _ in TABLE_COLUMNS) + " |"
    lines = [header, table_separator()]
    for _, row in rows.iterrows():
        completion = first_sentence(row["generation_text"])
        lines.append(
            f"| {row['display']} | {int(row['bigram_count']):,} | "
            f"\u201c\u2026{completion}\u201d | {OUTCOME_LABEL[row['outcome']]} |"
        )
    OUT_TABLE.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {OUT_TABLE}")
    print()
    print("\n".join(lines))


def main() -> None:
    rows = load_rows()
    make_figure(rows)
    write_table(rows)


if __name__ == "__main__":
    main()
