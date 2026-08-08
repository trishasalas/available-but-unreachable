# Entropy Notebooks + Manifest Update — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Extend the manifest with GPU/HF/revision fields, then update the 3 entropy notebooks to use the 5 YAML prompt files and the updated manifest.

**Architecture:** One shared manifest function in `src/manifest.py` serves all experiment types via a `battery_name` parameter. Each entropy notebook inlines `compute_entropy()` and loops over the 5 YAML files, saving per-domain CSVs and a battery-specific manifest. The `src/entropy.py` module is intentionally left unchanged to avoid breaking `binding-pythia.ipynb`.

**Tech Stack:** Python, TransformerLens 2.18.0, PyTorch, HuggingFace `huggingface_hub`, YAML

## Global Constraints

- `transformer_lens==2.18.0`, `numpy==1.26.4`, `transformers==4.57.6`
- OLMo revisions come from `src/olmo_config.py` — never hardcode them
- These are Jupyter notebooks run on Colab (A100) — no pytest, no CI. Testing = "run the cell, check the output"
- Don't modify `src/entropy.py` or `src/binding.py`
- Don't modify elicitation or binding or frequency notebooks

---

### Task 1: Extend `src/manifest.py`

**Files:**
- Modify: `src/manifest.py` (all 49 lines)

**Interfaces:**
- Produces: `create_manifest_file(PROJECT_ROOT, output_dir, model_name, model, battery_name, domain_counts, results_df, prompt_files, gen_kwargs=None, hf_commit_sha=None, revision=None)` — writes a Markdown manifest file to `output_dir / f'{model_name}-{battery_name}.md'`

- [ ] **Step 1: Update the function signature**

Change the signature from:
```python
def create_manifest_file(PROJECT_ROOT, output_dir, model_name, model, gen_kwargs, domain_counts, results_df, prompt_files):
```

To:
```python
def create_manifest_file(PROJECT_ROOT, output_dir, model_name, model, battery_name, domain_counts, results_df, prompt_files, gen_kwargs=None, hf_commit_sha=None, revision=None):
```

Note: `battery_name` is positional (required). `gen_kwargs` moves to keyword-only with `None` default.

- [ ] **Step 2: Update the filename and header**

Change:
```python
with open(output_dir / f'{model_name}-elicitation.md', 'w') as f:
    f.write(f"# Model data captured during Elicitation Battery\n\n")
```

To:
```python
with open(output_dir / f'{model_name}-{battery_name}.md', 'w') as f:
    f.write(f"# Model data captured during {battery_name.title()} Battery\n\n")
```

- [ ] **Step 3: Add revision to the Model section**

After the existing `f.write(f"- Params: ...")` line, add:
```python
if revision:
    f.write(f"- Revision: {revision}\n")
f.write(f"\n")
```

And remove the existing `f.write(f"\n")` that currently follows the Params line (to avoid a double blank line).

- [ ] **Step 4: Add the Server section**

After the Model section (after the revision/newline block), add:
```python
f.write(f"## Server\n\n")
import torch
if torch.cuda.is_available():
    gpu_name = torch.cuda.get_device_name(0)
    f.write(f"- GPU: {gpu_name}\n")
elif torch.backends.mps.is_available():
    f.write(f"- GPU: Apple MPS\n")
else:
    f.write(f"- GPU: CPU\n")
f.write(f"\n")
```

Move `import torch` to the top of the file alongside the other imports.

- [ ] **Step 5: Make the Generation section conditional**

Change the Generation section from unconditional:
```python
f.write(f"## Generation\n\n")
for k, v in gen_kwargs.items():
    f.write(f"- {k}: {v}\n")
f.write(f"\n")
```

To conditional:
```python
if gen_kwargs:
    f.write(f"## Generation\n\n")
    for k, v in gen_kwargs.items():
        f.write(f"- {k}: {v}\n")
    f.write(f"\n")
```

- [ ] **Step 6: Add the Hugging Face section**

After the Environment section, before the Domains section, add:
```python
if hf_commit_sha:
    f.write(f"## Hugging Face\n\n")
    f.write(f"- Commit SHA: {hf_commit_sha}\n")
    if revision:
        f.write(f"- Revision: {revision}\n")
    f.write(f"\n")
```

- [ ] **Step 7: Verify the complete file**

The final file should have this section order:
1. Header (battery name)
2. Run metadata (UTC timestamp, git commit)
3. `## Model` (name, dtype, device, layers, heads, hidden, vocab, params, optional revision)
4. `## Server` (GPU name)
5. `## Generation` (only if gen_kwargs provided)
6. `## Environment` (package versions)
7. `## Hugging Face` (only if hf_commit_sha provided)
8. `## Domains` (expected vs written table)

Read the file back and confirm it matches.

- [ ] **Step 8: Smoke test — verify existing elicitation calls still work**

The elicitation notebooks call:
```python
create_manifest_file(
    PROJECT_ROOT, output_dir, model_name, model,
    GEN_KWARGS, domain_counts, results_df, prompt_files,
)
```

This passes `GEN_KWARGS` (a dict) as the 5th positional arg, which is now `battery_name`. This **will break**. The elicitation notebooks need their calls updated to use the new signature:

```python
create_manifest_file(
    PROJECT_ROOT, output_dir, model_name, model,
    "elicitation", domain_counts, results_df, prompt_files,
    gen_kwargs=GEN_KWARGS,
)
```

**Do NOT modify the elicitation notebooks in this task** — they're out of scope per the spec. But note this in the plan: the elicitation notebooks will need a one-line fix to their `create_manifest_file()` calls before their next run. Log this as a known follow-up.

Actually — to avoid breaking elicitation notebooks silently, add a type guard at the top of the function:
```python
if isinstance(battery_name, dict):
    raise TypeError(
        "create_manifest_file() signature changed: battery_name is now the 5th arg. "
        "Pass gen_kwargs as a keyword argument: gen_kwargs={...}"
    )
```

This will give a clear error message if someone runs an old-style call.

- [ ] **Step 9: Commit**

```bash
git add src/manifest.py
git commit -m "extend manifest with battery_name, GPU, HF commit SHA, revision"
```

---

### Task 2: Update `notebooks/entropy-pythia.ipynb`

**Files:**
- Modify: `notebooks/entropy-pythia.ipynb`

**Interfaces:**
- Consumes: `create_manifest_file(PROJECT_ROOT, output_dir, model_name, model, "entropy", domain_counts, results_df, prompt_files)` from Task 1

- [ ] **Step 1: Rewrite the entropy battery cell**

Replace the current entropy cell (which references `all_prompts.yml` and produces a flat 92-row result) with the multi-domain version. The cell to replace is the one containing `prompts_path = PROJECT_ROOT / 'data' / 'all_prompts.yml'`.

New cell content:

```python
from pathlib import Path
import torch
import yaml
import pandas as pd
from src.manifest import create_manifest_file

def compute_entropy(logits):
    """H = -Σ P(x_i) log P(x_i)"""
    probs = torch.nn.functional.softmax(logits[0], dim=-1)
    log_probs = torch.log(probs + 1e-10)
    entropy = -torch.sum(probs * log_probs, dim=-1)
    return entropy

prompt_files = [
    'control.yaml',
    'accessibility.yaml',
    'medical.yaml',
    'legal.yaml',
    'finance.yaml',
]

all_results = []
domain_counts = {}

output_dir = PROJECT_ROOT / 'results' / 'entropy' / 'pythia' / model_name
output_dir.mkdir(parents=True, exist_ok=True)

for prompts_file in prompt_files:
    domain = Path(prompts_file).stem
    prompts_path = PROJECT_ROOT / 'data' / prompts_file
    with open(prompts_path, 'r') as f:
        templates = yaml.safe_load(f)
    prompts = templates['prompts']
    print(f"\n--- Running {domain}: {len(prompts)} prompts ---")

    results = []
    for i, case in enumerate(prompts):
        print(f"\r  {i+1}/{len(prompts)}", end="")
        prompt = case['prompt']
        tokens = model.to_tokens(prompt)
        with torch.no_grad():
            logits = model(tokens)
        entropy = compute_entropy(logits)

        results.append({
            'domain': domain,
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
            'model': model_name,
        })
    print()

    domain_df = pd.DataFrame(results)
    filename = f'{model_name}-{domain}.csv'
    domain_df.to_csv(output_dir / filename, index=False)
    all_results.append(domain_df)

    domain_counts[domain] = {
        'expected': len(prompts),
        'written': len(domain_df),
        'file': filename,
    }

print(f"  → {filename}  ({len(domain_df)} rows)")

results_df = pd.concat(all_results, ignore_index=True)

create_manifest_file(
    PROJECT_ROOT, output_dir, model_name, model,
    "entropy", domain_counts, results_df, prompt_files,
)
print(f"\nSaved {len(results_df)} rows across {len(all_results)} domains → {output_dir}")
```

- [ ] **Step 2: Remove the old save-results cell**

Delete the cell that previously saved a single `{short_name}-entropy.csv` file:
```python
output_dir = PROJECT_ROOT / 'results' / 'entropy' / suite
...
entropy_df.to_csv(output_path, index=False)
```

This is now handled inside the battery cell above.

- [ ] **Step 3: Remove the old hand-written manifest cell**

Delete the cell that writes the manual markdown file:
```python
with open(output_dir / f'{model_name}-elicitation-entropy-binding.md', 'w') as f:
    f.write(f"# Model data captured during Elicitation/Entropy/Binding Battery\n")
    ...
```

This is now handled by `create_manifest_file()`.

- [ ] **Step 4: Verify notebook structure**

Read back the notebook and confirm this cell order:
1. Markdown: `# Entropy - Pythia Model Family` (keep existing)
2. Environment detection
3. Dependency pinning
4. Project root & path setup
5. Imports (torch, HookedTransformer)
6. Model name variable (`model_name = "pythia-160m"`)
7. Model loading (`HookedTransformer.from_pretrained(f"EleutherAI/{model_name}")`)
8. Markdown: `### Entropy`
9. Entropy battery cell (the new one from Step 1)
10. Git commit & push
11. Markdown: `### Delete Model & Clear Cache`
12. Memory cleanup

- [ ] **Step 5: Commit**

```bash
git add notebooks/entropy-pythia.ipynb
git commit -m "entropy-pythia: 5 YAML domains, manifest, per-domain CSVs"
```

---

### Task 3: Update `notebooks/entropy-gpt2.ipynb`

**Files:**
- Modify: `notebooks/entropy-gpt2.ipynb`

**Interfaces:**
- Consumes: `create_manifest_file(...)` from Task 1

- [ ] **Step 1: Rewrite the entropy battery cell**

Same as Task 2 Step 1, except the output directory line changes to:
```python
output_dir = PROJECT_ROOT / 'results' / 'entropy' / 'gpt2' / model_name
```

Everything else in the battery cell is identical to Task 2.

- [ ] **Step 2: Remove the old save-results cell**

Delete the cell containing:
```python
output_dir = PROJECT_ROOT / 'results' / 'entropy' / 'gpt2' / model_name
...
entropy_df.to_csv(output_path, index=False)
```

- [ ] **Step 3: Remove the old hand-written manifest cell**

Delete the cell containing:
```python
with open(output_dir / f'{model_name}-entropy.md', 'w') as f:
    f.write(f"# Model data captured during Entropy Battery\n")
    ...
```

- [ ] **Step 4: Verify notebook structure**

Same cell order as Task 2 Step 4, but with:
- Header: `# Entropy - GPT2 Model Family`
- Model loading: `HookedTransformer.from_pretrained(f"{model_name}")`

- [ ] **Step 5: Commit**

```bash
git add notebooks/entropy-gpt2.ipynb
git commit -m "entropy-gpt2: 5 YAML domains, manifest, per-domain CSVs"
```

---

### Task 4: Update `notebooks/entropy-olmo.ipynb`

**Files:**
- Modify: `notebooks/entropy-olmo.ipynb`

**Interfaces:**
- Consumes: `create_manifest_file(...)` from Task 1, `OLMO_REVISIONS` from `src/olmo_config`, `load_olmo2_tl217` from `src/tl217_olmo2_adapter`

- [ ] **Step 1: Fix the markdown header**

Replace the current header (which has wrong revisions) with:
```markdown
# Entropy - OLMo 2 Model Family

### Olmo 2 - 1B
model_name = OLMo-2-0425-1B  
revision = stage1-step1907359-tokens4001B

### Olmo 2 - 7B
model_name = OLMo-2-1124-7B  
revision = stage1-step928646-tokens3896B

### Olmo 2 - 13B
model_name = OLMo-2-1124-13B  
revision = stage1-step596057-tokens5001B
```

These match `OLMO_REVISIONS` in `src/olmo_config.py`.

- [ ] **Step 2: Add OLMo-specific imports cell**

After the general imports cell (torch, HookedTransformer), add a cell:
```python
import src
from src.olmo_config import OLMO_REVISIONS
from src.tl217_olmo2_adapter import load_olmo2_tl217
```

If this cell already exists, verify it imports `OLMO_REVISIONS`.

- [ ] **Step 3: Fix the model name + revision cell**

Replace the current hardcoded revision:
```python
model_name = "OLMo-2-0425-1B" 
revision = "stage1-step990000-tokens2077B"
short_name = model_name.split('/')[-1] 
```

With:
```python
model_name = "OLMo-2-0425-1B"
revision = OLMO_REVISIONS[model_name]
```

- [ ] **Step 4: Verify model loading cell uses the adapter**

Confirm the model loading cell reads:
```python
model = load_olmo2_tl217(f"allenai/{model_name}", device=device, revision=revision)
```

(This should already be correct in the current notebook.)

- [ ] **Step 5: Rewrite the entropy battery cell**

Same structure as Task 2 Step 1, with these differences:

Output directory:
```python
output_dir = PROJECT_ROOT / 'results' / 'entropy' / 'olmo' / model_name
```

And the manifest call at the end includes the OLMo-specific fields:
```python
from huggingface_hub import model_info
info = model_info(f"allenai/{model_name}")

create_manifest_file(
    PROJECT_ROOT, output_dir, model_name, model,
    "entropy", domain_counts, results_df, prompt_files,
    hf_commit_sha=info.sha, revision=revision,
)
```

Full cell content:

```python
from pathlib import Path
import torch
import yaml
import pandas as pd
from src.manifest import create_manifest_file
from huggingface_hub import model_info

def compute_entropy(logits):
    """H = -Σ P(x_i) log P(x_i)"""
    probs = torch.nn.functional.softmax(logits[0], dim=-1)
    log_probs = torch.log(probs + 1e-10)
    entropy = -torch.sum(probs * log_probs, dim=-1)
    return entropy

prompt_files = [
    'control.yaml',
    'accessibility.yaml',
    'medical.yaml',
    'legal.yaml',
    'finance.yaml',
]

all_results = []
domain_counts = {}

output_dir = PROJECT_ROOT / 'results' / 'entropy' / 'olmo' / model_name
output_dir.mkdir(parents=True, exist_ok=True)

for prompts_file in prompt_files:
    domain = Path(prompts_file).stem
    prompts_path = PROJECT_ROOT / 'data' / prompts_file
    with open(prompts_path, 'r') as f:
        templates = yaml.safe_load(f)
    prompts = templates['prompts']
    print(f"\n--- Running {domain}: {len(prompts)} prompts ---")

    results = []
    for i, case in enumerate(prompts):
        print(f"\r  {i+1}/{len(prompts)}", end="")
        prompt = case['prompt']
        tokens = model.to_tokens(prompt)
        with torch.no_grad():
            logits = model(tokens)
        entropy = compute_entropy(logits)

        results.append({
            'domain': domain,
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
            'model': model_name,
        })
    print()

    domain_df = pd.DataFrame(results)
    filename = f'{model_name}-{domain}.csv'
    domain_df.to_csv(output_dir / filename, index=False)
    all_results.append(domain_df)

    domain_counts[domain] = {
        'expected': len(prompts),
        'written': len(domain_df),
        'file': filename,
    }

print(f"  → {filename}  ({len(domain_df)} rows)")

results_df = pd.concat(all_results, ignore_index=True)

info = model_info(f"allenai/{model_name}")

create_manifest_file(
    PROJECT_ROOT, output_dir, model_name, model,
    "entropy", domain_counts, results_df, prompt_files,
    hf_commit_sha=info.sha, revision=revision,
)
print(f"\nSaved {len(results_df)} rows across {len(all_results)} domains → {output_dir}")
```

- [ ] **Step 6: Remove old save-results and manifest cells**

Delete the cell saving `{short_name}-entropy.csv` and the cell writing `{model_name}-entropy.md`.

- [ ] **Step 7: Verify notebook structure**

Cell order:
1. Markdown: `# Entropy - OLMo 2 Model Family` (updated revisions)
2. Environment detection
3. Dependency pinning
4. Project root & path setup
5. General imports (torch, HookedTransformer)
6. OLMo imports (`OLMO_REVISIONS`, `load_olmo2_tl217`)
7. Model name + revision (`revision = OLMO_REVISIONS[model_name]`)
8. Model loading (`load_olmo2_tl217(...)`)
9. Markdown: `### Entropy`
10. Entropy battery cell (with HF commit SHA)
11. Git commit & push
12. Markdown: `### Delete Model & Clear Cache`
13. Memory cleanup

- [ ] **Step 8: Commit**

```bash
git add notebooks/entropy-olmo.ipynb
git commit -m "entropy-olmo: 5 YAML domains, manifest, correct OLMO_REVISIONS, HF SHA"
```

---

## Known Follow-ups (out of scope)

- **Elicitation notebooks:** Their `create_manifest_file()` calls pass `GEN_KWARGS` as the 5th positional arg, which is now `battery_name`. They'll get a clear `TypeError` on next run. Fix: change the call to `create_manifest_file(PROJECT_ROOT, output_dir, model_name, model, "elicitation", domain_counts, results_df, prompt_files, gen_kwargs=GEN_KWARGS)`. The type guard added in Task 1 Step 8 ensures the error message is obvious.
- **Binding notebooks:** Need differentiation (gpt2/olmo are clones of pythia), new domain compounds TBD.
- **Frequency notebooks:** Structurally different, deferred.
- **`src/entropy.py`:** Still references `all_prompts.yml`. Safe to leave — only `binding-pythia.ipynb` imports it.
