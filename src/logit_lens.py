"""Logit lens analysis: trace predictions through the residual stream.

Projects the residual stream at each layer into vocabulary space
to see when the model starts predicting the correct answer.
"""

import torch
import torch.nn.functional as F
import pandas as pd
from transformer_lens import HookedTransformer


def logit_lens(
    model: HookedTransformer,
    prompt: str,
    target: str,
    position: int = -1,
) -> pd.DataFrame:
    """Run logit lens across all layers for a target token.

    At each layer, projects the residual stream through the final
    layer norm and unembedding to see what the model would predict
    if decoding stopped at that layer.

    Args:
        model: A loaded HookedTransformer.
        prompt: Input text, e.g. "The capital of France is"
        target: Target token with leading space, e.g. " Paris"
        position: Token position to analyze. Default -1 (last token).

    Returns:
        DataFrame with columns:
            layer, top_prediction, target_rank, target_prob
    """
    target_token = model.to_single_token(target)
    logits, cache = model.run_with_cache(prompt)

    # What does the model actually predict at the final layer?
    final_pred = model.to_string(logits[0, position].argmax())

    rows = []
    for layer in range(model.cfg.n_layers):
        resid = cache["resid_post", layer][0, position]

        # Project through final layer norm + unembedding
        normed = model.ln_final(resid)
        layer_logits = model.unembed(normed.unsqueeze(0).unsqueeze(0))[0, 0]

        top_prediction = model.to_string(layer_logits.argmax())

        probs = F.softmax(layer_logits, dim=-1)
        target_prob = probs[target_token].item()

        sorted_indices = layer_logits.argsort(descending=True)
        target_rank = (sorted_indices == target_token).nonzero().item() + 1

        rows.append({
            "layer": layer,
            "top_prediction": top_prediction,
            "target_rank": target_rank,
            "target_prob": target_prob,
        })

    df = pd.DataFrame(rows)
    df.attrs["model"] = model.cfg.model_name
    df.attrs["prompt"] = prompt
    df.attrs["target"] = target
    df.attrs["target_token_id"] = int(target_token)
    df.attrs["final_prediction"] = final_pred

    return df, cache


def print_logit_lens(df: pd.DataFrame) -> None:
    """Pretty-print a logit lens DataFrame."""
    attrs = df.attrs
    print(f"Model: {attrs.get('model', '?')}")
    print(f"Prompt: \"{attrs.get('prompt', '?')}\"")
    print(f"Target: \"{attrs.get('target', '?')}\" (token {attrs.get('target_token_id', '?')})")
    print(f"Final prediction: \"{attrs.get('final_prediction', '?')}\"")
    print()
    print(f"{'Layer':<8} {'Top Prediction':<20} {'Target Rank':<14} {'Target Prob':<12}")
    print("-" * 54)
    for _, row in df.iterrows():
        print(f"{row['layer']:<8} {row['top_prediction']:<20} "
              f"{row['target_rank']:<14} {row['target_prob']:<12.6f}")
