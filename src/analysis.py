"""
Analysis module — loads and combines results across all models.

Usage (from notebook):
    from src.analysis import load_all_results
    elicitation, entropy, binding = load_all_results(PROJECT_ROOT)

Directory layout (post-reorganisation):
    results/{elicitation,entropy,binding}/{suite}/{model}/{model}-{domain}.csv
    Suites: pythia, gpt2, olmo
    Domains: accessibility, control, medical, legal, finance
"""

from pathlib import Path
import pandas as pd


KNOWN_DOMAINS = {'accessibility', 'control', 'medical', 'legal', 'finance'}


def load_all_results(project_root):
    """
    Load and concatenate all result CSVs across all model families.

    Returns three DataFrames:
        elicitation_df — all prompt responses across all models
        entropy_df     — all entropy measurements across all models
        binding_df     — all binding scores across all models

    Each DataFrame has 'model', 'suite', 'scale', 'domain', and 'source'
    columns.
    """
    project_root = Path(project_root)
    results_dir = project_root / 'results'

    frames = {'elicitation': [], 'entropy': [], 'binding': []}

    for data_type in frames:
        type_dir = results_dir / data_type
        if not type_dir.exists():
            continue

        for suite_dir in sorted(type_dir.iterdir()):
            if not suite_dir.is_dir():
                continue
            dir_suite = suite_dir.name

            for model_dir in sorted(suite_dir.iterdir()):
                if not model_dir.is_dir():
                    continue
                model_name = model_dir.name
                suite = _infer_suite(model_name, dir_suite)

                for csv_file in sorted(model_dir.glob('*.csv')):
                    domain = _extract_domain(csv_file.stem, model_name)
                    if domain not in KNOWN_DOMAINS:
                        continue

                    df = pd.read_csv(csv_file)
                    if 'domain' not in df.columns:
                        df['domain'] = domain
                    df['suite'] = suite
                    df['scale'] = _extract_scale(model_name, suite)
                    df['source'] = 'original'
                    frames[data_type].append(df)

    elicitation_df = pd.concat(frames['elicitation'], ignore_index=True) if frames['elicitation'] else pd.DataFrame()
    entropy_df = pd.concat(frames['entropy'], ignore_index=True) if frames['entropy'] else pd.DataFrame()
    binding_df = pd.concat(frames['binding'], ignore_index=True) if frames['binding'] else pd.DataFrame()

    for df in [elicitation_df, entropy_df, binding_df]:
        if 'scale' in df.columns:
            df.sort_values('scale', inplace=True)

    print("Loaded:")
    for name, df in [('Elicitation', elicitation_df), ('Entropy', entropy_df), ('Binding', binding_df)]:
        if not df.empty and 'model' in df.columns:
            print(f"  {name}: {len(df)} rows across {df['model'].nunique()} models "
                  f"({sorted(df['suite'].unique())})")
        else:
            print(f"  {name}: {len(df)} rows")

    return elicitation_df, entropy_df, binding_df


def _infer_suite(model_name, dir_suite):
    """Correct suite when model dirs are misplaced (e.g. OLMo under gpt2/)."""
    if model_name.startswith('OLMo'):
        return 'olmo'
    return dir_suite


def _extract_domain(csv_stem, model_name):
    """Extract domain from filename: 'pythia-160m-accessibility' -> 'accessibility'."""
    prefix = model_name + '-'
    if csv_stem.startswith(prefix):
        return csv_stem[len(prefix):]
    return csv_stem


def _extract_scale(model_name, suite):
    """
    Extract parameter count as integer for sorting.
    'pythia-160m'        -> 160_000_000
    'gpt2-xl'           -> 1_500_000_000
    'OLMo-2-1124-7B'    -> 7_000_000_000
    """
    gpt2_scales = {
        'gpt2': 124_000_000,
        'gpt2-small': 124_000_000,
        'gpt2-medium': 355_000_000,
        'gpt2-large': 774_000_000,
        'gpt2-xl': 1_500_000_000,
    }
    if suite == 'gpt2':
        return gpt2_scales.get(model_name, 0)

    # pythia-13b is the same checkpoint as pythia-12b
    if model_name == 'pythia-13b':
        return 12_000_000_000

    multipliers = {'m': 1_000_000, 'b': 1_000_000_000}
    parts = model_name.split('-')
    for part in parts:
        p = part.lower()
        for suffix, mult in multipliers.items():
            if p.endswith(suffix):
                try:
                    return int(float(p[:-1]) * mult)
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
    For each compound x model, find the layer with the strongest binding head.
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
