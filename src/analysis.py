"""
Analysis module — loads and combines results across all models.

Usage (from notebook):
    from src.analysis import load_all_results
    elicitation, entropy, binding = load_all_results(PROJECT_ROOT)
"""

from pathlib import Path
import pandas as pd


def load_all_results(project_root):
    """
    Load and concatenate all result CSVs across both model families.

    Returns three DataFrames:
        elicitation_df — all prompt responses across all models
        entropy_df     — all entropy measurements across all models
        binding_df     — all binding scores across all models

    Each DataFrame has a 'model' column and an added 'suite' column
    (pythia or gpt2) and 'scale' column (parameter count as int for sorting).
    """
    project_root = Path(project_root)
    results_dir = project_root / 'results'

    elicitation_frames = []
    entropy_frames = []
    binding_frames = []

    for suite_dir in sorted(results_dir.iterdir()):
        if suite_dir.name.startswith('_') or not suite_dir.is_dir():
            continue
        if suite_dir.name not in ('pythia', 'gpt2'):
            # Experiment output dirs (analysis/, frequency/, logits/,
            # mlp_investigation/) are not raw suites — skip them.
            # Canonical layout: raw per-model CSVs live at results/{suite}/.
            continue

        suite = suite_dir.name  # 'pythia' or 'gpt2'

        for csv_file in sorted(suite_dir.glob('*.csv')):
            name = csv_file.stem  # e.g. 'pythia-160m-results'

            df = pd.read_csv(csv_file)
            df['suite'] = suite
            df['scale'] = _extract_scale(name, suite)
            # Provenance tag: the n=49 frequency-stratified probes live in
            # *-expansion-results.csv. Downstream, the declarative-evaluative
            # gap (a paradigm-level mean) is restricted to source=='original';
            # trajectory/scaling/frequency analyses use all sources.
            df['source'] = 'expansion' if 'expansion' in name else 'original'

            if name.endswith('-results'):
                elicitation_frames.append(df)
            elif name.endswith('-entropy'):
                entropy_frames.append(df)
            elif name.endswith('-binding'):
                binding_frames.append(df)

    elicitation_df = pd.concat(elicitation_frames, ignore_index=True) if elicitation_frames else pd.DataFrame()
    entropy_df = pd.concat(entropy_frames, ignore_index=True) if entropy_frames else pd.DataFrame()
    binding_df = pd.concat(binding_frames, ignore_index=True) if binding_frames else pd.DataFrame()

    # Sort by scale for consistent plotting
    for df in [elicitation_df, entropy_df, binding_df]:
        if 'scale' in df.columns:
            df.sort_values('scale', inplace=True)

    print(f"Loaded:")
    print(f"  Elicitation: {len(elicitation_df)} rows across {elicitation_df['model'].nunique()} models")
    print(f"  Entropy:     {len(entropy_df)} rows across {entropy_df['model'].nunique()} models")
    print(f"  Binding:     {len(binding_df)} rows across {binding_df['model'].nunique()} models")

    return elicitation_df, entropy_df, binding_df


def _extract_scale(filename, suite):
    """
    Extract parameter count as integer for sorting.
    'pythia-160m-results' -> 160_000_000
    'gpt2-xl-results' -> 1_500_000_000
    """
    # GPT-2 scale mapping
    gpt2_scales = {
        'gpt2': 124_000_000,
        'gpt2-medium': 355_000_000,
        'gpt2-large': 774_000_000,
        'gpt2-xl': 1_500_000_000,
    }

    if suite == 'gpt2':
        # Remove the suffix (-results, -entropy, -binding)
        model_key = filename.rsplit('-', 1)[0] if filename.endswith(('results', 'entropy', 'binding')) else filename
        # Handle 'gpt2-large-results' -> need to check for compound names
        for key in sorted(gpt2_scales.keys(), key=len, reverse=True):
            if filename.startswith(key):
                return gpt2_scales[key]
        return 0

    # Pythia scale extraction
    multipliers = {'m': 1_000_000, 'b': 1_000_000_000, 'B': 1_000_000_000}
    parts = filename.split('-')
    for part in parts:
        for suffix, mult in multipliers.items():
            if part.endswith(suffix):
                try:
                    return float(part[:-1]) * mult
                except ValueError:
                    continue
    return 0


def scale_label(scale_int):
    """Convert scale integer to readable label: 160000000 -> '160M'"""
    if scale_int >= 1_000_000_000:
        return f"{scale_int / 1_000_000_000:.1f}B".replace('.0B', 'B')
    elif scale_int >= 1_000_000:
        return f"{scale_int / 1_000_000:.0f}M"
    return str(scale_int)


def binding_summary(binding_df, threshold=0.1):
    """
    Summarize binding data: count of heads above threshold per compound per model.
    Returns a pivot table suitable for heatmaps.
    """
    above = binding_df[binding_df['binding_score'] > threshold]
    summary = above.groupby(['model', 'compound', 'scale']).size().reset_index(name='n_heads_above')
    return summary


def max_binding_layer(binding_df):
    """
    For each compound × model, find the layer with the strongest binding head.
    Useful for tracking binding depth across scales.
    """
    idx = binding_df.groupby(['model', 'compound'])['binding_score'].idxmax()
    return binding_df.loc[idx][['model', 'compound', 'layer', 'head', 'binding_score', 'scale']].reset_index(drop=True)


def tokenization_comparison(binding_df):
    """
    Compare binding scores between cleanly-tokenized and subword-split compounds.
    Returns summary statistics for each group.
    """
    clean = ['screen_reader', 'alt_text', 'skip_link', 'color_contrast',
             'page_title', 'form_label', 'link_text', 'focus_indicator']
    split = ['keyboard_navigation', 'closed_captions', 'semantic_html']

    binding_df = binding_df.copy()
    binding_df['tokenization'] = binding_df['compound'].apply(
        lambda x: 'clean' if x in clean else 'subword_split' if x in split else 'unknown'
    )

    summary = binding_df.groupby(['tokenization', 'model', 'scale']).agg(
        mean_binding=('binding_score', 'mean'),
        max_binding=('binding_score', 'max'),
        heads_above_01=('binding_score', lambda x: (x > 0.1).sum()),
    ).reset_index()

    return summary
