"""Visualizations for logit lens, decomposition, and per-head analysis.

Matplotlib-based plots designed for notebooks. Each function returns
the figure so you can save it or display inline.
"""

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd
from typing import Optional
plt.ioff()  # turn off interactive mode


# Consistent colors across all plots
COLORS = {
    "attn": "#2196F3",      # blue
    "mlp": "#FF9800",       # orange
    "target": "#4CAF50",    # green
    "suppression": "#F44336",  # red
    "neutral": "#9E9E9E",   # grey
}


def _save_if_path(fig: plt.Figure, save: Optional[str]) -> None:
    """Save figure if a path is provided."""
    if save:
        fig.savefig(save, dpi=150, bbox_inches="tight")
        print(f"Saved: {save}")


def plot_logit_lens(df: pd.DataFrame, figsize=(12, 5), save: Optional[str] = None) -> plt.Figure:
    """Plot target token rank and probability across layers.

    Two subplots:
      Left: target rank (log scale, inverted — rank 1 at top)
      Right: target probability

    The phase transition shows up as a sharp cliff on the left
    and a sharp spike on the right.
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)
    attrs = df.attrs
    model = attrs.get("model", "?")
    prompt = attrs.get("prompt", "?")
    target = attrs.get("target", "?")

    layers = df["layer"]

    # Left: rank (log scale, inverted)
    ax1.plot(layers, df["target_rank"], color=COLORS["target"],
             linewidth=2, marker="o", markersize=4)
    ax1.set_yscale("log")
    ax1.invert_yaxis()
    ax1.set_xlabel("Layer")
    ax1.set_ylabel("Target Rank (log, lower = better)")
    ax1.set_title("When does the model find the answer?")
    ax1.axhline(y=1, color=COLORS["neutral"], linestyle="--", alpha=0.5, label="Rank 1")
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Right: probability
    ax2.plot(layers, df["target_prob"], color=COLORS["target"],
             linewidth=2, marker="o", markersize=4)
    ax2.set_xlabel("Layer")
    ax2.set_ylabel("Target Probability")
    ax2.set_title("How confident is the model?")
    ax2.set_ylim(-0.05, max(df["target_prob"].max() * 1.1, 0.1))
    ax2.grid(True, alpha=0.3)

    fig.suptitle(f"{model}: \"{prompt}\" → \"{target}\"", fontsize=12, fontweight="bold")
    fig.tight_layout()
    _save_if_path(fig, save)
    return fig


def plot_decomposition(df: pd.DataFrame, figsize=(12, 5), save: Optional[str] = None) -> plt.Figure:
    """Plot attention vs MLP contribution per layer.

    Bars above zero push toward the target. Bars below zero suppress it.
    The story is in the balance — and especially in any layers where
    MLP goes negative while attention goes positive, or vice versa.
    """
    fig, ax = plt.subplots(figsize=figsize)
    attrs = df.attrs
    model = attrs.get("model", "?")
    target = attrs.get("target", "?")

    layers = df["layer"]
    width = 0.35

    ax.bar(layers - width/2, df["attn_logit"], width,
           label="Attention", color=COLORS["attn"], alpha=0.8)
    ax.bar(layers + width/2, df["mlp_logit"], width,
           label="MLP", color=COLORS["mlp"], alpha=0.8)

    ax.axhline(y=0, color="black", linewidth=0.5)
    ax.set_xlabel("Layer")
    ax.set_ylabel(f"Logit contribution → \"{target}\"")
    ax.set_title(f"{model}: Who's voting for \"{target}\"?")
    ax.legend()
    ax.grid(True, alpha=0.3, axis="y")

    fig.tight_layout()
    _save_if_path(fig, save)
    return fig


def plot_head_heatmap(df: pd.DataFrame, figsize=(14, 6), save: Optional[str] = None) -> plt.Figure:
    """Heatmap of per-head contributions: layer × head.

    Hot spots are heads strongly pushing toward the target.
    Cold spots are heads suppressing it.
    """
    attrs = df.attrs
    model = attrs.get("model", "?")
    target = attrs.get("target", "?")

    n_layers = df["layer"].max() + 1
    n_heads = df["head"].max() + 1

    # Pivot to 2D grid
    grid = df.pivot(index="layer", columns="head", values="logit").values

    fig, ax = plt.subplots(figsize=figsize)

    # Diverging colormap: blue (suppress) → white (neutral) → red (promote)
    vmax = max(abs(grid.min()), abs(grid.max()))
    im = ax.imshow(grid, cmap="RdBu_r", aspect="auto",
                   vmin=-vmax, vmax=vmax)

    ax.set_xlabel("Head")
    ax.set_ylabel("Layer")
    ax.set_title(f"{model}: Per-head contribution → \"{target}\"")
    ax.set_xticks(range(n_heads))
    ax.set_yticks(range(n_layers))

    plt.colorbar(im, ax=ax, label="Logit contribution")

    fig.tight_layout()
    _save_if_path(fig, save)
    return fig


def plot_phase_comparison(
    dfs: dict[str, pd.DataFrame],
    metric: str = "target_rank",
    figsize=(10, 5),
    save: Optional[str] = None,
) -> plt.Figure:
    """Compare logit lens results across models on the same axes.

    Pass in multiple logit lens DataFrames keyed by model name.
    Useful for seeing when different model sizes find the answer.

    Args:
        dfs: Dict mapping model name to logit_lens DataFrame.
        metric: "target_rank" or "target_prob"
        figsize: Figure size.
        save: Optional filepath to save the figure.
    """
    fig, ax = plt.subplots(figsize=figsize)
    colors = plt.cm.viridis(np.linspace(0, 0.85, len(dfs)))

    for (name, df), color in zip(dfs.items(), colors):
        # Normalize x-axis to [0, 1] so different-depth models align
        layers = df["layer"] / df["layer"].max()
        ax.plot(layers, df[metric], label=name, linewidth=2,
                marker="o", markersize=3, color=color)

    ax.set_xlabel("Relative depth (0 = first layer, 1 = last)")
    ax.set_ylabel(metric.replace("_", " ").title())

    if metric == "target_rank":
        ax.set_yscale("log")
        ax.invert_yaxis()
        ax.set_title("When does each model find the answer?")
    else:
        ax.set_title("How confident is each model?")

    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    _save_if_path(fig, save)
    return fig


def save_figures(
    model_name: str,
    target_label: str,
    logit_lens: Optional[pd.DataFrame] = None,
    decomposition: Optional[pd.DataFrame] = None,
    heads: Optional[pd.DataFrame] = None,
    out_dir: Optional[str] = None,
) -> list[str]:
    """Batch-save all analysis figures with consistent naming.

    Uses the convention: {target}-{analysis}.png inside a model directory.
    If out_dir is not specified, defaults to ../results/{model_name}/.
    Only generates/saves plots for DataFrames you pass in.

    Returns list of saved file paths.
    """
    import os
    if out_dir is None:
        out_dir = f"../results/{model_name}"
    os.makedirs(out_dir, exist_ok=True)

    saved = []

    plots = [
        (logit_lens, plot_logit_lens, "logit-lens"),
        (decomposition, plot_decomposition, "decomposition"),
        (heads, plot_head_heatmap, "head-heatmap"),
    ]

    for df, plot_fn, suffix in plots:
        if df is not None:
            path = os.path.join(out_dir, f"{target_label}-{suffix}.png")
            fig = plot_fn(df, save=path)
            plt.close(fig)
            saved.append(path)

    return saved
