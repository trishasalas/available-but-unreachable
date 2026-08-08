# Binding Notebook Migration — GPT-2

**Date:** 2026-08-08
**Status:** Approved

## Problem

`src/binding.py` was written for a single compound list. Four more domains
(CONTROL, LEGAL, MEDICAL, FINANCE) were added alongside the original
ACCESSIBILITY array, but `run_binding_sweep()` was never updated to consume
them. Its `compounds=None` default assigns a list of *strings*:

```python
compounds = ['CONTROL', 'ACCESSIBILITY', 'MEDICAL', 'LEGAL', 'FINANCE']
```

The loop then does `for compound_name, word1, word2, prompt in compounds:`,
which tries to unpack the 7-character string `'CONTROL'` into four names and
raises `ValueError`. The call in `binding-gpt2.ipynb` cannot be running today.

`run_binding_sweep()` also picks its own output directory from the model name:

```python
suite = 'pythia' if 'pythia' in short_name else 'gpt2'
```

The elicitation and entropy batteries put that decision in the notebook, where
it is visible next to the model being run. Binding is the last battery still
inferring it.

The prior spec (`2026-08-07-entropy-manifest-update-design.md`) deferred the
binding notebooks with "compound scope TBD". This spec resolves that for GPT-2.

## Scope

### In scope

1. Convert the 5 compound arrays to `data/binding/*.yaml`
2. Replace `binding-gpt2.ipynb` cell 9 with a self-contained battery cell
3. Delete `binding-gpt2.ipynb` cell 10 (superseded by `create_manifest_file`)

### Out of scope

- `src/binding.py` — **unmodified**, including its 5 arrays. See Risks.
- `binding-pythia.ipynb` / `binding-olmo.ipynb` — follow-up, same pattern
- `src/qk_ov.py`, `src/head_characterization.py`, `src/d6_multihead_ablation.py`
- Existing result files on disk, including `results/_archive/*-binding.csv`

## Design

### 1. `data/binding/*.yaml` — 5 new files

One file per domain, named to match `data/*.yaml` so the notebook loop reads
the same as entropy's:

Listed in run order (the order of `prompt_files` in the notebook):

| file | compounds |
|---|---|
| `data/binding/control.yaml` | 44 |
| `data/binding/accessibility.yaml` | 53 |
| `data/binding/medical.yaml` | 42 |
| `data/binding/legal.yaml` | 44 |
| `data/binding/finance.yaml` | 44 |
| **total** | **227** |

Schema:

```yaml
compounds:
  - name: blue_sky
    word1: blue
    word2: sky
    prompt: I like to look at the blue sky
```

The four keys map to the existing tuple positions
`(compound_name, word1, word2, prompt)`. No compound name repeats within a
domain (verified).

**Conversion is mechanical, not retyped.** A throwaway script in the session
scratchpad `ast.literal_eval`s the five arrays out of `src/binding.py`, writes
the YAML, then reloads each file and asserts it round-trips tuple-for-tuple
against the source array. Nothing is hand-transcribed.

### 2. `notebooks/binding-gpt2.ipynb` cell 9 — replaced

Self-contained, structured to match `entropy-gpt2.ipynb` cell 10:

```python
from pathlib import Path
import torch, yaml, pandas as pd
from src.manifest import create_manifest_file

def find_token_index(tokens, target):
    """Subword-aware index lookup; returns the LAST subtoken of a span."""
    ...   # own copy — logic unchanged from src/binding.py

prompt_files = ['control.yaml', 'accessibility.yaml',
                'medical.yaml', 'legal.yaml', 'finance.yaml']

all_results, domain_counts = [], {}

output_dir = PROJECT_ROOT / 'results' / 'binding' / 'gpt2' / model_name
output_dir.mkdir(parents=True, exist_ok=True)

for prompts_file in prompt_files:
    domain = Path(prompts_file).stem
    with open(PROJECT_ROOT / 'data' / 'binding' / prompts_file) as f:
        compounds = yaml.safe_load(f)['compounds']
    ...
    domain_df.to_csv(output_dir / f'{model_name}-{domain}.csv', index=False)

create_manifest_file(PROJECT_ROOT, output_dir, model_name, model,
                     "binding", domain_counts, results_df, prompt_files)
```

The `suite = 'pythia' if ... else 'gpt2'` conditional is gone. The path is
literal in the notebook; `binding-pythia.ipynb` will differ only in that one
segment.

Per compound:

1. `tokens = model.to_str_tokens(prompt)`
2. Resolve `idx1`, `idx2` via `find_token_index`; if either is `None`, record
   the compound as unresolved, print the warning, and continue
3. `target_idx = max(idx1, idx2)`, `source_idx = min(idx1, idx2)` — the later
   token attending back to the earlier one
4. `model.run_with_cache(prompt, names_filter=lambda n: n.endswith("pattern"))`
5. Emit one row per `layer × head` reading
   `cache["pattern", layer][0, head][target_idx, source_idx]`, rounded to 4dp

**`names_filter` is new.** `run_single_compound` currently calls
`run_with_cache(prompt)` with no filter, caching every activation in the model
when only attention patterns are ever read. On gpt2-xl and pythia-12b that is a
large amount of memory held for nothing.

### 3. Output files

Per model run, in `results/binding/gpt2/{model_name}/`:

- `{model_name}-accessibility.csv`
- `{model_name}-control.csv`
- `{model_name}-legal.csv`
- `{model_name}-medical.csv`
- `{model_name}-finance.csv`
- `{model_name}-binding.md` (manifest)

CSV schema per row — archived column order plus `domain`:

```
compound, layer, head, binding_score, word1, word2, prompt, tokens,
word1_idx, word2_idx, domain, model
```

Approximate row counts: gpt2-small (12L × 12H) ≈ 32.7K rows total across the
five files; gpt2-xl (48L × 25H) ≈ 272K rows, largest single domain file
≈ 64K rows.

### 4. `binding-gpt2.ipynb` cell 10 — deleted

It hand-writes `{model_name}-binding.md` into the same directory with a subset
of the manifest's fields (name, dtype, layers, heads, hidden size, params).
`create_manifest_file` writes that exact filename with all of those plus git
commit and dirty flag, device, vocab size, GPU, environment versions, and the
domain table. Keeping both means two writers racing for one path.

### 5. Unresolved-compound reporting

`run_single_compound` currently prints a warning and returns `[]` when a word
cannot be located in its prompt. With 227 compounds a silent drop is easy to
miss in scrollback.

`domain_counts` carries the check into the manifest:

```python
domain_counts[domain] = {
    'expected': len(compounds) * model.cfg.n_layers * model.cfg.n_heads,
    'written': len(domain_df),
    'file': filename,
}
```

`create_manifest_file` already appends ⚠️ to any row where `expected != written`
(`src/manifest.py:73`), so an unresolved compound shows up as a flagged row in
the committed manifest rather than only in a print statement.

## Risks

- **The 227 compounds exist in two places after this change** — the YAML files
  and the arrays still in `src/binding.py`. They can drift. Removing the arrays
  now would break `binding-pythia.ipynb` and `binding-olmo.ipynb`, which still
  call `run_binding_sweep()`. Strip them once all three notebooks are migrated,
  not before.

- **`src/binding.py` keeps a broken `run_binding_sweep()`.** Its `compounds=None`
  default still raises `ValueError`. The pythia and olmo notebooks pass no
  `compounds` argument, so they are already non-functional; this change neither
  fixes nor worsens them. Their migration is the fix.

- **`find_token_index` is duplicated** into the notebook. This follows the
  established precedent — `src/entropy.py:18` defines `compute_entropy` and
  `entropy-gpt2.ipynb` redefines it inline rather than importing. The src copy
  must stay regardless: `qk_ov.py:26`, `head_characterization.py:34`, and
  `d6_multihead_ablation.py:42` all import it.

- **Row counts grow ~20×** versus the archived runs (11 compounds → 227). The
  archived `gpt2-binding.csv` is 198K; gpt2-xl will land near 35MB across five
  files in a git-tracked `results/`. Accepted for now; the per-domain split
  keeps any single file manageable and the schema comparable to the archive.

- **New output directory.** `results/binding/gpt2/{model_name}/` does not
  collide with `results/_archive/{model_name}-binding.csv`, so no prior data is
  overwritten.
