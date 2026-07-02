"""
Elicitation experiment runner.

Loads prompts from a YAML file, runs them through a model,
and saves results to a per-model CSV.

Usage (from notebook):
    from src.elicitation import run_all_prompts
    results_df = run_all_prompts(model, model_name, PROJECT_ROOT)
"""

from pathlib import Path
import yaml
import pandas as pd


def load_prompts(prompts_path):
    """Load the consolidated prompt YAML file."""
    with open(prompts_path, 'r') as f:
        templates = yaml.safe_load(f)
    return templates['prompts']


def run_all_prompts(model, model_name, project_root, prompts_file='all_prompts.yml',
                    concepts=None, tag=None):
    """
    Run prompts through the model and save results.

    Args:
        model: A loaded TransformerLens model.
        model_name: Full model name (e.g. "EleutherAI/pythia-160m").
        project_root: Path to the project root directory.
        prompts_file: Name of the YAML file in data/ (default: all_prompts.yml).
        concepts: Optional set/list of concept names; if given, only prompts
            whose concept is in this collection are run (e.g. PENDING_CRITERIA
            from src.accuracy_coding for the n=49 expansion).
        tag: Optional filename tag. tag='expansion' writes
            {model}-expansion-results.csv, protecting the original
            {model}-results.csv raws from being overwritten. The '-results'
            suffix is preserved so src.analysis.load_all_results picks it up.

    Returns:
        DataFrame with columns: prompt_id, concept, prompt_type,
        template_type, prompt, output, max_tokens, model
    """
    prompts_path = Path(project_root) / 'data' / prompts_file
    prompts = load_prompts(prompts_path)

    results = []

    for case in prompts:
        if concepts is not None and case['concept'] not in concepts:
            continue
        prompt = case['prompt']
        full_output = model.generate(prompt, max_new_tokens=case['max_tokens'], temperature=0)
        response = full_output[len(prompt):].strip()

        results.append({
            'prompt_id': case['prompt_id'],
            'concept': case['concept'],
            'prompt_type': case['prompt_type'],
            'template_type': case['template_type'],
            'prompt': prompt,
            'output': response,
            'max_tokens': case['max_tokens'],
            'model': model_name
        })

    results_df = pd.DataFrame(results)

    # Save per-model CSV
    short_name = model_name.split('/')[-1]
    suite = 'pythia' if 'pythia' in short_name else 'gpt2'
    output_dir = Path(project_root) / 'results' / suite
    output_dir.mkdir(parents=True, exist_ok=True)
    run_name = f'{short_name}-{tag}-results.csv' if tag else f'{short_name}-results.csv'
    output_path = output_dir / run_name
    results_df.to_csv(output_path, index=False)
    print(f"Saved {len(results_df)} results to {output_path}")

    return results_df
