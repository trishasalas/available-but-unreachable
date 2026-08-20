# Paired evaluative run manifest

- Run time (UTC): 2026-08-20T22:35:59.462548+00:00
- Git commit: `5c1b10a043cd835b2473a0636c60ae6b1237b65b`
- Working tree dirty at run time: `True`
- Battery: `data/evaluative_paired.yaml`
- Battery SHA-256: `e495f5ce0af138484b7d7f34ecf4f467d5fbe6e918f2a165a78b52eddd7e75de`
- Result CSV: `results/evaluative_paired/gpt2/gpt2-large/gpt2-large-evaluative-paired.csv`
- Result SHA-256: `42bd302943801a975a6344ca0cc196d29f7e4aef2095c669bddc8576c4880f22`

## Model

- Requested model: `gpt2-large`
- Frozen model key: `gpt2-large`
- Suite: `gpt2`
- Scale: `774M`
- Parameter dtype: `torch.float32`
- Device: `cuda:0`
- Layers: 36
- Heads: 20
- Hidden size: 1280
- Vocabulary size: 50257
- Requested revision: `main`
- Resolved Hugging Face commit: `32b71b12589c2f8d625668d2335a01cac3249519`

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
