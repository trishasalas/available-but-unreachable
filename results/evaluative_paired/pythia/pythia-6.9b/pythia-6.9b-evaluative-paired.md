# Paired evaluative run manifest

- Run time (UTC): 2026-08-20T22:52:16.260412+00:00
- Git commit: `8e816cc6eec5f74258e1d30ab59941317a9db10a`
- Working tree dirty at run time: `True`
- Battery: `data/evaluative_paired.yaml`
- Battery SHA-256: `e495f5ce0af138484b7d7f34ecf4f467d5fbe6e918f2a165a78b52eddd7e75de`
- Result CSV: `results/evaluative_paired/pythia/pythia-6.9b/pythia-6.9b-evaluative-paired.csv`
- Result SHA-256: `310c149210c17e90c464611b55054f0874eb8456d95e05b810b2b2f9a4973980`

## Model

- Requested model: `pythia-6.9b`
- Frozen model key: `pythia-6.9b`
- Suite: `pythia`
- Scale: `6.9B`
- Parameter dtype: `torch.float32`
- Device: `cuda:0`
- Layers: 32
- Heads: 32
- Hidden size: 4096
- Vocabulary size: 50432
- Requested revision: `main`
- Resolved Hugging Face commit: `c0e3eee36dc47af0c49f361c74cfe459c09f7f23`

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
