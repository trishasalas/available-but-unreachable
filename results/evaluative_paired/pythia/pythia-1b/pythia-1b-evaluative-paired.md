# Paired evaluative run manifest

- Run time (UTC): 2026-08-20T22:23:00.303193+00:00
- Git commit: `fe1ff0b44ecc9f2453b37be4582adfd965ae4e1a`
- Working tree dirty at run time: `True`
- Battery: `data/evaluative_paired.yaml`
- Battery SHA-256: `e495f5ce0af138484b7d7f34ecf4f467d5fbe6e918f2a165a78b52eddd7e75de`
- Result CSV: `results/evaluative_paired/pythia/pythia-1b/pythia-1b-evaluative-paired.csv`
- Result SHA-256: `9165bd1988db24fc7024e0b515aa444b61e2db9594825c0a92655f15a260242f`

## Model

- Requested model: `pythia-1b`
- Frozen model key: `pythia-1b`
- Suite: `pythia`
- Scale: `1B`
- Parameter dtype: `torch.float32`
- Device: `cuda:0`
- Layers: 16
- Heads: 8
- Hidden size: 2048
- Vocabulary size: 50304
- Requested revision: `main`
- Resolved Hugging Face commit: `f73d7dcc545c8bd326d8559c8ef84ffe92fea6b2`

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
