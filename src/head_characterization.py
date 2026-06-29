"""
Head characterization module.

After `binding.py` identifies which (layer, head) bind compound terms most
strongly, this module asks *what kind of head* those are. It runs the standard
behavioral diagnostics — induction (Olsson et al. 2022 prefix-matching),
previous-token, and duplicate-token — and a cross-domain collocation scan that
tests whether a head's binding is accessibility-specific or domain-general.

Design notes:
  - Top heads are DERIVED from a binding CSV, never hardcoded. Head indices are
    architecture-specific (GPT-2 XL's L15/H19 is not Pythia's), so the head set
    must come from the binding result for the model under test.
  - The three token-pattern diagnostics share ONE forward pass over a single
    repeated-random sequence — induction/prev/dup are just different reads of the
    same attention cache.
  - Token positions for the collocation scan come from `binding.find_token_index`
    (subword-aware), not fixed indices, so multi-token compounds work too.

Usage (from notebook):
    from src.head_characterization import (
        get_top_binding_heads, characterize_heads, collocation_scan,
    )
    heads = get_top_binding_heads(PROJECT_ROOT / "results/pythia/pythia-2.8b-binding.csv")
    table = characterize_heads(model, heads)
    colloc = collocation_scan(model, heads_of_interest=[(layer, head), ...])
"""

from pathlib import Path

import pandas as pd
import torch

from .binding import find_token_index


# Cross-domain compounds for the collocation / specificity test. Accessibility
# vs. four unrelated domains plus weak-collocation controls ("bicycle wheel").
# Word pairs are looked up by `find_token_index`, so prompts may tokenize freely.
DOMAIN_COMPOUNDS = {
    "a11y":    [("screen", "reader",  "A screen reader is"),
                ("alt",    "text",    "The purpose of alt text is"),
                ("skip",   "link",    "A skip link is"),
                ("focus",  "indicator", "A focus indicator is"),
                ("color",  "contrast", "Color contrast is important because")],
    "finance": [("stock",  "market",  "A stock market is"),
                ("credit", "score",   "A credit score is"),
                ("hedge",  "fund",    "A hedge fund is")],
    "legal":   [("court",  "order",   "A court order is"),
                ("case",   "law",     "Case law is"),
                ("due",    "process", "Due process is")],
    "medical": [("blood",  "pressure", "Blood pressure is"),
                ("heart",  "rate",    "Heart rate is"),
                ("side",   "effect",  "A side effect is")],
    "general": [("bicycle", "wheel",  "A bicycle wheel is"),
                ("coffee", "table",   "A coffee table is"),
                ("phone",  "call",    "A phone call is")],
}

# Induction-head threshold from the literature; behavioral scores well below this
# mean the head is not doing prefix-matching induction.
INDUCTION_THRESHOLD = 0.5
PATTERN_THRESHOLD = 0.5    # for prev-token / dup-token classification
SINK_THRESHOLD = 0.5       # mean attention to BOS above which a head is a sink
STRUCTURAL_THRESHOLD = 0.5  # mean attention to position 1 (the "A"/"The" token)


# --------------------------------------------------------------------------- #
# 1. Derive the head set from a binding CSV (no hardcoding)                    #
# --------------------------------------------------------------------------- #
def get_top_binding_heads(binding_csv, n_per_compound=1, min_layer=0,
                          score_threshold=0.1):
    """
    Derive the set of top binding heads from a binding-sweep CSV.

    Mirrors `binding.run_binding_sweep`'s own summary definition: the strongest
    head(s) per compound, pooled into a unique set. Returns a DataFrame so the
    caller can see WHY each head was selected (which compounds, what scores) —
    not just the bare indices.

    Args:
        binding_csv: path to a `<model>-binding.csv` (compound, layer, head,
                     binding_score, word1_idx, word2_idx, ...).
        n_per_compound: how many top heads to take per compound (default 1).
        min_layer: drop heads below this layer (useful to exclude early-layer
                   positional heads; default 0 = keep all).
        score_threshold: ignore heads whose binding is below this (noise floor).

    Returns:
        DataFrame[layer, head, mean_binding, max_binding, n_compounds_top,
                  top_compounds] sorted by mean_binding descending.
    """
    df = pd.read_csv(binding_csv)
    df = df[(df["binding_score"] >= score_threshold) & (df["layer"] >= min_layer)]

    selected = []
    for _, sub in df.groupby("compound"):
        top = sub.sort_values("binding_score", ascending=False).head(n_per_compound)
        selected.append(top)
    if not selected:
        return pd.DataFrame(columns=["layer", "head", "mean_binding",
                                     "max_binding", "n_compounds_top",
                                     "top_compounds"])
    picks = pd.concat(selected)

    # Aggregate the per-compound picks into a unique (layer, head) set, and
    # report each head's binding across ALL compounds (not just the ones that
    # elected it) so the caller sees its overall strength.
    out = []
    for (layer, head), grp in picks.groupby(["layer", "head"]):
        full = df[(df["layer"] == layer) & (df["head"] == head)]
        out.append({
            "layer": int(layer),
            "head": int(head),
            "mean_binding": round(full["binding_score"].mean(), 4),
            "max_binding": round(full["binding_score"].max(), 4),
            "n_compounds_top": int(grp["compound"].nunique()),
            "top_compounds": ", ".join(sorted(grp["compound"].unique())),
        })
    return (pd.DataFrame(out)
            .sort_values("mean_binding", ascending=False)
            .reset_index(drop=True))


def heads_as_tuples(heads_df):
    """Convenience: DataFrame[layer, head] -> [(layer, head), ...]."""
    return list(zip(heads_df["layer"].astype(int), heads_df["head"].astype(int)))


# --------------------------------------------------------------------------- #
# 2. Token-pattern battery: induction / prev-token / dup-token, one pass      #
# --------------------------------------------------------------------------- #
def run_token_pattern_battery(model, seq_len=50, seed=0):
    """
    Run the three token-pattern diagnostics from a SINGLE repeated-random
    sequence forward pass.

    The input is `[rand(seq_len), rand(seq_len)]` (one batch). All three scores
    are different reads of the same attention cache:

      induction : attention from position i (2nd half) to the token that FOLLOWED
                  this token's first occurrence  (the prefix-matching stripe).
      prev-token: attention from position i to position i-1.
      dup-token : attention from position i to earlier positions holding the same
                  token id (in a repeated sequence, that's i-seq_len).

    Returns three [n_layers, n_heads] tensors: (induction, prev_token, dup_token).
    """
    device = next(model.parameters()).device
    gen = torch.Generator().manual_seed(seed)  # reproducible, doesn't touch global RNG
    rand = torch.randint(0, model.cfg.d_vocab, (1, seq_len), generator=gen)
    repeated = torch.cat([rand, rand], dim=1).to(device)

    _, cache = model.run_with_cache(repeated, return_type=None)
    tokens = repeated[0]

    nL, nH = model.cfg.n_layers, model.cfg.n_heads
    induction = torch.zeros(nL, nH)
    prev_token = torch.zeros(nL, nH)
    dup_token = torch.zeros(nL, nH)

    # Precompute, for each query position, the earlier positions with the same
    # token id (for the duplicate-token score).
    dup_targets = {}
    for i in range(1, len(tokens)):
        matches = (tokens[:i] == tokens[i]).nonzero(as_tuple=True)[0]
        if len(matches):
            dup_targets[i] = matches

    for layer in range(nL):
        patt = cache["pattern", layer][0]  # [heads, seq, seq]
        for head in range(nH):
            attn = patt[head]
            # induction: second-half rows vs cols shifted by 1 (prefix match)
            induction[layer, head] = attn[seq_len:, 1:seq_len + 1].diag().mean().item()
            # previous-token: sub-diagonal
            prev_token[layer, head] = attn[1:, :-1].diag().mean().item()
            # duplicate-token: average attention mass onto same-token positions
            if dup_targets:
                dscores = [attn[i, idx].sum().item() for i, idx in dup_targets.items()]
                dup_token[layer, head] = sum(dscores) / len(dscores)

    return induction, prev_token, dup_token


def classify_head(induction, prev, dup):
    """Label a head from its three pattern scores (literature thresholds)."""
    if induction >= INDUCTION_THRESHOLD:
        return "induction"
    if prev >= PATTERN_THRESHOLD:
        return "previous-token"
    if dup >= PATTERN_THRESHOLD:
        return "duplicate-token"
    if prev >= 0.25 or dup >= 0.25:
        return "partial (prev/dup)"
    return "uncharacterized"


def characterize_heads(model, heads, seq_len=50, seed=0):
    """
    Run the token-pattern battery and report scores + a type label for the given
    heads.

    Args:
        model: loaded TransformerLens model.
        heads: list of (layer, head) tuples, or a DataFrame from
               `get_top_binding_heads` (its layer/head columns are used).
        seq_len, seed: passed to `run_token_pattern_battery`.

    Returns:
        DataFrame[layer, head, induction, prev_token, dup_token, type].
    """
    if isinstance(heads, pd.DataFrame):
        heads = heads_as_tuples(heads)

    induction, prev_token, dup_token = run_token_pattern_battery(model, seq_len, seed)

    rows = []
    for layer, head in heads:
        ind = induction[layer, head].item()
        pv = prev_token[layer, head].item()
        dp = dup_token[layer, head].item()
        rows.append({
            "layer": layer, "head": head,
            "induction": round(ind, 4),
            "prev_token": round(pv, 4),
            "dup_token": round(dp, 4),
            "type": classify_head(ind, pv, dp),
        })
    return pd.DataFrame(rows)


# --------------------------------------------------------------------------- #
# 3. Cross-domain collocation / specificity scan                              #
# --------------------------------------------------------------------------- #
def collocation_scan(model, heads_of_interest, domain_compounds=None, template=None):
    """
    For each head, measure word2->word1 attention across domains. If a head fires
    high on compounds from MANY domains it is a domain-general collocation
    detector, not an accessibility-specific binder.

    Positions are resolved with `binding.find_token_index` (subword-aware), so no
    token index is hardcoded.

    Args:
        model: loaded TransformerLens model.
        heads_of_interest: list of (layer, head) tuples to scan.
        domain_compounds: dict {domain: [(word1, word2, prompt), ...]}.
                          Defaults to DOMAIN_COMPOUNDS.
        template: if given (e.g. "A {w1} {w2} is"), the per-compound prompt is
                  IGNORED and this single frame is used for every compound. Use
                  this for a clean cross-domain comparison — it removes the prompt
                  confound that arises when compounds carry different templates.

    Returns:
        DataFrame[layer, head, domain, compound, score].
    """
    if domain_compounds is None:
        domain_compounds = DOMAIN_COMPOUNDS

    rows = []
    for domain, items in domain_compounds.items():
        for word1, word2, prompt in items:
            if template is not None:
                prompt = template.format(w1=word1, w2=word2)
            str_tokens = model.to_str_tokens(prompt)
            idx1 = find_token_index(str_tokens, word1)
            idx2 = find_token_index(str_tokens, word2)
            if idx1 is None or idx2 is None:
                print(f"  WARNING: tokens '{word1}'/'{word2}' not found in: {str_tokens}")
                continue
            target_idx, source_idx = max(idx1, idx2), min(idx1, idx2)
            _, cache = model.run_with_cache(prompt, return_type=None)
            for layer, head in heads_of_interest:
                score = cache["pattern", layer][0, head, target_idx, source_idx].item()
                rows.append({
                    "layer": layer, "head": head,
                    "domain": domain, "compound": f"{word1} {word2}",
                    "score": round(score, 4),
                })
    return pd.DataFrame(rows)


def attention_to_position(model, heads, position=0, prompts=None,
                          template="A {w1} {w2} is"):
    """
    Mean attention to a fixed KEY position per head, averaged over the query
    positions that can see it (strictly after `position`) and over prompts.

      position=0 -> attention to BOS / <|endoftext|>  (attention-SINK detector)
      position=1 -> attention to the first content token, e.g. "A"/"The"
                    (STRUCTURAL / position-1 head detector)

    These are the two most common reasons a late head reads "uncharacterized" on
    content metrics: it parks its mass on BOS, or on a fixed structural slot.

    Args:
        model: loaded TransformerLens model.
        heads: list of (layer, head) tuples.
        position: the key position to measure attention to.
        prompts: optional list of prompt strings. Defaults to every compound in
                 DOMAIN_COMPOUNDS rendered through `template`.
        template: frame used to build default prompts.

    Returns:
        DataFrame[layer, head, attn_to_pos{position}].
    """
    if prompts is None:
        prompts = [template.format(w1=w1, w2=w2)
                   for items in DOMAIN_COMPOUNDS.values() for (w1, w2, _p) in items]

    sums = {hd: 0.0 for hd in heads}
    n = 0
    for prompt in prompts:
        _, cache = model.run_with_cache(prompt, return_type=None)
        for layer, head in heads:
            attn = cache["pattern", layer][0, head]   # [seq, seq]
            q = attn[position + 1:, position]          # queries after `position`
            sums[(layer, head)] += q.mean().item() if q.numel() else 0.0
        n += 1

    col = f"attn_to_pos{position}"
    return pd.DataFrame([{"layer": l, "head": h, col: round(sums[(l, h)] / n, 4)}
                         for (l, h) in heads])


def attention_to_bos(model, heads, prompts=None, template="A {w1} {w2} is"):
    """Attention-sink score: mean attention to BOS (position 0) per head.
    Thin wrapper over `attention_to_position`; column named `bos_attention`."""
    df = attention_to_position(model, heads, position=0, prompts=prompts,
                               template=template)
    return df.rename(columns={"attn_to_pos0": "bos_attention"})


def final_label(induction, prev, dup, bos=None, pos1=None):
    """
    Full head-type label from the behavioral battery plus the structural signals.

    Priority: a genuine content type (induction / prev / dup) wins; otherwise a
    head that parks on BOS is a sink, and one that parks on position 1 is
    structural; the weak-signal and none-of-the-above cases fall through last.

    `bos`/`pos1` may be None or NaN (NaN comparisons are False, so they simply
    don't fire) — pass them when available for the richer labels.
    """
    if induction >= INDUCTION_THRESHOLD:
        return "induction"
    if prev >= PATTERN_THRESHOLD:
        return "previous-token"
    if dup >= PATTERN_THRESHOLD:
        return "duplicate-token"
    if bos is not None and bos >= SINK_THRESHOLD:
        return "attention-sink (BOS)"
    if pos1 is not None and pos1 >= STRUCTURAL_THRESHOLD:
        return "structural (position-1)"
    if prev >= 0.25 or dup >= 0.25:
        return "partial (prev/dup)"
    return "uncharacterized"


# --------------------------------------------------------------------------- #
# 4. Persist results (repo convention: results are CSVs)                       #
# --------------------------------------------------------------------------- #
def save_head_results(model_name, project_root, char_df=None, colloc_df=None):
    """
    Write characterization / collocation results to results/<suite>/.

    Args:
        model_name: e.g. "pythia-2.8b" (used for the suite + filename).
        project_root: Path to the tmlr repo root.
        char_df: DataFrame from `characterize_heads` (optional).
        colloc_df: DataFrame from `collocation_scan` (optional).

    Returns:
        dict of {kind: written path}.
    """
    short = model_name.split("/")[-1]
    suite = "pythia" if "pythia" in short else "gpt2"
    out_dir = Path(project_root) / "results" / suite
    out_dir.mkdir(parents=True, exist_ok=True)

    written = {}
    if char_df is not None:
        p = out_dir / f"{short}-head-characterization.csv"
        char_df.to_csv(p, index=False)
        written["characterization"] = p
        print(f"Saved {len(char_df)} head rows to {p}")
    if colloc_df is not None:
        p = out_dir / f"{short}-collocation.csv"
        colloc_df.to_csv(p, index=False)
        written["collocation"] = p
        print(f"Saved {len(colloc_df)} collocation rows to {p}")
    return written
