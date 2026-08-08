# Per-Battery Manifest Writers

**Date:** 2026-08-08
**Status:** Approved

## Problem

`create_manifest_file()` takes eight positional arguments of mixed types:

```python
create_manifest_file(PROJECT_ROOT, output_dir, model_name, model,
                     battery_name, domain_counts, results_df, prompt_files,
                     gen_kwargs=None, hf_commit_sha=None, revision=None)
```

All three elicitation notebooks pass `GEN_KWARGS` where `battery_name` belongs:

```python
create_manifest_file(
    PROJECT_ROOT, output_dir, model_name, model,
    GEN_KWARGS, domain_counts, results_df, prompt_files,
)
```

`src/manifest.py:7` catches this with an explicit `TypeError`, so the failure is
loud rather than silent — but it fires only at the *end* of a battery run, after
every prompt has been generated. On a 13B OLMo model that is a long wait for an
error that a signature could have made impossible.

The guard exists because the argument order already changed once. Nothing
prevents the next reorder from causing the same class of bug.

Two adjacent defects live in the same cells:

1. **`elicitation-gpt2.ipynb` writes to the wrong suite directory:**
   `results/elicitation/pythia/{model_name}` instead of `.../gpt2/...`. Four
   GPT-2 model directories currently sit under `pythia/` as a result.

2. **`elicitation-olmo.ipynb` cells 16–17 record provenance for the wrong
   model.** Cell 16 reassigns `model_name` to a hardcoded
   `"allenai/OLMo-2-1124-13B"` and hardcodes a 13B revision, overwriting the
   model selected in cell 9. Cell 17 reassigns `PROJECT_ROOT = Path.cwd().parent`
   (which breaks under Colab) and writes `{short_name}-commit-sha.md` into the
   13B directory. Running the notebook for the 7B still emits 13B provenance,
   filed under a model that run never loaded.

`entropy-olmo.ipynb` already does this correctly — `info =
model_info(f"allenai/{model_name}")` computed inline against the real
`model_name`, passed as `hf_commit_sha=info.sha, revision=revision`.

## Scope

### In scope

1. Restructure `src/manifest.py` into one private writer plus three
   per-battery public functions
2. Migrate all 7 notebook call sites
3. Fix `elicitation-gpt2.ipynb`'s output path
4. Fold `elicitation-olmo.ipynb`'s separate commit-sha file into the manifest
   and delete cells 16–17

### Out of scope

- **The misplaced `results/elicitation/pythia/gpt2*` directories.** The notebook
  is fixed so future runs land correctly; the existing committed data stays put.
  Moving it rewrites result provenance and is a separate decision.
- **`frequency-*.ipynb`** — these write no manifest today. No
  `write_frequency_manifest` until one is needed (YAGNI).
- **Manifest field content.** The body of the writer is unchanged; only the
  call surface changes.
- **Re-running any battery.** No results are regenerated.

## Design

### 1. `src/manifest.py`

The existing function body becomes private and keeps its signature verbatim:

```python
def _write_manifest(PROJECT_ROOT, output_dir, model_name, model, battery_name,
                    domain_counts, results_df, prompt_files,
                    gen_kwargs=None, hf_commit_sha=None, revision=None):
    ...   # body unchanged, minus the isinstance(battery_name, dict) guard
```

The `isinstance(battery_name, dict)` guard at lines 7–11 is removed. It exists to
catch a caller passing `gen_kwargs` into the `battery_name` slot; after this
change no public function has a `battery_name` slot, so the mistake is
unrepresentable and the guard is dead.

Three public writers:

```python
def write_elicitation_manifest(PROJECT_ROOT, output_dir, model_name, model,
                               domain_counts, results_df, prompt_files,
                               gen_kwargs, revision=None, hf_commit_sha=None):
    """Elicitation runs generate text, so gen_kwargs is required."""
    return _write_manifest(
        PROJECT_ROOT, output_dir, model_name, model, "elicitation",
        domain_counts, results_df, prompt_files,
        gen_kwargs=gen_kwargs, hf_commit_sha=hf_commit_sha, revision=revision)


def write_entropy_manifest(PROJECT_ROOT, output_dir, model_name, model,
                           domain_counts, results_df, prompt_files,
                           revision=None, hf_commit_sha=None):
    """Entropy is forward-pass only — no generation settings to record."""
    return _write_manifest(
        PROJECT_ROOT, output_dir, model_name, model, "entropy",
        domain_counts, results_df, prompt_files,
        hf_commit_sha=hf_commit_sha, revision=revision)


def write_binding_manifest(PROJECT_ROOT, output_dir, model_name, model,
                           domain_counts, results_df, prompt_files,
                           revision=None, hf_commit_sha=None):
    """Binding is forward-pass only — no generation settings to record."""
    return _write_manifest(
        PROJECT_ROOT, output_dir, model_name, model, "binding",
        domain_counts, results_df, prompt_files,
        hf_commit_sha=hf_commit_sha, revision=revision)
```

Two properties this buys, in order of weight:

- **There is no `battery_name` slot to misplace an argument into.** This is the
  actual fix for the bug in hand.
- **`gen_kwargs` is required for elicitation and absent from the other two.**
  A forward-pass battery cannot claim generation settings it never used, and an
  elicitation run cannot forget to record them.

All three accept `revision` / `hf_commit_sha`, because each battery has an OLMo
variant that needs them.

The old name is retained as a loud shim rather than deleted, so a stale Colab
copy fails with instructions instead of `ImportError`:

```python
def create_manifest_file(*args, **kwargs):
    raise TypeError(
        "create_manifest_file() has been replaced by per-battery writers. Use:\n"
        "  write_elicitation_manifest(...)  — takes gen_kwargs\n"
        "  write_entropy_manifest(...)\n"
        "  write_binding_manifest(...)"
    )
```

### 2. Notebook migrations

| notebook | change |
|---|---|
| `binding-gpt2` | → `write_binding_manifest`, drop the `"binding"` argument |
| `entropy-gpt2` | → `write_entropy_manifest`, drop `"entropy"` |
| `entropy-pythia` | → `write_entropy_manifest`, drop `"entropy"` |
| `entropy-olmo` | → `write_entropy_manifest`, drop `"entropy"`, keep `hf_commit_sha` / `revision` |
| `elicitation-pythia` | → `write_elicitation_manifest(..., gen_kwargs=GEN_KWARGS)` |
| `elicitation-gpt2` | same, **plus** output path `'pythia'` → `'gpt2'` |
| `elicitation-olmo` | same, **plus** `info = model_info(...)` inline, `revision` + `hf_commit_sha` passed, cells 16–17 deleted |

Each notebook's `from src.manifest import create_manifest_file` becomes an import
of the writer it uses.

### 3. `elicitation-olmo.ipynb` specifically

Mirror `entropy-olmo.ipynb` exactly. In the battery cell (index 12):

- Add `from huggingface_hub import model_info` to the cell's imports
- Immediately before the manifest call, add
  `info = model_info(f"allenai/{model_name}")`
- Call:

```python
write_elicitation_manifest(
    PROJECT_ROOT, output_dir, model_name, model,
    domain_counts, results_df, prompt_files,
    gen_kwargs=GEN_KWARGS, revision=revision, hf_commit_sha=info.sha,
)
```

`revision` is already in scope from cell 9 (`revision = OLMO_REVISIONS[model_name]`).

Then **delete cells 16 and 17**. Cell 16 defines only `info` and `short_name`,
both of which exist solely to serve cell 17; cell 17 is the file being replaced.
Nothing downstream references either name.

## Risks

- **All 7 notebooks change at once.** They sync to Colab, so a notebook opened in
  a Colab runtime from before this change will call `create_manifest_file` and
  hit the shim's `TypeError`. That is the intended failure — the message names
  the replacement — but it means pulling before re-running.

- **`elicitation-gpt2.ipynb` has uncommitted output-clearing in the working
  tree.** Those cleared outputs will be committed alongside this change. The
  diff is `execution_count` and `outputs` only, no code, so nothing is lost —
  but the commit will look larger than the code change.

- **The OLMo commit-sha files already on disk stay.** `results/elicitation/olmo/
  {model}/{model}-commit-sha.md` files written by the old cells 16–17 are not
  deleted, and some may describe the wrong model. They are not regenerated by
  this change. Auditing them is a separate task.

- **The `isinstance(battery_name, dict)` guard is removed.** If any un-migrated
  caller exists outside the 7 notebooks it would lose that specific error
  message — but a repo-wide grep found `create_manifest_file` referenced only in
  `src/manifest.py` itself and the 7 notebooks, and the shim covers those.
