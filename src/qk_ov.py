"""
QK / OV circuit analysis for a single attention head.

Companion to `head_characterization.py`. That module asks "what TYPE is this head";
this one asks "what is this specific head computing" — built to dissect the one
genuine lexical lead from the Pythia-2.8B characterization: L29/H7 and its
reader->screen carve-out.

A head factors into two independent circuits (Elhage et al. 2021,
"A Mathematical Framework for Transformer Circuits"):
  QK (W_Q W_K^T): WHERE attention goes — which key token a query token prefers.
  OV (W_V W_O):   WHAT gets written — the residual-stream edit when attention lands.

Functions come in two flavors:
  - weight-based (W_E ... W_U): the head's INTRINSIC token preferences, ignoring
    context/position. Cleanest test of "is this a lexical lock?". (Pythia uses
    rotary position embeddings, so weight-based QK is pure token-content preference
    — position is applied to q/k only at runtime.)
  - activation-based (from cache): the realized q/k/v on an actual prompt, capturing
    the contextualized layer-29 representations.
"""

import pandas as pd
import torch

from .binding import find_token_index


def _tok_id(model, word):
    """Token id for a word — prefer the leading-space form (' screen'), which is how
    these words tokenize mid-sentence; fall back to bare, then to first sub-token."""
    for cand in (" " + word, word):
        ids = model.to_tokens(cand, prepend_bos=False)[0]
        if ids.numel() == 1:
            return ids[0].item()
    return model.to_tokens(" " + word, prepend_bos=False)[0, 0].item()


# --------------------------------------------------------------------------- #
# QK circuit                                                                   #
# --------------------------------------------------------------------------- #
def qk_token_matrix(model, layer, head, query_words, key_words):
    """
    Weight-based QK scores between token sets (intrinsic lexical preference).

        score(q, k) = (E[q] W_Q) . (E[k] W_K) / sqrt(d_head)

    Returns DataFrame: rows = query words, columns = key words. A "lexical lock"
    shows up as one key dominating a query's row.
    """
    W_Q, W_K = model.W_Q[layer, head], model.W_K[layer, head]   # [d_model, d_head]
    d_head = W_Q.shape[-1]
    E = model.W_E
    qids = {w: _tok_id(model, w) for w in query_words}
    kids = {w: _tok_id(model, w) for w in key_words}

    data = {}
    for qw in query_words:
        q = E[qids[qw]] @ W_Q                       # [d_head]
        data[qw] = {kw: round(((q @ (E[kids[kw]] @ W_K)) / (d_head ** 0.5)).item(), 3)
                    for kw in key_words}
    return pd.DataFrame(data).T                     # rows=query, cols=key


def realized_attention(model, layer, head, prompt, query_word, key_word):
    """The trustworthy QK signal: the post-softmax attention the head actually places
    from `query_word` to `key_word` on a real prompt.

    (We deliberately do NOT return a raw q·k dot product. On Pythia the cached q/k
    are dominated by massive-activation outlier dimensions — the raw score is ~constant
    across keys and does not track attention. The realized pattern is the honest
    measure; compare it across compounds via `collocation_scan` for selectivity.)"""
    str_tokens = model.to_str_tokens(prompt)
    qi = find_token_index(str_tokens, query_word)
    ki = find_token_index(str_tokens, key_word)
    _, cache = model.run_with_cache(prompt)
    return {
        "query": query_word, "key": key_word,
        "attention": round(cache["pattern", layer][0, head, qi, ki].item(), 4),
    }


# --------------------------------------------------------------------------- #
# OV circuit                                                                   #
# --------------------------------------------------------------------------- #
def ov_logit_lens(model, layer, head, prompt, source_word, dest_word, top_k=15):
    """
    What the head writes into `dest_word`'s residual when it attends to `source_word`.

    Uses proper direct-logit-attribution: take the actual write
    `attn[dest,source] * (v_source @ W_O)`, center it, divide by the REAL ln_final
    scale at the destination position (from the forward pass), then unembed. This
    avoids the artifact of applying LayerNorm to an isolated vector (which otherwise
    makes rare byte-tokens dominate). Returns the most promoted / suppressed tokens.
    """
    str_tokens = model.to_str_tokens(prompt)
    si = find_token_index(str_tokens, source_word)
    di = find_token_index(str_tokens, dest_word)
    _, cache = model.run_with_cache(prompt)

    v = cache["v", layer][0, si, head]                       # [d_head]
    attn = cache["pattern", layer][0, head, di, si]
    written = attn * (v @ model.W_O[layer, head])           # [d_model] write to dest
    written = written - written.mean()                      # LN centering
    scale = cache["ln_final.hook_scale"][0, di]             # real scale at dest [1]
    logits = ((written / scale) @ model.W_U)               # [d_vocab]

    def names(idx):
        return [(model.to_single_str_token(i.item()), round(logits[i].item(), 3))
                for i in idx]

    return {
        "source": source_word, "dest": dest_word,
        "attention": round(attn.item(), 4),
        "promoted": names(torch.topk(logits, top_k).indices),
        "suppressed": names(torch.topk(logits, top_k, largest=False).indices),
    }


# --------------------------------------------------------------------------- #
# Causal check                                                                 #
# --------------------------------------------------------------------------- #
def ablate_head_at_position(model, prompt, layer, head, dest_word, top_k=10):
    """
    Zero a single head's output at the `dest_word` position and measure the effect on
    the model's NEXT-token prediction (final sequence position).

    Returns the KL(baseline || ablated) and the top tokens before/after. Small KL +
    unchanged top tokens => the head's contribution is not load-bearing here
    (consistent with the distributed/redundant story); large KL => a genuine,
    necessary single-head mechanism.
    """
    str_tokens = model.to_str_tokens(prompt)
    di = find_token_index(str_tokens, dest_word)

    base = model(prompt)[0, -1].log_softmax(-1)

    def hook(z, hook):
        z[:, di, head, :] = 0.0
        return z

    abl = model.run_with_hooks(
        prompt, fwd_hooks=[(f"blocks.{layer}.attn.hook_z", hook)]
    )[0, -1].log_softmax(-1)

    kl = torch.sum(base.exp() * (base - abl)).item()

    def top(lp):
        return [(model.to_single_str_token(i.item()), round(lp[i].exp().item(), 4))
                for i in torch.topk(lp, top_k).indices]

    return {
        "dest_word": dest_word, "ablated_head": (layer, head),
        "kl_base_to_ablated": round(kl, 5),
        "baseline_top": top(base),
        "ablated_top": top(abl),
    }
