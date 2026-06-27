"""
Compound binding sweep module.

Measures attention binding between token pairs across all layers and heads.
Runs multiple compounds per model, saves per-model CSV.

Usage (from notebook):
    from src.binding import run_binding_sweep
    binding_df = run_binding_sweep(model, model_name, PROJECT_ROOT)
"""

from pathlib import Path
import pandas as pd


# Default compound set — aligned to elicitation prompt concepts.
# Each entry: (name, word1, word2, prompt_template)
# The prompt_template places both words where binding can be measured.
DEFAULT_COMPOUNDS = [
    ("screen_reader",     "screen",   "reader",     "A screen reader is"),
    ("alt_text",          "alt",      "text",       "The purpose of alt text is"),
    ("skip_link",         "skip",     "link",       "A skip link is"),
    ("color_contrast",    "color",    "contrast",   "Color contrast is important because"),
    ("keyboard_navigation", "keyboard", "navigation", "Keyboard navigation allows"),
    ("closed_captions",   "closed",   "captions",   "Closed captions display"),
    ("page_title",        "page",     "title",      "A page title describes"),
    ("form_label",        "form",     "label",      "A form label is"),
    ("link_text",         "link",     "text",       "Link text describes"),
    ("focus_indicator",   "focus",    "indicator",  "A focus indicator is"),
    ("semantic_html",     "semantic", "HTML",        "Semantic HTML helps"),
]


def find_token_index(tokens, target):
    """
    Find the index of a target word in a list of tokens.
    Handles leading-space tokenization (e.g., ' screen' for 'screen')
    and subword splits (e.g., 'keyboard' -> ['Key', 'board']).

    For multi-token matches, returns the LAST subtoken index — that's
    where the composed representation lives after the model processes
    the subword sequence.

    Returns the index or None if not found.
    """
    target_lower = target.lower()

    # Pass 1: exact single-token match (stripped of whitespace)
    for i, tok in enumerate(tokens):
        if tok.strip().lower() == target_lower:
            return i

    # Pass 2: multi-token match — concatenate adjacent tokens
    for start in range(len(tokens)):
        concat = ""
        for end in range(start, len(tokens)):
            concat += tokens[end].strip().lower()
            if concat == target_lower:
                # Return the LAST token in the span
                return end
            if len(concat) > len(target_lower):
                break

    return None


def run_single_compound(model, compound_name, word1, word2, prompt, threshold=0.1):
    """
    Run binding analysis for a single compound pair.

    Returns list of dicts with layer, head, binding score for all heads
    (not just above threshold — threshold applied at analysis time).
    """
    tokens = model.to_str_tokens(prompt)

    # Find token indices
    idx1 = find_token_index(tokens, word1)
    idx2 = find_token_index(tokens, word2)

    if idx1 is None or idx2 is None:
        print(f"  WARNING: Could not find tokens for '{compound_name}'")
        print(f"    Looking for '{word1}' and '{word2}' in: {tokens}")
        return []

    # word2 attending to word1 (e.g., "reader" attending to "screen")
    target_idx = max(idx1, idx2)   # later token
    source_idx = min(idx1, idx2)   # earlier token

    logits, cache = model.run_with_cache(prompt)

    rows = []
    for layer in range(model.cfg.n_layers):
        attention = cache["pattern", layer]  # [batch, heads, seq, seq]
        for head in range(model.cfg.n_heads):
            attn = attention[0, head]  # [seq, seq]
            score = attn[target_idx, source_idx].item()
            rows.append({
                "compound": compound_name,
                "layer": layer,
                "head": head,
                "binding_score": round(score, 4),
                "word1": word1,
                "word2": word2,
                "prompt": prompt,
                "tokens": str(tokens),
                "word1_idx": source_idx,
                "word2_idx": target_idx,
            })

    return rows


def run_binding_sweep(model, model_name, project_root, compounds=None):
    """
    Run binding analysis for all compounds and save results.

    Args:
        model: A loaded TransformerLens model.
        model_name: Full model name (e.g. "EleutherAI/pythia-160m").
        project_root: Path to the project root directory.
        compounds: Optional list of (name, word1, word2, prompt) tuples.
                   Defaults to DEFAULT_COMPOUNDS.

    Returns:
        DataFrame with binding scores for all compounds × layers × heads.
    """
    if compounds is None:
        compounds = DEFAULT_COMPOUNDS

    all_rows = []

    for compound_name, word1, word2, prompt in compounds:
        print(f"Running binding: {compound_name} (\"{prompt}\")")
        rows = run_single_compound(model, compound_name, word1, word2, prompt)
        all_rows.extend(rows)

    if not all_rows:
        print("WARNING: No binding data collected.")
        return pd.DataFrame()

    binding_df = pd.DataFrame(all_rows)
    binding_df["model"] = model_name

    # Save per-model CSV
    short_name = model_name.split('/')[-1]
    suite = 'pythia' if 'pythia' in short_name else 'gpt2'
    output_dir = Path(project_root) / 'results' / suite
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f'{short_name}-binding.csv'
    binding_df.to_csv(output_path, index=False)
    print(f"\nSaved {len(binding_df)} rows ({len(compounds)} compounds × "
          f"{model.cfg.n_layers} layers × {model.cfg.n_heads} heads) to {output_path}")

    # Print summary: top binding heads per compound
    print(f"\nTop binding heads per compound (threshold > 0.1):")
    for compound_name, _, _, _ in compounds:
        subset = binding_df[
            (binding_df['compound'] == compound_name) &
            (binding_df['binding_score'] > 0.1)
        ].sort_values('binding_score', ascending=False)
        if len(subset) > 0:
            top = subset.iloc[0]
            print(f"  {compound_name:25s} — L{int(top['layer']):2d}H{int(top['head']):2d} "
                  f"({top['binding_score']:.4f}), {len(subset)} heads above threshold")
        else:
            print(f"  {compound_name:25s} — no heads above threshold")

    return binding_df
