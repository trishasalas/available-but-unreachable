# Binding Notebook Migration (GPT-2) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Move binding-sweep orchestration out of `src/binding.py` and into
`notebooks/binding-gpt2.ipynb`, driven by five YAML domain files, matching the
structure already used by `entropy-gpt2.ipynb`.

**Architecture:** The 227 compound tuples become `data/binding/*.yaml`. The
notebook gains one self-contained cell that defines `find_token_index`, loops
the five domains, writes one CSV per domain, and calls the shared
`create_manifest_file`. `src/binding.py` is not modified — three other `src/`
modules import from it.

**Tech Stack:** Python 3.11 · TransformerLens 2.18 · PyTorch · pandas · PyYAML

## Global Constraints

- **Python interpreter for all verification scripts:**
  `/opt/homebrew/Caskroom/miniconda/base/envs/mechinterp/bin/python`
  (the `mechinterp` conda env — the base env lacks pandas and transformer_lens).
- **Working directory for all commands:** `/Users/trishasalas/Repos/Research/tmlr`
- **Scratchpad for throwaway scripts:**
  `/private/tmp/claude-501/-Users-trishasalas-Repos-Research-tmlr/35a30dac-d2d9-49c8-a191-050032d5453e/scratchpad`
  Nothing in this plan writes a permanent script to the repo.
- **`src/binding.py` is read-only for this plan.** Do not edit it, do not delete
  its arrays. `src/qk_ov.py:26`, `src/head_characterization.py:34`, and
  `src/d6_multihead_ablation.py:42` import `find_token_index` from it;
  `src/d6_multihead_ablation.py:44` also imports `run_single_compound`.
- **`binding-pythia.ipynb` and `binding-olmo.ipynb` are out of scope.** Do not
  touch them.
- **Compound counts (verified):** control 44, accessibility 53, medical 42,
  legal 44, finance 44 — **total 227**. Any script that produces different
  numbers has a bug.
- **CSV column order (exact):** `compound, layer, head, binding_score, word1,
  word2, prompt, tokens, word1_idx, word2_idx, domain, model`
- **Notebooks are lab records.** Do not reformat, restructure, or clear outputs
  on cells this plan does not name.

---

### Task 1: Generate `data/binding/*.yaml` from the arrays

Convert the five compound arrays in `src/binding.py` into YAML, verifying the
conversion round-trips exactly rather than trusting it.

**Files:**
- Create: `data/binding/control.yaml`
- Create: `data/binding/accessibility.yaml`
- Create: `data/binding/medical.yaml`
- Create: `data/binding/legal.yaml`
- Create: `data/binding/finance.yaml`
- Read only: `src/binding.py`
- Scratch: `<scratchpad>/convert_binding_yaml.py`

**Interfaces:**
- Consumes: nothing.
- Produces: five YAML files, each with a top-level `compounds:` key holding a
  list of mappings with exactly the keys `name`, `word1`, `word2`, `prompt`
  (all string values). Task 2 and Task 3 read these.

- [ ] **Step 1: Write the conversion script**

Create `<scratchpad>/convert_binding_yaml.py`. It parses `src/binding.py` with
`ast` rather than importing it, so no torch/pandas import is triggered:

```python
import ast
from pathlib import Path

import yaml

REPO = Path("/Users/trishasalas/Repos/Research/tmlr")
OUT = REPO / "data" / "binding"

# array name in src/binding.py -> output filename stem
DOMAINS = {
    "CONTROL": "control",
    "ACCESSIBILITY": "accessibility",
    "MEDICAL": "medical",
    "LEGAL": "legal",
    "FINANCE": "finance",
}

EXPECTED = {
    "control": 44, "accessibility": 53, "medical": 42,
    "legal": 44, "finance": 44,
}

HEADER = """\
# ============================================================
# Binding compounds — {domain}
# ============================================================
# Generated from src.binding.{array} — do not hand-edit both.
#
# Schema:
#   name    — compound identifier (unique within this file)
#   word1   — first constituent, the attention SOURCE (earlier token)
#   word2   — second constituent, the attention TARGET (later token)
#   prompt  — natural sentence containing both constituents
# ============================================================

"""

tree = ast.parse((REPO / "src" / "binding.py").read_text())
arrays = {
    node.targets[0].id: ast.literal_eval(node.value)
    for node in tree.body
    if isinstance(node, ast.Assign)
    and isinstance(node.targets[0], ast.Name)
    and node.targets[0].id in DOMAINS
}

assert set(arrays) == set(DOMAINS), f"missing arrays: {set(DOMAINS) - set(arrays)}"

OUT.mkdir(parents=True, exist_ok=True)

for array_name, stem in DOMAINS.items():
    tuples = arrays[array_name]
    records = [
        {"name": n, "word1": w1, "word2": w2, "prompt": p}
        for (n, w1, w2, p) in tuples
    ]

    path = OUT / f"{stem}.yaml"
    with open(path, "w") as f:
        f.write(HEADER.format(domain=stem, array=array_name))
        yaml.safe_dump(
            {"compounds": records},
            f,
            sort_keys=False,
            default_flow_style=False,
            allow_unicode=True,
            width=1000,
        )

    # Round-trip: reload and compare tuple-for-tuple against the source array.
    reloaded = yaml.safe_load(path.read_text())["compounds"]
    back = [(r["name"], r["word1"], r["word2"], r["prompt"]) for r in reloaded]
    assert back == list(tuples), f"{stem}: round-trip mismatch"
    assert len(back) == EXPECTED[stem], (
        f"{stem}: got {len(back)}, expected {EXPECTED[stem]}"
    )

    names = [r["name"] for r in reloaded]
    assert len(names) == len(set(names)), f"{stem}: duplicate compound names"

    print(f"  {stem:15s} {len(back):3d} compounds  round-trip OK")

total = sum(EXPECTED.values())
print(f"\nTotal: {total} compounds across {len(DOMAINS)} files -> {OUT}")
assert total == 227, f"expected 227 total, got {total}"
```

- [ ] **Step 2: Run it**

```bash
cd /Users/trishasalas/Repos/Research/tmlr
/opt/homebrew/Caskroom/miniconda/base/envs/mechinterp/bin/python \
  "/private/tmp/claude-501/-Users-trishasalas-Repos-Research-tmlr/35a30dac-d2d9-49c8-a191-050032d5453e/scratchpad/convert_binding_yaml.py"
```

Expected output — every line must say `round-trip OK`, and the total must be 227:

```
  control          44 compounds  round-trip OK
  accessibility    53 compounds  round-trip OK
  medical          42 compounds  round-trip OK
  legal            44 compounds  round-trip OK
  finance          44 compounds  round-trip OK

Total: 227 compounds across 5 files -> .../data/binding
```

If any assertion fires, fix the script and re-run. Do not proceed with a
mismatch.

- [ ] **Step 3: Eyeball one file**

```bash
head -25 data/binding/control.yaml
```

Expected: the header comment block, then `compounds:`, then the first record
with `name: blue_sky` / `word1: blue` / `word2: sky` / `prompt: I like to look
at the blue sky`. Confirm the apostrophe case survived quoting:

```bash
grep -n "tax shelter" data/binding/finance.yaml
```

Expected: the prompt `The tax shelter reduced the company's total liability`
appears intact (PyYAML will wrap it in double quotes or leave it bare — either
is fine as long as the apostrophe is present and the round-trip assertion
passed).

- [ ] **Step 4: Commit**

```bash
git add data/binding/
git commit -m "add data/binding YAML — 227 compounds across 5 domains

Generated from the arrays in src/binding.py and verified to round-trip
tuple-for-tuple. src/binding.py keeps its copies until binding-pythia
and binding-olmo are migrated."
```

---

### Task 2: Audit compound resolution under GPT-2 tokenization

`find_token_index` returns `None` when a constituent word cannot be located as a
token span in its prompt, and the battery skips that compound. Find out how many
of the 227 that affects *before* running the sweep, using the tokenizer alone.

**Files:**
- Read only: `data/binding/*.yaml`, `src/binding.py`
- Scratch: `<scratchpad>/audit_binding_tokens.py`

**Interfaces:**
- Consumes: the five YAML files from Task 1.
- Produces: a count of unresolvable compounds. No repo files change in this
  task unless the audit finds failures that need a decision.

- [ ] **Step 1: Write the audit script**

Create `<scratchpad>/audit_binding_tokens.py`. It imports `find_token_index`
from `src.binding` — the same function the notebook will copy — and uses the
raw HuggingFace GPT-2 tokenizer so no model weights load:

```python
import sys
from pathlib import Path

import yaml
from transformers import AutoTokenizer

REPO = Path("/Users/trishasalas/Repos/Research/tmlr")
sys.path.insert(0, str(REPO))

from src.binding import find_token_index  # noqa: E402

tok = AutoTokenizer.from_pretrained("gpt2")

FILES = ["control.yaml", "accessibility.yaml", "medical.yaml",
         "legal.yaml", "finance.yaml"]

failures = []
total = 0

for fname in FILES:
    data = yaml.safe_load((REPO / "data" / "binding" / fname).read_text())
    domain = Path(fname).stem
    for case in data["compounds"]:
        total += 1
        # Mirrors HookedTransformer.to_str_tokens, which prepends BOS.
        str_tokens = ["<|endoftext|>"] + [
            tok.decode([t]) for t in tok.encode(case["prompt"])
        ]
        i1 = find_token_index(str_tokens, case["word1"])
        i2 = find_token_index(str_tokens, case["word2"])
        if i1 is None or i2 is None:
            failures.append({
                "domain": domain,
                "name": case["name"],
                "word1": case["word1"], "found1": i1,
                "word2": case["word2"], "found2": i2,
                "tokens": str_tokens,
            })

print(f"Checked {total} compounds; {len(failures)} unresolvable\n")
for f in failures:
    miss = []
    if f["found1"] is None:
        miss.append(f"word1={f['word1']!r}")
    if f["found2"] is None:
        miss.append(f"word2={f['word2']!r}")
    print(f"  {f['domain']}/{f['name']}: missing {', '.join(miss)}")
    print(f"    tokens: {f['tokens']}\n")
```

- [ ] **Step 2: Run it**

```bash
cd /Users/trishasalas/Repos/Research/tmlr
/opt/homebrew/Caskroom/miniconda/base/envs/mechinterp/bin/python \
  "/private/tmp/claude-501/-Users-trishasalas-Repos-Research-tmlr/35a30dac-d2d9-49c8-a191-050032d5453e/scratchpad/audit_binding_tokens.py"
```

Expected: `Checked 227 compounds; N unresolvable`. The `227` must match; `N` is
the number being discovered.

- [ ] **Step 3: Act on the result**

- **If `N == 0`:** nothing to do. Record "227/227 resolve under GPT-2" and move
  to Task 3.
- **If `N > 0`:** **stop and report the failing compounds to Trisha.** Do not
  rewrite prompts or rename constituents to force a match — the prompts are
  experimental stimuli, and silently altering them changes what the measurement
  means. Present the list and let her decide. The battery already handles
  unresolved compounds by skipping them and flagging the count in the manifest,
  so a non-zero `N` does not block Task 3.

There is no commit in this task; it produces a finding, not a change.

---

### Task 3: Replace the battery cell in `binding-gpt2.ipynb`

**Files:**
- Modify: `notebooks/binding-gpt2.ipynb` — replace cell 9, delete cell 10

**Interfaces:**
- Consumes: `data/binding/*.yaml` (Task 1); `create_manifest_file` from
  `src/manifest.py:6` with signature
  `(PROJECT_ROOT, output_dir, model_name, model, battery_name, domain_counts,
  results_df, prompt_files, gen_kwargs=None, hf_commit_sha=None, revision=None)`.
- Produces: cell 9 defines `find_token_index`, `prompt_files`, `results_df`,
  `domain_counts`, `unresolved`, and `output_dir`. Task 4 executes this cell's
  source directly.

**Notebook cell indices before editing** (confirm with the command in Step 1):

| index | type | content |
|---|---|---|
| 9 | code | `from src.binding import run_binding_sweep` — **replace** |
| 10 | code | hand-written `{model_name}-binding.md` writer — **delete** |
| 11 | markdown | `### Delete Model & Clear Cache` — keep |
| 12 | code | free-memory cell — keep |

- [ ] **Step 1: Confirm the cell indices before editing**

```bash
cd /Users/trishasalas/Repos/Research/tmlr
/opt/homebrew/Caskroom/miniconda/base/envs/mechinterp/bin/python -c "
import json
nb = json.load(open('notebooks/binding-gpt2.ipynb'))
for i, c in enumerate(nb['cells']):
    s = c['source']
    s = ''.join(s) if isinstance(s, list) else s
    print(i, c['cell_type'], repr(s.strip().splitlines()[0] if s.strip() else '')[:70])
"
```

Expected: 13 cells; index 9 begins with the `# Binding — Uses \`src/binding\``
comment, index 10 begins with `output_dir = PROJECT_ROOT / 'results' / ...`.
If the indices differ, use the ones printed — do not edit by position blindly.

- [ ] **Step 2: Replace cell 9**

Use `NotebookEdit` with `cell_id`/index 9, `edit_mode: replace`, and this exact
source:

```python
# Binding Battery — Loads compound pairs from YAML, measures attention from the
# second constituent back to the first across every layer and head, and saves
# per-domain CSVs plus a run manifest.
from pathlib import Path
import torch
import yaml
import pandas as pd
from src.manifest import create_manifest_file


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


prompt_files = [
    'control.yaml',
    'accessibility.yaml',
    'medical.yaml',
    'legal.yaml',
    'finance.yaml',
]

all_results = []
domain_counts = {}
unresolved = []

output_dir = PROJECT_ROOT / 'results' / 'binding' / 'gpt2' / model_name
output_dir.mkdir(parents=True, exist_ok=True)

for prompts_file in prompt_files:
    domain = Path(prompts_file).stem
    prompts_path = PROJECT_ROOT / 'data' / 'binding' / prompts_file
    with open(prompts_path, 'r') as f:
        templates = yaml.safe_load(f)
    compounds = templates['compounds']
    print(f"\n--- Running {domain}: {len(compounds)} compounds ---")

    results = []
    for i, case in enumerate(compounds):
        print(f"\r  {i+1}/{len(compounds)}", end="")
        name = case['name']
        word1, word2, prompt = case['word1'], case['word2'], case['prompt']

        tokens = model.to_str_tokens(prompt)
        idx1 = find_token_index(tokens, word1)
        idx2 = find_token_index(tokens, word2)

        if idx1 is None or idx2 is None:
            unresolved.append((domain, name, word1, word2))
            print(f"\n  WARNING: could not locate '{word1}' / '{word2}' in {name}")
            continue

        # word2 attends back to word1 (e.g. "reader" -> "screen")
        target_idx = max(idx1, idx2)   # later token
        source_idx = min(idx1, idx2)   # earlier token

        # Only attention patterns are read — caching every activation wastes
        # a lot of memory on the larger models.
        with torch.no_grad():
            _, cache = model.run_with_cache(
                prompt, names_filter=lambda n: n.endswith("pattern")
            )

        for layer in range(model.cfg.n_layers):
            attention = cache["pattern", layer]   # [batch, heads, seq, seq]
            for head in range(model.cfg.n_heads):
                score = attention[0, head, target_idx, source_idx].item()
                results.append({
                    'compound': name,
                    'layer': layer,
                    'head': head,
                    'binding_score': round(score, 4),
                    'word1': word1,
                    'word2': word2,
                    'prompt': prompt,
                    'tokens': str(tokens),
                    'word1_idx': source_idx,
                    'word2_idx': target_idx,
                    'domain': domain,
                    'model': model_name,
                })

        del cache
    print()

    domain_df = pd.DataFrame(results)
    filename = f'{model_name}-{domain}.csv'
    domain_df.to_csv(output_dir / filename, index=False)
    all_results.append(domain_df)

    domain_counts[domain] = {
        'expected': len(compounds) * model.cfg.n_layers * model.cfg.n_heads,
        'written': len(domain_df),
        'file': filename,
    }
    print(f"  → {filename}  ({len(domain_df)} rows)")

results_df = pd.concat(all_results, ignore_index=True)

create_manifest_file(
    PROJECT_ROOT, output_dir, model_name, model,
    "binding", domain_counts, results_df, prompt_files,
)

if unresolved:
    print(f"\n⚠️  {len(unresolved)} compounds unresolved (skipped):")
    for d, n, w1, w2 in unresolved:
        print(f"    {d}/{n}: '{w1}' / '{w2}'")

print(f"\nSaved {len(results_df)} rows across {len(all_results)} domains → {output_dir}")
```

- [ ] **Step 3: Delete cell 10**

Use `NotebookEdit` with `cell_id`/index 10 and `edit_mode: delete`. This is the
hand-written manifest cell starting `output_dir = PROJECT_ROOT / 'results' /
'binding' / 'gpt2' / model_name`. `create_manifest_file` now writes that exact
filename with strictly more content.

- [ ] **Step 4: Verify structure and that the file is still valid JSON**

```bash
cd /Users/trishasalas/Repos/Research/tmlr
/opt/homebrew/Caskroom/miniconda/base/envs/mechinterp/bin/python -c "
import json
nb = json.load(open('notebooks/binding-gpt2.ipynb'))
print('cells:', len(nb['cells']))
src = ''.join(nb['cells'][9]['source'])
assert 'run_binding_sweep' not in src, 'old sweep call still present'
assert 'src.binding' not in src, 'still importing src.binding'
assert \"data' / 'binding'\" in src, 'not reading data/binding'
assert 'names_filter' in src, 'names_filter missing'
assert '\"binding\"' in src, 'battery_name not passed'
compiled = compile(src, 'cell9', 'exec')   # syntax check
print('cell 9: syntax OK, all assertions passed')
for i, c in enumerate(nb['cells']):
    s = ''.join(c['source']) if isinstance(c['source'], list) else c['source']
    print(i, c['cell_type'], repr(s.strip().splitlines()[0] if s.strip() else '')[:60])
"
```

Expected: `cells: 12`, `cell 9: syntax OK, all assertions passed`, and the
listing shows index 10 is now the `### Delete Model & Clear Cache` markdown.

- [ ] **Step 5: Confirm nothing outside the notebook changed**

```bash
git status --porcelain
git diff --stat -- src/
```

Expected: `src/` shows no diff from this task. `notebooks/binding-gpt2.ipynb`
is modified. (`src/binding.py`, `notebooks/elicitation-gpt2.ipynb` may already
appear modified from before this plan started — that is pre-existing, leave it.)

- [ ] **Step 6: Commit**

```bash
git add notebooks/binding-gpt2.ipynb
git commit -m "binding-gpt2: 5 YAML domains, manifest, per-domain CSVs

Battery logic moves into the notebook, matching entropy-gpt2. Output path
is literal instead of inferred from the model name. Caches only attention
patterns. Unresolved compounds are counted and surface as an expected vs
written mismatch in the manifest. src/binding.py unchanged."
```

---

### Task 4: Execute the battery on gpt2 and verify the outputs

Run the real cell source against the real model and check the artifacts.

**Files:**
- Read only: `notebooks/binding-gpt2.ipynb`
- Creates (as run output): `results/binding/gpt2/gpt2/{gpt2-*.csv, gpt2-binding.md}`
- Scratch: `<scratchpad>/run_binding_cell.py`

**Interfaces:**
- Consumes: cell 9 of `binding-gpt2.ipynb` (Task 3), `data/binding/*.yaml`
  (Task 1).
- Produces: five CSVs and one manifest under `results/binding/gpt2/gpt2/`.

- [ ] **Step 1: Write the runner**

Create `<scratchpad>/run_binding_cell.py`. It executes the notebook cell's
**actual source pulled from the .ipynb**, so what gets tested is the artifact
itself and cannot drift from it:

```python
import json
import sys
from pathlib import Path

import torch
from transformer_lens import HookedTransformer

PROJECT_ROOT = Path("/Users/trishasalas/Repos/Research/tmlr")
sys.path.insert(0, str(PROJECT_ROOT))

model_name = "gpt2"

nb = json.loads((PROJECT_ROOT / "notebooks" / "binding-gpt2.ipynb").read_text())
cell = nb["cells"][9]
source = "".join(cell["source"])
assert "Binding Battery" in source, "cell 9 is not the battery cell"

device = (
    "cuda" if torch.cuda.is_available()
    else "mps" if torch.backends.mps.is_available()
    else "cpu"
)
print(f"Loading {model_name} on {device} ...")
model = HookedTransformer.from_pretrained(model_name)
print(f"Layers: {model.cfg.n_layers}  Heads: {model.cfg.n_heads}")

exec(compile(source, "binding-gpt2.ipynb:cell9", "exec"), globals())
```

- [ ] **Step 2: Run it**

```bash
cd /Users/trishasalas/Repos/Research/tmlr
/opt/homebrew/Caskroom/miniconda/base/envs/mechinterp/bin/python \
  "/private/tmp/claude-501/-Users-trishasalas-Repos-Research-tmlr/35a30dac-d2d9-49c8-a191-050032d5453e/scratchpad/run_binding_cell.py"
```

Expected: five `--- Running <domain>: N compounds ---` blocks with N matching
44 / 53 / 42 / 44 / 44, then

```
Saved 32688 rows across 5 domains → .../results/binding/gpt2/gpt2
```

The row total is `227 × 12 layers × 12 heads = 32,688`. A smaller number means
compounds were skipped — cross-check against Task 2's audit; the counts must
agree.

- [ ] **Step 3: Verify the written artifacts**

```bash
cd /Users/trishasalas/Repos/Research/tmlr
/opt/homebrew/Caskroom/miniconda/base/envs/mechinterp/bin/python -c "
import pandas as pd
from pathlib import Path

d = Path('results/binding/gpt2/gpt2')
EXPECTED_COLS = ['compound','layer','head','binding_score','word1','word2',
                 'prompt','tokens','word1_idx','word2_idx','domain','model']
COUNTS = {'control':44,'accessibility':53,'medical':42,'legal':44,'finance':44}

total = 0
for dom, n in COUNTS.items():
    df = pd.read_csv(d / f'gpt2-{dom}.csv')
    assert list(df.columns) == EXPECTED_COLS, f'{dom}: columns {list(df.columns)}'
    assert df['domain'].unique().tolist() == [dom], f'{dom}: domain column wrong'
    assert df['model'].unique().tolist() == ['gpt2'], f'{dom}: model column wrong'
    assert df['layer'].max() == 11 and df['head'].max() == 11, f'{dom}: layer/head range'
    assert df['binding_score'].between(0, 1).all(), f'{dom}: score out of [0,1]'
    print(f'  {dom:15s} {df[\"compound\"].nunique():3d}/{n} compounds  {len(df):6d} rows')
    total += len(df)
print(f'\ntotal rows: {total}')
print((d / 'gpt2-binding.md').read_text())
"
```

Expected: every domain shows `N/N compounds`, total 32,688, and the printed
manifest has a **Domains** table with no ⚠️ markers, a `## Server` section, and
`Model name: gpt2`. Attention scores are softmax outputs, so the `[0, 1]` bound
is a genuine correctness check — a violation means the wrong tensor axis is
being indexed.

- [ ] **Step 4: Confirm the old hand-written manifest did not survive**

```bash
ls -la results/binding/gpt2/gpt2/
```

Expected: exactly six files — five `gpt2-*.csv` and one `gpt2-binding.md`. The
manifest must contain a `Git commit:` line (the hand-written version had none):

```bash
grep -c "Git commit:" results/binding/gpt2/gpt2/gpt2-binding.md
```

Expected: `1`.

- [ ] **Step 5: Report sizes and hand the commit decision to Trisha**

```bash
du -sh results/binding/gpt2/gpt2/
```

These are real experimental results, not test fixtures. Report the total size
and row counts and **ask whether to commit them** before running
`git add results/`. Do not commit result data unprompted.

---

## Follow-ups (not part of this plan)

- Apply the same cell to `binding-pythia.ipynb` (output path `.../pythia/...`)
  and `binding-olmo.ipynb` (output path `.../olmo/...`, plus `revision` and
  `hf_commit_sha` arguments as in `entropy-olmo.ipynb`).
- Once all three are migrated, delete the five arrays and `run_binding_sweep`
  from `src/binding.py`, keeping `find_token_index` and `run_single_compound`
  for `qk_ov.py`, `head_characterization.py`, and `d6_multihead_ablation.py`.
- `notebooks/elicitation-gpt2.ipynb` passes `GEN_KWARGS` as the 5th positional
  argument to `create_manifest_file`, where `src/manifest.py:6` now expects
  `battery_name` — and `src/manifest.py:7` raises `TypeError` on a dict there.
  That cell will fail when run. Separate fix.
