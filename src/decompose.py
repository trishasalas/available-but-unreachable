"""Attention vs MLP decomposition: who's voting for the target token?

At each layer, projects the attention output and MLP output separately
through the unembedding matrix to measure their individual contribution
to the target token's logit.

NOTE on architecture:
  - GPT-2 (sequential): MLP sees attention's output. The MLP contribution
    includes refinement of what attention found.
  - Pythia (parallel): Attention and MLP read the same input independently.
    Neither component sees the other's output within the same layer.

This matters for interpretation. A large MLP contribution in GPT-2 could
mean "MLP stored this fact" OR "MLP amplified what attention retrieved."
In Pythia, contributions are genuinely independent within a layer.
"""

import torch
import pandas as pd
from transformer_lens import HookedTransformer


def decompose_contributions(
    model: HookedTransformer,
    cache,
    target: str,
    position: int = -1,
) -> pd.DataFrame:
    """Decompose attention vs MLP contribution to a target token at each layer.

    Projects each component's output through the unembedding matrix (W_U)
    to see its direct "vote" for the target token. Skips layer norm to
    measure raw contributions to the residual stream.

    Args:
        model: A loaded HookedTransformer.
        cache: Activation cache from model.run_with_cache().
        target: Target token with leading space, e.g. " Paris"
        position: Token position to analyze. Default -1 (last token).

    Returns:
        DataFrame with columns:
            layer, attn_logit, mlp_logit, dominant
    """
    target_token = model.to_single_token(target)

    rows = []
    for layer in range(model.cfg.n_layers):
        attn_out = cache["attn_out", layer][0, position]
        mlp_out = cache["mlp_out", layer][0, position]

        # Project each through unembedding to get logit contribution
        attn_logit = (attn_out @ model.unembed.W_U)[target_token].item()
        mlp_logit = (mlp_out @ model.unembed.W_U)[target_token].item()

        dominant = "ATTN" if abs(attn_logit) > abs(mlp_logit) else "MLP"

        rows.append({
            "layer": layer,
            "attn_logit": attn_logit,
            "mlp_logit": mlp_logit,
            "dominant": dominant,
        })

    df = pd.DataFrame(rows)
    df.attrs["model"] = model.cfg.model_name
    df.attrs["target"] = target
    df.attrs["target_token_id"] = int(target_token)

    return df


def print_decomposition(df: pd.DataFrame) -> None:
    """Pretty-print a decomposition DataFrame."""
    attrs = df.attrs
    print(f"Model: {attrs.get('model', '?')}")
    print(f"Target: \"{attrs.get('target', '?')}\"")
    print()
    print(f"{'Layer':<8} {'Attn→Target':<16} {'MLP→Target':<16} {'Dominant':<10}")
    print("-" * 50)
    for _, row in df.iterrows():
        print(f"{row['layer']:<8} {row['attn_logit']:<16.4f} "
              f"{row['mlp_logit']:<16.4f} {row['dominant']:<10}")


def summarize_contributions(df: pd.DataFrame) -> dict:
    """Quick summary stats for a decomposition.

    Returns dict with:
        total_attn: sum of all attention logit contributions
        total_mlp: sum of all MLP logit contributions
        peak_attn_layer: layer with largest absolute attention contribution
        peak_mlp_layer: layer with largest absolute MLP contribution
        attn_dominant_count: number of layers where attention dominates
        mlp_dominant_count: number of layers where MLP dominates
    """
    return {
        "total_attn": df["attn_logit"].sum(),
        "total_mlp": df["mlp_logit"].sum(),
        "peak_attn_layer": int(df["attn_logit"].abs().idxmax()),
        "peak_attn_value": df.loc[df["attn_logit"].abs().idxmax(), "attn_logit"],
        "peak_mlp_layer": int(df["mlp_logit"].abs().idxmax()),
        "peak_mlp_value": df.loc[df["mlp_logit"].abs().idxmax(), "mlp_logit"],
        "attn_dominant_count": (df["dominant"] == "ATTN").sum(),
        "mlp_dominant_count": (df["dominant"] == "MLP").sum(),
    }
