# Paired evaluative run manifest

- Run time (UTC): 2026-08-20T22:32:21.909368+00:00
- Git commit: `32b1ff9db7377ed1aa869daf987bb7bce4d83e43`
- Working tree dirty at run time: `True`
- Battery: `data/evaluative_paired.yaml`
- Battery SHA-256: `e495f5ce0af138484b7d7f34ecf4f467d5fbe6e918f2a165a78b52eddd7e75de`
- Result CSV: `results/evaluative_paired/gpt2/gpt2-medium/gpt2-medium-evaluative-paired.csv`
- Result SHA-256: `f35cb00997af4e13e171432da63dc4e391594124ecefe5637b6de596ebcd43f9`

## Model

- Requested model: `gpt2-medium`
- Frozen model key: `gpt2-medium`
- Suite: `gpt2`
- Scale: `355M`
- Parameter dtype: `torch.float32`
- Device: `cuda:0`
- Layers: 24
- Heads: 16
- Hidden size: 1024
- Vocabulary size: 50257
- Requested revision: `main`
- Resolved Hugging Face commit: `6dcaa7a952f72f9298047fd5137cd6e4f05f41da`

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
