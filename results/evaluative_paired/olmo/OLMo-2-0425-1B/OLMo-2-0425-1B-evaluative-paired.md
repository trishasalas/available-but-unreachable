# Paired evaluative run manifest

- Run time (UTC): 2026-08-20T22:46:25.034831+00:00
- Git commit: `c68b8e6c4213f93ef713cda7ddc204fe70bd0223`
- Working tree dirty at run time: `True`
- Battery: `data/evaluative_paired.yaml`
- Battery SHA-256: `e495f5ce0af138484b7d7f34ecf4f467d5fbe6e918f2a165a78b52eddd7e75de`
- Result CSV: `results/evaluative_paired/olmo/OLMo-2-0425-1B/OLMo-2-0425-1B-evaluative-paired.csv`
- Result SHA-256: `afa46b26fb5eb50a61e63d1a53e5c1d9507135aeb056e531d57e5acb5fee18c6`

## Model

- Requested model: `OLMo-2-0425-1B`
- Frozen model key: `OLMo-2-0425-1B`
- Suite: `olmo`
- Scale: `1B`
- Parameter dtype: `torch.float32`
- Device: `cuda:0`
- Layers: 16
- Heads: 16
- Hidden size: 2048
- Vocabulary size: 100352
- Requested revision: `stage1-step1907359-tokens4001B`
- Resolved Hugging Face commit: `9d3e43659f00c17e6da23cf32333afd1fc39fa1a`

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
