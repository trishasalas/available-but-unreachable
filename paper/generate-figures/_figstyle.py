"""Shared plotting style + palette for the generated paper figures.

Palette conventions (Okabe-Ito, colorblind-safe). A palette swap is one edit here.
  Family axis  : Pythia=orange, GPT-2=purple, OLMo 2=green   (when family is a color series)
  Prompt axis  : Declarative=blue (solid), Evaluative=vermillion (dashed)
  Quality axis : Correct=grey (baseline), Incorrect=vermillion (signal)  — quality figures only

Paths are resolved relative to this file so scripts run from anywhere.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from pathlib import Path

PROJECT_DIR  = Path(__file__).resolve().parents[2]
ANALYSIS_DIR = PROJECT_DIR / "results" / "analysis"
RESULTS_DIR  = PROJECT_DIR / "results"
FIGURES_DIR  = PROJECT_DIR / "paper" / "figures"

OKABE = {
    "purple":  "#CC79A7",
    "blue":    "#0072B2",
    "skyblue": "#56B4E9",
    "green":   "#009E73",
    "yellow":  "#F0E442",
    "orange":  "#E69F00",
    "red":     "#D55E00",   # vermillion
    "grey":    "#7F7F7F",
}

DECL_COLOR = OKABE["blue"]     # declarative, solid
EVAL_COLOR = OKABE["red"]      # evaluative, dashed

FAMILY_COLOR = {"pythia": OKABE["orange"], "gpt2": OKABE["purple"], "olmo": OKABE["green"]}

CORRECT_COLOR   = OKABE["grey"]   # baseline
INCORRECT_COLOR = OKABE["red"]    # signal

_avail = {f.name for f in fm.fontManager.ttflist}
FONT = "Atkinson Hyperlegible" if "Atkinson Hyperlegible" in _avail else "DejaVu Sans"


def apply_style():
    plt.rcParams.update({
        "font.family":       FONT,
        "axes.spines.top":   False,
        "axes.spines.right": False,
        "figure.facecolor":  "white",
        "axes.facecolor":    "white",
        "axes.titlecolor":   "#333333",
    })
