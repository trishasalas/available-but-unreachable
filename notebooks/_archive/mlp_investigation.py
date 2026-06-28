# %% [markdown]
# # MLP Interference Investigation: skip_link inverse scaling
#
# **Question:** Why does skip_link generation regress at 12B despite
# near-identical binding scores to 6.9B?
#
# **Hypothesis:** MLP layers in the late-layer region are overwriting
# the compound binding signal with stronger general-language priors.
# At 12B, the MLPs have more capacity and stronger opinions about
# "skip" in general English, interfering with the domain-specific
# compound binding that attention established.
#
# **Method:** Residual stream decomposition — extract attention and MLP
# output norms at each layer for the last token position. Compare
# 6.9B (correct generation) vs 12B (degenerate generation).
# Control: color_contrast (monotonic climb, no inverse scaling).
#
# **Ref:** DECISIONS.md 2026-06-28

# %% [markdown]
# ## Setup

# %%
import sys
import torch
import pandas as pd
import numpy as np
from pathlib import Path

# Colab
if 'google.colab' in sys.modules:
    from google.colab import drive
    drive.mount('/content/drive')
    PROJECT_ROOT = Path('/content/drive/MyDrive/tmlr-results')
    PROJECT_ROOT.mkdir(parents=True, exist_ok=True)
else:
    PROJECT_ROOT = Path.cwd().parent
    sys.path.insert(0, str(PROJECT_ROOT))

print(f"Project root: {PROJECT_ROOT}")

device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f"Device: {device}")

# %%
# Install TL2 if needed (Colab)
# !pip install transformer_lens==2.7.0 --quiet

# %%
from transformer_lens import HookedTransformer

# %% [markdown]
# ## Prompts
#
# skip_link: the inverse scaling case (correct at 6.9B, degenerate at 12B)
# color_contrast: the control (monotonic climb, no regression)

# %%
PROMPTS = {
    'skip_link': 'A skip link is',
    'color_contrast': 'Color contrast is important because',
}

MODELS = ['EleutherAI/pythia-6.9b', 'EleutherAI/pythia-12b']

# %% [markdown]
# ## Step 1: Residual Stream Decomposition
#
# For each model × prompt, cache all activations and extract:
# - Attention output norm at each layer (last token position)
# - MLP output norm at each layer (last token position)
# - MLP/attention ratio
# - Residual stream norm after each layer

# %%
def decompose_residual_stream(model, prompt, prompt_label):
    """
    Run prompt through model, cache activations, extract per-layer
    attention and MLP contributions at the last token position.
    """
    tokens = model.to_tokens(prompt)
    last_pos = tokens.shape[1] - 1

    _, cache = model.run_with_cache(prompt)

    n_layers = model.cfg.n_layers
    rows = []

    for layer in range(n_layers):
        # Attention output at last token position
        attn_out = cache[f'blocks.{layer}.hook_attn_out'][0, last_pos]
        attn_norm = attn_out.norm().item()

        # MLP output at last token position
        mlp_out = cache[f'blocks.{layer}.hook_mlp_out'][0, last_pos]
        mlp_norm = mlp_out.norm().item()

        # Residual stream after this layer
        resid_post = cache[f'blocks.{layer}.hook_resid_post'][0, last_pos]
        resid_norm = resid_post.norm().item()

        # MLP/attention ratio
        ratio = mlp_norm / attn_norm if attn_norm > 0 else float('inf')

        rows.append({
            'model': model.cfg.model_name,
            'prompt': prompt_label,
            'layer': layer,
            'attn_norm': round(attn_norm, 6),
            'mlp_norm': round(mlp_norm, 6),
            'mlp_attn_ratio': round(ratio, 4),
            'resid_norm': round(resid_norm, 6),
            'layer_frac': round(layer / (n_layers - 1), 4),
        })

    del cache
    torch.cuda.empty_cache()

    return pd.DataFrame(rows)


# %%
def run_decomposition(model_name, prompts):
    """Load model and run decomposition on all prompts."""
    print(f"\nLoading {model_name}...")
    model = HookedTransformer.from_pretrained(model_name, device=device)
    model.eval()

    frames = []
    for label, prompt in prompts.items():
        print(f"  Decomposing: {label}")
        df = decompose_residual_stream(model, prompt, label)
        frames.append(df)

    del model
    torch.cuda.empty_cache()

    return pd.concat(frames, ignore_index=True)

# %% [markdown]
# ## Step 2: Run both models

# %%
all_results = []

for model_name in MODELS:
    df = run_decomposition(model_name, PROMPTS)
    all_results.append(df)

results = pd.concat(all_results, ignore_index=True)

# Add short model label
results['model_label'] = results['model'].map({
    'pythia-6.9b': '6.9B',
    'EleutherAI/pythia-6.9b': '6.9B',
    'pythia-12b': '12B',
    'EleutherAI/pythia-12b': '12B',
})

print(f"\nTotal rows: {len(results)}")
print(results.head())

# %% [markdown]
# ## Step 3: Analysis — MLP interference at late layers

# %%
def analyze_late_layers(results, prompt_label):
    """
    Compare late-layer MLP behavior between 6.9B and 12B for a given prompt.
    Late = last 25% of layers.
    """
    print(f"\n{'='*70}")
    print(f"LATE-LAYER MLP ANALYSIS: {prompt_label}")
    print(f"{'='*70}")

    for model_label in ['6.9B', '12B']:
        subset = results[
            (results['model_label'] == model_label) &
            (results['prompt'] == prompt_label)
        ].copy()

        n_layers = len(subset)
        late_start = int(n_layers * 0.75)

        late = subset[subset['layer'] >= late_start]
        early = subset[subset['layer'] < late_start]

        print(f"\n  {model_label} ({n_layers} layers, late = L{late_start}+):")
        print(f"    Early MLP/attn ratio mean: {early['mlp_attn_ratio'].mean():.3f}")
        print(f"    Late  MLP/attn ratio mean: {late['mlp_attn_ratio'].mean():.3f}")
        print(f"    Late  MLP/attn ratio max:  {late['mlp_attn_ratio'].max():.3f} (L{late.loc[late['mlp_attn_ratio'].idxmax(), 'layer']})")
        print(f"    Late  MLP norm mean:       {late['mlp_norm'].mean():.3f}")
        print(f"    Late  MLP norm max:        {late['mlp_norm'].max():.3f} (L{late.loc[late['mlp_norm'].idxmax(), 'layer']})")
        print()
        print(f"    Per-layer detail (late):")
        for _, row in late.iterrows():
            bar = '█' * int(row['mlp_attn_ratio'] * 5)
            print(f"      L{int(row['layer']):2d}  attn={row['attn_norm']:.3f}  mlp={row['mlp_norm']:.3f}  ratio={row['mlp_attn_ratio']:.3f}  {bar}")


# %%
# Skip link: the target compound (inverse scaling)
analyze_late_layers(results, 'skip_link')

# %%
# Color contrast: the control compound (no inverse scaling)
analyze_late_layers(results, 'color_contrast')

# %% [markdown]
# ## Step 4: Cross-prompt comparison — is MLP interference skip_link-specific?

# %%
def compare_mlp_profiles(results):
    """
    Compare MLP/attn ratio profiles between skip_link and color_contrast
    for each model. If skip_link shows elevated MLP interference at 12B
    but color_contrast doesn't, the effect is compound-specific.
    """
    print(f"\n{'='*70}")
    print(f"CROSS-PROMPT MLP COMPARISON")
    print(f"{'='*70}")

    for model_label in ['6.9B', '12B']:
        model_data = results[results['model_label'] == model_label]
        n_layers = len(model_data[model_data['prompt'] == 'skip_link'])
        late_start = int(n_layers * 0.75)

        print(f"\n  {model_label} late layers (L{late_start}+):")
        print(f"  {'Metric':<30s} {'skip_link':>12s} {'color_contrast':>15s} {'delta':>10s}")
        print(f"  {'─'*30} {'─'*12} {'─'*15} {'─'*10}")

        for prompt in ['skip_link', 'color_contrast']:
            subset = model_data[
                (model_data['prompt'] == prompt) &
                (model_data['layer'] >= late_start)
            ]
            globals()[f'{prompt}_ratio'] = subset['mlp_attn_ratio'].mean()
            globals()[f'{prompt}_mlp'] = subset['mlp_norm'].mean()

        ratio_delta = skip_link_ratio - color_contrast_ratio
        mlp_delta = skip_link_mlp - color_contrast_mlp

        print(f"  {'MLP/attn ratio (mean)':<30s} {skip_link_ratio:>12.3f} {color_contrast_ratio:>15.3f} {ratio_delta:>+10.3f}")
        print(f"  {'MLP norm (mean)':<30s} {skip_link_mlp:>12.3f} {color_contrast_mlp:>15.3f} {mlp_delta:>+10.3f}")


# %%
compare_mlp_profiles(results)

# %% [markdown]
# ## Step 5: Save results

# %%
output_dir = PROJECT_ROOT / 'results' / 'mlp_investigation'
output_dir.mkdir(parents=True, exist_ok=True)

# Full decomposition data
results.to_csv(output_dir / 'residual_stream_decomposition.csv', index=False)

# Late-layer summary
summaries = []
for model_label in ['6.9B', '12B']:
    for prompt in ['skip_link', 'color_contrast']:
        subset = results[
            (results['model_label'] == model_label) &
            (results['prompt'] == prompt)
        ]
        n_layers = len(subset)
        late_start = int(n_layers * 0.75)
        late = subset[subset['layer'] >= late_start]
        early = subset[subset['layer'] < late_start]

        summaries.append({
            'model': model_label,
            'prompt': prompt,
            'n_layers': n_layers,
            'late_start': late_start,
            'early_mlp_attn_ratio_mean': round(early['mlp_attn_ratio'].mean(), 4),
            'late_mlp_attn_ratio_mean': round(late['mlp_attn_ratio'].mean(), 4),
            'late_mlp_attn_ratio_max': round(late['mlp_attn_ratio'].max(), 4),
            'late_mlp_norm_mean': round(late['mlp_norm'].mean(), 4),
            'late_mlp_norm_max': round(late['mlp_norm'].max(), 4),
            'late_attn_norm_mean': round(late['attn_norm'].mean(), 4),
        })

pd.DataFrame(summaries).to_csv(output_dir / 'late_layer_summary.csv', index=False)

print(f"Saved to {output_dir}/:")
for f in sorted(output_dir.glob('*.csv')):
    print(f"  {f.name}")

# %% [markdown]
# ## Interpretation guide
#
# **If MLP interference is confirmed (skip_link shows elevated MLP/attn
# ratio at 12B vs 6.9B, while color_contrast does not):**
#
# The declarative-evaluative gap is not passive absence. The model's
# attention correctly binds the compound, but MLP layers actively
# compete with domain-specific binding using stronger general-language
# priors. Scaling amplifies the interference because it amplifies the
# general-language signal.
#
# **If MLP interference is NOT confirmed (both compounds show similar
# profiles, or 12B doesn't differ from 6.9B):**
#
# The interference is elsewhere — possibly in the unembedding step
# or in the interaction between residual stream components that norms
# alone can't capture. Would need to move to directional analysis
# (projecting MLP output onto vocabulary space) rather than just norms.
#
# **Next step if confirmed:** Step 3 from the investigation plan —
# project MLP output at interference layers onto vocabulary to see
# what tokens the MLP is promoting. If "skip" is being pulled toward
# general-English associations at 12B, that's the mechanism.
