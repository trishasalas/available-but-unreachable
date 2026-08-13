# Effective-binding experiment notebooks

These notebooks follow the setup, model-selection, model-loading, result-saving,
Git commit, and memory-cleanup conventions of the existing Paper 2 notebooks.
They are additions: they do not replace the original binding notebooks.

## Files

- `effective-binding-pythia.ipynb`
- `effective-binding-gpt2.ipynb`
- `effective-binding-olmo.ipynb`
- `effective-binding-analysis.ipynb`
- `frequency-head-ablation-pythia.ipynb`

## Recommended first run

1. Put all five notebooks in the project's `notebooks/` folder.
2. Open `effective-binding-pythia.ipynb`.
3. Leave `model_name = "pythia-160m"` and
   `PROMPT_CONDITION = "natural"` unchanged.
4. Run the cells from top to bottom.
5. Confirm the final check says that expected rows equal written rows and that
   every compound was resolved.
6. Open `effective-binding-analysis.ipynb`, leave `CONDITION = "natural"`, and
   run it from top to bottom.

That small-model run verifies the full workflow before using larger models.

## Uniform-prompt replication

In an effective-binding model notebook, change only:

```python
PROMPT_CONDITION = "uniform"
```

Rerun the measurement cell. Natural and uniform outputs are written to separate
folders and cannot overwrite one another. Then set `CONDITION = "uniform"` in
the analysis notebook and run it again.

## What the measurements mean

- `binding_score` and `attention_weight`: the original raw attention measure.
- `ov_write_norm`: the magnitude of the source token's head-specific OV write.
- `weighted_ov_norm`: attention multiplied by the OV-write magnitude.
- `relative_weighted_ov_norm`: the weighted write divided by the target token's
  residual-stream norm.

For OLMo, the norm-aware quantity is measured immediately before OLMo's
attention-branch RMS normalization. It is not labeled as full ALTI information
flow.

## Causal screen

Run `frequency-head-ablation-pythia.ipynb` only after the corresponding Pythia
effective-binding file and analysis notebook have completed. It:

- reads five heads selected using half of the compounds;
- ablates them on the untouched half;
- compares them with five random heads matched by layer; and
- saves KL-divergence effects.

This first causal screen tests whether the selected heads affect the prediction
distribution. It does not by itself establish a change in answer correctness.

## Suggested run order after the smoke test

1. Pythia models, natural prompts.
2. GPT-2 models, natural prompts.
3. OLMo models, natural prompts.
4. Analysis of all natural-prompt results.
5. Uniform-prompt replication.
6. Pythia held-out ablation, beginning with 160M.

The model notebooks default to the 49 accessibility compounds because those are
the compounds matched to the project's frozen frequency table.
