# Cell 5: Experiment 1 — Run all prompts
import yaml
import pandas as pd

pd.set_option('display.max_colwidth', 200)

# Load consolidated prompt file
with open(PROJECT_ROOT / 'data' / 'all_prompts.yml', 'r') as f:
    templates = yaml.safe_load(f)

# Run every prompt through the loaded model
all_results = []

for case in templates['prompts']:
    prompt = case['prompt']
    full_output = model.generate(prompt, max_new_tokens=case['max_tokens'], temperature=0)
    response = full_output[len(prompt):].strip()

    all_results.append({
        'prompt_id': case['prompt_id'],
        'concept': case['concept'],
        'prompt_type': case['prompt_type'],
        'template_type': case['template_type'],
        'prompt': prompt,
        'output': response,
        'max_tokens': case['max_tokens'],
        'model': model_name
    })

results_df = pd.DataFrame(all_results)

# Save per-model CSV
short_name = model_name.split('/')[-1]  # "EleutherAI/pythia-160m" -> "pythia-160m"
output_path = PROJECT_ROOT / 'results' / 'pythia' / f'{short_name}-results.csv'
results_df.to_csv(output_path, index=False)
print(f"Saved {len(results_df)} results to {output_path}")

# Display
results_df.style.set_properties(**{'text-align': 'left'}).set_table_styles([
    {'selector': 'th', 'props': [('text-align', 'center')]}
]).hide(axis='index')
