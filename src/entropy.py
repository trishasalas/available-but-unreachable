"""
Entropy analysis module.

Computes mean and last-token entropy on prompts to measure
the model's internal uncertainty at the point of generation.

Usage (from notebook):
    from src.entropy import run_entropy_analysis
    entropy_df = run_entropy_analysis(model, model_name, PROJECT_ROOT)
"""

from pathlib import Path
import torch
import yaml
import pandas as pd


def compute_entropy(logits):
    """
    Compute entropy from logits at each token position.

    H = -Σ P(x_i) log P(x_i)

    Args:
        logits: Tensor of shape [1, seq_len, vocab_size]

    Returns:
        Tensor of entropy values, one per token position [seq_len]
    """
    probs = torch.nn.functional.softmax(logits[0], dim=-1)
    log_probs = torch.log(probs + 1e-10)  # small epsilon to avoid log(0)
    entropy = -torch.sum(probs * log_probs, dim=-1)
    return entropy


def run_entropy_analysis(model, model_name, project_root, prompts_file='all_prompts.yml'):
    """
    Compute entropy for all prompts and save results.

    For each prompt, computes:
        - mean_entropy: average entropy across all token positions
        - last_token_entropy: entropy at the final token (generation point)
        - max_entropy: highest entropy at any position
        - min_entropy: lowest entropy at any position

    Args:
        model: A loaded TransformerLens model.
        model_name: Full model name (e.g. "EleutherAI/pythia-160m").
        project_root: Path to the project root directory.
        prompts_file: Name of the YAML file in data/ (default: all_prompts.yml).

    Returns:
        DataFrame with entropy measurements for all prompts.
    """
    prompts_path = Path(project_root) / 'data' / prompts_file
    with open(prompts_path, 'r') as f:
        templates = yaml.safe_load(f)

    results = []

    for case in templates['prompts']:
        prompt = case['prompt']
        tokens = model.to_tokens(prompt)
        logits = model(tokens)

        entropy = compute_entropy(logits)

        results.append({
            'prompt_id': case['prompt_id'],
            'concept': case['concept'],
            'prompt_type': case['prompt_type'],
            'template_type': case['template_type'],
            'prompt': prompt,
            'n_tokens': len(entropy),
            'mean_entropy': round(entropy.mean().item(), 4),
            'last_token_entropy': round(entropy[-1].item(), 4),
            'max_entropy': round(entropy.max().item(), 4),
            'min_entropy': round(entropy.min().item(), 4),
            'model': model_name
        })

    entropy_df = pd.DataFrame(results)

    # Save per-model CSV
    short_name = model_name.split('/')[-1]
    suite = 'pythia' if 'pythia' in short_name else 'gpt2'
    output_dir = Path(project_root) / 'results' / suite
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f'{short_name}-entropy.csv'
    entropy_df.to_csv(output_path, index=False)
    print(f"Saved {len(entropy_df)} entropy measurements to {output_path}")

    return entropy_df
