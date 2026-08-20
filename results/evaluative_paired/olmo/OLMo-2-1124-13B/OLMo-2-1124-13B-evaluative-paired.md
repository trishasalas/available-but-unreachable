# Paired evaluative run manifest

- Run time (UTC): 2026-08-20T23:45:37.176993+00:00
- Git commit: `204f3a3cd17c472e2c0b267eca73c5f764110b53`
- Working tree dirty at run time: `True`
- Battery: `data/evaluative_paired.yaml`
- Battery SHA-256: `e495f5ce0af138484b7d7f34ecf4f467d5fbe6e918f2a165a78b52eddd7e75de`
- Result CSV: `results/evaluative_paired/olmo/OLMo-2-1124-13B/OLMo-2-1124-13B-evaluative-paired.csv`
- Result SHA-256: `402c3c9b6280ce5ced36a1c786e97973ebbed8fe85d67e3035f5f9ef4b97a034`

## Model

- Requested model: `OLMo-2-1124-13B`
- Frozen model key: `OLMo-2-1124-13B`
- Suite: `olmo`
- Scale: `13B`
- Parameter dtype: `torch.float32`
- Device: `cuda:0`
- Layers: 40
- Heads: 40
- Hidden size: 5120
- Vocabulary size: 100352
- Requested revision: `stage1-step596057-tokens5001B`
- Resolved Hugging Face commit: `08d2aca2e28ab67ad859793f76ef5c923e94ac11`

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
