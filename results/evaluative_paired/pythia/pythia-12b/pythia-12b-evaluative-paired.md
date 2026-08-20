# Paired evaluative run manifest

- Run time (UTC): 2026-08-20T22:59:16.376565+00:00
- Git commit: `2a9029ac216e6b79131329dc75e48851cff78323`
- Working tree dirty at run time: `True`
- Battery: `data/evaluative_paired.yaml`
- Battery SHA-256: `e495f5ce0af138484b7d7f34ecf4f467d5fbe6e918f2a165a78b52eddd7e75de`
- Result CSV: `results/evaluative_paired/pythia/pythia-12b/pythia-12b-evaluative-paired.csv`
- Result SHA-256: `89e3dcea16863eec39fe68de77df91be538d5c1b56294cab2d5e867298284d82`

## Model

- Requested model: `pythia-12b`
- Frozen model key: `pythia-12b`
- Suite: `pythia`
- Scale: `12B`
- Parameter dtype: `torch.float32`
- Device: `cuda:0`
- Layers: 36
- Heads: 40
- Hidden size: 5120
- Vocabulary size: 50688
- Requested revision: `main`
- Resolved Hugging Face commit: `bb1e3e710cdf6b524461d543cfb5ba773f0a81b6`

## Generation

- `do_sample=False`
- `max_new_tokens=100`
- Raw continuation preserved without stripping leading whitespace
- Expected rows: 16
- Written rows: 16

## Environment

- Python: `3.12.13`
- torch: `2.11.0+cu128`
- transformers: `4.57.6`
- transformer-lens: `2.18.0`
