# Paired evaluative run manifest

- Run time (UTC): 2026-08-20T22:27:38.929465+00:00
- Git commit: `47ec6dffbd9bcfbcd60b7759131fcee6fb3a733c`
- Working tree dirty at run time: `True`
- Battery: `data/evaluative_paired.yaml`
- Battery SHA-256: `e495f5ce0af138484b7d7f34ecf4f467d5fbe6e918f2a165a78b52eddd7e75de`
- Result CSV: `results/evaluative_paired/gpt2/gpt2/gpt2-evaluative-paired.csv`
- Result SHA-256: `a1cb13e8c8de261a12f2b435a4038db7afb7de833a058e1b8cba5527159f7fd9`

## Model

- Requested model: `gpt2`
- Frozen model key: `gpt2`
- Suite: `gpt2`
- Scale: `124M`
- Parameter dtype: `torch.float32`
- Device: `cuda:0`
- Layers: 12
- Heads: 12
- Hidden size: 768
- Vocabulary size: 50257
- Requested revision: `main`
- Resolved Hugging Face commit: `607a30d783dfa663caf39e06633721c8d4cfcd7e`

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
