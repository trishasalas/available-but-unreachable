# Paired evaluative run manifest

- Run time (UTC): 2026-08-20T22:39:41.205965+00:00
- Git commit: `42aed95ddc182b6d00fd648317ccb18e5a39163d`
- Working tree dirty at run time: `True`
- Battery: `data/evaluative_paired.yaml`
- Battery SHA-256: `e495f5ce0af138484b7d7f34ecf4f467d5fbe6e918f2a165a78b52eddd7e75de`
- Result CSV: `results/evaluative_paired/gpt2/gpt2-xl/gpt2-xl-evaluative-paired.csv`
- Result SHA-256: `d381eee32e706bdf91186a53ec606fc77def2c9fc772695aa97b26d8633fb325`

## Model

- Requested model: `gpt2-xl`
- Frozen model key: `gpt2-xl`
- Suite: `gpt2`
- Scale: `1.5B`
- Parameter dtype: `torch.float32`
- Device: `cuda:0`
- Layers: 48
- Heads: 25
- Hidden size: 1600
- Vocabulary size: 50257
- Requested revision: `main`
- Resolved Hugging Face commit: `15ea56dee5df4983c59b2538573817e1667135e2`

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
