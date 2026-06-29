"""
Corpus frequency analysis and token competition tracing.

Tests whether compound frequency in the training corpus (The Pile) predicts
which behavioral trajectory class a concept takes (peak_regress, monotonic_climb,
never_emerges, mixed). Uses the Infini-gram API (Liu et al. 2024) for n-gram
counts and TransformerLens for token competition tracing.

The frequency hypothesis: compounds that inverse-scale (peak_regress) are the
ones whose correct continuation token has a high-frequency competitor at the
decision point. Compounds that monotonic_climb don't have that competition.

Usage (from notebook):
    from src.frequency import (
        COMPOUNDS, load_trajectories,
        query_infinigram, build_frequency_table,
        token_competition_trace,
        frequency_trajectory_correlation,
        save_frequency_results,
    )

    # Get corpus frequencies
    freq_df = build_frequency_table()

    # Trace token competition at a specific scale
    comp = token_competition_trace(model, "A skip link is", top_k=10)

    # Correlate frequency with trajectory class
    corr = frequency_trajectory_correlation(freq_df, traj_df)
"""

import time
from pathlib import Path

import pandas as pd
import requests
import torch
import torch.nn.functional as F


# --------------------------------------------------------------------------- #
# Compound inventory                                                           #
# --------------------------------------------------------------------------- #
# Aligned with binding.py DEFAULT_COMPOUNDS and per_concept_trajectories.csv.
# Each entry: (concept_name, word1, word2, prompt)
# word1 and word2 are the compound components for frequency queries.
COMPOUNDS = [
    ("screen_reader",       "screen",   "reader",    "A screen reader is"),
    ("alt_text",            "alt",      "text",      "The purpose of alt text is"),
    ("skip_link",           "skip",     "link",      "A skip link is"),
    ("color_contrast",      "color",    "contrast",  "Color contrast is important because"),
    ("keyboard_navigation", "keyboard", "navigation", "Keyboard navigation allows"),
    ("focus_indicator",     "focus",    "indicator", "A focus indicator is"),
    ("semantic_html",       "semantic", "HTML",      "Semantic HTML helps"),
    ("captions",            "closed",   "captions",  "Closed captions display"),
    ("WCAG",                "WCAG",     None,        "WCAG stands for"),
    ("ARIA",                "ARIA",     None,        "ARIA stands for"),
]

# The concept names used in per_concept_trajectories.csv, mapped to compound names.
# Trajectory CSV uses display names; this maps them to our underscore names.
CONCEPT_TO_COMPOUND = {
    "screen reader":       "screen_reader",
    "alt text":            "alt_text",
    "skip link":           "skip_link",
    "color contrast":      "color_contrast",
    "keyboard navigation": "keyboard_navigation",
    "focus indicator":     "focus_indicator",
    "semantic HTML":       "semantic_html",
    "closed captions":     "closed_captions",
    "WCAG":                "WCAG",
    "ARIA":                "ARIA",
}


# --------------------------------------------------------------------------- #
# Trajectory data                                                              #
# --------------------------------------------------------------------------- #
def load_trajectories(project_root):
    """Load per-concept trajectory classifications from the analysis CSV.

    Returns DataFrame with columns: suite, concept, compound, trajectory.
    """
    path = Path(project_root) / "results" / "analysis" / "per_concept_trajectories.csv"
    df = pd.read_csv(path)
    df["compound"] = df["concept"].map(CONCEPT_TO_COMPOUND)
    return df[["suite", "concept", "compound", "trajectory"]]


# --------------------------------------------------------------------------- #
# Infini-gram API                                                              #
# --------------------------------------------------------------------------- #
INFINIGRAM_API = "https://api.infini-gram.io/"
PILE_INDEX = "v4_piletrain_llama"   # Pile-train, Llama-2 tokenizer, 380B tokens


def query_infinigram(ngram, index=PILE_INDEX, retries=3, delay=1.0):
    """Query Infini-gram for the count of an n-gram in the corpus.

    Args:
        ngram: string to count (e.g. "skip link", "screen reader").
                Case-sensitive. Tokenized by infini-gram server-side.
        index: corpus index. Default is Pile-train (Llama-2 tokenizer).
        retries: number of retry attempts on failure.
        delay: seconds between retries.

    Returns:
        dict with keys: ngram, count, approx, tokens, latency_ms.
        On failure after retries: count=-1 and an error key.

    Note: the Pile-train index uses the Llama-2 tokenizer, not Pythia's
    GPT-NeoX tokenizer. For regular English words this doesn't affect
    counts. For acronyms (WCAG, ARIA) or unusual tokens, verify that
    the tokenization shown in the response matches expectations.
    """
    payload = {
        "index": index,
        "query_type": "count",
        "query": ngram,
    }

    for attempt in range(retries):
        try:
            resp = requests.post(INFINIGRAM_API, json=payload, timeout=30)
            resp.raise_for_status()
            data = resp.json()

            if "error" in data:
                print(f"  API error for '{ngram}': {data['error']}")
                return {"ngram": ngram, "count": -1, "error": data["error"]}

            return {
                "ngram": ngram,
                "count": data["count"],
                "approx": data.get("approx", False),
                "tokens": data.get("tokens", []),
                "latency_ms": round(data.get("latency", 0), 1),
            }
        except Exception as e:
            if attempt < retries - 1:
                print(f"  Retry {attempt + 1}/{retries} for '{ngram}': {e}")
                time.sleep(delay)
            else:
                print(f"  Failed after {retries} attempts for '{ngram}': {e}")
                return {"ngram": ngram, "count": -1, "error": str(e)}


def build_frequency_table(compounds=None, index=PILE_INDEX):
    """Query Infini-gram for all compounds and their component words.

    For each compound, queries:
      - bigram count (e.g. "skip link")
      - word1 unigram count (e.g. "skip")
      - word2 unigram count (e.g. "link")

    Computes conditional probability: P(word2 | word1) = count(bigram) / count(word1).

    Args:
        compounds: list of (name, word1, word2, prompt) tuples.
                   Defaults to COMPOUNDS.
        index: Infini-gram corpus index.

    Returns:
        DataFrame with columns: compound, word1, word2, bigram_count,
        word1_count, word2_count, conditional_prob.
    """
    if compounds is None:
        compounds = COMPOUNDS

    rows = []
    for name, w1, w2, _prompt in compounds:
        print(f"Querying: {name}...")

        # Bigram (skip for single-word concepts like WCAG, ARIA)
        if w2 is not None:
            bigram = f"{w1} {w2}"
            bg = query_infinigram(bigram, index=index)
            bigram_count = bg["count"]
        else:
            bigram_count = None

        # Unigram: word1
        ug1 = query_infinigram(w1, index=index)
        w1_count = ug1["count"]

        # Unigram: word2 (if it exists)
        if w2 is not None:
            ug2 = query_infinigram(w2, index=index)
            w2_count = ug2["count"]
        else:
            w2_count = None

        # Conditional probability
        if bigram_count is not None and w1_count > 0:
            cond_prob = bigram_count / w1_count
        else:
            cond_prob = None

        rows.append({
            "compound": name,
            "word1": w1,
            "word2": w2,
            "bigram_count": bigram_count,
            "word1_count": w1_count,
            "word2_count": w2_count,
            "conditional_prob": round(cond_prob, 6) if cond_prob else None,
        })

        # Be polite to the API
        time.sleep(0.5)

    return pd.DataFrame(rows)


def query_competitor_frequency(competitors, index=PILE_INDEX):
    """Query Infini-gram for a list of competitor tokens.

    Use after token_competition_trace to get corpus frequency for
    the tokens that compete at the decision point.

    Args:
        competitors: list of token strings (e.g. [" click", " displayed"]).
        index: Infini-gram corpus index.

    Returns:
        DataFrame with columns: token, count.
    """
    rows = []
    for tok in competitors:
        result = query_infinigram(tok.strip(), index=index)
        rows.append({"token": tok, "count": result["count"]})
        time.sleep(0.3)
    return pd.DataFrame(rows)


# --------------------------------------------------------------------------- #
# Token competition tracing                                                    #
# --------------------------------------------------------------------------- #
def token_competition_trace(model, prompt, top_k=10, position=-1):
    """Trace the top-k candidate tokens across all layers via the logit lens.

    At the final layer, identifies the top-k predicted tokens. Then traces
    each of those tokens' rank and probability back through every layer,
    showing where and how they compete.

    This is the generalized version of the skip_link "displayed vs click"
    trace — it works for any prompt and any set of competing tokens.

    Args:
        model: a loaded TransformerLens HookedTransformer.
        prompt: input text (e.g. "A skip link is").
        top_k: number of top tokens to trace from the final layer.
        position: which token position to analyze (default: last).

    Returns:
        dict with:
            final_top: list of (token_str, prob) for the final prediction.
            traces: DataFrame with columns:
                layer, token, token_id, rank, prob, logit
            prompt: the input prompt.
            model: the model name.
    """
    logits, cache = model.run_with_cache(prompt)
    final_logits = logits[0, position]

    # Identify the top-k tokens at the final layer
    final_probs = F.softmax(final_logits, dim=-1)
    top_ids = torch.topk(final_probs, top_k).indices
    top_tokens = [(model.to_single_str_token(tid.item()), round(final_probs[tid].item(), 6))
                  for tid in top_ids]

    # Trace each of those tokens through every layer
    rows = []
    for layer in range(model.cfg.n_layers):
        resid = cache["resid_post", layer][0, position]
        normed = model.ln_final(resid)
        layer_logits = model.unembed(normed.unsqueeze(0).unsqueeze(0))[0, 0]
        layer_probs = F.softmax(layer_logits, dim=-1)
        sorted_indices = layer_logits.argsort(descending=True)

        for tid in top_ids:
            tid_int = tid.item()
            rank = (sorted_indices == tid_int).nonzero().item() + 1
            rows.append({
                "layer": layer,
                "token": model.to_single_str_token(tid_int),
                "token_id": tid_int,
                "rank": rank,
                "prob": round(layer_probs[tid_int].item(), 6),
                "logit": round(layer_logits[tid_int].item(), 4),
            })

    traces = pd.DataFrame(rows)
    traces.attrs["model"] = model.cfg.model_name
    traces.attrs["prompt"] = prompt

    return {
        "final_top": top_tokens,
        "traces": traces,
        "prompt": prompt,
        "model": model.cfg.model_name,
    }


def compare_tokens_across_scales(results_by_scale, token_a, token_b):
    """Compare two specific tokens' trajectories across model scales.

    Takes the output of multiple token_competition_trace calls (one per
    scale) and extracts the layer-by-layer rank of two tokens for
    direct comparison.

    Args:
        results_by_scale: dict of {scale_name: token_competition_trace result}.
            e.g. {"160M": trace_160m, "2.8B": trace_2_8b, ...}
        token_a: first token string to compare (e.g. " displayed").
        token_b: second token string to compare (e.g. " click").

    Returns:
        DataFrame with columns: scale, layer, token_a_rank, token_b_rank,
        token_a_prob, token_b_prob, leader.
    """
    rows = []
    for scale, result in results_by_scale.items():
        traces = result["traces"]
        a_data = traces[traces["token"] == token_a]
        b_data = traces[traces["token"] == token_b]

        if a_data.empty or b_data.empty:
            print(f"  Warning: '{token_a}' or '{token_b}' not in top-k at {scale}")
            continue

        for _, row_a in a_data.iterrows():
            layer = row_a["layer"]
            row_b = b_data[b_data["layer"] == layer]
            if row_b.empty:
                continue
            row_b = row_b.iloc[0]

            rows.append({
                "scale": scale,
                "layer": layer,
                f"{token_a.strip()}_rank": row_a["rank"],
                f"{token_b.strip()}_rank": row_b["rank"],
                f"{token_a.strip()}_prob": row_a["prob"],
                f"{token_b.strip()}_prob": row_b["prob"],
                "leader": token_a.strip() if row_a["rank"] < row_b["rank"]
                          else token_b.strip(),
            })

    return pd.DataFrame(rows)


# --------------------------------------------------------------------------- #
# Correlation analysis                                                         #
# --------------------------------------------------------------------------- #
def frequency_trajectory_correlation(freq_df, traj_df, suite="pythia"):
    """Spearman correlation between corpus frequency and trajectory class.

    Merges the frequency table with trajectory classifications and tests
    whether frequency metrics predict which trajectory a compound takes.

    Args:
        freq_df: DataFrame from build_frequency_table.
        traj_df: DataFrame from load_trajectories.
        suite: which model suite to use for trajectories ("pythia" or "gpt2").

    Returns:
        dict with:
            merged: the merged DataFrame (for inspection).
            bigram_spearman: Spearman r and p-value for bigram count vs
                             trajectory ordinal.
            conditional_spearman: Spearman r and p-value for conditional
                                  probability vs trajectory ordinal.
            word1_spearman: Spearman r and p-value for word1 (component)
                            frequency vs trajectory ordinal.
    """
    from scipy.stats import spearmanr

    # Trajectory ordinal: higher = "better" scaling behavior
    # never_emerges=0, mixed=1, peak_regress=2, monotonic_climb=3
    trajectory_ordinal = {
        "never_emerges": 0,
        "mixed": 1,
        "peak_regress": 2,
        "monotonic_climb": 3,
    }

    traj = traj_df[traj_df["suite"] == suite].copy()
    traj["traj_ordinal"] = traj["trajectory"].map(trajectory_ordinal)

    merged = freq_df.merge(traj, on="compound", how="inner")

    results = {"merged": merged}

    # Only compute correlations where we have enough data points
    valid = merged.dropna(subset=["traj_ordinal"])

    for col, label in [("bigram_count", "bigram_spearman"),
                       ("conditional_prob", "conditional_spearman"),
                       ("word1_count", "word1_spearman")]:
        subset = valid.dropna(subset=[col])
        if len(subset) >= 4:
            r, p = spearmanr(subset[col], subset["traj_ordinal"])
            results[label] = {"r": round(r, 4), "p": round(p, 4), "n": len(subset)}
        else:
            results[label] = {"r": None, "p": None, "n": len(subset),
                              "note": "too few data points"}

    return results


# --------------------------------------------------------------------------- #
# Persistence                                                                  #
# --------------------------------------------------------------------------- #
def save_frequency_results(freq_df, project_root, filename="frequency_analysis.csv"):
    """Save frequency analysis results to results/analysis/.

    Args:
        freq_df: DataFrame from build_frequency_table.
        project_root: path to the tmlr repo root.
        filename: output filename.

    Returns:
        Path to the saved file.
    """
    out_dir = Path(project_root) / "results" / "analysis"
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / filename
    freq_df.to_csv(path, index=False)
    print(f"Saved {len(freq_df)} rows to {path}")
    return path


def save_competition_trace(result, project_root, model_name, compound_name):
    """Save a token competition trace to results/mlp_investigation/.

    Args:
        result: dict from token_competition_trace.
        project_root: path to the tmlr repo root.
        model_name: e.g. "pythia-12b".
        compound_name: e.g. "skip_link".

    Returns:
        Path to the saved file.
    """
    short = model_name.split("/")[-1]
    suite = "pythia" if "pythia" in short else "gpt2"
    out_dir = Path(project_root) / "results" / "mlp_investigation" / suite
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{short}_{compound_name}_competition.csv"
    result["traces"].to_csv(path, index=False)
    print(f"Saved competition trace to {path}")
    return path
