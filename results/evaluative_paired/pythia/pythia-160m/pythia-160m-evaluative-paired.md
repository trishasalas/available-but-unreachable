# Paired evaluative run manifest

- Run time (UTC): 2026-08-20T22:05:05.939079+00:00
- Git commit: `91a2c3a79b62322465daffa0a9fec0bee92016d0`
- Working tree dirty at run time: `True`
- Battery: `data/evaluative_paired.yaml`
- Battery SHA-256: `e495f5ce0af138484b7d7f34ecf4f467d5fbe6e918f2a165a78b52eddd7e75de`
- Result CSV: `results/evaluative_paired/pythia/pythia-160m/pythia-160m-evaluative-paired.csv`
- Result SHA-256: `b748dd2bd99538c1a551b96058f5b00de3b46b2486ef04dece8c0814256db0ee`

## Model

- Requested model: `pythia-160m`
- Frozen model key: `pythia-160m`
- Suite: `pythia`
- Scale: `160M`
- Parameter dtype: `torch.float32`
- Device: `cpu`
- Layers: 12
- Heads: 12
- Hidden size: 768
- Vocabulary size: 50304
- Requested revision: `main`

## Generation

- `do_sample=False`
- `max_new_tokens=100`
- Raw continuation preserved without stripping leading whitespace
- Expected rows: 16
- Written rows: 16

## Environment

- Python: `3.11.14`
- torch: `2.10.0`
- transformers: `4.57.6`
- transformer-lens: `2.18.0`
