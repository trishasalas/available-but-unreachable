# Paired evaluative run manifest

- Run time (UTC): 2026-08-20T23:24:56.394379+00:00
- Git commit: `5953dc4410a698ed0b9d836d382ab2a2d30b661f`
- Working tree dirty at run time: `True`
- Battery: `data/evaluative_paired.yaml`
- Battery SHA-256: `e495f5ce0af138484b7d7f34ecf4f467d5fbe6e918f2a165a78b52eddd7e75de`
- Result CSV: `results/evaluative_paired/olmo/OLMo-2-1124-7B/OLMo-2-1124-7B-evaluative-paired.csv`
- Result SHA-256: `9ad2957f6aa3dcf24bdf3c710c6b0a30bb6210a69b0fc6df9980cbb9e9091c18`

## Model

- Requested model: `OLMo-2-1124-7B`
- Frozen model key: `OLMo-2-1124-7B`
- Suite: `olmo`
- Scale: `7B`
- Parameter dtype: `torch.float32`
- Device: `cuda:0`
- Layers: 32
- Heads: 32
- Hidden size: 4096
- Vocabulary size: 100352
- Requested revision: `stage1-step928646-tokens3896B`
- Resolved Hugging Face commit: `c0371f4281bf2376207646c6b62ddc6c442c7577`

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
