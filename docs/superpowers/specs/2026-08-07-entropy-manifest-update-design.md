# Entropy Notebooks + Manifest Update

**Date:** 2026-08-07
**Status:** Approved

## Problem

The entropy notebooks (pythia, gpt2, olmo) reference `all_prompts.yml`, which
no longer exists — it was split into 5 domain-specific YAML files during the
elicitation update. The notebooks also use hand-written markdown manifests
instead of the shared `create_manifest_file()` from `src/manifest.py`. The
OLMo entropy notebook hardcodes wrong checkpoint revisions that don't match
`OLMO_REVISIONS` in `src/olmo_config.py`.

The manifest itself is missing fields needed for reproducibility: GPU type,
HF commit SHA (for OLMo), and checkpoint revision.

## Scope

### In scope

1. Extend `src/manifest.py` with new fields
2. Update 3 entropy notebooks to use 5 YAML prompt files + updated manifest

### Out of scope

- Binding notebooks (deferred — compound scope TBD)
- Frequency notebooks (deferred — structurally different)
- `src/entropy.py` module (left as-is to avoid breaking `binding-pythia.ipynb`)
- Elicitation notebooks (already updated, can adopt new manifest fields later)
- Existing result files on disk

## Design

### 1. `src/manifest.py`

Extend `create_manifest_file()` signature:

```python
def create_manifest_file(
    PROJECT_ROOT, output_dir, model_name, model,
    battery_name,                          # NEW — required: "elicitation", "entropy", etc.
    domain_counts, results_df, prompt_files,
    gen_kwargs=None,                       # CHANGED — now optional (entropy has no gen kwargs)
    hf_commit_sha=None,                    # NEW — optional: HF model commit SHA
    revision=None,                         # NEW — optional: OLMo checkpoint revision
):
```

Changes to the output:

- **Filename:** `{model_name}-{battery_name}.md` (was `{model_name}-elicitation.md`)
- **Header:** `"# Model data captured during {battery_name.title()} Battery"`
- **Model section:** Add `- Revision: {revision}` line when provided
- **Generation section:** Omitted entirely when `gen_kwargs` is `None`
- **New Server section** (after Model): Auto-detect and record GPU info:
  - CUDA: `torch.cuda.get_device_name(0)`
  - MPS: `"Apple MPS"`
  - CPU: `"CPU"`
- **New Hugging Face section** (after Server): When `hf_commit_sha` is provided:
  - `- Commit SHA: {hf_commit_sha}`
  - `- Revision: {revision}` (repeated here for the HF context)

This replaces the bolt-on `-commit-sha.md` file the OLMo elicitation notebook
currently writes separately.

### 2. `notebooks/entropy-pythia.ipynb`

Structure (matching elicitation pattern):

1. Environment detection (Colab vs Local)
2. Dependency pinning (`transformer_lens==2.18.0`, `numpy==1.26.4`, `transformers==4.57.6`)
3. Project root & path setup (Colab clone or local `Path.cwd().parent`)
4. Imports (torch, HookedTransformer)
5. Model name variable: `model_name = "pythia-160m"`
6. Model loading: `HookedTransformer.from_pretrained(f"EleutherAI/{model_name}")`
7. Entropy battery cell:
   - Inline `compute_entropy()` function
   - Loop over 5 YAML prompt files
   - For each prompt: tokenize, forward pass, compute entropy
   - Results include `domain` column
   - Save per-domain CSVs to `results/entropy/pythia/{model_name}/`
   - Track `domain_counts` dict
8. Manifest: `create_manifest_file(..., battery_name="entropy")`
9. Git commit & push
10. Delete model & clear cache

Output files per model run:
- `results/entropy/pythia/{model_name}/{model_name}-accessibility.csv`
- `results/entropy/pythia/{model_name}/{model_name}-control.csv`
- `results/entropy/pythia/{model_name}/{model_name}-medical.csv`
- `results/entropy/pythia/{model_name}/{model_name}-legal.csv`
- `results/entropy/pythia/{model_name}/{model_name}-finance.csv`
- `results/entropy/pythia/{model_name}/{model_name}-entropy.md` (manifest)

CSV schema per row:
```
domain, prompt_id, concept, prompt_type, template_type, prompt,
n_tokens, mean_entropy, last_token_entropy, max_entropy, min_entropy, model
```

### 3. `notebooks/entropy-gpt2.ipynb`

Same structure as entropy-pythia, with:
- Model loading: `HookedTransformer.from_pretrained(f"{model_name}")`
- Output dir: `results/entropy/gpt2/{model_name}/`

### 4. `notebooks/entropy-olmo.ipynb`

Same structure, with these OLMo-specific additions:
- Import `OLMO_REVISIONS` from `src.olmo_config` (fixes wrong hardcoded revisions)
- Import `load_olmo2_tl217` from `src.tl217_olmo2_adapter`
- Model name + revision: `revision = OLMO_REVISIONS[model_name]`
- Model loading: `load_olmo2_tl217(f"allenai/{model_name}", device=device, revision=revision)`
- HF commit SHA cell: `model_info(f"allenai/{model_name}").sha`
- Manifest call includes `revision=revision, hf_commit_sha=info.sha`
- Output dir: `results/entropy/olmo/{model_name}/`
- Markdown header lists all 3 OLMo models with their correct revisions from `OLMO_REVISIONS`

## Risks

- **`src/entropy.py` left stale:** It still references `all_prompts.yml`. This is
  intentional — `binding-pythia.ipynb` imports `run_entropy_analysis()` from it.
  Updating it would require updating binding notebooks (out of scope). The entropy
  notebooks inline the computation instead of importing.

- **Existing entropy results on disk:** Old results used 92 prompts, new runs
  will produce 266. The files land in new per-model subdirectories so they
  won't overwrite old data.
