"""Per-head attention decomposition: which heads are voting for the target?

Goes one level deeper than decompose.py — instead of total attention
contribution per layer, breaks it down to individual attention heads.

This is where you find factual recall heads, induction heads, and other
specific circuits responsible for the model's behavior.
"""

import torch
import pandas as pd
from transformer_lens import HookedTransformer


def per_head_contributions(
    model: HookedTransformer,
    cache,
    target: str,
    position: int = -1,
) -> pd.DataFrame:
    """Decompose each attention head's contribution to the target token.

    Each head's output is projected through W_U to see how much it
    individually pushes toward (or away from) the target.

    Args:
        model: A loaded HookedTransformer.
        cache: Activation cache from model.run_with_cache().
        target: Target token with leading space, e.g. " Paris"
        position: Token position to analyze. Default -1 (last token).

    Returns:
        DataFrame with columns:
            layer, head, logit, abs_logit
        Sorted by absolute contribution (strongest first).
    """
    target_token = model.to_single_token(target)

    rows = []
    for layer in range(model.cfg.n_layers):
        # hook_z is pre-output-projection: (batch, pos, n_heads, d_head)
        # We need to project each head through W_O then W_U to get logit contribution
        z = cache["z", layer][0, position]  # (n_heads, d_head)
        W_O = model.blocks[layer].attn.W_O  # (n_heads, d_head, d_model)

        for head in range(model.cfg.n_heads):
            # Project through this head's output matrix to get d_model vector
            head_out = z[head] @ W_O[head]  # (d_model,)
            logit = (head_out @ model.unembed.W_U)[target_token].item()

            rows.append({
                "layer": layer,
                "head": head,
                "logit": logit,
                "abs_logit": abs(logit),
            })

    df = pd.DataFrame(rows)
    df.attrs["model"] = model.cfg.model_name
    df.attrs["target"] = target
    df.attrs["target_token_id"] = int(target_token)

    return df


def top_heads(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """Return the n heads with the largest absolute contribution."""
    return df.nlargest(n, "abs_logit").reset_index(drop=True)


def layer_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Summarize per-head contributions by layer.

    Shows total attention contribution (sum of all heads), the
    peak head, and how concentrated the contribution is.

    Returns:
        DataFrame with columns:
            layer, total_logit, peak_head, peak_logit,
            peak_share (what fraction of the layer's total came from one head)
    """
    rows = []
    for layer, group in df.groupby("layer"):
        total = group["logit"].sum()
        peak_idx = group["abs_logit"].idxmax()
        peak_head = group.loc[peak_idx, "head"]
        peak_logit = group.loc[peak_idx, "logit"]

        # How much of this layer's contribution comes from one head?
        abs_total = group["abs_logit"].sum()
        peak_share = group.loc[peak_idx, "abs_logit"] / abs_total if abs_total > 0 else 0

        rows.append({
            "layer": int(layer),
            "total_logit": total,
            "peak_head": int(peak_head),
            "peak_logit": peak_logit,
            "peak_share": peak_share,
        })

    return pd.DataFrame(rows)


def print_top_heads(df: pd.DataFrame, n: int = 10) -> None:
    """Pretty-print the top contributing heads."""
    attrs = df.attrs
    print(f"Model: {attrs.get('model', '?')}")
    print(f"Target: \"{attrs.get('target', '?')}\"")
    print(f"\nTop {n} attention heads by contribution:")
    print(f"{'Layer':<8} {'Head':<8} {'Logit':<12}")
    print("-" * 28)
    for _, row in top_heads(df, n).iterrows():
        print(f"{row['layer']:<8} {row['head']:<8} {row['logit']:<12.4f}")


def print_layer_summary(df: pd.DataFrame) -> None:
    """Pretty-print the layer summary."""
    summary = layer_summary(df)
    attrs = df.attrs
    print(f"Model: {attrs.get('model', '?')}")
    print(f"Target: \"{attrs.get('target', '?')}\"")
    print(f"\n{'Layer':<8} {'Total':<12} {'Peak Head':<12} {'Peak Logit':<14} {'Concentration':<14}")
    print("-" * 60)
    for _, row in summary.iterrows():
        print(f"{row['layer']:<8} {row['total_logit']:<12.4f} "
              f"L{row['layer']}H{row['peak_head']:<7} "
              f"{row['peak_logit']:<14.4f} {row['peak_share']:<14.1%}")
