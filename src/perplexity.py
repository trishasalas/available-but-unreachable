"""Perplexity: how surprised is the model by this text?

Lower perplexity = the model expected this language.
Higher perplexity = the model found this surprising.

Comparing perplexity across model sizes for the same prompt reveals
when a model family starts "understanding" domain-specific terminology.
"""

import math
from typing import Optional

import torch
import torch.nn.functional as F
import pandas as pd
from transformer_lens import HookedTransformer


def perplexity(
    model: HookedTransformer,
    text: str,
) -> dict:
    """Compute overall perplexity for a text.

    Args:
        model: A loaded HookedTransformer.
        text: Input text to evaluate.

    Returns:
        Dict with:
            perplexity: exp(mean cross-entropy loss)
            mean_loss: average per-token cross-entropy
            n_tokens: number of tokens scored (excludes first token)
    """
    tokens = model.to_tokens(text)  # (1, seq_len)
    logits = model(tokens)          # (1, seq_len, vocab_size)

    # Shift: predict token[i+1] from logits[i]
    # First token has no prediction, so we score tokens[1:]
    shift_logits = logits[0, :-1]   # (seq_len-1, vocab_size)
    shift_targets = tokens[0, 1:]   # (seq_len-1,)

    loss = F.cross_entropy(shift_logits, shift_targets)

    return {
        "perplexity": math.exp(loss.item()),
        "mean_loss": loss.item(),
        "n_tokens": shift_targets.shape[0],
    }


def per_token_perplexity(
    model: HookedTransformer,
    text: str,
) -> pd.DataFrame:
    """Compute per-token surprise (cross-entropy loss).

    Useful for seeing exactly which tokens the model struggles with.
    A model that "knows" screen readers might have low loss on " reader"
    after "screen" but high loss on the same token in a different context.

    Args:
        model: A loaded HookedTransformer.
        text: Input text to evaluate.

    Returns:
        DataFrame with columns:
            position, token, token_str, loss, perplexity
    """
    tokens = model.to_tokens(text)
    logits = model(tokens)

    shift_logits = logits[0, :-1]
    shift_targets = tokens[0, 1:]

    # Per-token cross-entropy (no reduction)
    losses = F.cross_entropy(
        shift_logits, shift_targets, reduction="none"
    )

    rows = []
    for i in range(len(shift_targets)):
        token_id = shift_targets[i].item()
        token_str = model.to_string(token_id)
        token_loss = losses[i].item()

        rows.append({
            "position": i + 1,  # +1 because we skip the first token
            "token_id": token_id,
            "token_str": token_str,
            "loss": token_loss,
            "perplexity": math.exp(token_loss),
        })

    df = pd.DataFrame(rows)
    df.attrs["model"] = model.cfg.model_name
    df.attrs["text"] = text
    df.attrs["overall_perplexity"] = math.exp(losses.mean().item())

    return df


def compare_perplexity(
    results: dict[str, dict],
) -> pd.DataFrame:
    """Build a comparison table from multiple perplexity runs.

    Args:
        results: Dict mapping model name to perplexity() output.
                 e.g. {"gpt2": {...}, "gpt2-medium": {...}}

    Returns:
        DataFrame sorted by perplexity, one row per model.
    """
    rows = []
    for model_name, data in results.items():
        rows.append({
            "model": model_name,
            "perplexity": data["perplexity"],
            "mean_loss": data["mean_loss"],
            "n_tokens": data["n_tokens"],
        })

    return pd.DataFrame(rows).sort_values("perplexity")


def print_per_token(df: pd.DataFrame) -> None:
    """Pretty-print per-token perplexity."""
    attrs = df.attrs
    print(f"Model: {attrs.get('model', '?')}")
    print(f"Text: \"{attrs.get('text', '?')}\"")
    print(f"Overall perplexity: {attrs.get('overall_perplexity', 0):.2f}")
    print()
    print(f"{'Pos':<6} {'Token':<16} {'Loss':<10} {'Perplexity':<12}")
    print("-" * 44)
    for _, row in df.iterrows():
        print(f"{row['position']:<6} {row['token_str']:<16} "
              f"{row['loss']:<10.4f} {row['perplexity']:<12.2f}")
